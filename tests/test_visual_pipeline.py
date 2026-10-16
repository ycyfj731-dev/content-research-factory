"""Offline regression tests: no credentials, network, or image-generation spend."""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import struct
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'projects/youtube/001-therapy-speak/visual-batch-v1'
spec = importlib.util.spec_from_file_location('visual_batch', ROOT / 'batch.py')
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)

class VisualPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name) / 'batch'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('outputs', '__pycache__'))
        for name in batch.read(ROOT / 'source-lock.json')['files']:
            shutil.copyfile(ROOT.parent / name, self.root.parent / name)

    def save(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding='utf-8')

    def ready(self):
        units, contracts = batch.validate(self.root)
        c = contracts['units'][0]
        c['status'] = 'READY_FOR_REVIEW'
        c['elements'] = [dict(kind='hold', description='Hold empty white frame; test fixture only', sentence_id=s['id'], quote=s['text'], appears_at=s['id']) for s in units[0]['sentences']]
        self.save('contracts.json', contracts)
        return contracts

    def approved(self):
        self.ready()
        records = batch.compile_records(self.root)[:1]
        r = records[0]
        self.save('approvals.json', dict(compiler_sha256=batch.text_digest(self.root/'batch.py'), style_sha256=batch.digest(batch.STYLE), units={r['unit_id']:dict(reviewer='TEST ONLY', reviewed_at='test', decision='APPROVED', semantic_review='PASS', contract_sha256=r['contract_sha256'], prompt_sha256=r['prompt_sha256'])}))
        return records

    def test_real_source_coverage_and_lossless_sentence_spans(self):
        units, _ = batch.validate(self.root)
        self.assertEqual(len(units), 34)
        sentences = [s for u in units for s in u['sentences']]
        self.assertEqual(len(sentences), 184)
        self.assertEqual(len({s['paragraph'] for s in sentences}), 150)
        lines = (self.root.parent/'episode-001-v6.1-production-locked.md').read_text(encoding='utf-8').splitlines()
        for s in sentences:
            self.assertEqual(lines[s['source_line']-1][s['start']:s['end']], s['text'])

    def test_deterministic_drafts_never_become_prompts(self):
        a = batch.compile_records(self.root)
        self.assertEqual(a, batch.compile_records(self.root))
        self.assertEqual(sum(r['status']=='BLOCKED_DRAFT' for r in a), 30)
        self.assertEqual([r['unit_id'] for r in a if r['status']=='PENDING_APPROVAL'], ['VC-27','VC-28','VC-29','VC-30'])
        self.assertTrue(all((r['prompt'] is None) == (r['status']=='BLOCKED_DRAFT') for r in a))
        with self.assertRaises(batch.GateError): batch.approval_gate(self.root, a)

    def test_source_tamper(self):
        p = self.root.parent/'episode-001-v6.1-production-locked.md'
        p.write_bytes(p.read_bytes()+b'changed')
        with self.assertRaises(batch.GateError): batch.validate(self.root)

    def test_trace_tamper_even_if_hash_relocked(self):
        name='episode-001-v6.1-exact-visual-traceability.md'
        p=self.root.parent/name
        p.write_text(p.read_text(encoding='utf-8').replace('**P001** Apparently', '**P001** Unrelated'),encoding='utf-8')
        lock=batch.read(self.root/'source-lock.json'); lock['files'][name]=batch.digest(p.read_bytes()); self.save('source-lock.json',lock)
        with self.assertRaises(batch.GateError): batch.validate(self.root)

    def test_contract_negative_cases(self):
        base=self.ready()
        for change in ('missing_unit','duplicate_unit','missing_sentence','unrelated','quote','early','mandatory_dog','missing_element'):
            with self.subTest(change=change):
                c=json.loads(json.dumps(base)); first=c['units'][0]
                if change=='missing_unit': c['units'].pop()
                elif change=='duplicate_unit': c['units'][1]=first
                elif change=='missing_sentence': first['sentence_ids'].pop()
                elif change=='unrelated': first['elements'][0]['sentence_id']='P150-S01'
                elif change=='quote': first['elements'][0]['quote']='a random astronaut'
                elif change=='early': first['elements'][0]['appears_at']='P000-S01'
                elif change=='mandatory_dog': first['border_collie']='required'
                else: first['elements'].pop()
                self.save('contracts.json',c)
                with self.assertRaises(batch.GateError): batch.validate(self.root)

    def test_exact_approval_and_stale_scene(self):
        records=self.approved(); batch.approval_gate(self.root,records)
        c=batch.read(self.root/'contracts.json'); c['units'][0]['elements'][0]['description']='Random person'
        self.save('contracts.json',c)
        with self.assertRaises(batch.GateError): batch.approval_gate(self.root,batch.compile_records(self.root)[:1])

    def test_compiler_change_invalidates_approval(self):
        records=self.approved()
        with (self.root/'batch.py').open('a') as f: f.write('\n# changed\n')
        with self.assertRaises(batch.GateError): batch.approval_gate(self.root,records)

    def test_qa_all_gates_and_image_identity(self):
        records=self.approved(); r=records[0]
        (self.root/'outputs').mkdir(); image=self.root/'outputs/frame.png'
        def chunk(kind, data):
            return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
        image.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',320,180,8,0,0,0,0))+chunk(b'IDAT',zlib.compress((b'\x00'+b'\xff'*320)*180))+chunk(b'IEND',b''))
        report={r['unit_id']:dict(reviewer='TEST ONLY',reviewed_at='test',prompt_sha256=r['prompt_sha256'],path='outputs/frame.png',image_sha256=batch.digest(image.read_bytes()),gates={g:'PASS' for g in batch.GATES})}
        batch.qa_gate(self.root,records,report)
        for gate in batch.GATES:
            report[r['unit_id']]['gates'][gate]='FAIL'
            with self.assertRaises(batch.GateError): batch.qa_gate(self.root,records,report)
            report[r['unit_id']]['gates'][gate]='PASS'
        image.write_bytes(b'changed')
        with self.assertRaises(batch.GateError): batch.qa_gate(self.root,records,report)

    def test_non_image_cannot_pass_qa(self):
        with self.assertRaises(batch.GateError): batch.image_gate(b'not an image')

    def test_cross_platform_line_endings(self):
        for name in batch.read(self.root/'source-lock.json')['files']:
            p=self.root.parent/name
            p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
        self.assertEqual(len(batch.compile_records(self.root)),34)

    def test_legacy_prompt_is_never_loaded(self):
        before=batch.compile_records(self.root)
        (self.root/'prompt.txt').write_text('MAKE A COLOR GRID OF RANDOM PEOPLE')
        self.assertEqual(before,batch.compile_records(self.root))

    def test_even_approved_generate_never_calls_provider(self):
        self.approved()
        result=subprocess.run([sys.executable,str(self.root/'batch.py'),'--mode','generate','--shots','VC-01'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('Provider disabled',result.stdout)
        self.assertFalse((self.root/'outputs').exists())

    def test_cli_fails_closed(self):
        for args in (['--mode','generate'],['--shots','CH1-01'],['--shots','VC-01','VC-01'],['--mode','qa']):
            result=subprocess.run([sys.executable,str(self.root/'batch.py'),*args],capture_output=True,text=True)
            self.assertEqual(result.returncode,2,result.stdout)
            self.assertIn('BLOCKED',result.stdout)
        self.assertFalse((self.root/'outputs').exists())

if __name__=='__main__': unittest.main()
