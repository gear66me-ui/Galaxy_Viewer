from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-45-2 — audit pass 2
# Locked source: reviewed VIEWER-45-1 commit f2aeb8d7fe6ffff1f043d51404a43c2c67e476db.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/f2aeb8d7fe6ffff1f043d51404a43c2c67e476db/VIEWER-45-1.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-45-1-base.py", "exec"))


display(Javascript(r'''
(() => {
  const title='Galaxy Viewer — VIEWER-45-2';
  function apply(){
    const h=document.querySelector('#viewer14-root h3');
    if(h) h.textContent=title;
    let style=document.getElementById('viewer45TitleStyle');
    if(!style){style=document.createElement('style');style.id='viewer45TitleStyle';document.head.appendChild(style);}
    style.textContent=`#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"${title}";font-size:22px!important;color:#35c6ff!important}`;
  }
  apply();
  window.viewer452Guard=setInterval(apply,100);
})();
'''))
