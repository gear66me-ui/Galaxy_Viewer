from __future__ import annotations

import base64
import urllib.request
from pathlib import Path
from IPython.display import HTML, display

# VIEWER-48
# Exact user-supplied JPEG. No AI image, crop, filter, recolor, resize, or substitution.
IMAGE_PATH = Path("/content/drive/MyDrive/GALAXY_VIEWER_HEADER.jpeg")

if not IMAGE_PATH.exists():
    try:
        from google.colab import drive
        drive.mount("/content/drive")
    except Exception:
        pass

if not IMAGE_PATH.exists():
    raise FileNotFoundError(
        "Exact header image not found at "
        "/content/drive/MyDrive/GALAXY_VIEWER_HEADER.jpeg"
    )

image_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("ascii")
image_data = f"data:image/jpeg;base64,{image_b64}"

display(HTML(f"""
<div id="galaxyViewer48Header" style="
    position:relative;
    width:100%;
    max-width:1180px;
    margin:0 auto 12px auto;
    overflow:hidden;
    border:1px solid #0b4f6c;
    border-radius:10px;
    background:#000;
    box-sizing:border-box;
">
  <img src="{image_data}" alt="Galaxy Viewer header" style="
      display:block;
      width:100%;
      height:auto;
      max-width:100%;
      object-fit:contain;
      object-position:center;
      margin:0;
      padding:0;
      border:0;
  ">
  <div style="
      position:absolute;
      inset:0;
      display:flex;
      align-items:center;
      justify-content:center;
      pointer-events:none;
      color:#f4fbff;
      font-family:Arial,Helvetica,sans-serif;
      font-size:clamp(30px,6.2vw,86px);
      font-weight:300;
      letter-spacing:0.24em;
      white-space:nowrap;
      text-shadow:0 0 4px #fff,0 0 10px #bfefff,0 0 20px #75cfff;
      padding-left:0.24em;
      box-sizing:border-box;
  ">GALAXY VIEWER</div>
</div>
"""))

# Invoke the locked Aladin/viewer configuration. Do not replace or edit it here.
LOCK_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/"
    "GALAXY-VIEWER-ALADIN-LOCK.py"
)
with urllib.request.urlopen(LOCK_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

exec(compile(source, "GALAXY-VIEWER-ALADIN-LOCK.py", "exec"))
