import gv0034 from './gv-cloudflare-auto-astrometry-curator-0034-worker.js';

const REV='0035';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:42:55 COT';
const BUILD_STAMP_ISO='2026-08-29T19:42:55-05:00';

const PATCH=String.raw`<style id="gv35-lock-style">
#gv35ManualHint{margin-left:6px;color:#ffd166;font:900 9px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace}
</style>
<script>(()=>{'use strict';
let cleanButton=null,lastHint=null;
function isMachineButton(b){return !!b&&b.tagName==='BUTTON'&&/APPLY MACHINE (?:ASTROMETRY|PREDICTION)|MACHINE SOLVING|TAP RECEIVED/i.test((b.textContent||'').trim())}
function ensureLayout(){
  const compare=document.querySelector('main > section.compare')||document.querySelector('.compare');
  const readouts=document.querySelector('main > section.readouts')||document.querySelector('.readouts');
  const rot=document.getElementById('rotRange');
  const rotRow=rot?.closest?.('.controls');
  if(!compare||!readouts||!rotRow)return false;
  let panel=document.getElementById('gv34OrientationPanel')||document.getElementById('gv35OrientationPanel');
  if(!panel){panel=document.createElement('section');panel.id='gv35OrientationPanel';panel.className='panel';const t=document.createElement('div');t.id='gv34OrientationTitle';t.textContent='ORIENTATION / ANGLE ADJUSTMENT';panel.appendChild(t)}
  if(rotRow.parentElement!==panel)panel.appendChild(rotRow);
  if(compare.nextElementSibling!==panel)compare.insertAdjacentElement('afterend',panel);
  if(panel.nextElementSibling!==readouts)panel.insertAdjacentElement('afterend',readouts);
  panel.dataset.gv35Layout='LOCKED: images -> orientation -> readouts';
  return true;
}
function installCleanMachineButton(){
  let b=[...document.querySelectorAll('button')].find(isMachineButton)||document.querySelector('button[data-gv-machine-button="1"]');
  if(!b)return false;
  if(b.dataset.gv35Clean==='1'){cleanButton=b;return true}
  const c=b.cloneNode(true);
  c.dataset.gv35Clean='1';
  c.dataset.gvMachineButton='1';
  b.replaceWith(c);
  cleanButton=c;
  c.addEventListener('pointerdown',e=>{e.stopImmediatePropagation();e.stopPropagation()},true);
  c.addEventListener('click',e=>{e.stopImmediatePropagation();e.stopPropagation()},true);
  console.log('[GV0035][BUTTON] legacy direct/bubble machine handler stripped; document-capture Gaia handler preserved');
  return true;
}
function readManualAngle(){const d=Number(document.getElementById('rotDeg')?.value);if(Number.isFinite(d))return d;const r=Number(document.getElementById('rotRange')?.value);return Number.isFinite(r)?r:null}
function showHint(v){
  const panel=document.getElementById('gv34OrientationPanel')||document.getElementById('gv35OrientationPanel');if(!panel)return;
  let el=document.getElementById('gv35ManualHint');if(!el){el=document.createElement('span');el.id='gv35ManualHint';panel.appendChild(el)}
  el.textContent=Number.isFinite(v)?'MACHINE START HINT: '+v.toFixed(1)+'° · MANUAL ORIENTATION PRESERVED':'MANUAL ORIENTATION PRESERVED';
}
document.addEventListener('pointerdown',e=>{const b=e.target?.closest?.('button');if(!isMachineButton(b))return;lastHint=readManualAngle();window.__gv0035ManualRotationHint=lastHint;showHint(lastHint)},true);
function enforce(){ensureLayout();installCleanMachineButton()}
enforce();setInterval(enforce,500);
console.log('[GV0035] permanent orientation-row lock + manual-orientation-preserving machine button installed');
})();</script>`;

function normalizeIdentity(html){
  return html
    .replaceAll('GV 0034 LIVE','GV 0035 LIVE')
    .replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0034','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0035')
    .replaceAll('2026-08-29 19:39:04 COT',BUILD_STAMP_COLOMBIA)
    .replaceAll('2026-08-29 19:38:03 COT',BUILD_STAMP_COLOMBIA)
    .replaceAll('2026-08-29 19:33:28 COT',BUILD_STAMP_COLOMBIA)
    .replaceAll('2026-08-29 19:22:14 COT',BUILD_STAMP_COLOMBIA);
}
function injectBeforeBodyEnd(html){const i=html.lastIndexOf('</body>');if(i<0)return null;return html.slice(0,i)+PATCH+html.slice(i)}

async function page(request,env){
  const r=await gv0034.fetch(request,env);let h=normalizeIdentity(await r.text());const out=injectBeforeBodyEnd(h);
  if(out==null)return new Response('0035 STARTUP ERROR: body anchor missing',{status:500});
  const headers=new Headers(r.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('pragma','no-cache');headers.set('expires','0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-layout-order','images-orientation-source-live-locked');headers.set('x-gv-manual-orientation','preserved-on-machine-start');
  return new Response(out,{status:r.status,headers});
}
async function health(request,env){
  const r=await gv0034.fetch(request,env);let data={};try{data=await r.json()}catch{}
  data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0035',inherited_from:'0034',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',layout_order:['images','orientation-angle-controls','source-image-data','live-validation-data'],layout_lock:'continuous-500ms-enforcement',manual_orientation_on_machine_start:'preserved',legacy_machine_button_handler:'stripped-by-clean-clone',manual_rotation_hint:'captured-before-machine-solve'};
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}})
}
export default {async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(request,env);return gv0034.fetch(request,env)}};
