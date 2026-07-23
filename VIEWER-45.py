from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-45
# Locked base: VIEWER-44. Only the Interest score row is removed.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-44.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-44-base.py", "exec"))


display(Javascript(r'''
(() => {
  const PATCH_ID = 'viewer45-remove-interest-score';
  if (window[PATCH_ID]) return;
  window[PATCH_ID] = true;

  function clean(v){ return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function apply(){
    const status=document.getElementById('viewer14Status');
    if(!status) return false;
    [...status.querySelectorAll('tr')].forEach(row=>{
      const label=clean(row.querySelector('th')?.textContent).toLowerCase();
      if(label==='interest score') row.remove();
    });
    const h=document.querySelector('#viewer14-root h3');
    if(h) h.textContent='Galaxy Viewer — VIEWER-45';
    return true;
  }

  apply();
  const target=document.getElementById('viewer14Status');
  if(target){
    const observer=new MutationObserver(()=>{
      clearTimeout(window.viewer45Timer);
      window.viewer45Timer=setTimeout(apply,80);
    });
    observer.observe(target,{childList:true,subtree:true,characterData:true});
  }
  const timer=setInterval(apply,500);
  setTimeout(()=>clearInterval(timer),20000);
})();
'''))
