from __future__ import annotations
import urllib.request
from IPython.display import Javascript, display
# VIEWER-42-10 — audit pass 10, final release candidate
BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-42-1.py"
with urllib.request.urlopen(BASE_URL,timeout=60) as response: source=response.read().decode("utf-8")
exec(compile(source,"VIEWER-42-1-base.py","exec"))
display(Javascript(r'''(() => { const setTitle=()=>{const h=document.querySelector('#viewer14-root h3');if(h)h.textContent='Galaxy Viewer — VIEWER-42';};setTitle();const t=setInterval(setTitle,300);setTimeout(()=>clearInterval(t),20000);})();'''))
