from IPython.display import HTML, Javascript, display

# GV-beta-0010Q
# Standalone release derived directly from the exact GV-beta-0010K baseline.
# Authorized 10L changes only: restore the compact Hubble/JWST archive-source icon footprint;
# keep that source control lower-right inside the HD image; put the Galaxy Viewer target SVG
# inside its own square return-control tile; preserve BACK TO SKY; and make Galaxy Info use
# full width until its text reaches the actual lower-right BACK TO SKY button rectangle.

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
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:#E8FFF0;font:400 15.5px/1 "Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 4px rgba(229,255,239,.76);box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
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
<script>(()=>{const cover=document.getElementById('gv-apk-cover');if(!cover)return;const img=cover.querySelector('img');if(img)img.src='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/icon_target_vector.svg';const version=document.createElement('div');version.className='gv-10e-version';version.textContent='VERSION 10Q';cover.appendChild(version)})();</script>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='10Q';
    const DISPLAY_VERSION='10Q';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=28d4acb0b724e2c9ec9764f4f3ce92ee1e3210a5';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0004.js?v=5c323a13b92f146426b45c047fc716b599494f3a';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=7b877f841f091f214d844bdc8ae2f933530f4592';
    const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/559dfd10c0c3dafa7f7a5c3f7fe2c76337f26066/viewer/modules/gv-random-galaxy-0031.js?v=4abd2d76e717c0f4abbb61777154b7db14f49cf8';
    const Hubble_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0018.json';
    const JWST_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json';
    const TRAVEL_SECONDS=18;
    const HOME=Object.freeze({name:'MILKY WAY',ra:266.4051,dec:-28.936175,distance:0,constellation:'Sagittarius',designation:'MILKY WAY',commonName:'Milky Way',age:'13.6 billion years',ageYears:13.6e9,physicalSizeLy:100000,fov:360,hdUrl:'',sourceUrl:'',orientation:'',credit:'',imageType:'Observation',category:'Galaxies'});
    const HUBBLE_PREFETCH_TARGET=10;
    const HUBBLE_PREFETCH_RETRY_MS=12000;
    const PREFETCH_MAX_WORKERS=3;
    const PREFETCH_HEALTH_INTERVAL_MS=30000;
    const ALADIN_PREWARM_DWELL_MS=900;
    const ALADIN_PREWARM_SAMPLE_MS=140;
    const FRAMING_SAMPLE_SIZE=128;
    const FRAMING_MAX_SHIFT_FRACTION=.26;
    const HD_PREFERRED_MAX_BYTES=1048576;
    const HD_PROBE_MAX_WORKERS=4;
    const Hubble_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble-ESA-icon-BW.svg';
    const JWST_ICON_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/JWST/esa-jwst-logo.png?v=7169a77e4b56dc582f9b0fb0b76bf389bcf337ce';
    const TARGET_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/icon_target_vector.svg';
    const ARRIVAL_OCCUPANCY=Object.freeze({target:.28,minFov:.03,maxFov:12});
    let galaxyCatalog=[],catalogRecordCount=0,catalogDatabaseCounts=Object.freeze({hubble:0,jwst:0,total:0,eligibleHubble:0,eligibleJwst:0,eligibleTotal:0});
    let activePreparedItem=null,historyPreparedItem=null,activeTargetKey='',priorityPrefetchDestination=null;
    let prefetchReady=[],prefetchQueued=[],prefetchLoading=new Map(),prefetchControllers=new Map(),prefetchRetryAfter=new Map(),prefetchRetryTimer=0,prefetchFailedCount=0,prefetchHealthTimer=0,lastPrefetchHealth=null;
    let hdDownloadStatus=new Map(),backgroundWorkSuspended=false;
    let aladinPrewarm=null,aladinPrewarmReady=null,aladinPrewarmHost=null,aladinPrewarmTimer=0,aladinPrewarmWaitResolve=null,aladinPrewarmActiveKey='',aladinPrewarmLastKey='',aladinPrefetchSerial=Promise.resolve(),aladinPrewarmedKeys=new Set();
    let galaxyHistory=[],galaxyHistoryIndex=-1,pendingHistoryIndex=null,forcedDestination=null,navigationPending=false,travelHudFrame=0;

    const approvedHost=host=>host==='cdn.spacetelescope.org'||host==='cdn.esahubble.org'||host==='cdn.esawebb.org'||host==='raw.githubusercontent.com';
    const json=async url=>{const response=await fetch(url,{cache:'no-store'});if(!response.ok)throw new Error(`HTTP ${response.status} ${url}`);return response.json()};
    const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
    const clamp=(value,min,max)=>Math.max(min,Math.min(max,value));
    const smootherstep=t=>{const x=clamp(t,0,1);return x*x*x*(x*(x*6-15)+10)};
    const createHost=(parent,id)=>{const host=document.createElement('div');host.id=id;parent.appendChild(host);return host};
    const loadScript=(src,key)=>new Promise((resolve,reject)=>{if(key&&window[key]){resolve(window[key]);return}const script=document.createElement('script');script.src=src;script.async=true;script.onload=()=>resolve(window[key]);script.onerror=()=>reject(new Error(`SCRIPT LOAD FAILED: ${src}`));document.head.appendChild(script)});
    const ensureAladin=()=>new Promise((resolve,reject)=>{if(window.A?.init){resolve(window.A);return}const script=document.createElement('script');script.src=ALADIN_URL;script.async=true;script.onload=()=>resolve(window.A);script.onerror=()=>reject(new Error('ALADIN LOAD FAILED'));document.head.appendChild(script)});

    function createCenterReticle(root){
        const div=document.createElement('div');div.id='gv-center-reticle';
        const img=document.createElement('img');img.src=TARGET_ICON_URL;img.alt='CENTER TARGET';div.appendChild(img);root.appendChild(div);return div;
    }
    function createBottomControls(root){
        const nav=document.createElement('div');nav.id='gv-galaxy-nav';
        const back=document.createElement('button');back.type='button';back.className='gv-galaxy-history gv-galaxy-history-back';back.setAttribute('aria-label','PREVIOUS GALAXY');back.disabled=true;
        const random=document.createElement('button');random.type='button';random.id='gv-random-galaxy';random.textContent='RANDOM GALAXY';
        const forward=document.createElement('button');forward.type='button';forward.className='gv-galaxy-history gv-galaxy-history-forward';forward.setAttribute('aria-label','NEXT GALAXY');forward.disabled=true;
        nav.append(back,random,forward);root.appendChild(nav);
        const version=document.createElement('div');version.id='gv-version-label';version.textContent=`VERSION ${DISPLAY_VERSION}`;root.appendChild(version);
        return {nav,back,random,forward,version};
    }
    function createUniverseContext(root){
        const wrap=document.createElement('div');wrap.id='gv-universe-context';
        const label=document.createElement('div');label.className='gv-universe-label';label.innerHTML='OBSERVABLE UNIVERSE<span class="gv-universe-count">ABOUT 2 TRILLION GALAXIES</span>';
        const leader=document.createElement('div');leader.className='gv-universe-leader';wrap.append(label,leader);root.appendChild(wrap);return wrap;
    }
    function createHomeOverlay(root){
        const wrap=document.createElement('div');wrap.id='gv-we-are-here';
        const leader=document.createElement('div');leader.className='gv-home-leader';
        const label=document.createElement('div');label.className='gv-home-label';label.innerHTML='<div class="gv-home-origin"><span class="gv-earth-icon">🌎</span><span>WE ARE HERE</span></div><div class="gv-home-sub">MILKY WAY</div><div class="gv-home-hint">CLICK RANDOM GALAXY TO NAVIGATE</div>';
        wrap.append(leader,label);root.appendChild(wrap);return wrap;
    }

    function parseArchiveOrientation(value){
        const text=String(value||'').trim();if(!text)return null;
        const numeric=text.match(/(?:orientation|rotation|position angle|pa)[^+\-\d]*([+\-]?\d+(?:\.\d+)?)/i)||text.match(/^\s*([+\-]?\d+(?:\.\d+)?)\s*(?:deg|degrees?|°)?\s*$/i);
        if(!numeric)return null;
        const angle=Number(numeric[1]);return Number.isFinite(angle)?angle:null;
    }
    function parseFieldOfView(value){
        const text=String(value||'').toLowerCase();if(!text)return null;
        const values=[...text.matchAll(/([0-9]+(?:\.[0-9]+)?)\s*(arcsec|arcmin|degrees?|deg|°)/g)].map(match=>{const number=Number(match[1]);const unit=match[2];if(!Number.isFinite(number)||number<=0)return null;if(unit==='arcsec')return number/3600;if(unit==='arcmin')return number/60;return number}).filter(Number.isFinite);
        if(!values.length)return null;return Math.max(...values);
    }
    function parsePhysicalSizeLy(value){
        if(Array.isArray(value)){const v=value.map(Number).filter(n=>Number.isFinite(n)&&n>0);return v.length?v:null}
        if(Number.isFinite(Number(value))&&Number(value)>0)return Number(value);
        const text=String(value||'').toLowerCase();if(!text)return null;
        const values=[...text.matchAll(/([0-9]+(?:\.[0-9]+)?)\s*(?:x\s*([0-9]+(?:\.[0-9]+)?)\s*)?(million\s+)?light[\s-]*years?/g)].flatMap(match=>{const scale=match[3]?1e6:1;const a=Number(match[1])*scale,b=match[2]?Number(match[2])*scale:null;return Number.isFinite(b)?[a,b]:[a]}).filter(n=>Number.isFinite(n)&&n>0);return values.length?values:null;
    }
    function destinationFromHubble(candidate,index){
        const name=String(candidate.commonName||candidate.designation||candidate.name||`HUBBLE GALAXY ${index+1}`).trim();
        const designation=String(candidate.designation||candidate.name||name).trim();
        const commonName=String(candidate.commonName||candidate.pseudonym||name).trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec),distance=Number(candidate.distance),ageYears=Number(candidate.ageYears);
        const age=String(candidate.age||'').trim(),constellation=String(candidate.constellation||'').trim();
        const fieldDegrees=parseFieldOfView(candidate.fieldOfView||candidate.imageFieldOfView||candidate.fov);
        if(!Number.isFinite(ra)||!Number.isFinite(dec)||!Number.isFinite(distance)||distance<=0||!fieldDegrees)return null;
        let hd,source;try{hd=new URL(String(candidate.selectedImageUrl||candidate.hdUrl||''));source=new URL(String(candidate.sourceUrl||''))}catch(_){return null}
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        const fov=clamp(fieldDegrees/ARRIVAL_OCCUPANCY.target,ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov);
        return Object.freeze({
            source:'ESA/HUBBLE GALAXIES CATALOG FULL-0002',provider:'HUBBLE',hubble:true,
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy:Array.isArray(physicalSizeLy)?physicalSizeLy.filter(value=>Number.isFinite(value)&&value>0):Number.isFinite(physicalSizeLy)&&physicalSizeLy>0?physicalSizeLy:null,
            fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,orientation:String(candidate.orientation||'').trim(),
            credit:String(candidate.credit||'ESA/Hubble').trim()||'ESA/Hubble',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'Hubble Space Telescope',
            githubImageUrl:'',sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }
    function destinationFromJwst(candidate,index){
        const name=String(candidate.commonName||candidate.designation||candidate.name||`JWST GALAXY ${index+1}`).trim();
        const designation=String(candidate.designation||candidate.name||name).trim();
        const commonName=String(candidate.commonName||candidate.pseudonym||name).trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec),distance=Number(candidate.distance),ageYears=Number(candidate.ageYears);
        const age=String(candidate.age||'').trim(),constellation=String(candidate.constellation||'').trim();
        const fieldDegrees=parseFieldOfView(candidate.fieldOfView||candidate.imageFieldOfView||candidate.fov);
        const physicalSizeLy=parsePhysicalSizeLy(candidate.physicalSizeLy||candidate.size||candidate.diameterLy||candidate.diameter);
        if(!Number.isFinite(ra)||!Number.isFinite(dec)||!Number.isFinite(distance)||distance<=0||!fieldDegrees)return null;
        let hd,source;try{hd=new URL(String(candidate.selectedImageUrl||candidate.hdUrl||''));source=new URL(String(candidate.sourceUrl||''))}catch(_){return null}
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        const fov=clamp(fieldDegrees/ARRIVAL_OCCUPANCY.target,ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov);
        const orientation=String(candidate.orientation||'').trim();
        const archiveRotation=parseArchiveOrientation(orientation);
        return Object.freeze({
            source:'ESA/WEBB GALAXIES CATALOG FULL-0002',provider:'JWST',hubble:true,
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

    async function loadGalaxyCatalog(){
        const [hubbleRaw,jwstRaw]=await Promise.all([json(Hubble_CATALOG_URL),json(JWST_CATALOG_URL)]);
        const hubbleRecords=Array.isArray(hubbleRaw)?hubbleRaw:Array.isArray(hubbleRaw?.records)?hubbleRaw.records:[];
        const jwstRecords=Array.isArray(jwstRaw)?jwstRaw:Array.isArray(jwstRaw?.records)?jwstRaw.records:[];
        const hubble=hubbleRecords.map(destinationFromHubble).filter(Boolean);
        const jwst=jwstRecords.map(destinationFromJwst).filter(Boolean);
        const combined=[...hubble,...jwst];
        catalogRecordCount=combined.length;
        catalogDatabaseCounts=Object.freeze({hubble:hubbleRecords.length,jwst:jwstRecords.length,total:hubbleRecords.length+jwstRecords.length,eligibleHubble:hubble.length,eligibleJwst:jwst.length,eligibleTotal:combined.length});
        console.info('GV-10G CATALOG COUNTS',catalogDatabaseCounts);
        return combined;
    }

    function destinationKey(destination){return String(destination?.archiveId||destination?.name||'').trim().toLowerCase()}
    function chooseGalaxy(catalog,excludeName=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        const available=catalog.filter(item=>item.name.toLowerCase()!==excluded&&destinationKey(item)!==activeTargetKey);
        const pool=available.length?available:catalog;
        return pool[Math.floor(Math.random()*pool.length)];
    }

    async function probeHdSourceBytes(source,signal=null){
        let response=null;
        try{response=await fetch(source.url,{method:'HEAD',cache:'no-store',signal})}catch(_){}
        if(response?.ok){
            const size=Number(response.headers.get('content-length'));
            if(Number.isFinite(size)&&size>0)return size;
        }
        try{
            response=await fetch(source.url,{headers:{Range:'bytes=0-0'},cache:'no-store',signal});
            if(response.ok||response.status===206){
                const range=String(response.headers.get('content-range')||'');
                const match=range.match(/\/(\d+)$/);
                const size=match?Number(match[1]):Number(response.headers.get('content-length'));
                if(Number.isFinite(size)&&size>0)return size;
            }
        }catch(_){}
        return null;
    }

    async function orderHdSourcesBySize(sources,signal=null){
        const probed=new Array(sources.length);let next=0;
        const workers=Array.from({length:Math.min(HD_PROBE_MAX_WORKERS,sources.length)},async()=>{
            for(;;){
                const index=next++;if(index>=sources.length)return;
                let bytes=null;try{bytes=await probeHdSourceBytes(sources[index],signal)}catch(error){if(error?.name==='AbortError')throw error}
                probed[index]={...sources[index],bytes:Number.isFinite(bytes)&&bytes>0?bytes:null};
            }
        });
        await Promise.all(workers);
        const known=probed.filter(source=>Number.isFinite(source.bytes)&&source.bytes>0);
        const preferred=known.filter(source=>source.bytes<=HD_PREFERRED_MAX_BYTES).sort((a,b)=>b.rank-a.rank||b.bytes-a.bytes);
        const oversized=known.filter(source=>source.bytes>HD_PREFERRED_MAX_BYTES).sort((a,b)=>a.bytes-b.bytes||b.rank-a.rank);
        const unknown=probed.filter(source=>!Number.isFinite(source.bytes)).sort((a,b)=>b.rank-a.rank);
        return [...preferred,...oversized,...unknown];
    }

    function hdVariantRank(path){
        if(/publicationjpg/i.test(path))return 70;
        if(/large/i.test(path))return 60;
        if(/screen/i.test(path))return 50;
        if(/wallpaper1/i.test(path))return 40;
        if(/thumb700x/i.test(path))return 30;
        if(/thumb300y/i.test(path))return 20;
        return 45;
    }

    function hdSourceCandidates(destination){
        const sources=[],seen=new Set();
        const add=(url,kind,rank=45)=>{
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

    async function decodePreparedBlob(blob){
        const objectUrl=URL.createObjectURL(blob);
        try{
            const image=new Image();image.decoding='async';image.src=objectUrl;
            if(typeof image.decode==='function')await image.decode();else await new Promise((resolve,reject)=>{image.onload=resolve;image.onerror=reject});
            return {image,objectUrl};
        }catch(error){URL.revokeObjectURL(objectUrl);throw error}
    }

    function setHdStatus(destination,state,sourceKind=''){
        const key=destinationKey(destination);if(!key)return;
        const current=hdDownloadStatus.get(key)||{};
        const now=Date.now();
        hdDownloadStatus.set(key,Object.freeze({...current,key,state,sourceKind:sourceKind||current.sourceKind||'',updatedAt:now,lastProgressAt:now}));
    }

    async function prepareHdDestination(destination,signal=null){
        const sources=await orderHdSourcesBySize(hdSourceCandidates(destination),signal);
        if(!sources.length)throw new Error('HD PRELOAD HAS NO SOURCES');
        let lastError=null;
        for(const source of sources){
            if(signal?.aborted)throw new DOMException('HD PRELOAD SUSPENDED','AbortError');
            setHdStatus(destination,'DOWNLOADING',source.kind);
            try{
                const response=await fetch(source.url,{cache:'force-cache',signal});
                if(!response.ok)throw new Error(`HTTP ${response.status} ${source.url}`);
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
            console.warn('GV-10G ISOLATED ALADIN PREWARM WARNING',error);
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
            let rotation=Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):null;
            if(rotation===null&&hubble.eccentricity>.22&&sky.eccentricity>.22){
                const delta=normalizeSignedAngle(hubble.angle-sky.angle);
                if(Number.isFinite(delta)&&Math.abs(delta)<=90)rotation=delta;
            }
            return Object.freeze({...destination,ra,dec,aladinRotation:rotation,framingCorrected:true});
        }catch(error){
            console.warn('GV-10G OPTIONAL ARCHIVE FRAMING SKIPPED',error);
            return destination;
        }
    }

    function blockedPrefetchKeys(){
        const keys=new Set(prefetchReady.map(item=>item.key));
        for(const destination of prefetchQueued)keys.add(destinationKey(destination));
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
        if(prefetchRetryTimer)return;
        const now=Date.now();
        const waits=[...prefetchRetryAfter.values()].map(value=>Number(value)-now).filter(value=>value>0);
        if(!waits.length)return;
        prefetchRetryTimer=setTimeout(()=>{prefetchRetryTimer=0;fillPrefetchQueue()},Math.max(100,Math.min(...waits)));
    }

    function queueHasKey(key){return prefetchQueued.some(destination=>destinationKey(destination)===key)}

    function enqueuePrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key)return false;
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
                const ahead=chooseAladinAheadCandidates(destination,2);
                for(const candidate of [destination,...ahead]){
                    if(backgroundWorkSuspended)return;
                    try{await prepareAladinDestination(candidate,priority&&candidate===destination)}catch(error){
                        if(error?.name==='AbortError')return;
                        console.warn('GV-10G ALADIN AHEAD PREWARM WARNING',error);
                    }
                }
                if(backgroundWorkSuspended||aladinPrewarmLastKey!==key)return;
                let preparedDestination=deriveHubbleFraming(destination,item.image);
                if(preparedDestination!==destination&&preparedDestination.framingCorrected){
                    try{await prepareAladinDestination(preparedDestination,true)}catch(error){
                        if(error?.name==='AbortError')return;
                        preparedDestination=destination;
                    }
                }
                item.destination=preparedDestination;
            }catch(error){
                if(error?.name!=='AbortError')console.warn('GV-10G SERIAL ALADIN PREWARM WARNING',error);
            }
        };
        const run=aladinPrefetchSerial.then(task,task);
        aladinPrefetchSerial=run.catch(()=>null);
    }

    function startPrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key)return;
        if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return}
        if(prefetchLoading.size>=PREFETCH_MAX_WORKERS){enqueuePrefetch(destination,priority);return}
        const controller=new AbortController();
        prefetchControllers.set(key,controller);
        const promise=(async()=>{
            try{
                const item=await prepareHdDestination(destination,controller.signal);
                item.destination=destination;
                prefetchRetryAfter.delete(key);
                if(key===activeTargetKey&&!activePreparedItem){
                    activePreparedItem=item;
                    window.__gv10eRandomGalaxy?.setPreparedHdResource?.(key,item.objectUrl,item.sourceKind,item.image);
                }else if(prefetchReady.length<HUBBLE_PREFETCH_TARGET){
                    prefetchReady.push(item);
                }else{
                    releasePreparedItem(item);
                    return;
                }
                scheduleAladinEnhancement(item,destination,priority);
            }catch(error){
                if(error?.name==='AbortError'){
                    setHdStatus(destination,'SUSPENDED');
                    if(key===activeTargetKey)priorityPrefetchDestination=destination;
                    return;
                }
                prefetchFailedCount++;
                setHdStatus(destination,'RETRY-WAIT');
                prefetchRetryAfter.set(key,Date.now()+HUBBLE_PREFETCH_RETRY_MS);
            }
        })().finally(()=>{
            prefetchLoading.delete(key);
            prefetchControllers.delete(key);
            queueMicrotask(fillPrefetchQueue);
        });
        prefetchLoading.set(key,promise);
    }

    function fillPrefetchQueue(){
        if(priorityPrefetchDestination){
            const destination=priorityPrefetchDestination;
            priorityPrefetchDestination=null;
            enqueuePrefetch(destination,true);
        }
        while(prefetchReady.length+prefetchLoading.size+prefetchQueued.length<HUBBLE_PREFETCH_TARGET){
            const candidate=choosePrefetchCandidate();
            if(!candidate||!enqueuePrefetch(candidate))break;
        }
        while(prefetchLoading.size<PREFETCH_MAX_WORKERS&&prefetchQueued.length){
            const destination=prefetchQueued.shift();
            startPrefetch(destination,destinationKey(destination)===activeTargetKey);
        }
        if(prefetchReady.length+prefetchLoading.size+prefetchQueued.length<HUBBLE_PREFETCH_TARGET)scheduleRetryFill();
    }

    function prefetchHealthCheck(){
        const ready=prefetchReady.length;
        const loading=prefetchLoading.size;
        const queued=prefetchQueued.length;
        const activeKeys=[...prefetchLoading.keys()];
        const retryWait=[...prefetchRetryAfter.entries()].filter(([,time])=>Date.now()<Number(time)).map(([key])=>key);
        const workers=activeKeys.map(key=>Object.freeze({...hdDownloadStatus.get(key)}));
        lastPrefetchHealth=Object.freeze({ready,loading,queued,total:ready+loading+queued,activeKeys:Object.freeze(activeKeys),retryWait:Object.freeze(retryWait),workers:Object.freeze(workers),checkedAt:Date.now()});
        if(!backgroundWorkSuspended&&lastPrefetchHealth.total<HUBBLE_PREFETCH_TARGET)fillPrefetchQueue();
        return lastPrefetchHealth;
    }

    prefetchHealthTimer=setInterval(prefetchHealthCheck,PREFETCH_HEALTH_INTERVAL_MS);

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
        priorityPrefetchDestination=destination;
        queueMicrotask(fillPrefetchQueue);
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
            if(!destination)destination=setUnpreparedActive(requested);
        }else{
            if(!galaxyCatalog.length)throw new Error('COMBINED GALAXY CATALOG IS EMPTY');
            const requested=galaxyCatalog[Math.floor(Math.random()*galaxyCatalog.length)];
            destination=consumeReady(requested,excludeName);
            if(!destination)destination=setUnpreparedActive(requested);
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

    function getHubblePrefetchState(){
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            maxWorkers:PREFETCH_MAX_WORKERS,
            readyCount:prefetchReady.length,
            loadingCount:prefetchLoading.size,
            queuedCount:prefetchQueued.length,
            pipelineCount:prefetchReady.length+prefetchLoading.size+prefetchQueued.length,
            failedCount:prefetchFailedCount,
            activeDownloadKeys:Object.freeze([...prefetchLoading.keys()]),
            activePreparedGalaxy:activePreparedItem?.destination?.name||'',
            activePreparedProvider:activePreparedItem?.destination?.provider||'',
            historyPreparedGalaxy:historyPreparedItem?.destination?.name||'',
            backgroundWorkSuspended,
            health:lastPrefetchHealth
        });
    }
    function getHubbleDownloadStatus(){return Object.freeze([...hdDownloadStatus.values()].map(value=>Object.freeze({...value})))}
    function getAladinPrewarmState(){return Object.freeze({ready:Boolean(aladinPrewarm),activeKey:aladinPrewarmActiveKey,lastKey:aladinPrewarmLastKey,warmedCount:aladinPrewarmedKeys.size,suspended:backgroundWorkSuspended})}

    function releasePreparedItem(item){if(item?.objectUrl)try{URL.revokeObjectURL(item.objectUrl)}catch(_){}}
    function suspendBackgroundWork(){
        if(backgroundWorkSuspended)return;
        backgroundWorkSuspended=true;
        for(const [key,controller] of prefetchControllers){
            if(key===activeTargetKey)continue;
            try{controller.abort()}catch(_){}
        }
        prefetchQueued.length=0;
        if(prefetchRetryTimer){clearTimeout(prefetchRetryTimer);prefetchRetryTimer=0}
        if(aladinPrewarmTimer){clearTimeout(aladinPrewarmTimer);aladinPrewarmTimer=0}
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
    }
    function resumeBackgroundWork(){
        if(!backgroundWorkSuspended)return;
        backgroundWorkSuspended=false;
        fillPrefetchQueue();
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
            }catch(error){console.error('GV-10G PROJECTION FAILURE',name,detail?.code,error)}
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
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GV-10G FRAME CHANGE WARNING',error)}
        renderCoordinates();
    }});
    const updateCoo=()=>{try{const coo=aladin.getRaDec();if(Array.isArray(coo)&&coo.length>=2){latestRa=Number(coo[0]);latestDec=Number(coo[1]);renderCoordinates()}}catch(_){}};
    if(typeof aladin.on==='function'){
        try{aladin.on('positionChanged',updateCoo)}catch(_){}
        try{aladin.on('objectClicked',updateCoo)}catch(_){}
        try{aladin.on('zoomChanged',updateCoo)}catch(_){}
    }
    updateCoo();

    await loadScript(TARGET_URL,'gvTargetSimbad0001');
    if(!window.GalaxyTargetSimbad)throw new Error('TARGET MODULE EXPORT MISSING');
    const target=window.GalaxyTargetSimbad.init({host:targetHost,aladin});

    await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0031');
    if(!window.GalaxyRandomGalaxy0031)throw new Error('RANDOM GALAXY MODULE 0031 EXPORT MISSING');
    const randomGalaxy=window.GalaxyRandomGalaxy0031.init({
        host:randomGalaxyHost,
        aladin,
        button:bottom.random,
        provider:randomHubbleProvider,
        travelSeconds:TRAVEL_SECONDS,
        onArrival(destination){
            navigationPending=false;
            endTravelHud();
            recordArrival(destination);
            syncHdProviderPresentation(destination);
            setHistoryControls();
            resumeBackgroundWork();
        },
        onError(error){
            navigationPending=false;pendingHistoryIndex=null;forcedDestination=null;endTravelHud();setHistoryControls();resumeBackgroundWork();console.error('GV-10G RANDOM GALAXY FAILURE',error);
        }
    });
    window.__gv10eRandomGalaxy=randomGalaxy;
    await randomGalaxy.ready;
    bottom.random.disabled=false;
    const launchRandomGalaxy=()=>{
        if(navigationPending||randomGalaxy.getState().busy)return;
        randomGalaxy.travelToRandom().catch(error=>{
            navigationPending=false;pendingHistoryIndex=null;forcedDestination=null;endTravelHud();setHistoryControls();resumeBackgroundWork();console.error('GV-10G RANDOM GALAXY CLICK FAILURE',error);
        });
    };
    bottom.random.addEventListener('click',launchRandomGalaxy);

    // 10N HD presentation: exact scope is archive/source controls + Galaxy Info + BACK TO SKY.
    const presentationStyle=document.createElement('style');
    presentationStyle.textContent='#gv-random-galaxy{border:2px solid #ABB3AA!important;box-shadow:none!important;filter:brightness(1.10)}.gv-galaxy-history{border:2px solid #ABB3AA!important;box-shadow:none!important;filter:brightness(1.10);opacity:1!important}.gvrg-hd-science,.gvrg-hd-viewport,#gv-hd-info-panel{box-sizing:border-box!important;width:min(680px,calc(100vw - 20px))!important;border:1px solid #78FFAB!important;border-radius:8px!important}.gvrg-hd-science,#gv-hd-info-panel{background:transparent!important;box-shadow:none!important}.gvrg-hd-science{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;overflow:hidden!important;pointer-events:none!important}.gvrg-hd-science .gvrg-hd-science-value{font-size:10.5px!important}.gvrg-hd-viewport{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;aspect-ratio:auto!important;overflow:hidden!important;background:#020B07!important;box-shadow:inset 0 0 6px rgba(120,255,171,.10),0 0 8px rgba(87,255,147,.22)!important;pointer-events:auto!important}.gvrg-hd-viewport>img:not(#gv-hd-archive-button img){width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;object-fit:cover!important;object-position:50% 50%;scale:1!important}.gvrg-hd-scale,.gvrg-hd-scale-label{font-size:13.5px!important}#gv-hd-info-panel{position:absolute;left:50%;z-index:4;transform:translateX(-50%);padding:9px 11px 10px;color:#DFFFEA;font:400 10.5px/1.45 "Space Age",sans-serif;letter-spacing:.42px;text-align:left;text-shadow:0 0 4px rgba(87,255,147,.22);display:flex;flex-direction:column;overflow:hidden;pointer-events:none}#gv-hd-info-title{flex:0 0 auto;margin-bottom:6px;color:#78FFAB;font-size:12px;letter-spacing:.75px;text-align:center}#gv-hd-info-body{flex:1 1 auto;min-height:0;overflow:hidden;overflow-wrap:anywhere}.gvrg-credit{display:none!important}#gv-hd-archive-button{position:absolute!important;right:14px!important;bottom:14px!important;z-index:40!important;width:36px!important;height:36px!important;margin:0!important;padding:2px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;box-sizing:content-box!important;border:2px solid #78FFAB!important;border-radius:5px!important;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94))!important;box-shadow:none!important;filter:none!important;overflow:hidden!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-archive-button img{display:block!important;width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;margin:0!important;padding:0!important;border:0!important;border-radius:3px!important;box-shadow:none!important}#gv-archive-overlay{position:fixed;inset:0;z-index:2147483000;background:#000;display:none;pointer-events:none}#gv-archive-overlay.gv-open{display:block;pointer-events:auto}#gv-archive-frame{position:absolute;inset:0;width:100%;height:100%;border:0;background:#000}#gv-archive-back{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom));z-index:2147483647;transform:translateX(-50%);display:inline-flex;align-items:center;justify-content:center;gap:10px;height:48px;padding:0 12px;border:2px solid #ABB3AA;border-radius:7px;background:linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98));color:#E8FFF0;font:400 13px/1 "Space Age",sans-serif;letter-spacing:.55px;text-transform:uppercase;white-space:nowrap;box-shadow:0 0 12px rgba(0,0,0,.75);pointer-events:auto;touch-action:manipulation;cursor:pointer}#gv-archive-arrow{position:relative;display:inline-flex;width:36px;height:36px;flex:0 0 36px;align-items:center;justify-content:center}#gv-archive-arrow::before,#gv-archive-arrow::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;box-sizing:border-box;pointer-events:none}#gv-archive-arrow::before{border-width:6px;border-color:#78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.90));transform:translate(-38%,-50%) rotate(-135deg)}#gv-archive-arrow::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-34%,-50%) rotate(-135deg)}#gv-archive-target-tile{box-sizing:border-box;width:36px;height:36px;flex:0 0 36px;display:inline-flex;align-items:center;justify-content:center;border:2px solid #ABB3AA;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98));overflow:hidden}#gv-archive-target-tile img{display:block;width:28px;height:28px;object-fit:contain;flex:0 0 28px;margin:0;padding:0;border:0}';
    document.head.appendChild(presentationStyle);

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
            if(ageItem?.parentNode)ageItem.parentNode.insertBefore(constellationItem,ageItem.nextSibling);else hdScience.appendChild(constellationItem);
        }else constellationValue=constellationItem.querySelector('.gvrg-hd-science-value');
        if(!constellationValue){
            constellationValue=document.createElement('div');constellationValue.className='gvrg-hd-science-value';constellationItem.appendChild(constellationValue);
        }
        constellationValue.textContent='UNKNOWN';
    }

    const hdInfoPanel=document.createElement('div');hdInfoPanel.id='gv-hd-info-panel';
    const hdInfoTitle=document.createElement('div');hdInfoTitle.id='gv-hd-info-title';hdInfoTitle.textContent='GALAXY INFO';
    const hdInfoBody=document.createElement('div');hdInfoBody.id='gv-hd-info-body';
    hdInfoPanel.append(hdInfoTitle,hdInfoBody);document.body.appendChild(hdInfoPanel);

    const hdBackToSky=randomGalaxy.hdBackButton||randomGalaxy.backToSkyButton||document.querySelector('.gvrg-hd-back');
    if(hdBackToSky){
        hdBackToSky.id='gv-hd-back-to-sky';
        hdBackToSky.textContent='BACK TO SKY';
    }

    function isHdPresentationActive(){return Boolean(randomGalaxy.getState?.().hdOpen)}

    function restoreNormalViewerPresentation(){
        bottom.version.style.top='';
        bottom.version.style.bottom='51px';
        if(!archiveOverlay.classList.contains('gv-open')){
            archiveOverlay.style.pointerEvents='none';
            archiveOverlay.setAttribute('aria-hidden','true');
            archiveFrame.style.pointerEvents='none';
        }
        if(!navigationPending&&!randomGalaxy.getState().busy)bottom.random.disabled=false;
        setHistoryControls();
    }

    function settleHdPresentation(){
        if(!isHdPresentationActive())return;
        const viewport=randomGalaxy.hdViewport;if(!viewport)return;
        const safeWidth=Math.min(680,Math.max(0,window.innerWidth-20));
        const topBannerHeight=randomGalaxy.hdScience?.offsetHeight||0;
        const top=10+topBannerHeight+8;
        const maxHeight=Math.max(120,window.innerHeight-top-150);
        const size=Math.min(safeWidth,maxHeight);
        viewport.style.width=`${size}px`;viewport.style.height=`${size}px`;viewport.style.top=`${top}px`;
        positionHdInfoPanel();
        bottom.version.style.top=`${Math.min(window.innerHeight-12,hdInfoPanel.offsetTop+hdInfoPanel.offsetHeight+6)}px`;
        bottom.version.style.bottom='auto';
    }

    function positionHdInfoPanel(){
        if(!isHdPresentationActive())return;
        const viewport=randomGalaxy.hdViewport;if(!viewport)return;
        const rect=viewport.getBoundingClientRect();
        const desiredTop=Math.min(window.innerHeight-92,Math.round(rect.bottom+8));
        hdInfoPanel.style.top=`${Math.max(0,desiredTop)}px`;
        hdInfoPanel.style.height=`${Math.max(84,window.innerHeight-desiredTop-22)}px`;
        fitHdInfoText();
    }

    function fitHdInfoText(){
        if(!isHdPresentationActive())return;
        const text=hdInfoBody.dataset.fullText||'';
        const button=hdBackToSky;if(!button){hdInfoBody.textContent=text;return}
        const panelRect=hdInfoPanel.getBoundingClientRect();
        const buttonRect=button.getBoundingClientRect();
        const bodyRect=hdInfoBody.getBoundingClientRect();
        const safety={left:buttonRect.left-panelRect.left-6,right:buttonRect.right-panelRect.left+6,top:buttonRect.top-bodyRect.top-4,bottom:buttonRect.bottom-bodyRect.top+4};
        const words=text.split(/\s+/).filter(Boolean);hdInfoBody.textContent='';
        const measure=document.createElement('span');measure.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;font:inherit;letter-spacing:inherit';document.body.appendChild(measure);
        const lines=[];const lineHeight=parseFloat(getComputedStyle(hdInfoBody).lineHeight)||15;const maxLines=Math.max(1,Math.floor(bodyRect.height/lineHeight));
        let line='';
        for(const word of words){
            const row=lines.length;const rowTop=row*lineHeight,rowBottom=rowTop+lineHeight;
            const intersects=rowBottom>safety.top&&rowTop<safety.bottom;
            const available=intersects?Math.max(30,bodyRect.right-buttonRect.right-10):bodyRect.width;
            const candidate=line?`${line} ${word}`:word;measure.textContent=candidate;
            if(measure.offsetWidth<=available){line=candidate;continue}
            if(line){lines.push(line);if(lines.length>=maxLines)break;line=word}else{lines.push(word);line='';if(lines.length>=maxLines)break}
        }
        if(line&&lines.length<maxLines)lines.push(line);measure.remove();hdInfoBody.textContent=lines.join(' ');
    }

    function renderHdInfoCandidate(destination){
        const text=galaxyInfoText(destination);hdInfoBody.dataset.fullText=text;hdInfoBody.textContent=text;requestAnimationFrame(()=>requestAnimationFrame(fitHdInfoText));
    }

    const hdArchiveButton=document.createElement('button');
    hdArchiveButton.id='gv-hd-archive-button';
    hdArchiveButton.type='button';
    hdArchiveButton.setAttribute('aria-label','OPEN ARCHIVE SOURCE');
    const hdArchiveIcon=document.createElement('img');
    hdArchiveIcon.alt='ARCHIVE SOURCE';
    hdArchiveButton.appendChild(hdArchiveIcon);
    randomGalaxy.hdViewport?.appendChild(hdArchiveButton);
    hdArchiveButton.addEventListener('pointerdown',event=>event.stopPropagation(),true);
    hdArchiveButton.addEventListener('pointerup',event=>event.stopPropagation(),true);

    const archiveOverlay=document.createElement('div');
    archiveOverlay.id='gv-archive-overlay';
    const archiveFrame=document.createElement('iframe');
    archiveFrame.id='gv-archive-frame';
    archiveFrame.title='GALAXY ARCHIVE SOURCE';
    const archiveBack=document.createElement('button');
    archiveBack.id='gv-archive-back';
    archiveBack.type='button';
    const archiveArrow=document.createElement('span');
    archiveArrow.id='gv-archive-arrow';
    archiveArrow.setAttribute('aria-hidden','true');
    const archiveTargetTile=document.createElement('span');
    archiveTargetTile.id='gv-archive-target-tile';
    archiveTargetTile.setAttribute('aria-hidden','true');
    const archiveTarget=document.createElement('img');
    archiveTarget.src=TARGET_ICON_URL;
    archiveTarget.alt='';
    archiveTarget.setAttribute('aria-hidden','true');
    archiveTargetTile.appendChild(archiveTarget);
    const archiveBackLabel=document.createElement('span');
    archiveBackLabel.textContent='BACK TO GALAXY VIEWER';
    archiveBack.append(archiveArrow,archiveBackLabel,archiveTargetTile);
    archiveBack.setAttribute('aria-label','BACK TO GALAXY VIEWER');
    archiveOverlay.append(archiveFrame,archiveBack);
    document.body.appendChild(archiveOverlay);
    let archiveSourceUrl='';
    const closeArchiveOverlay=()=>{
        archiveOverlay.classList.remove('gv-open');
        archiveOverlay.style.pointerEvents='none';
        archiveOverlay.setAttribute('aria-hidden','true');
        archiveFrame.style.pointerEvents='none';
        archiveFrame.blur();
        archiveFrame.src='about:blank';
        archiveSourceUrl='';
        requestAnimationFrame(()=>{
            reconcileViewerPresentation();
            if(!navigationPending&&!randomGalaxy.getState().busy)bottom.random.disabled=false;
            setHistoryControls();
            if(isHdPresentationActive())try{hdArchiveButton.focus({preventScroll:true})}catch(_){}
        });
    };
    archiveBack.addEventListener('click',event=>{
        event.preventDefault();
        event.stopPropagation();
        closeArchiveOverlay();
    });
    archiveFrame.addEventListener('error',()=>{
        const sourceUrl=archiveSourceUrl;
        closeArchiveOverlay();
        if(sourceUrl)window.open(sourceUrl,'_blank','noopener,noreferrer');
    });

    function currentArchiveDestination(){return randomGalaxy.getState?.().activeDestination||randomGalaxy.activeDestination||null}
    hdArchiveButton.addEventListener('click',event=>{
        event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();
        const destination=currentArchiveDestination();
        const sourceUrl=String(destination?.sourceUrl||'').trim();
        if(!/^https:\/\//i.test(sourceUrl))return;
        archiveSourceUrl=sourceUrl;
        archiveFrame.src=sourceUrl;
        archiveFrame.style.pointerEvents='auto';
        archiveOverlay.removeAttribute('aria-hidden');
        archiveOverlay.style.pointerEvents='auto';
        archiveOverlay.classList.add('gv-open');
    },true);

    function galaxyInfoText(destination){
        if(!destination)return '';
        const provider=providerFor(destination);
        return `${provider} ${destination.designation||destination.name}. ${destination.commonName||destination.name}. Distance ${Number(destination.distance).toFixed(1)} million light-years. ${destination.constellation?`Constellation ${destination.constellation}. `:''}${destination.age?`Estimated age ${destination.age}. `:''}${destination.orientation?`Orientation ${destination.orientation}. `:''}${destination.credit?`Credit ${destination.credit}.`:''}`.replace(/\s+/g,' ').trim();
    }

    function providerFor(destination){return String(destination?.provider||'HUBBLE').toUpperCase()==='JWST'?'JWST':'HUBBLE'}
    function syncHdProviderPresentation(destination=currentArchiveDestination()){
        const provider=providerFor(destination);hdArchiveIcon.src=provider==='JWST'?JWST_ICON_URL:Hubble_ICON_URL;hdArchiveButton.setAttribute('aria-label',`OPEN ${provider} ARCHIVE SOURCE`);renderHdInfoCandidate(destination);requestAnimationFrame(settleHdPresentation);
    }

    function recordArrival(destination){
        if(!destination)return;
        const item={...destination};
        if(pendingHistoryIndex!==null){galaxyHistoryIndex=pendingHistoryIndex;galaxyHistory[galaxyHistoryIndex]=item;pendingHistoryIndex=null;return}
        if(galaxyHistoryIndex<galaxyHistory.length-1)galaxyHistory=galaxyHistory.slice(0,galaxyHistoryIndex+1);
        galaxyHistory.push(item);galaxyHistoryIndex=galaxyHistory.length-1;
    }
    function setHistoryControls(){
        const busy=navigationPending||Boolean(randomGalaxy?.getState?.().busy);
        bottom.back.disabled=busy||galaxyHistoryIndex<=0;
        bottom.forward.disabled=busy||galaxyHistoryIndex<0||galaxyHistoryIndex>=galaxyHistory.length-1;
    }
    function navigateHistory(index){
        if(index<0||index>=galaxyHistory.length||navigationPending||randomGalaxy.getState().busy)return;
        const destination=galaxyHistory[index];pendingHistoryIndex=index;forcedDestination=destination;navigationPending=true;setHistoryControls();
        randomGalaxy.travelToRandom().catch(error=>{navigationPending=false;pendingHistoryIndex=null;forcedDestination=null;setHistoryControls();console.error('GV-10G HISTORY FAILURE',error)});
    }

    const originalShowHubbleHD=randomGalaxy.showHubbleHD.bind(randomGalaxy);
    randomGalaxy.showHubbleHD=function(){
        const result=originalShowHubbleHD();
        requestAnimationFrame(()=>requestAnimationFrame(settleHdPresentation));
        return result;
    };
    randomGalaxy.viewHdButton?.addEventListener('click',()=>requestAnimationFrame(settleHdPresentation),true);
    randomGalaxy.hubbleIconButton?.addEventListener('click',()=>requestAnimationFrame(settleHdPresentation),true);
    const handleViewerResize=()=>requestAnimationFrame(reconcileViewerPresentation);
    const handleViewerPageShow=()=>requestAnimationFrame(reconcileViewerPresentation);
    const handleViewerVisibility=()=>{if(!document.hidden)requestAnimationFrame(reconcileViewerPresentation)};
    window.addEventListener('resize',handleViewerResize);
    window.addEventListener('pageshow',handleViewerPageShow);
    document.addEventListener('visibilitychange',handleViewerVisibility);
    syncHdProviderPresentation();

    const deferHdUntilPrepared=async event=>{
        const destination=randomGalaxy.getState?.().activeDestination;
        const key=destinationKey(destination);
        const pending=Boolean(key&&(prefetchLoading.has(key)||queueHasKey(key)||(priorityPrefetchDestination&&destinationKey(priorityPrefetchDestination)===key)));
        if(!pending)return;
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        try{
            await waitForPreparedKey(key);
            randomGalaxy.showHubbleHD();
        }catch(error){
            console.error('GV-10G ARCHIVE PREPARATION WAIT FAILURE',error);
            try{randomGalaxy.showHubbleHD()}catch(fallbackError){console.error('GV-10G ARCHIVE FALLBACK FAILURE',fallbackError)}
        }
    };

    window.addEventListener('beforeunload',()=>{
        for(const controller of prefetchControllers.values())controller.abort();
        prefetchControllers.clear();
        if(prefetchRetryTimer)clearTimeout(prefetchRetryTimer);
        if(prefetchHealthTimer)clearInterval(prefetchHealthTimer);
        if(aladinPrewarmTimer)clearTimeout(aladinPrewarmTimer);
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        randomGalaxy.viewHdButton?.removeEventListener('click',deferHdUntilPrepared,true);
        randomGalaxy.hubbleIconButton?.removeEventListener('click',deferHdUntilPrepared,true);
        window.removeEventListener('resize',handleViewerResize);
        window.removeEventListener('pageshow',handleViewerPageShow);
        document.removeEventListener('visibilitychange',handleViewerVisibility);
        releasePreparedItem(activePreparedItem);releasePreparedItem(historyPreparedItem);prefetchReady.splice(0).forEach(releasePreparedItem);
        prefetchQueued.splice(0);
        try{aladinPrewarmHost?.remove()}catch(_){}
    },{once:true});
    bottom.random.addEventListener('click',suspendBackgroundWork,true);
    bottom.random.addEventListener('click',()=>{pendingHistoryIndex=null;navigationPending=true;homeOverlay.classList.add('gv-hidden');universeContext.classList.add('gv-hidden');setHistoryControls()});
    bottom.back.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex-1));
    bottom.forward.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex+1));
    setHistoryControls();
    window.GV10E=Object.freeze({version:VERSION,displayVersion:DISPLAY_VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,universeContext,homeOverlay,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,catalogDatabaseCounts,getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,startHubblePrefetch:fillPrefetchQueue,getGalaxyHistory:()=>({index:galaxyHistoryIndex,items:galaxyHistory.map(item=>({name:item.name,archiveId:item.archiveId,provider:item.provider||'HUBBLE'}))})});
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length}}));
})().catch(error=>{console.error('GALAXY VIEWER 10L STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});
"""))

# GV-beta-0010Q staged