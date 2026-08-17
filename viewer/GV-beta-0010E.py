from IPython.display import HTML, Javascript, display

# GV-beta-0010E
# Derived from exact repaired GV-beta-0009H baseline blob 6e29dd296343dc43e086b619872ad1ece1e8b833.
# Authorized 10E-A change: JSON 0002 preserved; Hubble HD starts first while isolated Aladin prewarms the current and two future destinations; next HD prefers a prewarmed target; navigation suspension/resume preserved; retryable no-timeout HD preload preserved; visible revision label VERSION 10E-A.
# Repaired 9H Hubble instant-open behavior and all unrelated behavior remain frozen.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
@font-face{
    font-family:"Space Age";
    src:url("https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001") format("opentype");
    font-style:normal;font-weight:400;font-display:block
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
#gv-galaxy-nav{position:absolute;left:50%;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;gap:5px;width:calc(100vw - 24px);height:36px;transform:translateX(-50%);pointer-events:auto}
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:#E8FFF0;font:400 11px/1 "Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 4px rgba(229,255,239,.76);box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
#gv-random-galaxy:active{filter:brightness(1.08)}
.gv-galaxy-history{appearance:none;-webkit-appearance:none;position:relative;display:flex;flex:0 0 36px;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:transparent;box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;overflow:hidden;pointer-events:auto}
.gv-galaxy-history::before,.gv-galaxy-history::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;pointer-events:none;box-sizing:border-box}
.gv-galaxy-history::before{border-width:6px;border-color:#78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.90));transform:translate(-62%,-50%) rotate(45deg)}
.gv-galaxy-history::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-66%,-50%) rotate(45deg)}
.gv-galaxy-history-back::before{transform:translate(-38%,-50%) rotate(-135deg)}
.gv-galaxy-history-back::after{transform:translate(-34%,-50%) rotate(-135deg)}
.gv-galaxy-history:disabled{opacity:.62;cursor:default;box-shadow:inset 0 0 7px rgba(167,255,203,.18),0 0 6px rgba(77,255,143,.24)}
#gv-travel-hud{position:absolute;left:50%;top:auto;bottom:64px;z-index:7350;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:4px;width:min(214px,68vw);padding:0;border:0;background:transparent;box-shadow:none;text-align:center;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-travel-hud.gv-visible{opacity:1;visibility:visible}
#gv-travel-primary{box-sizing:border-box;width:calc(100vw - 24px);padding:4px 7px 5px;border:1px solid rgba(131,255,176,.76);border-radius:6px;background:rgba(0,16,10,.72);box-shadow:0 0 8px rgba(65,255,133,.14);text-align:center}
#gv-travel-course,#gv-travel-heading{font:400 13px/1.05 "Space Age",sans-serif;letter-spacing:.55px;color:#E1FFEC;text-align:center;text-shadow:0 0 4px rgba(87,255,147,.20)}
#gv-travel-course{font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#78FFAB;text-shadow:0 0 7px rgba(87,255,147,.58)}
#gv-travel-heading{margin-top:1px;color:#AEEFC5}
#gv-travel-destination{margin-top:2px;font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#78FFAB;text-shadow:0 0 7px rgba(87,255,147,.58);text-align:center;white-space:normal;overflow-wrap:anywhere}
#gv-travel-distance{box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;width:172px;height:34px;padding:2px 6px 1px;border:1px solid rgba(131,255,176,.78);border-radius:5px;background:rgba(0,12,8,.76);color:#FFD85A;text-align:center;text-shadow:0 0 4px rgba(255,242,168,.82),0 0 9px rgba(255,180,45,.34);white-space:nowrap}
#gv-travel-distance-value{position:relative;display:block;width:100%;height:18px;font:400 17px/18px "Space Age",sans-serif;letter-spacing:.32px;text-align:center;font-variant-numeric:tabular-nums}
#gv-travel-distance-integer{position:absolute;right:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:right;white-space:nowrap}
#gv-travel-distance-decimal{position:absolute;left:50%;top:0;width:6px;height:18px;transform:translateX(-50%);font:inherit;letter-spacing:0;text-align:center;white-space:nowrap}
#gv-travel-distance-fraction{position:absolute;left:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:left;white-space:nowrap}
#gv-travel-distance-unit{display:block;width:100%;height:12px;font:400 10.5px/12px "Space Age",sans-serif;letter-spacing:.45px;text-align:center;white-space:nowrap}
#gv-version-label{position:absolute;left:50%;bottom:51px;z-index:7400;transform:translateX(-50%);height:10px;color:rgba(183,255,208,.86);font:400 8px/10px "Space Age",sans-serif;letter-spacing:.85px;text-align:center;text-transform:uppercase;text-shadow:0 0 5px rgba(87,255,147,.40);white-space:nowrap;pointer-events:none}
#gv-universe-context{position:absolute;left:50%;top:auto;bottom:calc(50% + min(25vw,50dvh) + 8px);z-index:7095;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;width:min(310px,76vw);pointer-events:none;transition:opacity .2s ease}
#gv-universe-context .gv-universe-label{padding:5px 8px 6px;border:1px solid rgba(120,255,171,.78);border-radius:6px;background:rgba(0,12,8,.68);box-shadow:0 0 9px rgba(87,255,147,.18);color:#DFFFEA;text-align:center;text-transform:uppercase;text-shadow:0 0 6px rgba(87,255,147,.42);font:400 9px/1.25 "Space Age",sans-serif;letter-spacing:.65px}
#gv-universe-context .gv-universe-count{display:block;margin-top:2px;color:#78FFAB;font-size:10px;letter-spacing:.8px}
#gv-universe-context .gv-universe-leader{position:relative;width:1px;height:18px;background:rgba(120,255,171,.86);box-shadow:0 0 7px rgba(87,255,147,.48)}
#gv-universe-context .gv-universe-leader::after{content:"";position:absolute;left:50%;bottom:-1px;width:0;height:0;transform:translateX(-50%);border-left:5px solid transparent;border-right:5px solid transparent;border-top:8px solid #78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.68))}
#gv-universe-context.gv-hidden{opacity:0;visibility:hidden}
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 16px);bottom:34%;width:1px;min-height:36px;transform:translateX(-50%);background:rgba(120,255,171,.88);box-shadow:0 0 8px rgba(87,255,147,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:66%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(120,255,171,.88);border-radius:6px;background:rgba(0,12,8,.74);color:#E8FFF0;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(87,255,147,.58);box-shadow:0 0 10px rgba(87,255,147,.24)}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#78FFAB;font:400 15px/1.2 "Space Age",sans-serif;letter-spacing:1.25px}
#gv-we-are-here .gv-earth-icon{display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:drop-shadow(0 0 5px rgba(87,255,147,.55))}
#gv-we-are-here .gv-home-sub{margin-top:4px;color:#CFFFE0;font:400 10px/1.3 "Space Age",sans-serif;letter-spacing:1px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#A7DDBA;font:400 9px/1.3 "Space Age",sans-serif;letter-spacing:.8px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
#gv-apk-cover{flex-direction:column;gap:18px}#gv-apk-cover .gv-10e-version{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}
</style>
<div id="aladin-cosmic-command-test"></div>
<script>(()=>{const cover=document.getElementById('gv-apk-cover');if(!cover)return;const img=cover.querySelector('img');if(img)img.src='artwork/icon.svg';const version=document.createElement('div');version.className='gv-10e-version';version.textContent='VERSION 10E';cover.appendChild(version)})();</script>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='10E';
    const DISPLAY_VERSION='10E';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=28d4acb0b724e2c9ec9764f4f3ce92ee1e3210a5';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0004.js?v=5c323a13b92f146426b45c047fc716b599494f3a';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=7b877f841f091f214d844bdc8ae2f933530f4592';
    const RANDOM_GALAXY_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-random-galaxy-0029.js?v=9fe0ac11b49b0e6629f4135f6d6dafb518ea59f6';
    const HUBBLE_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0017.json?v=e8009928f12dfc4138f215e2144edd16a0974fd4';
    const RETICLE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/5274c366f42bb1e764c4b2c4827df0bbba41b4cd/viewer/artwork/GV-reticle-0001.svg?v=fd0f8aa1d5d1f5746e373577c06ae6c81d1f9cc0';
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const ARRIVAL_OCCUPANCY=Object.freeze({target:0.35,max:0.40,minFov:0.05,maxFov:8});
    const HUBBLE_PREFETCH_TARGET=10;
    const ALADIN_PREWARM_DWELL_MS=1400;
    const PREFETCH_RETRY_MS=5000;
    const FRAMING_SAMPLE_SIZE=96;
    const FRAMING_MAX_SHIFT_FRACTION=0.18;
    const TRAVEL_SECONDS=18;

    let galaxyCatalog=[];
    let catalogRecordCount=0;
    const prefetchReady=[];
    const prefetchLoading=new Map();
    const prefetchRetryAfter=new Map();
    const hdDownloadStatus=new Map();
    let prefetchFailedCount=0;
    let prefetchRetryTimer=0;
    let priorityPrefetchDestination=null;
    let activePrefetchAbort=null;
    let activePrefetchKey='';
    let activePreparedItem=null;
    let historyPreparedItem=null;
    let activeTargetKey='';
    let forcedDestination=null;
    let pendingHistoryIndex=null;
    let navigationPending=false;
    let backgroundWorkSuspended=false;
    const galaxyHistory=[];
    let galaxyHistoryIndex=-1;
    let travelHudFrame=0;
    let aladinPrewarm=null;
    let aladinPrewarmHost=null;
    let aladinPrewarmReady=null;
    let aladinPrewarmTimer=0;
    let aladinPrewarmWaitResolve=null;
    let aladinPrewarmActiveKey='';
    let aladinPrewarmLastKey='';
    const aladinPrewarmedKeys=new Set();

    function setHdStatus(destination,state,sourceKind=''){
        const key=destinationKey(destination);
        if(!key)return;
        const old=hdDownloadStatus.get(key)||{};
        hdDownloadStatus.set(key,{key,name:String(destination?.name||old.name||''),state,sourceKind:sourceKind||old.sourceKind||'',updatedAt:Date.now()});
    }

    function getHubbleDownloadStatus(){
        return Object.freeze([...hdDownloadStatus.values()].map(item=>Object.freeze({...item})));
    }

    function suspendBackgroundWork(){
        if(backgroundWorkSuspended)return;
        backgroundWorkSuspended=true;
        if(activePrefetchKey){const active=galaxyCatalog.find(item=>destinationKey(item)===activePrefetchKey);if(active)setHdStatus(active,'SUSPENDED')}
        if(activePrefetchAbort)activePrefetchAbort.abort();
        if(prefetchRetryTimer){clearTimeout(prefetchRetryTimer);prefetchRetryTimer=0}
        if(aladinPrewarmTimer){clearTimeout(aladinPrewarmTimer);aladinPrewarmTimer=0}
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        aladinPrewarmActiveKey='';
        aladinPrewarm=null;
        aladinPrewarmReady=null;
        try{aladinPrewarmHost?.remove()}catch(_){}
        aladinPrewarmHost=null;
    }

    function resumeBackgroundWork(){
        if(!backgroundWorkSuspended)return;
        backgroundWorkSuspended=false;
        const active=galaxyCatalog.find(item=>destinationKey(item)===activeTargetKey);
        const alreadyReady=Boolean(activePreparedItem?.key===activeTargetKey||prefetchReady.some(item=>item.key===activeTargetKey));
        if(active&&!alreadyReady)priorityPrefetchDestination=active;
        queueMicrotask(fillPrefetchQueue);
    }

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
        const explicit=String(candidate?.designation||'').trim();
        const texts=[explicit,candidate?.name,candidate?.title,candidate?.displayName,candidate?.imageType,candidate?.category]
            .map(value=>String(value||'').trim()).filter(Boolean);
        const joined=texts.join(' | ');
        if(/stephan(?:'|’)?s\s+quintet/i.test(joined))return 'HCG 92';
        for(const text of texts){
            let match=text.match(/\bHCG\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bHICKSON(?:\s+COMPACT\s+GROUP)?\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bABELL\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `ABELL ${match[1].toUpperCase()}`;
        }
        if(explicit)return explicit.toUpperCase();
        for(const text of texts){
            const match=text.match(/\b(?:M|NGC|IC|UGC|PGC|ARP|ESO)\s*[- ]?\s*\d+[A-Z]?(?:[- ]?\d+)?\b/i);
            if(match)return match[0].replace(/\s+/g,' ').toUpperCase();
        }
        if(/\b(?:galaxy\s+cluster|cluster\s+of\s+galaxies|galaxies\s+cluster)\b/i.test(joined))return 'GALAXY CLUSTER';
        if(/\b(?:compact\s+group|galaxy\s+group|group\s+of\s+galaxies|quintet|quartet|triplet)\b/i.test(joined))return 'GALAXY GROUP';
        if(/\b(?:galaxy\s+pair|pair\s+of\s+galaxies|interacting\s+galaxies)\b/i.test(joined))return 'GALAXY PAIR';
        if(/\b(?:star\s+cluster|stellar\s+cluster)\b/i.test(joined))return 'STAR CLUSTER';
        if(/\b(?:star\s+field|stellar\s+field)\b/i.test(joined))return 'STAR FIELD';
        if(/\bnebula\b/i.test(joined))return 'NEBULA';
        if(/\bstar\b/i.test(joined)&&!/\bgalax/i.test(joined))return 'STAR';
        return 'GALAXY';
    }

    function normalizeCatalogGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??candidate.ageEstimate??candidate.age_estimate??'').trim();
        const ageGyr=Number(candidate.science?.ageGyr);
        const ageYears=Number.isFinite(ageGyr)&&ageGyr>0?ageGyr*1_000_000_000:Number(candidate.ageYears??candidate.age_years);
        const scienceSize=Array.isArray(candidate.science?.sizeKly)?candidate.science.sizeKly.map(value=>Number(value)*1000):null;
        const sizeRaw=scienceSize??candidate.physicalSizeLy??candidate.physical_size_ly??null;
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
            source:'ESA/HUBBLE GALAXIES CATALOG FULL-0002',
            hubble:true,
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy:Array.isArray(physicalSizeLy)?physicalSizeLy.filter(value=>Number.isFinite(value)&&value>0):Number.isFinite(physicalSizeLy)&&physicalSizeLy>0?physicalSizeLy:null,
            fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,
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

    async function prepareHdDestination(destination,signal=null){
        const sources=[];
        const github=String(destination.githubImageUrl||'').trim();
        const esa=String(destination.hdUrl||'').trim();
        if(github)sources.push({url:github,kind:'GITHUB'});
        if(esa&&!sources.some(item=>item.url===esa))sources.push({url:esa,kind:'ESA'});
        let lastError=null;
        for(const source of sources){
            try{
                setHdStatus(destination,'DOWNLOADING',source.kind);
                const response=await fetch(source.url,{cache:'force-cache',signal});
                if(!response.ok)throw new Error('HUBBLE HD PRELOAD RETURNED HTTP '+response.status);
                const blob=await response.blob();
                if(backgroundWorkSuspended||signal?.aborted)throw new DOMException('HUBBLE HD PRELOAD SUSPENDED','AbortError');
                setHdStatus(destination,'DECODING',source.kind);
                const prepared=await decodePreparedBlob(blob);
                setHdStatus(destination,'READY',source.kind);
                return {key:destinationKey(destination),destination,image:prepared.image,objectUrl:prepared.objectUrl,sourceUrl:source.url,sourceKind:source.kind};
            }catch(error){
                if(error?.name==='AbortError'){setHdStatus(destination,'SUSPENDED',source.kind);throw error}
                lastError=error;
            }
        }
        setHdStatus(destination,'RETRY-WAIT');
        throw lastError||new Error('HUBBLE HD PRELOAD HAS NO USABLE SOURCE');
    }

    function ensureAladinPrewarm(){
        if(backgroundWorkSuspended)return Promise.resolve(null);
        if(aladinPrewarmReady)return aladinPrewarmReady;
        aladinPrewarmReady=new Promise((resolve,reject)=>{
            const frame=document.createElement('iframe');
            aladinPrewarmHost=frame;
            frame.id='gv-aladin-prewarm-frame';
            frame.setAttribute('aria-hidden','true');
            frame.tabIndex=-1;
            Object.assign(frame.style,{position:'fixed',left:'-10000px',top:'0',width:'512px',height:'512px',border:'0',opacity:'0',pointerEvents:'none',overflow:'hidden'});
            frame.srcdoc=`<!doctype html><html><head><link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css"><style>html,body,#gv-prewarm{margin:0;width:512px;height:512px;overflow:hidden;background:#000}</style></head><body><div id="gv-prewarm"></div><script src="${ALADIN_URL}"><\/script></body></html>`;
            frame.addEventListener('load',async()=>{
                try{
                    if(backgroundWorkSuspended){resolve(null);return}
                    const win=frame.contentWindow;
                    if(!win?.A?.init)throw new Error('ISOLATED ALADIN PREWARM EXPORT MISSING');
                    await win.A.init;
                    if(backgroundWorkSuspended){resolve(null);return}
                    aladinPrewarm=win.A.aladin('#gv-prewarm',{
                        target:`${HOME.ra} ${HOME.dec}`,
                        survey:'P/DSS2/color',
                        fov:1,
                        projection:'SIN',
                        cooFrame:'ICRSd',
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
                        showSimbadPointerControl:false,
                        showProjectionControl:false,
                        showStatusBar:false,
                        showFrame:false,
                        showFov:false,
                        showCooLocation:false,
                        showContextMenu:false,
                        showCatalog:false,
                        showCooGrid:false
                    });
                    if(typeof aladinPrewarm.setFrame==='function')aladinPrewarm.setFrame('ICRSd');
                    if(typeof aladinPrewarm.setProjection==='function')aladinPrewarm.setProjection('SIN');
                    resolve(aladinPrewarm);
                }catch(error){reject(error)}
            },{once:true});
            frame.addEventListener('error',()=>reject(new Error('ISOLATED ALADIN PREWARM FRAME FAILED TO LOAD')),{once:true});
            document.body.appendChild(frame);
        }).catch(error=>{
            console.warn('GV-10E ISOLATED ALADIN PREWARM WARNING',error);
            aladinPrewarmReady=null;
            aladinPrewarm=null;
            try{aladinPrewarmHost?.remove()}catch(_){}
            aladinPrewarmHost=null;
            return null;
        });
        return aladinPrewarmReady;
    }

    function abortError(message='BACKGROUND PREPARATION SUSPENDED'){return new DOMException(message,'AbortError')}

    async function prepareAladinDestination(destination,force=false){
        if(backgroundWorkSuspended)throw abortError();
        const key=destinationKey(destination);
        if(!key)return false;
        if(aladinPrewarmedKeys.has(key)&&!force)return true;
        aladinPrewarmActiveKey=key;
        const isolated=await ensureAladinPrewarm();
        if(backgroundWorkSuspended||!isolated){aladinPrewarmActiveKey='';throw abortError()}
        try{
            if(typeof isolated.setFrame==='function')isolated.setFrame('ICRSd');
            if(typeof isolated.setProjection==='function')isolated.setProjection('SIN');
            if(typeof isolated.setRotation==='function'&&Number.isFinite(Number(destination.aladinRotation)))isolated.setRotation(Number(destination.aladinRotation));
            if(typeof isolated.gotoRaDec==='function')isolated.gotoRaDec(destination.ra,destination.dec);
            if(typeof isolated.setFov==='function')isolated.setFov(destination.fov);
        }catch(error){
            aladinPrewarmActiveKey='';
            throw error;
        }
        const completed=await new Promise(resolve=>{
            aladinPrewarmWaitResolve=resolve;
            aladinPrewarmTimer=setTimeout(()=>{
                aladinPrewarmTimer=0;
                if(aladinPrewarmWaitResolve===resolve)aladinPrewarmWaitResolve=null;
                resolve(true);
            },ALADIN_PREWARM_DWELL_MS);
        });
        aladinPrewarmActiveKey='';
        if(!completed||backgroundWorkSuspended)throw abortError();
        aladinPrewarmedKeys.add(key);
        aladinPrewarmLastKey=key;
        return true;
    }

    function imageLightProfile(source){
        if(!source)return null;
        try{
            const canvas=document.createElement('canvas');
            canvas.width=FRAMING_SAMPLE_SIZE;canvas.height=FRAMING_SAMPLE_SIZE;
            const ctx=canvas.getContext('2d',{willReadFrequently:true});
            if(!ctx)return null;
            ctx.filter='blur(2px)';
            ctx.drawImage(source,0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE);
            const data=ctx.getImageData(0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE).data;
            const lum=[];
            for(let i=0;i<data.length;i+=4)lum.push(.2126*data[i]+.7152*data[i+1]+.0722*data[i+2]);
            const sorted=[...lum].sort((a,b)=>a-b);
            const background=sorted[Math.floor(sorted.length*.45)]||0;
            const threshold=sorted[Math.floor(sorted.length*.78)]||background;
            let sum=0,sx=0,sy=0;
            const weights=new Float64Array(lum.length);
            for(let y=0;y<FRAMING_SAMPLE_SIZE;y++)for(let x=0;x<FRAMING_SAMPLE_SIZE;x++){
                const index=y*FRAMING_SAMPLE_SIZE+x;
                const edge=Math.min(x,y,FRAMING_SAMPLE_SIZE-1-x,FRAMING_SAMPLE_SIZE-1-y);
                const edgeFactor=clamp(edge/(FRAMING_SAMPLE_SIZE*.08),0,1);
                const weight=Math.max(0,lum[index]-Math.max(background,threshold*.82))*edgeFactor;
                weights[index]=weight;sum+=weight;sx+=weight*x;sy+=weight*y;
            }
            if(!(sum>1))return null;
            const cx=sx/sum,cy=sy/sum;
            let xx=0,yy=0,xy=0;
            for(let y=0;y<FRAMING_SAMPLE_SIZE;y++)for(let x=0;x<FRAMING_SAMPLE_SIZE;x++){
                const weight=weights[y*FRAMING_SAMPLE_SIZE+x];if(!weight)continue;
                const dx=x-cx,dy=y-cy;xx+=weight*dx*dx;yy+=weight*dy*dy;xy+=weight*dx*dy;
            }
            xx/=sum;yy/=sum;xy/=sum;
            const trace=xx+yy,disc=Math.sqrt(Math.max(0,(xx-yy)*(xx-yy)+4*xy*xy));
            const major=(trace+disc)/2,minor=(trace-disc)/2;
            const eccentricity=major>0?clamp(1-Math.max(0,minor)/major,0,1):0;
            const angle=.5*Math.atan2(2*xy,xx-yy)*180/Math.PI;
            return {x:cx,y:cy,angle,eccentricity,weight:sum};
        }catch(_){return null}
    }

    function normalizeSignedAngle(value){
        let angle=Number(value)||0;
        while(angle>90)angle-=180;
        while(angle<-90)angle+=180;
        return angle;
    }

    function angularSeparationDegrees(ra1,dec1,ra2,dec2){
        const d=Math.PI/180;
        const a1=ra1*d,a2=ra2*d,b1=dec1*d,b2=dec2*d;
        const cosine=Math.sin(b1)*Math.sin(b2)+Math.cos(b1)*Math.cos(b2)*Math.cos(a1-a2);
        return Math.acos(clamp(cosine,-1,1))/d;
    }

    function deriveHubbleFraming(destination,hubbleImage){
        if(!hubbleImage?.naturalWidth||!hubbleImage?.naturalHeight||!aladinPrewarm||!aladinPrewarmHost)return destination;
        try{
            const skyCanvas=aladinPrewarmHost.contentDocument?.querySelector('canvas');
            if(!skyCanvas)return destination;
            const hubble=imageLightProfile(hubbleImage),sky=imageLightProfile(skyCanvas);
            if(!hubble||!sky)return destination;
            const width=skyCanvas.clientWidth||skyCanvas.width||512,height=skyCanvas.clientHeight||skyCanvas.height||512;
            const desiredX=hubble.x/FRAMING_SAMPLE_SIZE*width;
            const desiredY=hubble.y/FRAMING_SAMPLE_SIZE*height;
            const currentX=sky.x/FRAMING_SAMPLE_SIZE*width;
            const currentY=sky.y/FRAMING_SAMPLE_SIZE*height;
            const maxDx=width*FRAMING_MAX_SHIFT_FRACTION,maxDy=height*FRAMING_MAX_SHIFT_FRACTION;
            const sampleX=width/2+clamp(currentX-desiredX,-maxDx,maxDx);
            const sampleY=height/2+clamp(currentY-desiredY,-maxDy,maxDy);
            if(typeof aladinPrewarm.pix2world!=='function')return destination;
            const world=aladinPrewarm.pix2world(sampleX,sampleY);
            const ra=Number(world?.[0]),dec=Number(world?.[1]);
            if(!Number.isFinite(ra)||!Number.isFinite(dec))return destination;
            const maxAngularShift=Math.max(.02,Number(destination.fov)*.30);
            if(angularSeparationDegrees(destination.ra,destination.dec,ra,dec)>maxAngularShift)return destination;
            let rotation=null;
            if(hubble.eccentricity>.22&&sky.eccentricity>.22){
                const delta=normalizeSignedAngle(hubble.angle-sky.angle);
                if(Number.isFinite(delta)&&Math.abs(delta)<=90)rotation=delta;
            }
            return Object.freeze({...destination,ra,dec,aladinRotation:rotation,framingCorrected:true});
        }catch(error){
            console.warn('GV-10E OPTIONAL HUBBLE FRAMING SKIPPED',error);
            return destination;
        }
    }

    function blockedPrefetchKeys(){
        const keys=new Set(prefetchReady.map(item=>item.key));
        for(const key of prefetchLoading.keys())keys.add(key);
        if(priorityPrefetchDestination)keys.add(destinationKey(priorityPrefetchDestination));
        if(activePreparedItem?.key)keys.add(activePreparedItem.key);
        if(historyPreparedItem?.key)keys.add(historyPreparedItem.key);
        if(activeTargetKey)keys.add(activeTargetKey);
        return keys;
    }

    function choosePrefetchCandidate(){
        const blocked=blockedPrefetchKeys(),now=Date.now();
        const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
        if(!pool.length)return null;
        const warmed=pool.filter(item=>aladinPrewarmedKeys.has(destinationKey(item)));
        const preferred=warmed.length?warmed:pool;
        return preferred[Math.floor(Math.random()*preferred.length)];
    }

    function chooseAladinAheadCandidates(destination,count=2){
        const blocked=blockedPrefetchKeys();
        blocked.add(destinationKey(destination));
        const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&!aladinPrewarmedKeys.has(key)});
        const chosen=[];
        while(pool.length&&chosen.length<count){const index=Math.floor(Math.random()*pool.length);chosen.push(pool.splice(index,1)[0])}
        return chosen;
    }

    function inFlightDestination(excludeName=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        for(const key of prefetchLoading.keys()){
            const destination=galaxyCatalog.find(item=>destinationKey(item)===key&&item.name.toLowerCase()!==excluded);
            if(destination)return destination;
        }
        return null;
    }

    function scheduleRetryFill(){
        if(backgroundWorkSuspended||prefetchRetryTimer)return;
        const now=Date.now();
        const waits=[...prefetchRetryAfter.values()].map(value=>Number(value)-now).filter(value=>value>0);
        if(!waits.length)return;
        prefetchRetryTimer=setTimeout(()=>{prefetchRetryTimer=0;fillPrefetchQueue()},Math.max(100,Math.min(...waits)));
    }

    function startPrefetch(destination,priority=false){
        if(backgroundWorkSuspended)return;
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key)return;
        if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return}
        if(prefetchLoading.size){
            if(priority){
                priorityPrefetchDestination=destination;
                if(activePrefetchAbort)activePrefetchAbort.abort();
            }
            return;
        }
        const controller=new AbortController();
        activePrefetchAbort=controller;
        activePrefetchKey=key;
        const promise=(async()=>{
            try{
                setHdStatus(destination,'QUEUED');
                const hdPromise=prepareHdDestination(destination,controller.signal);
                const ahead=chooseAladinAheadCandidates(destination,2);
                const aladinPromise=(async()=>{
                    for(const candidate of [destination,...ahead]){
                        if(backgroundWorkSuspended||controller.signal.aborted)throw abortError();
                        try{await prepareAladinDestination(candidate,priority&&candidate===destination)}catch(error){if(error?.name==='AbortError')throw error;console.warn('GV-10E ALADIN AHEAD PREWARM WARNING',error)}
                    }
                })();
                const item=await hdPromise;
                try{await aladinPromise}catch(error){if(error?.name==='AbortError')throw error}
                let preparedDestination=destination;
                if(!backgroundWorkSuspended&&item.image&&aladinPrewarmLastKey===key){
                    preparedDestination=deriveHubbleFraming(destination,item.image);
                    if(preparedDestination!==destination&&preparedDestination.framingCorrected){
                        try{await prepareAladinDestination(preparedDestination,true)}catch(error){if(error?.name==='AbortError')throw error;preparedDestination=destination}
                    }
                }
                item.destination=preparedDestination;
                prefetchRetryAfter.delete(key);
                if(backgroundWorkSuspended){releasePreparedItem(item);throw abortError()}
                if(key===activeTargetKey&&!activePreparedItem){
                    activePreparedItem=item;
                    window.__gv10eRandomGalaxy?.setPreparedHdResource?.(key,item.objectUrl,item.sourceKind,item.image);
                    return;
                }
                if(prefetchReady.length<HUBBLE_PREFETCH_TARGET)prefetchReady.push(item);else releasePreparedItem(item);
            }catch(error){
                if(error?.name==='AbortError'){
                    if(key===activeTargetKey)priorityPrefetchDestination=destination;
                    return;
                }
                prefetchFailedCount++;
                setHdStatus(destination,'RETRY-WAIT');
                prefetchRetryAfter.set(key,Date.now()+PREFETCH_RETRY_MS);
            }
        })().finally(()=>{
            prefetchLoading.delete(key);
            if(activePrefetchKey===key){activePrefetchAbort=null;activePrefetchKey=''}
            if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
        });
        prefetchLoading.set(key,promise);
    }

    function fillPrefetchQueue(){
        if(backgroundWorkSuspended)return;
        if(prefetchLoading.size)return;
        if(priorityPrefetchDestination){
            const destination=priorityPrefetchDestination;
            priorityPrefetchDestination=null;
            startPrefetch(destination,true);
            return;
        }
        if(prefetchReady.length>=HUBBLE_PREFETCH_TARGET)return;
        const candidate=choosePrefetchCandidate();
        if(candidate)startPrefetch(candidate);else scheduleRetryFill();
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
        setPreparedActive(item);
        if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
        return destinationWithPrepared(item);
    }

    async function waitForPreparedKey(key){
        for(;;){
            if(activePreparedItem?.key===key)return true;
            const loading=prefetchLoading.get(key);
            if(loading){
                try{await loading}catch(_){}
                return activePreparedItem?.key===key;
            }
            if(priorityPrefetchDestination&&destinationKey(priorityPrefetchDestination)===key){
                await new Promise(resolve=>setTimeout(resolve,25));
                continue;
            }
            return false;
        }
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
        const scaled=value>=1000?value/1000:value;
        const [integer,fraction='00']=scaled.toFixed(2).split('.');
        return {integer,fraction:fraction.padEnd(2,'0').slice(0,2),unit:value>=1000?'BILLION LIGHT-YEARS':'MILLION LIGHT-YEARS'};
    }

    function beginTravelHud(destination){
        const hud=document.getElementById('gv-travel-hud');
        const destinationEl=document.getElementById('gv-travel-destination');
        const distanceIntegerEl=document.getElementById('gv-travel-distance-integer');
        const distanceFractionEl=document.getElementById('gv-travel-distance-fraction');
        const distanceUnitEl=document.getElementById('gv-travel-distance-unit');
        if(!hud||!destinationEl||!distanceIntegerEl||!distanceFractionEl||!distanceUnitEl)return;
        cancelAnimationFrame(travelHudFrame);
        const state=window.GV10E?.randomGalaxy?.getState?.()||window.__gv10eRandomGalaxy?.getState?.()||{};
        const coords=window.aladin_cosmic_command_test?.getRaDec?.()||[HOME.ra,HOME.dec];
        const source={...(state.currentGalaxy||HOME),ra:Number(coords[0]),dec:Number(coords[1])};
        const fov=window.aladin_cosmic_command_test?.getFov?.()||[0,0];
        const firstHomeTrip=!(Number(source?.distance)>0)&&Number(fov[0])>=300;
        const hudSeconds=firstHomeTrip?10:TRAVEL_SECONDS;
        const total=routeDistanceMillionLy(source,destination);
        destinationEl.textContent=destination.name.toUpperCase();
        const initialDistance=formatTravelDistance(0);
        distanceIntegerEl.textContent=initialDistance.integer;
        distanceFractionEl.textContent=initialDistance.fraction;
        distanceUnitEl.textContent=initialDistance.unit;
        hud.classList.add('gv-visible');
        const started=performance.now();
        const frame=now=>{
            const t=Math.min(1,(now-started)/(hudSeconds*1000));
            const shown=formatTravelDistance(total*(firstHomeTrip?t:distanceProgress(t)));
            distanceIntegerEl.textContent=shown.integer;
            distanceFractionEl.textContent=shown.fraction;
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
            if(!destination){destination=setUnpreparedActive(requested)}
        }else{
            destination=consumeReady(null,excludeName);
            if(!destination){
                const inFlight=inFlightDestination(excludeName);
                if(inFlight)destination=setUnpreparedActive(inFlight);
                else destination=setUnpreparedActive(chooseGalaxy(galaxyCatalog,excludeName));
            }
        }
        activeTargetKey=destinationKey(destination);
        if(Number.isFinite(Number(destination.aladinRotation))&&typeof window.aladin_cosmic_command_test?.setRotation==='function'){
            try{window.aladin_cosmic_command_test.setRotation(Number(destination.aladinRotation))}catch(error){console.warn('GV-10E OPTIONAL ARRIVAL ROTATION SKIPPED',error)}
        }
        beginTravelHud(destination);
        return destination;
    }

    function getHubblePrefetchState(){
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            readyCount:prefetchReady.length,
            loadingCount:prefetchLoading.size,
            failedCount:prefetchFailedCount,
            activeDownloadKey:activePrefetchKey,
            activePreparedGalaxy:activePreparedItem?.destination?.name||'',
            activePreparedSource:activePreparedItem?.sourceKind||'',
            queuedDestinations:prefetchReady.map(item=>item.destination.name),
            downloads:getHubbleDownloadStatus()
        });
    }

    function getAladinPrewarmState(){
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            cachedCount:aladinPrewarmedKeys.size,
            activeKey:aladinPrewarmActiveKey,
            queuedDestinations:[]
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
        version.textContent=`VERSION ${DISPLAY_VERSION}`;
        version.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`);
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
        hud.innerHTML='<div id="gv-travel-distance"><span id="gv-travel-distance-value"><span id="gv-travel-distance-integer">0</span><span id="gv-travel-distance-decimal">.</span><span id="gv-travel-distance-fraction">00</span></span><span id="gv-travel-distance-unit">MILLION LIGHT-YEARS</span></div><div id="gv-travel-primary"><div id="gv-travel-course">COURSE LOCKED</div><div id="gv-travel-heading">HEADING TO</div><div id="gv-travel-destination"></div></div>';
        root.appendChild(hud);
        return {version,nav,back,random,forward,hud};
    }

    function createUniverseContext(root){
        const context=document.createElement('div');
        context.id='gv-universe-context';
        context.setAttribute('aria-live','polite');
        context.innerHTML='<div class="gv-universe-label">THIS IS OUR MAP OF THE OBSERVABLE UNIVERSE<span class="gv-universe-count">EST. ~2 TRILLION GALAXIES</span></div><div class="gv-universe-leader" aria-hidden="true"></div>';
        root.appendChild(context);
        return context;
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
        fov:360,
        projection:'MOL',
        cooFrame:'galactic',
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
    if(typeof aladin.setFrame==='function')aladin.setFrame('galactic');
    if(typeof aladin.setRotation==='function')aladin.setRotation(0);
    if(typeof aladin.gotoRaDec==='function')aladin.gotoRaDec(HOME.ra,HOME.dec);
    if(typeof aladin.setFov==='function')aladin.setFov(360);
    window.aladin_cosmic_command_test=aladin;

    const hamburgerHost=createHost(root,'gv-hamburger-host');
    const coordinateHost=createHost(root,'gv-coordinate-host');
    const targetHost=createHost(root,'gv-target-host');
    const randomGalaxyHost=createHost(root,'gv-random-galaxy-host');
    const reticle=createCenterReticle(root);
    const bottom=createBottomControls(root);
    const universeContext=createUniverseContext(root);
    const homeOverlay=createHomeOverlay(root);

    galaxyCatalog=await galaxyCatalogPromise;
    fillPrefetchQueue();

    await loadScript(HAMBURGER_URL,'gvHamburger0002');
    if(window.GalaxyViewerHamburgerMenu?.version!=='0002')throw new Error('HAMBURGER MODULE 0002 EXPORT MISSING');
    const hamburger=window.GalaxyViewerHamburgerMenu.init({
        host:hamburgerHost,
        onProjectionSelected(name,detail){
            try{
                if(typeof aladin.setProjection!=='function')throw new Error('ALADIN setProjection IS UNAVAILABLE');
                aladin.setProjection(detail.code);
            }catch(error){console.error('GV-10E PROJECTION FAILURE',name,detail?.code,error)}
        }
    });
    hamburger.root.style.position='absolute';
    hamburger.root.style.inset='0';
    hamburger.root.style.width='100%';
    hamburger.root.style.height='100%';
    hamburger.root.style.pointerEvents='none';
    hamburger.menuButton.style.pointerEvents='auto';

    await loadScript(COORDINATE_URL,'gvCoordinate0004');
    if(window.GalaxyCoordinateOverlay?.VERSION!=='0003')throw new Error('COORDINATE MODULE 0004 PATH / 0003 VERIFIED CORE EXPORT MISSING');
    let frame='GAL',latestRa=HOME.ra,latestDec=HOME.dec;
    let coordinate=null;
    function renderCoordinates(){
        if(!coordinate)return;
        const shown=frame==='GAL'?equatorialToGalactic(latestRa,latestDec):[latestRa,latestDec];
        coordinate.setFrame(frame);
        coordinate.update(shown[0],shown[1]);
    }
    coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GV-10E FRAME CHANGE WARNING',error)}
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

    await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0029');
    if(window.GalaxyRandomGalaxy?.VERSION!=='0012')throw new Error('RANDOM GALAXY 0029 PATH / 0012 VERIFIED CORE EXPORT MISSING');
    function historySnapshot(destination){
        const {preparedHdUrl,preparedSource,preparedHdImage,...snapshot}=destination||{};
        return Object.freeze({...snapshot});
    }
    function setHistoryControls(){
        const busy=navigationPending||Boolean(window.__gv10eRandomGalaxy?.getState?.().busy);
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
        suspendBackgroundWork();
        forcedDestination=galaxyHistory[index];
        pendingHistoryIndex=index;
        navigationPending=true;
        homeOverlay.classList.add('gv-hidden');universeContext.classList.add('gv-hidden');setHistoryControls();
        randomGalaxy.travelToRandom().catch(error=>{
            forcedDestination=null;pendingHistoryIndex=null;navigationPending=false;resumeBackgroundWork();endTravelHud();setHistoryControls();console.error('GV-10E HISTORY NAVIGATION FAILURE',error);
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
        travelSeconds:TRAVEL_SECONDS,
        onArrival(destination){
            navigationPending=false;
            endTravelHud();
            recordArrival(destination);
            setHistoryControls();
            resumeBackgroundWork();
        },
        onError(error){
            navigationPending=false;pendingHistoryIndex=null;forcedDestination=null;endTravelHud();setHistoryControls();resumeBackgroundWork();console.error('GV-10E RANDOM GALAXY FAILURE',error);
        }
    });
    window.__gv10eRandomGalaxy=randomGalaxy;
    await randomGalaxy.ready;
    const presentationStyle=document.createElement('style');
    presentationStyle.textContent='#gv-random-galaxy{font-size:15.5px!important;border:2px solid #ABB3AA!important;box-shadow:none!important;filter:brightness(1.10)}.gv-galaxy-history{border:2px solid #ABB3AA!important;box-shadow:none!important;filter:brightness(1.10);opacity:1!important}.gvrg-hd-science,.gvrg-hd-viewport{box-sizing:border-box!important;width:min(620px,96vw)!important;border:1px solid #78FFAB!important;border-radius:8px!important}.gvrg-hd-science{background:rgba(0,12,8,.88)!important;box-shadow:inset 0 0 6px rgba(120,255,171,.10),0 0 8px rgba(87,255,147,.22)!important}.gvrg-hd-viewport{left:50%!important;right:auto!important;transform:translateX(-50%);background:#020B07!important;box-shadow:inset 0 0 6px rgba(120,255,171,.10),0 0 8px rgba(87,255,147,.22)!important}.gvrg-hd-icon-button{background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94))!important;border:2px solid #ff8214!important;border-radius:5px!important;box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(255,130,20,.38),0 0 14px rgba(255,130,20,.18)!important}.gvrg-hd img{scale:1.052632}';
    document.head.appendChild(presentationStyle);
    const hubbleIcon=randomGalaxy.hubbleIconButton?.querySelector('img');
    if(hubbleIcon)hubbleIcon.src='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble-NASA-ESA-logo.png?v=9283e83cfbacd230551e9fc005794138be59709b';
    const hdScience=randomGalaxy.hdScience;
    if(hdScience){
        const scienceItems=[...hdScience.querySelectorAll('.gvrg-hd-science-item')];
        const constellationItems=scienceItems.filter(item=>String(item.querySelector('.gvrg-hd-science-label')?.textContent||'').trim().toUpperCase()==='CONST');
        let constellationItem=constellationItems.shift()||null;
        constellationItems.forEach(item=>item.remove());
        let constellationValue=null;
        if(!constellationItem){
            constellationItem=document.createElement('div');
            constellationItem.className='gvrg-hd-science-item';
            const key=document.createElement('div');
            key.className='gvrg-hd-science-label';
            key.textContent='CONST';
            constellationValue=document.createElement('div');
            constellationValue.className='gvrg-hd-science-value';
            constellationItem.append(key,constellationValue);
            const ageItem=scienceItems.find(item=>String(item.querySelector('.gvrg-hd-science-label')?.textContent||'').trim().toUpperCase()==='AGE');
            hdScience.insertBefore(constellationItem,ageItem||null);
        }else{
            constellationValue=constellationItem.querySelector('.gvrg-hd-science-value');
        }
        const syncHdConst=()=>{
            if(constellationValue)constellationValue.textContent=String(randomGalaxy.activeDestination?.constellation||randomGalaxy.constellationValueEl?.textContent||'').trim().toUpperCase();
        };
        if(randomGalaxy.constellationValueEl)new MutationObserver(syncHdConst).observe(randomGalaxy.constellationValueEl,{childList:true,subtree:true,characterData:true});
        randomGalaxy.viewHdButton?.addEventListener('click',syncHdConst,true);
        randomGalaxy.hubbleIconButton?.addEventListener('click',syncHdConst,true);
        syncHdConst();
    }

    const deferHdUntilPrepared=async event=>{
        const destination=randomGalaxy.getState?.().activeDestination;
        const key=destinationKey(destination);
        const pending=Boolean(key&&(prefetchLoading.has(key)||(priorityPrefetchDestination&&destinationKey(priorityPrefetchDestination)===key)));
        if(!pending)return;
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        try{
            await waitForPreparedKey(key);
            randomGalaxy.showHubbleHD();
        }catch(error){
            console.error('GV-10E HUBBLE PREPARATION WAIT FAILURE',error);
            try{randomGalaxy.showHubbleHD()}catch(fallbackError){console.error('GV-10E HUBBLE FALLBACK FAILURE',fallbackError)}
        }
    };

    window.addEventListener('beforeunload',()=>{
        if(activePrefetchAbort)activePrefetchAbort.abort();
        if(prefetchRetryTimer)clearTimeout(prefetchRetryTimer);
        if(aladinPrewarmTimer)clearTimeout(aladinPrewarmTimer);
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        randomGalaxy.viewHdButton?.removeEventListener('click',deferHdUntilPrepared,true);
        randomGalaxy.hubbleIconButton?.removeEventListener('click',deferHdUntilPrepared,true);
        releasePreparedItem(activePreparedItem);releasePreparedItem(historyPreparedItem);prefetchReady.splice(0).forEach(releasePreparedItem);
        try{aladinPrewarmHost?.remove()}catch(_){}
    },{once:true});
    bottom.random.addEventListener('click',suspendBackgroundWork,true);
    bottom.random.addEventListener('click',()=>{pendingHistoryIndex=null;navigationPending=true;homeOverlay.classList.add('gv-hidden');universeContext.classList.add('gv-hidden');setHistoryControls()});
    bottom.back.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex-1));
    bottom.forward.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex+1));
    setHistoryControls();
    window.GV10E=Object.freeze({version:VERSION,displayVersion:DISPLAY_VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,universeContext,homeOverlay,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,startHubblePrefetch:fillPrefetchQueue,getGalaxyHistory:()=>({index:galaxyHistoryIndex,items:galaxyHistory.map(item=>({name:item.name,archiveId:item.archiveId}))})});
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length}}));
})().catch(error=>{console.error('GALAXY VIEWER 10E STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});
"""))

# GV-beta-0010E staged