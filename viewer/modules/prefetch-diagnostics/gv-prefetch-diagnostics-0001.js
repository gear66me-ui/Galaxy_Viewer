/* Galaxy Viewer Prefetch Diagnostics 0001 — read-only telemetry overlay/export. */
(()=>{
    'use strict';
    if(window.GVPrefetchDiagnostics0001)return;
    const VERSION='0001';
    const sessionStartedAt=new Date().toISOString();
    const snapshots=[];
    let timer=0;
    let mounted=false;
    let lastEventCount=0;

    const waitForApi=async()=>{
        for(let i=0;i<600;i++){
            const api=window.GV10E;
            if(api&&typeof api.getHdSlots==='function'&&typeof api.getAladinSlots==='function')return api;
            await new Promise(resolve=>setTimeout(resolve,100));
        }
        throw new Error('11A TELEMETRY API TIMEOUT');
    };
    const clone=value=>JSON.parse(JSON.stringify(value??null));
    const shortProvider=value=>value==='CHANDRA'?'CHA':value==='JWST'?'JWS':'HUB';
    const shortState=value=>({QUEUED:'Q',DOWNLOADING:'DL',DECODING:'DEC',RETRY:'RET',READY:'✓',EMPTY:'—',WAIT:'WAIT',LOADING:'LOAD',FAILED:'FAIL'}[String(value||'').toUpperCase()]||String(value||'').slice(0,5));

    function makePanel(id,title,side){
        const panel=document.createElement('div');panel.id=id;panel.className='gv-prefetch-diag-panel';panel.dataset.side=side;
        const heading=document.createElement('div');heading.className='gv-prefetch-diag-title';heading.textContent=title;panel.appendChild(heading);
        for(let i=1;i<=10;i++){
            const row=document.createElement('div');row.className='gv-prefetch-diag-row';row.innerHTML=`<span class="gv-prefetch-diag-num">${i}</span><span class="gv-prefetch-diag-name">EMPTY</span><span class="gv-prefetch-diag-state">—</span>`;panel.appendChild(row);
        }
        return panel;
    }
    function installStyle(){
        const style=document.createElement('style');style.id='gv-prefetch-diag-style';style.textContent=`
.gv-prefetch-diag-panel{position:fixed;top:44%;transform:translateY(-50%);z-index:7600;width:138px;box-sizing:border-box;padding:4px 5px;border:1px solid rgba(120,255,171,.58);border-radius:5px;background:rgba(0,10,7,.72);color:#DFFFEA;font:7px/11px monospace;text-shadow:0 0 3px #000;pointer-events:none}
.gv-prefetch-diag-panel[data-side="left"]{left:5px}.gv-prefetch-diag-panel[data-side="right"]{right:5px}
.gv-prefetch-diag-title{text-align:center;color:#78FFAB;font-weight:700;letter-spacing:.8px;margin-bottom:2px}.gv-prefetch-diag-row{display:grid;grid-template-columns:11px minmax(0,1fr) 28px;gap:2px;height:11px;align-items:center;white-space:nowrap}.gv-prefetch-diag-name{overflow:hidden;text-overflow:ellipsis}.gv-prefetch-diag-state{text-align:right}.gv-prefetch-diag-active{margin-top:3px;padding-top:3px;border-top:1px solid rgba(120,255,171,.25);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#gv-prefetch-download-report{position:fixed;left:50%;top:8px;transform:translateX(-50%);z-index:7601;height:24px;padding:0 8px;border:1px solid #78FFAB;border-radius:5px;background:rgba(0,45,26,.88);color:#DFFFEA;font:700 8px/22px monospace;letter-spacing:.5px;cursor:pointer;touch-action:manipulation}
.gv-prefetch-diag-hidden{display:none!important}`;document.head.appendChild(style);
    }
    function snapshot(api,reason='interval'){
        const events=api.getPrefetchEvents?.()||[];
        const record={at:new Date().toISOString(),reason,hdSlots:clone(api.getHdSlots?.()||[]),aladinSlots:clone(api.getAladinSlots?.()||[]),active:clone(api.getActiveDestination?.()||null),newEvents:clone(events.slice(lastEventCount))};
        lastEventCount=events.length;snapshots.push(record);return record;
    }
    function render(api,hdPanel,aladinPanel,activeLine){
        const hd=api.getHdSlots?.()||[],aladin=api.getAladinSlots?.()||[];
        const hdRows=[...hdPanel.querySelectorAll('.gv-prefetch-diag-row')],alRows=[...aladinPanel.querySelectorAll('.gv-prefetch-diag-row')];
        hdRows.forEach((row,index)=>{const item=hd[index]||{};row.querySelector('.gv-prefetch-diag-name').textContent=item.key?`${shortProvider(item.provider)} ${item.name}`:'EMPTY';row.querySelector('.gv-prefetch-diag-state').textContent=shortState(item.state)});
        alRows.forEach((row,index)=>{const item=aladin[index]||{};row.querySelector('.gv-prefetch-diag-name').textContent=item.key?`${shortProvider(item.provider)} ${item.name}`:'EMPTY';row.querySelector('.gv-prefetch-diag-state').textContent=shortState(item.state)});
        const active=api.getActiveDestination?.();activeLine.textContent=active?`ACTIVE ${active.name} ${active.slot?`#${active.slot}`:'FALLBACK'}`:'ACTIVE —';
        const hidden=Boolean(api.randomGalaxy?.getState?.().hdOpen);hdPanel.classList.toggle('gv-prefetch-diag-hidden',hidden);aladinPanel.classList.toggle('gv-prefetch-diag-hidden',hidden);
    }
    function download(api){
        snapshot(api,'download');
        const report={schema:'GV-PREFETCH-DIAGNOSTIC-0001',viewerVersion:String(api.version||''),diagnosticsVersion:VERSION,sessionStartedAt,downloadedAt:new Date().toISOString(),catalogDatabaseCounts:clone(api.catalogDatabaseCounts||{}),startupMetrics:clone(api.startupMetrics||{}),finalHdSlots:clone(api.getHdSlots?.()||[]),finalAladinSlots:clone(api.getAladinSlots?.()||[]),finalActive:clone(api.getActiveDestination?.()||null),events:clone(api.getPrefetchEvents?.()||[]),snapshots};
        const blob=new Blob([JSON.stringify(report,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a'),stamp=new Date().toISOString().replace(/[:.]/g,'-');a.href=url;a.download=`GV-11A-prefetch-diagnostic-${stamp}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
    }
    async function mount(){
        if(mounted)return;mounted=true;const api=await waitForApi();installStyle();
        const hdPanel=makePanel('gv-prefetch-diag-hd','HD','right'),aladinPanel=makePanel('gv-prefetch-diag-aladin','ALDN','left'),activeLine=document.createElement('div');activeLine.className='gv-prefetch-diag-active';activeLine.textContent='ACTIVE —';hdPanel.appendChild(activeLine);
        const button=document.createElement('button');button.id='gv-prefetch-download-report';button.type='button';button.textContent='DOWNLOAD REPORT';button.addEventListener('click',()=>download(api));document.body.append(aladinPanel,hdPanel,button);
        snapshot(api,'mount');render(api,hdPanel,aladinPanel,activeLine);
        timer=setInterval(()=>{snapshot(api,'5-second');render(api,hdPanel,aladinPanel,activeLine)},5000);
        window.addEventListener('beforeunload',()=>{if(timer)clearInterval(timer)},{once:true});
    }
    window.GVPrefetchDiagnostics0001=Object.freeze({version:VERSION,mount,getSnapshots:()=>clone(snapshots)});
    mount().catch(error=>console.error('GV PREFETCH DIAGNOSTICS 0001 FAILURE',error));
})();
