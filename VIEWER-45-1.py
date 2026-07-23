from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-45-1
# Locked base: VIEWER-45. Fixes only yellow-row font size, concise age text, Interest score removal, and version-title overwrite.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-45.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-45-base.py", "exec"))


display(Javascript(r'''
(() => {
  const PATCH_ID = 'viewer45-1-final-corrections';
  if (window[PATCH_ID]) return;
  window[PATCH_ID] = true;

  const FINAL_TITLE = 'Galaxy Viewer — VIEWER-45-1';
  const YELLOW = '#ffd84d';

  function clean(v){ return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function status(){ return document.getElementById('viewer14Status'); }
  function rows(){ return [...(status()?.querySelectorAll('tr') || [])]; }
  function rowBy(label){
    const wanted=clean(label).toLowerCase();
    return rows().find(r=>clean(r.querySelector('th')?.textContent).toLowerCase()===wanted);
  }
  function normalFontSize(){
    const normal=rows().find(r=>{
      const label=clean(r.querySelector('th')?.textContent).toLowerCase();
      return label && !['galaxy age','redshift (z) / distance','redshift / distance'].includes(label);
    });
    const cell=normal?.querySelector('td') || normal?.querySelector('th');
    return cell ? getComputedStyle(cell).fontSize : '16px';
  }
  function installTitleStyle(){
    let style=document.getElementById('viewer45TitleStyle');
    if(!style){
      style=document.createElement('style');
      style.id='viewer45TitleStyle';
      document.head.appendChild(style);
    }
    style.textContent=`#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"${FINAL_TITLE}";font-size:22px!important;color:#35c6ff!important}`;
  }
  function apply(){
    const table=status();
    if(!table) return false;

    rows().forEach(row=>{
      if(clean(row.querySelector('th')?.textContent).toLowerCase()==='interest score') row.remove();
    });

    const age=rowBy('Galaxy age');
    if(age){
      const td=age.querySelector('td');
      if(td && clean(td.textContent)!=='Approximately 9.4 billion years') td.textContent='Approximately 9.4 billion years';
    }

    const size=normalFontSize();
    ['Galaxy age','Redshift (z) / Distance','Redshift / Distance'].forEach(label=>{
      const row=rowBy(label);
      if(!row) return;
      row.classList.remove('emphasis');
      [row.querySelector('th'),row.querySelector('td')].forEach(cell=>{
        if(!cell) return;
        cell.style.setProperty('color',YELLOW,'important');
        cell.style.setProperty('font-size',size,'important');
        cell.style.setProperty('line-height','normal','important');
      });
    });

    const h=document.querySelector('#viewer14-root h3');
    if(h) h.textContent=FINAL_TITLE;
    installTitleStyle();
    return true;
  }

  apply();
  const root=document.getElementById('viewer14-root');
  if(root){
    const observer=new MutationObserver(()=>{
      clearTimeout(window.viewer451Timer);
      window.viewer451Timer=setTimeout(apply,20);
    });
    observer.observe(root,{childList:true,subtree:true,characterData:true});
  }
  window.viewer451Guard=setInterval(apply,100);
})();
'''))
