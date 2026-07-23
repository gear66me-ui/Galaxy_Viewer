from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-43-1
# Locked base: VIEWER-42. No viewer controls, search logic, icons, or other rows changed.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-42.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-42-base.py", "exec"))


display(Javascript(r'''
(() => {
  const PATCH_ID = 'viewer43-size-row-patch';
  if (window[PATCH_ID]) return;
  window[PATCH_ID] = true;

  function clean(v){ return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function status(){ return document.getElementById('viewer14Status'); }
  function rows(){ return [...(status()?.querySelectorAll('tr') || [])]; }
  function label(row){ return clean(row?.querySelector('th')?.textContent); }
  function rowBy(...names){
    const wanted=names.map(x=>clean(x).toLowerCase());
    return rows().find(r=>wanted.includes(label(r).toLowerCase()));
  }

  function toThousands(text){
    let value=clean(text);
    value=value.replace(/([0-9]+(?:\.[0-9]+)?)\s*×\s*([0-9]+(?:\.[0-9]+)?)\s*million light-years/i,
      (_,a,b)=>`${(Number(a)*1000).toFixed(1)} × ${(Number(b)*1000).toFixed(1)} thousand light-years`);
    value=value.replace(/([0-9]+(?:\.[0-9]+)?)\s*million light-years/i,
      (_,a)=>`${(Number(a)*1000).toFixed(1)} thousand light-years`);
    value=value.replace(/\s*\/\s*/g,' / ');
    value=value.replace(/\s*×\s*/g,' × ');
    return value;
  }

  function apply(){
    const table=status();
    if(!table) return false;

    const sizeRow=rowBy('Physical / angular size','Physical size / Angular size','Physical size');
    if(sizeRow){
      const th=sizeRow.querySelector('th');
      const td=sizeRow.querySelector('td');
      if(th && clean(th.textContent)!=='Physical size / Angular size') th.textContent='Physical size / Angular size';
      if(td){
        const next=toThousands(td.textContent);
        if(clean(td.textContent)!==next) td.textContent=next;
      }
      const radial=rowBy('Radial velocity');
      if(radial && sizeRow.nextElementSibling!==radial) radial.parentNode.insertBefore(sizeRow,radial);
    }

    rows().forEach(r=>{
      if(label(r).toLowerCase()==='interest score') r.remove();
    });

    const h=document.querySelector('#viewer14-root h3');
    if(h) h.textContent='Galaxy Viewer — VIEWER-43-1';
    return true;
  }

  apply();
  const target=status();
  if(target){
    const observer=new MutationObserver(()=>{
      clearTimeout(window.viewer43SizeTimer);
      window.viewer43SizeTimer=setTimeout(apply,80);
    });
    observer.observe(target,{childList:true,subtree:true,characterData:true});
  }
  const timer=setInterval(apply,500);
  setTimeout(()=>clearInterval(timer),20000);
})();
'''))
