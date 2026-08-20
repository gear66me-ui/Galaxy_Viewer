from IPython.display import HTML, Javascript, display

# GV-beta-0010AE7
# Surgical patch over exact current AE6 runtime behavior.
# Scope: fixed ten-slot HD ownership, same-slot retry, travel continuity, and mirrored ALDN diagnostics.

display(HTML("""
<div id="gv-ae7-bootstrap" style="position:fixed;inset:0;background:#000;z-index:2147483647"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const AE6_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0010AE6.py';
    const replaceOnce=(text,oldText,newText,label)=>{
        const count=text.split(oldText).length-1;
        if(count!==1)throw new Error(`AE7 OUTER PATCH ${label} COUNT ${count}`);
        return text.replace(oldText,newText);
    };
    const replaceBlock=(text,start,end,newBlock,label)=>{
        const a=text.indexOf(start),b=text.indexOf(end,a+start.length);
        if(a<0||b<0)throw new Error(`AE7 OUTER BLOCK ${label} ANCHOR MISSING`);
        return text.slice(0,a)+newBlock+text.slice(b);
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

    const response=await fetch(AE6_URL+'?t='+Date.now(),{cache:'no-store'});
    if(!response.ok)throw new Error('AE7 BASELINE FETCH FAILED HTTP '+response.status);
    let wrapper=await response.text();
    wrapper=wrapper.replaceAll('10AE6','10AE7').replaceAll('gv-ae6-','gv-ae7-').replaceAll('GV-beta-0010AE6','GV-beta-0010AE7');

    const innerPatch=`
    // AE7 fixed-slot ownership. Applied to the already-AE6-patched standalone source.
    source=replaceOnce(source,
        'const hdDownloadStatus=new Map();',
        \`const hdDownloadStatus=new Map();\n    const hdSlots=Array.from({length:HUBBLE_PREFETCH_TARGET},(_,index)=>({slot:index+1,key:'',destination:null,state:'EMPTY',attempt:0,retryAt:0,lastError:'',preparedItem:null}));\n    let lastConsumedSlot=null;\n    const slotForKey=key=>hdSlots.find(slot=>slot.key===key)||null;\n    const emptyHdSlot=()=>hdSlots.find(slot=>!slot.key)||null;\n    const assignHdSlot=destination=>{const key=destinationKey(destination);if(!key)return null;let slot=slotForKey(key);if(slot)return slot;slot=emptyHdSlot();if(!slot)return null;Object.assign(slot,{key,destination,state:'QUEUED',attempt:0,retryAt:0,lastError:'',preparedItem:null});return slot};\n    const clearHdSlot=key=>{const slot=slotForKey(key);if(!slot)return null;const number=slot.slot;Object.assign(slot,{slot:number,key:'',destination:null,state:'EMPTY',attempt:0,retryAt:0,lastError:'',preparedItem:null});return slot};\n    const slotAladinState=slot=>!slot?.key?'EMPTY':aladinPrewarmedKeys.has(slot.key)?'READY':aladinPrewarmActiveKey===slot.key?'LOADING':'QUEUED';\`,
        'FIXED SLOT STATE');

    const ae7Status=\`function setHdStatus(destination,state,sourceKind=''){
        const key=destinationKey(destination);
        if(!key)return;
        const old=hdDownloadStatus.get(key)||{};
        hdDownloadStatus.set(key,{key,name:String(destination?.name||old.name||''),state,sourceKind:sourceKind||old.sourceKind||'',updatedAt:Date.now()});
        const slot=slotForKey(key);
        if(slot){
            slot.destination=destination||slot.destination;
            const normalized=String(state||'').toUpperCase();
            if(normalized==='RETRY-WAIT'){
                if(slot.state!=='RETRY')slot.attempt+=1;
                slot.state='RETRY';slot.retryAt=Number(prefetchRetryAfter.get(key)||0);slot.lastError='HD PRELOAD FAILED';
            }else if(normalized==='READY'){slot.state='READY';slot.retryAt=0;slot.lastError=''}
            else if(normalized==='DECODING')slot.state='DECODING';
            else if(normalized==='DOWNLOADING')slot.state='DOWNLOADING';
            else if(normalized==='QUEUED')slot.state='QUEUED';
            else if(normalized==='SUSPENDED')slot.state='DOWNLOADING';
        }
    }

    \`;
    source=replaceBlock(source,'function setHdStatus(destination,state,sourceKind=\'\'){','function getHubbleDownloadStatus(){',ae7Status,'SLOT STATUS');

    const ae7Suspend=\`function suspendBackgroundWork(){
        // AE7: Random/History travel preserves fixed HD downloads and Aladin prewarm state.
        backgroundWorkSuspended=false;
    }

    \`;
    source=replaceBlock(source,'function suspendBackgroundWork(){','function resumeBackgroundWork(){',ae7Suspend,'TRAVEL CONTINUITY');

    const ae7Choose=\`function choosePrefetchCandidate(){
        const now=Date.now();
        for(const slot of hdSlots){
            if(!slot.key||slot.state!=='RETRY'||now<Number(prefetchRetryAfter.get(slot.key)||slot.retryAt||0))continue;
            if(prefetchLoading.has(slot.key)||prefetchQueued.some(item=>destinationKey(item)===slot.key))continue;
            return slot.destination;
        }
        if(!emptyHdSlot())return null;
        const owned=new Set(hdSlots.map(slot=>slot.key).filter(Boolean));
        if(activePreparedItem?.key)owned.add(activePreparedItem.key);
        if(historyPreparedItem?.key)owned.add(historyPreparedItem.key);
        if(activeTargetKey)owned.add(activeTargetKey);
        let pool=[];
        if(chandraTestOverrideActive&&chandraTestQueue.length)pool=chandraTestQueue.filter(item=>!owned.has(destinationKey(item)));
        if(!pool.length)pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!owned.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
        if(!pool.length)return null;
        return pool[Math.floor(Math.random()*pool.length)];
    }

    \`;
    source=replaceBlock(source,'function choosePrefetchCandidate(){','function chooseAladinAheadCandidates(',ae7Choose,'FIXED SLOT CANDIDATE');

    const ae7Ahead=\`function chooseAladinAheadCandidates(destination,count=2){
        const current=destinationKey(destination);
        return hdSlots.filter(slot=>slot.key&&slot.key!==current&&slot.destination&&!aladinPrewarmedKeys.has(slot.key)).slice(0,count).map(slot=>slot.destination);
    }

    \`;
    source=replaceBlock(source,'function chooseAladinAheadCandidates(destination,count=2){','function inFlightDestination(',ae7Ahead,'ALADIN SLOT MIRROR');

    const ae7Enqueue=\`function enqueuePrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key)return false;
        let slot=slotForKey(key);
        if(!slot){slot=assignHdSlot(destination);if(!slot)return false}
        const queuedIndex=prefetchQueued.findIndex(item=>destinationKey(item)===key);
        if(queuedIndex>=0){
            if(priority&&queuedIndex>0){const [queued]=prefetchQueued.splice(queuedIndex,1);prefetchQueued.unshift(queued)}
            return false;
        }
        if(Date.now()<Number(prefetchRetryAfter.get(key)||0)){slot.state='RETRY';slot.retryAt=Number(prefetchRetryAfter.get(key)||0);scheduleRetryFill();return false}
        slot.state='QUEUED';setHdStatus(destination,'QUEUED');
        if(priority)prefetchQueued.unshift(destination);else prefetchQueued.push(destination);
        return true;
    }

    \`;
    source=replaceBlock(source,'function enqueuePrefetch(destination,priority=false){','function scheduleAladinEnhancement(',ae7Enqueue,'SLOT ENQUEUE');

    const ae7Consume=\`function consumeReady(destination=null,excludeName=''){
        const requestedKey=destination?destinationKey(destination):'';
        if(requestedKey&&activePreparedItem?.key===requestedKey)return destinationWithPrepared(activePreparedItem);
        if(requestedKey&&historyPreparedItem?.key===requestedKey){
            const item=historyPreparedItem;
            historyPreparedItem=activePreparedItem;
            activePreparedItem=item;
            activeTargetKey=item.key;
            if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
            return destinationWithPrepared(item);
        }
        let index=-1;
        if(destination)index=prefetchReady.findIndex(item=>item.key===requestedKey);
        else{
            const excluded=String(excludeName||'').trim().toLowerCase();
            index=prefetchReady.findIndex(item=>item.destination.name.toLowerCase()!==excluded);
        }
        if(index<0)return null;
        const [item]=prefetchReady.splice(index,1);
        const ownedSlot=slotForKey(item.key);
        if(ownedSlot)lastConsumedSlot={slot:ownedSlot.slot,key:item.key,name:item.destination?.name||'',provider:item.destination?.provider||'HUBBLE',aladinReady:aladinPrewarmedKeys.has(item.key)};
        clearHdSlot(item.key);
        setPreparedActive(item);
        queueMicrotask(fillPrefetchQueue);
        return destinationWithPrepared(item);
    }

    \`;
    source=replaceBlock(source,'function consumeReady(destination=null,excludeName=\'\'){','async function waitForPreparedKey(',ae7Consume,'SLOT CONSUMPTION');

    const ae7Api=\`function getHdSlots(){
        return Object.freeze(hdSlots.map(slot=>Object.freeze({slot:slot.slot,key:slot.key,provider:String(slot.destination?.provider||''),name:String(slot.destination?.name||''),state:slot.state,attempt:slot.attempt,retryAt:slot.retryAt,ready:slot.state==='READY',active:false,aladinState:slotAladinState(slot)})));
    }
    function getAladinSlots(){
        return Object.freeze(hdSlots.map(slot=>Object.freeze({slot:slot.slot,key:slot.key,name:String(slot.destination?.name||''),state:slotAladinState(slot),ready:Boolean(slot.key&&aladinPrewarmedKeys.has(slot.key)),active:Boolean(slot.key&&aladinPrewarmActiveKey===slot.key)})));
    }
    function getActiveSlotInfo(){return Object.freeze(lastConsumedSlot?{...lastConsumedSlot}:{});}

    \`;
    source=replaceOnce(source,'window.GV10E=Object.freeze({version:VERSION,',ae7Api+'window.GV10E=Object.freeze({version:VERSION,','SLOT API INSERT');
    source=replaceOnce(source,'getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,startHubblePrefetch:', 'getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,getHdSlots,getAladinSlots,getActiveSlotInfo,startHubblePrefetch:','SLOT API EXPORT');

    source=source.replaceAll('10AE2','10AE7');`;

    wrapper=replaceOnce(wrapper,"    source=source.replaceAll('10AE2','10AE7');",innerPatch,'INNER AE7 PATCH');

    const newRender="    const render=()=>{\n"+
        "        const hs=api.getHdSlots?.()||[];\n"+
        "        const as=api.getAladinSlots?.()||[];\n"+
        "        const hrows=[...hd.querySelectorAll('.gv-ae7-row')];\n"+
        "        hrows.forEach((row,i)=>{const item=hs[i]||{};const state=String(item.state||'EMPTY').toUpperCase();row.querySelector('.gv-ae7-name').textContent=item.key?(item.name+' '+(state==='READY'?'✓':state)):'EMPTY';row.classList.toggle('gv-ae7-fail',state==='RETRY');const pct=state==='READY'?100:state==='DECODING'?82:state==='DOWNLOADING'?48:state==='QUEUED'?14:state==='RETRY'?8:0;row.querySelector('.gv-ae7-fill').style.width=pct+'%'});\n"+
        "        const arows=[...aldn.querySelectorAll('.gv-ae7-row')];\n"+
        "        arows.forEach((row,i)=>{const item=as[i]||{};row.querySelector('.gv-ae7-name').textContent=item.key?(item.name+' '+(item.ready?'✓':item.state)):'EMPTY'});\n"+
        "        const current=api.randomGalaxy?.getState?.().activeDestination||api.randomGalaxy?.activeDestination||null;\n"+
        "        const info=api.getActiveSlotInfo?.()||{};\n"+
        "        active.textContent='ACTIVE '+String(current?.name||'—')+' — '+(info.slot?('FROM SLOT '+info.slot):'FALLBACK')+' / HD '+(info.slot?'READY':'NO READY SLOT')+' / ALDN '+(info.aladinReady?'READY':'NO');\n"+
        "        diag.classList.toggle('gv-hide',Boolean(api.randomGalaxy?.getState?.().hdOpen));\n"+
        "    };\n";
    wrapper=replaceBlock(wrapper,'    const render=()=>{','    render();const timer=',newRender,'STABLE DIAGNOSTIC RENDER');

    const htmlMatch=wrapper.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/);
    const jsMatches=[...wrapper.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(!htmlMatch||!jsMatches.length)throw new Error('AE7 WRAPPER EXTRACTION FAILED');
    document.getElementById('gv-ae7-bootstrap')?.remove();
    mountHtml(htmlMatch[1]);
    for(const match of jsMatches){const script=document.createElement('script');script.textContent=match[1];document.body.appendChild(script)}
})().catch(error=>{
    console.error('GALAXY VIEWER 10AE7 BOOTSTRAP FAILURE:',error);
    const box=document.getElementById('gv-ae7-bootstrap')||document.body.appendChild(document.createElement('div'));
    box.id='gv-ae7-bootstrap';Object.assign(box.style,{position:'fixed',inset:'0',zIndex:2147483647,padding:'24px',boxSizing:'border-box',background:'#000',color:'#FFD166',whiteSpace:'pre-wrap',font:'14px/1.45 monospace'});box.textContent='GALAXY VIEWER 10AE7 FAILED TO LOAD\n\n'+String(error?.stack||error);
});
"""))

# GV-beta-0010AE7 staged
