/* Galaxy Viewer opt-in ten-slot download analytics 0001. OFF means zero polling. */
(() => {
  'use strict';
  const VERSION='0001',POLL_MS=500,MAX_SNAPSHOTS=200;
  let enabled=false,timer=0,panel=null,statusEl=null,bodyEl=null,crossEl=null,frozenRows=[];
  const snapshots=[];
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const norm=value=>String(value??'').trim().toUpperCase();
  const key=value=>String(value??'').trim().toLowerCase();
  const core=()=>window.GalaxyViewerCore||window.GalaxyRandomGalaxy?.prefetchRuntime?.core||null;
  const telemetry=()=>window.GalaxyRandomGalaxy?.getPrefetchTelemetry?.()||null;
  const paused=()=>Boolean(core()?.getBackgroundWorkSuspended?.()||telemetry()?.suspended);
  const bottomBannerText=()=>String(document.querySelector('.gvrg-card .gvrg-row:first-child .gvrg-value')?.textContent||'').replace(/\s+/g,' ').trim().toUpperCase();
  function readRows(){
    const t=telemetry(),c=core(),rows=(t?.rows||[]).slice(0,10);
    return rows.map((row,index)=>{
      const resource=c?.getHdPreparedResource?.(row.key)||null;
      const resourceKey=key(resource?.key),expectedKey=key(row.key);
      const expectedBanner=String(row.bannerText??'').trim();
      const hdBanner=String(row.hdBannerText??window.GalaxyRandomGalaxy?.bannerIdentity?.(resource?.destination)??'').trim();
      const expectedProvider=norm(row.provider),hdProvider=norm(resource?.destination?.provider),errors=[];
      if(resource&&resourceKey!==expectedKey)errors.push(`KEY ${resourceKey||'MISSING'} != ${expectedKey}`);
      if(resource&&hdBanner!==expectedBanner)errors.push(`BANNER ${hdBanner||'MISSING'} != ${expectedBanner||'MISSING'}`);
      if(resource&&expectedProvider&&hdProvider&&hdProvider!==expectedProvider)errors.push(`PROVIDER ${hdProvider} != ${expectedProvider}`);
      if(String(row.hd?.state||'').toUpperCase()==='READY'&&!resource)errors.push('READY RESOURCE MISSING');
      return Object.freeze({slot:Number(row.slot||index+1),target:expectedBanner,name:String(row.name||''),provider:expectedProvider,hd:String(row.hd?.state||'QUEUED').toUpperCase(),aladin:String(row.aladin?.state||'QUEUED').toUpperCase(),web:String(row.web?.state||'QUEUED').toUpperCase(),source:String(resource?.sourceKind||row.hd?.detail||'').toUpperCase(),identity:errors.length?`IDENTITY ERROR: ${errors.join('; ')}`:(resource?'MATCH':'WAITING'),key:expectedKey,hdKey:resourceKey,hdTarget:hdBanner});
    });
  }
  function render(rows=frozenRows){
    if(!panel)return;
    const isPaused=paused();
    statusEl.textContent=enabled?(isPaused?'ON — FROZEN DURING RANDOM GALAXY TRAVEL':'ON — LIVE 10-SLOT ROSTER'):'OFF — NO POLLING';
    const active=telemetry()?.active;
    crossEl.textContent=`CROSS-CHECK — QUEUE #1: ${rows[0]?.target||'—'}   ACTIVE: ${active?.bannerText||active?.name||'—'}   BOTTOM BANNER: ${bottomBannerText()||'—'}`;
    bodyEl.innerHTML=rows.map(row=>`<tr class="${row.identity.startsWith('IDENTITY ERROR')?'gvdla-bad':''}"><td>${esc(row.slot)}</td><td>${esc(row.target)}</td><td>${esc(row.provider)}</td><td>${esc(row.hd)}</td><td>${esc(row.aladin)}</td><td>${esc(row.web)}</td><td>${esc(row.source)}</td><td>${esc(row.identity)}</td></tr>`).join('')||'<tr><td colspan="8">WAITING FOR AUTHORITATIVE FUTURE ROSTER</td></tr>';
  }
  function collect(){if(!enabled)return;if(paused()){render(frozenRows);return}frozenRows=readRows();snapshots.push(Object.freeze({at:new Date().toISOString(),rows:frozenRows}));if(snapshots.length>MAX_SNAPSHOTS)snapshots.splice(0,snapshots.length-MAX_SNAPSHOTS);render(frozenRows)}
  function setEnabled(next){next=Boolean(next);if(next===enabled){render();return enabled}enabled=next;if(enabled){frozenRows=readRows();collect();timer=setInterval(collect,POLL_MS)}else{if(timer)clearInterval(timer);timer=0}render();return enabled}
  function download(){const payload={module:'GalaxyViewerDownloadAnalytics',version:VERSION,exportedAt:new Date().toISOString(),enabled,currentRows:[...frozenRows],snapshots:[...snapshots]};const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`galaxy-viewer-download-analytics-${Date.now()}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
  function ensurePanel(){
    if(panel)return panel;
    const style=document.createElement('style');style.id='gv-download-analytics-0001-style';style.textContent=`#gv-download-analytics-0001{position:fixed;left:8px;top:54px;z-index:2147481999;width:calc(100vw - 16px);max-height:62vh;overflow:auto;padding:8px;border:1px solid rgba(255,216,77,.85);border-radius:6px;background:rgba(0,0,0,.38);backdrop-filter:blur(2px);color:#FFD84D;font:10px/1.2 monospace;box-shadow:0 0 10px rgba(255,216,77,.18)}#gv-download-analytics-0001 *{box-sizing:border-box}#gv-download-analytics-0001 .gvdla-head{display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:5px;font-weight:700}#gv-download-analytics-0001 .gvdla-controls{display:flex;gap:4px;flex-wrap:wrap}#gv-download-analytics-0001 button{padding:4px 6px;border:1px solid #FFD84D;border-radius:4px;background:rgba(0,0,0,.28);color:#FFD84D;font:10px monospace}#gv-download-analytics-0001 .gvdla-status,#gv-download-analytics-0001 .gvdla-cross{margin:4px 0;color:#FFE98A;white-space:normal}#gv-download-analytics-0001 table{width:100%;border-collapse:collapse;table-layout:auto}#gv-download-analytics-0001 td,#gv-download-analytics-0001 th{padding:3px 4px;border:1px solid rgba(255,216,77,.26);vertical-align:top;text-align:left;white-space:nowrap}#gv-download-analytics-0001 th{position:sticky;top:0;background:rgba(0,0,0,.72);color:#FFF1A8}#gv-download-analytics-0001 td:nth-child(2){font-weight:700;color:#FFF1A8}#gv-download-analytics-0001 .gvdla-bad td:last-child{color:#FF8A70;font-weight:700}`;document.head.appendChild(style);
    panel=document.createElement('section');panel.id='gv-download-analytics-0001';panel.innerHTML=`<div class="gvdla-head"><span>DOWNLOAD ANALYTICS 0001</span><div class="gvdla-controls"><button data-a="on">TURN ON</button><button data-a="off">TURN OFF</button><button data-a="download">DOWNLOAD</button><button data-a="close">CLOSE</button></div></div><div class="gvdla-status"></div><div class="gvdla-cross"></div><table><thead><tr><th>#</th><th>TARGET / BANNER</th><th>PROVIDER</th><th>HD</th><th>ALADIN</th><th>WEB</th><th>SOURCE</th><th>IDENTITY</th></tr></thead><tbody class="gvdla-body"></tbody></table>`;
    statusEl=panel.querySelector('.gvdla-status');crossEl=panel.querySelector('.gvdla-cross');bodyEl=panel.querySelector('.gvdla-body');panel.addEventListener('click',event=>{const a=event.target?.dataset?.a;if(a==='on')setEnabled(true);else if(a==='off')setEnabled(false);else if(a==='download')download();else if(a==='close')panel.style.display='none'});document.body.appendChild(panel);frozenRows=readRows();render();return panel;
  }
  function open(){ensurePanel().style.display='block';if(!enabled)frozenRows=readRows();render()}function close(){if(panel)panel.style.display='none'}
  window.GalaxyViewerDownloadAnalytics=Object.freeze({VERSION,open,close,enable:()=>setEnabled(true),disable:()=>setEnabled(false),setEnabled,getRows:()=>Object.freeze([...readRows()]),getState:()=>Object.freeze({enabled,rows:frozenRows.length,snapshots:snapshots.length}),download});
})();
