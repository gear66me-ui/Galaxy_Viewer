from IPython.display import HTML, Javascript, display

# GV-beta-200-0001
# Clean Random Galaxy baseline:
# Aladin Lite + catalog data + Random Galaxy 0240 only.
# No Navigation module. No AVM module. No preparation/prefetch/travel modules.

display(HTML(r"""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.css">
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#gv200{position:relative;width:100%;height:100vh;height:100dvh;background:#000;overflow:hidden}
#gv200-aladin{position:absolute;inset:0}
#gv200-random-host{position:absolute;inset:0;z-index:7300;pointer-events:none}
#gv200-random{position:absolute;left:50%;bottom:16px;z-index:7600;transform:translateX(-50%);pointer-events:auto;border:1px solid #7ccbff;border-radius:8px;background:linear-gradient(145deg,#071a38,#0d4278);color:#fff;padding:10px 16px;font:700 13px/1.1 system-ui,sans-serif;letter-spacing:1px}
#gv200-status{position:absolute;left:12px;top:12px;z-index:7600;padding:7px 9px;border-radius:6px;background:rgba(0,0,0,.72);color:#9be5ff;font:11px/1.3 monospace;pointer-events:none}
</style>
<div id="gv200">
  <div id="gv200-aladin"></div>
  <div id="gv200-random-host"></div>
  <button id="gv200-random" type="button">RANDOM GALAXY</button>
  <div id="gv200-status">GV-beta-200-0001 — LOADING</div>
</div>
"""))

display(Javascript(r"""
(async()=>{
'use strict';
const VERSION='GV-beta-200-0001';
const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
const RANDOM_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/random-galaxy/gv-random-galaxy-0240.js';
const MASTER_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/gv-master-catalog-0003-AVM.json';
const RAW_ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
const status=document.getElementById('gv200-status');
const button=document.getElementById('gv200-random');
const host=document.getElementById('gv200-random-host');

function say(v){status.textContent=String(v);console.log('[GV200]',v)}
function loadScript(url){return new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=url+'?v='+Date.now();s.onload=()=>resolve(s);s.onerror=()=>reject(new Error('SCRIPT LOAD FAILED '+url));document.head.appendChild(s)})}
async function json(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status+' '+url);return r.json()}
function number(v){const n=Number(v);return Number.isFinite(n)?n:null}
function imageOf(c){const x=[...(Array.isArray(c?.jpegCandidates)?c.jpegCandidates:[]),c?.selectedImageUrl,c?.hdUrl,c?.hd_url,c?.githubImageUrl,c?.github_image_url].map(v=>String(v||'').trim()).filter(Boolean);return x.find(v=>/\/screen\//i.test(v))||x[0]||''}
function fovOf(c){return [c?.fov,c?.fovDegrees,c?.fieldOfView,c?.fieldOfViewDegrees,c?.imageFovDegrees].map(number).find(v=>v>0)||0.15}
function normalize(c,i,key,meta){
  if(!c||typeof c!=='object')return null;
  const ra=number(c.ra),dec=number(c.dec),hdUrl=imageOf(c);
  if(ra==null||ra<0||ra>=360||dec==null||dec<-90||dec>90||!hdUrl)return null;
  const name=String(c.displayName||c.commonName||c.common_name||c.name||c.title||c.objectName||c.designation||('GALAXY '+(i+1))).trim();
  return Object.freeze({...c,name,ra,dec,fov:fovOf(c),hdUrl,provider:String(c.provider||meta.provider||key||'').trim(),telescope:String(c.telescope||c.facility||meta.telescope||meta.facility||'').trim(),constellation:String(c.constellation||'').trim(),designation:String(c.designation||'').trim(),commonName:String(c.commonName||c.common_name||c.displayName||name).trim()});
}
async function catalog(){
  const master=await json(MASTER_URL),pointers=Object.entries(master?.catalogs||{}),all=[];
  if(!pointers.length)throw new Error('MASTER CATALOG HAS NO POINTERS');
  await Promise.all(pointers.map(async([key,path])=>{try{const payload=await json(new URL(String(path),RAW_ROOT).href);const meta={provider:String(payload?.provider||''),telescope:String(payload?.telescope||''),facility:String(payload?.facility||'')};for(const [i,c] of (payload?.entries||[]).entries()){const g=normalize(c,i,key,meta);if(g)all.push(g)}}catch(e){console.warn('[GV200] CATALOG SKIPPED',key,e)}}));
  if(!all.length)throw new Error('NO TARGETABLE GALAXIES');
  for(let i=all.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[all[i],all[j]]=[all[j],all[i]]}
  return all;
}
try{
  say(VERSION+' — ALADIN');
  await loadScript(ALADIN_URL); await A.init;
  const aladin=A.aladin('#gv200-aladin',{survey:'P/DSS2/color',target:'M 31',fov:1.5,cooFrame:'ICRS',projection:'TAN',showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true});
  say(VERSION+' — CATALOGS');
  const galaxies=await catalog();
  say(VERSION+' — RANDOM 0240');
  await loadScript(RANDOM_URL);
  if(window.GalaxyRandomGalaxy?.VERSION!=='0240')throw new Error('RANDOM GALAXY 0240 EXPORT MISSING');
  const randomGalaxy=window.GalaxyRandomGalaxy.mount(host,{aladin,catalog:galaxies,randomButton:button});
  window.GV200=Object.freeze({VERSION,aladin,galaxies,randomGalaxy});
  say(VERSION+' — READY — '+galaxies.length+' GALAXIES');
}catch(error){console.error(error);say(VERSION+' — ERROR — '+(error?.message||error));button.disabled=true}
})();
"""))
