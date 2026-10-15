#!/usr/bin/env python3
"""Deterministic prompt compile and optional Gemini API execution."""
import argparse,base64,csv,hashlib,json,os,pathlib,urllib.request
import yaml
P=pathlib.Path(__file__).resolve().parent
def main():
 a=argparse.ArgumentParser()
 a.add_argument("--mode",choices=["dry-run","generate"],default="dry-run")
 a.add_argument("--shots",nargs="*",default=[])
 o=a.parse_args()
 cfg=yaml.safe_load((P/"collage_v1.yaml").read_text())
 shots=yaml.safe_load((P/"pilot_15_shots.yaml").read_text())["scenes"]
 assert len(shots)==15 and len(set(s["id"] for s in shots))==15
 template=(P/"prompt.txt").read_text()
 outputs=P/"outputs";outputs.mkdir(exist_ok=True)
 records=[]
 for shot in shots:
  if o.shots and shot["id"] not in o.shots:continue
  prompt=template.format(**shot)
  record={"id":shot["id"],"prompt":prompt,"sha256":hashlib.sha256(prompt.encode()).hexdigest(),"model":cfg["model"],"status":"DRY_RUN"}
  if o.mode=="generate":
   if not shot["narration_anchor"] or shot["status"]!="script-traced":
    record["status"]="BLOCKED_UNTRACED_SCRIPT"
   else:
    key=os.environ.get("GEMINI_API_KEY")
    if not key:raise SystemExit("GEMINI_API_KEY missing (set environment variable; never hard-code it)")
    refs=[]
    for name in cfg["references"]:
     path=P/name
     if not path.is_file():raise SystemExit("Reference not found: "+str(path))
     blob=path.read_bytes();mime="image/png" if path.suffix.lower()==".png" else "image/jpeg"
     refs.append({"inlineData":{"mimeType":mime,"data":base64.b64encode(blob).decode()}})
    body={"contents":[{"parts":[{"text":prompt},*refs]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":{"aspectRatio":cfg["aspect"],"imageSize":cfg["size"]}}}
    req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/"+cfg["model"]+":generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":key},method="POST")
    try:
     with urllib.request.urlopen(req,timeout=180) as r: response=json.load(r)
     parts=response.get("candidates",[{}])[0].get("content",{}).get("parts",[])
     img=next((x["inlineData"] for x in parts if "inlineData" in x),None)
     if img:
      raw=base64.b64decode(img["data"]);ext=".png" if raw.startswith(bytes([137,80,78,71])) else ".jpg" if raw.startswith(bytes([255,216])) else ".bin"
      file=outputs/(shot["id"]+ext);file.write_bytes(raw)
      record.update(status="GENERATED_UNREVIEWED",path=str(file),bytes=len(raw))
     else:record["status"]="NO_IMAGE"
    except Exception as e:record.update(status="ERROR",error=str(e))
  records.append(record)
 (outputs/"prompt_manifest.json").write_text(json.dumps(records,indent=2,ensure_ascii=False))
 print(json.dumps({"mode":o.mode,"processed":len(records),"statuses":[r["status"] for r in records]}))
if __name__=="__main__": main()
