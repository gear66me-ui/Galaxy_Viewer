import gv0030 from './gv-cloudflare-auto-astrometry-curator-0030-worker.js';

const REV='0032';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:33:28 COT';
const BUILD_STAMP_ISO='2026-08-29T19:33:28-05:00';

const FEEDBACK_PATCH=String.raw`<style id="gv32-machine-feedback-style">
#gv32DeployStamp{position:sticky;top:0;z-index:2147483647;box-sizing:border-box;width:100%;padding:5px 8px;background:#07131f;border-bottom:1px solid #2f8b60;color:#7dffb5;font:800 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;text-align:center}
#gv32DeployStamp strong{color:#fff}#gv32DeployStamp .now{color:#ffd166}
button.gv32Busy{background:#ffd166!important;border-color:#ffe59a!important;color:#171000!important;box-shadow:0 0 16px #ffd16699!important;animation:gv32Pulse .8s ease-in-out infinite alternate!important;opacity:1!important}
button.gv32Success{background:#123d2a!important;border-color:#57e39b!important;color:#eafff4!important;box-shadow:0 0 14px #57e39b88!important;opacity:1!important}
button.gv32Fail{background:#4b171b!important;border-color:#ff7575!important;color:#fff1f1!important;box-shadow:0 0 14px #ff757588!important;opacity:1!important}
#gv32MachineActivity{display:inline-flex;align-items:center;min-height:28px;padding:5px 8px;border:1px solid #42566f;border-radius:7px;background:#09121f;font:900 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:normal}
#gv32MachineActivity.busy{border-color:#9b8130;color:#ffd166;background:#2b240b}#gv32MachineActivity.good{border-color:#2f8b60;color:#57e39b;background:#0d2c20}#gv32MachineActivity.bad{border-color:#a94750;color:#ff8d8d;background:#351015}
@keyframes gv32Pulse{from{filter:brightness(.90)}to{filter:brightness(1.18)}}
@media(max-width:700px){#gv32DeployStamp{font-size:9px;padding:4px 5px}#gv32MachineActivity{width:100%;font-size:9px;min-height:24px;padding:4px 6px}}
</style>
<div id="gv32DeployStamp" role="status" aria-live="polite"><strong>GV 0032 LIVE</strong> · BUILD 2026-08-29 19:33:28 COT · LOAD-HANG REPAIR · MACHINE FEEDBACK · <span class="now" id="gv32ColombiaClock">COLOMBIA NOW —</span></div>
<script>(()=>{'use strict';
const NORMAL='★ APPLY MACHINE ASTROMETRY';
const SUCCESS_RE=/(GAIA VERIFIED|MACHINE SOLUTION APPLIED|STELLAR PASS|ACCEPTANCE GATE PASSED)/i;
const FAIL_RE=/(FAILED CLOSED|MACHINE FAILED|GAIA[^\n]{0,30}FAILED|SOLVE FAILED|BRIDGE FAILED|STARTUP FAILED|MACHINE START FAILED|BUTTON BRIDGE ERROR|STELLAR[^\n]{0,30}FAILED)/i;
const signalIds=['gv30MachineGate','gv29Gate','predConfidence','analysisLog','status','score','solveStatus'];
let active=false,button=null,activity=null,started=0,baseline={},ticker=null,watchdog=null;
function isMachineButton(b){return !!b&&b.tagName==='BUTTON'&&(b.dataset.gvMachineButton==='1'||/APPLY MACHINE (?:ASTROMETRY|PREDICTION)|MACHINE SOLVING|TAP RECEIVED/i.test((b.textContent||'').trim()))}
function findButton(){const marked=document.querySelector('button[data-gv-machine-button="1"]');if(marked)return marked;const b=[...document.querySelectorAll('button')].find(isMachineButton)||null;if(b)b.dataset.gvMachineButton='1';return b}
function ensureActivity(b){if(!b)return null;if(activity&&activity.isConnected)return activity;activity=document.getElementById('gv32MachineActivity');if(!activity){activity=document.createElement('span');activity.id='gv32MachineActivity';activity.setAttribute('role','status');activity.setAttribute('aria-live','assertive');activity.textContent='MACHINE READY — PRESS TO SOLVE';b.insertAdjacentElement('afterend',activity)}return activity}
function snapshot(){const o={};for(const id of signalIds)o[id]=(document.getElementById(id)?.textContent||'').trim();return o}
function changedText(now){const out=[];for(const id of signalIds)if((now[id]||'')!==(baseline[id]||''))out.push(now[id]||'');return out.join('\n')}
function setActivity(text,kind=''){const a=ensureActivity(button||findButton());if(a){a.className=kind;a.textContent=text}}
function paintBusy(){if(!button)return;button.classList.remove('gv32Success','gv32Fail');button.classList.add('gv32Busy');button.textContent='★ MACHINE SOLVING… DO NOT PRESS';button.setAttribute('aria-busy','true')}
function restoreNormal(){if(!button||!button.isConnected)button=findButton();if(!button)return;button.classList.remove('gv32Busy','gv32Success','gv32Fail');button.textContent=NORMAL;button.disabled=false;button.removeAttribute('aria-busy');setActivity('MACHINE READY — PRESS TO SOLVE','')}
function finish(ok,msg){if(!active)return;active=false;clearInterval(ticker);clearTimeout(watchdog);ticker=watchdog=null;if(!button||!button.isConnected)button=findButton();if(!button)return;button.disabled=false;button.removeAttribute('aria-busy');button.classList.remove('gv32Busy');button.classList.add(ok?'gv32Success':'gv32Fail');button.textContent=ok?'✓ MACHINE SOLVED — APPLIED':'✕ MACHINE SOLVE FAILED — RETRY';setActivity(msg,ok?'good':'bad');setTimeout(restoreNormal,ok?2500:4000)}
function begin(b){if(active)return;button=b;button.dataset.gvMachineButton='1';ensureActivity(button);active=true;started=Date.now();baseline=snapshot();paintBusy();setActivity('● TAP RECEIVED — STARTING MACHINE ASTROMETRY','busy');setTimeout(()=>{if(active&&button?.isConnected)button.disabled=true},0);ticker=setInterval(()=>{if(!active)return;if(!button||!button.isConnected){finish(false,'✕ MACHINE BUTTON DISAPPEARED DURING SOLVE');return}paintBusy();const changed=changedText(snapshot());if(SUCCESS_RE.test(changed)){finish(true,'✓ MACHINE SOLVED — GAIA-VALIDATED RESULT APPLIED');return}if(FAIL_RE.test(changed)){finish(false,'✕ MACHINE SOLVE FAILED — SEE DIAGNOSTICS / RETRY');return}const elapsed=Math.floor((Date.now()-started)/1000);setActivity('● MACHINE SOLVING · '+elapsed+'s · GAIA / ASTROMETRY WORKING','busy')},400);watchdog=setTimeout(()=>finish(false,'✕ NO COMPLETION SIGNAL AFTER 90s — SOLVER OR BRIDGE DID NOT RETURN'),90000)}
function acknowledge(b){button=b;button.dataset.gvMachineButton='1';ensureActivity(button);button.classList.add('gv32Busy');button.textContent='★ TAP RECEIVED — STARTING…';setActivity('● TAP RECEIVED — STARTING…','busy')}
document.addEventListener('pointerdown',e=>{const b=e.target?.closest?.('button');if(isMachineButton(b)&&!active)acknowledge(b)},true);
document.addEventListener('click',e=>{const b=e.target?.closest?.('button');if(isMachineButton(b)&&!active)begin(b)},true);
const clock=document.getElementById('gv32ColombiaClock'),fmt=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});function tickClock(){if(clock)clock.textContent='COLOMBIA NOW '+fmt.format(new Date())+' COT'}tickClock();setInterval(tickClock,1000);
setTimeout(()=>{const b=findButton();if(b){button=b;ensureActivity(b);if(!active&&/APPLY MACHINE/i.test(b.textContent||''))b.textContent=NORMAL}},500);
console.log('[GV0032] safe machine feedback installed; no MutationObserver');
})();</script>`;

function injectBeforeBodyEnd(html){const i=html.lastIndexOf('</body>');if(i<0)return null;return html.slice(0,i)+FEEDBACK_PATCH+html.slice(i)}

async function page(request,env){
  const r=await gv0030.fetch(request,env);let h=await r.text();
  h=h.replaceAll('GV 0030 LIVE','GV 0032 LIVE');
  h=h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0030','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0032');
  const out=injectBeforeBodyEnd(h);if(out==null)return new Response('0032 STARTUP ERROR: body anchor missing',{status:500});
  const headers=new Headers(r.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('pragma','no-cache');headers.set('expires','0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-machine-feedback','safe-no-mutation-observer');
  return new Response(out,{status:r.status,headers});
}
async function health(request,env){
  const r=await gv0030.fetch(request,env);let data={};try{data=await r.json()}catch{}
  data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0032',inherited_from:'0030',bypasses:'0031',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',load_hang_repair:'removed-self-triggering-mutation-observer',machine_button_feedback:{tap:'yellow-immediate',during:'yellow-disabled-pulsing-with-elapsed-seconds',success:'green-then-reset',failure:'red-then-reset',watchdog_seconds:90},features:[...new Set([...(Array.isArray(data.features)?data.features:[]),'bypass-0031','no-mutation-observer','machine-button-immediate-tap-feedback','machine-button-double-press-lock','machine-button-success-failure-state'])]};
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}})
}
export default {async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(request,env);return gv0030.fetch(request,env)}};
