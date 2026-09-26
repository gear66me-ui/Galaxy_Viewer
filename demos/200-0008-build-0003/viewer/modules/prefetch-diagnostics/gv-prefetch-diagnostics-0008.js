/* Galaxy Viewer 11H diagnostics + surgical runtime restoration 0008.
   11H Viewer source remains an exact 11G descendant; this removable layer supplies
   the authorized active-row identity proof, copy report, and existing-control restoration. */
(()=>{
'use strict';
const VERSION='0008';
const ROOT_ID='gv-prefetch-diagnostics-0008';
const POLL_MS=120;
let timer=0;
let core=null;
let queueApi=null;
let savedControls=null;
const lastRows=new Map();

function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]))}
function keyOf(value){return String(value?.archiveId||value?.key||value?.name||'').trim().toLowerCase()}
function progressValue(resource){const value=resource?.progress;return typeof value==='number'&&Number.isFinite(value)?value:null}
function stateText(resource){const state=String(resource?.state||'QUEUED').toUpperCase();const progress=progressValue(resource);if(state==='READY')return '✓ 100%';if(state==='FAILED')return '✕ FAILED';if(state==='RETRY'||state.includes('RETRY'))return 'RETRY';if(state==='SUSPENDED')return 'PAUSED';if(progress!==null)return `${Math.max(0,Math.min(100,Math.round(progress)))}%`;if(state==='DOWNLOADING')return 'DOWNLOADING';if(state==='DECODING')return 'DECODING';if(state==='PREPARING')return 'PREPARING';return 'QUEUED'}
function barClass(resource){const state=String(resource?.state||'QUEUED').toUpperCase();if(state==='READY')return 'gvpd-ready';if(state==='FAILED')return 'gvpd-failed';if(state.includes('RETRY'))return 'gvpd-retry';if(state==='SUSPENDED')return 'gvpd-paused';return 'gvpd-working'}
function bar(resource){const state=String(resource?.state||'QUEUED').toUpperCase();const progress=progressValue(resource);const determinate=progress!==null;const width=determinate?Math.max(0,Math.min(100,progress)):0;const cls=barClass(resource)+(determinate?' gvpd-determinate':' gvpd-indeterminate');return `<div class="gvpd-resource ${cls}" title="${escapeHtml(state)}"><div class="gvpd-track"><div class="gvpd-fill"${determinate?` style="width:${width}%"`:''}></div></div><span>${escapeHtml(stateText(resource))}</span></div>`}

function captureControls(){
  if(savedControls)return savedControls;
  const nav=document.getElementById('gv-galaxy-nav');
  const random=core?.randomGalaxyButton||document.getElementById('gv-random-galaxy');
  const back=core?.historyBackButton||nav?.querySelector('.gv-galaxy-history-back');
  const forward=core?.historyForwardButton||nav?.querySelector('.gv-galaxy-history-forward');
  const version=core?.versionLabel||document.getElementById('gv-version-label');
  if(nav&&random&&back&&forward&&version)savedControls={nav,random,back,forward,version};
  return savedControls;
}
function forceVisible(element,display){
  if(!element)return;
  element.removeAttribute('hidden');
  element.removeAttribute('aria-hidden');
  element.style.setProperty('display',display,'important');
  element.style.setProperty('visibility','visible','important');
  element.style.setProperty('opacity','1','important');
}
function restoreExistingNavigationShell(){
  const controls=captureControls();
  if(!controls)return false;
  const viewer=document.getElementById('aladin-cosmic-command-test');
  if(!controls.nav.isConnected&&viewer)viewer.appendChild(controls.nav);
  if(!controls.back.isConnected)controls.nav.appendChild(controls.back);
  if(!controls.random.isConnected)controls.nav.appendChild(controls.random);
  if(!controls.forward.isConnected)controls.nav.appendChild(controls.forward);
  forceVisible(controls.nav,'flex');
  forceVisible(controls.random,'flex');
  forceVisible(controls.back,'flex');
  forceVisible(controls.forward,'flex');
  forceVisible(controls.version,'block');
  controls.nav.style.setProperty('pointer-events','auto','important');
  controls.random.style.setProperty('pointer-events','auto','important');
  const busy=Boolean(core?.randomGalaxy?.getState?.().busy);
  if(!busy)controls.random.disabled=false;
  return true;
}
function hdOpen(){return Boolean(core?.randomGalaxy?.getState?.().hdOpen)}
function archiveOpen(){return document.getElementById('gv-archive-overlay')?.classList.contains('gv-open')||false}
function scheduleSkyRestore(){
  let frames=0;
  const check=()=>{
    frames++;
    if(!archiveOpen()&&!hdOpen()){restoreExistingNavigationShell();return}
    if(frames<90)requestAnimationFrame(check);
  };
  requestAnimationFrame(check);
}
function installBackRestoration(){
  const randomGalaxy=core?.randomGalaxy;
  if(!randomGalaxy)return;
  const providerBack=document.getElementById('gv-archive-back');
  if(providerBack&&!providerBack.dataset.gv11hBound){
    providerBack.dataset.gv11hBound='true';
    providerBack.addEventListener('click',()=>{
      /* Provider Back deliberately returns to the already-open HD viewport. */
      requestAnimationFrame(()=>{
        if(hdOpen()){
          const overlay=randomGalaxy.hdOverlay;
          if(overlay){overlay.style.removeProperty('display');overlay.style.removeProperty('visibility');overlay.style.removeProperty('opacity')}
        }
      });
    },false);
  }
  const hdBack=randomGalaxy.backButton;
  if(hdBack&&!hdBack.dataset.gv11hBound){
    hdBack.dataset.gv11hBound='true';
    hdBack.addEventListener('click',scheduleSkyRestore,false);
  }
}

function currentRuntimeDestination(data){
  const busy=Boolean(core?.randomGalaxy?.getState?.().busy);
  const runtime=core?.randomGalaxy?.getState?.().activeDestination||core?.randomGalaxy?.activeDestination||null;
  if(busy&&data?.active?.name)return {name:String(data.active.name),key:String(data.active.key||''),sequence:data.active.sequence,provider:String(data.active.provider||''),destination:runtime};
  if(runtime)return {name:String(runtime.name||data?.active?.name||''),key:keyOf(runtime)||String(data?.active?.key||''),sequence:data?.active?.sequence??'',provider:String(runtime.provider||data?.active?.provider||''),destination:runtime};
  return data?.active?{name:String(data.active.name||''),key:String(data.active.key||''),sequence:data.active.sequence,provider:String(data.active.provider||''),destination:null}:null;
}
function hdStateForActive(active,cached){
  const key=String(active?.key||'').toLowerCase();
  const status=(core?.getHubbleDownloadStatus?.()||[]).find(item=>String(item?.key||'').toLowerCase()===key);
  if(status){const state=String(status.state||'QUEUED').toUpperCase();return {state:state.includes('RETRY')?'RETRY':state,progress:state==='READY'?100:null,detail:String(status.sourceKind||'')}}
  return cached?.hd||{state:'QUEUED',progress:null};
}
function aladinStateForActive(active,cached){
  const key=String(active?.key||'').toLowerCase();
  if(core?.isAladinPrepared?.(key))return {state:'READY',progress:100};
  if(core?.getBackgroundWorkSuspended?.())return {state:'SUSPENDED',progress:null};
  const state=core?.getAladinPrewarmState?.()||{};
  if(String(state.activeKey||'').toLowerCase()===key)return {state:'PREPARING',progress:null};
  return cached?.aladin||{state:'QUEUED',progress:null};
}
function webStateForActive(cached){
  if(core?.getBackgroundWorkSuspended?.()&&cached?.web?.state!=='READY')return {state:'SUSPENDED',progress:null,detail:cached?.web?.detail||''};
  return cached?.web||{state:'QUEUED',progress:null,detail:''};
}
function activeResourceRow(active){
  if(!active)return null;
  const cached=lastRows.get(String(active.key||'').toLowerCase())||null;
  return {sequence:active.sequence,key:active.key,name:active.name,provider:active.provider,hd:hdStateForActive(active,cached),aladin:aladinStateForActive(active,cached),web:webStateForActive(cached)};
}

function ensureRoot(){
  let root=document.getElementById(ROOT_ID);if(root)return root;
  const style=document.createElement('style');style.id=ROOT_ID+'-style';style.textContent=`#${ROOT_ID}{position:absolute;left:12px;right:12px;top:56px;z-index:7060;box-sizing:border-box;max-width:calc(100vw - 24px);padding:5px 6px 4px;border:1px solid rgba(120,255,171,.72);border-radius:6px;background:rgba(0,10,7,.78);color:#e8fff0;font:400 8px/1.12 "Space Age",sans-serif;letter-spacing:.12px;pointer-events:none;box-shadow:0 0 8px rgba(77,255,143,.16)}#${ROOT_ID} .gvpd-active-title{height:14px;overflow:hidden;color:#78ffab;font-size:8px;line-height:14px;white-space:nowrap;text-overflow:ellipsis;text-align:center}#${ROOT_ID} table{width:100%;border-collapse:collapse;table-layout:fixed}#${ROOT_ID} th,#${ROOT_ID} td{height:15px;padding:1px 2px;border-top:1px solid rgba(120,255,171,.16);overflow:hidden;vertical-align:middle}#${ROOT_ID} th{height:14px;color:#aeefc5;font-size:7px;text-align:center}#${ROOT_ID} .gvpd-seq{width:24px;text-align:center;font-variant-numeric:tabular-nums}#${ROOT_ID} .gvpd-name{width:34%;white-space:nowrap;text-overflow:ellipsis;color:#fff}#${ROOT_ID} .gvpd-resource{display:grid;grid-template-columns:minmax(32px,1fr) 48px;align-items:center;gap:3px;min-width:0;font-family:system-ui,sans-serif;font-size:7px}#${ROOT_ID} .gvpd-track{position:relative;height:5px;border:1px solid rgba(210,255,230,.30);border-radius:4px;overflow:hidden;background:rgba(255,255,255,.08)}#${ROOT_ID} .gvpd-fill{height:100%;width:100%;background:#68e99a}#${ROOT_ID} .gvpd-indeterminate .gvpd-fill{width:38%;animation:gvpdMove .9s linear infinite}#${ROOT_ID} .gvpd-retry .gvpd-fill,#${ROOT_ID} .gvpd-failed .gvpd-fill{background:#ff4b4b}#${ROOT_ID} .gvpd-retry span,#${ROOT_ID} .gvpd-failed span{color:#ff7b7b}#${ROOT_ID} .gvpd-paused .gvpd-fill{background:#b8b8b8;animation:none;width:48%}#${ROOT_ID} .gvpd-ready span{color:#9fffc1}#${ROOT_ID} .gvpd-active-row{background:rgba(64,255,132,.13);box-shadow:inset 0 0 7px rgba(64,255,132,.18)}#${ROOT_ID} .gvpd-active-row.gvpd-traveling{background:rgba(255,216,90,.13);box-shadow:inset 0 0 7px rgba(255,216,90,.18)}#${ROOT_ID} .gvpd-dot{display:inline-block;width:7px;height:7px;margin-right:3px;border-radius:50%;vertical-align:middle;background:#46ff83;box-shadow:0 0 5px #46ff83}#${ROOT_ID} .gvpd-traveling .gvpd-dot{background:#ffd85a;box-shadow:0 0 5px #ffd85a;animation:gvpdBlink .7s steps(1,end) infinite}#${ROOT_ID} .gvpd-tools{height:20px;display:flex;align-items:flex-end;justify-content:flex-start;pointer-events:none}#${ROOT_ID} .gvpd-copy{position:relative;width:18px;height:18px;margin:2px 0 0;padding:0;border:1px solid rgba(120,255,171,.72);border-radius:4px;background:rgba(0,18,11,.92);pointer-events:auto;cursor:pointer}#${ROOT_ID} .gvpd-copy::before,#${ROOT_ID} .gvpd-copy::after{content:"";position:absolute;width:7px;height:9px;border:1px solid #dfffea;border-radius:1px;background:#03130c}#${ROOT_ID} .gvpd-copy::before{left:5px;top:3px}#${ROOT_ID} .gvpd-copy::after{left:3px;top:5px}#${ROOT_ID} .gvpd-copy.gvpd-copied{border-color:#78ffab;box-shadow:0 0 7px #46ff83}@keyframes gvpdMove{from{transform:translateX(-110%)}to{transform:translateX(290%)}}@keyframes gvpdBlink{0%,49%{opacity:1}50%,100%{opacity:.2}}@media(max-width:520px){#${ROOT_ID}{left:5px;right:5px;max-width:calc(100vw - 10px);padding-left:3px;padding-right:3px}#${ROOT_ID} .gvpd-name{width:30%;font-size:7px}#${ROOT_ID} .gvpd-resource{grid-template-columns:minmax(22px,1fr) 39px;gap:2px;font-size:6px}}`;
  document.head.appendChild(style);
  root=document.createElement('section');root.id=ROOT_ID;root.setAttribute('aria-label','GALAXY VIEWER 11H PREFETCH STATUS');
  root.innerHTML='<div class="gvpd-active-title">ACTIVE / TRAVELING TO — WAITING FOR 11H</div><table><thead><tr><th class="gvpd-seq">#</th><th class="gvpd-name">GALAXY</th><th>1 HD</th><th>2 ALADIN</th><th>3 WEB</th></tr></thead><tbody></tbody></table><div class="gvpd-tools"><button class="gvpd-copy" type="button" aria-label="COPY DIAGNOSTIC REPORT" title="COPY DIAGNOSTIC REPORT"></button></div>';
  const viewer=document.getElementById('aladin-cosmic-command-test');(viewer||document.body).appendChild(root);
  root.querySelector('.gvpd-copy').addEventListener('click',copyReport);
  return root;
}
function rowHtml(row,index,{active=false,traveling=false}={}){
  const cls=active?` class="gvpd-active-row${traveling?' gvpd-traveling':''}"`:'';
  const seq=active?`<span class="gvpd-dot" aria-hidden="true"></span>${escapeHtml(row.sequence||'A')}`:String(index+1);
  return `<tr${cls} data-key="${escapeHtml(row.key)}"><td class="gvpd-seq">${seq}</td><td class="gvpd-name" title="${escapeHtml(row.name)}">${escapeHtml(row.name)}</td><td>${bar(row.hd)}</td><td>${bar(row.aladin)}</td><td>${bar(row.web)}</td></tr>`;
}
function reportText(){
  const data=queueApi?.getPrefetchTelemetry?.()||{};
  const active=currentRuntimeDestination(data);
  const activeRow=activeResourceRow(active);
  const rows=Array.isArray(data.rows)?data.rows.slice(0,10):[];
  const lines=['GALAXY VIEWER 11H DIAGNOSTIC REPORT',`SUSPENDED: ${Boolean(core?.getBackgroundWorkSuspended?.())}`];
  if(activeRow)lines.push(`ACTIVE | SEQ ${activeRow.sequence} | KEY ${activeRow.key} | ${activeRow.provider} | ${activeRow.name} | HD ${stateText(activeRow.hd)} | ALADIN ${stateText(activeRow.aladin)} | WEB ${stateText(activeRow.web)}`);else lines.push('ACTIVE | NONE');
  rows.forEach((row,index)=>lines.push(`${index+1} | SEQ ${row.sequence} | KEY ${row.key} | ${row.provider} | ${row.name} | HD ${stateText(row.hd)} | ALADIN ${stateText(row.aladin)} | WEB ${stateText(row.web)}${row.hd?.detail?` | HD DETAIL ${row.hd.detail}`:''}${row.web?.detail?` | WEB DETAIL ${row.web.detail}`:''}`));
  return lines.join('\n');
}
async function copyReport(){
  const text=reportText();
  let copied=false;
  try{await navigator.clipboard.writeText(text);copied=true}catch(_){
    try{const area=document.createElement('textarea');area.value=text;area.style.position='fixed';area.style.left='-10000px';document.body.appendChild(area);area.select();copied=document.execCommand('copy');area.remove()}catch(__){}
  }
  if(copied){const button=document.querySelector(`#${ROOT_ID} .gvpd-copy`);button?.classList.add('gvpd-copied');setTimeout(()=>button?.classList.remove('gvpd-copied'),650)}
}
function render(){
  const root=ensureRoot();
  core=window.GV10E||core;
  queueApi=window.GV11F||queueApi;
  const title=root.querySelector('.gvpd-active-title');
  const body=root.querySelector('tbody');
  if(!core||!queueApi||typeof queueApi.getPrefetchTelemetry!=='function'){
    title.textContent='ACTIVE / TRAVELING TO — WAITING FOR 11H TELEMETRY';body.replaceChildren();return;
  }
  try{
    const data=queueApi.getPrefetchTelemetry()||{};
    const rows=Array.isArray(data.rows)?data.rows.slice(0,10):[];
    rows.forEach(row=>{if(row?.key)lastRows.set(String(row.key).toLowerCase(),structuredClone?structuredClone(row):JSON.parse(JSON.stringify(row)))});
    const active=currentRuntimeDestination(data);
    const activeRow=activeResourceRow(active);
    const traveling=Boolean(core.randomGalaxy?.getState?.().busy||core.getBackgroundWorkSuspended?.());
    title.textContent=active?`ACTIVE / TRAVELING TO — ${active.name} — SEQ ${active.sequence}`:'ACTIVE / TRAVELING TO — NONE';
    let html=activeRow?rowHtml(activeRow,-1,{active:true,traveling}):'';
    html+=rows.map((row,index)=>rowHtml(row,index)).join('');
    body.innerHTML=html;
    while(body.querySelectorAll('tr:not(.gvpd-active-row)').length<10){const index=body.querySelectorAll('tr:not(.gvpd-active-row)').length;const tr=document.createElement('tr');tr.innerHTML=`<td class="gvpd-seq">${index+1}</td><td class="gvpd-name">WAITING</td><td>${bar({state:'QUEUED'})}</td><td>${bar({state:'QUEUED'})}</td><td>${bar({state:'QUEUED'})}</td>`;body.appendChild(tr)}
    installBackRestoration();
    captureControls();
    if(!archiveOpen()&&!hdOpen()&&!traveling)restoreExistingNavigationShell();
    if(core.versionLabel){core.versionLabel.textContent='VERSION 11H';core.versionLabel.setAttribute('aria-label','GALAXY VIEWER VERSION 11H')}
    window.GV11H=Object.freeze({version:'11H',displayVersion:'11H',core,queueApi,getPrefetchTelemetry:()=>({active:activeRow,rows,suspended:traveling}),copyDiagnosticReport:copyReport});
  }catch(error){title.textContent='DIAGNOSTICS ERROR — '+String(error?.message||error)}
}
function start(){if(timer)return;ensureRoot();render();timer=setInterval(render,POLL_MS)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
window.GalaxyViewerPrefetchDiagnostics0008=Object.freeze({version:VERSION,render,copyReport});
})();
