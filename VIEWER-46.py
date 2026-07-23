from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-46 — FINAL
# Locked source: reviewed VIEWER-46-3 commit 88bf4b16cbab637b939759ba76a8874ecc1b4a13.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/88bf4b16cbab637b939759ba76a8874ecc1b4a13/VIEWER-46-3.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-46-3-final.py", "exec"))

display(Javascript(r'''
(() => {
  window.viewer46FinalTitle = 'Galaxy Viewer — VIEWER-46';
  const style = document.getElementById('viewer46TitleStyle');
  if(style){
    style.textContent = '#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"Galaxy Viewer — VIEWER-46";font-size:22px!important;color:#35c6ff!important}';
  }
})();
'''))
