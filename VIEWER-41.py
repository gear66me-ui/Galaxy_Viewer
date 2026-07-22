from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-40.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-40-base.py", "exec"))


display(Javascript(r'''
(() => {
  const aliases = {
    'NGC 4321':'M100', 'NGC 5194':'M51', 'NGC 4594':'M104', 'NGC 5457':'M101',
    'NGC 4826':'M64', 'NGC 3031':'M81', 'NGC 3034':'M82', 'NGC 224':'M31',
    'NGC 598':'M33', 'NGC 4258':'M106', 'NGC 4736':'M94', 'NGC 5055':'M63',
    'NGC 5236':'M83', 'NGC 7331':'NGC 7331', 'NGC 1365':'NGC 1365'
  };

  function clean(v){ return String(v ?? '').trim(); }
  function rows(){ return [...document.querySelectorAll('#viewer14Status tr')]; }
  function rowBy(label){ return rows().find(r => new RegExp(`^${label}$`,'i').test(clean(r.querySelector('th')?.textContent))); }
  function value(label){ return clean(rowBy(label)?.querySelector('td')?.textContent); }
  function setValue(label, next){ const cell=rowBy(label)?.querySelector('td'); if(cell && next) cell.textContent=next; }
  function objectName(){ return value('Object') || clean(window.viewer30CurrentGalaxy?.name) || clean(window.viewer27LastDisplayedGalaxy?.name) || 'galaxy'; }
  function exactNames(){ const n=objectName().replace(/\s+/g,' ').trim(); const a=aliases[n.toUpperCase()] || aliases[n]; return a && a.toUpperCase()!==n.toUpperCase() ? [n,a] : [n]; }
  function sourceQuery(){
    const names=exactNames().map(n=>`"${n}"`).join(' OR ');
    return `${names} galaxy NED SIMBAD HyperLEDA NASA ESA ESO distance redshift radial velocity morphology angular size apparent magnitude physical size stellar population age discovery`; 
  }
  function researchPrompt(){
    const names=exactNames().join(' / ');
    return `Search the web for authoritative astronomy information about ${names}. Confirm the identity and aliases first. Return a compact table with morphology, coordinates, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery history, notable structures, and scientific or visual interest. Prefer NED, SIMBAD, HyperLEDA, NASA, ESA, ESO, peer-reviewed papers, and major observatories. Clearly label measured values, catalog values, calculated values, and estimates. Resolve disagreements between sources instead of repeating them.`;
  }
  async function copyPrompt(){ try{await navigator.clipboard.writeText(researchPrompt());}catch(_){ } }
  function androidIntent(webUrl,pkg){ const u=webUrl.replace(/^https?:\/\//,''); return `intent://${u}#Intent;scheme=https;package=${pkg};S.browser_fallback_url=${encodeURIComponent(webUrl)};end`; }
  async function chrome(){ window.open(`https://www.google.com/search?q=${encodeURIComponent(sourceQuery())}`,'_blank','noopener,noreferrer'); }
  async function chatgpt(){ const p=researchPrompt(); await copyPrompt(); const u=`https://chatgpt.com/?q=${encodeURIComponent(p)}`; if(/Android/i.test(navigator.userAgent)) location.href=androidIntent(u,'com.openai.chatgpt'); else window.open(u,'_blank','noopener,noreferrer'); }
  async function gemini(){ const p=researchPrompt(); await copyPrompt(); const u=`https://gemini.google.com/app?q=${encodeURIComponent(p)}`; if(/Android/i.test(navigator.userAgent)) location.href=androidIntent(u,'com.google.android.apps.bard'); else window.open(u,'_blank','noopener,noreferrer'); }

  async function namedSimbad(name){
    const q=`SELECT TOP 1 b.main_id,b.ra,b.dec,b.otype,b.rvz_redshift,b.rvz_radvel,b.galdim_majaxis,b.galdim_minaxis FROM basic AS b JOIN ident AS i ON b.oid=i.oidref WHERE i.id='${name.replace(/'/g,"''")}'`;
    const url='https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query='+encodeURIComponent(q);
    const r=await fetch(url); if(!r.ok) throw Error(`SIMBAD HTTP ${r.status}`); const j=await r.json();
    if(!j.data?.length) return null; const out={}; j.metadata.forEach((m,k)=>out[m.name]=j.data[0][k]); return out;
  }
  function unavailable(v){ return !v || /not available|pending|not returned|^hii$/i.test(v); }
  function distanceFromZ(z){ const n=Number(z); if(!Number.isFinite(n)||n<=0||n>0.1)return null; return n*299792.458/70*3.26156; }
  function physicalSize(majArcmin, distMly){ const a=Number(majArcmin),d=Number(distMly); if(!Number.isFinite(a)||!Number.isFinite(d))return null; return Math.round(d*1e6*a*Math.PI/(180*60)); }
  async function enrich(){
    const name=exactNames()[0]; if(!/^(NGC|IC|M|MESSIER|UGC|ARP|ESO)\s*[- ]?\d+/i.test(name)) return;
    try{
      const d=await namedSimbad(name); if(!d)return;
      if(unavailable(value('Morphological type')) && d.otype) setValue('Morphological type', String(d.otype));
      if(unavailable(value('Angular size')) && Number.isFinite(Number(d.galdim_majaxis))) {
        const maj=Number(d.galdim_majaxis), min=Number(d.galdim_minaxis);
        setValue('Angular size', Number.isFinite(min) ? `${maj.toFixed(3)} × ${min.toFixed(3)} arcmin` : `${maj.toFixed(3)} arcmin`);
      }
      if(unavailable(value('Radial velocity')) && Number.isFinite(Number(d.rvz_radvel))) setValue('Radial velocity', `${Number(d.rvz_radvel).toLocaleString()} km/s`);
      if(/not available/i.test(value('Redshift (z) / Distance')) && Number.isFinite(Number(d.rvz_redshift))) {
        const z=Number(d.rvz_redshift), mly=distanceFromZ(z);
        setValue('Redshift (z) / Distance', mly ? `${z.toFixed(8)} / ${mly.toFixed(2)} million ly — redshift estimate` : z.toFixed(8));
      }
      const angular=value('Angular size').match(/([0-9.]+)/); const distance=value('Redshift (z) / Distance').match(/\/\s*([0-9.]+)\s*million/i);
      if(unavailable(value('Physical size')) && angular && distance){ const s=physicalSize(angular[1],distance[1]); if(s) setValue('Physical size', `Approximately ${s.toLocaleString()} ly — calculated from angular size and redshift distance`); }
    }catch(_){ }
  }
  function install(){
    const root=document.getElementById('viewer14-root'); if(!root)return false;
    const h=root.querySelector('h3'); if(h)h.textContent='Galaxy Viewer — VIEWER-41';
    const c=document.getElementById('viewer37Chrome'); if(c)c.onclick=e=>{e.preventDefault();chrome();};
    const g=document.getElementById('viewer37Gemini'); if(g)g.onclick=e=>{e.preventDefault();gemini();};
    const a=document.getElementById('viewer37ChatGPT'); if(a)a.onclick=e=>{e.preventDefault();chatgpt();};
    enrich(); return true;
  }
  install(); const t=setInterval(install,300); setTimeout(()=>clearInterval(t),20000);
  const status=document.getElementById('viewer14Status'); if(status)new MutationObserver(()=>setTimeout(install,60)).observe(status,{childList:true,subtree:true});
})();
'''))
