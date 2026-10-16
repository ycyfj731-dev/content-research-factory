#!/usr/bin/env python3
"""Deterministic review cut. Uses the real locked audio; never synthesizes media."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
EPISODE = HERE.parent
W, H, FPS = 1920, 1080, 24
START, END = 640.546, 721.556
AUDIO_SHA = '415fe806af8f9f7a14222520629b0941b0a28d603c39c593c20b933c8605c175'
AUDIO_URL = ('https://github.com/ycyfj731-dev/content-research-factory/releases/download/'
             'episode001-audio-v1/Episode_001_V6_1_full_narration_master.mp3')
INK, GRAY = '#171717', '#666666'


def sha(path, text=False):
    b = Path(path).read_bytes()
    return hashlib.sha256(b.replace(b'\r\n', b'\n') if text else b).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ffmpeg():
    if shutil.which('ffmpeg'):
        return shutil.which('ffmpeg')
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise ValueError('Install requirements.txt or supply ffmpeg on PATH') from exc


def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise ValueError(p.stderr.decode('utf-8', errors='replace')[-5000:])
    return p


def inputs():
    lock = load(EPISODE / 'visual-batch-v1/source-lock.json')
    for name, digest in lock['files'].items():
        if sha(EPISODE / name, text=True) != digest:
            raise ValueError('Locked script or trace changed: ' + name)
    provenance = load(HERE / 'provenance.json')
    for name, digest in provenance['locked_inputs'].items():
        if sha(HERE / name, text=True) != digest:
            raise ValueError('Prototype input changed: ' + name)
    plan = load(EPISODE / 'visual-batch-v1/ch5-edit-candidate-v1.json')
    if sha(EPISODE / 'visual-batch-v1/ch5-edit-candidate-v1.json', text=True) != provenance['candidate_sha256_lf']:
        raise ValueError('Candidate changed; review edit decisions again')
    shots = plan['edit_intervals']
    if [s['unit_id'] for s in shots] != ['VC-27', 'VC-28', 'VC-29', 'VC-30']:
        raise ValueError('Expected four ordered shots')
    for i, s in enumerate(shots):
        if not s['start'] <= s['verified_speech_start'] < s['verified_speech_end'] <= s['end']:
            raise ValueError('Speech outside shot')
        if i and shots[i-1]['end'] != s['start']:
            raise ValueError('Gap/overlap in candidate')
    if (shots[0]['start'], shots[-1]['end']) != (START, END):
        raise ValueError('Changed sequence range')
    timing = load(HERE / 'timing.json')
    spec = importlib.util.spec_from_file_location('locked_align', EPISODE / 'audio/forced_align.py')
    align = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(align)
    paras = align.spoken_paragraphs(EPISODE / 'episode-001-v6.1-production-locked.md')
    expected = [s for _, p in paras[109:125] for s in align.sentences(p)]
    if expected != [s['text'] for s in timing['sentences']]:
        raise ValueError('Captions differ from locked V6.1')
    last = START
    for s in timing['sentences']:
        if not s['boundary_verified'] or not last <= s['start'] < s['end'] <= END:
            raise ValueError('Missing or inverted sentence boundaries')
        last = s['end']
    return shots, timing


def ease(t, start, duration=.7):
    p = max(0., min(1., (t-start)/duration))
    return p*p*(3-2*p)


class Artwork:
    def __init__(self, timing):
        self.timing = timing
        self.fonts = {}
        self.bounds = []
        self.caption_font = self.font(39)

    def font(self, size, bold=False):
        key = size, bold
        if key not in self.fonts:
            filename = 'LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf'
            self.fonts[key] = ImageFont.truetype(str(HERE / 'fonts' / filename), size)
        return self.fonts[key]

    def text(self, d, xy, text, size=36, bold=False, fill=INK):
        font = self.font(size, bold)
        b = d.textbbox(xy, text, font=font)
        if b[0] < 110 or b[2] > W-110 or b[1] < 60 or b[3] > 864:
            raise ValueError(f'Artwork outside safe area: {text}: {b}')
        d.text(xy, text, font=font, fill=fill)
        self.bounds.append((text, b))

    def wrap(self, text, width=1620):
        lines, line = [], ''
        for word in text.split():
            test = (line + ' ' + word).strip()
            if self.caption_font.getlength(test) > width and line:
                lines.append(line)
                line = word
            else:
                line = test
        lines.append(line)
        if len(lines) > 2:
            raise ValueError('Caption requires more than two lines: ' + text)
        return lines

    def caption(self, d, t):
        for s in self.timing['sentences']:
            if s['start'] <= t < s['end']:
                lines = self.wrap(s['text'])
                top = 945 - (len(lines)-1)*24
                for n, text in enumerate(lines):
                    length = self.caption_font.getlength(text)
                    x, y = round((W-length)/2), top+n*50
                    d.rounded_rectangle((x-18, y-5, x+length+18, y+48), radius=5, fill=INK)
                    d.text((x,y), text, font=self.caption_font, fill='white')
                break

    def scene(self, d, t, shot):
        # One shared spatial layout. No named employer, invented messages or social UI.
        self.text(d, (140, 105), 'Illustrative example', 28, fill=GRAY)
        # Sparse desk and chair; the worker arrives at the first measured worker sentence.
        d.line([(400,630),(1120,630)], fill=INK, width=5)
        d.line([(430,630),(416,800)], fill=INK, width=4)
        d.line([(1088,630),(1102,800)], fill=INK, width=4)
        d.line([(385,540),(385,705),(590,705)], fill=INK, width=4)
        d.line([(420,705),(415,800)], fill=INK, width=4)
        if t >= 648.56:
            # Neutral line figure, held consistently through all WORLD shots.
            d.ellipse((510,330,614,439), fill='white', outline=INK, width=4)
            d.arc((500,316,623,441), 175, 320, fill=INK, width=5)
            d.line([(565,439),(560,470),(640,535),(686,618)], fill=INK, width=4)
            d.line([(548,470),(496,560),(500,660),(593,682),(672,787)], fill=INK, width=5)
            d.line([(500,660),(604,660),(706,785)], fill=INK, width=5)
            d.line([(535,502),(608,592),(727,615)], fill=INK, width=4)
            gesture = ease(t,703.481) if shot == 'VC-30' else 0
            d.line([(580,510),(657,round(586-80*gesture)),
                    (748,round(605-122*gesture))], fill=INK, width=4)
            d.line([(672,787),(718,787)], fill=INK, width=4)
            d.line([(706,785),(752,785)], fill=INK, width=4)
            d.ellipse((587,379,592,384), fill=INK)
            d.line([(609,383),(620,393),(609,397)], fill=INK, width=3)
            # Device and schedule remain unchanged when the personal boundary moves.
            d.line([(745,609),(905,609),(942,500),(792,500),(765,596)], fill=INK, width=4)
            d.line([(740,616),(925,616)], fill=INK, width=4)
        if t >= 655.506:
            self.calendar(d)
            p = ease(t, 663.233) if shot in ('VC-28','VC-30') else 0
            x = round(1030 + 100*p)
            d.rounded_rectangle((x,555,x+48,620), radius=7, outline=INK, width=4, fill='white')
            d.line([(x+15,610),(x+32,610)], fill=INK, width=2)
            self.text(d, (1200,573), 'weekends', 34)
            if p > 0:
                # A spatial boundary is illustrative; no claim of a successful employer reform.
                d.arc((440,285,1115,815), -62, -62+int(165*p), fill=GRAY, width=3)
        if shot == 'VC-30':
            if t >= 715.111:
                self.text(d, (1190,670), 'understaffing', 34)
                self.text(d, (1190,725), 'unreasonable deadlines', 34)
                self.text(d, (1190,780), 'constantly available', 34)

    def calendar(self, d):
        # No fabricated day-by-day hours or numerical chart. Only the narrated total.
        d.rectangle((1160,195,1650,495), outline=INK, width=3)
        d.line([(1160,255),(1650,255)], fill=INK, width=3)
        self.text(d, (1190,210), 'working week', 30, fill=GRAY)
        self.text(d, (1190,298), '60', 104, bold=True)
        self.text(d, (1345,345), 'hours / week', 36)
        for x in range(1210,1600,60):
            d.line([(x,430),(x+25,430)], fill=GRAY, width=3)

    def source(self, d, t):
        self.text(d, (150,105), 'World Health Organization', 34, bold=True)
        self.text(d, (150,157), '28 May 2019  /  ICD-11', 29, fill=GRAY)
        d.line([(150,225),(1745,225)], fill=INK, width=2)
        self.text(d, (150,270), 'Burnout', 96, bold=True)
        if t >= 683.052:
            self.text(d, (150,410), 'occupational phenomenon', 62)
            p = ease(t, 683.052, .6)
            d.line([(150,490),(150+int(748*p),490)], fill=INK, width=3)
        if t >= 687.074:
            self.text(d, (150,533), 'chronic workplace stress', 39)
            self.text(d, (150,586), 'not successfully managed', 36, fill=GRAY)
        if t >= 691.256:
            self.text(d, (150,670), 'Not classified as a medical condition', 39, bold=True)
        self.text(d, (150,787), 'Source: who.int  /  Departmental update', 28, fill=GRAY)
        self.text(d, (150,827), 'Editorial summary; full source reference accompanies this cut', 25, fill=GRAY)

    def frame(self, local_time, captions=False):
        t = START + local_time
        self.bounds = []
        im = Image.new('RGB', (W,H), 'white')
        d = ImageDraw.Draw(im)
        if t < 657.488:
            shot = 'VC-27'
        elif t < 678.72:
            shot = 'VC-28'
        elif t < 695.227:
            shot = 'VC-29'
        else:
            shot = 'VC-30'
        if shot == 'VC-29' and t < 678.91:
            # The candidate cut begins in a silent gap: hold the preceding scene
            # until the measured WHO sentence starts; do not pre-announce a source.
            self.scene(d,t,'VC-28')
        elif shot == 'VC-29':
            self.source(d,t)
        else:
            self.scene(d,t,shot)
        if captions:
            self.caption(d,t)
        return im


def srt_time(t):
    ms = round(t*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'


def captions(timing, out):
    art = Artwork(timing)
    cues = []
    for i, s in enumerate(timing['sentences'], 1):
        cues.append(f'{i}\n{srt_time(s["start"]-START)} --> {srt_time(s["end"]-START)}\n'
                    + '\n'.join(art.wrap(s['text'])) + '\n')
    (out/'chapter5.en.srt').write_text('\n'.join(cues), encoding='utf-8')


def verify(ff, path, out):
    # Decode the WHOLE exported video and audio; fail on corrupt frames/packets.
    run([ff,'-v','error','-xerror','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    info = run([ff,'-hide_banner','-i',str(path),'-map','0:a:0',
                '-af','ebur128=peak=true','-f','null','-']).stderr.decode(errors='replace')
    (out/'decode-and-loudness.log').write_text(info, encoding='utf-8')
    if '1920x1080' not in info or 'h264' not in info or 'aac' not in info:
        raise ValueError('Unexpected output streams')
    pcm = run([ff,'-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar','44100',
               '-f','s16le','-']).stdout
    summary = info[info.rfind('Summary:'):]
    return {'whole_file_decode':'PASS', 'audio_duration_seconds':len(pcm)/2/44100,
            'loudness_summary':summary.strip(), 'sha256':sha(path), 'bytes':path.stat().st_size}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--audio', type=Path, required=True)
    ap.add_argument('--outdir', type=Path, required=True)
    ap.add_argument('--download-audio', action='store_true')
    ap.add_argument('--frames-only', action='store_true')
    args = ap.parse_args()
    shots, timing = inputs()
    if args.download_audio and not args.audio.exists():
        import urllib.request
        args.audio.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(AUDIO_URL, args.audio)
    if not args.audio.is_file() or sha(args.audio) != AUDIO_SHA:
        raise ValueError('Missing or changed release narration; no substitute permitted')
    out = args.outdir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    art = Artwork(timing)
    captions(timing,out)
    frame_times = sorted(set([0, 8.1, 15.3, 16.9, 22.7, 23.04, 23.4, 24.1, 30,
                              38.15, 42.4, 42.81, 43.15, 43.7, 47.0, 50.71, 52, 54.67,
                              55, 62.93, 63.28, 63.63, 70, 75, 80.95] +
                             [s['start']-START for s in shots[1:]]))
    for t in frame_times:
        for cc in (False,True):
            art.frame(t,cc).save(out/f'frame-{t:06.2f}-{"cc" if cc else "clean"}.png')
    # A caption collision probe uses actual styled two-line captions inside the reserved band.
    probe = art.frame(52)
    d = ImageDraw.Draw(probe)
    d.rectangle((110,900,1810,1035), outline=GRAY, width=2)
    d.text((180,920),'Two-line caption exclusion probe',font=art.font(39),fill=INK)
    d.text((180,975),'Essential artwork stays above this band.',font=art.font(39),fill=INK)
    probe.save(out/'caption-exclusion-probe.png')
    if args.frames_only:
        print('Frames and SRT written; MP4 NOT_RUN')
        return
    ff = ffmpeg()
    frames = math.ceil((END-START)*FPS)
    # Keep one continuous original VO interval. Lossless PCM intermediate for content checks.
    wav = out/'chapter5-source.wav'
    run([ff,'-v','error','-y','-i',str(args.audio),'-af',f'atrim=start={START}:end={END},asetpts=PTS-STARTPTS',
         '-ac','1','-ar','44100','-c:a','pcm_s16le',str(wav)])
    reports = {}
    for cc, name in ((False,'chapter5-clean.mp4'),(True,'chapter5-review.mp4')):
        log = open(out/f'{name}.encode.log','wb')
        cmd = [ff,'-v','warning','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}',
               '-framerate',str(FPS),'-i','pipe:0','-i',str(wav),'-map','0:v:0','-map','1:a:0',
               '-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',
               '-movflags','+faststart','-metadata','title=Episode 001 Chapter 5 VC-27–VC-30 — review prototype',
               str(out/name)]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=log)
        try:
            for n in range(frames):
                p.stdin.write(art.frame(n/FPS,cc).tobytes())
                if n % (FPS*10) == 0:
                    print(f'{name}: {n/FPS:.0f}/{END-START:.2f}s', flush=True)
            p.stdin.close()
            if p.wait():
                raise ValueError('Encoder failed; inspect encode log')
        finally:
            if p.poll() is None:
                p.kill()
            log.close()
        reports[name] = verify(ff,out/name,out)
    report = {'state':'RENDERED_REVIEW_PROTOTYPE', 'publication_ready':False,
              'master_audio_sha256':sha(args.audio), 'source_audio_span':[START,END],
              'audio_edit':'single continuous trim; no TTS, substitutions, music, speed or level changes',
              'audio_duration_target':END-START,'video_frames':frames,'fps':FPS,
              'video_duration_seconds':frames/FPS,'resolution':[W,H],
              'frame_rounding_max_seconds':1/FPS,'subtitle_cues':len(timing['sentences']),
              'subtitle_basis':'archived measured sentence boundaries; two interior unmatched words retained',
              'cut_basis':'unmodified four-shot candidate; editorial proposal, not new speech alignment',
              'files':reports, 'renderer_sha256_lf':sha(Path(__file__),text=True),
              'font_sha256':{p.name:sha(p) for p in sorted((HERE/'fonts').glob('*.ttf'))},
              'ffmpeg_version':run([ff,'-version']).stdout.decode(errors='replace').splitlines()[0],
              'review_limits':['Human listening and final cut approval pending; see QA.md',
                               'Existing production contracts/approval hashes are not upgraded by this prototype']}
    save(out/'render-report.json',report)
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('BLOCKED:',exc,file=sys.stderr)
        sys.exit(2)
