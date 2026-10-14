#!/usr/bin/env python3
"""Align the *locked* Episode 001 V6.1 narration to its already-rendered audio.
Run in GitHub Actions with WhisperX; output word/sentence JSON and SRT.

The initial WhisperX recognition is used ONLY to locate utterance windows.
The source of all output words is the locked script. Exact text never comes
from transcription. We fail closed when alignment of a passage is uncertain.
"""
import argparse, json, re, sys
from pathlib import Path
from difflib import SequenceMatcher

def spoken_paragraphs(path):
    text=Path(path).read_text(encoding="utf8")
    ch=0; out=[]
    for line in text.splitlines():
        t=line.strip()
        if re.match(r"^## [1-6]\.",t):
            ch=int(t[3]); continue
        if ch and t and not t.startswith("#") and not t.startswith("<!--"):
            out.append((ch,re.sub(r"\*([^*]+)\*",r"\1",t)))
    if len(out)!=150:
        raise ValueError(f"Expected 150 paragraphs in locked script; got {len(out)}")
    return out

def normalize(s):
    return re.sub(r"[^a-z0-9']","",s.lower().replace("’","'"))

def sentences(text):
    return [x.strip() for x in re.split(r'(?<=[.!?])\s+(?=[A-Z"“])',text) if x.strip()]

def srt_time(t):
    ms=round(t*1000)
    return f"{ms//3600000:02d}:{(ms//60000)%60:02d}:{(ms//1000)%60:02d},{ms%1000:03d}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--audio",required=True)
    ap.add_argument("--script",required=True)
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--model",default="small")
    ap.add_argument("--min-match",type=float,default=.97)
    args=ap.parse_args()
    import torch, whisperx
    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True)
    device="cuda" if torch.cuda.is_available() else "cpu"
    compute_type="float16" if device=="cuda" else "int8"
    audio=whisperx.load_audio(args.audio)
    model=whisperx.load_model(args.model,device,compute_type=compute_type,language="en")
    asr=model.transcribe(audio,batch_size=8)
    del model
    if device=="cuda":torch.cuda.empty_cache()
    align_model,metadata=whisperx.load_align_model(language_code="en",device=device)
    aligned=whisperx.align(asr["segments"],align_model,metadata,audio,device,return_char_alignments=False)
    asr_words=[w for seg in aligned["segments"] for w in seg.get("words",[]) if w.get("start") is not None and w.get("end") is not None and normalize(w["word"])]
    canon=spoken_paragraphs(args.script)
    canonical_words=[]
    sentence_meta=[]
    for pi,(chapter,para) in enumerate(canon):
        for sent in sentences(para):
            start=len(canonical_words)
            for tok in re.findall(r"\S+",sent):
                if normalize(tok):canonical_words.append({"word":tok,"ch":chapter,"paragraph":pi+1})
            sentence_meta.append({"chapter":chapter,"paragraph":pi+1,"text":sent,"first":start,"last":len(canonical_words)})
    matches=SequenceMatcher(a=[normalize(w["word"]) for w in canonical_words],b=[normalize(w["word"]) for w in asr_words],autojunk=False)
    times={}
    for op,a0,a1,b0,b1 in matches.get_opcodes():
        if op=="equal":
            for k in range(a1-a0):times[a0+k]=(float(asr_words[b0+k]["start"]),float(asr_words[b0+k]["end"]))
    matched=len(times); coverage=matched/len(canonical_words)
    wordout=[]
    for i,w in enumerate(canonical_words):
        d=dict(w,index=i+1)
        if i in times:d.update(start=round(times[i][0],3),end=round(times[i][1],3),verified=True)
        else:d.update(start=None,end=None,verified=False)
        wordout.append(d)
    out.joinpath("word_timestamps.json").write_text(json.dumps(wordout,ensure_ascii=False,indent=2),encoding="utf8")
    sentenceout=[];uncertain=[]
    for i,sm in enumerate(sentence_meta):
        wids=list(range(sm["first"],sm["last"]))
        verified=[j for j in wids if j in times]
        good=len(verified)==len(wids) and bool(wids)
        if not good:uncertain.append(i+1)
        first,last=(round(times[verified[0]][0],3),round(times[verified[-1]][1],3)) if verified else (None,None)
        sentenceout.append({"index":i+1,"chapter":sm["chapter"],"paragraph":sm["paragraph"],"text":sm["text"],"start":first,"end":last,"verified":good,"matched_words":len(verified),"total_words":len(wids)})
    out.joinpath("sentence_timestamps.json").write_text(json.dumps(sentenceout,ensure_ascii=False,indent=2),encoding="utf8")
    report={"words_total":len(canonical_words),"words_matched":matched,"word_coverage":coverage,"sentences":len(sentenceout),"fully_verified_sentences":len(sentenceout)-len(uncertain),"unverified_sentence_indices":uncertain,"asr_is_not_output_text":True}
    out.joinpath("alignment_report.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    if coverage < args.min_match or uncertain:
        print("ALIGNMENT REVIEW REQUIRED:",json.dumps(report),file=sys.stderr)
        # Do not emit an apparently finished SRT containing guessed cue times.
        sys.exit(2)
    cues=[]
    for i,s in enumerate(sentenceout):
        cues.append(f'{i+1}\n{srt_time(s["start"])} --> {srt_time(s["end"])}\n{s["text"]}\n')
    out.joinpath("episode001_en.srt").write_text("\n".join(cues),encoding="utf8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
