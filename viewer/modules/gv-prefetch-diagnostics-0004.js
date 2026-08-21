/* Galaxy Viewer Prefetch Diagnostics 0004 — deterministic rolling telemetry, execution diary, recovery status, and export. */
(()=>{
    'use strict';
    if(window.GVPrefetchDiagnostics0004)return;
    const VERSION='0004';
    const sessionStartedAt=new Date().toISOString();
    const sessionStartedMs=performance.now();
    const snapshots=[];
    const interactions=[];
    const webRecent=new Map();
    let timer=0;
    let mounted=false;
    let lastEventCount=0;

    const waitForApi=async()=>{
        for(let i=0;i<600;i++){
            const api=window.GV10E;
            if(api&&String(api.version)==='11D'&&typeof api.getHdSlots==='function'&&typeof api.getAladinSlots==='function'&&typeof api.getArchivePreloadState==='function')return api;
            await new Promise(resolve=>setTimeout(resolve,100));
        }
        throw new Error('11D TELEMETRY API TIMEOUT');
    };
    const clone=value=>JSON.parse(JSON.stringify(value??null));
    const shortProvider=value=>value==='CHANDRA'?'CHA':value==='JWST'?'JWS':'HUB';
    const shortState=value=>({QUEUED:'Q',DOWNLOADING:'DL',DECODING:'DEC',RETRY:'RET',SUSPENDED:'SUSP',READY:'✓',EMPTY:'—',WAIT:'WAIT',LOADING:'LOAD',PENDING:'PEND',FAILED:'FAIL'}[String(value||'').toUpperCase()]||String(value||'').slice(0,5));
    const nowRecord=(type,detail={})=>({at:new Date().toISOString(),ms:performance.now(),type,...detail});

    function makePanel(id,title,side,rowCount){
        const panel=document.createElement('div');panel.id=id;panel.className='gv-prefetch-diag-panel';panel.dataset.side=side;
        const heading=document.createElement('div');heading.className='gv-prefetch-diag-title';heading.textContent=title;panel.appendChild(heading);
        for(let i=0;i<rowCount;i++){
            const row=document.createElement('div');row.className='gv-prefetch-diag-row';row.innerHTML='<span class="gv-prefetch-diag-num">—</span><span class="gv-prefetch-diag-name">EMPTY</span><span class="gv-prefetch-diag-state">—</span>';panel.appendChild(row);
        }
        return panel;
    }
    function installStyle(){
        const style=document.createElement('style');style.id='gv-prefetch-diag-style-0004';style.textContent=`
.gv-prefetch-diag-panel{position:fixed;top:44%;transform:translateY(-50%);z-index:7600;width:138px;box-sizing:border-box;padding:4px 5px;border:1px solid rgba(120,255,171,.58);border-radius:5px;background:rgba(0,10,7,.72);color:#DFFFEA;font:7px/11px monospace;text-shadow:0 0 3px #000;pointer-events:none}
.gv-prefetch-diag-panel[data-side="left"]{left:5px}.gv-prefetch-diag-panel[data-side="right"]{right:5px}
#gv-prefetch-diag-web{top:auto!important;bottom:42px!important;left:5px!important;right:auto!important;transform:none!important}
.gv-prefetch-diag-title{text-align:center;color:#78FFAB;font-weight:700;letter-spacing:.8px;margin-bottom:2px}.gv-prefetch-diag-row{display:grid;grid-template-columns:20px minmax(0,1fr) 28px;gap:2px;height:11px;align-items:center;white-space:nowrap}.gv-prefetch-diag-num{text-align:right}.gv-prefetch-diag-name{overflow:hidden;text-overflow:ellipsis}.gv-prefetch-diag-state{text-align:right}.gv-prefetch-diag-active{margin-top:3px;padding-top:3px;border-top:1px solid rgba(120,255,171,.25);white-space:normal;overflow-wrap:anywhere;color:#FFD85A}.gv-prefetch-diag-status{margin-top:3px;padding-top:3px;border-top:1px solid rgba(120,255,171,.25);white-space:normal;overflow-wrap:anywhere;color:#78FFAB}
#gv-prefetch-download-report{position:fixed;left:50%;top:8px;transform:translateX(-50%);z-index:7601;height:24px;padding:0 8px;border:1px solid #78FFAB;border-radius:5px;background:rgba(0,45,26,.88);color:#DFFFEA;font:700 8px/22px monospace;letter-spacing:.5px;cursor:pointer;touch-action:manipulation}
#gv-prefetch-download-report:disabled{opacity:.55;cursor:default}.gv-prefetch-diag-hidden{display:none!important}`;document.head.appendChild(style);
    }
    function captureInteraction(event){
        const target=event.target?.closest?.('button,a,[role="button"]');
        if(!target)return;
        const id=String(target.id||'');
        const text=String(target.getAttribute('aria-label')||target.textContent||'').trim().replace(/\s+/g,' ').slice(0,120);
        const interesting=id==='gv-random-galaxy'||id==='gv-hd-archive-button'||id==='gv-archive-back'||id==='gv-hd-download-button'||/VIEW .* IN HD|BACK TO SKY|PREVIOUS GALAXY|NEXT GALAXY/i.test(text);
        if(!interesting)return;
        const api=window.GV10E,active=api?.getActiveDestination?.()||null;
        interactions.push(nowRecord('ui-click',{id,label:text,active:clone(active)}));
        if(interactions.length>5000)interactions.splice(0,interactions.length-5000);
    }
    function snapshot(api,reason='interval'){
        const events=api.getPrefetchEvents?.()||[];
        const record={at:new Date().toISOString(),ms:performance.now(),reason,background:clone(api.getBackgroundWorkState?.()||null),hdSlots:clone(api.getHdSlots?.()||[]),aladinSlots:clone(api.getAladinSlots?.()||[]),web:clone(api.getArchivePreloadState?.()||null),active:clone(api.getActiveDestination?.()||null),recovery:clone(window.__gv11dRecoveryEvents||[]),newEvents:clone(events.slice(lastEventCount))};
        lastEventCount=events.length;snapshots.push(record);return record;
    }
    function renderRows(panel,items,rowCount){
        const rows=[...panel.querySelectorAll('.gv-prefetch-diag-row')];
        const ordered=[...(items||[])].filter(item=>item&&item.key).sort((a,b)=>(Number(a.sequence)||0)-(Number(b.sequence)||0)).slice(-rowCount);
        rows.forEach((row,index)=>{
            const item=ordered[index]||{};
            row.querySelector('.gv-prefetch-diag-num').textContent=item.key?String(item.sequence||'—'):'—';
            row.querySelector('.gv-prefetch-diag-name').textContent=item.key?String(item.name||'').toUpperCase():'EMPTY';
            row.querySelector('.gv-prefetch-diag-state').textContent=shortState(item.state);
        });
    }
    function render(api,hdPanel,aladinPanel,webPanel,activeLine,statusLine){
        const hd=api.getHdSlots?.()||[],aladin=api.getAladinSlots?.()||[],webState=api.getArchivePreloadState?.()||{},webItems=[...(webState.items||[])];
        if(webState.loading&&!webItems.some(item=>item.key===webState.loading.key))webItems.push(webState.loading);
        for(const item of webItems){if(item?.key)webRecent.set(item.key,clone(item))}
        const rollingWeb=[...webRecent.values()].sort((a,b)=>(Number(a.sequence)||0)-(Number(b.sequence)||0)).slice(-10);
        renderRows(hdPanel,hd,10);renderRows(aladinPanel,aladin,10);renderRows(webPanel,rollingWeb,10);
        const active=api.getActiveDestination?.();activeLine.textContent=active?`TRAVELING TO — ${String(active.bannerName||active.name||'').toUpperCase()}`:'TRAVELING TO —';
        const recovery=window.__gv11dRecoveryEvents||[],latest=recovery[recovery.length-1];statusLine.textContent=latest?`RECOVERY — ${String(latest.type||'').toUpperCase()}`:'TELEMETRY — MOUNTED';
        const hidden=Boolean(api.randomGalaxy?.getState?.().hdOpen);
        hdPanel.classList.toggle('gv-prefetch-diag-hidden',hidden);aladinPanel.classList.toggle('gv-prefetch-diag-hidden',hidden);webPanel.classList.toggle('gv-prefetch-diag-hidden',hidden);
    }
    function duration(a,b){return Number.isFinite(a)&&Number.isFinite(b)&&b>=a?Math.round((b-a)*10)/10:null}
    function summarizeDestinations(events){
        const bySeq=new Map();
        const bucket=sequence=>{const key=Number(sequence)||0;if(!key)return null;if(!bySeq.has(key))bySeq.set(key,{sequence:key,name:'',provider:'',events:[],metrics:{},errors:[]});return bySeq.get(key)};
        for(const event of events){const item=bucket(event.sequence);if(!item)continue;item.events.push(clone(event));if(event.name)item.name=event.name;if(event.provider)item.provider=event.provider;if(/fail|error|retry/i.test(String(event.type||'')))item.errors.push({type:event.type,error:event.error||''})}
        for(const item of bySeq.values()){const first=type=>item.events.find(e=>e.type===type)?.ms;item.metrics={randomClickToTravelSuspendMs:duration(first('random-click'),first('travel-suspend')),travelMs:duration(first('travel-suspend'),first('travel-arrival')),hdClickToVisibleMs:duration(first('hd-entry-click'),first('hd-visible')),providerClickToFrameLoadMs:duration(first('archive-click'),first('archive-frame-load')),providerClickToVisibleMs:duration(first('archive-click'),first('archive-visible')),websitePreloadMs:duration(first('archive-preload-start'),first('archive-preload-ready')),websiteStateAtClick:item.events.find(e=>e.type==='archive-click')?.sourceState??null}}
        return [...bySeq.values()].sort((a,b)=>a.sequence-b.sequence);
    }
    function resourceTiming(){try{return performance.getEntriesByType('resource').map(entry=>({name:entry.name,startTime:entry.startTime,duration:entry.duration,transferSize:entry.transferSize||null,encodedBodySize:entry.encodedBodySize||null,decodedBodySize:entry.decodedBodySize||null,initiatorType:entry.initiatorType||''})).filter(entry=>/aladin|esahubble|esawebb|chandra|Galaxy_Viewer/i.test(entry.name)).slice(-1000)}catch(_){return []}}
    function download(api){
        snapshot(api,'download');
        const events=clone(api.getPrefetchEvents?.()||[]);
        const report={schema:'GV-PREFETCH-DIAGNOSTIC-0004',viewerVersion:String(api.version||''),diagnosticsVersion:VERSION,sessionStartedAt,sessionDurationMs:Math.round((performance.now()-sessionStartedMs)*10)/10,downloadedAt:new Date().toISOString(),catalogDatabaseCounts:clone(api.catalogDatabaseCounts||{}),startupMetrics:clone(api.startupMetrics||{}),finalBackground:clone(api.getBackgroundWorkState?.()||null),finalHdSlots:clone(api.getHdSlots?.()||[]),finalAladinSlots:clone(api.getAladinSlots?.()||[]),finalWebPreload:clone(api.getArchivePreloadState?.()||null),finalActive:clone(api.getActiveDestination?.()||null),recovery:clone(window.__gv11dRecoveryEvents||[]),events,interactions:clone(interactions),perDestination:summarizeDestinations(events),resourceTiming:resourceTiming(),snapshots};
        const blob=new Blob([JSON.stringify(report,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a'),stamp=new Date().toISOString().replace(/[:.]/g,'-');a.href=url;a.download=`GV-11D-prefetch-diagnostic-${stamp}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
    }
    async function mount(){
        if(mounted)return;mounted=true;installStyle();
        const hdPanel=makePanel('gv-prefetch-diag-hd','HD','right',10),aladinPanel=makePanel('gv-prefetch-diag-aladin','ALDN','left',10),webPanel=makePanel('gv-prefetch-diag-web','WEB','left',10),activeLine=document.createElement('div'),statusLine=document.createElement('div');activeLine.className='gv-prefetch-diag-active';activeLine.textContent='TRAVELING TO —';statusLine.className='gv-prefetch-diag-status';statusLine.textContent='TELEMETRY — WAITING FOR 11D';hdPanel.append(activeLine,statusLine);
        const button=document.createElement('button');button.id='gv-prefetch-download-report';button.type='button';button.textContent='DOWNLOAD REPORT';button.disabled=true;document.addEventListener('click',captureInteraction,true);document.body.append(aladinPanel,hdPanel,webPanel,button);
        try{
            const api=await waitForApi();button.disabled=false;button.addEventListener('click',()=>download(api));statusLine.textContent='TELEMETRY — MOUNTED';snapshot(api,'mount');render(api,hdPanel,aladinPanel,webPanel,activeLine,statusLine);
            timer=setInterval(()=>{snapshot(api,'5-second');render(api,hdPanel,aladinPanel,webPanel,activeLine,statusLine)},5000);
            window.addEventListener('beforeunload',()=>{if(timer)clearInterval(timer);document.removeEventListener('click',captureInteraction,true)},{once:true});
        }catch(error){statusLine.textContent='TELEMETRY — ERROR: '+String(error?.message||error);statusLine.style.color='#FF8C8C';throw error}
    }
    window.GVPrefetchDiagnostics0004=Object.freeze({version:VERSION,mount,getSnapshots:()=>clone(snapshots),getInteractions:()=>clone(interactions)});
    mount().catch(error=>console.error('GV PREFETCH DIAGNOSTICS 0004 FAILURE',error));
})();
