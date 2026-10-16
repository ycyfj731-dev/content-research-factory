#!/usr/bin/env python3
"""Inspect actual MP4 frames/audio, never just the drawing instructions."""
import argparse
from array import array
import io
import json
import math
from pathlib import Path
import wave
from PIL import Image, ImageChops, ImageDraw
import render


def samples(ff, path):
    p=render.run([ff,'-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar','44100','-f','s16le','-'])
    a=array('h'); a.frombytes(p.stdout)
    return a


def correlation(a,b):
    # Samples are indexed on the decoded output timeline. Exclude padding and edges.
    x=a[4410:min(len(a),len(b))-4410:37]
    y=b[4410:min(len(a),len(b))-4410:37]
    mx,my=sum(x)/len(x),sum(y)/len(y)
    num=sum((u-mx)*(v-my) for u,v in zip(x,y))
    den=math.sqrt(sum((u-mx)**2 for u in x)*sum((v-my)**2 for v in y))
    return num/den


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--outdir',type=Path,required=True)
    args=ap.parse_args(); out=args.outdir
    ff=render.ffmpeg()
    report=render.load(out/'render-report.json')
    original=samples(ff,out/'chapter5-source.wav')
    if abs(len(original)/44100-(render.END-render.START))>1/44100:
        raise ValueError('Unexpected source trim duration')
    audio={}
    for filename in report['files']:
        if render.sha(out/filename)!=report['files'][filename]['sha256']:
            raise ValueError('Export differs from recorded render: '+filename)
        decoded=samples(ff,out/filename)
        corr=correlation(original,decoded)
        if corr<.99 or abs(len(decoded)-len(original))/44100>.05:
            raise ValueError(f'Audio altered or shifted: {filename}; correlation={corr}')
        audio[filename]={'waveform_correlation_at_zero_shift':corr,
                         'decoded_seconds':len(decoded)/44100,
                         'source_seconds':len(original)/44100,
                         'decode_minus_source_seconds':(len(decoded)-len(original))/44100,
                         'sample_peak_dbfs':20*math.log10(max(abs(x) for x in decoded)/32768)}
    times=[0,8.125,15.333,16.9167,23.0417,23.375,23.75,30,38.125,38.2084,38.375,38.4167,
           42.5417,42.8334,43.1667,46.5417,50.75,52,54.6667,54.7084,
           62.9584,63.2917,63.6667,70,74.625,75,80.9584]
    cols=5; tw,th=480,270
    sheet=Image.new('RGB',(cols*tw,math.ceil(len(times)/cols)*(th+36)),'#eeeeee')
    draw=ImageDraw.Draw(sheet)
    clean_sheet=sheet.copy(); clean_draw=ImageDraw.Draw(clean_sheet)
    art=render.Artwork(render.load(render.HERE/'timing.json'))
    font=art.font(22)
    details=[]
    for i,t in enumerate(times):
        for cc,filename in ((False,'chapter5-clean.mp4'),(True,'chapter5-review.mp4')):
            png=render.run([ff,'-v','error','-ss',str(t),'-i',str(out/filename),
                            '-frames:v','1','-f','image2pipe','-c:v','png','-']).stdout
            im=Image.open(io.BytesIO(png)).convert('RGB')
            if im.size!=(1920,1080):
                raise ValueError('Wrong dimensions')
            gray=im.convert('L')
            hist=gray.histogram()
            if sum(hist[:220])<500 or im.getpixel((0,0))!=(255,255,255):
                raise ValueError(f'Blank frame or lost white background at {t}')
            rg=ImageChops.difference(im.getchannel('R'),im.getchannel('G'))
            if rg.getextrema()[1]>2:
                raise ValueError('Unexpected color')
            if not cc:
                band=gray.crop((0,864,1920,1080))
                if band.getextrema()[0]<250:
                    raise ValueError('Artwork enters caption band')
            x,y=(i%cols)*tw,(i//cols)*(th+36)
            target,td=(sheet,draw) if cc else (clean_sheet,clean_draw)
            target.paste(im.resize((tw,th),Image.Resampling.LANCZOS),(x,y))
            td.text((x+12,y+th+5),f'{t:.3f} s',font=font,fill='black')
        details.append({'output_seconds':t,'master_seconds':round(t+render.START,4),
                        'clean_and_captioned_sample_checks':'PASS'})
    sheet.save(out/'encoded-review-contact-sheet.jpg',quality=93)
    clean_sheet.save(out/'encoded-clean-contact-sheet.jpg',quality=93)
    result={'technical_checks':'PASS','scope':'decoded actual exported MP4s',
            'audio':audio,'sampled_frames':details,
            'visual_review':'See QA.md for actual inspected contact sheets and qualitative limits',
            'human_listening_review':'NOT_RUN'}
    render.save(out/'export-checks.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
