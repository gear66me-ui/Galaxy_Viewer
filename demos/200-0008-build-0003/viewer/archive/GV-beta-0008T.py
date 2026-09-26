from IPython.display import HTML, Javascript, display

# GV-beta-0008O
# Derived from exact GV-beta-0008N baseline blob 0daf4b606c44ff98884ef9bb16f2a8b296e0ea7d.
# Authorized 8O changes: restore the prior centered/lower WE ARE HERE leader presentation,
# bold mirrored reference-style history chevrons, fixed two-decimal MLY-only travel display, and 0012 module identity.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
@font-face{
    font-family:"Space Age";
    src:url("https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001") format("opentype");
    font-style:normal;font-weight:400;font-display:block;
}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{position:relative!important;width:100%!important;height:100vh!important;height:100svh!important;height:100dvh!important;min-height:100vh!important;min-height:100svh!important;min-height:100dvh!important;overflow:hidden!important;background:#000!important}
#aladin-cosmic-command-test .aladin-logo,
#aladin-cosmic-command-test .aladin-copyright,
#aladin-cosmic-command-test .aladin-fov,
#aladin-cosmic-command-test .aladin-status-bar{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#aladin-cosmic-command-test [class*="simbadPointer"]{position:absolute!important;left:-10000px!important;top:-10000px!important;width:1px!important;height:1px!important;min-width:1px!important;min-height:1px!important;max-width:1px!important;max-height:1px!important;margin:0!important;padding:0!important;opacity:0!important;visibility:hidden!important;pointer-events:none!important;overflow:hidden!important}
#gv-hamburger-host{position:absolute;inset:0;z-index:7200;pointer-events:none}
#gv-hamburger-host>.gv-hamburger-module-root{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;min-height:0!important;pointer-events:none!important}
#gv-hamburger-host .gv-menu-proxy{pointer-events:auto!important}
#gv-hamburger-host .gv-viewer-menu.gv-open,#gv-hamburger-host .gv-projection-submenu.gv-open{pointer-events:auto!important}
#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}
#gv-target-host{position:absolute;left:342px;top:12px;z-index:7210;width:36px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}
#gv-random-galaxy-host{position:absolute;inset:0;z-index:7300;pointer-events:none}
#gv-center-reticle{position:absolute;left:50%;top:50%;z-index:7050;width:32px;height:32px;transform:translate(-50%,-50%);pointer-events:none;user-select:none;-webkit-user-select:none}
#gv-center-reticle img{display:block;width:32px;height:32px}
#gv-galaxy-nav{position:absolute;left:50%;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;gap:5px;height:36px;transform:translateX(-50%);pointer-events:auto}
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:#E8FFF0;font:400 11px/1 "Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 4px rgba(229,255,239,.76);box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
#gv-random-galaxy:active{filter:brightness(1.08)}
.gv-galaxy-history{appearance:none;-webkit-appearance:none;position:relative;display:flex;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:transparent;box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;overflow:hidden;pointer-events:auto}
.gv-galaxy-history::before,.gv-galaxy-history::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;pointer-events:none;box-sizing:border-box}
.gv-galaxy-history::before{border-width:6px;border-color:#78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.90));transform:translate(-62%,-50%) rotate(45deg)}
.gv-galaxy-history::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-66%,-50%) rotate(45deg)}
.gv-galaxy-history-back::before{transform:translate(-38%,-50%) rotate(-135deg)}
.gv-galaxy-history-back::after{transform:translate(-34%,-50%) rotate(-135deg)}
.gv-galaxy-history:disabled{opacity:.62;cursor:default;box-shadow:inset 0 0 7px rgba(167,255,203,.18),0 0 6px rgba(77,255,143,.24)}
#gv-travel-hud{position:absolute;left:50%;top:66px;z-index:7350;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:4px;width:min(214px,68vw);padding:0;border:0;background:transparent;box-shadow:none;text-align:center;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-travel-hud.gv-visible{opacity:1;visibility:visible}
#gv-travel-primary{width:100%;padding:4px 7px 5px;border:1px solid rgba(131,255,176,.76);border-radius:6px;background:rgba(0,16,10,.72);box-shadow:0 0 8px rgba(65,255,133,.14);text-align:center}
#gv-travel-course,#gv-travel-heading{font:400 13px/1.05 "Space Age",sans-serif;letter-spacing:.55px;color:#E1FFEC;text-align:center;text-shadow:0 0 4px rgba(87,255,147,.20)}
#gv-travel-course{font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#78FFAB;text-shadow:0 0 7px rgba(87,255,147,.58)}
#gv-travel-heading{margin-top:1px;color:#AEEFC5}
#gv-travel-destination{margin-top:2px;font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#78FFAB;text-shadow:0 0 7px rgba(87,255,147,.58);text-align:center;white-space:normal;overflow-wrap:anywhere}
#gv-travel-distance{box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;width:172px;height:34px;padding:2px 6px 1px;border:1px solid rgba(131,255,176,.78);border-radius:5px;background:rgba(0,12,8,.76);color:#FFFFFF;text-align:center;text-shadow:0 0 4px rgba(205,255,224,.20);white-space:nowrap}
#gv-travel-distance-value{display:block;width:100%;height:18px;font:400 17px/18px "Space Age",sans-serif;letter-spacing:.32px;text-align:center;font-variant-numeric:tabular-nums}
#gv-travel-distance-unit{display:block;width:100%;height:12px;font:400 10.5px/12px "Space Age",sans-serif;letter-spacing:.45px;text-align:center;white-space:nowrap}
#gv-version-label{position:absolute;left:12px;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;min-width:36px;height:30px;margin:0;padding:0 8px;border:1px solid #D7F4FF;border-radius:5px;background:rgba(0,0,0,.84);color:#62D8FF;font:400 12px/1 "Space Age",sans-serif;letter-spacing:.2px;text-transform:uppercase;text-shadow:0 0 7px rgba(98,216,255,.65);box-shadow:0 0 9px rgba(98,216,255,.35);pointer-events:none}
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 16px);bottom:34%;width:1px;min-height:36px;transform:translateX(-50%);background:rgba(120,255,171,.88);box-shadow:0 0 8px rgba(87,255,147,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:66%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(120,255,171,.88);border-radius:6px;background:rgba(0,12,8,.74);color:#E8FFF0;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(87,255,147,.58);box-shadow:0 0 10px rgba(87,255,147,.24)}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#78FFAB;font:400 15px/1.2 "Space Age",sans-serif;letter-spacing:1.25px}
#gv-we-are-here .gv-earth-icon{display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:drop-shadow(0 0 5px rgba(87,255,147,.55))}
#gv-we-are-here .gv-home-sub{margin-top:4px;color:#CFFFE0;font:400 10px/1.3 "Space Age",sans-serif;letter-spacing:1px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#A7DDBA;font:400 9px/1.3 "Space Age",sans-serif;letter-spacing:.8px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
</style>
<div id="aladin-cosmic-command-test"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='8T';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=28d4acb0b724e2c9ec9764f4f3ce92ee1e3210a5';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0003.js?v=34e599fe4e8d3881105b6491c2d9eda9b5c1c17a';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=7b877f841f091f214d844bdc8ae2f933530f4592';
    const RANDOM_GALAXY_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-random-galaxy-0016.js?v=ea62c3923d846b9b06894260ba8cbbeb17876069';
    const HUBBLE_CATALOG_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0001.json?v=060f0abadd103e320c70f035ac93f42d200eda0f';
    const RETICLE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/5274c366f42bb1e764c4b2c4827df0bbba41b4cd/viewer/artwork/GV-reticle-0001.svg?v=fd0f8aa1d5d1f5746e373577c06ae6c81d1f9cc0';
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const ARRIVAL_OCCUPANCY=Object.freeze({target:0.35,max:0.40,minFov:0.05,maxFov:8});
    const HUBBLE_PREFETCH_TARGET=10;
    const TRAVEL_SECONDS=24.075;

    let galaxyCatalog=[];
    let catalogRecordCount=0;
    const prefetchReady=[];
    const prefetchLoading=new Map();
    const prefetchFailedKeys=new Set();
    let prefetchFailedCount=0;
    let activePreparedItem=null;
    let historyPreparedItem=null;
    let activeTargetKey='';
    let forcedDestination=null;
    let pendingHistoryIndex=null;
    let navigationPending=false;
    const galaxyHistory=[];
    let galaxyHistoryIndex=-1;
    let travelHudFrame=0;

    function clamp(value,min,max){return Math.max(min,Math.min(max,Number(value)))}
    function clamp01(value){return clamp(value,0,1)}
    function smootherstep(value){const t=clamp01(value);return t*t*t*(t*(t*6-15)+10)}

    function parseDistanceMly(value){
        if(typeof value==='number'&&Number.isFinite(value)&&value>0)return value;
        const text=String(value??'').trim().toLowerCase().replace(/,/g,'');
        if(!text)return null;
        let match=text.match(/([0-9]+(?:\.[0-9]+)?)\s*(billion|million|thousand)\s+light\s*-?\s*years?/i);
        if(match){
            const number=Number(match[1]);
            if(!Number.isFinite(number)||number<=0)return null;
            if(match[2]==='billion')return number*1000;
            if(match[2]==='million')return number;
            return number/1000;
        }
        match=text.match(/([0-9][0-9\s]*(?:\.[0-9]+)?)\s+light\s*-?\s*years?/i);
        if(!match)return null;
        const lightYears=Number(match[1].replace(/\s+/g,''));
        return Number.isFinite(lightYears)&&lightYears>0?lightYears/1_000_000:null;
    }

    function parseFieldOfViewDegrees(value){
        const text=String(value??'').trim().toLowerCase();
        if(!text)return null;
        const numbers=[...text.matchAll(/[0-9]+(?:\.[0-9]+)?/g)].slice(0,2).map(match=>Number(match[0])).filter(Number.isFinite);
        if(!numbers.length)return null;
        let span=Math.max(...numbers);
        if(/arcsec/.test(text))span/=3600;
        else if(/arcmin/.test(text))span/=60;
        else if(!/(?:degree|\bdeg\b)/.test(text))return null;
        return span>0?span:null;
    }

    function extractDesignation(candidate){
        const texts=[candidate?.name,candidate?.title].map(value=>String(value||'').trim()).filter(Boolean);
        for(const text of texts){
            const match=text.match(/\b(?:M|NGC|IC|UGC|PGC)\s*[- ]?\s*\d+[A-Z]?\b/i);
            if(match)return match[0].replace(/\s+/g,' ').toUpperCase();
        }
        return '';
    }

    function normalizeCatalogGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.title||candidate.name||'').trim();
        const age=String(candidate.age??candidate.ageEstimate??candidate.age_estimate??'').trim();
        const ageYears=Number(candidate.ageYears??candidate.age_years);
        const sizeRaw=candidate.physicalSizeLy??candidate.physical_size_ly??null;
        const physicalSizeLy=Array.isArray(sizeRaw)?sizeRaw.map(Number):Number(sizeRaw);
        const fieldDegrees=parseFieldOfViewDegrees(candidate.fieldOfView);
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const hdUrl=String(candidate.selectedImageUrl||'').trim();
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation||!Number.isFinite(fieldDegrees)||fieldDegrees<=0)return null;
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){return null}
        const approvedHost=host=>host==='esahubble.org'||host.endsWith('.esahubble.org');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        const fov=clamp(fieldDegrees/ARRIVAL_OCCUPANCY.target,ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov);
        return Object.freeze({
            source:'ESA/HUBBLE GALAXIES CATALOG FULL-0001',
            hubble:true,
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy:Array.isArray(physicalSizeLy)?physicalSizeLy.filter(value=>Number.isFinite(value)&&value>0):Number.isFinite(physicalSizeLy)&&physicalSizeLy>0?physicalSizeLy:null,
            fov,hdUrl:hd.href,sourceUrl:source.href,
            credit:String(candidate.credit||'ESA/Hubble').trim()||'ESA/Hubble',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'Hubble Space Telescope',
            githubImageUrl:String(candidate.githubImageUrl||'').trim(),sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    async function loadGalaxyCatalog(){
        const response=await fetch(HUBBLE_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL HUBBLE CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(!Array.isArray(raw)||raw.length!==1879||declared!==1879)throw new Error('FULL HUBBLE CATALOG MUST CONTAIN EXACTLY 1879 ENTRIES');
        catalogRecordCount=raw.length;
        const eligible=raw.map(normalizeCatalogGalaxy).filter(Boolean);
        if(eligible.length<HUBBLE_PREFETCH_TARGET)throw new Error('FULL HUBBLE CATALOG HAS FEWER THAN TEN TRUTHFULLY TARGETABLE GALAXIES');
        return Object.freeze(eligible);
    }

    function destinationKey(destination){return String(destination?.archiveId||destination?.name||'').trim().toLowerCase()}
    function chooseGalaxy(catalog,excludeName=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        const available=catalog.filter(item=>item.name.toLowerCase()!==excluded&&destinationKey(item)!==activeTargetKey);
        const pool=available.length?available:catalog;
        return pool[Math.floor(Math.random()*pool.length)];
    }

    function releasePreparedItem(item){
        if(!item)return;
        try{if(item.image)item.image.src=''}catch(_){}
        try{if(item.objectUrl)URL.revokeObjectURL(item.objectUrl)}catch(_){}
    }

    async function decodePreparedBlob(blob){
        const objectUrl=URL.createObjectURL(blob);
        const image=new Image();
        image.decoding='async';
        image.loading='eager';
        image.src=objectUrl;
        try{
            if(image.decode){
                try{await image.decode()}catch(_){
                    if(!(image.complete&&image.naturalWidth))await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HUBBLE HD PRELOAD FAILED')),{once:true})});
                }
            }else if(!(image.complete&&image.naturalWidth)){
                await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HUBBLE HD PRELOAD FAILED')),{once:true})});
            }
            if(!image.naturalWidth||!image.naturalHeight)throw new Error('HUBBLE HD PRELOAD DECODED WITHOUT IMAGE DIMENSIONS');
            return {image,objectUrl};
        }catch(error){
            image.src='';
            URL.revokeObjectURL(objectUrl);
            throw error;
        }
    }

    async function prepareHdDestination(destination){
        const sources=[];
        const github=String(destination.githubImageUrl||'').trim();
        const esa=String(destination.hdUrl||'').trim();
        if(github)sources.push({url:github,kind:'GITHUB'});
        if(esa&&!sources.some(item=>item.url===esa))sources.push({url:esa,kind:'ESA'});
        let lastError=null;
        for(const source of sources){
            try{
                const response=await fetch(source.url,{cache:'force-cache'});
                if(!response.ok)throw new Error('HUBBLE HD PRELOAD RETURNED HTTP '+response.status);
                const blob=await response.blob();
                const prepared=await decodePreparedBlob(blob);
                return {key:destinationKey(destination),destination,image:prepared.image,objectUrl:prepared.objectUrl,sourceUrl:source.url,sourceKind:source.kind};
            }catch(error){lastError=error}
        }
        throw lastError||new Error('HUBBLE HD PRELOAD HAS NO USABLE SOURCE');
    }

    function blockedPrefetchKeys(){
        const keys=new Set(prefetchReady.map(item=>item.key));
        for(const key of prefetchLoading.keys())keys.add(key);
        if(activePreparedItem?.key)keys.add(activePreparedItem.key);
        if(historyPreparedItem?.key)keys.add(historyPreparedItem.key);
        if(activeTargetKey)keys.add(activeTargetKey);
        return keys;
    }

    function choosePrefetchCandidate(){
        const blocked=blockedPrefetchKeys();
        const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&!prefetchFailedKeys.has(key)});
        return pool.length?pool[Math.floor(Math.random()*pool.length)]:null;
    }

    function startPrefetch(destination){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key||prefetchFailedKeys.has(key))return;
        const promise=prepareHdDestination(destination).then(item=>{
            if(key===activeTargetKey&&!activePreparedItem){
                activePreparedItem=item;
                window.__gv8tRandomGalaxy?.setPreparedHdResource?.(key,item.objectUrl,item.sourceKind,item.image);
                return;
            }
            if(prefetchReady.length<HUBBLE_PREFETCH_TARGET)prefetchReady.push(item);else releasePreparedItem(item);
        }).catch(()=>{prefetchFailedCount++;prefetchFailedKeys.add(key)}).finally(()=>{
            prefetchLoading.delete(key);
            queueMicrotask(fillPrefetchQueue);
        });
        prefetchLoading.set(key,promise);
    }

    function fillPrefetchQueue(){
        while(prefetchReady.length+prefetchLoading.size<HUBBLE_PREFETCH_TARGET){
            const candidate=choosePrefetchCandidate();
            if(!candidate)break;
            startPrefetch(candidate);
        }
    }

    function destinationWithPrepared(item){
        return {...item.destination,preparedHdUrl:item.objectUrl,preparedSource:item.sourceKind,preparedHdImage:item.image};
    }

    function setPreparedActive(item){
        if(activePreparedItem&&activePreparedItem!==item&&activePreparedItem.key!==item.key){
            releasePreparedItem(historyPreparedItem);
            historyPreparedItem=activePreparedItem;
        }
        activePreparedItem=item;
        activeTargetKey=item.key;
    }

    function setUnpreparedActive(destination){
        const key=destinationKey(destination);
        if(activePreparedItem&&activePreparedItem.key!==key){
            releasePreparedItem(historyPreparedItem);
            historyPreparedItem=activePreparedItem;
        }
        activePreparedItem=null;
        activeTargetKey=key;
        return {...destination,preparedHdUrl:'',preparedSource:'',preparedHdImage:null};
    }

    function consumeReady(destination=null,excludeName=''){
        const requestedKey=destination?destinationKey(destination):'';
        if(requestedKey&&activePreparedItem?.key===requestedKey)return destinationWithPrepared(activePreparedItem);
        if(requestedKey&&historyPreparedItem?.key===requestedKey){
            const item=historyPreparedItem;
            historyPreparedItem=activePreparedItem;
            activePreparedItem=item;
            activeTargetKey=item.key;
            queueMicrotask(fillPrefetchQueue);
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
        setPreparedActive(item);
        queueMicrotask(fillPrefetchQueue);
        return destinationWithPrepared(item);
    }

    function distanceProgress(t){
        const turn=0.46,ninety=0.58,complete=0.68;
        if(t<=turn)return 0.20*smootherstep(t/turn);
        if(t<=ninety)return 0.20+0.70*smootherstep((t-turn)/(ninety-turn));
        if(t<=complete)return 0.90+0.08*smootherstep((t-ninety)/(complete-ninety));
        return 0.98+0.02*smootherstep((t-complete)/(1-complete));
    }

    function routeDistanceMillionLy(source,destination){
        const dA=Number(source?.distance),dB=Number(destination?.distance);
        if(Number.isFinite(dA)&&dA>0&&Number.isFinite(dB)&&dB>0){
            const toVector=(ra,dec)=>{const r=Number(ra)*Math.PI/180,d=Number(dec)*Math.PI/180;return [Math.cos(d)*Math.cos(r),Math.cos(d)*Math.sin(r),Math.sin(d)]};
            const a=toVector(source.ra,source.dec),b=toVector(destination.ra,destination.dec);
            const theta=Math.acos(clamp(a[0]*b[0]+a[1]*b[1]+a[2]*b[2],-1,1));
            return Math.sqrt(Math.max(0,dA*dA+dB*dB-2*dA*dB*Math.cos(theta)));
        }
        return Number.isFinite(dB)&&dB>0?dB:0;
    }

    function formatTravelDistance(millionLy){
        const value=Number.isFinite(Number(millionLy))&&Number(millionLy)>0?Number(millionLy):0;
        if(value>=1000)return {value:(value/1000).toFixed(2),unit:'BILLION LIGHT-YEARS'};
        return {value:value.toFixed(2),unit:'MILLION LIGHT-YEARS'};
    }

    function beginTravelHud(destination){
        const hud=document.getElementById('gv-travel-hud');
        const destinationEl=document.getElementById('gv-travel-destination');
        const distanceValueEl=document.getElementById('gv-travel-distance-value');
        const distanceUnitEl=document.getElementById('gv-travel-distance-unit');
        if(!hud||!destinationEl||!distanceValueEl||!distanceUnitEl)return;
        cancelAnimationFrame(travelHudFrame);
        const state=window.GV8T?.randomGalaxy?.getState?.()||window.__gv8tRandomGalaxy?.getState?.()||{};
        const coords=window.aladin_cosmic_command_test?.getRaDec?.()||[HOME.ra,HOME.dec];
        const source={...(state.currentGalaxy||HOME),ra:Number(coords[0]),dec:Number(coords[1])};
        const total=routeDistanceMillionLy(source,destination);
        destinationEl.textContent=destination.name.toUpperCase();
        const initialDistance=formatTravelDistance(0);
        distanceValueEl.textContent=initialDistance.value;
        distanceUnitEl.textContent=initialDistance.unit;
        hud.classList.add('gv-visible');
        const started=performance.now();
        const frame=now=>{
            const t=Math.min(1,(now-started)/(TRAVEL_SECONDS*1000));
            const shown=formatTravelDistance(total*distanceProgress(t));
            distanceValueEl.textContent=shown.value;
            distanceUnitEl.textContent=shown.unit;
            if(t<1)travelHudFrame=requestAnimationFrame(frame);
        };
        travelHudFrame=requestAnimationFrame(frame);
    }

    function endTravelHud(){
        cancelAnimationFrame(travelHudFrame);
        const hud=document.getElementById('gv-travel-hud');
        if(hud)hud.classList.remove('gv-visible');
    }

    function randomHubbleProvider({excludeName}={}){
        let destination=null;
        if(forcedDestination){
            const requested=forcedDestination;
            forcedDestination=null;
            destination=consumeReady(requested,excludeName);
            if(!destination){
                destination=setUnpreparedActive(requested);
                const key=destinationKey(destination);
                if(!prefetchLoading.has(key)&&!prefetchFailedKeys.has(key))startPrefetch(destination);
            }
        }else{
            destination=consumeReady(null,excludeName);
            if(!destination){
                destination=setUnpreparedActive(chooseGalaxy(galaxyCatalog,excludeName));
                const key=destinationKey(destination);
                if(!prefetchLoading.has(key)&&!prefetchFailedKeys.has(key))startPrefetch(destination);
            }
        }
        activeTargetKey=destinationKey(destination);
        beginTravelHud(destination);
        queueMicrotask(fillPrefetchQueue);
        return destination;
    }

    function getHubblePrefetchState(){
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            readyCount:prefetchReady.length,
            loadingCount:prefetchLoading.size,
            failedCount:prefetchFailedCount,
            activePreparedGalaxy:activePreparedItem?.destination?.name||'',
            activePreparedSource:activePreparedItem?.sourceKind||'',
            queuedDestinations:prefetchReady.map(item=>item.destination.name)
        });
    }

    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const existing=[...document.scripts].find(script=>script.src===url||script.dataset[datasetKey]==='true');
            if(existing){
                if(existing.dataset.gvLoaded==='true'){resolve(existing);return}
                existing.addEventListener('load',()=>resolve(existing),{once:true});
                existing.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
                return;
            }
            const script=document.createElement('script');
            script.src=url;
            script.charset='utf-8';
            script.dataset[datasetKey]='true';
            script.addEventListener('load',()=>{script.dataset.gvLoaded='true';resolve(script)},{once:true});
            script.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
            document.head.appendChild(script);
        });
    }

    async function ensureAladin(){
        if(window.A?.init)return window.A;
        await loadScript(ALADIN_URL,'gvAladin382');
        if(!window.A?.init)throw new Error('ALADIN LITE 3.8.2 EXPORT MISSING');
        return window.A;
    }

    function createHost(root,id){
        let host=root.querySelector('#'+id);
        if(!host){host=document.createElement('div');host.id=id;root.appendChild(host)}
        return host;
    }

    function createCenterReticle(root){
        const reticle=document.createElement('div');
        reticle.id='gv-center-reticle';
        reticle.setAttribute('aria-hidden','true');
        const image=document.createElement('img');
        image.src=RETICLE_URL;
        image.alt='';
        image.width=32;
        image.height=32;
        reticle.appendChild(image);
        root.appendChild(reticle);
        return reticle;
    }

    function createBottomControls(root){
        const version=document.createElement('div');
        version.id='gv-version-label';
        version.textContent=VERSION;
        version.setAttribute('aria-label','GALAXY VIEWER VERSION 8T');
        root.appendChild(version);

        const nav=document.createElement('div');
        nav.id='gv-galaxy-nav';
        const back=document.createElement('button');
        back.type='button';back.className='gv-galaxy-history gv-galaxy-history-back';back.textContent='';back.setAttribute('aria-label','PREVIOUS GALAXY');back.disabled=true;
        const random=document.createElement('button');
        random.id='gv-random-galaxy';random.type='button';random.textContent='RANDOM GALAXY';random.setAttribute('aria-label','RANDOM GALAXY');
        const forward=document.createElement('button');
        forward.type='button';forward.className='gv-galaxy-history gv-galaxy-history-forward';forward.textContent='';forward.setAttribute('aria-label','NEXT GALAXY');forward.disabled=true;
        nav.append(back,random,forward);root.appendChild(nav);

        const hud=document.createElement('div');
        hud.id='gv-travel-hud';hud.setAttribute('role','status');hud.setAttribute('aria-live','polite');
        hud.innerHTML='<div id="gv-travel-primary"><div id="gv-travel-course">COURSE LOCKED</div><div id="gv-travel-heading">HEADING TO</div><div id="gv-travel-destination"></div></div><div id="gv-travel-distance"><span id="gv-travel-distance-value">0.00</span><span id="gv-travel-distance-unit">MILLION LIGHT-YEARS</span></div>';
        root.appendChild(hud);
        return {version,nav,back,random,forward,hud};
    }

    function createHomeOverlay(root){
        const overlay=document.createElement('div');
        overlay.id='gv-we-are-here';
        overlay.setAttribute('aria-live','polite');
        overlay.innerHTML='<div class="gv-home-leader" aria-hidden="true"></div><div class="gv-home-label"><div class="gv-home-origin"><span class="gv-earth-icon" aria-hidden="true">🌎</span><strong>WE ARE HERE</strong></div><div class="gv-home-sub">EARTH — MILKY WAY</div><div class="gv-home-hint">TAP RANDOM GALAXY TO BEGIN</div></div>';
        root.appendChild(overlay);
        return overlay;
    }

    function equatorialToGalactic(raDeg,decDeg){
        const d=Math.PI/180,ra=raDeg*d,dec=decDeg*d;
        const raNGP=192.85948*d,decNGP=27.12825*d,lOmega=32.93192*d;
        const b=Math.asin(Math.sin(dec)*Math.sin(decNGP)+Math.cos(dec)*Math.cos(decNGP)*Math.cos(ra-raNGP));
        const y=Math.sin(dec)*Math.cos(decNGP)-Math.cos(dec)*Math.sin(decNGP)*Math.cos(ra-raNGP);
        const x=Math.cos(dec)*Math.sin(ra-raNGP);
        let l=(Math.atan2(y,x)+lOmega)/d;
        l=((l%360)+360)%360;
        return [l,b/d];
    }

    function readCurrentRaDec(aladin,root){
        try{
            const value=aladin.getRaDec?.();
            const ra=Number(value?.[0]),dec=Number(value?.[1]);
            if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
        }catch(error){console.warn('GV-8K GETRADEC WARNING',error)}
        try{
            const canvas=root.querySelector('canvas');
            if(canvas&&typeof aladin.pix2world==='function'){
                const value=aladin.pix2world(canvas.clientWidth/2,canvas.clientHeight/2);
                const ra=Number(value?.[0]),dec=Number(value?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
            }
        }catch(error){console.warn('GV-8K PIX2WORLD WARNING',error)}
        return null;
    }


    const galaxyCatalogPromise=loadGalaxyCatalog();

    const A=await ensureAladin();
    await A.init;
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('GALAXY VIEWER ROOT MISSING');

    const aladin=A.aladin('#aladin-cosmic-command-test',{
        target:`${HOME.ra} ${HOME.dec}`,
        survey:'P/DSS2/color',
        fov:1.5,
        projection:'MOL',
        showReticle:false,
        showZoomControl:false,
        showFullscreenControl:false,
        showLayersControl:false,
        showGotoControl:false,
        showCooGridControl:false,
        showSettingsControl:false,
        showSelectionModeControl:false,
        showColorPickerControl:false,
        showShareControl:false,
        showSimbadPointerControl:true,
        showProjectionControl:false,
        showStatusBar:false,
        showFrame:false,
        showFov:false,
        showCooLocation:false,
        showContextMenu:false,
        showCatalog:false,
        showCooGrid:false
    });
    window.aladin_cosmic_command_test=aladin;

    const hamburgerHost=createHost(root,'gv-hamburger-host');
    const coordinateHost=createHost(root,'gv-coordinate-host');
    const targetHost=createHost(root,'gv-target-host');
    const randomGalaxyHost=createHost(root,'gv-random-galaxy-host');
    const reticle=createCenterReticle(root);
    const bottom=createBottomControls(root);
    const homeOverlay=createHomeOverlay(root);

    galaxyCatalog=await galaxyCatalogPromise;

    await loadScript(HAMBURGER_URL,'gvHamburger0002');
    if(window.GalaxyViewerHamburgerMenu?.version!=='0002')throw new Error('HAMBURGER MODULE 0002 EXPORT MISSING');
    const hamburger=window.GalaxyViewerHamburgerMenu.init({
        host:hamburgerHost,
        onProjectionSelected(name,detail){
            try{
                if(typeof aladin.setProjection!=='function')throw new Error('ALADIN setProjection IS UNAVAILABLE');
                aladin.setProjection(detail.code);
            }catch(error){console.error('GV-8O PROJECTION FAILURE',name,detail?.code,error)}
        }
    });
    hamburger.root.style.position='absolute';
    hamburger.root.style.inset='0';
    hamburger.root.style.width='100%';
    hamburger.root.style.height='100%';
    hamburger.root.style.pointerEvents='none';
    hamburger.menuButton.style.pointerEvents='auto';

    await loadScript(COORDINATE_URL,'gvCoordinate0003');
    if(window.GalaxyCoordinateOverlay?.VERSION!=='0003')throw new Error('COORDINATE MODULE 0003 EXPORT MISSING');
    let frame='ICRSD',latestRa=0,latestDec=0;
    let coordinate=null;
    function renderCoordinates(){
        if(!coordinate)return;
        const shown=frame==='GAL'?equatorialToGalactic(latestRa,latestDec):[latestRa,latestDec];
        coordinate.setFrame(frame);
        coordinate.update(shown[0],shown[1]);
    }
    coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GV-8O FRAME CHANGE WARNING',error)}
        renderCoordinates();
    }});
    await coordinate.ready;
    const initialCoordinates=readCurrentRaDec(aladin,root);
    if(initialCoordinates){latestRa=initialCoordinates[0];latestDec=initialCoordinates[1];renderCoordinates()}
    let lastRa=NaN,lastDec=NaN;
    const coordinateTimer=setInterval(()=>{
        const value=readCurrentRaDec(aladin,root);
        if(!value)return;
        const ra=value[0],dec=value[1];
        if(ra===lastRa&&dec===lastDec)return;
        lastRa=ra;lastDec=dec;latestRa=ra;latestDec=dec;renderCoordinates();
    },100);
    window.addEventListener('beforeunload',()=>clearInterval(coordinateTimer),{once:true});

    await loadScript(TARGET_URL,'gvTarget0001');
    if(window.GalaxyViewerTargetSimbad?.version!=='0001')throw new Error('TARGET / SIMBAD MODULE 0001 EXPORT MISSING');
    const target=window.GalaxyViewerTargetSimbad.init({host:targetHost,aladin,viewerRoot:root});

    await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0016');
    if(window.GalaxyRandomGalaxy?.VERSION!=='0011')throw new Error('RANDOM GALAXY 0016 PATH / 0011 VERIFIED CORE EXPORT MISSING');
    function historySnapshot(destination){
        const {preparedHdUrl,preparedSource,preparedHdImage,...snapshot}=destination||{};
        return Object.freeze({...snapshot});
    }
    function setHistoryControls(){
        const busy=navigationPending||Boolean(window.__gv8tRandomGalaxy?.getState?.().busy);
        bottom.back.disabled=busy||galaxyHistoryIndex<=0;
        bottom.forward.disabled=busy||galaxyHistoryIndex<0||galaxyHistoryIndex>=galaxyHistory.length-1;
    }
    function recordArrival(destination){
        if(Number.isInteger(pendingHistoryIndex)){
            galaxyHistoryIndex=pendingHistoryIndex;
            pendingHistoryIndex=null;
        }else{
            if(galaxyHistoryIndex<galaxyHistory.length-1)galaxyHistory.splice(galaxyHistoryIndex+1);
            galaxyHistory.push(historySnapshot(destination));
            galaxyHistoryIndex=galaxyHistory.length-1;
        }
    }
    function navigateHistory(index){
        if(index<0||index>=galaxyHistory.length||navigationPending||randomGalaxy.getState().busy)return;
        forcedDestination=galaxyHistory[index];
        pendingHistoryIndex=index;
        navigationPending=true;
        homeOverlay.classList.add('gv-hidden');setHistoryControls();
        randomGalaxy.travelToRandom().catch(error=>{
            forcedDestination=null;pendingHistoryIndex=null;navigationPending=false;endTravelHud();setHistoryControls();console.error('GV-8O HISTORY NAVIGATION FAILURE',error);
        });
    }

    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{
        aladin,
        randomButton:bottom.random,
        bindClick:true,
        prefetch:false,
        hubbleProvider:randomHubbleProvider,
        currentGalaxy:HOME,
        catalogCount:catalogRecordCount,
        onArrival(destination){
            navigationPending=false;
            endTravelHud();
            recordArrival(destination);
            setHistoryControls();
        },
        onError(error){
            navigationPending=false;pendingHistoryIndex=null;forcedDestination=null;endTravelHud();setHistoryControls();console.error('GV-8O RANDOM GALAXY FAILURE',error);
        }
    });
    window.__gv8tRandomGalaxy=randomGalaxy;
    await randomGalaxy.ready;
    window.addEventListener('beforeunload',()=>{releasePreparedItem(activePreparedItem);releasePreparedItem(historyPreparedItem);prefetchReady.splice(0).forEach(releasePreparedItem)},{once:true});
    bottom.random.addEventListener('click',()=>{pendingHistoryIndex=null;navigationPending=true;homeOverlay.classList.add('gv-hidden');setHistoryControls()});
    bottom.back.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex-1));
    bottom.forward.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex+1));
    setHistoryControls();
    window.GV8T=Object.freeze({version:VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,homeOverlay,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,getHubblePrefetchState,startHubblePrefetch:fillPrefetchQueue,getGalaxyHistory:()=>({index:galaxyHistoryIndex,items:galaxyHistory.map(item=>({name:item.name,archiveId:item.archiveId}))})});
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length}}));
})().catch(error=>console.error('GALAXY VIEWER 8O STARTUP FAILURE:',error));
"""))

# GV-beta-0008O staged