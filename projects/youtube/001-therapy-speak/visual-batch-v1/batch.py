#!/usr/bin/env python3
"""Offline, fail-closed visual compiler. Never calls a paid provider."""
import argparse
import hashlib
import json
import pathlib
import re
import struct
import zlib

P = pathlib.Path(__file__).resolve().parent
STYLE = 'ONE continuous 16:9 editorial line drawing, black ink on white. No color, photography, collage, grid, panels, PPT, slides, readable text, random people or fabricated evidence. Border collie optional, never mandatory.'
GATES = ('narration_fit', 'sentence_timing', 'style_match', 'single_frame', 'anti_ppt', 'no_unapproved_people', 'no_fabricated_evidence', 'video_usability')

class GateError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise GateError(message)

def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(value).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def text_digest(path):
    # Git checkouts may use CRLF. Only normalize line endings, never prose.
    return digest(path.read_bytes().replace(b'\r\n', b'\n'))

def source_units(root=P):
    source = root.parent / 'episode-001-v6.1-production-locked.md'
    trace = root.parent / 'episode-001-v6.1-exact-visual-traceability.md'
    chapter, paragraphs = 0, []
    for line_no, line in enumerate(source.read_text(encoding='utf-8').splitlines(), 1):
        if line.startswith('## '):
            chapter += 1
        elif chapter and line.strip() and not line.startswith('#'):
            paragraphs.append((chapter, line_no, line))
    require(len(paragraphs) == 150 and chapter == 6, 'Expected 150 paragraphs / six chapters')
    blocks = re.split(r'^## (VC-\d+)', trace.read_text(encoding='utf-8'), flags=re.M)
    units, covered = [], []
    for uid, block in zip(blocks[1::2], blocks[2::2]):
        header = re.match(r' · Chapter (\d+) · P(\d+)–P(\d+) · lines (\d+)–(\d+)', block)
        require(header is not None, 'Invalid trace header')
        ch, start, end, first, last = map(int, header.groups())
        quoted = re.findall(r'^> \*\*P(\d+)\*\* (.+)$', block, re.M)
        require([int(n) for n, _ in quoted] == list(range(start, end + 1)), 'Trace range mismatch')
        require((first, last) == (paragraphs[start-1][1], paragraphs[end-1][1]), 'Source line mismatch')
        sentences = []
        for n, quote in quoted:
            n = int(n)
            require(paragraphs[n-1][0] == ch and paragraphs[n-1][2] == quote, 'Verbatim trace mismatch')
            covered.append(n)
            parts = re.split(r'(?<=[.!?])(?=\s+[A-Z"*])', quote)
            offset = 0
            for index, part in enumerate(parts, 1):
                sentences.append(dict(id=f'P{n:03d}-S{index:02d}', paragraph=n, source_line=paragraphs[n-1][1], start=offset, end=offset+len(part), text=part))
                offset += len(part)
        units.append(dict(id=uid, chapter=ch, sentences=sentences))
    require(covered == list(range(1, 151)), 'Coverage gap, overlap or reordering')
    require([u['id'] for u in units] == [f'VC-{n:02d}' for n in range(1, 35)], 'Expected 34 ordered units')
    return units

def validate(root=P):
    lock = read(root / 'source-lock.json')
    require(lock['version'] == 'V6.1/34', 'Wrong source version')
    require(set(lock['files']) == {'episode-001-v6.1-production-locked.md', 'episode-001-v6.1-exact-visual-traceability.md'}, 'Missing source lock')
    for name, expected in lock['files'].items():
        require(text_digest(root.parent / name) == expected, 'Locked source changed: ' + name)
    units = source_units(root)
    contracts = read(root / 'contracts.json')
    require(contracts['version'] == 'V6.1/34', 'Wrong contract version')
    require([c['unit_id'] for c in contracts['units']] == [u['id'] for u in units], 'Contract coverage mismatch')
    for unit, contract in zip(units, contracts['units']):
        ids = [s['id'] for s in unit['sentences']]
        require(contract['sentence_ids'] == ids, 'Sentence coverage mismatch')
        require(contract['status'] in ('DRAFT', 'READY_FOR_REVIEW'), 'Invalid status')
        require(contract['border_collie'] in ('absent', 'optional'), 'Collie cannot be mandatory')
        if contract['status'] == 'DRAFT':
            require(not contract['elements'], 'Draft elements must be submitted for review')
            continue
        require(bool(contract['elements']), 'Empty visual task')
        seen = set()
        for element in contract['elements']:
            require(element['kind'] in ('object', 'action', 'person', 'metaphor', 'hold'), 'Invalid element kind')
            require(element['description'].strip(), 'Empty description')
            require(element['sentence_id'] in ids, 'Unrelated sentence')
            sentence = next(s for s in unit['sentences'] if s['id'] == element['sentence_id'])
            require(element['quote'] and element['quote'] in sentence['text'], 'Unsupported quote')
            require(element['appears_at'] == element['sentence_id'], 'Premature visual reveal')
            seen.add(element['sentence_id'])
        require(seen == set(ids), 'Every sentence needs an element or explicit hold')
    return units, contracts

def compile_records(root=P):
    units, contracts = validate(root)
    records = []
    for unit, contract in zip(units, contracts['units']):
        prompt = None
        if contract['status'] == 'READY_FOR_REVIEW':
            prompt = STYLE + '\nTask candidate; quoted narration is context, never screen text:\n' + json.dumps(contract, ensure_ascii=False, sort_keys=True)
        records.append(dict(unit_id=unit['id'], contract_sha256=digest(contract), sentences=unit['sentences'], prompt=prompt, prompt_sha256=digest(prompt) if prompt else None, status='PENDING_APPROVAL' if prompt else 'BLOCKED_DRAFT'))
    return records

def approval_gate(root, records):
    approval = read(root / 'approvals.json')
    require(approval.get('compiler_sha256') == text_digest(root / 'batch.py'), 'Compiler not approved or changed')
    require(approval.get('style_sha256') == digest(STYLE), 'Style not approved or changed')
    for record in records:
        entry = approval.get('units', {}).get(record['unit_id'], {})
        require(record['prompt'] is not None, 'Draft cannot generate')
        require(entry.get('reviewer') and entry.get('reviewed_at') and entry.get('decision') == 'APPROVED', 'Missing editorial approval')
        require(all(entry.get(k) == record[k] for k in ('contract_sha256', 'prompt_sha256')), 'Stale approval')
        require(entry.get('semantic_review') == 'PASS', 'Scene relevance / people / evidence review required')

def image_gate(raw):
    """Validate a bounded, non-interlaced 16:9 PNG; semantic QA remains human."""
    require(raw.startswith(b'\x89PNG\r\n\x1a\n'), 'QA requires a PNG image')
    offset, chunks = 8, []
    while offset < len(raw):
        require(offset + 12 <= len(raw), 'Truncated PNG')
        size = struct.unpack('>I', raw[offset:offset+4])[0]
        kind = raw[offset+4:offset+8]
        data = raw[offset+8:offset+8+size]
        require(offset + size + 12 <= len(raw), 'Truncated PNG chunk')
        crc = struct.unpack('>I', raw[offset+8+size:offset+12+size])[0]
        require(zlib.crc32(kind + data) == crc, 'Invalid PNG checksum')
        chunks.append((kind, data))
        offset += size + 12
    require(chunks and chunks[0][0] == b'IHDR' and len(chunks[0][1]) == 13, 'Missing PNG header')
    require(chunks[-1] == (b'IEND', b'') and sum(k == b'IHDR' for k, _ in chunks) == 1, 'Invalid PNG structure')
    w, h, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', chunks[0][1])
    require(320 <= w <= 8192 and 180 <= h <= 4608 and w * 9 == h * 16, 'Expected bounded 16:9 image')
    require(depth == 8 and color in (0, 2, 4, 6) and (compression, filtering, interlace) == (0, 0, 0), 'Unsupported PNG encoding')
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[color]
    expected = (w * channels + 1) * h
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(b''.join(d for k, d in chunks if k == b'IDAT'), expected + 1)
    require(len(pixels) == expected and decoder.eof and not decoder.unused_data, 'Invalid PNG pixels')
    require(all(pixels[i] <= 4 for i in range(0, expected, w * channels + 1)), 'Invalid PNG row filter')

def qa_gate(root, records, report):
    approval_gate(root, records)
    require(set(report) == {r['unit_id'] for r in records}, 'QA coverage mismatch')
    for record in records:
        review = report[record['unit_id']]
        require(review.get('reviewer') and review.get('reviewed_at'), 'QA reviewer required')
        require(review.get('prompt_sha256') == record['prompt_sha256'], 'QA prompt mismatch')
        path = (root / review['path']).resolve()
        require(path.is_relative_to((root / 'outputs').resolve()) and path.is_file(), 'Invalid image artifact')
        require(digest(path.read_bytes()) == review.get('image_sha256'), 'Image changed after review')
        image_gate(path.read_bytes())
        require(all(review.get('gates', {}).get(g) == 'PASS' for g in GATES), 'All QA gates must pass')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['dry-run', 'validate', 'generate', 'qa'], default='dry-run')
    parser.add_argument('--shots', nargs='*', default=[])
    parser.add_argument('--qa-report', type=pathlib.Path)
    args = parser.parse_args()
    try:
        records = compile_records()
        require(len(args.shots) == len(set(args.shots)), 'Duplicate shot IDs')
        require(set(args.shots) <= {r['unit_id'] for r in records}, 'Unknown shot ID')
        selected = [r for r in records if not args.shots or r['unit_id'] in args.shots]
        if args.mode == 'generate':
            approval_gate(P, selected)
            raise GateError('Provider disabled: reviewed adapter and explicit paid-run authorization still required')
        if args.mode == 'qa':
            require(args.qa_report is not None, '--qa-report required')
            qa_gate(P, selected, read(args.qa_report))
        if args.mode == 'dry-run':
            output = P / 'outputs'
            output.mkdir(exist_ok=True)
            (output / 'prompt_manifest.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(dict(mode=args.mode, units=len(selected), statuses=[r['status'] for r in selected], actual_images_generated=0, production_ready=False)))
        return 0
    except (GateError, KeyError, TypeError, ValueError, OSError, zlib.error, struct.error) as exc:
        print(json.dumps(dict(status='BLOCKED', reason=str(exc))))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
