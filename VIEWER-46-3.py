from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-46-3 — audit pass 3
# Locked source: reviewed VIEWER-46-2 commit 5ec539236328fa2eb567211fe6f958aa2b834613.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/5ec539236328fa2eb567211fe6f958aa2b834613/VIEWER-46-2.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-46-2-audited.py", "exec"))

display(Javascript(r'''
(() => {
  window.viewer46FinalTitle = 'Galaxy Viewer — VIEWER-46-3';
  const style = document.getElementById('viewer46TitleStyle');
  if(style){
    style.textContent = '#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"Galaxy Viewer — VIEWER-46-3";font-size:22px!important;color:#35c6ff!important}';
  }
})();
'''))
