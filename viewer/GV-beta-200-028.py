from IPython.display import HTML, Javascript, display
import json

# ============================================================================
# SECTION 001 — FILE IDENTITY / PYTHON IMPORTS
# ECO: GV200-001
# ============================================================================
VIEWER_VERSION = "RC-V1.0.0"
# BUILD 0008 — frozen dependency set; native provider browser integration

# ============================================================================
# SECTION 002 — ALADIN MIRROR POINTERS
# ECO: GV200-001
# ============================================================================
ALADIN_VERSION = "3.8.2"
ALADIN_CSS_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/aladin-source-clone/src/css/aladin.css"
ALADIN_JS_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/vendor/aladin-lite/3.8.2/aladin.js"

# ============================================================================
# SECTION 003 — GALAXY VIEWER MODULE POINTERS
# ECO: GV200-001
# ============================================================================
HAMBURGER_BASE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hamburger-menu/gv-hamburger-menu-0009.js"
HAMBURGER_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hamburger-menu/gv-hamburger-menu-0009.js"
COORDINATE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js"
TARGET_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/target-simbad/gv-target-simbad-0005.js"
DIAGNOSTICS_URL = HAMBURGER_BASE_URL
GALAXY_ROUTE_ENGINE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js?v=0001"
GALAXY_NAVIGATOR_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js?v=0003"
HEADS_UP_DISPLAY_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hud/gv-heads-up-display-0001.js"

# ============================================================================
# SECTION 004 — HTML APPLICATION ROOT
# ECO: GV200-001
# ============================================================================
display(HTML("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/aladin-source-clone/src/css/aladin.css" />
<div id="aladin-cosmic-command-test">

<!-- =======================================================================
     SECTION 005 — MODULE HOST ELEMENTS
     ECO: GV200-001
     ======================================================================= -->
<div id="gv-hamburger-host"></div>
<div id="gv-coordinate-host"></div>
<div id="gv-target-host"></div>
<div id="gv-navigation-host"></div>

<!-- =======================================================================
     SECTION 006 — VIEWER BASE CSS
     ECO: GV200-001
     ======================================================================= -->
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{position:relative;width:100%;height:100dvh;max-height:100%;overflow:hidden;background:#000;padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box}
#aladin-cosmic-command-test .aladin-logo-container,#aladin-cosmic-command-test .aladin-logo{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
</style>

<!-- =======================================================================
     SECTION 007 — MODULE HOST LAYOUT
     ECO: GV200-001
     ======================================================================= -->
<style>
#gv-hamburger-host{position:absolute;inset:0;z-index:9000;pointer-events:none}
#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;pointer-events:auto}
#gv-target-host{position:absolute;left:342px;top:12px;z-index:7210;width:36px;height:36px;pointer-events:auto}
#gv-navigation-host{position:absolute;left:50%;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:7300;display:flex;gap:5px;width:min(430px,calc(100vw - 20px));transform:translateX(-50%);pointer-events:auto}
#gv-center-reticle{position:absolute;left:50%;top:50%;z-index:7301;width:270px;height:270px;transform:translate(-50%,-50%);pointer-events:none;user-select:none;-webkit-user-select:none}
#gv-center-reticle img{display:block;width:32px;height:32px}
</style>
</div>
"""))

# ============================================================================
# SECTION 010 — BOOT CONFIGURATION
# ECO: GV200-001
# ============================================================================
# Launcher-safe configuration: injected into the single extracted JS block.

# ============================================================================
# SECTION 008 — JAVASCRIPT APPLICATION ENTRY
# ECO: GV200-001
# ============================================================================
display(Javascript(r"""
(async()=>{
'use strict';
const VERSION='GV-beta-200-028';
const GV200001_BUILD='0001';
const GV_RUNTIME='0082';
const fresh=url=>`${url}${url.includes('?')?'&':'?'}v=GV200001-${GV200001_BUILD}`;
const requestPortraitLock=()=>{try{const lock=screen?.orientation?.lock;if(typeof lock==='function')Promise.resolve(lock.call(screen.orientation,'portrait-primary')).catch(()=>{})}catch(_){}};
requestPortraitLock();
document.addEventListener('pointerdown',requestPortraitLock,{once:true,passive:true});
window.GV_BOOT_CONFIG=Object.freeze({
    viewerVersion:'GV-beta-200-028',
    aladinVersion:'3.8.2',
    aladinCssUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/aladin-source-clone/src/css/aladin.css',
    aladinJsUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/vendor/aladin-lite/3.8.2/aladin.js',
    hamburgerBaseUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hamburger-menu/gv-hamburger-menu-0009.js',
    hamburgerUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hamburger-menu/gv-hamburger-menu-0009.js',
    coordinateUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js',
    targetUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/target-simbad/gv-target-simbad-0005.js',
    diagnosticsUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hamburger-menu/gv-hamburger-menu-0009.js',
    galaxyRouteEngineUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js',
    galaxyNavigatorUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js',
    headsUpDisplayUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/hud/gv-heads-up-display-0001.js',
    travelPresentationUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/random-galaxy/gv-random-travel-presentation.js',
    destinationPresentationUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/destination-presentation/gv-destination-presentation-0017.js'
});


// ============================================================================
// SECTION 009 — SCRIPT LOADER
// ECO: GV200-001
// ============================================================================
function loadScript(url){
    const attempt=(retry=false)=>new Promise((resolve,reject)=>{
        const requested=new URL(url,window.location.href).href;
        let script=[...document.scripts].find(s=>new URL(s.src||'',window.location.href).href===requested);
        if(script?.dataset.gvReady==='1')return resolve(script);
        if(retry&&script){script.remove();script=null}
        if(!script){script=document.createElement('script');script.src=url;script.async=true;document.head.appendChild(script)}
        let settled=false;
        const finish=(error)=>{if(settled)return;settled=true;clearTimeout(timer);error?reject(error):(script.dataset.gvReady='1',resolve(script))};
        script.addEventListener('load',()=>finish(),{once:true});
        script.addEventListener('error',()=>finish(new Error(`SCRIPT LOAD FAILED: ${url}`)),{once:true});
        const timer=setTimeout(()=>finish(new Error(`SCRIPT LOAD TIMEOUT: ${url}`)),12000);
    });
    return attempt(false).catch(error=>{
        console.warn('GV SCRIPT RETRY',url,error);
        return attempt(true);
    });
}


// ============================================================================
// SECTION 011 — ALADIN CSS RESOURCE GATE
// ECO: GV200-001
// ============================================================================
const config=window.GV_BOOT_CONFIG;
if(!document.querySelector(`link[href="${config.aladinCssUrl}"]`)){
    const css=document.createElement('link');
    css.rel='stylesheet';
    css.href=config.aladinCssUrl;
    document.head.appendChild(css);
}


// ============================================================================
// SECTION 012 — BOOT CONFIGURATION VALIDATION
// ECO: GV200-001
// ============================================================================
for(const key of [
    'viewerVersion','aladinVersion','aladinCssUrl','aladinJsUrl',
    'hamburgerBaseUrl','hamburgerUrl','coordinateUrl','targetUrl',
    'diagnosticsUrl','galaxyRouteEngineUrl','galaxyNavigatorUrl','headsUpDisplayUrl','travelPresentationUrl'
]){
    if(!config?.[key])throw new Error(`BOOT CONFIG MISSING: ${key}`);
}


// ============================================================================
// SECTION 013 — ALADIN JAVASCRIPT LOAD
// ECO: GV200-001
// ============================================================================
await loadScript(config.aladinJsUrl);
const A=globalThis.A;
if(!A?.init)throw new Error('ALADIN CDS GLOBAL MISSING: A.init');
await A.init;


// ============================================================================
// SECTION 014 — ALADIN VIEWER INITIALIZATION
// ECO: GV200-001
// ============================================================================
const aladin=A.aladin('#aladin-cosmic-command-test',{
    survey:'P/DSS2/color',
    projection:'MOL',
    fov:360,
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


// ============================================================================
// SECTION 015 — HOME DEFINITION
// ECO: GV200-001
// ============================================================================


const HOME=Object.freeze({
    name:'EARTH — MILKY WAY',
    ra:266.41683,
    dec:-29.00781,
    fov:360,
    rotation:0
});

const GV_SPACE_AGE_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf';
const gvSpaceAgeFace=new FontFace('GV Space Age',`url("${GV_SPACE_AGE_URL}")`,{style:'normal',weight:'400'});
const gvSpaceAgeReady=gvSpaceAgeFace.load().then(face=>{
    document.fonts.add(face);
    return face;
});

// Top observable-universe callout. Geometry is copied from Random Galaxy 0166.
async function installUniverseContext(){
    if(document.getElementById('gv-universe-context'))return;
    await gvSpaceAgeReady;
    const style=document.createElement('style');
    style.id='gv200001-universe-context-style';    style.textContent=`
#gv-universe-context{position:absolute;left:50%;top:auto;bottom:calc(50% + min(25vw,50dvh) + 67px);z-index:7095;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;width:min(240px,66vw);pointer-events:none;transition:opacity .2s ease;font-family:"GV Space Age",sans-serif}
#gv-universe-context .gv-universe-label{position:relative;overflow:hidden;padding:8px 10px 9px;border:1px solid rgba(124,203,255,.78);border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.94),rgba(11,49,119,.88),rgba(41,109,189,.78)) padding-box,linear-gradient(135deg,#DDF8FF,#58BFFF,#296DBD) border-box;box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72),0 0 18px rgba(20,116,219,.35);color:#DDF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 6px rgba(88,191,255,.42);font:400 9px/1.35 "GV Space Age",sans-serif;letter-spacing:.65px}
#gv-universe-context .gv-universe-label::before{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.34) 0%,rgba(118,225,255,.08) 25%,transparent 44%);pointer-events:none}\n#gv-universe-context .gv-universe-count{display:block;margin-top:2px;color:#7CCBFF;font-size:10px;letter-spacing:.8px}
#gv-universe-context .gv-universe-size{display:block;margin-top:2px;color:#7CCBFF;font-size:9px;letter-spacing:.8px}
#gv-universe-context .gv-universe-leader{position:relative;width:1px;height:18px;background:rgba(124,203,255,.86);box-shadow:0 0 7px rgba(88,191,255,.48)}
#gv-universe-context .gv-universe-leader::after{content:"";position:absolute;left:50%;bottom:-1px;width:0;height:0;transform:translateX(-50%);border-left:5px solid transparent;border-right:5px solid transparent;border-top:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.68))}
`;
    document.head.appendChild(style);
    const universe=document.createElement('div');
    universe.id='gv-universe-context';
    universe.setAttribute('aria-live','polite');
    universe.innerHTML=
      '<div class="gv-universe-label">'+
        'THIS IS OUR MAP OF THE OBSERVABLE UNIVERSE'+
        '<span class="gv-universe-count">OVER 2 TRILLION GALAXIES</span>'+
        '<span class="gv-universe-size">93 BILLION LIGHT-YEARS ACROSS</span>'+
      '</div>'+
      '<div class="gv-universe-leader" aria-hidden="true"></div>';
    document.getElementById('aladin-cosmic-command-test').appendChild(universe);
}
gvSpaceAgeReady.then(()=>installUniverseContext()).catch(error=>console.error('GV SPACE AGE FONT LOAD FAILURE',error));

// ============================================================================
// SECTION 041 — COMPASS / CENTER RETICLE / NORTH ROTATION
// ECO: GV200-001
// ============================================================================
const RETICLE_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/artwork/compass/compass.png';

function createCenterReticle(root){
    const SIZE=270;
    const reticle=document.createElement('div');
    reticle.id='gv-center-reticle';
    reticle.setAttribute('aria-hidden','true');
    const compass=document.createElement('img');
    compass.id='gv-compass-reticle';
    compass.src=fresh(RETICLE_URL); compass.alt=''; compass.width=SIZE; compass.height=SIZE;
    Object.assign(compass.style,{position:'absolute',inset:'0',width:`${SIZE}px`,height:`${SIZE}px`,objectFit:'contain',opacity:'0.6',transform:'rotate(0deg)',transformOrigin:'50% 50%',pointerEvents:'none',willChange:'transform'});
    reticle.appendChild(compass);
    reticle.gvDirectional={northRotor:compass,lastNorthBearing:null};
    root.appendChild(reticle);
    return reticle;
}

let gvAuthoritativeRotation=HOME.rotation;
function readCelestialNorthBearing(aladin,root){
    return ((-gvAuthoritativeRotation%360)+360)%360;
}

const compassRoot=document.getElementById('aladin-cosmic-command-test');
if(!compassRoot)throw new Error('GALAXY VIEWER ROOT MISSING');
const reticle=createCenterReticle(compassRoot);

function setNorthMarker(bearing){
    const state=reticle.gvDirectional;
    if(!state||!state.northRotor||!Number.isFinite(bearing))return;
    const northBearing=((bearing%360)+360)%360;
    state.lastNorthBearing=northBearing;
    state.northRotor.style.transform=`rotate(${northBearing}deg)`;
    state.northRotor.dataset.northBearing=northBearing.toFixed(3);
}

aladin.on('rotationChanged',rotation=>{
    const liveRotation=Number(rotation);
    if(!Number.isFinite(liveRotation))return;
    gvAuthoritativeRotation=liveRotation;
    setNorthMarker(-liveRotation);
});

const updateDirectionalReticle=()=>{
    const state=reticle.gvDirectional;
    if(!state)return;
    const northBearing=readCelestialNorthBearing(aladin,compassRoot);
    if(Number.isFinite(northBearing))setNorthMarker(northBearing);
    else if(Number.isFinite(state.lastNorthBearing))setNorthMarker(state.lastNorthBearing);
};

const directionalReticleTimer=setInterval(updateDirectionalReticle,40);
updateDirectionalReticle();
window.addEventListener(
    'beforeunload',
    ()=>clearInterval(directionalReticleTimer),
    {once:true}
);

// ============================================================================
// SECTION 041B — EARTH BEARING POINTER / ARRIVAL DISTANCE
// ECO: GV200-028 BUILD 0001
// ============================================================================
function gvInstallEarthBearingPointer(){
    if(document.getElementById('gv-earth-bearing-rotor'))return;
    const rotor=document.createElement('div');
    rotor.id='gv-earth-bearing-rotor';
    rotor.setAttribute('aria-hidden','true');
    Object.assign(rotor.style,{position:'absolute',inset:'0',width:'270px',height:'270px',pointerEvents:'none',transformOrigin:'50% 50%',willChange:'transform',zIndex:'2'});
    const tick=document.createElement('i');
    Object.assign(tick.style,{position:'absolute',left:'50%',top:'-7px',width:'0',height:'0',transform:'translateX(-50%)',borderLeft:'5px solid transparent',borderRight:'5px solid transparent',borderBottom:'9px solid #FFD84A',filter:'drop-shadow(0 0 4px rgba(255,216,74,.9))'});
    rotor.appendChild(tick);
    reticle.appendChild(rotor);
}
function gvEarthScreenBearing(){
    try{
        const p=aladin.getRaDec?.();
        const ra=Number(Array.isArray(p)?p[0]:p?.ra),dec=Number(Array.isArray(p)?p[1]:p?.dec);
        if(!Number.isFinite(ra)||!Number.isFinite(dec))return null;
        const r=Math.PI/180,p1=dec*r,p2=Number(HOME.dec)*r,dl=(Number(HOME.ra)-ra)*r;
        const separation=Math.acos(Math.max(-1,Math.min(1,Math.sin(p1)*Math.sin(p2)+Math.cos(p1)*Math.cos(p2)*Math.cos(dl))));
        if(separation<1e-7)return null;
        const bearing=Math.atan2(Math.sin(dl)*Math.cos(p2),Math.cos(p1)*Math.sin(p2)-Math.sin(p1)*Math.cos(p2)*Math.cos(dl))*180/Math.PI;
        return ((readCelestialNorthBearing(aladin,compassRoot)+bearing)%360+360)%360;
    }catch(_){return null}
}
function gvUpdateEarthBearingPointer(){
    const rotor=document.getElementById('gv-earth-bearing-rotor');if(!rotor)return;
    const a=gvEarthScreenBearing();
    rotor.style.opacity=Number.isFinite(a)?'1':'0';
    if(Number.isFinite(a))rotor.style.transform=`rotate(${a}deg)`;
}
gvInstallEarthBearingPointer();
const gvEarthBearingTimer=setInterval(gvUpdateEarthBearingPointer,40);
window.addEventListener('beforeunload',()=>clearInterval(gvEarthBearingTimer),{once:true});

function gvFormatEarthDistance(destination){
    const m=Number(destination?.distanceMly??destination?.distance);
    if(!(m>0))return '';
    const label=String(destination?.distanceUnit||destination?.distanceUnits||'').toUpperCase();
    if(label.includes('BLY'))return `${m.toLocaleString('en-US',{maximumFractionDigits:2})} BLY TO EARTH`;
    if(label.includes('KLY'))return `${m.toLocaleString('en-US',{maximumFractionDigits:2})} KLY TO EARTH`;
    return `${m.toLocaleString('en-US',{maximumFractionDigits:m<10?1:0})} MLY TO EARTH`;
}
function gvInstallEarthDistanceBanner(){
    if(document.getElementById('gv-earth-distance-banner'))return;
    const style=document.createElement('style');style.textContent=`
#gv-earth-distance-banner{position:fixed;left:50%;z-index:7362;transform:translateX(-50%);box-sizing:border-box;width:33vw;max-width:150px;min-width:0;min-height:22px;padding:3px 5px;border:1px solid transparent;border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.95),rgba(11,49,119,.90) 50%,rgba(20,132,219,.70)) padding-box,linear-gradient(135deg,#DDF8FF,#58BFFF 58%,#296DBD) border-box;box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72),0 0 18px rgba(20,116,219,.35);font:400 7px/1.05 "GV Space Age",sans-serif;letter-spacing:.12px;white-space:nowrap;color:#FFD84A;text-align:center;text-shadow:0 0 4px rgba(255,216,74,.75);pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-earth-distance-banner.gv-visible{opacity:1;visibility:visible}
#gv-earth-distance-banner .gv-earth-distance-tick{display:inline-block;margin-left:7px;width:0;height:0;border-top:5px solid transparent;border-bottom:5px solid transparent;border-left:9px solid #FFD84A;filter:drop-shadow(0 0 4px rgba(255,216,74,.9));vertical-align:-1px}`;document.head.appendChild(style);
    const b=document.createElement('div');b.id='gv-earth-distance-banner';document.body.appendChild(b);
}
function gvHideEarthDistance(){document.getElementById('gv-earth-distance-banner')?.classList.remove('gv-visible')}
function gvShowEarthDistance(destination){
    gvInstallEarthDistanceBanner();const b=document.getElementById('gv-earth-distance-banner'),text=gvFormatEarthDistance(destination);if(!b||!text)return;
    b.innerHTML=`${text}<span class="gv-earth-distance-tick" aria-hidden="true"></span>`;
    const card=document.querySelector('.gvdp-card');const place=()=>{const r=card?.getBoundingClientRect();b.style.bottom=`${r&&r.height?Math.max(0,innerHeight-r.top+6):130}px`};place();requestAnimationFrame(place);
    b.classList.add('gv-visible');
}
gvInstallEarthDistanceBanner();

// ============================================================================
// SECTION 042 — HOME EARTH POINTER / WE ARE HERE
// ECO: GV200-001
// ============================================================================
function installHomeEarthPointer(){
    if(document.getElementById('gv-we-are-here'))return;
    const style=document.createElement('style');
    style.id='gv200001-home-earth-style';
    style.textContent=`
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease;font-family:"GV Space Age",sans-serif}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 18px);bottom:auto;height:calc(25% - 18px);width:1px;min-height:36px;transform:translateX(-50%);background:rgba(124,203,255,.88);box-shadow:0 0 8px rgba(88,191,255,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.75))}
#gv-we-are-here .gv-home-label{position:absolute;overflow:hidden;left:50%;top:75%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(124,203,255,.88);border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.94),rgba(11,49,119,.88),rgba(41,109,189,.78));color:#EAF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(88,191,255,.58);box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72),0 0 18px rgba(20,116,219,.35)}
#gv-we-are-here .gv-home-label::before{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.34) 0%,rgba(118,225,255,.08) 25%,transparent 44%);pointer-events:none}\n#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#7CCBFF;font:400 15px/1.2 "GV Space Age",sans-serif;letter-spacing:1.25px}
#gv-we-are-here .gv-earth-icon{position:relative;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:drop-shadow(0 0 2px rgba(87,255,147,.34))}
#gv-we-are-here .gv-earth-icon::before{content:"";position:absolute;left:50%;top:50%;width:31px;height:31px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(87,255,147,.27) 0%,rgba(77,255,143,.13) 46%,rgba(77,255,143,0) 76%);filter:blur(3px);z-index:-1}
#gv-we-are-here .gv-home-sub{margin-top:4px;color:#CDEEFF;font:400 10px/1.3 "GV Space Age",sans-serif;letter-spacing:1px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#A6DFFF;font:400 9px/1.3 "GV Space Age",sans-serif;letter-spacing:.8px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
`;
    document.head.appendChild(style);
    const home=document.createElement('div');
    home.id='gv-we-are-here';
    home.setAttribute('aria-live','polite');
    home.innerHTML=
      '<div class="gv-home-leader" aria-hidden="true"></div>'+
      '<div class="gv-home-label">'+
        '<div class="gv-home-origin">'+
          '<span class="gv-earth-icon" aria-hidden="true">🌎</span>'+
          '<strong>WE ARE HERE</strong>'+
        '</div>'+
        '<div class="gv-home-sub">EARTH — MILKY WAY</div>'+
        '<div class="gv-home-hint">TAP START TO BEGIN</div>'+
      '</div>';
    document.getElementById('aladin-cosmic-command-test').appendChild(home);
}
gvSpaceAgeReady.then(()=>installHomeEarthPointer()).catch(error=>console.error('GV HOME EARTH POINTER FAILURE',error));




// ============================================================================
// SECTION 016 — INITIAL CAMERA STATE
// ECO: GV200-001
// ============================================================================
if(typeof aladin.setFrame==='function')aladin.setFrame('ICRSd');
if(typeof aladin.setRotation==='function')aladin.setRotation(HOME.rotation);
if(typeof aladin.gotoRaDec==='function')aladin.gotoRaDec(HOME.ra,HOME.dec);
if(typeof aladin.setFov==='function')aladin.setFov(HOME.fov);


// ============================================================================
// SECTION 017 — ALADIN PUBLIC REFERENCE
// ECO: GV200-001
// ============================================================================
window.aladin_cosmic_command_test=aladin;
const gvCosmicReveal=(()=>{
    let prepared=false,fired=false,veil=null,ctx=null,order=null,cols=0,count=0,cell=5;
    const prepare=()=>{
        if(prepared)return true;
        prepared=true;
        veil=document.createElement('canvas');
        veil.id='gv-cosmic-reveal';
        Object.assign(veil.style,{position:'fixed',inset:'0',width:'100vw',height:'100vh',zIndex:'98000',pointerEvents:'none',background:'#000'});
        document.body.appendChild(veil);
        const dpr=window.devicePixelRatio||1,w=Math.max(1,Math.round(innerWidth*dpr)),h=Math.max(1,Math.round(innerHeight*dpr));
        veil.width=w;veil.height=h;ctx=veil.getContext('2d',{alpha:true});
        if(!ctx){veil.remove();veil=null;return false}
        ctx.fillStyle='#000';ctx.fillRect(0,0,w,h);
        veil.style.background='transparent';
        cols=Math.ceil(w/cell);const rows=Math.ceil(h/cell);count=cols*rows;order=new Uint32Array(count);
        for(let i=0;i<count;i++)order[i]=i;
        for(let i=count-1;i>0;i--){const j=(Math.random()*(i+1))|0,t=order[i];order[i]=order[j];order[j]=t}
        return true;
    };
    const start=()=>{
        if(fired)return;
        fired=true;
        if(!prepared&&!prepare())return;
        if(!veil||!ctx)return;
        let cursor=0,startTime=0;
        const frame=now=>{
            if(!startTime)startTime=now;
            const elapsed=Math.min(2000,now-startTime),target=Math.floor(count*(elapsed/2000));
            for(;cursor<target;cursor++){const n=order[cursor],x=(n%cols)*cell,y=Math.floor(n/cols)*cell;ctx.clearRect(x,y,cell,cell)}
            if(elapsed<2000)requestAnimationFrame(frame);else veil.remove();
        };
        requestAnimationFrame(frame);
        setTimeout(()=>veil?.remove(),2400);
    };
    return {prepare,start};
})();

// ============================================================================
// SECTION 018 — GALAXY VIEWER MODULE LOAD
// ECO: GV200-001
// ============================================================================
await loadScript(fresh(config.hamburgerBaseUrl));
await Promise.all([
    loadScript(fresh(config.coordinateUrl)).catch(error=>console.error('COORDINATE OVERLAY LOAD FAILED',error)),
    loadScript(fresh(config.targetUrl)),
    loadScript(fresh(config.galaxyRouteEngineUrl)),
    loadScript(fresh(config.galaxyNavigatorUrl)),
    loadScript(fresh(config.headsUpDisplayUrl)),
    loadScript(fresh(config.travelPresentationUrl)),
    loadScript(fresh(config.destinationPresentationUrl))
]);


// ============================================================================
// SECTION 019 — REQUIRED MODULE EXPORT VALIDATION
// ECO: GV200-001
// ============================================================================
if(window.GalaxyViewerHamburgerMenu?.version!=='0009')throw new Error('HAMBURGER 0009 EXPORT MISSING');
if(window.GalaxyCoordinateOverlay&&window.GalaxyCoordinateOverlay.VERSION!=='0006')console.error('COORDINATE 0006 EXPORT INVALID');
if(window.GalaxyViewerTargetSimbad?.version!=='0005')throw new Error('TARGET 0005 EXPORT MISSING');
/* GV014: diagnostics intentionally not loaded. */
if(window.GalaxyRouteEngine?.VERSION!=='0002')throw new Error('GALAXY ROUTE ENGINE 002 EXPORT MISSING');
if(window.GalaxyNavigator?.VERSION!=='001'||typeof window.GalaxyNavigator.mount!=='function')throw new Error('GALAXY NAVIGATOR 001 EXPORT MISSING');
if(window.GalaxyViewerHeadsUpDisplay?.VERSION!=='0001'||typeof window.GalaxyViewerHeadsUpDisplay.mount!=='function')throw new Error('HEADS-UP DISPLAY 0001 EXPORT MISSING');
if(typeof window.GalaxyRandomTravelPresentation?.mount!=='function')throw new Error('RANDOM TRAVEL PRESENTATION EXPORT MISSING');
if(window.GalaxyDestinationPresentation?.VERSION!=='0017'||typeof window.GalaxyDestinationPresentation.mount!=='function')throw new Error('DESTINATION PRESENTATION 0017 EXPORT MISSING');
// Navigator is presentation: mount immediately. Route preparation must never block its appearance.
const earlyNavigationHost=document.getElementById('gv-navigation-host');
if(!earlyNavigationHost)throw new Error('REQUIRED HOST MISSING: navigation');
const galaxyNavigator=window.GalaxyNavigator.mount(earlyNavigationHost,{
    onBack:()=>navigateBack(),
    onRandom:()=>navigateRandom(),
    onForward:()=>navigateForward()
});
// References acquired at immediate Navigator mount.
galaxyNavigator.setEnabled({back:false,random:false,forward:false});
galaxyNavigator.setBusy(true);

const gvVersionReadout=document.createElement('div');
gvVersionReadout.id='gv-version-readout';
gvVersionReadout.textContent=`${VERSION.replace(/^GV-beta-/,'')}   BLD ${GV200001_BUILD}   RT ${GV_RUNTIME}`;
Object.assign(gvVersionReadout.style,{position:'fixed',left:'50%',bottom:'59px',transform:'translate(-50%,50%)',display:'block',width:'min(430px,calc(100vw - 20px))',height:'8px',font:'400 8px/8px "GV Space Age",sans-serif',letterSpacing:'.3px',color:'#9edcff',textAlign:'center',margin:'0',padding:'0',border:'0',background:'transparent',boxShadow:'none',pointerEvents:'none',zIndex:'7361'});
document.body.appendChild(gvVersionReadout);


// ============================================================================
// SECTION 020 — MINIMAL ALADIN BOOT GATE
// ECO: GV200-001
// ============================================================================
if(!aladin)throw new Error('ALADIN VIEWER INITIALIZATION FAILED');


// ============================================================================
// SECTION 021 — DOM HOST ACQUISITION
// ECO: GV200-001
// ============================================================================
const hosts=Object.freeze({
    hamburger:document.getElementById('gv-hamburger-host'),
    coordinate:document.getElementById('gv-coordinate-host'),
    target:document.getElementById('gv-target-host'),
    navigation:document.getElementById('gv-navigation-host')
});


// ============================================================================
// SECTION 022 — DOM HOST VALIDATION
// ECO: GV200-001
// ============================================================================
for(const [name,host] of Object.entries(hosts)){
    if(!host)throw new Error(`REQUIRED HOST MISSING: ${name}`);
}


// ============================================================================
// SECTION 023 — HAMBURGER 0007 INITIALIZATION
// ECO: GV200-001
// ============================================================================
const GV_DOE_RATES=Object.freeze([20,60,120]);
let gvDoeRate=20;
const gvDoeReports={20:[],60:[],120:[]};
let gvDoeActiveRun=null;
function gvDoeNow(){return performance.now()}
function gvDoeBeginRun(meta){
    const run={schema:'gv-flight-doe-0001',build:GV200001_BUILD,rateHz:gvDoeRate,startedAt:gvDoeNow(),meta:{...meta},browserRaf:[],aladinRedraw:[],commands:[]};
    gvDoeActiveRun=run;return run;
}
function gvDoeCommand(type,args){if(type==='setRotation'){const rotation=Number(args?.[0]);if(Number.isFinite(rotation))gvAuthoritativeRotation=rotation}if(gvDoeActiveRun)gvDoeActiveRun.commands.push({t:gvDoeNow()-gvDoeActiveRun.startedAt,type,args})}
function gvDoeFinishRun(run){
    if(gvDoeActiveRun===run)gvDoeActiveRun=null;
    run.endedAt=gvDoeNow();run.durationMs=run.endedAt-run.startedAt;
    gvDoeReports[run.rateHz]?.push(run);return run;
}
function gvDoeDownload(rate){
    const selected=Number(rate);
    const payload={schema:'gv-flight-doe-report-0001',viewer:VERSION,build:GV200001_BUILD,aladinVersion:config.aladinVersion,selectedRateHz:selected,generatedAt:new Date().toISOString(),runs:gvDoeReports[selected]||[]};
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download=`GV_DOE_${selected}Hz_BLD${GV200001_BUILD}_${Date.now()}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
}
try{
    const view=aladin.view;
    if(view&&typeof view.redrawClbk==='function'&&!view.__gvDoeWrapped){
        const original=view.redrawClbk;
        view.redrawClbk=function(now){
            if(gvDoeActiveRun)gvDoeActiveRun.aladinRedraw.push({t:gvDoeNow()-gvDoeActiveRun.startedAt,rafNow:Number(now),rendering:typeof view.wasm?.isRendering==='function'?!!view.wasm.isRendering():null});
            return original(now);
        };
        view.__gvDoeWrapped=true;
    }
}catch(error){console.error('GV DOE ALADIN REDRAW PROBE FAILED',error)}

const GV_ABOUT_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/modules/about/gv-about-presentation-0013.js';
let gvAboutPromise=null;
async function gvOpenAbout(){
    hamburger?.close?.();
    if(!gvAboutPromise)gvAboutPromise=loadScript(fresh(GV_ABOUT_URL)).then(()=>{
        if(window.GalaxyViewerAbout?.VERSION!=='0013'||typeof window.GalaxyViewerAbout.mount!=='function')throw new Error('ABOUT PRESENTATION 0013 EXPORT MISSING');
        return window.GalaxyViewerAbout.mount(document.getElementById('aladin-cosmic-command-test'));
    }).catch(error=>{gvAboutPromise=null;throw error});
    (await gvAboutPromise).open();
}

let gvGridEnabled=false;
const hamburger=window.GalaxyViewerHamburgerMenu.init({
    host:hosts.hamburger,
    onMenuAction(action){
        if(action==='DIAGNOSTICS')window.GalaxyViewerDiagnostics?.open?.();
        if(action==='GRID'){
            gvGridEnabled=!gvGridEnabled;
            try{aladin.setCooGrid?.({enabled:gvGridEnabled,color:'#79DFFF',opacity:.64,thickness:1,labelSize:12})}catch(error){console.error('GV GRID TOGGLE FAILED',error)}
        }
        if(action==='RETICLE OFF'||action==='RETICLE ON'){
            const visible=action==='RETICLE ON';
            reticle.style.display=visible?'block':'none';
        }
        if(action==='ABOUT'){
            gvOpenAbout().catch(error=>console.error('GALAXY VIEWER ABOUT OPEN FAILED',error));
        }
    },
    onProjectionSelected(name,detail){
        if(typeof aladin.setProjection==='function')aladin.setProjection(detail.code);
    }
});
hamburger.root.style.position='absolute';
hamburger.root.style.inset='0';
hamburger.root.style.width='100%';
hamburger.root.style.height='100%';
hamburger.root.style.pointerEvents='none';
hamburger.menuButton.style.pointerEvents='auto';
hamburger.root.addEventListener('gv-doe-rate-selected',event=>{
    const rate=Number(event.detail?.rate);
    if(GV_DOE_RATES.includes(rate))gvDoeRate=rate;
});
hamburger.root.addEventListener('gv-doe-download',event=>gvDoeDownload(Number(event.detail?.rate)));


// ============================================================================
// SECTION 024 — COORDINATE OVERLAY 0006 INITIALIZATION
// ECO: GV200-001
// ============================================================================
let coordinate=null;
try{
    if(window.GalaxyCoordinateOverlay?.mount){
        coordinate=window.GalaxyCoordinateOverlay.mount(hosts.coordinate,{});
        coordinate.ready.then(()=>{
            coordinate.setFrame('ICRSd');
            coordinate.update(HOME.ra,HOME.dec);
        }).catch(error=>console.error('COORDINATE OVERLAY READY FAILED',error));
    }
}catch(error){console.error('COORDINATE OVERLAY MOUNT FAILED',error)}
function gvSyncCoordinateFromAladin(){
    try{
        const size=aladin.getSize?.(),center=Array.isArray(size)&&size.length>=2?aladin.pix2world?.(Number(size[0])/2,Number(size[1])/2):aladin.getRaDec?.();
        if(coordinate&&Array.isArray(center)&&Number.isFinite(Number(center[0]))&&Number.isFinite(Number(center[1])))coordinate.update(Number(center[0]),Number(center[1]));
    }catch(_){}
    requestAnimationFrame(gvSyncCoordinateFromAladin);
}
requestAnimationFrame(gvSyncCoordinateFromAladin);


// ============================================================================
// SECTION 025 — TARGET / SIMBAD 0004 INITIALIZATION
// ECO: GV200-001
// ============================================================================
const target=await window.GalaxyViewerTargetSimbad.init({
    host:hosts.target,
    aladin
});


// ============================================================================
// SECTION 026 — DIAGNOSTICS 0019 INITIALIZATION
// ECO: GV200-001
// ============================================================================
const diagnostics=null;


// ============================================================================
// SECTION 027 — NAVIGATION RUNTIME CONTRACT
// ECO: GV200-001
// ============================================================================
const navigationRuntime=window.GalaxyRouteEngine;
if(typeof navigationRuntime.initialize!=='function')throw new Error('NAVIGATION initialize() MISSING');
if(typeof navigationRuntime.snapshot!=='function')throw new Error('NAVIGATION snapshot() MISSING');


// ============================================================================
// SECTION 028 — NAVIGATION RUNTIME INITIALIZATION
// ECO: GV200-001
// ============================================================================
const navigationState=await navigationRuntime.initialize();


// ============================================================================
// SECTION 029 — NAVIGATION RUNTIME STATE GATE
// ECO: GV200-001
// ============================================================================
const runtimeState=navigationRuntime.snapshot();
if(runtimeState.phase!=='READY')throw new Error(`NAVIGATION NOT READY: ${runtimeState.phase}`);
if(runtimeState.active!==100)throw new Error(`NAVIGATION ACTIVE INVALID: ${runtimeState.active}`);
if(runtimeState.reserve!==30)throw new Error(`NAVIGATION RESERVE INVALID: ${runtimeState.reserve}`);
if(runtimeState.excluded!==130)throw new Error(`NAVIGATION EXCLUSION INVALID: ${runtimeState.excluded}`);
galaxyNavigator.setBusy(false);
galaxyNavigator.setEnabled({back:false,random:true,forward:false});
galaxyNavigator.setStart?.(true);


// ============================================================================
// SECTION 030 — NAVIGATION RUNTIME PUBLIC EXPOSURE
// ECO: GV200-001
// ============================================================================
window.GalaxyViewerRuntime=Object.freeze({
    viewerVersion:VERSION,
    navigationVersion:navigationRuntime.VERSION,
    get navigationState(){return navigationRuntime.snapshot()}
});


// ============================================================================
// SECTION 031 — NAVIGATION CONTROL MARKUP
// ECO: GV200-001
// ============================================================================
// Mounted immediately after module validation so Route Engine preparation cannot delay UI.


// ============================================================================
// SECTION 032 — NAVIGATION CONTROL REFERENCES
// ECO: GV200-001
// ============================================================================
const backButton=galaxyNavigator.back;
const randomButton=galaxyNavigator.random;
const forwardButton=galaxyNavigator.forward;


// ============================================================================
// SECTION 033 — TEST HISTORY STATE
// ECO: GV200-001
// ============================================================================
const history=[];
let historyIndex=-1;
let routeIndex=0;
let navigationInFlight=false;
let activeDestination=null;
const randomGalaxyBridge=Object.freeze({
    get activeDestination(){return activeDestination},
    get currentDestination(){return activeDestination},
    getState(){return {activeDestination,currentDestination:activeDestination}}
});
window.GalaxyRandomGalaxy=randomGalaxyBridge;
const travelPresentation=window.GalaxyRandomTravelPresentation.mount(document.getElementById('aladin-cosmic-command-test'));
const destinationPresentation=window.GalaxyDestinationPresentation.mount(document.getElementById('aladin-cosmic-command-test'));
const headsUpDisplay=window.GalaxyViewerHeadsUpDisplay.mount(document.getElementById('aladin-cosmic-command-test'),{
    routeEngine:navigationRuntime,
    randomGalaxy:randomGalaxyBridge
});

// ============================================================================
// SECTION 033A — DIRECT ARRIVAL HD OVERLAY / VIGNETTE LAB
// ECO: GV200-001 BUILD 0037
// Presentation only: vignette + CROSS FADE + spring-loaded ZOOM.
// Navigation remains sole owner of destination RA/Dec/FOV/orientation.
// ============================================================================
const DIRECT_HD_LAYER='GV_DIRECT_HD_0056';
const CANVAS_IMAGE_PROXY='https://gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev/api/image?url=';
const MAX_BLEND_DIMENSION=2048;
const VIGNETTE=Object.freeze({diameter:1.04,core:0.72,mid1:0.42,mid2:0.72,mid3:0.90,alpha1:0.90,alpha2:0.52,alpha3:0.16});
let directHdOverlay=null;
let directHdDestination=null;
// BUILD 0014 — bounded ownership of Galaxy Viewer-created HD object URLs.
// Navigation/catalog history remains unlimited and lightweight; this bank never retains blobs or Aladin layers.
const GV_HD_RESOURCE_WINDOW=10;
const gvHdObjectUrls=[];
function gvTrackHdObjectUrl(url){
    gvHdObjectUrls.push(url);
    while(gvHdObjectUrls.length>GV_HD_RESOURCE_WINDOW){
        const stale=gvHdObjectUrls.shift();
        try{URL.revokeObjectURL(stale)}catch(_){}
    }
}
function gvReleaseHdObjectUrl(url){
    const index=gvHdObjectUrls.indexOf(url);
    if(index>=0)gvHdObjectUrls.splice(index,1);
    try{URL.revokeObjectURL(url)}catch(_){}
}
const GV_MASTER_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/gv-master-catalog.json';
const GV_AVM_RUNTIME_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0001.json';
let gvAvmRuntimePromise=null;
async function gvLoadAvmRuntimeCatalog(){
    if(!gvAvmRuntimePromise){
        gvAvmRuntimePromise=fetch(fresh(GV_AVM_RUNTIME_CATALOG_URL),{cache:'force-cache'})
            .then(response=>{if(!response.ok)throw new Error('GV AVM RUNTIME CATALOG HTTP '+response.status);return response.json()})
            .then(payload=>{
                const records=Array.isArray(payload)?payload:payload?.records;
                if(!Array.isArray(records)||records.length!==1871)throw new Error('GV AVM RUNTIME CATALOG INVALID');
                const byUrl=new Map(),byId=new Map();
                for(const record of records){
                    const url=String(record?.imageUrl||'').trim().toLowerCase();
                    const id=String(record?.archiveId||'').trim().toLowerCase();
                    if(url)byUrl.set(url,record);
                    if(id)byId.set(id,record);
                }
                return Object.freeze({records,byUrl,byId});
            });
    }
    return gvAvmRuntimePromise;
}
async function gvRuntimeAvmRecord(destination){
    const catalog=await gvLoadAvmRuntimeCatalog();
    const url=directHdUrl(destination).toLowerCase();
    const id=String(destination?.archiveId||destination?.id||destination?.providerId||'').trim().toLowerCase();
    const record=catalog.byId.get(id)||catalog.byUrl.get(url);
    if(!record)throw new Error('GV AVM RUNTIME RECORD MISSING: '+(id||url));
    return record;
}
function gvSyntheticWcsFromRuntimeRecord(record,width,height){
    const ra=Number(record?.ra),dec=Number(record?.dec);
    const fovX=Number(record?.fovXDegrees??record?.fovDegrees);
    const fovY=Number(record?.fovYDegrees??record?.fovDegrees);
    const rotation=Number(record?.aladinRotation??record?.spatialRotationDeg);
    if(!Number.isFinite(ra)||!Number.isFinite(dec))throw new Error('GV JSON WCS CENTER INVALID');
    if(!Number.isFinite(fovX)||fovX<=0||!Number.isFinite(fovY)||fovY<=0)throw new Error('GV JSON WCS FOV INVALID');
    if(!Number.isFinite(rotation))throw new Error('GV JSON WCS ROTATION INVALID');
    if(!Number.isFinite(width)||width<=0||!Number.isFinite(height)||height<=0)throw new Error('GV JSON WCS DIMENSION INVALID');
    const sx=fovX/width,sy=fovY/height,t=rotation*Math.PI/180,c=Math.cos(t),s=Math.sin(t);
    const referencePixel=record?.referencePixel,referenceDimension=record?.referenceDimension;
    const rawCrpix1=Number(referencePixel?.[0]),rawCrpix2=Number(referencePixel?.[1]);
    const rawWidth=Number(referenceDimension?.[0]),rawHeight=Number(referenceDimension?.[1]);
    const crpix1=Number.isFinite(rawCrpix1)&&Number.isFinite(rawWidth)&&rawWidth>0?rawCrpix1*(width/rawWidth):(width+1)/2;
    const crpix2=Number.isFinite(rawCrpix2)&&Number.isFinite(rawHeight)&&rawHeight>0?rawCrpix2*(height/rawHeight):(height+1)/2;
    return {
        NAXIS:2,CTYPE1:'RA---TAN',CTYPE2:'DEC--TAN',EQUINOX:2000,LONPOLE:180,LATPOLE:dec,CUNIT1:'deg',CUNIT2:'deg',
        CRVAL1:ra,CRVAL2:dec,CRPIX1:crpix1,CRPIX2:crpix2,
        CD1_1:-sx*c,CD1_2:-sy*s,CD2_1:-sx*s,CD2_2:sy*c,
        NAXIS1:width,NAXIS2:height
    };
}
function gvTanPixelToWorld(wcs,x,y){
    const d2r=Math.PI/180,r2d=180/Math.PI;
    const dx=Number(x)-Number(wcs.CRPIX1),dy=Number(y)-Number(wcs.CRPIX2);
    const xi=(Number(wcs.CD1_1)*dx+Number(wcs.CD1_2)*dy)*d2r;
    const eta=(Number(wcs.CD2_1)*dx+Number(wcs.CD2_2)*dy)*d2r;
    const ra0=Number(wcs.CRVAL1)*d2r,dec0=Number(wcs.CRVAL2)*d2r;
    const denom=Math.cos(dec0)-eta*Math.sin(dec0);
    let ra=ra0+Math.atan2(xi,denom);
    const dec=Math.atan2(Math.sin(dec0)+eta*Math.cos(dec0),Math.sqrt(denom*denom+xi*xi));
    ra=((ra*r2d)%360+360)%360;
    return [ra,dec*r2d];
}
function gvControlPanel(id,title,side){
    const panel=document.createElement('div');
    panel.id=id;
    Object.assign(panel.style,{
        position:'absolute',[side]:'-4px',top:'calc(50% - 79px)',zIndex:'7312',
        width:'57px',height:'158px',borderRadius:'18px',
        background:'rgba(0,22,54,.12)',pointerEvents:'auto',touchAction:'none',
        fontFamily:'"GV Space Age","Space Age",Arial,sans-serif',color:'#9eefff',
        filter:'drop-shadow(0 0 10px rgba(76,205,255,.82))'
    });
    panel.innerHTML='<div class="gv-lab-title">'+title+'</div><div class="gv-lab-rail"></div><div class="gv-lab-thumb"></div><div class="gv-lab-hit"></div>';
    const titleNode=panel.querySelector('.gv-lab-title');
    const rail=panel.querySelector('.gv-lab-rail');
    const thumb=panel.querySelector('.gv-lab-thumb');
    const hit=panel.querySelector('.gv-lab-hit');
    Object.assign(titleNode.style,{position:'absolute',left:side==='left'?'11px':'39px',top:'50%',transform:'translate(-50%,-50%)',height:'108px',display:'flex',alignItems:'center',justifyContent:'center',writingMode:'vertical-rl',textOrientation:'mixed',font:'400 6px/1 "GV Space Age","Space Age",Arial,sans-serif',letterSpacing:'1.5px',color:'#6feaff',textShadow:'0 0 4px rgba(190,250,255,.96),0 0 10px rgba(35,190,255,.9)',userSelect:'none',pointerEvents:'none',whiteSpace:'nowrap'});
    Object.assign(rail.style,{position:'absolute',left:side==='left'?'27px':'20px',top:'14px',width:'10px',height:'131px',borderRadius:'999px',background:'linear-gradient(180deg,rgba(18,187,255,.95),rgba(4,18,58,.82))',boxShadow:'0 0 8px rgba(100,226,255,.88),0 0 18px rgba(18,157,255,.72)',pointerEvents:'none'});
    Object.assign(thumb.style,{position:'absolute',left:side==='left'?'32px':'25px',top:'145px',width:'18px',height:'18px',borderRadius:'50%',transform:'translate(-50%,-50%)',background:'#72e8ff',border:'2px solid rgba(224,255,255,.98)',boxShadow:'0 0 12px rgba(185,250,255,.98),0 0 28px rgba(20,176,255,.82)',pointerEvents:'none'});
    Object.assign(hit.style,{position:'absolute',inset:'0',zIndex:'3',pointerEvents:'auto',touchAction:'none',background:'transparent'});
    document.getElementById('aladin-cosmic-command-test').appendChild(panel);
    return {panel,rail,thumb,hit};}

const crossFadeControl=gvControlPanel('gv-cross-fade','CROSS FADE','left');
const crossFadeInput=document.createElement('input');
crossFadeInput.type='range';crossFadeInput.min='0';crossFadeInput.max='100';crossFadeInput.step='1';crossFadeInput.value='0';
crossFadeInput.setAttribute('aria-label','CROSS FADE');
Object.assign(crossFadeInput.style,{position:'absolute',left:'9px',top:'14px',width:'39px',height:'131px',opacity:'.001',appearance:'none',WebkitAppearance:'none',pointerEvents:'none',touchAction:'none'});
crossFadeControl.panel.appendChild(crossFadeInput);

function directHdUrl(destination){return String(destination?.selectedImageUrl??destination?.imageUrl??destination?.hdUrl??'').trim()}
function directHdOpacity(){return Math.max(0.01,Math.min(1,1-(Number(crossFadeInput.value||0)/100)))}
function updateCrossFadeThumb(){
    const v=Math.max(0,Math.min(100,Number(crossFadeInput.value||0)));
    crossFadeControl.thumb.style.top=`${crossFadeControl.rail.offsetTop+((100-v)/100)*crossFadeControl.rail.offsetHeight}px`;
}
function applyDirectHdOpacity(){
    const value=directHdOpacity();
    const target=directHdOverlay||aladin.getOverlayImageLayer?.(DIRECT_HD_LAYER);
    try{target?.setOpacity?.(value)}catch(_){}
    try{target?.setAlpha?.(value)}catch(_){}
    try{target?.setOptions?.({opacity:value})}catch(_){}
    if(target?.options)try{target.options.opacity=value}catch(_){}
    updateCrossFadeThumb();
    return value;
}
function setCrossFadeFromY(clientY){
    const r=crossFadeControl.rail.getBoundingClientRect();if(!r.height)return;
    crossFadeInput.value=String(Math.max(0,Math.min(100,Math.round(((r.bottom-clientY)/r.height)*100))));
    applyDirectHdOpacity();
}
let crossFadePointer=null;
crossFadeControl.hit.addEventListener('pointerdown',e=>{
    e.preventDefault();e.stopPropagation();crossFadePointer=e.pointerId;
    try{crossFadeControl.hit.setPointerCapture?.(e.pointerId)}catch(_){}
    setCrossFadeFromY(e.clientY);
},{passive:false});
crossFadeControl.hit.addEventListener('pointermove',e=>{
    if(crossFadePointer!==e.pointerId)return;
    e.preventDefault();e.stopPropagation();setCrossFadeFromY(e.clientY);
},{passive:false});
for(const ev of ['pointerup','pointercancel'])crossFadeControl.hit.addEventListener(ev,e=>{
    if(crossFadePointer!==e.pointerId)return;
    e.stopPropagation();
    try{crossFadeControl.hit.releasePointerCapture?.(e.pointerId)}catch(_){}
    crossFadePointer=null;
},{passive:true});
crossFadeInput.addEventListener('input',applyDirectHdOpacity);
updateCrossFadeThumb();

const zoomControl=gvControlPanel('gv-spring-zoom','ZOOM','right');
zoomControl.thumb.style.top='79px';
const gvFovReadout=document.createElement('div');
gvFovReadout.innerHTML='<span id="gv-fov-title"><span id="gv-fov-f">F</span><span id="gv-fov-rest">OV °</span></span><span id="gv-fov-int">360</span><span id="gv-fov-dot">.</span><span id="gv-fov-frac">000</span>';
Object.assign(gvFovReadout.style,{position:'absolute',right:'2px',top:'calc(50% - 108px)',zIndex:'7313',width:'62px',height:'16.2px',padding:'0',border:'1px solid rgba(124,203,255,.92)',borderRadius:'4px',background:'linear-gradient(145deg,rgba(4,20,48,.96),rgba(12,52,116,.96))',boxShadow:'0 0 5px rgba(158,230,255,.95),0 0 12px rgba(46,172,255,.72)',font:'400 8.6px/16.2px "GV Space Age","Space Age",Arial,sans-serif',letterSpacing:'.3px',color:'#8fe7ff',textShadow:'0 0 3px #d8f8ff,0 0 8px rgba(66,195,255,.95)',whiteSpace:'nowrap',pointerEvents:'none'});Object.assign(gvFovReadout.querySelector('#gv-fov-title').style,{position:'absolute',left:'50%',top:'-14px',transform:'translateX(-50%)',lineHeight:'9px',fontSize:'7.2px',color:'#8fe7ff'});Object.assign(gvFovReadout.querySelector('#gv-fov-f').style,{position:'relative',left:'4px'});Object.assign(gvFovReadout.querySelector('#gv-fov-rest').style,{position:'relative',left:'4px'});Object.assign(gvFovReadout.querySelector('#gv-fov-int').style,{position:'absolute',right:'32px',width:'25.2px',textAlign:'right',fontVariantNumeric:'tabular-nums'});Object.assign(gvFovReadout.querySelector('#gv-fov-dot').style,{position:'absolute',left:'29px',width:'4px',textAlign:'center'});Object.assign(gvFovReadout.querySelector('#gv-fov-frac').style,{position:'absolute',left:'33px',width:'21.6px',textAlign:'left',fontVariantNumeric:'tabular-nums'});
document.getElementById('aladin-cosmic-command-test').appendChild(gvFovReadout);
function gvSetFovDigits(element,value,digitWidth){
    if(element.dataset.gvDigits===value)return;
    element.dataset.gvDigits=value;
    element.replaceChildren(...Array.from(value,digit=>{
        const slot=document.createElement('span');
        Object.assign(slot.style,{display:'inline-block',width:digitWidth,textAlign:'center'});
        slot.textContent=digit;
        return slot;
    }));
}
let gvDisplayedFov=null;
const GV_FOV_REPORT_MS=400;
const GV_FOV_REPORT_HYSTERESIS=0.001;
function gvSyncFovReadout(){
    try{
        const raw=aladin.getFov?.(),fov=Number(Array.isArray(raw)?raw[0]:raw);
        if(Number.isFinite(fov)&&fov>=0){
            if(gvDisplayedFov===null||Math.abs(fov-gvDisplayedFov)>=GV_FOV_REPORT_HYSTERESIS)gvDisplayedFov=Number(fov.toFixed(3));
            const parts=gvDisplayedFov.toFixed(3).split('.');
            gvSetFovDigits(gvFovReadout.querySelector('#gv-fov-int'),parts[0].padStart(3,' '),'8.4px');
            gvSetFovDigits(gvFovReadout.querySelector('#gv-fov-frac'),parts[1],'7.2px');
        }
    }catch(_){}
}
gvSyncFovReadout();
setInterval(gvSyncFovReadout,GV_FOV_REPORT_MS);

let zoomCommand=0;
let zoomFrame=0;
let gvAutoZoom=null;
function gvSetZoomCommand(command){
    zoomCommand=Math.max(-1,Math.min(1,Number(command)||0));
    zoomControl.thumb.style.top=`${zoomControl.rail.offsetTop+((zoomCommand+1)/2)*zoomControl.rail.offsetHeight}px`;
}
function zoomStep(){
    zoomFrame=0;
    if(!zoomCommand)return;
    try{
        const raw=aladin.getFov?.(),current=Number(Array.isArray(raw)?raw[0]:raw);
        if(Number.isFinite(current)&&current>0){
            if(gvAutoZoom){
                const a=gvAutoZoom,elapsed=performance.now()-a.started;
                const attack=Math.min(1,elapsed/a.attackMs);
                const eta=Math.abs(Math.log(current/a.target)/0.018)*(1000/60);
                if(!a.approachStarted&&eta<=a.approachMs){a.approachStarted=true;try{a.onApproach?.()}catch(error){console.error('GV ZOOM APPROACH CALLBACK FAILED',error)}}
                let level=attack;
                if(a.linearLanding&&eta<=a.landingMs)level=Math.min(level,Math.max(0.035,eta/a.landingMs));
                gvSetZoomCommand(a.direction*Math.max(0.035,Math.min(1,level)));
                if((a.direction<0&&current>=a.target)||(a.direction>0&&current<=a.target)||Math.abs(a.target-current)<=Math.max(1e-7,a.target*.001)){
                    aladin.setFov(a.target);const done=a.resolve;gvAutoZoom=null;gvSetZoomCommand(0);done(true);return;
                }
            }
            aladin.setFov(Math.max(.0001,Math.min(360,current*Math.exp(-zoomCommand*.018))));
        }
    }catch(_){}
    zoomFrame=requestAnimationFrame(zoomStep);
}
function gvSettleAutoZoom(result=false){
    if(!gvAutoZoom)return;
    const done=gvAutoZoom.resolve;gvAutoZoom=null;
    try{done(result)}catch(_){}
}
function gvEnergizeZoomJoystick(command,targetFov,{attackMs=500,landingMs=2500,approachMs=500,linearLanding=true,onApproach=null}={}){
    const target=Number(targetFov),direction=Math.sign(Number(command));
    if(!Number.isFinite(target)||target<=0||!direction)return Promise.resolve(false);
    const raw=aladin.getFov?.(),start=Number(Array.isArray(raw)?raw[0]:raw);
    if(!Number.isFinite(start)||start<=0)return Promise.resolve(false);
    gvSettleAutoZoom(false);
    return new Promise(resolve=>{gvAutoZoom={target,start,direction,started:performance.now(),attackMs,landingMs,approachMs,linearLanding,onApproach,approachStarted:false,resolve};gvSetZoomCommand(direction*.035);if(!zoomFrame)zoomFrame=requestAnimationFrame(zoomStep)});
}
function gvTimedZoomToTarget(targetFov,{durationMs=null,attackMs=500,releaseMs=500}={}){
    const target=Number(targetFov),raw=aladin.getFov?.(),start=Number(Array.isArray(raw)?raw[0]:raw);
    if(!Number.isFinite(target)||target<=0||!Number.isFinite(start)||start<=0)return Promise.resolve(false);
    gvSettleAutoZoom(false);
    if(zoomFrame){cancelAnimationFrame(zoomFrame);zoomFrame=0}
    const direction=target>start?-1:1,logDistance=Math.abs(Math.log(target/start));
    const naturalMs=(logDistance/(.018*60))*1000+(attackMs+releaseMs)/2;
    const totalMs=Math.max(attackMs+releaseMs+1,Number.isFinite(durationMs)?durationMs:naturalMs);
    const cruiseMs=Math.max(0,totalMs-attackMs-releaseMs);
    const totalArea=(attackMs/2)+cruiseMs+(releaseMs/2);
    return new Promise(resolve=>{
        const started=performance.now();
        function frame(now){
            const elapsed=Math.min(totalMs,now-started);
            let level,area;
            if(elapsed<attackMs){
                level=elapsed/attackMs;area=elapsed*elapsed/(2*attackMs);
            }else if(elapsed<attackMs+cruiseMs){
                level=1;area=(attackMs/2)+(elapsed-attackMs);
            }else{
                const u=Math.min(releaseMs,elapsed-attackMs-cruiseMs);
                level=Math.max(0,1-u/releaseMs);
                area=(attackMs/2)+cruiseMs+u-u*u/(2*releaseMs);
            }
            const progress=totalArea>0?Math.max(0,Math.min(1,area/totalArea)):1;
            gvSetZoomCommand(direction*Math.min(.8,level));
            aladin.setFov(start*Math.exp(Math.log(target/start)*progress));
            if(elapsed<totalMs)requestAnimationFrame(frame);
            else{gvSetZoomCommand(0);resolve(true)}
        }
        requestAnimationFrame(frame);
    });
}
function setZoomCommandFromY(clientY){
    const r=zoomControl.rail.getBoundingClientRect();
    if(!r.height)return;
    gvSettleAutoZoom(false);
    gvSetZoomCommand(((clientY-(r.top+r.height/2))/(r.height/2)));
    if(!zoomFrame)zoomFrame=requestAnimationFrame(zoomStep);
}
function releaseZoom(){
    gvSettleAutoZoom(false);
    gvSetZoomCommand(0);
    if(zoomFrame){cancelAnimationFrame(zoomFrame);zoomFrame=0}
    zoomControl.thumb.style.top=`${zoomControl.rail.offsetTop+zoomControl.rail.offsetHeight/2}px`;
}
for(const ev of ['pointerdown','pointermove'])zoomControl.hit.addEventListener(ev,e=>{if(ev==='pointermove'&&e.buttons===0)return;e.preventDefault();e.stopPropagation();setZoomCommandFromY(e.clientY)},{passive:false});
for(const ev of ['pointerup','pointercancel','pointerleave'])zoomControl.hit.addEventListener(ev,e=>{e.stopPropagation();releaseZoom()},{passive:true});

async function gvLoadGate2MImage(url){
    if(typeof createImageBitmap!=='function')throw new Error('createImageBitmap unavailable');
    const attempts=[url,CANVAS_IMAGE_PROXY+encodeURIComponent(url)+'&consumer=gv0037'];
    let last='';
    for(const source of attempts){
        try{
            const response=await fetch(source,{mode:'cors',credentials:'omit',cache:'no-store',redirect:'follow'});
            if(!response.ok)throw new Error('HTTP '+response.status);
            const blob=await response.blob();
            if(!blob||blob.size<=0)throw new Error('EMPTY IMAGE BLOB');
            const bitmap=await createImageBitmap(blob);
            try{
                const w=bitmap.width,h=bitmap.height;
                const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;
                const ctx=canvas.getContext('2d');if(!ctx)throw new Error('VIGNETTE 2D CONTEXT UNAVAILABLE');
                ctx.drawImage(bitmap,0,0,w,h);
                const p=VIGNETTE,cx=w/2,cy=h/2,actualAspect=Math.max(w/h,h/w),highAspect=actualAspect>1.3;
                if(highAspect){
                    const imageData=ctx.getImageData(0,0,w,h),d=imageData.data,dia=1.31,rx=w*.5*dia,ry=h*.5*dia;
                    const core=0.68,blend=0.24,decay=1.75;
                    for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++){
                        const i=(yy*w+xx)*4,ex=(xx-cx)/rx,ey=(yy-cy)/ry,er=Math.hypot(ex,ey);
                        const edgePx=Math.min(xx,yy,w-1-xx,h-1-yy),edgeNorm=edgePx/Math.max(1,Math.min(w,h)*.5);
                        const rectFade=Math.max(0,Math.min(1,edgeNorm/Math.max(.01,blend)));
                        const ellipseFade=er<=core?1:Math.max(0,1-(er-core)/Math.max(.001,1-core));
                        const t=Math.min(rectFade,ellipseFade),smooth=t*t*(3-2*t);
                        const expTail=(1-Math.exp(-Math.max(.1,decay)*t))/(1-Math.exp(-Math.max(.1,decay)));
                        const mix=Math.max(0,Math.min(1,blend*1.8)),alpha=(1-mix)*smooth+mix*expTail;
                        d[i+3]=Math.round(d[i+3]*Math.max(0,Math.min(1,alpha)));
                    }
                    ctx.putImageData(imageData,0,0);
                }else{
                    const r=Math.min(w,h)*.5*.96,core=0.68,mid1=0.78,mid2=0.88,mid3=0.95;
                    ctx.save();ctx.globalCompositeOperation='destination-in';
                    const mask=ctx.createRadialGradient(cx,cy,0,cx,cy,r);
                    mask.addColorStop(0,'rgba(0,0,0,1)');mask.addColorStop(core,'rgba(0,0,0,1)');
                    mask.addColorStop(mid1,'rgba(0,0,0,0.88)');mask.addColorStop(mid2,'rgba(0,0,0,0.48)');
                    mask.addColorStop(mid3,'rgba(0,0,0,0.12)');mask.addColorStop(1,'rgba(0,0,0,0)');
                    ctx.fillStyle=mask;ctx.fillRect(0,0,w,h);ctx.restore();
                }
                const vignetteBlob=await new Promise((resolve,reject)=>canvas.toBlob(value=>value?resolve(value):reject(new Error('VIGNETTE PNG ENCODE FAILED')),'image/png'));
                return {blob:vignetteBlob,width:w,height:h};
            }finally{try{bitmap.close?.()}catch(_){}}
        }catch(error){last=String(error?.message||error||'')}
    }
    throw new Error('GATE 2M IMAGE SOURCE FAILED: '+last);
}
async function gvPrepareDirectHd(destination,recordPromise=gvRuntimeAvmRecord(destination)){
    const record=await recordPromise;
    const url=directHdUrl(destination);
    if(!url)throw new Error('GV DESTINATION IMAGE URL MISSING');
    const fovX=Number(record.fovXDegrees??record.fovDegrees);
    const fovY=Number(record.fovYDegrees??record.fovDegrees);
    const rotation=Number(record.aladinRotation??record.spatialRotationDeg);
    const raster=await gvLoadGate2MImage(url);
    const imageObjectUrl=URL.createObjectURL(raster.blob);gvTrackHdObjectUrl(imageObjectUrl);
    const displayWcs=gvSyntheticWcsFromRuntimeRecord(record,raster.width,raster.height);
    const imageCenter=gvTanPixelToWorld(displayWcs,(raster.width+1)/2,(raster.height+1)/2);
    return {destination,record,imageObjectUrl,displayWcs,imageCenter,rotation,finalFov:Math.max(fovX,fovY)*1.0};
}
function gvInstallPreparedHd(prepared){
    const {destination,record,imageObjectUrl,displayWcs}=prepared;
    let resolveReady,rejectReady;
    const ready=new Promise((resolve,reject)=>{resolveReady=resolve;rejectReady=reject});
    directHdDestination=destination;
    const layer=A.image(imageObjectUrl,{
        name:DIRECT_HD_LAYER,imgFormat:'png',wcs:displayWcs,opacity:directHdOpacity(),
        successCallback:()=>{if(directHdDestination!==destination){resolveReady(false);return}directHdOverlay=layer;applyDirectHdOpacity();resolveReady(true);setTimeout(()=>gvReleaseHdObjectUrl(imageObjectUrl),30000)},
        errorCallback:error=>{gvReleaseHdObjectUrl(imageObjectUrl);rejectReady(error);console.error('GV DIRECT HD JSON-WCS LAYER LOAD FAILED',error)}
    });
    try{aladin.removeImageLayer?.(DIRECT_HD_LAYER)}catch(_){}
    directHdOverlay=layer;aladin.setOverlayImageLayer(layer,DIRECT_HD_LAYER);return ready;
}
function gvFlightClamp01(value){return Math.max(0,Math.min(1,Number(value)))}
function gvFlightNavigationSmootherstep(value){const t=gvFlightClamp01(value);return 35*t**4-84*t**5+70*t**6-20*t**7}
function gvFlightSmootherstep(value){const t=gvFlightClamp01(value);return t*t*t*(t*(t*6-15)+10)}
function gvFlightNormalizeRotationDelta(value){let angle=Number(value)||0;while(angle>180)angle-=360;while(angle<=-180)angle+=360;return angle}
function gvFlightGreatCirclePosition(ra1,dec1,ra2,dec2,progress){
    const d2r=Math.PI/180,r2d=180/Math.PI,toVec=(ra,dec)=>{const r=Number(ra)*d2r,d=Number(dec)*d2r,cd=Math.cos(d);return [cd*Math.cos(r),cd*Math.sin(r),Math.sin(d)]};
    const a=toVec(ra1,dec1),b=toVec(ra2,dec2),dot=Math.max(-1,Math.min(1,a[0]*b[0]+a[1]*b[1]+a[2]*b[2])),omega=Math.acos(dot),u=gvFlightClamp01(progress);
    let v;if(omega<1e-9)v=b;else{const so=Math.sin(omega),w0=Math.sin((1-u)*omega)/so,w1=Math.sin(u*omega)/so;v=[w0*a[0]+w1*b[0],w0*a[1]+w1*b[1],w0*a[2]+w1*b[2]]}
    let ra=Math.atan2(v[1],v[0])*r2d;if(ra<0)ra+=360;return [ra,Math.atan2(v[2],Math.hypot(v[0],v[1]))*r2d];
}
function gvFlightLogLerp(a,b,u){const x=Math.max(Number(a),1e-12),y=Math.max(Number(b),1e-12),t=gvFlightClamp01(u);return Math.exp(Math.log(x)+(Math.log(y)-Math.log(x))*t)}
function gvFlightStateAt(sec,{firstHomeTrip,startFov,finalFov,maxFov,startRotation,targetRotation}){
    const duration=firstHomeTrip?7.5:17,t=gvFlightClamp01((Math.max(0,Number(sec)||0))/duration);
    if(firstHomeTrip){
        const translateStart=.30,translationComplete=.70;
        let translation;if(t<=translateStart)translation=0;else if(t>=translationComplete)translation=1;else translation=gvFlightNavigationSmootherstep((t-translateStart)/(translationComplete-translateStart));
        let fov;if(t<=.50){const p=gvFlightNavigationSmootherstep(t/.50);fov=gvFlightLogLerp(startFov,maxFov,p)}else{const p=gvFlightNavigationSmootherstep((t-.50)/.50);fov=gvFlightLogLerp(maxFov,finalFov,p)}
        return {translation,fov,rotation:startRotation+gvFlightNormalizeRotationDelta(targetRotation-startRotation)*translation};
    }
    const translateStart=.30,translationComplete=.70;
    let translation;if(t<=translateStart)translation=0;else if(t>=translationComplete)translation=1;else translation=gvFlightNavigationSmootherstep((t-translateStart)/(translationComplete-translateStart));
    let fov;if(t<=.50){const p=gvFlightNavigationSmootherstep(t/.50);fov=gvFlightLogLerp(startFov,maxFov,p)}else{const p=gvFlightNavigationSmootherstep((t-.50)/.50);fov=gvFlightLogLerp(maxFov,finalFov,p)}
    return {translation,fov,rotation:startRotation+gvFlightNormalizeRotationDelta(targetRotation-startRotation)*translation};
}
async function gvFly130H(prepared,{firstHomeTrip=false,onZoomInStart=null,registeredPromise=null}={}){
    const initialCenter=prepared?.imageCenter;let ra1=Number(initialCenter?.[0]),dec1=Number(initialCenter?.[1]),finalFov=Number(prepared?.finalFov),targetRotation=Number(prepared?.rotation);
    if(!Number.isFinite(ra1)||!Number.isFinite(dec1)||!Number.isFinite(finalFov)||finalFov<=0||!Number.isFinite(targetRotation))throw new Error('GV 130H DESTINATION STATE INVALID');
    const startRaDec=aladin.getRaDec?.()||[HOME.ra,HOME.dec],ra0=Number(startRaDec[0]),dec0=Number(startRaDec[1]),rawFov=aladin.getFov?.(),startFov=Number(Array.isArray(rawFov)?rawFov[0]:rawFov);
    let startRotation=0;try{startRotation=Number(aladin.getRotation?.()??aladin.view?.rotation??0)||0}catch(_){}
    if(firstHomeTrip){
        const translateSeconds=3.0,rotationSeconds=1.25,zoomSeconds=6.0,durationSeconds=translateSeconds+rotationSeconds+zoomSeconds;
        const doeRun=gvDoeBeginRun({firstHomeTrip:true,durationSeconds,start:{ra:ra0,dec:dec0,fov:startFov,rotation:startRotation},target:{ra:ra1,dec:dec1,fov:finalFov,rotation:targetRotation}});
        const translateStarted=performance.now();let lastSample=-1;
        await new Promise((resolve,reject)=>{
            const frame=now=>{try{
                const elapsed=Math.min(translateSeconds*1000,now-translateStarted),u=gvFlightNavigationSmootherstep(elapsed/(translateSeconds*1000)),sample=Math.floor(elapsed*gvDoeRate/1000);
                doeRun.browserRaf.push({t:gvDoeNow()-doeRun.startedAt,rafNow:Number(now)});
                if(sample!==lastSample){
                    const pos=gvFlightGreatCirclePosition(ra0,dec0,ra1,dec1,u);
                    gvDoeCommand('gotoRaDec',[pos[0],pos[1]]);aladin.gotoRaDec(pos[0],pos[1]);coordinate?.update(pos[0],pos[1]);
                    lastSample=sample;
                }
                if(elapsed<translateSeconds*1000){requestAnimationFrame(frame);return}resolve();
            }catch(error){reject(error)}};requestAnimationFrame(frame);
        });
        if(registeredPromise){
            const registered=await registeredPromise,center=registered?.imageCenter;
            ra1=Number(center?.[0]);dec1=Number(center?.[1]);finalFov=Number(registered?.finalFov);targetRotation=Number(registered?.rotation);
            if(!Number.isFinite(ra1)||!Number.isFinite(dec1)||!Number.isFinite(finalFov)||finalFov<=0||!Number.isFinite(targetRotation))throw new Error('GV FIRST TRIP REGISTERED STATE INVALID');
            gvDoeCommand('gotoRaDec',[ra1,dec1]);aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1);
            let rotationStart=0;try{rotationStart=Number(aladin.getRotation?.()??aladin.view?.rotation??startRotation)||startRotation}catch(_){rotationStart=startRotation}
            const rotationDelta=gvFlightNormalizeRotationDelta(targetRotation-rotationStart),rotationStarted=performance.now();lastSample=-1;
            await new Promise((resolve,reject)=>{const frame=now=>{try{const elapsed=Math.min(rotationSeconds*1000,now-rotationStarted),u=gvFlightNavigationSmootherstep(elapsed/(rotationSeconds*1000)),sample=Math.floor(elapsed*gvDoeRate/1000);if(sample!==lastSample){const rotation=rotationStart+rotationDelta*u;gvDoeCommand('setRotation',[rotation]);aladin.setRotation(rotation);lastSample=sample}if(elapsed<rotationSeconds*1000){requestAnimationFrame(frame);return}resolve()}catch(error){reject(error)}};requestAnimationFrame(frame)});
            gvDoeCommand('setRotation',[targetRotation]);aladin.setRotation(targetRotation);
            try{await onZoomInStart?.(registered)}catch(error){console.error('GV 130H FIRST-TRIP ZOOM-IN CALLBACK FAILED',error)}
        }else{try{await onZoomInStart?.()}catch(error){console.error('GV 130H FIRST-TRIP ZOOM-IN CALLBACK FAILED',error)}}
        const zoomStarted=performance.now(),zoomStartRaw=aladin.getFov?.(),zoomStartFov=Number(Array.isArray(zoomStartRaw)?zoomStartRaw[0]:zoomStartRaw);lastSample=-1;
        await new Promise((resolve,reject)=>{
            const frame=now=>{try{
                const elapsed=Math.min(zoomSeconds*1000,now-zoomStarted),p=gvFlightNavigationSmootherstep(elapsed/(zoomSeconds*1000)),sample=Math.floor(elapsed*gvDoeRate/1000);
                doeRun.browserRaf.push({t:gvDoeNow()-doeRun.startedAt,rafNow:Number(now)});
                if(sample!==lastSample){const fov=gvFlightLogLerp(zoomStartFov,finalFov,p);gvDoeCommand('setFov',[fov]);aladin.setFov(fov);lastSample=sample}
                if(elapsed<zoomSeconds*1000){requestAnimationFrame(frame);return}resolve();
            }catch(error){reject(error)}};requestAnimationFrame(frame);
        });
        gvDoeCommand('gotoRaDec',[ra1,dec1]);aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1);
        gvDoeCommand('setFov',[finalFov]);aladin.setFov(finalFov);gvDoeCommand('setRotation',[targetRotation]);aladin.setRotation(targetRotation);
        doeRun.meta.targetFinal={ra:ra1,dec:dec1,fov:finalFov,rotation:targetRotation};gvDoeFinishRun(doeRun);return prepared;
    }
    if(registeredPromise)registeredPromise.then(registered=>{const center=registered?.imageCenter,nra=Number(center?.[0]),ndec=Number(center?.[1]),nfov=Number(registered?.finalFov),nrotation=Number(registered?.rotation);if(Number.isFinite(nra)&&Number.isFinite(ndec)&&Number.isFinite(nfov)&&nfov>0&&Number.isFinite(nrotation)){ra1=nra;dec1=ndec;finalFov=nfov;targetRotation=nrotation}}).catch(error=>console.error('GV 130H REGISTERED DESTINATION PREPARE FAILED',error));
    const durationSeconds=17,duration=durationSeconds*1000,started=performance.now(),zoomInThreshold=.50;let lastSample=-1,destinationCenterApplied=false,zoomInStarted=false;
    const doeRun=gvDoeBeginRun({firstHomeTrip:false,durationSeconds,start:{ra:ra0,dec:dec0,fov:startFov,rotation:startRotation},target:{ra:ra1,dec:dec1,fov:finalFov,rotation:targetRotation}});
    await new Promise((resolve,reject)=>{
        const frame=now=>{try{
            const elapsedMs=now-started,t=Math.min(1,elapsedMs/duration),sample=Math.floor(elapsedMs*gvDoeRate/1000);
            doeRun.browserRaf.push({t:gvDoeNow()-doeRun.startedAt,rafNow:Number(now)});
            if(!zoomInStarted&&t>=zoomInThreshold){zoomInStarted=true;try{onZoomInStart?.()}catch(error){console.error('GV 130H ZOOM-IN CALLBACK FAILED',error)}}
            if(t<1&&sample!==lastSample){
                const state=gvFlightStateAt(t*durationSeconds,{firstHomeTrip:false,startFov,finalFov,maxFov:60,startRotation,targetRotation});
                gvDoeCommand('setFov',[state.fov]);aladin.setFov(state.fov);
                if(state.translation>0&&state.translation<1){const pos=gvFlightGreatCirclePosition(ra0,dec0,ra1,dec1,state.translation);gvDoeCommand('gotoRaDec',[pos[0],pos[1]]);aladin.gotoRaDec(pos[0],pos[1]);coordinate?.update(pos[0],pos[1])}
                else if(state.translation>=1&&!destinationCenterApplied){gvDoeCommand('gotoRaDec',[ra1,dec1]);aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1);destinationCenterApplied=true}
                gvDoeCommand('setRotation',[state.rotation]);aladin.setRotation(state.rotation);lastSample=sample;
            }
            if(t<1){requestAnimationFrame(frame);return}
            if(!destinationCenterApplied){gvDoeCommand('gotoRaDec',[ra1,dec1]);aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1)}
            gvDoeCommand('setFov',[finalFov]);aladin.setFov(finalFov);gvDoeCommand('setRotation',[targetRotation]);aladin.setRotation(targetRotation);resolve(prepared);
        }catch(error){reject(error)}};requestAnimationFrame(frame);
    });
    doeRun.meta.targetFinal={ra:ra1,dec:dec1,fov:finalFov,rotation:targetRotation};gvDoeFinishRun(doeRun);return prepared;
}


// ============================================================================
// SECTION 034 — AUTHORITATIVE ACTIVE ROUTE ACCESS
// ECO: GV200-001
// ============================================================================
const activeRoute=navigationRuntime.active?.route;
if(!Array.isArray(activeRoute))throw new Error('NAVIGATION ACTIVE ROUTE MISSING');
if(activeRoute.length!==100)throw new Error(`NAVIGATION ACTIVE ROUTE LENGTH INVALID: ${activeRoute.length}`);


// ============================================================================
// SECTION 035 — DESTINATION VALIDATION
// ECO: GV200-001
// ============================================================================
function validateDestination(destination){
    if(!destination)throw new Error('DESTINATION MISSING');
    const ra=Number(destination.ra);
    const dec=Number(destination.dec);
    const fov=Number(destination.fovDegrees);
    const rotation=destination.aladinRotation;
    if(!Number.isFinite(ra))throw new Error('DESTINATION RA INVALID');
    if(!Number.isFinite(dec))throw new Error('DESTINATION DEC INVALID');
    if(!Number.isFinite(fov)||fov<=0)throw new Error('DESTINATION FOV INVALID');
    if(!Number.isFinite(rotation))throw new Error('DESTINATION ROTATION INVALID');
    return Object.freeze({destination,ra,dec,fov,rotation});
}


function gvPrewarmProviderWebsite(destination){
    // BUILD 0003 performance rollback: provider websites must remain dormant
    // while Galaxy Viewer is visible. Loading begins only after Website press.
    return;
}

// ============================================================================
// SECTION 036 — DESTINATION → ALADIN HANDOFF
// ECO: GV200-001
// ============================================================================
async function showDestination(destination,{firstTrip=false}={}){
    gvHideEarthDistance();
    const v=validateDestination(destination),preparedPromise=gvPrepareDirectHd(v.destination),sourceDestination=activeDestination;
    activeDestination=v.destination;destinationPresentation.depart();
    travelPresentation.begin(v.destination,{source:sourceDestination,firstHomeTrip:firstTrip,durationSeconds:firstTrip?9:17});
    let installed=false,displayReady=Promise.resolve(false);
    const installWhenReady=prepared=>{if(activeDestination===v.destination&&!installed){displayReady=gvInstallPreparedHd(prepared);installed=true}return displayReady};
    if(firstTrip){
        const provisional={imageCenter:[v.ra,v.dec],finalFov:v.fov,rotation:v.rotation};
        const travelPromise=gvFly130H(provisional,{firstHomeTrip:true,registeredPromise:preparedPromise,onZoomInStart:installWhenReady});
        const prepared=await preparedPromise;headsUpDisplay.markReady?.(v.destination);await travelPromise;
        if(activeDestination!==v.destination)return v.destination;
        if(!installed)await installWhenReady(prepared);else await displayReady;
        travelPresentation.end();destinationPresentation.arrive(v.destination,{imageUrl:String(prepared.record?.imageUrl||directHdUrl(v.destination)).trim()});headsUpDisplay.render();gvShowEarthDistance(v.destination);gvPrewarmProviderWebsite(v.destination);return v.destination;
    }
    let prepared=null;
    preparedPromise.then(value=>{prepared=value;headsUpDisplay.markReady?.(v.destination)}).catch(error=>console.error('GV DIRECT HD PREPARE FAILED',error));
    const provisional={imageCenter:[v.ra,v.dec],finalFov:v.fov,rotation:v.rotation};
    const travelPromise=gvFly130H(provisional,{firstHomeTrip:false,registeredPromise:preparedPromise,onZoomInStart:()=>{preparedPromise.then(installWhenReady).catch(error=>console.error('GV DIRECT HD ZOOM-IN INSTALL FAILED',error))}});
    await travelPromise;if(activeDestination!==v.destination)return v.destination;
    prepared=prepared||await preparedPromise;
    if(!installed)await installWhenReady(prepared);else await displayReady;
    travelPresentation.end();destinationPresentation.arrive(v.destination,{imageUrl:String(prepared.record?.imageUrl||directHdUrl(v.destination)).trim()});headsUpDisplay.render();gvShowEarthDistance(v.destination);gvPrewarmProviderWebsite(v.destination);return v.destination;
}

// ============================================================================
// SECTION 037 — RANDOM GALAXY ACTION
// ECO: GV200-001
// ============================================================================
async function navigateRandom(){
    if(navigationInFlight)return;
    document.getElementById('gv-universe-context')?.remove();
    document.getElementById('gv-we-are-here')?.remove();
    navigationInFlight=true;
    galaxyNavigator.setBusy(true);
    galaxyNavigator.setTraveling?.(true);
    updateNavigationAvailability();
    try{
        const destination=await navigationRuntime.nextDestination();
        if(historyIndex<history.length-1)history.splice(historyIndex+1);
        history.push(destination);
        historyIndex=history.length-1;
        const firstTrip=routeIndex===0;
        routeIndex++;
        await showDestination(destination,{firstTrip});
    }finally{
        navigationInFlight=false;
        galaxyNavigator.setTraveling?.(false);
        galaxyNavigator.setBusy(false);
        updateNavigationAvailability();
    }
}


// ============================================================================
// SECTION 038 — BACK ACTION
// ECO: GV200-001
// ============================================================================
async function navigateBack(){
    if(navigationInFlight||historyIndex<=0)return;
    navigationInFlight=true;galaxyNavigator.setBusy(true);galaxyNavigator.setTraveling?.(true);historyIndex--;updateNavigationAvailability();
    try{await showDestination(history[historyIndex])}finally{navigationInFlight=false;galaxyNavigator.setTraveling?.(false);galaxyNavigator.setBusy(false);updateNavigationAvailability()}
}


// ============================================================================
// SECTION 039 — FORWARD ACTION
// ECO: GV200-001
// ============================================================================
async function navigateForward(){
    if(navigationInFlight||historyIndex>=history.length-1)return;
    navigationInFlight=true;galaxyNavigator.setBusy(true);galaxyNavigator.setTraveling?.(true);historyIndex++;updateNavigationAvailability();
    try{await showDestination(history[historyIndex])}finally{navigationInFlight=false;galaxyNavigator.setTraveling?.(false);galaxyNavigator.setBusy(false);updateNavigationAvailability()}
}

function updateNavigationAvailability(){
    galaxyNavigator.setEnabled({
        back:historyIndex>0,
        random:true,
        forward:historyIndex>=0&&historyIndex<history.length-1
    });
}
updateNavigationAvailability();


// ============================================================================
// SECTION 040 — TRIAL READY GATE / PUBLIC TEST STATE
// ECO: GV200-001
// ============================================================================
window.GalaxyViewerCore=Object.freeze({
    version:VERSION,
    displayVersion:VERSION,
    aladin,
    home:HOME,
    hamburger,
    coordinate,
    target,
    diagnostics,
    headsUpDisplay,
    travelPresentation,
    navigationRuntime,
    get routeIndex(){return routeIndex},
    get historyIndex(){return historyIndex},
    get historyLength(){return history.length},
    get navigationState(){return navigationRuntime.snapshot()}
});

window.GalaxyViewerPrepareCosmicReveal=gvCosmicReveal.prepare;
window.GalaxyViewerStartCosmicReveal=gvCosmicReveal.start;
console.info(`${VERSION} — TRIAL READY`,{
    routeLength:activeRoute.length,
    navigation:navigationRuntime.snapshot()
});
})().catch(error=>{
    console.error('GV200-001 BOOT FAILURE',error);
});
"""))