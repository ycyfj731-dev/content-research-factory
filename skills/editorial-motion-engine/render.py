"""Frame-accurate SVG renderer for an HTML scene exposing window.motionEngine.seek(t).

Install: pip install playwright && python -m playwright install chromium; install ffmpeg.
Run: python render.py --html demo/index.html --out preview.mp4
Uses set_content instead of file:// navigation (which can be blocked in sandboxed Chromium).
"""
import argparse
import subprocess
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

def render(html: Path, output: Path, fps: int=24, width: int=1280, height: int=720):
    with sync_playwright() as p, tempfile.TemporaryDirectory(prefix="motion_") as temp:
        browser=p.chromium.launch(headless=True, args=["--no-sandbox"])
        page=browser.new_page(viewport={"width":width,"height":height})
        page.set_content(html.read_text(encoding="utf-8"),wait_until="load")
        page.evaluate("document.fonts.ready")
        scene=page.locator("#canvas")
        scene.evaluate("(el,w)=>{el.style.width=w+'px';el.style.height=w*9/16+'px'}",width)
        duration=float(page.evaluate("window.motionEngine.duration"))
        frames=round(duration*fps)
        for i in range(frames):
            page.evaluate("(t)=>window.motionEngine.seek(t)",i/fps)
            scene.screenshot(path=str(Path(temp)/f"{i:05d}.png"),animations="disabled")
        browser.close()
        output.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),
            "-i",str(Path(temp)/"%05d.png"),"-c:v","libx264","-pix_fmt","yuv420p",
            "-crf","19","-movflags","+faststart",str(output)],check=True)
        print(f"Rendered {frames} frames into {output}")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--html",type=Path,default=Path(__file__).parent/"demo/index.html")
    parser.add_argument("--out",type=Path,default=Path("motion-preview.mp4"))
    parser.add_argument("--fps",type=int,default=24)
    a=parser.parse_args()
    render(a.html,a.out,a.fps)
