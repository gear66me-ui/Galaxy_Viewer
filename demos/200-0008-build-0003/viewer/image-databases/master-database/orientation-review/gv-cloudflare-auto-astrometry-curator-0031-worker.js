import gv0030 from './gv-cloudflare-auto-astrometry-curator-0030-worker.js';

const REV='0031';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:27:42 COT';
const BUILD_STAMP_ISO='2026-08-29T19:27:42-05:00';

const FEEDBACK_PATCH=String.raw`<style id="gv31-machine-feedback-style">
#gv31DeployStamp{position:sticky;top:0;z-index:2147483647;box-sizing:border-box;width:100%;padding:5px 8px;background:#07131f;border-bottom:1px solid #2f8b60;color:#7dffb5;font:800 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;text-align:center}
#gv31DeployStamp strong{color:#fff}#gv31DeployStamp .now{color:#ffd166}
button.gv31MachineBusy{background:#ffd166!important;border-color:#ffe59a!important;color:#171000!important;box-shadow:0 0 0 2px #ffd16655,0 0 16px #ffd16699!important;animation:gv31Pulse .8s ease-in-out infinite alternate!important;opacity:1!important}
button.gv31MachineSuccess{background:#123d2a!important;border-color:#57e39b!important;color:#eafff4!important;box-shadow:0 0 14px #57e39b88!important;opacity:1!important}
button.gv31MachineFail{background:#4b171b!important;border-color:#ff7575!important;color:#fff1f1!important;box-shadow:0 0 14px #ff757588!important;opacity:1!important}
#gv31MachineActivity{display:inline-flex;align-items:center;min-height:28px;padding:5px 8px;border:1px solid #42566f;border-radius:7px;background:#09121f;font:900 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:normal}
#gv31MachineActivity.busy{border-color:#9b8130;color:#ffd166;background:#2b240b}#gv31MachineActivity.good{border-color:#2f8b60;color:#57e39b;background:#0d2c20}#gv31MachineActivity.bad{border-color:#a94750;color:#ff8d8d;background:#351015}
@keyframes gv31Pulse{from{filter:brightness(.90)}to{filter:brightness(1.18)}}
@media(max-width:700px){#gv31DeployStamp{font-size:9px;padding:4px 5px}#gv31MachineActivity{width:100%;font-size:9px;min-height:24px;padding:4px 6px}}
</style>
<div id="gv31DeployStamp" role="status" aria-live="polite"><strong>GV 0031 LIVE</strong> · BUILD 2026-08-29 19:27:42 COT · MACHINE BUTTON VISUAL FEEDBACK · <span class="now" id="gv31ColombiaClock">COLOMBIA NOW —</span></div>
<script>(()=>{'use strict';
const NORMAL='★ APPLY MACHINE ASTROMETRY';
const SUCCESS_RE=/(GAIA VERIFIED|MACHINE SOLUTION APPLIED|STELLAR PASS|ACCEPTANCE GATE PASSED)/i;
const FAIL_RE=/(FAILED CLOSED|MACHINE FAILED|GAIA[^\n]{0,30}FAILED|SOLVE FAILED|BRIDGE FAILED|STARTUP FAILED|MACHINE START FAILED|BUTTON BRIDGE ERROR|STELLAR[^\n]{0,30}FAILED)/i;
let active=false,button=null,activity=null,started=0,baseline={},lastSignal='',watchdog=null,ticker=null,pressTimer=null;
const ids=['gv30MachineGate','gv29Gate','predConfidence','analysisLog','status','score','solveStatus'];
function findButton(){return [...document.querySelectorAll('button')].find(b=>/APPLY MACHINE (?:ASTROMETRY|PREDICTION)|MACHINE SOLVING/i.test((b.textContent||'').trim()))||null}
function ensureActivity(b){if(activity&&activity.isConnected)return activity;activity=document.getElementById('gv31MachineActivity');if(!activity){activity=document.createElement('span');activity.id='gv31MachineActivity';activity.setAttribute('role','status');activity.setAttribute('aria-live','assertive');activity.textContent='MACHINE READY — PRESS TO SOLVE';b.insertAdjacentElement('afterend',activity)}return activity}
function snap(){const o={};for(const id of ids)o[id]=(document.getElementById(id)?.textContent||'').trim();return o}
function changedText(now){const out=[];for(const id of ids)if((now[id]||'')!==(baseline[id]||''))out.push(now[id]||'');return out.join('\n')}
function setActivity(text,kind=''){const a=ensureActivity(button||findButton());if(!a)return;a.className=kind;a.textContent=text}
function paintBusy(b){b.classList.remove('gv31MachineSuccess','gv31MachineFail');b.classList.add('gv31MachineBusy');b.textContent='★ MACHINE SOLVING… DO NOT PRESS';b.setAttribute('aria-busy','true')}
function restoreNormal(){const b=button||findButton();if(!b)return;b.classList.remove('gv31MachineBusy','gv31MachineSuccess','gv31MachineFail');b.textContent=NORMAL;b.disabled=false;b.removeAttribute('aria-busy');button=b;setActivity('MACHINE READY — PRESS TO SOLVE','')}
function finish(ok,message){if(!active)return;active=false;clearTimeout(watchdog);clearInterval(ticker);watchdog=ticker=null;const b=button||findButton();if(!b)return;b.disabled=false;b.removeAttribute('aria-busy');b.classList.remove('gv31MachineBusy');b.classList.add(ok?'gv31MachineSuccess':'gv31MachineFail');b.textContent=ok?'✓ MACHINE SOLVED — APPLIED':'✕ MACHINE SOLVE FAILED — RETRY';setActivity(message,ok?'good':'bad');setTimeout(restoreNormal,ok?2500:4000)}
function stageText(){const s=snap(),changed=changedText(s).replace(/\s+/g,' ').trim();if(changed)return changed.slice(0,120);return 'GAIA / ASTROMETRY WORKING'}
function start(b){if(active)return;button=b;ensureActivity(b);active=true;started=Date.now();baseline=snap();lastSignal='';paintBusy(b);setActivity('● TAP RECEIVED — STARTING MACHINE ASTROMETRY','busy');setTimeout(()=>{if(active&&button===b)b.disabled=true},0);ticker=setInterval(()=>{if(!active)return;paintBusy(b);const elapsed=Math.max(0,Math.floor((Date.now()-started)/1000));const s=snap(),changed=changedText(s);if(changed&&changed!==lastSignal){lastSignal=changed;if(SUCCESS_RE.test(changed)){finish(true,'✓ MACHINE SOLVED — GAIA-VALIDATED RESULT APPLIED');return}if(FAIL_RE.test(changed)){finish(false,'✕ MACHINE SOLVE FAILED — SEE DIAGNOSTICS / RETRY');return}}setActivity('● MACHINE SOLVING · '+elapsed+'s · '+stageText(),'busy')},350);watchdog=setTimeout(()=>finish(false,'✕ NO COMPLETION SIGNAL AFTER 90s — SOLVER OR BRIDGE DID NOT RETURN'),90000)}
function acknowledgePress(b){if(active)return;button=b;ensureActivity(b);b.classList.add('gv31MachineBusy');b.textContent='★ TAP RECEIVED — STARTING…';setActivity('● TAP RECEIVED — STARTING…','busy');clearTimeout(pressTimer);pressTimer=setTimeout(()=>{if(!active)restoreNormal()},1200)}
function normalize(){const b=findButton();if(!b)return;button=b;ensureActivity(b);if(!active){b.classList.remove('gv31MachineBusy','gv31MachineSuccess','gv31MachineFail');b.textContent=NORMAL;if(!/LOADING|POSITIONING|ANALYZING/i.test(document.getElementById('status')?.textContent||''))b.disabled=false}}
document.addEventListener('pointerdown',e=>{const b=e.target?.closest?.('button');if(b&&/APPLY MACHINE/i.test(b.textContent||''))acknowledgePress(b)},true);
document.addEventListener('click',e=>{const b=e.target?.closest?.('button');if(!b||!/APPLY MACHINE|TAP RECEIVED/i.test(b.textContent||''))return;start(b)},true);
const observer=new MutationObserver(()=>{normalize();if(!active)return;const changed=changedText(snap());if(changed&&changed!==lastSignal){lastSignal=changed;if(SUCCESS_RE.test(changed))finish(true,'✓ MACHINE SOLVED — GAIA-VALIDATED RESULT APPLIED');else if(FAIL_RE.test(changed))finish(false,'✕ MACHINE SOLVE FAILED — SEE DIAGNOSTICS / RETRY')}});observer.observe(document.documentElement,{subtree:true,childList:true,characterData:true});
const clock=document.getElementById('gv31ColombiaClock'),fmt=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});function tickClock(){if(clock)clock.textContent='COLOMBIA NOW '+fmt.format(new Date())+' COT'}tickClock();setInterval(tickClock,1000);setInterval(normalize,500);normalize();
console.log('[GV0031][MACHINE-FEEDBACK] immediate yellow tap acknowledgement + success/failure reset installed');
})();</script>`;

function injectBeforeBodyEnd(html){
  const i=html.lastIndexOf('</body>');
  if(i<0)return null;
  return html.slice(0,i)+FEEDBACK_PATCH+html.slice(i);
}

async function page(request,env){
  const r=await gv0030.fetch(request,env);
  let h=await r.text();
  h=h.replaceAll('GV 0030 LIVE','GV 0031 LIVE');
  h=h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0030','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0031');
  const out=injectBeforeBodyEnd(h);
  if(out==null)return new Response('0031 STARTUP ERROR: body anchor missing',{status:500});
  const headers=new Headers(r.headers);
  headers.set('content-type','text/html; charset=utf-8');
  headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
  headers.set('pragma','no-cache');
  headers.set('expires','0');
  headers.set('x-gv-revision',REV);
  headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);
  headers.set('x-gv-machine-feedback','yellow-busy-green-success-red-failure');
  return new Response(out,{status:r.status,headers});
}

async function health(request,env){
  const r=await gv0030.fetch(request,env);
  let data={};try{data=await r.json()}catch{}
  data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0031',inherited_from:'0030',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',machine_button_feedback:{tap:'yellow-immediate',during:'yellow-disabled-pulsing-with-elapsed-seconds',success:'green-then-reset',failure:'red-then-reset',watchdog_seconds:90},features:[...new Set([...(Array.isArray(data.features)?data.features:[]),'machine-button-immediate-tap-feedback','machine-button-double-press-lock','machine-button-success-failure-state','machine-button-90s-watchdog'])]};
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA,'x-gv-machine-feedback':'installed'}});
}

export default {async fetch(request,env){
  const u=new URL(request.url);
  if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);
  if(u.pathname==='/api/health')return health(request,env);
  return gv0030.fetch(request,env);
}};
