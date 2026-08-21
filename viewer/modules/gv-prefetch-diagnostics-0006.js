/* Galaxy Viewer 11F removable unified prefetch diagnostics 0006. */
(()=>{
'use strict';
const VERSION='0006';
const EXPECTED='11F';
const ROOT_ID='gv-prefetch-diagnostics-0006';
let timer=0;

function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]))}
function stateText(resource){
  const state=String(resource?.state||'QUEUED').toUpperCase();
  const progress=Number(resource?.progress);
  if(state==='READY')return '✓ 100%';
  if(state==='FAILED')return '✕ FAILED';
  if(state==='RETRY')return 'RETRY';
  if(state==='SUSPENDED')return 'PAUSED';
  if(Number.isFinite(progress))return `${Math.max(0,Math.min(100,Math.round(progress)))}%`;
  if(state==='DOWNLOADING')return 'DOWNLOADING';
  if(state==='DECODING')return 'DECODING';
  if(state==='PREPARING')return 'PREPARING';
  return 'QUEUED';
}
function barClass(resource){
  const state=String(resource?.state||'QUEUED').toUpperCase();
  if(state==='READY')return 'gvpd-ready';
  if(state==='FAILED')return 'gvpd-failed';
  if(state==='RETRY')return 'gvpd-retry';
  if(state==='SUSPENDED')return 'gvpd-paused';
  return 'gvpd-working';
}
function bar(resource){
  const state=String(resource?.state||'QUEUED').toUpperCase();
  const progress=Number(resource?.progress);
  const determinate=Number.isFinite(progress);
  const width=determinate?Math.max(0,Math.min(100,progress)):0;
  const cls=barClass(resource)+(determinate?' gvpd-determinate':' gvpd-indeterminate');
  return `<div class="gvpd-resource ${cls}" title="${escapeHtml(state)}"><div class="gvpd-track"><div class="gvpd-fill"${determinate?` style="width:${width}%"`:''}></div></div><span>${escapeHtml(stateText(resource))}</span></div>`;
}
function ensureRoot(){
  let root=document.getElementById(ROOT_ID);
  if(root)return root;
  const style=document.createElement('style');
  style.id=ROOT_ID+'-style';
  style.textContent=`
#${ROOT_ID}{position:absolute;left:12px;right:12px;top:56px;z-index:7060;box-sizing:border-box;max-width:calc(100vw - 24px);padding:5px 6px 6px;border:1px solid rgba(120,255,171,.72);border-radius:6px;background:rgba(0,10,7,.78);color:#e8fff0;font:400 8px/1.12 "Space Age",sans-serif;letter-spacing:.12px;pointer-events:none;box-shadow:0 0 8px rgba(77,255,143,.16)}
#${ROOT_ID} .gvpd-active{height:14px;overflow:hidden;color:#78ffab;font-size:8px;line-height:14px;white-space:nowrap;text-overflow:ellipsis;text-align:center}
#${ROOT_ID} table{width:100%;border-collapse:collapse;table-layout:fixed}
#${ROOT_ID} th,#${ROOT_ID} td{height:15px;padding:1px 2px;border-top:1px solid rgba(120,255,171,.16);overflow:hidden;vertical-align:middle}
#${ROOT_ID} th{height:14px;color:#aeeFC5;font-size:7px;text-align:center}
#${ROOT_ID} .gvpd-seq{width:24px;text-align:center;font-variant-numeric:tabular-nums}
#${ROOT_ID} .gvpd-name{width:34%;white-space:nowrap;text-overflow:ellipsis;color:#fff}
#${ROOT_ID} .gvpd-resource{display:grid;grid-template-columns:minmax(32px,1fr) 48px;align-items:center;gap:3px;min-width:0;font-family:system-ui,sans-serif;font-size:7px}
#${ROOT_ID} .gvpd-track{position:relative;height:5px;border:1px solid rgba(210,255,230,.30);border-radius:4px;overflow:hidden;background:rgba(255,255,255,.08)}
#${ROOT_ID} .gvpd-fill{height:100%;width:100%;background:#68e99a}
#${ROOT_ID} .gvpd-indeterminate .gvpd-fill{width:38%;animation:gvpdMove .9s linear infinite}
#${ROOT_ID} .gvpd-retry .gvpd-fill,#${ROOT_ID} .gvpd-failed .gvpd-fill{background:#ff4b4b}
#${ROOT_ID} .gvpd-retry span,#${ROOT_ID} .gvpd-failed span{color:#ff7b7b}
#${ROOT_ID} .gvpd-paused .gvpd-fill{background:#b8b8b8;animation:none;width:48%}
#${ROOT_ID} .gvpd-ready span{color:#9fffc1}
@keyframes gvpdMove{from{transform:translateX(-110%)}to{transform:translateX(290%)}}
@media(max-width:520px){#${ROOT_ID}{left:5px;right:5px;max-width:calc(100vw - 10px);padding-left:3px;padding-right:3px}#${ROOT_ID} .gvpd-name{width:30%;font-size:7px}#${ROOT_ID} .gvpd-resource{grid-template-columns:minmax(22px,1fr) 39px;gap:2px;font-size:6px}}
`;
  document.head.appendChild(style);
  root=document.createElement('section');
  root.id=ROOT_ID;
  root.setAttribute('aria-label','GALAXY VIEWER 11F PREFETCH STATUS');
  root.innerHTML='<div class="gvpd-active">ACTIVE / TRAVELING TO — WAITING FOR 11F</div><table><thead><tr><th class="gvpd-seq">#</th><th class="gvpd-name">GALAXY</th><th>1 HD</th><th>2 ALADIN</th><th>3 WEB</th></tr></thead><tbody></tbody></table>';
  const viewer=document.getElementById('aladin-cosmic-command-test');
  (viewer||document.body).appendChild(root);
  return root;
}
function render(){
  const root=ensureRoot();
  const api=window.GV11F;
  const active=root.querySelector('.gvpd-active');
  const body=root.querySelector('tbody');
  if(!api||api.version!==EXPECTED||typeof api.getPrefetchTelemetry!=='function'){
    active.textContent='ACTIVE / TRAVELING TO — WAITING FOR 11F TELEMETRY';
    body.replaceChildren();
    return;
  }
  try{
    const data=api.getPrefetchTelemetry()||{};
    active.textContent=data.active?`ACTIVE / TRAVELING TO — ${data.active.name} — SEQ ${data.active.sequence}`:'ACTIVE / TRAVELING TO — NONE';
    const rows=Array.isArray(data.rows)?data.rows.slice(0,10):[];
    body.innerHTML=rows.map((row,index)=>`<tr data-key="${escapeHtml(row.key)}"><td class="gvpd-seq">${index+1}</td><td class="gvpd-name" title="${escapeHtml(row.name)}">${escapeHtml(row.name)}</td><td>${bar(row.hd)}</td><td>${bar(row.aladin)}</td><td>${bar(row.web)}</td></tr>`).join('');
    while(body.children.length<10){const tr=document.createElement('tr');tr.innerHTML=`<td class="gvpd-seq">${body.children.length+1}</td><td class="gvpd-name">WAITING</td><td>${bar({state:'QUEUED'})}</td><td>${bar({state:'QUEUED'})}</td><td>${bar({state:'QUEUED'})}</td>`;body.appendChild(tr)}
  }catch(error){
    active.textContent='DIAGNOSTICS ERROR — '+String(error?.message||error);
  }
}
function start(){if(timer)return;ensureRoot();render();timer=setInterval(render,120)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
window.GalaxyViewerPrefetchDiagnostics0006=Object.freeze({version:VERSION,render});
})();
