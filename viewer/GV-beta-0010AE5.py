from IPython.display import HTML, Javascript, display

# GV-beta-0010AE5
# Surgical runtime patch over current AE3 behavior.
# Authorized changes only: HD-ready selection integrity, persistent retry, truthful HD/ALDN diagnostics, and AE5 labels.

display(HTML("""
<div id="gv-ae5-bootstrap" style="position:fixed;inset:0;background:#000;z-index:2147483647"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const AE2_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/8476dc286c55cb2a75801e1858292587c9146f29/viewer/GV-beta-0010AE2.py';
    const CHANDRA_OLD='viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001.json';
    const CHANDRA_AE3='viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001-FOV-updated.json';
    const OVERRIDE_OLD='chandraTestTotal=chandraTestQueue.length;\n        chandraTestOverrideActive=false;';
    const OVERRIDE_AE3='chandraTestTotal=chandraTestQueue.length;\n        chandraTestOverrideActive=chandraTestTotal>0;';

    const replaceOnce=(source,oldText,newText,label)=>{
        const count=source.split(oldText).length-1;
        if(count!==1)throw new Error(`AE5 PATCH ${label} COUNT ${count}`);
        return source.replace(oldText,newText);
    };
    const replaceBlock=(source,start,end,newBlock,label)=>{
        const a=source.indexOf(start),b=source.indexOf(end,a+start.length);
        if(a<0||b<0)throw new Error(`AE5 BLOCK ${label} ANCHOR MISSING`);
        return source.slice(0,a)+newBlock+source.slice(b);
    };
    function mountHtml(html){
        const template=document.createElement('template');
        template.innerHTML=html;
        for(const node of [...template.content.childNodes]){
            if(node.nodeName==='SCRIPT'){
                const script=document.createElement('script');
                for(const attr of [...node.attributes])script.setAttribute(attr.name,attr.value);
                script.textContent=node.textContent;
                document.body.appendChild(script);
            }else document.body.appendChild(node);
        }
    }

    const response=await fetch(AE2_URL+'?t='+Date.now(),{cache:'no-store'});
    if(!response.ok)throw new Error('AE5 BASELINE FETCH FAILED HTTP '+response.status);
    let source=await response.text();

    // Preserve AE3 runtime behavior exactly before applying AE5 diagnostics/queue repairs.
    source=replaceOnce(source,CHANDRA_OLD,CHANDRA_AE3,'AE3 CHANDRA');
    source=replaceOnce(source,OVERRIDE_OLD,OVERRIDE_AE3,'AE3 CHANDRA OVERRIDE');
    source=source.replaceAll('10AE2','10AE5');

    source=replaceOnce(source,
        'const prefetchRetryAfter=new Map();',
        'const prefetchRetryAfter=new Map();\n    const prefetchRetryAttempts=new Map();\n    const prefetchRetryMeta=new Map();',
        'RETRY MAPS');

    source=replaceOnce(source,
        'prefetchRetryAfter.delete(key);',
        'prefetchRetryAfter.delete(key);\n                prefetchRetryAttempts.delete(key);\n                prefetchRetryMeta.delete(key);',
        'RETRY RESET');

    source=replaceOnce(source,
        "prefetchFailedCount++;\n                setHdStatus(destination,'RETRY-WAIT');\n                prefetchRetryAfter.set(key,Date.now()+PREFETCH_RETRY_MS);",
        "prefetchFailedCount++;\n                const attempt=Number(prefetchRetryAttempts.get(key)||0)+1;\n                prefetchRetryAttempts.set(key,attempt);\n                const delay=Math.min(30000,5000*Math.pow(2,Math.min(3,attempt-1)));\n                const retryAt=Date.now()+delay;\n                setHdStatus(destination,'RETRY-WAIT');\n                prefetchRetryAfter.set(key,retryAt);\n                prefetchRetryMeta.set(key,{attempt,retryAt,lastError:String(error?.message||error||'HD PRELOAD FAILED')});",
        'PERSISTENT RETRY');

    const choosePrefetchBlock=`function choosePrefetchCandidate(){
        const blocked=blockedPrefetchKeys(),now=Date.now();
        if(chandraTestOverrideActive&&chandraTestQueue.length){
            const priority=chandraTestQueue.find(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
            if(priority)return priority;
        }
        for(const [key,retryAt] of prefetchRetryAfter.entries()){
            if(now<Number(retryAt)||blocked.has(key))continue;
            const retry=galaxyCatalog.find(item=>destinationKey(item)===key);
            if(retry)return retry;
        }
        const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
        if(!pool.length)return null;
        const warmed=pool.filter(item=>aladinPrewarmedKeys.has(destinationKey(item)));
        const preferred=warmed.length?warmed:pool;
        return preferred[Math.floor(Math.random()*preferred.length)];
    }

    `;
    source=replaceBlock(source,'function choosePrefetchCandidate(){','function chooseAladinAheadCandidates(',choosePrefetchBlock,'PREFETCH CANDIDATE');

    const randomProviderBlock=`function consumePreferredReady(excludeName='',provider=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        const allowed=(item)=>item&&item.destination&&item.destination.name.toLowerCase()!==excluded&&(!provider||String(item.destination.provider||'').toUpperCase()===provider);
        let index=prefetchReady.findIndex(item=>allowed(item)&&aladinPrewarmedKeys.has(item.key));
        if(index<0)index=prefetchReady.findIndex(allowed);
        if(index<0)return null;
        const [item]=prefetchReady.splice(index,1);
        setPreparedActive(item);
        if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
        return destinationWithPrepared(item);
    }

    function consumeReadyChandraTest(excludeName=''){
        if(!chandraTestOverrideActive||!chandraTestQueue.length)return null;
        const ready=consumePreferredReady(excludeName,'CHANDRA');
        if(!ready)return null;
        const key=destinationKey(ready);
        const queueIndex=chandraTestQueue.findIndex(item=>destinationKey(item)===key);
        if(queueIndex>=0)chandraTestQueue.splice(queueIndex,1);
        if(!chandraTestQueue.length)chandraTestOverrideActive=false;
        return ready;
    }

    function randomHubbleProvider({excludeName}={}){
        let destination=null;
        if(forcedDestination){
            releaseActiveArchivePreload();
            const requested=forcedDestination;
            forcedDestination=null;
            destination=consumeReady(requested,excludeName);
            if(!destination)destination=setUnpreparedActive(requested);
        }else{
            if(!galaxyCatalog.length)throw new Error('COMBINED GALAXY CATALOG IS EMPTY');
            releaseActiveArchivePreload();
            destination=consumeReadyChandraTest(excludeName);
            if(!destination)destination=consumePreferredReady(excludeName);
            if(!destination){
                const requested=galaxyCatalog[Math.floor(Math.random()*galaxyCatalog.length)];
                destination=setUnpreparedActive(requested);
                console.warn('GV-10AE5 NO_READY_HD_DESTINATION',destinationKey(destination));
            }
        }
        activeTargetKey=destinationKey(destination);
        if(Number.isFinite(Number(destination.aladinRotation))&&typeof window.aladin_cosmic_command_test?.setRotation==='function'){
            try{window.aladin_cosmic_command_test.setRotation(Number(destination.aladinRotation))}catch(error){console.warn('GV-10G OPTIONAL ARRIVAL ROTATION SKIPPED',error)}
        }else if(typeof window.aladin_cosmic_command_test?.setRotation==='function'){
            try{window.aladin_cosmic_command_test.setRotation(0)}catch(_){}
        }
        beginTravelHud(destination);
        return destination;
    }

    `;
    source=replaceBlock(source,'function randomHubbleProvider({excludeName}={}){','function getHubblePrefetchState(){',randomProviderBlock,'RANDOM READY SELECTION');

    const apiHelpers=`function getHdPipelineSlots(){
        const slots=[],seen=new Set();
        const add=(destination,state,keyOverride='')=>{
            const key=keyOverride||destinationKey(destination);if(!key||seen.has(key)||slots.length>=10)return;
            seen.add(key);
            const meta=prefetchRetryMeta.get(key)||{};
            const status=hdDownloadStatus.get(key)||{};
            slots.push(Object.freeze({slot:slots.length+1,key,provider:String(destination?.provider||'HUBBLE').toUpperCase(),name:String(destination?.name||status?.name||key),state,attempt:Number(meta.attempt||0),bytesReceived:null,totalBytes:null,percent:state==='READY'?100:state==='DECODING'?82:state==='DOWNLOADING'?48:state==='QUEUED'?14:state==='RETRY'?8:0,sourceKind:String(status?.sourceKind||''),lastError:String(meta.lastError||''),retryAt:Number(meta.retryAt||0),ready:state==='READY',aladinReady:aladinPrewarmedKeys.has(key)}));
        };
        prefetchReady.forEach(item=>add(item.destination,'READY',item.key));
        for(const key of prefetchLoading.keys())add(galaxyCatalog.find(item=>destinationKey(item)===key),'DOWNLOADING',key);
        prefetchQueued.forEach(item=>add(item,'QUEUED'));
        for(const [key,retryAt] of prefetchRetryAfter.entries())if(Number(retryAt)>Date.now())add(galaxyCatalog.find(item=>destinationKey(item)===key),'RETRY',key);
        while(slots.length<10)slots.push(Object.freeze({slot:slots.length+1,key:'',provider:'',name:'',state:'EMPTY',attempt:0,bytesReceived:null,totalBytes:null,percent:0,sourceKind:'',lastError:'',retryAt:0,ready:false,aladinReady:false}));
        return Object.freeze(slots);
    }

    function getAladinPipelineSlots(){
        const keys=[...aladinPrewarmedKeys];
        const active=String(aladinPrewarmActiveKey||'');
        if(active&&!keys.includes(active))keys.unshift(active);
        const out=[];
        for(const key of keys.slice(0,10)){
            const destination=galaxyCatalog.find(item=>destinationKey(item)===key);
            out.push(Object.freeze({slot:out.length+1,key,name:String(destination?.name||key),state:key===active&&!aladinPrewarmedKeys.has(key)?'LOAD':'READY',active:key===active,ready:aladinPrewarmedKeys.has(key)}));
        }
        while(out.length<10)out.push(Object.freeze({slot:out.length+1,key:'',name:'',state:'EMPTY',active:false,ready:false}));
        return Object.freeze(out);
    }

    function getActiveDestinationDiagnostic(){
        const destination=randomGalaxy.getState?.().activeDestination||randomGalaxy.activeDestination||null;
        const key=destinationKey(destination);
        const slot=getHdPipelineSlots().find(item=>item.key===key);
        return Object.freeze({key,provider:String(destination?.provider||''),name:String(destination?.name||''),state:slot?.state||(activePreparedItem?.key===key?'READY':'UNPREPARED'),slot:slot?.slot||null,aladinReady:aladinPrewarmedKeys.has(key)});
    }

    `;
    source=replaceOnce(source,'window.GV10E=Object.freeze({version:VERSION,displayVersion:DISPLAY_VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,universeContext,homeOverlay,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,catalogDatabaseCounts,startupMetrics,getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,startHubblePrefetch:fillPrefetchQueue,getChandraTestOverrideState:()=>Object.freeze({chandraTestOverrideActive,chandraTestRemaining:chandraTestQueue.length,chandraTestTotal}),getGalaxyHistory:()=>({index:galaxyHistoryIndex,items:galaxyHistory.map(item=>({name:item.name,archiveId:item.archiveId,provider:item.provider||\'HUBBLE\'}))})});',apiHelpers+"window.GV10E=Object.freeze({version:VERSION,displayVersion:DISPLAY_VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,universeContext,homeOverlay,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,catalogDatabaseCounts,startupMetrics,getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,getHdPipelineSlots,getAladinPipelineSlots,getActiveDestinationDiagnostic,startHubblePrefetch:fillPrefetchQueue,getChandraTestOverrideState:()=>Object.freeze({chandraTestOverrideActive,chandraTestRemaining:chandraTestQueue.length,chandraTestTotal}),getGalaxyHistory:()=>({index:galaxyHistoryIndex,items:galaxyHistory.map(item=>({name:item.name,archiveId:item.archiveId,provider:item.provider||'HUBBLE'}))})});",'DIAGNOSTIC API');

    const htmlMatch=source.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/);
    const jsMatches=[...source.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(!htmlMatch||!jsMatches.length)throw new Error('AE5 BASELINE EXTRACTION FAILED');

    document.getElementById('gv-ae5-bootstrap')?.remove();
    mountHtml(htmlMatch[1]);
    for(const match of jsMatches){const script=document.createElement('script');script.textContent=match[1];document.body.appendChild(script)}

    const waitForViewer=async()=>{for(let i=0;i<400;i++){if(window.GV10E?.getHdPipelineSlots)return window.GV10E;await new Promise(r=>setTimeout(r,25))}throw new Error('AE5 VIEWER API TIMEOUT')};
    const api=await waitForViewer();
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('AE5 VIEWER ROOT MISSING');

    const style=document.createElement('style');
    style.textContent=`#gv-ae5-diag{position:absolute;left:0;right:0;bottom:max(360px,26vh);z-index:7600;pointer-events:none;font-family:monospace;color:#DFFFEA;text-shadow:0 0 3px #000}#gv-ae5-hd,#gv-ae5-aldn{position:absolute;top:0;width:158px;box-sizing:border-box;border:1px solid rgba(120,255,171,.72);border-radius:5px;background:rgba(0,10,7,.82);padding:4px 5px}#gv-ae5-hd{right:8px}#gv-ae5-aldn{left:8px}.gv-ae5-title{color:#78FFAB;font:700 8px/11px monospace;letter-spacing:.8px;text-align:center;margin-bottom:3px}.gv-ae5-row{display:grid;grid-template-columns:12px 1fr 42px;gap:3px;align-items:center;height:12px;font:7px/10px monospace;white-space:nowrap}.gv-ae5-name{overflow:hidden;text-overflow:ellipsis}.gv-ae5-track{height:4px;border:1px solid rgba(120,255,171,.38);border-radius:3px;background:rgba(8,30,18,.76);overflow:hidden}.gv-ae5-fill{height:100%;background:linear-gradient(90deg,#1C7D47,#78FFAB)}.gv-ae5-fail{color:#FF8D8D}.gv-ae5-active{margin-top:4px;border-top:1px solid rgba(120,255,171,.24);padding-top:3px;font:7px/9px monospace;color:#CFFFE0}#gv-ae5-diag.gv-hide{display:none!important}`;
    document.head.appendChild(style);
    const diag=document.createElement('div');diag.id='gv-ae5-diag';
    const hd=document.createElement('div');hd.id='gv-ae5-hd';hd.innerHTML='<div class="gv-ae5-title">HD</div>';
    const aldn=document.createElement('div');aldn.id='gv-ae5-aldn';aldn.innerHTML='<div class="gv-ae5-title">ALDN</div>';
    for(let i=1;i<=10;i++){
        const row=document.createElement('div');row.className='gv-ae5-row';row.innerHTML=`<span>${i}</span><span class="gv-ae5-name">EMPTY</span><span class="gv-ae5-track"><span class="gv-ae5-fill" style="width:0%"></span></span>`;hd.appendChild(row);
        const arow=document.createElement('div');arow.className='gv-ae5-row';arow.innerHTML=`<span>${i}</span><span class="gv-ae5-name">EMPTY</span><span></span>`;aldn.appendChild(arow);
    }
    const active=document.createElement('div');active.className='gv-ae5-active';active.textContent='ACTIVE —';hd.appendChild(active);
    diag.append(hd,aldn);root.appendChild(diag);

    const providerAbbr=p=>p==='CHANDRA'?'CHA':p==='JWST'?'JWS':'HUB';
    const render=()=>{
        const hs=api.getHdPipelineSlots();
        [...hd.querySelectorAll('.gv-ae5-row')].forEach((row,i)=>{
            const item=hs[i];const name=row.querySelector('.gv-ae5-name');const fill=row.querySelector('.gv-ae5-fill');
            const state=item.state==='READY'?'✓':item.state==='RETRY'?'RETRY':item.state;
            name.textContent=item.key?`${providerAbbr(item.provider)} ${item.name} ${state}`:'EMPTY';
            row.classList.toggle('gv-ae5-fail',item.state==='RETRY');fill.style.width=`${Math.max(0,Math.min(100,Number(item.percent||0)))}%`;
        });
        const as=api.getAladinPipelineSlots();
        [...aldn.querySelectorAll('.gv-ae5-row')].forEach((row,i)=>{const item=as[i];row.querySelector('.gv-ae5-name').textContent=item.key?`${item.active?'→ ':''}${item.name} ${item.ready?'✓':item.state}`:'EMPTY'});
        const ac=api.getActiveDestinationDiagnostic();active.textContent=`ACTIVE ${providerAbbr(ac.provider)} ${ac.name||'—'} — ${ac.state}${ac.slot?` #${ac.slot}`:''} / ALDN ${ac.aladinReady?'✓':'NO'}`;
        const hdOpen=Boolean(api.randomGalaxy?.getState?.().hdOpen);diag.classList.toggle('gv-hide',hdOpen);
    };
    render();setInterval(render,250);
})().catch(error=>{
    console.error('GALAXY VIEWER 10AE5 BOOTSTRAP FAILURE:',error);
    const box=document.getElementById('gv-ae5-bootstrap')||document.body.appendChild(document.createElement('div'));
    box.id='gv-ae5-bootstrap';Object.assign(box.style,{position:'fixed',inset:'0',zIndex:'2147483647',padding:'24px',boxSizing:'border-box',background:'#000',color:'#FFD166',whiteSpace:'pre-wrap',font:'14px/1.45 monospace'});box.textContent='GALAXY VIEWER 10AE5 FAILED TO LOAD\n\n'+String(error?.stack||error);
});
"""))

# GV-beta-0010AE5 staged
