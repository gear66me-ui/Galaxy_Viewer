from __future__ import annotations

import base64
import urllib.request
from pathlib import Path
from IPython.display import HTML, display

# VIEWER-49
# Uses the exact user-supplied JPEG saved in My Drive. No generated image,
# crop, filter, recolor, resampling, substitution, or image editing.
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

display(HTML(f"""
<div id="galaxyViewer49Header">
  <img src="{image_data}" alt="Galaxy Viewer header">
  <div class="galaxy-viewer-49-title">GALAXY VIEWER</div>
</div>
<style>
#galaxyViewer49Header{{
  position:relative;
  width:100%;
  max-width:1180px;
  aspect-ratio:1536 / 316;
  margin:0 auto 10px auto;
  padding:0;
  overflow:hidden;
  box-sizing:border-box;
  background:#000;
  border:1px solid #0b4f6c;
  border-radius:10px;
  box-shadow:0 0 18px rgba(0,174,239,.18);
}}
#galaxyViewer49Header img{{
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
#galaxyViewer49Header .galaxy-viewer-49-title{{
  position:absolute;
  left:3%;
  top:50%;
  transform:translateY(-50%);
  margin:0;
  padding:0;
  color:#f7fbff;
  font-family:"Helvetica Neue","Arial Narrow",Arial,Helvetica,sans-serif;
  font-size:clamp(34px,5.15vw,72px);
  font-weight:200;
  font-stretch:condensed;
  line-height:1;
  letter-spacing:0.12em;
  white-space:nowrap;
  pointer-events:none;
  text-shadow:0 0 2px rgba(255,255,255,.98),0 0 7px rgba(225,247,255,.92),0 0 15px rgba(120,210,255,.68);
}}
</style>
"""))

# Invoke only the locked reviewed viewer configuration with fixed Aladin API 3.8.2.
LOCK_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/"
    "GALAXY-VIEWER-ALADIN-3_8_2-LOCK.py"
)
with urllib.request.urlopen(LOCK_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "GALAXY-VIEWER-ALADIN-3_8_2-LOCK.py", "exec"))
