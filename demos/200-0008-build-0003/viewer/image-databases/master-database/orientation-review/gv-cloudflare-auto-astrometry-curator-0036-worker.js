import gv0030 from './gv-cloudflare-auto-astrometry-curator-0030-worker.js';

const REV='0036';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:51:05 COT';
const BUILD_STAMP_ISO='2026-08-29T19:51:05-05:00';

const CLIENT_PATCH=String.raw`<style id="gv36-style">
#gv36DeployStamp{position:sticky;top:0;z-index:2147483647;box-sizing:border-box;width:100%;padding:5px 8px;background:#07131f;border-bottom:1px solid #2f8b60;color:#7dffb5;font:800 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;text-align:center}
#gv36DeployStamp strong{color:#fff}#gv36DeployStamp .now{color:#ffd166}
#gv36OrientationPanel{margin:0 0 6px!important;border-color:#9b8130!important;background:#161207!important}
#gv36OrientationTitle{margin:0 0 5px;color:#ffd166;font:900 10px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.5px}
#gv36MachineActivity{display:inline-flex;align-items:center;min-height:28px;padding:5px 8px;border:1px solid #42566f;border-radius:7px;background:#09121f;font:900 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:normal}
#gv36MachineActivity.busy{border-color:#9b8130;color:#ffd166;background:#2b240b}#gv36MachineActivity.good{border-color:#2f8b60;color:#57e39b;background:#0d2c20}#gv36MachineActivity.bad{border-color:#a94750;color:#ff8d8d;background:#351015}
button.gv36Busy{background:#ffd166!important;border-color:#ffe59a!important;color:#171000!important;box-shadow:0 0 16px #ffd16699!important;animation:gv36Pulse .8s ease-in-out infinite alternate!important;opacity:1!important}
button.gv36Success{background:#123d2a!important;border-color:#57e39b!important;color:#eafff4!important;box-shadow:0 0 14px #57e39b88!important;opacity:1!important}
button.gv36Fail{background:#4b171b!important;border-color:#ff7575!important;color:#fff1f1!important;box-shadow:0 0 14px #ff757588!important;opacity:1!important}
@keyframes gv36Pulse{from{filter:brightness(.90)}to{filter:brightness(1.18)}}
@media(max-width:700px){#gv36DeployStamp{font-size:9px;padding:4px 5px}#gv36MachineActivity{width:100%;font-size:9px;min-height:24px;padding:4px 6px}}
</style>
<div id="gv36DeployStamp" role="status" aria-live="polite"><strong>GV 0036 LIVE</strong> · BUILD 2026-08-29 19:51:05 COT · DIRECT GAIA BUTTON BINDING · <span class="now" id="gv36ColombiaClock">COLOMBIA NOW —</span></div>
<script>(()=>{'use strict';
let active=false,button=null,activity=null,lastManual=null;
function isMachineButton(b){return !!b&&b.tagName==='BUTTON'&&/APPLY MACHINE (?:ASTROMETRY|PREDICTION)|LEGACY SIFT DISABLED/i.test((b.textContent||'').trim())}
function findMachineButton(){return [...document.querySelectorAll('button')].find(isMachineButton)||null}
function ensureActivity(b){if(activity&&activity.isConnected)return activity;if(!b)return null;activity=document.getElementById('gv36MachineActivity');if(!activity){activity=document.createElement('span');activity.id='gv36MachineActivity';activity.setAttribute('role','status');activity.setAttribute('aria-live','assertive');activity.textContent='MACHINE READY — PRESS TO SOLVE';b.insertAdjacentElement('afterend',activity)}return activity}
function setActivity(text,kind=''){const a=ensureActivity(button||findMachineButton());if(a){a.className=kind;a.textContent=text}}
function readManualAngle(){const d=Number(document.getElementById('rotDeg')?.value);if(Number.isFinite(d))return d;const r=Number(document.getElementById('rotRange')?.value);return Number.isFinite(r)?r:null}
function ensureLayout(){const compare=document.querySelector('main > section.compare')||document.querySelector('.compare');const readouts=document.querySelector('main > section.readouts')||document.querySelector('.readouts');const rot=document.getElementById('rotRange');const rotRow=rot?.closest?.('.controls');if(!compare||!readouts||!rotRow)return false;let panel=document.getElementById('gv36OrientationPanel');if(!panel){panel=document.createElement('section');panel.id='gv36OrientationPanel';panel.className='panel';const title=document.createElement('div');title.id='gv36OrientationTitle';title.textContent='ORIENTATION / ANGLE ADJUSTMENT';panel.appendChild(title)}if(rotRow.parentElement!==panel)panel.appendChild(rotRow);if(compare.nextElementSibling!==panel)compare.insertAdjacentElement('afterend',panel);if(panel.nextElementSibling!==readouts)panel.insertAdjacentElement('afterend',readouts);panel.dataset.gv36Layout='LOCKED: images -> orientation -> readouts';return true}
function paintTap(b){button=b;ensureActivity(b);lastManual=readManualAngle();window.__gv0036ManualRotationHint=lastManual;b.classList.add('gv36Busy');setActivity('● TAP RECEIVED · MANUAL START '+(Number.isFinite(lastManual)?lastManual.toFixed(1)+'°':'UNKNOWN')+' · CLICK WILL START GAIA','busy')}
function paintBusy(b){button=b;b.classList.remove('gv36Success','gv36Fail');b.classList.add('gv36Busy');b.textContent='★ MACHINE SOLVING… DO NOT PRESS';b.setAttribute('aria-busy','true');b.disabled=true;setActivity('● GAIA MACHINE SOLVER STARTED · MANUAL ORIENTATION '+(Number.isFinite(lastManual)?lastManual.toFixed(1)+'°':'PRESERVED'),'busy')}
function restore(){if(!button||!button.isConnected)button=findMachineButton();if(!button)return;button.classList.remove('gv36Busy','gv36Success','gv36Fail');button.textContent='★ APPLY MACHINE ASTROMETRY';button.disabled=false;button.removeAttribute('aria-busy');setActivity('MACHINE READY — PRESS TO SOLVE','')}
function finish(ok,msg){active=false;if(!button||!button.isConnected)button=findMachineButton();if(!button)return;button.disabled=false;button.removeAttribute('aria-busy');button.classList.remove('gv36Busy');button.classList.add(ok?'gv36Success':'gv36Fail');button.textContent=ok?'✓ MACHINE SOLVED — APPLIED':'✕ MACHINE SOLVE FAILED — RETRY';setActivity(msg,ok?'good':'bad');setTimeout(restore,ok?2500:5000)}
window.addEventListener('pointerdown',e=>{const b=e.target?.closest?.('button');if(!isMachineButton(b)||active)return;paintTap(b)},true);
window.addEventListener('click',e=>{const b=e.target?.closest?.('button');if(!isMachineButton(b)||active)return;e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();button=b;lastManual=readManualAngle();if(typeof window.__gv0036Solve!=='function'){finish(false,'✕ SOLVER EXPORT MISSING — MACHINE DID NOT START');return}active=true;const log=document.getElementById('analysisLog');if(log)log.textContent='[0036] MACHINE CLICK ACCEPTED · MANUAL ROTATION '+(Number.isFinite(lastManual)?lastManual.toFixed(1)+'°':'UNKNOWN')+' · STARTING GAIA';let p;try{p=window.__gv0036Solve();paintBusy(b)}catch(err){finish(false,'✕ MACHINE START FAILED — '+String(err?.message||err));return}Promise.resolve(p).then(()=>finish(true,'✓ MACHINE SOLVER RETURNED — SEE GAIA VALIDATION / LIVE ALADIN')).catch(err=>finish(false,'✕ MACHINE SOLVE FAILED — '+String(err?.message||err)))},true);
function normalizeButton(){if(active)return;const b=findMachineButton();if(!b)return;button=b;ensureActivity(b);if(!/APPLY MACHINE ASTROMETRY/i.test(b.textContent||''))b.textContent='★ APPLY MACHINE ASTROMETRY';if(!/LOADING|POSITIONING|ANALYZING/i.test(document.getElementById('status')?.textContent||''))b.disabled=false}
ensureLayout();normalizeButton();setInterval(()=>{ensureLayout();normalizeButton()},250);
const clock=document.getElementById('gv36ColombiaClock'),fmt=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});function tickClock(){if(clock)clock.textContent='COLOMBIA NOW '+fmt.format(new Date())+' COT'}tickClock();setInterval(tickClock,1000);
console.log('[GV0036] direct window-capture machine binding installed; 0031-0035 bypassed');
})();</script>`;

function normalizeIdentity(html){return html
  .replaceAll('GV 0030 LIVE','GV 0036 LIVE')
  .replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0030','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0036')
  .replaceAll('2026-08-29 19:22:14 COT',BUILD_STAMP_COLOMBIA)}
function exportSolver(html){
  if(!html.includes('gv0030SolveAndApply'))return null;
  const marker='boot();';const i=html.lastIndexOf(marker);if(i<0)return null;
  return html.slice(0,i)+"window.__gv0036Solve=gv0030SolveAndApply;window.__gv0036SolverExportInstalled=true;console.log('[GV0036] same-scope Gaia solver exported');\n"+html.slice(i)
}
function injectBeforeBodyEnd(html){const i=html.lastIndexOf('</body>');if(i<0)return null;return html.slice(0,i)+CLIENT_PATCH+html.slice(i)}

async function page(request,env){
  const r=await gv0030.fetch(request,env);let h=normalizeIdentity(await r.text());h=exportSolver(h);if(h==null)return new Response('0036 STARTUP ERROR: same-scope Gaia solver export anchor missing',{status:500});const out=injectBeforeBodyEnd(h);if(out==null)return new Response('0036 STARTUP ERROR: body anchor missing',{status:500});const headers=new Headers(r.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('pragma','no-cache');headers.set('expires','0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-machine-binding','window-capture-direct-export');headers.set('x-gv-layout-order','images-orientation-source-live-locked');headers.set('x-gv-manual-orientation','preserved-until-verified-solver-result');return new Response(out,{status:r.status,headers})
}
async function health(request,env){const r=await gv0030.fetch(request,env);let data={};try{data=await r.json()}catch{}data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0036',direct_from:'0030',bypasses:['0031','0032','0033','0034','0035'],build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',machine_binding:'window-capture-direct-to-exported-gv0030SolveAndApply',pointerdown_changes_label:false,manual_orientation_on_machine_start:'preserved',layout_order:['images','orientation-angle-controls','source-image-data','live-validation-data'],layout_lock:'250ms-enforcement',solver_export_required:true};return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}})}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(request,env);return gv0030.fetch(request,env)}};
