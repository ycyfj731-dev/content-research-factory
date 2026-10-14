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
    # Speech recognition often writes the canonical compound "therapy-speak" as
    # two words ("therapy", "speak"). Match the atomic components while retaining
    # the exact *original* canonical spelling in captions and the output JSON.
    atomic=[]; owners=[]
    for wi,w in enumerate(canonical_words):
        parts=[normalize(part) for part in re.split(r"[-‐‑–]",w["word"])]
        parts=[part for part in parts if part]
        for part in parts:
            atomic.append(part)
            owners.append(wi)
    asr_atomic=[]; asr_owners=[]
    for ai,w in enumerate(asr_words):
        parts=[normalize(part) for part in re.split(r"[-‐‑–]",w["word"])]
        for part in parts:
            if part:
                asr_atomic.append(part)
                asr_owners.append(ai)
    matches=SequenceMatcher(a=atomic,b=asr_atomic,autojunk=False)
    pieces={}
    for op,a0,a1,b0,b1 in matches.get_opcodes():
        if op=="equal":
            for k in range(a1-a0):
                source=asr_words[asr_owners[b0+k]]
                pieces.setdefault(owners[a0+k],[]).append((a0+k,float(source["start"]),float(source["end"])))
    needed={}
    for wi in owners:needed[wi]=needed.get(wi,0)+1
    times={}
    for wi,values in pieces.items():
        # A compound is verified only when *all* of its parts matched.
        if len(values)==needed[wi]:
            values.sort()
            times[wi]=(min(v[1] for v in values),max(v[2] for v in values))
    # Re-align only sentences with a missing first/last word using the EXACT
    # locked text and the measured time limits of adjacent sentences. This is
    # acoustic alignment, not an interpolation of duration or invented timestamps.
    repaired=[]
    for si,sm in enumerate(sentence_meta):
        ids=list(range(sm["first"],sm["last"]))
        if not ids or (ids[0] in times and ids[-1] in times):
            continue
        present=[j for j in ids if j in times]
        if len(present)<max(2,len(ids)//2):
            continue
        left=times[ids[0]-1][1] if ids[0]>0 and ids[0]-1 in times else max(0.0,times[present[0]][0]-2.0)
        right=times[ids[-1]+1][0] if ids[-1]+1<len(canonical_words) and ids[-1]+1 in times else times[present[-1]][1]+2.0
        start=max(0.,left-0.10)
        end=min(len(audio)/16000.,right+0.10)
        if end<=start or end-start>30:
            continue
        segment=[{"start":start,"end":end,"text":sm["text"]}]
        local=whisperx.align(segment,align_model,metadata,audio,device,return_char_alignments=False)
        local_words=[w for q in local.get("segments",[]) for w in q.get("words",[]) if w.get("start") is not None and w.get("end") is not None and normalize(w["word"])]
        if not local_words:
            continue
        # Same complete-part matching as global pass, but with known local scope.
        local_atoms=[];local_owner=[]
        for wi in ids:
            for part in re.split(r"[-‐‑–]",canonical_words[wi]["word"]):
                norm=normalize(part)
                if norm:local_atoms.append(norm);local_owner.append(wi)
        reco_atoms=[];reco_owner=[]
        for li,word in enumerate(local_words):
            for part in re.split(r"[-‐‑–]",word["word"]):
                norm=normalize(part)
                if norm:reco_atoms.append(norm);reco_owner.append(li)
        mm=SequenceMatcher(a=local_atoms,b=reco_atoms,autojunk=False)
        recovered={}
        for op,a0,a1,b0,b1 in mm.get_opcodes():
            if op=="equal":
                for k in range(a1-a0):
                    wid=local_owner[a0+k]; word=local_words[reco_owner[b0+k]]
                    recovered.setdefault(wid,[]).append((a0+k,float(word["start"]),float(word["end"])))
        required={wi:sum(v==wi for v in local_owner) for wi in ids}
        for wi,v in recovered.items():
            if wi in times or len(v)!=required[wi]:continue
            t=(min(x[1] for x in v),max(x[2] for x in v))
            if t[0] < start or t[1] > end or t[1]<t[0]:continue
            times[wi]=t
            repaired.append({"sentence":si+1,"word":canonical_words[wi]["word"],"start":round(t[0],3),"end":round(t[1],3)})
    out.joinpath("local_repair_report.json").write_text(json.dumps(repaired,indent=2),encoding="utf8")
    matched=len(times); coverage=matched/len(canonical_words)
    wordout=[]
    for i,w in enumerate(canonical_words):
        d=dict(w,index=i+1)
        if i in times:d.update(start=round(times[i][0],3),end=round(times[i][1],3),verified=True)
        else:d.update(start=None,end=None,verified=False)
        wordout.append(d)
    out.joinpath("word_timestamps.json").write_text(json.dumps(wordout,ensure_ascii=False,indent=2),encoding="utf8")
    sentenceout=[];uncertain=[];boundary_missing=[]
    for i,sm in enumerate(sentence_meta):
        wids=list(range(sm["first"],sm["last"]))
        verified=[j for j in wids if j in times]
        good=len(verified)==len(wids) and bool(wids)
        boundaries_ok=bool(wids) and wids[0] in times and wids[-1] in times
        if not good:uncertain.append(i+1)
        if not boundaries_ok:boundary_missing.append(i+1)
        first,last=(round(times[wids[0]][0],3),round(times[wids[-1]][1],3)) if boundaries_ok else (None,None)
        missing=[canonical_words[j]["word"] for j in wids if j not in times]
        sentenceout.append({"index":i+1,"chapter":sm["chapter"],"paragraph":sm["paragraph"],"text":sm["text"],"start":first,"end":last,"all_words_matched":good,"boundary_verified":boundaries_ok,"missing_words":missing,"matched_words":len(verified),"total_words":len(wids)})
    out.joinpath("sentence_timestamps.json").write_text(json.dumps(sentenceout,ensure_ascii=False,indent=2),encoding="utf8")
    report={"words_total":len(canonical_words),"words_matched":matched,"word_coverage":coverage,"sentences":len(sentenceout),"fully_verified_sentences":len(sentenceout)-len(uncertain),"unverified_sentence_indices":uncertain,"boundary_missing_indices":boundary_missing,"srt_boundaries_supported":not boundary_missing,"asr_is_not_output_text":True}
    out.joinpath("alignment_report.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    if coverage < args.min_match or boundary_missing:
        print("ALIGNMENT REVIEW REQUIRED:",json.dumps(report),file=sys.stderr)
        # Do not emit an apparently finished SRT containing guessed cue times.
        sys.exit(2)
    # Interior unmatched words remain flagged, but independently measured sentence boundaries are usable.
    cues=[]
    for i,s in enumerate(sentenceout):
        cues.append(f'{i+1}\n{srt_time(s["start"])} --> {srt_time(s["end"])}\n{s["text"]}\n')
    out.joinpath("episode001_en.srt").write_text("\n".join(cues),encoding="utf8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
