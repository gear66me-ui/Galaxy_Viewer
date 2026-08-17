from IPython.display import Javascript, display

# GV-beta-0010G
# Surgical composition release. The exact frozen 10F baseline is loaded from immutable commit a88b56749bd73efe166e0a849749f15d03fed47d,
# then the isolated 10G INFO module is attached. 10F itself is never modified.

display(Javascript(r"""
(async()=>{
  'use strict';
  const BASELINE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a88b56749bd73efe166e0a849749f15d03fed47d/viewer/GV-beta-0010F.py';
  const INFO_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-info-module-0001.js?v=df2e313042f398e518aca64bffde455389e10f5b';
  const source=await fetch(BASELINE_URL,{cache:'force-cache'}).then(r=>{if(!r.ok)throw new Error('10F baseline HTTP '+r.status);return r.text()});
  const htmlMatches=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error('10G could not extract frozen 10F baseline');
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML('beforeend',match[1]));
  jsMatches.forEach(match=>{const script=document.createElement('script');script.textContent=match[1];document.body.appendChild(script)});
  const loadInfo=()=>new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=INFO_URL;s.onload=resolve;s.onerror=()=>reject(new Error('10G INFO module failed to load'));document.head.appendChild(s)});
  await loadInfo();
  const stamp=()=>{
    const v=document.getElementById('gv-version-label');
    if(v){v.textContent='VERSION 10G';v.setAttribute('aria-label','GALAXY VIEWER VERSION 10G')}
    const cover=document.getElementById('gv-apk-cover');
    const old=cover&&cover.querySelector('.gv-10e-version');
    if(old)old.textContent='VERSION 10G';
    if(window.GalaxyViewerInfo10G)window.GalaxyViewerInfo10G.refresh();
  };
  stamp();setTimeout(stamp,500);setTimeout(stamp,1800);
})().catch(error=>{console.error('[GALAXY VIEWER 10G]',error);throw error});
"""))
