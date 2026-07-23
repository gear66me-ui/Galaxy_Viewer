from __future__ import annotations

import base64
from pathlib import Path
from IPython.display import HTML, display

# GALAXY-VIEWER-CORE-002
# Core display only: exact user-supplied header image + native compact Aladin viewer.
# No Google Drive authentication, search, bridge, data table, catalog module, or enrichment code.

IMAGE_PATH = Path('/content/1000009616.jpg')

if not IMAGE_PATH.exists():
    from google.colab import files
    uploaded = files.upload()
    if not uploaded:
        raise FileNotFoundError('Upload the exact Galaxy Viewer JPEG when prompted.')
    first_name, first_bytes = next(iter(uploaded.items()))
    IMAGE_PATH.write_bytes(first_bytes)

header_bytes = IMAGE_PATH.read_bytes()
header_b64 = base64.b64encode(header_bytes).decode('ascii')

display(HTML(f"""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.min.css">
<div id="galaxyCoreRoot">
  <div id="galaxyCoreHeader">
    <img src="data:image/jpeg;base64,{header_b64}" alt="Galaxy Viewer">
    <div id="galaxyCoreTitle">GALAXY VIEWER</div>
  </div>
  <div id="galaxyCoreAladin"></div>
</div>
<style>
#galaxyCoreRoot{{width:100%;max-width:1180px;margin:0 auto;background:#000;box-sizing:border-box}}
#galaxyCoreHeader{{position:relative;width:100%;aspect-ratio:1536/316;overflow:hidden;border:1px solid #0b4f6c;border-radius:12px;background:#000;box-shadow:0 0 18px rgba(0,174,239,.18);box-sizing:border-box;margin:0 0 12px 0}}
#galaxyCoreHeader img{{position:absolute;inset:0;width:100%;height:100%;display:block;object-fit:contain;object-position:center;border:0;margin:0;padding:0}}
#galaxyCoreTitle{{position:absolute;left:2.2%;top:50%;transform:translateY(-50%) scaleX(.93);transform-origin:left center;color:#f7fbff;white-space:nowrap;pointer-events:none;font-family:'Arial Narrow','Helvetica Neue',Arial,Helvetica,sans-serif;font-size:clamp(34px,5.55vw,78px);font-weight:300;line-height:1;letter-spacing:.135em;text-shadow:0 0 2px #fff,0 0 8px #dff8ff,0 0 18px #75cfff}}
#galaxyCoreAladin{{width:100%;height:680px;border:1px solid #0b4f6c;border-radius:12px;overflow:hidden;background:#000;box-sizing:border-box}}
#galaxyCoreAladin .aladin-btn{{font-size:inherit!important;padding:.2rem!important;margin:0!important}}
@media(max-width:700px){{#galaxyCoreAladin{{height:560px}}#galaxyCoreTitle{{left:2%;font-size:clamp(28px,7vw,52px);letter-spacing:.11em}}}}
</style>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
(() => {{
  const start = async () => {{
    if (!window.A || !A.init) {{ setTimeout(start, 100); return; }}
    await A.init;
    if (window.galaxyCoreAladinInstance) return;
    window.galaxyCoreAladinInstance = A.aladin('#galaxyCoreAladin', {{
      target: 'M 31',
      survey: 'P/DSS2/color',
      fov: 1.3,
      cooFrame: 'ICRS',
      showReticle: true,
      showZoomControl: true,
      showFullscreenControl: true,
      showLayersControl: true,
      showGotoControl: true,
      showCooGridControl: true,
      showSimbadPointerControl: true
    }});
  }};
  start();
}})();
</script>
"""))
