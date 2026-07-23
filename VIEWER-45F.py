from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-45F — FINAL
# Locked source: reviewed VIEWER-45-3 commit c8a1e51466b842f09ada1692cf67b3a045ed808f.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/c8a1e51466b842f09ada1692cf67b3a045ed808f/VIEWER-45-3.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-45-3-base.py", "exec"))


display(Javascript(r'''
(() => {
  const title='Galaxy Viewer — VIEWER-45F';
  function apply(){
    const h=document.querySelector('#viewer14-root h3');
    if(h) h.textContent=title;
    let style=document.getElementById('viewer45TitleStyle');
    if(!style){style=document.createElement('style');style.id='viewer45TitleStyle';document.head.appendChild(style);}
    style.textContent=`#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"${title}";font-size:22px!important;color:#35c6ff!important}`;
  }
  apply();
  window.viewer45FGuard=setInterval(apply,100);
})();
'''))
