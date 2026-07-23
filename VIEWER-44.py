from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-44
# Locked base: VIEWER-43. Only the Galaxy age text and emphasis font size are changed.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-43.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-43-base.py", "exec"))


display(Javascript(r'''
(() => {
  const PATCH_ID = 'viewer44-age-font-patch';
  if (window[PATCH_ID]) return;
  window[PATCH_ID] = true;

  function clean(v){ return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function status(){ return document.getElementById('viewer14Status'); }
  function rows(){ return [...(status()?.querySelectorAll('tr') || [])]; }
  function rowBy(label){
    const wanted=clean(label).toLowerCase();
    return rows().find(r=>clean(r.querySelector('th')?.textContent).toLowerCase()===wanted);
  }

  function apply(){
    const age=rowBy('Galaxy age');
    if(age){
      const td=age.querySelector('td');
      if(td && clean(td.textContent)!=='Approximately 9.2 billion years') td.textContent='Approximately 9.2 billion years';
    }

    ['Galaxy age','Redshift (z) / Distance','Redshift / Distance'].forEach(label=>{
      const row=rowBy(label);
      const th=row?.querySelector('th');
      const td=row?.querySelector('td');
      if(th){ th.style.color='#ffd84d'; th.style.fontWeight='700'; th.style.fontSize='inherit'; }
      if(td){ td.style.color='#ffd84d'; td.style.fontWeight='700'; td.style.fontSize='inherit'; }
    });

    const h=document.querySelector('#viewer14-root h3');
    if(h) h.textContent='Galaxy Viewer — VIEWER-44';
    return true;
  }

  apply();
  const target=status();
  if(target){
    const observer=new MutationObserver(()=>{
      clearTimeout(window.viewer44Timer);
      window.viewer44Timer=setTimeout(apply,80);
    });
    observer.observe(target,{childList:true,subtree:true,characterData:true});
  }
  const timer=setInterval(apply,500);
  setTimeout(()=>clearInterval(timer),20000);
})();
'''))
