from __future__ import annotations

import base64
import urllib.request
from pathlib import Path
from IPython.display import HTML, display

# VIEWER-50 — core viewer revision
# Exact user-supplied JPEG bytes; no AI image, image generation, editing,
# filtering, recoloring, cropping, replacement, or substitution.
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
image_data = "data:image/jpeg;base64," + image_b64

display(HTML(f'''
<div id="galaxyViewer50Header">
  <img src="{image_data}" alt="Galaxy Viewer header">
  <div class="galaxy-viewer-50-title">GALAXY VIEWER</div>
</div>
<style>
#galaxyViewer50Header{{
  position:relative;
  width:100%;
  max-width:1180px;
  aspect-ratio:1536 / 282;
  margin:0 auto 10px auto;
  padding:0;
  overflow:hidden;
  box-sizing:border-box;
  background:#000;
  border:1px solid #0b4f6c;
  border-radius:10px;
  box-shadow:0 0 18px rgba(0,174,239,.18);
}}
#galaxyViewer50Header img{{
  position:absolute;
  inset:0;
  display:block;
  width:100%;
  height:100%;
  margin:0;
  padding:0;
  border:0;
  object-fit:contain;
  object-position:center;
}}
#galaxyViewer50Header .galaxy-viewer-50-title{{
  position:absolute;
  left:3.2%;
  top:50%;
  transform:translateY(-50%) scaleX(.84);
  transform-origin:left center;
  margin:0;
  padding:0;
  color:#f7fbff;
  font-family:"Arial Narrow","Helvetica Neue",Arial,Helvetica,sans-serif;
  font-size:clamp(31px,5.75vw,76px);
  font-weight:200;
  line-height:1;
  letter-spacing:.145em;
  white-space:nowrap;
  pointer-events:none;
  text-shadow:0 0 3px #fff,0 0 8px #d5f2ff,0 0 16px #86d8ff;
}}
</style>
'''))

# Invoke only the locked immutable Viewer 46 core and compact white Aladin UI.
LOCK_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "1ba952f0cdbf4edf57dc8698ca7adec43d9fb021/"
    "GALAXY-VIEWER-ALADIN-CLASSIC-LOCK.py"
)
with urllib.request.urlopen(LOCK_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "GALAXY-VIEWER-ALADIN-CLASSIC-LOCK.py", "exec"))
