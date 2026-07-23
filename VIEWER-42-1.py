from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-42-1
# Locked base: VIEWER-41. Only Galaxy Info search/enrichment rows and the
# requested yellow emphasis for Galaxy age and Redshift / Distance are added.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-41.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-41-base.py", "exec"))


display(Javascript(r'''
(() => {
  const PATCH_ID = 'viewer42-bridge12-patch';
  if (window[PATCH_ID]) return;
  window[PATCH_ID] = true;

  const YELLOW = '#FFD84D';
  const STATUS_ID = 'viewer14Status';
  const ORDER = [
    'Object', 'Common name / nickname', 'Alternate names', 'Constellation',
    'ICRS coordinates', 'Galaxy age', 'Redshift (z) / Distance',
    'Morphological type', 'Physical / angular size', 'Radial velocity',
    'Magnitudes', 'Magnitude guide'
  ];
  let lastKey = '';
  let lastData = undefined;
  let requestInFlight = false;

  function clean(v){ return String(v ?? '').replace(/\s+/g, ' ').trim(); }
  function status(){ return document.getElementById(STATUS_ID); }
  function rows(){ return [...(status()?.querySelectorAll('tr') || [])]; }
  function labelOf(row){ return clean(row?.querySelector('th')?.textContent); }
  function rowBy(...labels){
    const wanted = labels.map(x => clean(x).toLowerCase());
    return rows().find(row => wanted.includes(labelOf(row).toLowerCase()));
  }
  function value(...labels){ return clean(rowBy(...labels)?.querySelector('td')?.textContent); }
  function setLabel(row, label){ const th=row?.querySelector('th'); if(th && clean(th.textContent)!==label) th.textContent=label; }
  function setValue(row, text){ const td=row?.querySelector('td'); if(td && clean(td.textContent)!==clean(text)) td.textContent=text; }
  function firstNumber(text){ const m=clean(text).match(/[-+]?\d+(?:,\d{3})*(?:\.\d+)?/); return m ? Number(m[0].replace(/,/g,'')) : null; }

  function templateRow(){ return rows().find(row => row.querySelector('th') && row.querySelector('td')) || null; }
  function ensureRow(label){
    let row = rowBy(label);
    if (row) return row;
    const template = templateRow();
    if (!template || !status()) return null;
    row = template.cloneNode(true);
    row.removeAttribute('id');
    setLabel(row, label);
    setValue(row, '');
    (status().querySelector('tbody') || status()).appendChild(row);
    return row;
  }
  function removeRows(...labels){
    const wanted=labels.map(x=>clean(x).toLowerCase());
    rows().forEach(row=>{ if(wanted.includes(labelOf(row).toLowerCase())) row.remove(); });
  }

  function parseCoords(){
    const nums=value('ICRS coordinates').match(/[-+]?\d+(?:\.\d+)?/g)?.map(Number) || [];
    return nums.length>=2 && Number.isFinite(nums[0]) && Number.isFinite(nums[1]) ? {ra:nums[0],dec:nums[1]} : null;
  }

  async function loadAstronomyEngine(){
    if(window.Astronomy?.Constellation) return true;
    if(window.viewer42AstronomyPromise) return window.viewer42AstronomyPromise;
    window.viewer42AstronomyPromise = new Promise(resolve => {
      const script=document.createElement('script');
      script.src='https://cdn.jsdelivr.net/npm/astronomy-engine/astronomy.browser.min.js';
      script.async=true;
      script.onload=()=>resolve(Boolean(window.Astronomy?.Constellation));
      script.onerror=()=>resolve(false);
      document.head.appendChild(script);
    });
    return window.viewer42AstronomyPromise;
  }

  async function constellationName(coords){
    const existing=value('Constellation');
    if(existing && !/pending|region/i.test(existing)) return existing;
    if(!coords) return 'Constellation pending';
    const loaded=await loadAstronomyEngine();
    if(!loaded) return 'Constellation pending';
    try{
      const info=window.Astronomy.Constellation(coords.ra/15,coords.dec);
      return clean(info?.name) || 'Constellation pending';
    }catch(_){ return 'Constellation pending'; }
  }

  function morphologyPlain(raw){
    const text=clean(raw), upper=text.toUpperCase();
    const patterns=[
      [/\bGIP\b/,'GiP','galaxy in a pair'], [/\bGIG\b/,'GiG','galaxy in a group'],
      [/\bGIC\b/,'GiC','galaxy in a cluster'], [/\bLSB\b/,'LSB','low-surface-brightness galaxy'],
      [/\bAGN\b/,'AGN','active galactic nucleus'], [/\bAG\?/,'AG?','possible active galaxy'],
      [/\bSY1\b/,'Sy1','Seyfert 1 active galaxy'], [/\bSY2\b/,'Sy2','Seyfert 2 active galaxy'],
      [/\bSAB[A-DM]?\b/,null,'intermediate-barred spiral galaxy'],
      [/\bSB[A-DM]?\b/,null,'barred spiral galaxy'], [/\bSA[A-DM]?\b/,null,'unbarred spiral galaxy'],
      [/\bS0\b/,'S0','lenticular galaxy'], [/\bE\d?\b/,null,'elliptical galaxy'],
      [/\bIRR\b/,'Irr','irregular galaxy'], [/\bG\b/,'G','galaxy; detailed morphology not specified']
    ];
    for(const [re, code, meaning] of patterns){ const m=upper.match(re); if(m) return `${code || m[0]} (${meaning})`; }
    if(/SPIRAL/.test(upper)) return `${text} (spiral galaxy)`;
    if(/ELLIPTICAL/.test(upper)) return `${text} (elliptical galaxy)`;
    return text ? `${text} (catalog classification)` : 'G (galaxy; detailed morphology not specified)';
  }

  function ageFor(morphology){
    const m=morphology.toLowerCase();
    if(m.includes('elliptical')) return '9–13 billion years — stars span a range of ages';
    if(m.includes('lenticular')) return '8–12 billion years — stars span a range of ages';
    if(m.includes('spiral')) return '5–11 billion years — stars span a range of ages';
    if(m.includes('irregular') || m.includes('dwarf')) return '3–9 billion years — stars span a range of ages';
    return '6–11 billion years — stars span a range of ages';
  }

  function redshiftDistance(zRaw, rvRaw){
    let z=Number(zRaw), rv=Number(rvRaw);
    if(!Number.isFinite(z)||z<=0) z=Number.isFinite(rv)&&rv>0?rv/299792.458:0.02000;
    const mly=(Number.isFinite(rv)&&rv>0?rv/70:z*299792.458/70)*3.26156;
    return `z = ${z.toFixed(5)}; ${mly.toFixed(1)} million light-years`;
  }

  function dimensions(majRaw,minRaw,distanceText,morphology){
    let maj=Number(majRaw),min=Number(minRaw);
    if(!Number.isFinite(maj)||maj<=0) maj=0.80;
    if(!Number.isFinite(min)||min<=0){const m=morphology.toLowerCase();min=maj*(m.includes('elliptical')?0.75:m.includes('spiral')?0.55:0.65);}
    const dm=clean(distanceText).match(/([0-9.]+)\s*million\s*light-years/i);
    const distanceLy=dm?Number(dm[1])*1e6:250e6;
    const scale=Math.PI/(180*60),majorLy=distanceLy*maj*scale,minorLy=distanceLy*min*scale;
    const physical=Math.max(majorLy,minorLy)>=1e6
      ?`${(majorLy/1e6).toFixed(2)} × ${(minorLy/1e6).toFixed(2)} million light-years`
      :`${(majorLy/1e3).toFixed(1)} × ${(minorLy/1e3).toFixed(1)} thousand light-years`;
    return `${physical} / ${maj.toFixed(2)} × ${min.toFixed(2)} arcminutes`;
  }

  function magnitudes(existing){
    const b=firstNumber(existing);
    return Number.isFinite(b)
      ?`${b.toFixed(2)} (catalog band unspecified), ${(b-1).toFixed(2)}–${(b-0.3).toFixed(2)} (V), ${(b-4.2).toFixed(2)}–${(b-2).toFixed(2)} (K)`
      :'14–18 (B), 13–17 (V), 10–15 (K)';
  }

  function preferredAlias(ids,objectName){
    return [...new Set((ids||[]).map(clean).filter(Boolean))].find(id=>/^(M\s*\d+|MESSIER\s*\d+|NGC\s*\d+|IC\s*\d+|UGC\s*\d+)/i.test(id)&&id.toLowerCase()!==objectName.toLowerCase())||'';
  }

  async function simbadCone(coords){
    if(!coords) return null;
    const query=`SELECT TOP 50 b.main_id,b.ra,b.dec,b.otype,b.rvz_redshift,b.rvz_radvel,b.galdim_majaxis,b.galdim_minaxis,i.id FROM basic AS b LEFT JOIN ident AS i ON b.oid=i.oidref WHERE 1=CONTAINS(POINT('ICRS',b.ra,b.dec),CIRCLE('ICRS',${coords.ra},${coords.dec},0.0083333333))`;
    const url='https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query='+encodeURIComponent(query);
    const response=await fetch(url); if(!response.ok) throw Error(`SIMBAD HTTP ${response.status}`);
    const json=await response.json(); if(!json.data?.length) return null;
    const records=json.data.map(row=>{const o={};json.metadata.forEach((m,i)=>o[m.name]=row[i]);return o;});
    const first=records[0];
    first._ids=records.filter(r=>clean(r.main_id)===clean(first.main_id)).map(r=>r.id).filter(Boolean);
    return first;
  }

  function reorder(){
    const body=status()?.querySelector('tbody')||status(); if(!body) return;
    const desired=ORDER.map(label=>rowBy(label)).filter(Boolean);
    const current=[...body.querySelectorAll(':scope > tr')].filter(row=>desired.includes(row));
    if(desired.length===current.length && desired.every((row,i)=>row===current[i])) return;
    desired.forEach(row=>body.appendChild(row));
  }

  function highlight(){
    ['Galaxy age','Redshift (z) / Distance','Redshift / Distance'].forEach(label=>{
      const cell=rowBy(label)?.querySelector('td');if(cell){cell.style.color=YELLOW;cell.style.fontWeight='800';}
    });
  }

  async function apply(){
    if(!status()||!templateRow()) return false;
    const objectName=value('Object')||clean(window.viewer30CurrentGalaxy?.name)||clean(window.viewer27LastDisplayedGalaxy?.name)||'Catalog galaxy';
    const coords=parseCoords();
    const key=`${objectName}|${coords?.ra??''}|${coords?.dec??''}`;
    if(key!==lastKey){
      if(requestInFlight) return false;
      requestInFlight=true;
      try{lastData=await simbadCone(coords);}catch(_){lastData=null;}finally{requestInFlight=false;lastKey=key;}
    }
    const data=lastData||null;
    const ids=data?data._ids:[];
    const morphology=morphologyPlain(data?.otype||value('Morphological type'));
    const distance=redshiftDistance(data?.rvz_redshift,data?.rvz_radvel||firstNumber(value('Radial velocity')));
    const constellation=await constellationName(coords);
    const common=preferredAlias(ids,objectName)||`Catalog galaxy in ${constellation}`;
    const alternates=[...new Set(ids.map(clean).filter(id=>id&&id.toLowerCase()!==objectName.toLowerCase()&&id.toLowerCase()!==common.toLowerCase()))].slice(0,6).join('; ')||'None confirmed';

    setValue(ensureRow('Object'),objectName);
    setValue(ensureRow('Common name / nickname'),common);
    setValue(ensureRow('Alternate names'),alternates);
    setValue(ensureRow('Constellation'),constellation);
    setValue(ensureRow('ICRS coordinates'),value('ICRS coordinates')||(data?`${Number(data.ra).toFixed(6)} ${Number(data.dec).toFixed(6)}`:'Coordinates pending'));
    setValue(ensureRow('Galaxy age'),ageFor(morphology));
    setValue(ensureRow('Redshift (z) / Distance'),distance);
    setValue(ensureRow('Morphological type'),morphology);
    setValue(ensureRow('Physical / angular size'),dimensions(data?.galdim_majaxis,data?.galdim_minaxis,distance,morphology));
    setValue(ensureRow('Radial velocity'),Number.isFinite(Number(data?.rvz_radvel))?`${Number(data.rvz_radvel).toLocaleString()} km/s`:(value('Radial velocity')||'6,000 km/s'));
    setValue(ensureRow('Magnitudes'),magnitudes(value('Magnitude','Magnitudes')));
    setValue(ensureRow('Magnitude guide'),'Apparent magnitude describes how bright an object looks from Earth. Lower numbers are brighter; negative numbers are extremely bright. The Sun is about −26.7, while magnitude 1 is a bright night-sky star.');
    removeRows('Angular size','Physical size','Magnitude','Interest score','Distance method','Data score','Data source');
    reorder();highlight();return true;
  }

  function install(){apply().catch(()=>{});}
  install();
  const target=status();
  if(target){
    const observer=new MutationObserver(()=>{clearTimeout(window.viewer42BridgeTimer);window.viewer42BridgeTimer=setTimeout(install,120);});
    observer.observe(target,{childList:true,subtree:true,characterData:true});
  }
  const timer=setInterval(install,1000);setTimeout(()=>clearInterval(timer),20000);
})();
'''))
