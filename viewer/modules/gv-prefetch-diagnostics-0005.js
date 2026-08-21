/* Galaxy Viewer Prefetch Diagnostics 0005 — unified HD/ALDN/WEB rolling-ten telemetry, active identity, button-state diary, and export. */
(()=>{
    'use strict';
    if(window.GVPrefetchDiagnostics0005)return;
    const VERSION='0005';
    const sessionStartedAt=new Date().toISOString();
    const sessionStartedMs=performance.now();
    const snapshots=[];
    const interactions=[];
    let timer=0;
    let mounted=false;
    let lastEventCount=0;

    const waitForApi=async()=>{
        for(let i=0;i<600;i++){
            const api=window.GV10E;
            if(api&&String(api.version)==='11E'&&typeof api.getHdSlots==='function'&&typeof api.getAladinSlots==='function'&&typeof api.getArchivePreloadState==='function')return api;
            await new Promise(resolve=>setTimeout(resolve,100));
        }
        throw new Error('11E TELEMETRY API TIMEOUT');
    };
    const clone=value=>JSON.parse(JSON.stringify(value??null));
    const nowRecord=(type,detail={})=>({at:new Date().toISOString(),ms:performance.now(),type,...detail});
    const normalized=value=>String(value||'').trim().toUpperCase();
    const stateText=value=>{
        const state=normalized(value);
        const map={READY:'✓ (READY)',DOWNLOADING:'… (DOWNLOADING)',DECODING:'… (DECODING)',LOADING:'… (LOADING)',PENDING:'… (PENDING)',QUEUED:'— (QUEUED)',WAIT:'— (WAIT)',RETRY:'↻ (RETRY)',SUSPENDED:'⏸ (SUSPENDED)',FAILED:'✕ (FAILED)',EMPTY:'— (EMPTY)'};
        return map[state]||`${state?'…':'—'} (${state||'EMPTY'})`;
    };
    function randomButtonState(reason='sample'){
        const button=document.getElementById('gv-random-galaxy');
        if(!button)return {reason,exists:false,attached:false,parent:'',display:'',visibility:'',opacity:'',width:0,height:0,disabled:null};
        const style=getComputedStyle(button),rect=button.getBoundingClientRect();
        return {reason,exists:true,attached:button.isConnected,parent:button.parentElement?.id||button.parentElement?.className||button.parentElement?.tagName||'',display:style.display,visibility:style.visibility,opacity:style.opacity,width:Math.round(rect.width*10)/10,height:Math.round(rect.height*10)/10,disabled:Boolean(button.disabled)};
    }
    function installStyle(){
        const style=document.createElement('style');style.id='gv-prefetch-diag-style-0005';style.textContent=`
#gv-prefetch-diag-unified{position:fixed;left:50px;top:52px;z-index:7600;width:min(690px,calc(100vw - 58px));box-sizing:border-box;padding:4px 5px;border:1px solid rgba(120,255,171,.62);border-radius:5px;background:rgba(0,10,7,.76);color:#DFFFEA;font:7.5px/11px monospace;text-shadow:0 0 3px #000;pointer-events:none}
.gv-prefetch-diag-title{text-align:center;color:#78FFAB;font-weight:700;letter-spacing:.8px;margin-bottom:2px}.gv-prefetch-diag-active{padding:2px 3px 3px;border-bottom:1px solid rgba(120,255,171,.28);white-space:normal;overflow-wrap:anywhere;color:#FFD85A;font-weight:700}.gv-prefetch-diag-status{padding:2px 3px;color:#78FFAB;white-space:normal;overflow-wrap:anywhere}.gv-prefetch-diag-head,.gv-prefetch-diag-row{display:grid;grid-template-columns:28px minmax(105px,1fr) 86px 86px 86px;gap:3px;align-items:center}.gv-prefetch-diag-head{height:12px;color:#AEEFC5;font-weight:700;border-top:1px solid rgba(120,255,171,.20);border-bottom:1px solid rgba(120,255,171,.20)}.gv-prefetch-diag-row{min-height:12px;border-bottom:1px solid rgba(120,255,171,.08)}.gv-prefetch-diag-seq{text-align:right}.gv-prefetch-diag-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.gv-prefetch-diag-cell{text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.gv-prefetch-diag-hidden{display:none!important}
#gv-prefetch-download-report{position:fixed;left:50%;top:8px;transform:translateX(-50%);z-index:7601;height:24px;padding:0 8px;border:1px solid #78FFAB;border-radius:5px;background:rgba(0,45,26,.88);color:#DFFFEA;font:700 8px/22px monospace;letter-spacing:.5px;cursor:pointer;touch-action:manipulation}#gv-prefetch-download-report:disabled{opacity:.55;cursor:default}`;document.head.appendChild(style);
    }
    function makeTable(){
        const panel=document.createElement('div');panel.id='gv-prefetch-diag-unified';
        const title=document.createElement('div');title.className='gv-prefetch-diag-title';title.textContent='ROLLING 10 — HD / ALDN / WEB';
        const active=document.createElement('div');active.className='gv-prefetch-diag-active';active.textContent='ACTIVE / TRAVELING TO —';
        const status=document.createElement('div');status.className='gv-prefetch-diag-status';status.textContent='TELEMETRY — WAITING FOR 11E';
        const head=document.createElement('div');head.className='gv-prefetch-diag-head';head.innerHTML='<span>SEQ</span><span>GALAXY</span><span>HD</span><span>ALDN</span><span>WEB</span>';
        panel.append(title,active,status,head);
        for(let i=0;i<10;i++){const row=document.createElement('div');row.className='gv-prefetch-diag-row';row.innerHTML='<span class="gv-prefetch-diag-seq">—</span><span class="gv-prefetch-diag-name">EMPTY</span><span class="gv-prefetch-diag-cell gv-prefetch-diag-hd">— (EMPTY)</span><span class="gv-prefetch-diag-cell gv-prefetch-diag-aladin">— (EMPTY)</span><span class="gv-prefetch-diag-cell gv-prefetch-diag-web">— (EMPTY)</span>';panel.appendChild(row)}
        return {panel,active,status};
    }
    function webMap(state){
        const map=new Map();
        for(const item of state?.items||[])if(item?.key)map.set(item.key,item);
        const loading=state?.loading;
        if(Array.isArray(loading)){for(const item of loading)if(item?.key)map.set(item.key,item)}else if(loading?.key)map.set(loading.key,loading);
        return map;
    }
    function render(api,ui){
        const hd=(api.getHdSlots?.()||[]).filter(item=>item?.key).sort((a,b)=>(Number(a.sequence)||0)-(Number(b.sequence)||0)).slice(0,10);
        const aladinByKey=new Map((api.getAladinSlots?.()||[]).filter(item=>item?.key).map(item=>[item.key,item]));
        const webState=api.getArchivePreloadState?.()||{},webByKey=webMap(webState);
        const rows=[...ui.panel.querySelectorAll('.gv-prefetch-diag-row')];
        rows.forEach((row,index)=>{
            const item=hd[index]||null,aladin=item?aladinByKey.get(item.key):null,web=item?webByKey.get(item.key):null;
            row.querySelector('.gv-prefetch-diag-seq').textContent=item?String(item.sequence||'—'):'—';
            row.querySelector('.gv-prefetch-diag-name').textContent=item?String(item.name||''):'EMPTY';
            row.querySelector('.gv-prefetch-diag-hd').textContent=stateText(item?.state||'EMPTY');
            row.querySelector('.gv-prefetch-diag-aladin').textContent=stateText(aladin?.state||'EMPTY');
            row.querySelector('.gv-prefetch-diag-web').textContent=stateText(web?.state||'EMPTY');
            row.dataset.key=item?.key||'';row.dataset.sequence=String(item?.sequence||0);
        });
        const active=api.getActiveDestination?.();ui.active.textContent=active?`ACTIVE / TRAVELING TO — ${String(active.name||active.bannerName||'')} — SEQ ${active.sequence||'—'}`:'ACTIVE / TRAVELING TO —';
        const recovery=window.__gv11eRecoveryEvents||[],latest=recovery[recovery.length-1];ui.status.textContent=latest?`RECOVERY — ${normalized(latest.type)}`:`TELEMETRY — MOUNTED | WEB ${webState.items?.length||0}/10`;
        ui.panel.classList.toggle('gv-prefetch-diag-hidden',Boolean(api.randomGalaxy?.getState?.().hdOpen));
    }
    function captureInteraction(event){
        const target=event.target?.closest?.('button,a,[role="button"]');if(!target)return;
        const id=String(target.id||''),label=String(target.getAttribute('aria-label')||target.textContent||'').trim().replace(/\s+/g,' ').slice(0,160);
        const interesting=id==='gv-random-galaxy'||id==='gv-hd-archive-button'||id==='gv-archive-back'||id==='gv-hd-download-button'||/VIEW .* IN HD|BACK TO SKY|PREVIOUS GALAXY|NEXT GALAXY/i.test(label);if(!interesting)return;
        const api=window.GV10E;interactions.push(nowRecord('ui-click',{id,label,active:clone(api?.getActiveDestination?.()||null),randomButton:randomButtonState('ui-click:'+id)}));if(interactions.length>5000)interactions.splice(0,interactions.length-5000);
    }
    function snapshot(api,reason='interval'){
        const events=api.getPrefetchEvents?.()||[];
        const record={at:new Date().toISOString(),ms:performance.now(),reason,background:clone(api.getBackgroundWorkState?.()||null),hdSlots:clone(api.getHdSlots?.()||[]),aladinSlots:clone(api.getAladinSlots?.()||[]),web:clone(api.getArchivePreloadState?.()||null),active:clone(api.getActiveDestination?.()||null),randomButton:randomButtonState(reason),recovery:clone(window.__gv11eRecoveryEvents||[]),newEvents:clone(events.slice(lastEventCount))};lastEventCount=events.length;snapshots.push(record);if(snapshots.length>5000)snapshots.splice(0,snapshots.length-5000);return record;
    }
    function resourceTiming(){try{return performance.getEntriesByType('resource').map(entry=>({name:entry.name,startTime:entry.startTime,duration:entry.duration,transferSize:entry.transferSize||null,encodedBodySize:entry.encodedBodySize||null,decodedBodySize:entry.decodedBodySize||null,initiatorType:entry.initiatorType||''})).filter(entry=>/aladin|esahubble|esawebb|chandra|Galaxy_Viewer/i.test(entry.name)).slice(-1500)}catch(_){return []}}
    function download(api){snapshot(api,'download');const events=clone(api.getPrefetchEvents?.()||[]),report={schema:'GV-PREFETCH-DIAGNOSTIC-0005',viewerVersion:String(api.version||''),diagnosticsVersion:VERSION,sessionStartedAt,sessionDurationMs:Math.round((performance.now()-sessionStartedMs)*10)/10,downloadedAt:new Date().toISOString(),catalogDatabaseCounts:clone(api.catalogDatabaseCounts||{}),startupMetrics:clone(api.startupMetrics||{}),finalBackground:clone(api.getBackgroundWorkState?.()||null),finalHdSlots:clone(api.getHdSlots?.()||[]),finalAladinSlots:clone(api.getAladinSlots?.()||[]),finalWebPreload:clone(api.getArchivePreloadState?.()||null),finalActive:clone(api.getActiveDestination?.()||null),randomButton:randomButtonState('download'),recovery:clone(window.__gv11eRecoveryEvents||[]),events,interactions:clone(interactions),resourceTiming:resourceTiming(),snapshots};const blob=new Blob([JSON.stringify(report,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a'),stamp=new Date().toISOString().replace(/[:.]/g,'-');a.href=url;a.download=`GV-11E-prefetch-diagnostic-${stamp}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000)}
    async function mount(){
        if(mounted)return;mounted=true;installStyle();const ui=makeTable(),button=document.createElement('button');button.id='gv-prefetch-download-report';button.type='button';button.textContent='DOWNLOAD REPORT';button.disabled=true;document.addEventListener('click',captureInteraction,true);document.body.append(ui.panel,button);
        const transitionSample=reason=>{const api=window.GV10E;if(api)snapshot(api,reason)};
        window.addEventListener('pageshow',()=>transitionSample('pageshow'));document.addEventListener('visibilitychange',()=>{if(!document.hidden)transitionSample('visibility-visible')});document.addEventListener('gv-launcher-recovery',()=>transitionSample('launcher-recovery'));
        try{const api=await waitForApi();button.disabled=false;button.addEventListener('click',()=>download(api));ui.status.textContent='TELEMETRY — MOUNTED';snapshot(api,'mount');render(api,ui);timer=setInterval(()=>{snapshot(api,'2-second');render(api,ui)},2000);window.addEventListener('beforeunload',()=>{if(timer)clearInterval(timer);document.removeEventListener('click',captureInteraction,true)},{once:true})}catch(error){ui.status.textContent='TELEMETRY — ERROR: '+String(error?.message||error);ui.status.style.color='#FF8C8C';throw error}
    }
    window.GVPrefetchDiagnostics0005=Object.freeze({version:VERSION,mount,getSnapshots:()=>clone(snapshots),getInteractions:()=>clone(interactions),getRandomButtonState:()=>randomButtonState('manual')});
    mount().catch(error=>console.error('GV PREFETCH DIAGNOSTICS 0005 FAILURE',error));
})();