import gv0030 from './gv-cloudflare-auto-astrometry-curator-0030-worker.js';

const REV='0038';
const BUILD_STAMP_COLOMBIA='2026-08-29 20:07:05 COT';
const BUILD_STAMP_ISO='2026-08-29T20:07:05-05:00';

const APPLY_ANCHOR="function applyState(st){if(!st||!aladin||st.ra===null||st.dec===null)return false;";
const APPLY_REPLACEMENT="function applyState(st){const gv38Verified=/GAIA VERIFIED/i.test(document.querySelector('#predConfidence')?.textContent||'');if(window.__gv0038PreSolveLock&&!gv38Verified){console.log('[GV0038][GUARD] blocked pre-verified applyState',st);return true}if(gv38Verified)window.__gv0038PreSolveLock=false;if(!st||!aladin||st.ra===null||st.dec===null)return false;";
const ROT_ANCHOR="function setRot(v){const r=norm(v);";
const ROT_REPLACEMENT="function setRot(v){const gv38Verified=/GAIA VERIFIED/i.test(document.querySelector('#predConfidence')?.textContent||'');if(window.__gv0038PreSolveLock&&!gv38Verified){console.log('[GV0038][GUARD] blocked pre-verified setRot',v);return}if(gv38Verified)window.__gv0038PreSolveLock=false;const r=norm(v);";

const CLIENT_PATCH=String.raw`<style id="gv38-style">
#gv38OrientationPanel{margin:0 0 6px!important;border-color:#9b8130!important;background:#161207!important}
#gv38OrientationTitle{margin:0 0 5px;color:#ffd166;font:900 10px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.5px}
#gv38MachineActivity{display:block;margin:5px 0;padding:6px 8px;border:1px solid #42566f;border-radius:7px;background:#09121f;font:900 10px/1.35 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:normal}
#gv38MachineActivity.busy{border-color:#9b8130;color:#ffd166;background:#2b240b}#gv38MachineActivity.good{border-color:#2f8b60;color:#57e39b;background:#0d2c20}#gv38MachineActivity.bad{border-color:#a94750;color:#ff8d8d;background:#351015}
button.gv38Tap{background:#ffd166!important;border-color:#ffe59a!important;color:#171000!important;box-shadow:0 0 16px #ffd16699!important;opacity:1!important}
@media(max-width:700px){#gv38MachineActivity{font-size:9px;padding:5px 6px}}
</style>
<script>(()=>{'use strict';
let machineButton=null,startView=null,startedAt=0,watch=null;
function isMachineButton(b){return !!b&&b.tagName==='BUTTON'&&/APPLY MACHINE (?:ASTROMETRY|PREDICTION)|LEGACY SIFT DISABLED|MACHINE SOLVING/i.test((b.textContent||'').trim())}
function findMachineButton(){return [...document.querySelectorAll('button')].find(isMachineButton)||document.querySelector('button[data-gv0030-machine="1"],button[data-gv-machine-button="1"]')||null}
function numText(sel){const n=Number(String(document.querySelector(sel)?.textContent||'').replace(/[^0-9+\-.eE]/g,''));return Number.isFinite(n)?n:null}
function readStartView(){const rotInput=Number(document.getElementById('rotDeg')?.value),rotRange=Number(document.getElementById('rotRange')?.value);return{ra:numText('#liveRa'),dec:numText('#liveDec'),fov:numText('#liveFov'),rot:Number.isFinite(rotInput)?rotInput:(Number.isFinite(rotRange)?rotRange:null),capturedAt:new Date().toISOString()}}
function ensureActivity(){let a=document.getElementById('gv38MachineActivity');if(a)return a;const b=machineButton||findMachineButton();if(!b)return null;a=document.createElement('div');a.id='gv38MachineActivity';a.setAttribute('role','status');a.setAttribute('aria-live','assertive');a.textContent='MACHINE READY — MANUAL VIEW WILL BE PRESERVED UNTIL GAIA VERIFIES';b.insertAdjacentElement('afterend',a);return a}
function activity(text,kind=''){const a=ensureActivity();if(a){a.className=kind;a.textContent=text}}
function ensureLayout(){const compare=document.querySelector('main > section.compare')||document.querySelector('.compare');const readouts=document.querySelector('main > section.readouts')||document.querySelector('.readouts');const rot=document.getElementById('rotRange'),row=rot?.closest?.('.controls');if(!compare||!readouts||!row)return false;let panel=document.getElementById('gv38OrientationPanel');if(!panel){panel=document.createElement('section');panel.id='gv38OrientationPanel';panel.className='panel';const t=document.createElement('div');t.id='gv38OrientationTitle';t.textContent='ORIENTATION / ANGLE ADJUSTMENT';panel.appendChild(t)}if(row.parentElement!==panel)panel.appendChild(row);if(compare.nextElementSibling!==panel)compare.insertAdjacentElement('afterend',panel);if(panel.nextElementSibling!==readouts)panel.insertAdjacentElement('afterend',readouts);panel.dataset.gv38Layout='LOCKED: images -> orientation -> source/live readouts';return true}
function fmt(v,d){return Number.isFinite(v)?v.toFixed(d):'—'}
function arm(b){machineButton=b;startView=readStartView();window.__gv0038ManualStart=startView;window.__gv0038PreSolveLock=true;startedAt=Date.now();b.classList.add('gv38Tap');activity('● START VIEW LOCKED · RA '+fmt(startView.ra,6)+' · DEC '+fmt(startView.dec,6)+' · FOV '+fmt(startView.fov,6)+'° · ROT '+fmt(startView.rot,1)+'° · WAITING FOR GAIA','busy');console.log('[GV0038][START] manual center/FOV/rotation preserved',startView);clearInterval(watch);watch=setInterval(checkState,150)}
function release(kind,text){window.__gv0038PreSolveLock=false;if(machineButton?.isConnected)machineButton.classList.remove('gv38Tap');clearInterval(watch);watch=null;activity(text,kind)}
function checkState(){const pred=document.querySelector('#predConfidence')?.textContent||'',score=document.querySelector('#score')?.textContent||'',gate=document.querySelector('#gv29Gate')?.textContent||document.querySelector('#targetGate')?.textContent||'',status=document.querySelector('#status')?.textContent||'';if(/GAIA VERIFIED/i.test(pred)){release('good','✓ GAIA VERIFIED · PRE-SOLVE LOCK RELEASED · APPLYING SOLVED RA / DEC / FOV / ROTATION');return}if(/FAILED CLOSED|MACHINE FAILED|SOLVE-FAIL/i.test(score+' '+gate+' '+status)){release('bad','✕ MACHINE FAILED CLOSED · MANUAL CENTER / FOV / ROTATION LEFT UNCHANGED');return}if(startedAt&&Date.now()-startedAt>90000){release('bad','✕ 90s WITHOUT GAIA VERIFICATION · MANUAL VIEW LEFT UNCHANGED')}}
window.addEventListener('pointerdown',e=>{const b=e.target?.closest?.('button');if(!isMachineButton(b))return;arm(b)},true);
window.addEventListener('click',e=>{const b=e.target?.closest?.('button');if(!isMachineButton(b))return;machineButton=b;activity('● MACHINE CLICK RECEIVED · LEGACY PRE-SOLVE MOVEMENT BLOCKED · GAIA MAY SOLVE FROM CURRENT VIEW','busy');console.log('[GV0038][BUTTON] native solver click allowed; pre-verified Aladin movement is guarded')},true);
function maintain(){ensureLayout();const b=findMachineButton();if(b){machineButton=b;ensureActivity()}}
maintain();setInterval(maintain,250);
console.log('[GV0038] pre-solve applyState/setRot guard installed; final GAIA-verified center/FOV/rotation remains allowed');
})();</script>`;

function normalizeIdentity(html){return html
  .replaceAll('GV 0030 LIVE','GV 0038 LIVE')
  .replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0030','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0038')
  .replaceAll('2026-08-29 19:22:14 COT',BUILD_STAMP_COLOMBIA)}
function patchCore(html){if(!html.includes(APPLY_ANCHOR))return{ok:false,reason:'applyState anchor missing'};if(!html.includes(ROT_ANCHOR))return{ok:false,reason:'setRot anchor missing'};let h=html.replace(APPLY_ANCHOR,APPLY_REPLACEMENT).replace(ROT_ANCHOR,ROT_REPLACEMENT);return{ok:true,html:h}}
function injectBeforeBodyEnd(html){const i=html.lastIndexOf('</body>');if(i<0)return null;return html.slice(0,i)+CLIENT_PATCH+html.slice(i)}

async function page(request,env){const r=await gv0030.fetch(request,env);let h=normalizeIdentity(await r.text());const core=patchCore(h);if(!core.ok)return new Response('0038 STARTUP ERROR: '+core.reason,{status:500});const out=injectBeforeBodyEnd(core.html);if(out==null)return new Response('0038 STARTUP ERROR: body anchor missing',{status:500});const headers=new Headers(r.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('pragma','no-cache');headers.set('expires','0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-pre-solve-movement','blocked-until-gaia-verified');headers.set('x-gv-machine-solution-contract','ra-dec-fov-rotation-from-stellar-transform');headers.set('x-gv-layout-order','images-orientation-source-live-locked');return new Response(out,{status:r.status,headers})}
async function health(request,env){const r=await gv0030.fetch(request,env);let data={};try{data=await r.json()}catch{}data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0038',direct_from:'0030',bypasses:['0031','0032','0033','0034','0035','0036','0037'],build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',pre_solve_applyState:'blocked_until_predConfidence_GAIA_VERIFIED',pre_solve_setRot:'blocked_until_predConfidence_GAIA_VERIFIED',manual_start_view:['ra','dec','fov','rotation'],machine_solution_contract:['ra','dec','fov','rotation'],fov_source:'stellar-transform-left-image-with-astrometry-cross-check',failure_behavior:'manual-view-remains-unchanged',layout_order:['images','orientation-angle-controls','source-image-data','live-validation-data'],layout_lock:'250ms-enforcement'};return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}})}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(request,env);return gv0030.fetch(request,env)}};
