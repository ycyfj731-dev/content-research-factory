#!/usr/bin/env python3
"""Assemble six independently exported narration MP3s; never guess sentence timestamps.
Usage: python assemble_and_check.py /path/to/chapter-mp3-directory
Requires ffmpeg and ffprobe. Expects ch01.mp3 ... ch06.mp3.
"""
import json, subprocess, sys, pathlib, tempfile
def ffprobe(path):
    raw=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],text=True)
    return float(raw.strip())
def main():
    root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
    files=[root / f"ch{i:02d}.mp3" for i in range(1,7)]
    missing=[str(p) for p in files if not p.is_file()]
    if missing: sys.exit("Missing actual audio files: "+", ".join(missing))
    lengths=[ffprobe(p) for p in files]
    # Transcode every chapter to the same PCM spec so MP3 encoder padding does not cause spurious seams.
    with tempfile.TemporaryDirectory() as tmp:
        pcm=[]
        for i,p in enumerate(files):
            wav=pathlib.Path(tmp)/f"ch{i+1:02}.wav"
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(p),"-ar","48000","-ac","1","-c:a","pcm_s16le",str(wav)],check=True)
            pcm.append(wav)
        playlist=pathlib.Path(tmp)/"concat.txt"
        playlist.write_text("".join(f"file '{p}'\n" for p in pcm),encoding="utf-8")
        out=root/"episode001_v6.1_master.wav"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(playlist),"-c:a","pcm_s16le",str(out)],check=True)
    start=0.0; segments=[]
    for i,d in enumerate(lengths):
        segments.append(dict(chapter=i+1,input=str(files[i]),start_s=start,end_s=start+d,duration_s=d))
        start+=d
    report={"master":str(out),"master_duration_s":ffprobe(out),"source_mp3_durations_s":lengths,"segments_nominal":segments,"caveat":"Nominal segment boundaries use MP3 duration. Use decoded PCM durations and voice forced alignment for accurate word/cue timings; never publish estimated SRT as verified."}
    (root/"assembly_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
