from IPython.display import HTML, Javascript, display

# GV-beta-0010AE6
# Direct surgical runtime patch over the known standalone AE2 source.
# Uses the current populated Hubble/JWST/Chandra catalogs on beta.
# Repairs ready-queue selection, persistent retry priority, and truthful HD/ALDN diagnostics.

display(HTML("""
<div id="gv-ae6-bootstrap" style="position:fixed;inset:0;background:#000;z-index:2147483647"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const BASE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/8476dc286c55cb2a75801e1858292587c9146f29/viewer/GV-beta-0010AE2.py';
    const JWST_OLD="const JWST_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/948867116a8f35e5265c4cecf887c60c1df0cd77/viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json?v=bcc37a66bc5bb697b57530d07daee5886c63338a';";
    const JWST_NEW="const JWST_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json';";
    const CHANDRA_CANONICAL="const CHANDRA_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001.json';";

    const replaceOnce=(source,oldText,newText,label)=>{
        const count=source.split(oldText).length-1;
        if(count!==1)throw new Error(`AE6 PATCH ${label} COUNT ${count}`);
        return source.replace(oldText,newText);
    };
    const replaceBlock=(source,start,end,newBlock,label)=>{
        const a=source.indexOf(start),b=source.indexOf(end,a+start.length);
        if(a<0||b<0)throw new Error(`AE6 BLOCK ${label} ANCHOR MISSING`);
        return source.slice(0,a)+newBlock+source.slice(b);
    };
    function mountHtml(html){
        const template=document.createElement('template');template.innerHTML=html;
        for(const node of [...template.content.childNodes]){
            if(node.nodeName==='SCRIPT'){
                const script=document.createElement('script');
                for(const attr of [...node.attributes])script.setAttribute(attr.name,attr.value);
                script.textContent=node.textContent;document.body.appendChild(script);
            }else document.body.appendChild(node);
        }
    }

    const response=await fetch(BASE_URL+'?t='+Date.now(),{cache:'no-store'});
    if(!response.ok)throw new Error('AE6 BASELINE FETCH FAILED HTTP '+response.status);
    let source=await response.text();

    // Catalogs: current populated canonical files on beta.
    source=replaceOnce(source,JWST_OLD,JWST_NEW,'JWST CURRENT CATALOG');
    if(!source.includes("viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0018.json"))throw new Error('AE6 HUBBLE 0018 CATALOG MISSING');
    if(!source.includes(CHANDRA_CANONICAL))throw new Error('AE6 CANONICAL CHANDRA 0001 CATALOG MISSING');

    // Preserve AE3 Chandra-first intent, but never force an unprepared Chandra destination.
    source=replaceOnce(source,
        'chandraTestTotal=chandraTestQueue.length;\n        chandraTestOverrideActive=false;',
        'chandraTestTotal=chandraTestQueue.length;\n        chandraTestOverrideActive=chandraTestTotal>0;',
        'CHANDRA TEST ENABLE');

    // Failed entries are retried ahead of new random candidates once their retry timer expires.
    const choosePrefetch=`function choosePrefetchCandidate(){
        const blocked=blockedPrefetchKeys(),now=Date.now();
        if(chandraTestOverrideActive&&chandraTestQueue.length){
            const chandra=chandraTestQueue.find(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
            if(chandra)return chandra;
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
    source=replaceBlock(source,'function choosePrefetchCandidate(){','function chooseAladinAheadCandidates(',choosePrefetch,'PREFETCH PRIORITY');

    // Random navigation consumes an actually prepared HD entry first. Aladin-prewarmed READY entries win.
    const randomProvider=`function consumeBestReady(excludeName='',provider=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        const acceptable=item=>item&&item.destination&&item.destination.name.toLowerCase()!==excluded&&(!provider||String(item.destination.provider||'').toUpperCase()===provider);
        let index=prefetchReady.findIndex(item=>acceptable(item)&&aladinPrewarmedKeys.has(item.key));
        if(index<0)index=prefetchReady.findIndex(acceptable);
        if(index<0)return null;
        return consumeReady(prefetchReady[index].destination,excludeName);
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
            if(chandraTestOverrideActive){
                destination=consumeBestReady(excludeName,'CHANDRA');
                if(destination){
                    const key=destinationKey(destination);
                    const index=chandraTestQueue.findIndex(item=>destinationKey(item)===key);
                    if(index>=0)chandraTestQueue.splice(index,1);
                    if(!chandraTestQueue.length)chandraTestOverrideActive=false;
                }
            }
            if(!destination)destination=consumeBestReady(excludeName);
            if(!destination){
                const requested=galaxyCatalog[Math.floor(Math.random()*galaxyCatalog.length)];
                destination=setUnpreparedActive(requested);
                console.warn('GV-10AE6 NO READY HD DESTINATION — FALLBACK',destinationKey(destination));
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
    source=replaceBlock(source,'function randomHubbleProvider({excludeName}={}){','function getHubblePrefetchState(){',randomProvider,'READY QUEUE SELECTION');

    // Expose the real Aladin cached destination names, not just aggregate 10/10.
    const aladinState=`function getAladinPrewarmState(){
        const cachedKeys=[...aladinPrewarmedKeys];
        const cachedDestinations=cachedKeys.map(key=>galaxyCatalog.find(item=>destinationKey(item)===key)).filter(Boolean).map(item=>Object.freeze({key:destinationKey(item),name:item.name,provider:item.provider||'HUBBLE'}));
        const activeDestination=galaxyCatalog.find(item=>destinationKey(item)===aladinPrewarmActiveKey)||null;
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            cachedCount:aladinPrewarmedKeys.size,
            activeKey:aladinPrewarmActiveKey,
            activeName:activeDestination?.name||'',
            cachedDestinations:Object.freeze(cachedDestinations),
            queuedDestinations:[]
        });
    }

    `;
    source=replaceBlock(source,'function getAladinPrewarmState(){','function loadScript(',aladinState,'ALADIN STATE');

    source=source.replaceAll('10AE2','10AE6');

    const htmlMatch=source.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/);
    const jsMatches=[...source.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(!htmlMatch||!jsMatches.length)throw new Error('AE6 BASELINE EXTRACTION FAILED');
    document.getElementById('gv-ae6-bootstrap')?.remove();
    mountHtml(htmlMatch[1]);
    for(const match of jsMatches){const script=document.createElement('script');script.textContent=match[1];document.body.appendChild(script)}

    const waitForViewer=async()=>{for(let i=0;i<400;i++){if(window.GV10E)return window.GV10E;await new Promise(r=>setTimeout(r,25))}throw new Error('AE6 VIEWER API TIMEOUT')};
    const api=await waitForViewer();
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('AE6 VIEWER ROOT MISSING');

    const style=document.createElement('style');
    style.textContent=`
#gv-ae6-diag{position:absolute;left:0;right:0;bottom:max(370px,26vh);z-index:7600;pointer-events:none;font-family:monospace;color:#DFFFEA;text-shadow:0 0 3px #000}
#gv-ae6-hd,#gv-ae6-aldn{position:absolute;top:0;width:165px;box-sizing:border-box;border:1px solid rgba(120,255,171,.72);border-radius:5px;background:rgba(0,10,7,.82);padding:4px 5px;box-shadow:0 0 7px rgba(87,255,147,.18)}
#gv-ae6-hd{right:8px}#gv-ae6-aldn{left:8px}.gv-ae6-title{color:#78FFAB;font:700 8px/11px monospace;letter-spacing:.8px;text-align:center;margin-bottom:3px}.gv-ae6-row{display:grid;grid-template-columns:12px 1fr 44px;gap:3px;align-items:center;height:12px;font:7px/10px monospace;white-space:nowrap}.gv-ae6-name{overflow:hidden;text-overflow:ellipsis}.gv-ae6-track{height:4px;border:1px solid rgba(120,255,171,.38);border-radius:3px;background:rgba(8,30,18,.76);overflow:hidden}.gv-ae6-fill{height:100%;width:0;background:linear-gradient(90deg,#1C7D47,#78FFAB);transition:width .18s linear}.gv-ae6-fail{color:#FF8D8D}.gv-ae6-active{margin-top:4px;border-top:1px solid rgba(120,255,171,.24);padding-top:3px;font:7px/9px monospace;color:#CFFFE0}#gv-ae6-diag.gv-hide{display:none!important}`;
    document.head.appendChild(style);
    const diag=document.createElement('div');diag.id='gv-ae6-diag';
    const hd=document.createElement('div');hd.id='gv-ae6-hd';hd.innerHTML='<div class="gv-ae6-title">HD</div>';
    const aldn=document.createElement('div');aldn.id='gv-ae6-aldn';aldn.innerHTML='<div class="gv-ae6-title">ALDN</div>';
    for(let i=1;i<=10;i++){
        const h=document.createElement('div');h.className='gv-ae6-row';h.innerHTML=`<span>${i}</span><span class="gv-ae6-name">EMPTY</span><span class="gv-ae6-track"><span class="gv-ae6-fill"></span></span>`;hd.appendChild(h);
        const a=document.createElement('div');a.className='gv-ae6-row';a.innerHTML=`<span>${i}</span><span class="gv-ae6-name">EMPTY</span><span></span>`;aldn.appendChild(a);
    }
    const active=document.createElement('div');active.className='gv-ae6-active';active.textContent='ACTIVE —';hd.appendChild(active);
    diag.append(hd,aldn);root.appendChild(diag);

    const render=()=>{
        let p={readyDestinations:[],queuedDestinations:[],activeDownloadKeys:[],downloads:[]};
        try{p=api.getHubblePrefetchState?.()||p}catch(_){}
        const statusByKey=new Map((p.downloads||[]).map(item=>[String(item.key||''),item]));
        const slots=[];
        for(const name of p.readyDestinations||[])slots.push({name,state:'READY'});
        for(const key of p.activeDownloadKeys||[]){const s=statusByKey.get(String(key))||{};slots.push({name:s.name||key,state:s.state||'DOWNLOADING'})}
        for(const name of p.queuedDestinations||[])slots.push({name,state:'QUEUED'});
        const recentRetry=(p.downloads||[]).filter(item=>String(item.state||'').toUpperCase()==='RETRY-WAIT').sort((a,b)=>Number(b.updatedAt||0)-Number(a.updatedAt||0));
        for(const item of recentRetry)if(slots.length<10&&!slots.some(x=>x.name===item.name))slots.push({name:item.name,state:'RETRY'});
        const hrows=[...hd.querySelectorAll('.gv-ae6-row')];
        hrows.forEach((row,i)=>{const item=slots[i]||null;const state=String(item?.state||'EMPTY').toUpperCase();row.querySelector('.gv-ae6-name').textContent=item?`${item.name} ${state==='READY'?'✓':state}`:'EMPTY';row.classList.toggle('gv-ae6-fail',state==='RETRY');const pct=state==='READY'?100:state==='DECODING'?82:state==='DOWNLOADING'?48:state==='QUEUED'?14:state==='RETRY'?8:0;row.querySelector('.gv-ae6-fill').style.width=pct+'%'});

        let a={cachedDestinations:[],activeName:'',activeKey:''};try{a=api.getAladinPrewarmState?.()||a}catch(_){}
        const alist=[...(a.cachedDestinations||[])].slice(0,10);
        const arows=[...aldn.querySelectorAll('.gv-ae6-row')];
        arows.forEach((row,i)=>{const item=alist[i]||null;row.querySelector('.gv-ae6-name').textContent=item?`${item.name} ✓`:(i===alist.length&&a.activeName?`→ ${a.activeName} LOAD`:'EMPTY')});

        const current=api.randomGalaxy?.getState?.().activeDestination||api.randomGalaxy?.activeDestination||null;
        const currentName=String(current?.name||'').trim();
        const readyIndex=(p.readyDestinations||[]).findIndex(name=>String(name)===currentName);
        const alReady=alist.some(item=>String(item.name)===currentName);
        active.textContent=`ACTIVE ${currentName||'—'} — ${readyIndex>=0?'HD READY':'HD ACTIVE/FALLBACK'} / ALDN ${alReady?'✓':'NO'}`;
        diag.classList.toggle('gv-hide',Boolean(api.randomGalaxy?.getState?.().hdOpen));
    };
    render();const timer=setInterval(render,250);window.addEventListener('beforeunload',()=>clearInterval(timer),{once:true});
})().catch(error=>{
    console.error('GALAXY VIEWER 10AE6 BOOTSTRAP FAILURE:',error);
    const box=document.getElementById('gv-ae6-bootstrap')||document.body.appendChild(document.createElement('div'));box.id='gv-ae6-bootstrap';Object.assign(box.style,{position:'fixed',inset:'0',zIndex:'2147483647',padding:'24px',boxSizing:'border-box',background:'#000',color:'#FFD166',whiteSpace:'pre-wrap',font:'14px/1.45 monospace'});box.textContent='GALAXY VIEWER 10AE6 FAILED TO LOAD\n\n'+String(error?.stack||error);
});
"""))

# GV-beta-0010AE6 staged
