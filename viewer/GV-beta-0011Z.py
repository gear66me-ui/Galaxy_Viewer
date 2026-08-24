from IPython.display import HTML, Javascript, display

# Galaxy Viewer active implementation
# Standalone Galaxy Viewer implementation.
# Galaxy Viewer consolidated active implementation.
# Functional sections own startup, controls, random navigation, prefetch, HD presentation,
# stale-render recovery, and bounded navigation-resource retention.

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
#gv-startup-wait{position:absolute;inset:0;z-index:7085;display:flex;align-items:center;justify-content:center;background:#000;pointer-events:none}
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
#gv-version-label{position:absolute;left:50%;bottom:51px;z-index:7400;transform:translateX(-50%);height:10px;color:#9BE5FF;font:400 8px/10px "Space Age",sans-serif;letter-spacing:.85px;text-align:center;text-transform:uppercase;text-shadow:0 0 4px rgba(221,248,255,.28),0 0 7px rgba(88,191,255,.58);white-space:nowrap;pointer-events:none}
#gv-apk-cover{flex-direction:column;gap:18px}#gv-apk-cover .gv-viewer-version{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}
</style>
<div id="aladin-cosmic-command-test"><div id="gv-startup-wait" aria-hidden="true"></div></div>
<script>(()=>{const cover=document.getElementById('gv-apk-cover');if(!cover)return;const img=cover.querySelector('img');if(img)img.src='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';const version=document.createElement('div');version.className='gv-viewer-version';version.textContent='VERSION 11X';cover.appendChild(version)})();</script>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='ACTIVE';
    const DISPLAY_VERSION='11X';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=9ed18798f4c7010b76782d0ff2bf0c8ec5eb4cba';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0004.js?v=4c9a595860ed69d800d4c1a038c4e0402c69bba0';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=9f50e6c8e199b64b82ee49267250157c35997662';
    const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/gv-random-galaxy-0034.js';
    const MASTER_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
    const RAW_BETA_ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
    const RETICLE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/runtime/navigation/galaxy-viewer-reticle.svg?v=fd0f8aa1d5d1f5746e373577c06ae6c81d1f9cc0';
    const TARGET_ICON_URL='data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%20role%3D%22img%22%20aria-label%3D%22Galaxy%20Viewer%20target%20icon%22%3E%0A%20%20%3Cdefs%3E%0A%20%20%20%20%3ClinearGradient%20id%3D%22ring%22%20x1%3D%224.5%22%20y1%3D%2210%22%20x2%3D%2227.5%22%20y2%3D%2222%22%20gradientUnits%3D%22userSpaceOnUse%22%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%220%22%20stop-color%3D%22%2345E7FF%22%2F%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%220.52%22%20stop-color%3D%22%234F9DFF%22%2F%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%221%22%20stop-color%3D%22%237575FF%22%2F%3E%0A%20%20%20%20%3C%2FlinearGradient%3E%0A%20%20%3C%2Fdefs%3E%0A%20%20%3Ccircle%20cx%3D%2216%22%20cy%3D%2216%22%20r%3D%229.5%22%20fill%3D%22%23000000%22%20stroke%3D%22%23FF6B2D%22%20stroke-width%3D%221.8%22%2F%3E%0A%20%20%3Cellipse%20cx%3D%2216%22%20cy%3D%2216%22%20rx%3D%2211.5%22%20ry%3D%224.2%22%20fill%3D%22none%22%20stroke%3D%22url%28%23ring%29%22%20stroke-width%3D%222.2%22%20transform%3D%22rotate%28-18%2016%2016%29%22%2F%3E%0A%20%20%3Cellipse%20cx%3D%2216%22%20cy%3D%2216%22%20rx%3D%225.7%22%20ry%3D%222.2%22%20fill%3D%22none%22%20stroke%3D%22%2345E7FF%22%20stroke-width%3D%221.6%22%20transform%3D%22rotate%28-18%2016%2016%29%22%2F%3E%0A%20%20%3Ccircle%20cx%3D%2216%22%20cy%3D%2216%22%20r%3D%221.6%22%20fill%3D%22%237575FF%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M16%202.5V7%20M16%2025V29.5%20M2.5%2016H7%20M25%2016H29.5%22%20fill%3D%22none%22%20stroke%3D%22%23FFFFFF%22%20stroke-width%3D%221.6%22%20stroke-linecap%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E';
    const HUBBLE_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/hubble/hubble-icon.png';
    const JWST_ICON_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/runtime/providers/jwst/jwst-icon.png';
    const CHANDRA_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/chandra/chandra-icon.png';
    const HD_LAYOUT=Object.freeze({bannerRatio:403/1536,imageRatio:630/1536,gap:6,edge:6,iconInset:20});
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const ARRIVAL_OCCUPANCY=Object.freeze({target:0.35,max:0.40,minFov:0.05,maxFov:8});
    const PREFETCH_TARGET=10;
    const HISTORY_PREPARED_TARGET=10;
    const HEAVY_PREPARED_TARGET=5;
    const PREFETCH_MAX_WORKERS=3;
    const PREFETCH_PROBE_CONCURRENCY=3;
    const PREFETCH_HEALTH_INTERVAL_MS=30000;
    const ALADIN_PREWARM_DWELL_MS=1400;
    const ALADIN_PREWARM_INIT_TIMEOUT_MS=5000;
    const PREFETCH_RETRY_MS=5000;
    const HD_PREFERRED_MAX_BYTES=1024*1024;
    const FRAMING_SAMPLE_SIZE=96;
    const FRAMING_MAX_SHIFT_FRACTION=0.18;
    const TRAVEL_SECONDS=17.0;
    const FIRST_HOME_TRAVEL_SECONDS=7.5;
    const ARCHIVE_PRELOAD_TARGET=3;
    const startupTiming={startedAt:performance.now(),shellReadyAt:null,catalogReadyAt:null,randomReadyAt:null,fullReadyAt:null};

    let galaxyCatalog=[];
    let catalogRecordCount=0;
    let catalogDatabaseCounts=Object.freeze({hubble:0,jwst:0,chandra:0,total:0,eligibleHubble:0,eligibleJwst:0,eligibleChandra:0,eligibleTotal:0});
    let chandraTestQueue=[];
    let chandraTestTotal=0;
    let chandraTestOverrideActive=false;
    const prefetchReady=[];
    const prefetchQueued=[];
    const prefetchLoading=new Map();
    const prefetchControllers=new Map();
    const prefetchRetryAfter=new Map();
    const hdDownloadStatus=new Map();
    let prefetchFailedCount=0;
    let prefetchRetryTimer=0;
    let prefetchHealthTimer=0;
    let lastPrefetchHealth=Object.freeze({ready:0,loading:0,queued:0,total:0,activeKeys:Object.freeze([]),retryWait:Object.freeze([]),workers:Object.freeze([]),checkedAt:0});
    let priorityPrefetchDestination=null;
    let aladinPrefetchSerial=Promise.resolve();
    let activePreparedItem=null;
    const historyPreparedItems=[];
    let activeTargetKey='';
    let forcedDestination=null;
    let navigationPending=false;
    let backgroundWorkSuspended=false;
    let ensureArchivePreloadQueue=()=>{};
    let suspendArchivePreloads=()=>{};
    let resumeArchivePreloads=()=>{};
    let releaseActiveArchivePreload=()=>{};
    let syncHdProviderPresentation=()=>{};
    let hdArchiveIntegration=null;
    let aladinPrewarm=null;
    let aladinPrewarmHost=null;
    let aladinPrewarmReady=null;
    let aladinPrewarmUnavailable=false;
    let aladinPrewarmTimer=0;
    let aladinPrewarmWaitResolve=null;
    let aladinPrewarmActiveKey='';
    let aladinPrewarmLastKey='';
    const aladinPrewarmedKeys=new Set();
    const aladinPreparedReceipts=new Map();

    function setHdStatus(destination,state,sourceKind=''){
        const key=destinationKey(destination);
        if(!key)return;
        const old=hdDownloadStatus.get(key)||{};
        hdDownloadStatus.set(key,{key,name:String(destination?.name||old.name||''),state,sourceKind:sourceKind||old.sourceKind||'',updatedAt:Date.now()});
    }

    function getDownloadStatus(){
        return Object.freeze([...hdDownloadStatus.values()].map(item=>Object.freeze({...item})));
    }

    function suspendBackgroundWork(){
        if(backgroundWorkSuspended)return;
        backgroundWorkSuspended=true;
        const navigationState=randomNavigationWindow?.getState?.();
        const protectedAladinKey=destinationKey(navigationState?.pending?.destination||navigationState?.locked?.destination||navigationState?.locked||null);
        const preserveProtectedAladin=Boolean(
            protectedAladinKey&&
            aladinPrewarm&&
            aladinPrewarmHost&&
            aladinPrewarmLastKey===protectedAladinKey
        );
        if(aladinPrewarmTimer){clearTimeout(aladinPrewarmTimer);aladinPrewarmTimer=0}
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        aladinPrewarmActiveKey='';
        if(!preserveProtectedAladin){
            aladinPrewarm=null;
            aladinPrewarmReady=null;
            try{aladinPrewarmHost?.remove()}catch(_){}
            aladinPrewarmHost=null;
        }
        for(const controller of prefetchControllers.values())try{controller.abort()}catch(_){}
    }

    function resumeBackgroundWork(){
        if(!backgroundWorkSuspended)return;
        backgroundWorkSuspended=false;
        enforceHotPreparedWindow();
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

    function parseArchiveOrientation(value){
        const text=String(value??'').trim();
        if(!text)return null;
        const match=text.match(/North\s+is\s+([0-9]+(?:\.[0-9]+)?)\s*°?\s*(right|left)\s+of\s+vertical/i);
        if(!match)return null;
        const angle=Number(match[1]);
        if(!Number.isFinite(angle))return null;
        return normalizeSignedAngle((match[2].toLowerCase()==='left'?-1:1)*angle);
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
        const fov=fieldDegrees/ARRIVAL_OCCUPANCY.target;
        return Object.freeze({
            source:'ESA/HUBBLE GALAXIES CATALOG FULL-0002',provider:'HUBBLE',
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy:Array.isArray(physicalSizeLy)?physicalSizeLy.filter(value=>Number.isFinite(value)&&value>0):Number.isFinite(physicalSizeLy)&&physicalSizeLy>0?physicalSizeLy:null,
            fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,orientation:String(candidate.orientation||'').trim(),
            credit:String(candidate.credit||'ESA/Hubble').trim()||'ESA/Hubble',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'Hubble Space Telescope',
            githubImageUrl:String(candidate.githubImageUrl||'').trim(),sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    function chooseJwstImageUrl(candidate){
        const candidates=[...(Array.isArray(candidate?.jpegCandidates)?candidate.jpegCandidates:[]),candidate?.selectedImageUrl].map(value=>String(value||'').trim()).filter(Boolean);
        return candidates.find(url=>/\/screen\//i.test(url))||String(candidate?.selectedImageUrl||candidates[0]||'').trim();
    }

    function normalizeJwstGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??'').trim();
        const ageGyr=Number(candidate.science?.ageGyr);
        const ageYears=Number.isFinite(ageGyr)&&ageGyr>0?ageGyr*1_000_000_000:null;
        const scienceSize=Array.isArray(candidate.science?.sizeKly)?candidate.science.sizeKly.map(value=>Number(value)*1000):null;
        const physicalSizeLy=Array.isArray(scienceSize)?scienceSize.filter(value=>Number.isFinite(value)&&value>0):null;
        const fieldDegrees=parseFieldOfViewDegrees(candidate.fieldOfView);
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const hdUrl=chooseJwstImageUrl(candidate);
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation||!Number.isFinite(fieldDegrees)||fieldDegrees<=0)return null;
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){return null}
        const approvedHost=host=>host==='esawebb.org'||host.endsWith('.esawebb.org');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        const fov=fieldDegrees/ARRIVAL_OCCUPANCY.target;
        const orientation=String(candidate.orientation||'').trim();
        const archiveRotation=parseArchiveOrientation(orientation);
        return Object.freeze({
            source:'ESA/WEBB GALAXIES CATALOG FULL-0002',provider:'JWST',
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy, fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,orientation,
            aladinRotation:Number.isFinite(archiveRotation)?archiveRotation:null,
            credit:String(candidate.credit||'ESA/Webb, NASA & CSA').trim()||'ESA/Webb, NASA & CSA',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'James Webb Space Telescope',
            githubImageUrl:'',sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    function normalizeChandraGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??'').trim();
        const ageGyr=Number(candidate.science?.ageGyr);
        const ageYears=Number.isFinite(ageGyr)&&ageGyr>0?ageGyr*1_000_000_000:null;
        const scienceSize=Array.isArray(candidate.science?.sizeKly)?candidate.science.sizeKly.map(value=>Number(value)*1000):null;
        const physicalSizeLy=Array.isArray(scienceSize)?scienceSize.filter(value=>Number.isFinite(value)&&value>0):null;
        const fieldDegrees=parseFieldOfViewDegrees(candidate.fieldOfView);
        const fov=Number.isFinite(fieldDegrees)&&fieldDegrees>0?fieldDegrees/ARRIVAL_OCCUPANCY.target:0.25;
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const hdUrl=String(candidate.selectedImageUrl||'').trim();
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation)return null;
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){return null}
        const approvedHost=host=>host==='chandra.harvard.edu'||host.endsWith('.chandra.harvard.edu');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        return Object.freeze({
            source:'NASA CHANDRA X-RAY CENTER CATALOG FULL-0001',provider:'CHANDRA',
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy,fov,imageFovDegrees:Number.isFinite(fieldDegrees)&&fieldDegrees>0?fieldDegrees:null,hdUrl:hd.href,sourceUrl:source.href,orientation:String(candidate.orientation||'').trim(),
            credit:String(candidate.credit||'NASA/CXC').trim()||'NASA/CXC',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'Chandra X-ray Observatory',
            githubImageUrl:'',sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    async function loadMasterCatalog(){
        const response=await fetch(MASTER_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('MASTER CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const catalogs=payload?.catalogs;
        if(!catalogs?.hubble||!catalogs?.jwst||!catalogs?.chandra)throw new Error('MASTER CATALOG POINTERS MISSING');
        return Object.freeze({
            hubble:RAW_BETA_ROOT+catalogs.hubble,
            jwst:RAW_BETA_ROOT+catalogs.jwst,
            chandra:RAW_BETA_ROOT+catalogs.chandra
        });
    }

    async function loadHubbleCatalog(catalogUrl){
        const response=await fetch(catalogUrl,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL HUBBLE CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(!Array.isArray(raw)||!raw.length||!Number.isFinite(declared)||declared!==raw.length)throw new Error('FULL HUBBLE CATALOG COUNT MISMATCH');
        const eligible=raw.map(normalizeCatalogGalaxy).filter(Boolean);
        if(eligible.length<PREFETCH_TARGET)throw new Error('FULL HUBBLE CATALOG HAS FEWER THAN TEN TRUTHFULLY TARGETABLE GALAXIES');
        return Object.freeze({rawCount:raw.length,eligible:Object.freeze(eligible)});
    }

    async function loadJwstCatalog(catalogUrl){
        const response=await fetch(catalogUrl,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL JWST CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(payload?.version!=='full-0002')throw new Error('JWST CATALOG MUST BE FULL-0002');
        if(!Array.isArray(raw)||!raw.length||!Number.isFinite(declared)||declared!==raw.length)throw new Error('FULL JWST CATALOG COUNT MISMATCH');
        const eligible=raw.map(normalizeJwstGalaxy).filter(Boolean);
        if(!eligible.length)throw new Error('FULL JWST CATALOG HAS NO TARGETABLE GALAXIES');
        return Object.freeze({rawCount:raw.length,eligible:Object.freeze(eligible)});
    }

    async function loadChandraCatalog(catalogUrl){
        const response=await fetch(catalogUrl,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL CHANDRA CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(payload?.version!=='full-0001')throw new Error('CHANDRA CATALOG MUST BE FULL-0001');
        if(!Array.isArray(raw)||!raw.length||!Number.isFinite(declared)||declared!==raw.length)throw new Error('FULL CHANDRA CATALOG COUNT MISMATCH');
        const eligible=raw.map(normalizeChandraGalaxy).filter(Boolean);
        if(!eligible.length)throw new Error('FULL CHANDRA CATALOG HAS NO TARGETABLE GALAXIES');
        return Object.freeze({rawCount:raw.length,eligible:Object.freeze(eligible)});
    }

    function shuffledCopy(items){
        const copy=[...items];
        for(let i=copy.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]]}
        return copy;
    }

    async function loadCombinedGalaxyCatalog(){
        const catalogUrls=await loadMasterCatalog();
        const combined=[];
        const state={
            hubble:{rawCount:0,eligibleCount:0,done:false},
            jwst:{rawCount:0,eligibleCount:0,done:false},
            chandra:{rawCount:0,eligibleCount:0,done:false}
        };
        let settled=0;
        let startupResolved=false;
        let resolveStartup,rejectStartup;
        const startup=new Promise((resolve,reject)=>{resolveStartup=resolve;rejectStartup=reject});

        const publishCounts=()=>{
            catalogRecordCount=combined.length;
            catalogDatabaseCounts=Object.freeze({
                hubble:state.hubble.rawCount,
                jwst:state.jwst.rawCount,
                chandra:state.chandra.rawCount,
                total:state.hubble.rawCount+state.jwst.rawCount+state.chandra.rawCount,
                eligibleHubble:state.hubble.eligibleCount,
                eligibleJwst:state.jwst.eligibleCount,
                eligibleChandra:state.chandra.eligibleCount,
                eligibleTotal:combined.length
            });
            console.info('GALAXY VIEWER CATALOG COUNTS',catalogDatabaseCounts);
        };

        const maybeReleaseStartup=()=>{
            publishCounts();
            if(!startupResolved&&combined.length>=PREFETCH_TARGET){
                startupResolved=true;
                resolveStartup(combined);
                return;
            }
            if(settled===3&&!startupResolved){
                startupResolved=true;
                if(combined.length)resolveStartup(combined);
                else rejectStartup(new Error('NO TARGETABLE GALAXY CATALOG COULD BE LOADED'));
            }
        };

        const attach=(provider,loader)=>{
            loader.then(data=>{
                state[provider].rawCount=data.rawCount;
                state[provider].eligibleCount=data.eligible.length;
                state[provider].done=true;
                combined.push(...data.eligible);
                if(provider==='chandra'){
                    chandraTestQueue=shuffledCopy(data.eligible);
                    chandraTestTotal=chandraTestQueue.length;
                    chandraTestOverrideActive=false;
                }
            }).catch(error=>{
                state[provider].done=true;
                console.warn(`GALAXY VIEWER ${provider.toUpperCase()} CATALOG STARTUP WARNING`,error);
            }).finally(()=>{
                settled++;
                maybeReleaseStartup();
                if(startupResolved&&!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
            });
        };

        attach('hubble',loadHubbleCatalog(catalogUrls.hubble));
        attach('jwst',loadJwstCatalog(catalogUrls.jwst));
        attach('chandra',loadChandraCatalog(catalogUrls.chandra));

        return startup;
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

    function enforceHotPreparedWindow(){
        const hotOrder=[
            ...(randomNavigationWindow?.hotKeys?.() ||
               randomNavigationWindow?.getState?.().hotKeys ||
               [])
        ].slice(0,HEAVY_PREPARED_TARGET);
        const hotKeys=new Set(hotOrder);
        const retainedKeys=new Set();

        if(activePreparedItem?.key){
            if(hotKeys.has(activePreparedItem.key)){
                retainedKeys.add(activePreparedItem.key);
            }else{
                releasePreparedItem(activePreparedItem);
                activePreparedItem=null;
            }
        }

        for(let i=historyPreparedItems.length-1;i>=0;i--){
            const item=historyPreparedItems[i];
            const keep=Boolean(
                item?.key&&
                hotKeys.has(item.key)&&
                !retainedKeys.has(item.key)&&
                retainedKeys.size<HEAVY_PREPARED_TARGET
            );
            if(keep){
                retainedKeys.add(item.key);
                continue;
            }
            historyPreparedItems.splice(i,1);
            releasePreparedItem(item);
        }

        for(let i=prefetchReady.length-1;i>=0;i--){
            const item=prefetchReady[i];
            const keep=Boolean(
                item?.key&&
                hotKeys.has(item.key)&&
                !retainedKeys.has(item.key)&&
                retainedKeys.size<HEAVY_PREPARED_TARGET
            );
            if(keep){
                retainedKeys.add(item.key);
                continue;
            }
            prefetchReady.splice(i,1);
            releasePreparedItem(item);
            if(item?.destination)setHdStatus(item.destination,'QUEUED');
        }

        for(const key of hotOrder){
            if(retainedKeys.has(key)||
               prefetchLoading.has(key)||
               prefetchQueued.some(destination=>destinationKey(destination)===key))
                continue;
            const destination=galaxyCatalog.find(item=>destinationKey(item)===key);
            if(destination){
                enqueuePrefetch(destination,key===activeTargetKey);
                retainedKeys.add(key);
            }
        }
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
                    if(!(image.complete&&image.naturalWidth))await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HD PRELOAD FAILED')),{once:true})});
                }
            }else if(!(image.complete&&image.naturalWidth)){
                await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HD PRELOAD FAILED')),{once:true})});
            }
            if(!image.naturalWidth||!image.naturalHeight)throw new Error('HD PRELOAD DECODED WITHOUT IMAGE DIMENSIONS');
            return {image,objectUrl};
        }catch(error){
            image.src='';
            URL.revokeObjectURL(objectUrl);
            throw error;
        }
    }

    function hdVariantRank(url){
        const value=String(url||'').toLowerCase();
        if(value.includes('/publicationjpg/'))return 60;
        if(value.includes('/large/'))return 50;
        if(value.includes('/screen/'))return 40;
        if(value.includes('/wallpaper'))return 30;
        if(value.includes('/thumb700'))return 20;
        if(value.includes('/thumb300'))return 10;
        return 45;
    }

    function buildHdSourceCandidates(destination){
        const sources=[];
        const seen=new Set();
        const add=(url,kind,rank=hdVariantRank(url))=>{
            const value=String(url||'').trim();
            if(!/^https:\/\//i.test(value)||seen.has(value))return;
            seen.add(value);sources.push({url:value,kind,rank});
        };
        const github=String(destination.githubImageUrl||'').trim();
        const archive=String(destination.hdUrl||'').trim();
        if(github)add(github,'GITHUB',55);
        if(archive){
            const provider=destination.provider||'ARCHIVE';
            const match=archive.match(/^(https:\/\/[^/]+\/archives\/images\/)([^/]+)(\/[^?#]+(?:\?[^#]*)?)$/i);
            if(match){
                for(const variant of ['publicationjpg','large','screen','wallpaper1','thumb700x','thumb300y'])add(match[1]+variant+match[3],provider,hdVariantRank('/'+variant+'/'));
            }
            add(archive,provider);
        }
        return sources.sort((a,b)=>b.rank-a.rank);
    }

    async function probeHdSourceBytes(source,signal=null){
        try{
            const head=await fetch(source.url,{method:'HEAD',cache:'force-cache',signal});
            if(head.ok){
                const length=Number(head.headers.get('content-length'));
                if(Number.isFinite(length)&&length>0)return length;
            }
        }catch(error){if(error?.name==='AbortError')throw error}
        try{
            const probe=await fetch(source.url,{method:'GET',headers:{Range:'bytes=0-0'},cache:'force-cache',signal});
            if(!probe.ok&&probe.status!==206)return null;
            const range=String(probe.headers.get('content-range')||'');
            const total=Number(range.match(/\/(\d+)$/)?.[1]);
            const length=Number(probe.headers.get('content-length'));
            try{await probe.body?.cancel()}catch(_){}
            if(Number.isFinite(total)&&total>0)return total;
            if(probe.status===200&&Number.isFinite(length)&&length>0)return length;
        }catch(error){if(error?.name==='AbortError')throw error}
        return null;
    }

    async function mapWithConcurrency(items,limit,worker){
        const results=new Array(items.length);
        let next=0;
        const count=Math.max(1,Math.min(Number(limit)||1,items.length));
        await Promise.all(Array.from({length:count},async()=>{
            for(;;){
                const index=next++;
                if(index>=items.length)return;
                results[index]=await worker(items[index],index);
            }
        }));
        return results;
    }

    async function orderHdSourcesBySize(destination,signal=null){
        const sources=buildHdSourceCandidates(destination);
        if(sources.length<2)return sources;
        const probed=await mapWithConcurrency(sources,PREFETCH_PROBE_CONCURRENCY,async source=>({...source,bytes:await probeHdSourceBytes(source,signal)}));
        const preferred=[];
        const oversized=[];
        const unknown=[];
        for(const source of probed){
            const bytes=source.bytes;
            if(Number.isFinite(bytes)&&bytes>0&&bytes<=HD_PREFERRED_MAX_BYTES)preferred.push(source);
            else if(Number.isFinite(bytes)&&bytes>HD_PREFERRED_MAX_BYTES)oversized.push(source);
            else unknown.push(source);
        }
        preferred.sort((a,b)=>b.rank-a.rank||b.bytes-a.bytes);
        oversized.sort((a,b)=>a.bytes-b.bytes||a.rank-b.rank);
        unknown.sort((a,b)=>a.rank-b.rank);
        return [...preferred,...oversized,...unknown];
    }

    async function prepareHdDestination(destination,signal=null){
        const sources=await orderHdSourcesBySize(destination,signal);
        let lastError=null;
        for(const source of sources){
            try{
                setHdStatus(destination,'DOWNLOADING',source.kind);
                const response=await fetch(source.url,{cache:'force-cache',signal});
                if(!response.ok)throw new Error('HD PRELOAD RETURNED HTTP '+response.status);
                const blob=await response.blob();
                if(signal?.aborted)throw new DOMException('HD PRELOAD SUSPENDED','AbortError');
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
        throw lastError||new Error('HD PRELOAD HAS NO USABLE SOURCE');
    }

    function ensureAladinPrewarm(){
        if(backgroundWorkSuspended)return Promise.resolve(null);
        if(aladinPrewarmReady)return aladinPrewarmReady;
        aladinPrewarmReady=new Promise((resolve,reject)=>{
            let settled=false;
            let initTimeout=0;
            const finish=(callback,value)=>{
                if(settled)return;
                settled=true;
                if(initTimeout){clearTimeout(initTimeout);initTimeout=0}
                callback(value);
            };
            const frame=document.createElement('iframe');
            aladinPrewarmHost=frame;
            frame.id='gv-aladin-prewarm-frame';
            frame.setAttribute('aria-hidden','true');
            frame.tabIndex=-1;
            Object.assign(frame.style,{position:'fixed',left:'-10000px',top:'0',width:'512px',height:'512px',border:'0',opacity:'0',pointerEvents:'none',overflow:'hidden'});
            frame.srcdoc=`<!doctype html><html><head><link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css"><style>html,body,#gv-prewarm{margin:0;width:512px;height:512px;overflow:hidden;background:#000}</style></head><body><div id="gv-prewarm"></div><script src="${ALADIN_URL}"><\/script></body></html>`;
            initTimeout=setTimeout(()=>finish(reject,new Error('ISOLATED ALADIN PREWARM INITIALIZATION TIMED OUT')),ALADIN_PREWARM_INIT_TIMEOUT_MS);
            frame.addEventListener('load',async()=>{
                try{
                    if(backgroundWorkSuspended){finish(resolve,null);return}
                    const win=frame.contentWindow;
                    if(!win?.A?.init)throw new Error('ISOLATED ALADIN PREWARM EXPORT MISSING');
                    await win.A.init;
                    if(settled)return;
                    if(backgroundWorkSuspended){finish(resolve,null);return}
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
                    aladinPrewarmUnavailable=false;
                    finish(resolve,aladinPrewarm);
                }catch(error){finish(reject,error)}
            },{once:true});
            frame.addEventListener('error',()=>finish(reject,new Error('ISOLATED ALADIN PREWARM FRAME FAILED TO LOAD')),{once:true});
            document.body.appendChild(frame);
        }).catch(error=>{
            console.warn('GALAXY VIEWER ISOLATED ALADIN PREWARM WARNING',error);
            aladinPrewarmUnavailable=true;
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
        const receipt=Object.freeze({
            key,
            ra:Number(destination.ra),
            dec:Number(destination.dec),
            fov:Number(destination.fov),
            rotation:Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):0,
            projection:'SIN',
            preparedAt:Date.now()
        });
        aladinPrewarmedKeys.add(key);
        aladinPreparedReceipts.set(key,receipt);
        aladinPrewarmLastKey=key;
        return receipt;
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

    function deriveSourceFraming(destination,sourceImage){
        if(!sourceImage?.naturalWidth||!sourceImage?.naturalHeight||!aladinPrewarm||!aladinPrewarmHost)return destination;
        try{
            const skyCanvas=aladinPrewarmHost.contentDocument?.querySelector('canvas');
            if(!skyCanvas)return destination;
            const sourceImageProfile=imageLightProfile(sourceImage),sky=imageLightProfile(skyCanvas);
            if(!sourceImageProfile||!sky)return destination;
            const width=skyCanvas.clientWidth||skyCanvas.width||512,height=skyCanvas.clientHeight||skyCanvas.height||512;
            const desiredX=sourceImageProfile.x/FRAMING_SAMPLE_SIZE*width;
            const desiredY=sourceImageProfile.y/FRAMING_SAMPLE_SIZE*height;
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
            let rotation=Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):null;
            if(rotation===null&&sourceImageProfile.eccentricity>.22&&sky.eccentricity>.22){
                const delta=normalizeSignedAngle(sourceImageProfile.angle-sky.angle);
                if(Number.isFinite(delta)&&Math.abs(delta)<=90)rotation=delta;
            }
            return Object.freeze({...destination,ra,dec,aladinRotation:rotation,framingCorrected:true});
        }catch(error){
            console.warn('GALAXY VIEWER OPTIONAL ARCHIVE FRAMING SKIPPED',error);
            return destination;
        }
    }

    function blockedPrefetchKeys(){
        const keys=new Set(prefetchReady.map(item=>item.key));
        for(const destination of prefetchQueued)keys.add(destinationKey(destination));
        for(const key of prefetchLoading.keys())keys.add(key);
        if(priorityPrefetchDestination)keys.add(destinationKey(priorityPrefetchDestination));
        if(activePreparedItem?.key)keys.add(activePreparedItem.key);
        for(const item of historyPreparedItems)if(item?.key)keys.add(item.key);
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
        if(prefetchRetryTimer)return;
        const now=Date.now();
        const waits=[...prefetchRetryAfter.values()].map(value=>Number(value)-now).filter(value=>value>0);
        if(!waits.length)return;
        prefetchRetryTimer=setTimeout(()=>{prefetchRetryTimer=0;fillPrefetchQueue()},Math.max(100,Math.min(...waits)));
    }

    function queueHasKey(key){return prefetchQueued.some(destination=>destinationKey(destination)===key)}

    function enqueuePrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItems.some(item=>item?.key===key))return false;
        const queuedIndex=prefetchQueued.findIndex(item=>destinationKey(item)===key);
        if(queuedIndex>=0){
            if(priority&&queuedIndex>0){const [queued]=prefetchQueued.splice(queuedIndex,1);prefetchQueued.unshift(queued)}
            return false;
        }
        if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return false}
        setHdStatus(destination,'QUEUED');
        if(priority)prefetchQueued.unshift(destination);else prefetchQueued.push(destination);
        return true;
    }

    function scheduleAladinEnhancement(item,destination,priority=false){
        const key=destinationKey(destination);
        const task=async()=>{
            if(backgroundWorkSuspended||!item?.image)return;
            try{
                try{await prepareAladinDestination(destination,priority)}catch(error){
                    if(error?.name==='AbortError')return;
                    console.warn('GALAXY VIEWER ALADIN DESTINATION PREWARM WARNING',error);
                }
                if(backgroundWorkSuspended||aladinPrewarmLastKey!==key)return;
                let preparedDestination=deriveSourceFraming(destination,item.image);
                if(preparedDestination!==destination&&preparedDestination.framingCorrected){
                    try{await prepareAladinDestination(preparedDestination,true)}catch(error){
                        if(error?.name==='AbortError')return;
                        preparedDestination=destination;
                    }
                }
                item.destination=preparedDestination;
            }catch(error){
                if(error?.name!=='AbortError')console.warn('GALAXY VIEWER SERIAL ALADIN PREWARM WARNING',error);
            }
        };
        const run=aladinPrefetchSerial.then(task,task);
        aladinPrefetchSerial=run.catch(()=>null);
    }

    function startPrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItems.some(item=>item?.key===key))return;
        if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return}
        if(prefetchLoading.size>=PREFETCH_MAX_WORKERS){enqueuePrefetch(destination,priority);return}
        const controller=new AbortController();
        prefetchControllers.set(key,controller);
        const promise=(async()=>{
            try{
                const item=await prepareHdDestination(destination,controller.signal);
                item.destination=destination;
                prefetchRetryAfter.delete(key);

                const hotKeys=new Set(
                    randomNavigationWindow?.hotKeys?.() ||
                    randomNavigationWindow?.getState?.().hotKeys ||
                    []
                );
                if(key!==activeTargetKey&&!hotKeys.has(key)){
                    releasePreparedItem(item);
                    setHdStatus(destination,'QUEUED');
                    return;
                }

                if(key===activeTargetKey&&!activePreparedItem){
                    activePreparedItem=item;
                    window.GalaxyViewerRandomGalaxy?.setPreparedHdResource?.(key,item.objectUrl,item.sourceKind,item.image);
                }else if(prefetchReady.length<PREFETCH_TARGET){
                    prefetchReady.push(item);
                }else{
                    releasePreparedItem(item);
                    return;
                }
                enforceHotPreparedWindow();
                scheduleAladinEnhancement(item,destination,priority);
            }catch(error){
                if(error?.name==='AbortError'){
                    setHdStatus(destination,'SUSPENDED');
                    if(key===activeTargetKey)priorityPrefetchDestination=destination;
                    return;
                }
                prefetchFailedCount++;
                setHdStatus(destination,'RETRY-WAIT');
                prefetchRetryAfter.set(key,Date.now()+PREFETCH_RETRY_MS);
            }
        })().finally(()=>{
            prefetchLoading.delete(key);
            prefetchControllers.delete(key);
            queueMicrotask(fillPrefetchQueue);
            queueMicrotask(ensureArchivePreloadQueue);
        });
        prefetchLoading.set(key,promise);
    }

    function fillPrefetchQueue(){
        if(backgroundWorkSuspended)return;
        if(priorityPrefetchDestination){
            const destination=priorityPrefetchDestination;
            priorityPrefetchDestination=null;
            enqueuePrefetch(destination,true);
        }
        while(prefetchLoading.size<PREFETCH_MAX_WORKERS&&prefetchQueued.length){
            const destination=prefetchQueued.shift();
            startPrefetch(destination,destinationKey(destination)===activeTargetKey);
        }
        if(prefetchQueued.length)scheduleRetryFill();
    }

    function prefetchHealthCheck(){
        const ready=prefetchReady.length;
        const loading=prefetchLoading.size;
        const queued=prefetchQueued.length;
        const activeKeys=[...prefetchLoading.keys()];
        const retryWait=[...prefetchRetryAfter.entries()].filter(([,time])=>Date.now()<Number(time)).map(([key])=>key);
        const workers=activeKeys.map(key=>Object.freeze({...hdDownloadStatus.get(key)}));
        lastPrefetchHealth=Object.freeze({ready,loading,queued,total:ready+loading+queued,activeKeys:Object.freeze(activeKeys),retryWait:Object.freeze(retryWait),workers:Object.freeze(workers),checkedAt:Date.now()});
        if(!backgroundWorkSuspended&&lastPrefetchHealth.total<PREFETCH_TARGET)fillPrefetchQueue();
        return lastPrefetchHealth;
    }

    prefetchHealthTimer=setInterval(prefetchHealthCheck,PREFETCH_HEALTH_INTERVAL_MS);

    function destinationWithPrepared(item){
        return {...item.destination,preparedHdUrl:item.objectUrl,preparedSource:item.sourceKind,preparedHdImage:item.image};
    }

    function retainHistoryPrepared(item){
        if(!item?.key)return;
        const existing=historyPreparedItems.findIndex(candidate=>candidate?.key===item.key);
        if(existing>=0)historyPreparedItems.splice(existing,1);
        historyPreparedItems.unshift(item);
        while(historyPreparedItems.length>HISTORY_PREPARED_TARGET)
            releasePreparedItem(historyPreparedItems.pop());
        enforceHotPreparedWindow();
    }

    function takeHistoryPrepared(key){
        const index=historyPreparedItems.findIndex(item=>item?.key===key);
        return index>=0?historyPreparedItems.splice(index,1)[0]:null;
    }

    function setPreparedActive(item){
        if(activePreparedItem&&activePreparedItem!==item&&activePreparedItem.key!==item.key)
            retainHistoryPrepared(activePreparedItem);
        activePreparedItem=item;
        activeTargetKey=item.key;
    }

    function setUnpreparedActive(destination){
        const key=destinationKey(destination);
        if(activePreparedItem&&activePreparedItem.key!==key)
            retainHistoryPrepared(activePreparedItem);
        activePreparedItem=null;
        activeTargetKey=key;
        priorityPrefetchDestination=destination;
        if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
        return {...destination,preparedHdUrl:'',preparedSource:'',preparedHdImage:null};
    }

    function consumeReady(destination=null,excludeName=''){
        const requestedKey=destination?destinationKey(destination):'';
        if(requestedKey&&activePreparedItem?.key===requestedKey)return destinationWithPrepared(activePreparedItem);
        if(requestedKey){
            const item=takeHistoryPrepared(requestedKey);
            if(item){
                if(activePreparedItem&&activePreparedItem.key!==item.key)
                    retainHistoryPrepared(activePreparedItem);
                activePreparedItem=item;
                activeTargetKey=item.key;
                if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
                return destinationWithPrepared(item);
            }
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

    function takeNextChandraTestDestination(excludeName=''){
        if(!chandraTestOverrideActive||!chandraTestQueue.length){chandraTestOverrideActive=false;return null}
        const excluded=String(excludeName||'').trim().toLowerCase();
        let index=chandraTestQueue.findIndex(item=>String(item?.name||'').trim().toLowerCase()!==excluded);
        if(index<0)index=0;
        const [destination]=chandraTestQueue.splice(index,1);
        if(!chandraTestQueue.length)chandraTestOverrideActive=false;
        return destination||null;
    }

    function randomGalaxyProvider({excludeName}={}){
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
            const chandraRequested=takeNextChandraTestDestination(excludeName);
            if(chandraRequested){
                destination=consumeReady(chandraRequested,excludeName);
                if(!destination)destination=setUnpreparedActive(chandraRequested);
            }else{
                destination=consumeReady(null,excludeName);
                if(!destination){
                    const requested=galaxyCatalog[Math.floor(Math.random()*galaxyCatalog.length)];
                    destination=setUnpreparedActive(requested);
                }
            }
        }
        activeTargetKey=destinationKey(destination);
        return destination;
    }

    function getRandomNavigationState(){
        const state=randomNavigationWindow.getState();
        return Object.freeze({
            futureTarget:state.futureTarget,
            historyTarget:state.historyTarget,
            hotTarget:state.hotTarget,
            futureCount:state.futureCount,
            historyCount:state.historyCount,
            hotCount:state.hotKeys.length,
            hotKeys:Object.freeze([...state.hotKeys]),
            currentKey:destinationKey(state.current),
            lockedKey:destinationKey(state.locked?.destination||state.locked),
            nextKey:destinationKey(state.next?.destination||state.next),
            forwardCount:state.forwardCount,
            pendingKind:String(state.pending?.kind||'')
        });
    }

    function getPrefetchState(){
        return Object.freeze({
            targetReady:PREFETCH_TARGET,
            maxWorkers:PREFETCH_MAX_WORKERS,
            readyCount:prefetchReady.length,
            loadingCount:prefetchLoading.size,
            queuedCount:prefetchQueued.length,
            pipelineCount:prefetchReady.length+prefetchLoading.size+prefetchQueued.length,
            failedCount:prefetchFailedCount,
            activeDownloadKeys:Object.freeze([...prefetchLoading.keys()]),
            activePreparedGalaxy:activePreparedItem?.destination?.name||'',
            activePreparedSource:activePreparedItem?.sourceKind||'',
            readyDestinations:prefetchReady.map(item=>item.destination.name),
            queuedDestinations:prefetchQueued.map(item=>item.name),
            health:lastPrefetchHealth,
            downloads:getDownloadStatus()
        });
    }

    function getAladinPrewarmState(){
        return Object.freeze({
            targetReady:PREFETCH_TARGET,
            cachedCount:aladinPrewarmedKeys.size,
            activeKey:aladinPrewarmActiveKey,
            queuedDestinations:[]
        });
    }

    // ==================== VIEWER STARTUP / SCRIPT LOADING ====================
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
            script.charset='utf-8';
            script.dataset[datasetKey]='true';
            if(url.startsWith('https://raw.githubusercontent.com/')){
                fetch(url,{cache:'no-store'}).then(response=>{
                    if(!response.ok)throw new Error('SCRIPT FETCH RETURNED HTTP '+response.status+': '+url);
                    return response.text();
                }).then(source=>{
                    script.textContent=source;
                    document.head.appendChild(script);
                    script.dataset.gvLoaded='true';
                    resolve(script);
                }).catch(error=>reject(new Error('SCRIPT FAILED TO LOAD: '+url+' — '+String(error?.message||error))));
                return;
            }
            script.src=url;
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
        random.id='gv-random-galaxy';random.type='button';random.innerHTML='<span class="gvrg-random-layout"><span class="gvrg-random-star-wrap gvrg-random-star-wrap-left" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet gvrg-random-comet-left"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span><span class="gvrg-random-label">RANDOM GALAXY</span><span class="gvrg-random-star-wrap gvrg-random-star-wrap-right" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span></span>';random.setAttribute('aria-label','RANDOM GALAXY');
        const forward=document.createElement('button');
        forward.type='button';forward.className='gv-galaxy-history gv-galaxy-history-forward';forward.textContent='';forward.setAttribute('aria-label','NEXT GALAXY');forward.disabled=true;
        nav.append(back,random,forward);root.appendChild(nav);

        const hud=document.createElement('div');
        hud.id='gv-travel-hud';hud.setAttribute('role','status');hud.setAttribute('aria-live','polite');
        hud.innerHTML='<div id="gv-travel-distance"><span id="gv-travel-distance-value"><span id="gv-travel-distance-integer">0</span><span id="gv-travel-distance-decimal">.</span><span id="gv-travel-distance-fraction">00</span></span><span id="gv-travel-distance-unit">MILLION LIGHT-YEARS</span></div><div id="gv-travel-primary"><div id="gv-travel-course">COURSE LOCKED</div><div id="gv-travel-heading">HEADING TO</div><div id="gv-travel-destination"></div></div>';
        root.appendChild(hud);
        return {version,nav,back,random,forward,hud};
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
        }catch(error){console.warn('GALAXY VIEWER GETRADEC WARNING',error)}
        try{
            const canvas=root.querySelector('canvas');
            if(canvas&&typeof aladin.pix2world==='function'){
                const value=aladin.pix2world(canvas.clientWidth/2,canvas.clientHeight/2);
                const ra=Number(value?.[0]),dec=Number(value?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
            }
        }catch(error){console.warn('GALAXY VIEWER PIX2WORLD WARNING',error)}
        return null;
    }

    const galaxyCatalogPromise=loadCombinedGalaxyCatalog();
    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0002'),
        loadScript(COORDINATE_URL,'gvCoordinate0004'),
        loadScript(TARGET_URL,'gvTarget0001'),
        loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0034')
    ]);
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('GALAXY VIEWER ROOT MISSING');
    const startupWait=document.getElementById('gv-startup-wait');
    document.dispatchEvent(new CustomEvent('gv-viewer-startup-visible',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:performance.now()-startupTiming.startedAt}}));

    const A=await ensureAladin();
    await A.init;

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

    // Generic Aladin physical field scale.  Random Galaxy supplies the
    // current destination distance, but the ruler belongs to viewer
    // presentation because it follows the live Aladin FOV.
    const skyPhysicalScale=document.createElement('div');
    skyPhysicalScale.id='gv-sky-physical-scale';
    skyPhysicalScale.setAttribute('aria-hidden','true');

    const skyPhysicalScaleLabel=document.createElement('div');
    skyPhysicalScaleLabel.className='gv-sky-scale-label';

    const skyPhysicalScaleLine=document.createElement('div');
    skyPhysicalScaleLine.className='gv-sky-scale-line';

    skyPhysicalScale.append(skyPhysicalScaleLabel,skyPhysicalScaleLine);
    root.appendChild(skyPhysicalScale);

    const skyPhysicalScaleStyle=document.createElement('style');
    skyPhysicalScaleStyle.textContent=
        '#gv-sky-physical-scale{position:absolute;left:50%;z-index:28;transform:translateX(-50%);display:none;flex-direction:column;align-items:center;gap:4px;pointer-events:none;color:#FFD85A;font:400 9px/1.05 "Space Age",sans-serif;letter-spacing:.7px;text-align:center;text-shadow:0 0 3px rgba(255,242,168,.72),0 0 7px rgba(255,180,45,.28);white-space:nowrap}' +
        '#gv-sky-physical-scale .gv-sky-scale-label{font:400 9px/1.05 "Space Age",sans-serif;color:#FFD85A;letter-spacing:.7px;text-shadow:0 0 3px rgba(255,242,168,.72),0 0 7px rgba(255,180,45,.28)}' +
        '#gv-sky-physical-scale .gv-sky-scale-line{position:relative;height:10px;border-top:1px solid #FFD85A;filter:drop-shadow(0 0 2px rgba(255,216,90,.52))}' +
        '#gv-sky-physical-scale .gv-sky-scale-line::before,#gv-sky-physical-scale .gv-sky-scale-line::after{content:"";position:absolute;top:-5px;width:1px;height:9px;background:#FFD85A;box-shadow:0 0 2px rgba(255,216,90,.48)}' +
        '#gv-sky-physical-scale .gv-sky-scale-line::before{left:0}' +
        '#gv-sky-physical-scale .gv-sky-scale-line::after{right:0}';
    document.head.appendChild(skyPhysicalScaleStyle);

    startupWait?.remove();
    startupTiming.shellReadyAt=performance.now();
    document.dispatchEvent(new CustomEvent('gv-viewer-shell-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:startupTiming.shellReadyAt-startupTiming.startedAt}}));

    await moduleLoads;

    // HOME / observable-universe presentation is owned by Random Galaxy
    // 0034, but must appear before the catalog wait.
    if(
        window.GalaxyRandomGalaxy?.VERSION!=='0034' ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error('RANDOM GALAXY 0034 HOME BOOTSTRAP EXPORT MISSING');

    window.GalaxyRandomGalaxy.bootstrapHomePresentation(root);

    // ==================== HAMBURGER MENU ====================
    if(window.GalaxyViewerHamburgerMenu?.version!=='0002')throw new Error('HAMBURGER MODULE 0002 EXPORT MISSING');
    const hamburger=window.GalaxyViewerHamburgerMenu.init({
        host:hamburgerHost,
        onProjectionSelected(name,detail){
            try{
                if(typeof aladin.setProjection!=='function')throw new Error('ALADIN setProjection IS UNAVAILABLE');
                aladin.setProjection(detail.code);
            }catch(error){console.error('GALAXY VIEWER PROJECTION FAILURE',name,detail?.code,error)}
        }
    });
    hamburger.root.style.position='absolute';
    hamburger.root.style.inset='0';
    hamburger.root.style.width='100%';
    hamburger.root.style.height='100%';
    hamburger.root.style.pointerEvents='none';
    hamburger.menuButton.style.pointerEvents='auto';

    // ==================== COORDINATE BOX / NAVIGATION INSTRUMENTS ====================
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
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
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

    // ==================== TARGET / SIMBAD ====================
    if(window.GalaxyViewerTargetSimbad?.version!=='0001')throw new Error('TARGET / SIMBAD MODULE 0001 EXPORT MISSING');
    const target=window.GalaxyViewerTargetSimbad.init({host:targetHost,aladin,viewerRoot:root});
    const targetButtonIcon=target.button?.querySelector('img');
    if(targetButtonIcon)targetButtonIcon.src=TARGET_ICON_URL;

    galaxyCatalog=await galaxyCatalogPromise;
    startupTiming.catalogReadyAt=performance.now();

    // ==================== RANDOM NAVIGATION ====================
    if(window.GalaxyRandomGalaxy?.VERSION!=='0034')throw new Error('RANDOM GALAXY 0034 EXPORT MISSING OR VERSION MISMATCH');
    if(typeof window.GalaxyRandomNavigationWindow!=='function')throw new Error('RANDOM GALAXY 0034 NAVIGATION WINDOW EXPORT MISSING');
    const randomNavigationWindow=new window.GalaxyRandomNavigationWindow({
        futureTarget:10,
        historyTarget:10,
        hotTarget:5,
        keyOf:destination=>destinationKey(destination)
    });
    randomNavigationWindow.setCurrent(HOME);

    function historySnapshot(destination){
        const {preparedHdUrl,preparedSource,preparedHdImage,...snapshot}=destination||{};
        return Object.freeze({...snapshot});
    }
    function setHistoryControls(){
        const busy=navigationPending||Boolean(window.GalaxyViewerRandomGalaxy?.getState?.().busy);
        bottom.back.disabled=busy||!randomNavigationWindow.canBack();
        bottom.forward.disabled=busy||!randomNavigationWindow.canForward();
    }
    let earthReturnApi=Object.freeze({
        hide(){},
        show(_destination){}
    });

    const hideEarthReturnIndicator=()=>earthReturnApi.hide();
    const showEarthReturnIndicator=destination=>earthReturnApi.show(destination);

    let skyPhysicalScaleValue=null;
    let skyPhysicalScaleFrame=0;
    let skyPhysicalScaleLastUpdate=0;

    const formatPhysicalScale=valueLy=>{
        const ly=Number(valueLy);
        if(!Number.isFinite(ly)||ly<=0)return '';

        let divisor=1000,unit='KLY';
        if(ly>=1_000_000_000){divisor=1_000_000_000;unit='BLY'}
        else if(ly>=1_000_000){divisor=1_000_000;unit='MLY'}

        const value=ly/divisor;
        let digits;
        if(value>=100)digits=Math.round(value).toString();
        else if(value>=10)digits=(Math.round(value*10)/10).toString();
        else if(value>=1)digits=(Math.round(value*10)/10).toString();
        else if(value>=0.1)digits=(Math.round(value*100)/100).toString();
        else digits=(Math.round(value*1000)/1000).toString();

        return `${digits} ${unit}`;
    };

    const choosePhysicalScaleValue=(lyPerPx,usableWidth)=>{
        const targetFraction=.40;
        const targetLy=Number(lyPerPx)*Number(usableWidth)*targetFraction;
        if(!(targetLy>0))return null;

        const exponent=Math.floor(Math.log10(targetLy));
        const candidates=[];
        for(let e=exponent-2;e<=exponent+2;e++)
            for(const m of [1,2,5])
                candidates.push(m*Math.pow(10,e));

        const scored=candidates.map(value=>{
            const fraction=(value/lyPerPx)/usableWidth;
            const inBand=fraction>=.30&&fraction<=.50;
            return {
                value,
                score:Math.abs(fraction-targetFraction)+(inBand?0:10)
            };
        }).sort((a,b)=>a.score-b.score);

        return scored.length?scored[0].value:null;
    };

    const hideSkyPhysicalScale=()=>{
        skyPhysicalScale.style.display='none';
        skyPhysicalScale.setAttribute('aria-hidden','true');
        skyPhysicalScaleValue=null;
    };

    const updateSkyPhysicalScale=now=>{
        skyPhysicalScaleFrame=requestAnimationFrame(updateSkyPhysicalScale);

        // Ten updates per second is plenty for a scale ruler and prevents
        // unnecessary layout churn while Aladin is animating.
        if(Number(now)-skyPhysicalScaleLastUpdate<100)return;
        skyPhysicalScaleLastUpdate=Number(now);

        if(navigationPending){
            hideSkyPhysicalScale();
            return;
        }

        const state=randomNavigationWindow?.getState?.()||{};
        const destination=state.current||null;
        const distanceMly=Number(destination?.distance);

        const card=document.querySelector('#gv-random-galaxy .gvrg-card');
        const cardVisible=Boolean(card?.classList?.contains('gvrg-card-visible'));
        if(!cardVisible||!Number.isFinite(distanceMly)||distanceMly<=0){
            hideSkyPhysicalScale();
            return;
        }

        const rootRect=root.getBoundingClientRect();
        const cardRect=card.getBoundingClientRect();
        const usableWidth=Math.min(680,Math.max(40,rootRect.width-20));

        let fovDegrees=NaN;
        try{
            const fov=aladin.getFov?.();
            fovDegrees=Number(Array.isArray(fov)?fov[0]:fov);
        }catch(_){}

        if(!Number.isFinite(fovDegrees)||fovDegrees<=0){
            hideSkyPhysicalScale();
            return;
        }

        // Approximate transverse physical width of the live Aladin field.
        // Arrival/normal galaxy views are well inside the useful range;
        // clamp only pathological ultra-wide manual zoom-outs.
        const boundedFov=Math.min(170,Math.max(.000001,fovDegrees));
        const angleRadians=boundedFov*Math.PI/180;
        const distanceLy=distanceMly*1_000_000;
        const physicalViewportLy=2*distanceLy*Math.tan(angleRadians/2);

        if(!Number.isFinite(physicalViewportLy)||physicalViewportLy<=0){
            hideSkyPhysicalScale();
            return;
        }

        const lyPerPx=physicalViewportLy/usableWidth;
        if(!Number.isFinite(lyPerPx)||lyPerPx<=0){
            hideSkyPhysicalScale();
            return;
        }

        let widthPx=skyPhysicalScaleValue>0
            ? skyPhysicalScaleValue/lyPerPx
            : 0;
        let fraction=widthPx/usableWidth;

        // Wider hysteresis than the normal target band prevents rapid
        // label switching near a pinch-zoom threshold.
        if(!(skyPhysicalScaleValue>0)||fraction<.27||fraction>.53){
            skyPhysicalScaleValue=choosePhysicalScaleValue(lyPerPx,usableWidth);
            widthPx=skyPhysicalScaleValue>0
                ? skyPhysicalScaleValue/lyPerPx
                : 0;
        }

        if(!(skyPhysicalScaleValue>0)||!(widthPx>0)){
            hideSkyPhysicalScale();
            return;
        }

        // Hard 50% ruler maximum regardless of transient zoom geometry.
        const hardMaxPx=usableWidth*.50;
        skyPhysicalScaleLine.style.width=
            `${Math.max(4,Math.min(hardMaxPx,widthPx))}px`;

        skyPhysicalScaleLabel.textContent=
            formatPhysicalScale(skyPhysicalScaleValue);

        if(!skyPhysicalScaleLabel.textContent){
            hideSkyPhysicalScale();
            return;
        }

        skyPhysicalScale.style.display='flex';
        skyPhysicalScale.setAttribute('aria-hidden','false');

        // Entire ruler sits above the Random Galaxy / View-HD card.
        const bottomGap=Math.max(6,rootRect.bottom-cardRect.top+6);
        skyPhysicalScale.style.bottom=`${bottomGap}px`;
    };

    skyPhysicalScaleFrame=requestAnimationFrame(updateSkyPhysicalScale);

function navigateHistory(direction){
        if(navigationPending||randomGalaxy.getState().busy)return;

        const historyDestination=
            direction==='back'
                ? randomNavigationWindow.lockHistoryBack()
                : direction==='forward'
                    ? randomNavigationWindow.lockHistoryForward()
                    : null;

        if(!historyDestination)return;

        // 0034 now owns the history transaction. forcedDestination is only
        // the shell/provider transport for the already-locked destination.
        forcedDestination=historyDestination;
        navigationPending=true;

        suspendBackgroundWork();
        suspendArchivePreloads();
        releaseActiveArchivePreload();

        hideEarthReturnIndicator();
        setHistoryControls();

        randomGalaxy.travelToRandom().catch(error=>{
            randomNavigationWindow.rollbackPending();
            forcedDestination=null;
            navigationPending=false;
            hideEarthReturnIndicator();
            resumeBackgroundWork();
            resumeArchivePreloads();
            
            setHistoryControls();
            console.error('GALAXY VIEWER HISTORY NAVIGATION FAILURE',error);
        });
    }

    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{
        aladin,
        viewerRoot:root,
        earthReturnOptions:Object.freeze({
            home:HOME,
            hamburgerHost,
            coordinateHost,
            targetHost,
            nav:bottom.nav,
            skyPhysicalScale,
            isNavigationPending:()=>navigationPending
        }),
        randomButton:bottom.random,
        bindClick:false,
        prefetch:false,
        provider:randomGalaxyProvider,
        currentGalaxy:HOME,
        catalogCount:catalogRecordCount,
        travelSeconds:TRAVEL_SECONDS,
        firstHomeTravelSeconds:FIRST_HOME_TRAVEL_SECONDS,
        maxFov:297,
        turnPoint:0.4705882353,
        onArrival(destination){
            navigationPending=false;
            
            showEarthReturnIndicator(destination);
            if(randomNavigationWindow.getState().pending)
                randomNavigationWindow.commitPending(destination);
            else
                randomNavigationWindow.setCurrent(destination);
            enforceHotPreparedWindow();
            syncHdProviderPresentation(destination);
            setHistoryControls();
            resumeBackgroundWork();
            
            resumeArchivePreloads();
            // 0034 owns Random Galaxy Aladin arrival validation/recovery.
        },
        onError(error){
            randomNavigationWindow.rollbackPending();
            navigationPending=false;forcedDestination=null;hideEarthReturnIndicator();setHistoryControls();resumeBackgroundWork();resumeArchivePreloads();console.error('GALAXY VIEWER RANDOM GALAXY FAILURE',error);
        }
    });
    window.GalaxyViewerRandomGalaxy=randomGalaxy;

    earthReturnApi=Object.freeze({
        hide:()=>randomGalaxy.hideEarthReturn(),
        show:destination=>randomGalaxy.showEarthReturn(destination)
    });


    hdArchiveIntegration=randomGalaxy.installHdArchiveIntegration({
        bottom,
        targetIconUrl:TARGET_ICON_URL,
        hdLayout:HD_LAYOUT,
        getPrefetchReady:()=>prefetchReady,
        isBackgroundWorkSuspended:()=>backgroundWorkSuspended,
        isNavigationPending:()=>navigationPending,
        getActiveTargetKey:()=>activeTargetKey,
        onSetHistoryControls:()=>setHistoryControls(),
        onHideEarthReturn:()=>hideEarthReturnIndicator()
    });

    ensureArchivePreloadQueue=
        ()=>hdArchiveIntegration.ensureArchivePreloadQueue();

    suspendArchivePreloads=
        ()=>hdArchiveIntegration.suspendArchivePreloads();

    resumeArchivePreloads=
        ()=>hdArchiveIntegration.resumeArchivePreloads();

    releaseActiveArchivePreload=
        ()=>hdArchiveIntegration.releaseActiveArchivePreload();

    syncHdProviderPresentation=
        destination=>hdArchiveIntegration.syncHdProviderPresentation(destination);

    // Do not let optional Random Galaxy font/calibration initialization
    // prevent the physical Random button from becoming operational.
    // travelToRandom() awaits randomGalaxy.ready internally, so replace that
    // gate with the already-mounted instance while the original initialization
    // continues independently.
    const randomGalaxyInitialization=randomGalaxy.ready;
    randomGalaxy.ready=Promise.resolve(randomGalaxy);
    startupTiming.randomReadyAt=performance.now();
    bottom.random.disabled=false;
    fillPrefetchQueue();
    randomGalaxyInitialization.catch(error=>console.warn(
        "GALAXY VIEWER RANDOM GALAXY OPTIONAL INITIALIZATION WARNING",error
    ));
    const launchRandomGalaxy=()=>{
        if(navigationPending||randomGalaxy.getState().busy)return;

        reconcileFutureQueue();

        const nextReady=randomNavigationWindow.isNextReady(bundle=>{
            const destination=bundle?.destination||bundle;
            const key=destinationKey(destination);
            return key===String(bundle?.key||key).trim().toLowerCase()&&
                core.isHdPrepared?.(key)&&
                window.GalaxyViewerPrefetch?.hasReadyNavigation?.();
        });

        if(!nextReady){
            fillPrefetchQueue();
            return;
        }

        forceAladinRepaint();
        navigationPending=true;
        hideEarthReturnIndicator();
        setHistoryControls();

        randomGalaxy.travelToRandom().then(destination=>{
            if(destination){
                const hud=document.getElementById('gv-travel-hud');
                if(!hud)console.error('GALAXY VIEWER TRAVEL HUD MISSING');
            }
        }).catch(error=>{
            randomNavigationWindow.rollbackPending();
            navigationPending=false;
            forcedDestination=null;
            hideEarthReturnIndicator();
            
            setHistoryControls();
            resumeBackgroundWork();
            resumeArchivePreloads();
            console.error('GALAXY VIEWER RANDOM GALAXY CLICK FAILURE',error);
        });
    };
    bottom.random.addEventListener('click',launchRandomGalaxy);


    window.addEventListener('beforeunload',()=>{
        for(const controller of prefetchControllers.values())controller.abort();
        prefetchControllers.clear();
        if(prefetchRetryTimer)clearTimeout(prefetchRetryTimer);
        if(prefetchHealthTimer)clearInterval(prefetchHealthTimer);
        if(aladinPrewarmTimer)clearTimeout(aladinPrewarmTimer);
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        releasePreparedItem(activePreparedItem);historyPreparedItems.splice(0).forEach(releasePreparedItem);prefetchReady.splice(0).forEach(releasePreparedItem);
        prefetchQueued.splice(0);
        try{aladinPrewarmHost?.remove()}catch(_){}
    },{once:true});
    bottom.back.addEventListener('click',()=>navigateHistory('back'));
    bottom.forward.addEventListener('click',()=>navigateHistory('forward'));
    setHistoryControls();
    startupTiming.fullReadyAt=performance.now();
    const startupMetrics=Object.freeze({...startupTiming,shellMs:startupTiming.shellReadyAt-startupTiming.startedAt,catalogMs:startupTiming.catalogReadyAt-startupTiming.startedAt,randomMs:startupTiming.randomReadyAt-startupTiming.startedAt,fullMs:startupTiming.fullReadyAt-startupTiming.startedAt});
    window.GalaxyViewerCore=Object.freeze({version:VERSION,displayVersion:DISPLAY_VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomNavigationWindow,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,catalogDatabaseCounts,startupMetrics,getPrefetchState,getRandomNavigationState,getDownloadStatus,getAladinPrewarmState,fillPrefetchQueue,getGalaxyCatalog:()=>Object.freeze([...galaxyCatalog]),activateQueuedDestination:(destination,excludeName='')=>consumeReady(destination,excludeName)||setUnpreparedActive(destination),requestHdPrefetch:destination=>{if(!destination)return '';enqueuePrefetch(destination,true);fillPrefetchQueue();return destinationKey(destination)},getHdPreparedResource:key=>{const normalized=String(key||'').trim().toLowerCase();return activePreparedItem?.key===normalized?activePreparedItem:prefetchReady.find(item=>item?.key===normalized)||historyPreparedItems.find(item=>item?.key===normalized)||null},isHdPrepared:key=>{const normalized=String(key||'').trim().toLowerCase();return Boolean(activePreparedItem?.key===normalized||prefetchReady.some(item=>item?.key===normalized)||historyPreparedItems.some(item=>item?.key===normalized))},getAladinPreparedReceipt:key=>aladinPreparedReceipts.get(String(key||'').trim().toLowerCase())||null,isAladinPrepared:key=>{
        const normalized=String(key||'').trim().toLowerCase();
        if(aladinPrewarmUnavailable)return true;
        return Boolean(normalized&&aladinPreparedReceipts.has(normalized));
    },ensureAladinPreparedForNavigation:async destination=>{
        const key=destinationKey(destination);
        if(!key)return null;
        const existing=aladinPreparedReceipts.get(key)||null;
        if(aladinPrewarmUnavailable)return existing||Object.freeze({
            key,
            ra:Number(destination.ra),
            dec:Number(destination.dec),
            fov:Number(destination.fov),
            rotation:Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):0,
            projection:'SIN',
            preparedAt:Date.now(),
            unavailable:true
        });
        if(existing&&aladinPrewarm&&aladinPrewarmHost&&aladinPrewarmLastKey===key)return existing;
        return await prepareAladinDestination(destination,true);
    },getBackgroundWorkSuspended:()=>backgroundWorkSuspended,suspendBackgroundWork,resumeBackgroundWork,suspendArchivePreloads,resumeArchivePreloads,getChandraTestOverrideState:()=>Object.freeze({chandraTestOverrideActive,chandraTestRemaining:chandraTestQueue.length,chandraTestTotal}),getGalaxyHistory:()=>{const state=randomNavigationWindow.getState();const items=[...state.history,state.current,...[...state.forwardHistory].reverse()].filter(Boolean);return {index:state.history.length,items:items.map(item=>({name:item.name,archiveId:item.archiveId,provider:providerFor(item)}))}}});
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,startupMetrics}}));
})().catch(error=>{console.error('GALAXY VIEWER STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});
"""))

# Galaxy Viewer active implementation staged
