from IPython.display import HTML, Javascript, display
import json

# ============================================================================
# SECTION 001 — FILE IDENTITY / PYTHON IMPORTS
# ECO: GV200-001
# ============================================================================
VIEWER_VERSION = "RC-V1.0.0.3"
BUILD_NUMBER = "0055"
# ROLLUP 1.0.0.3 / BUILD 0003 — Galaxy Search result simplification

# ============================================================================
# SECTION 002 — ALADIN MIRROR POINTERS
# ECO: GV200-001
# ============================================================================
ALADIN_VERSION = "3.8.2"
ALADIN_CSS_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/aladin-source-clone/src/css/aladin.css"
ALADIN_JS_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/vendor/aladin-lite/3.8.2/aladin.js"

# ============================================================================
# SECTION 003 — GALAXY VIEWER MODULE POINTERS
# ECO: GV200-001
# ============================================================================
HAMBURGER_BASE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/hamburger-menu/gv-hamburger-menu-0011.js"
HAMBURGER_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/hamburger-menu/gv-hamburger-menu-0011.js"
COORDINATE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js"
TARGET_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@e197403c8525b90f21c95967f11ab0bd01c3d0c4/viewer/modules/target-simbad/gv-target-simbad-0007.js"
DIAGNOSTICS_URL = ""
GALAXY_ROUTE_ENGINE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js?v=0001"
GALAXY_NAVIGATOR_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/galaxy-navigator/gv-galaxy-navigator-013.js"
HEADS_UP_DISPLAY_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/hud/gv-heads-up-display-0002.js"

# ============================================================================
# SECTION 004 — HTML APPLICATION ROOT
# ECO: GV200-001
# ============================================================================
display(HTML("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/aladin-source-clone/src/css/aladin.css" />
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
#gv-hamburger-host{position:absolute;left:50%;top:0;width:390px;height:100%;transform:translateX(-50%);z-index:9000;pointer-events:none}
#gv-coordinate-host{position:absolute;left:50%;top:12px;z-index:7210;width:290px;height:36px;transform:translateX(-145px);pointer-events:auto}
#gv-target-host{position:absolute;left:50%;top:12px;z-index:9101;width:36px;height:36px;transform:translateX(147px);pointer-events:auto}
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
const VERSION='RC-V1.0.0.3';
const GV200001_BUILD='0055';
const GV_RUNTIME='0082';
const fresh=url=>`${url}${url.includes('?')?'&':'?'}v=GV200001-${GV200001_BUILD}-CROSSFADE0055`;
const requestPortraitLock=()=>{try{const lock=screen?.orientation?.lock;if(typeof lock==='function')Promise.resolve(lock.call(screen.orientation,'portrait-primary')).catch(()=>{})}catch(_){}};
requestPortraitLock();
document.addEventListener('pointerdown',requestPortraitLock,{once:true,passive:true});
window.GV_BOOT_CONFIG=Object.freeze({
    viewerVersion:'RC-V1.0.0.3',
    aladinVersion:'3.8.2',
    aladinCssUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/aladin-source-clone/src/css/aladin.css',
    aladinJsUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/vendor/aladin-lite/3.8.2/aladin.js',
    hamburgerBaseUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/hamburger-menu/gv-hamburger-menu-0011.js',
    hamburgerUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/hamburger-menu/gv-hamburger-menu-0011.js',
    coordinateUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js',
    targetUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@e197403c8525b90f21c95967f11ab0bd01c3d0c4/viewer/modules/target-simbad/gv-target-simbad-0007.js',
    galaxyRouteEngineUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js',
    galaxyNavigatorUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/galaxy-navigator/gv-galaxy-navigator-013.js',
    headsUpDisplayUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/hud/gv-heads-up-display-0002.js',
    providerArtworkUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@5781bcedd8faaaa81b7eb3df1cda6ce586765181/viewer/modules/provider-artwork/gv-provider-artwork-0004.js',
    travelPresentationUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/random-galaxy/gv-random-travel-presentation-003.js',
    destinationPresentationUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@becf6505e865477c9550302e30b3ffb01392d571/viewer/modules/destination-presentation/gv-destination-presentation-0034.js'
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
const gvModuleLoadPromise=Promise.all([
    loadScript(config.hamburgerBaseUrl).catch(error=>{console.error('HAMBURGER MODULE LOAD FAILED',error)}),
    loadScript(config.providerArtworkUrl).catch(error=>{console.error('PROVIDER ARTWORK LOAD FAILED',error)}),
    loadScript(config.coordinateUrl).catch(error=>console.error('COORDINATE OVERLAY LOAD FAILED',error)),
    loadScript(fresh(config.targetUrl)).catch(error=>{console.error('TARGET MODULE LOAD FAILED',error)}),
    loadScript(config.galaxyRouteEngineUrl).catch(error=>{console.error('ROUTE ENGINE LOAD FAILED',error)}),
    loadScript(config.galaxyNavigatorUrl).catch(error=>{console.error('GALAXY NAVIGATOR LOAD FAILED',error)}),
    loadScript(config.headsUpDisplayUrl).catch(error=>{console.error('HEADS-UP DISPLAY LOAD FAILED',error)}),
    loadScript(config.travelPresentationUrl).catch(error=>{console.error('TRAVEL PRESENTATION LOAD FAILED',error)}),
    loadScript(fresh(config.destinationPresentationUrl)).catch(error=>{console.error('DESTINATION PRESENTATION LOAD FAILED',error)}),
    Promise.resolve()
]);
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
    'galaxyRouteEngineUrl','galaxyNavigatorUrl','headsUpDisplayUrl','providerArtworkUrl','travelPresentationUrl','destinationPresentationUrl'
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
    survey:'https://alaskybis.unistra.fr/DSS/DSSColor',
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

// Galaxy Viewer owns the sky interaction surface. Aladin Lite 3.8.2 starts an
// independent 800 ms one-finger long-touch timer whose callback calls
// contextMenu._show() directly, even when showContextMenu is false.
// Disable that presentation path without intercepting touchstart/touchmove,
// so normal pan, pinch-zoom and rotation remain under Aladin control.
if(aladin.contextMenu){
    try{aladin.contextMenu._hide?.()}catch(_){}
    aladin.contextMenu._show=()=>{};
}
const gvSkyRoot=document.getElementById('aladin-cosmic-command-test');
gvSkyRoot?.addEventListener('contextmenu',event=>{
    event.preventDefault();
    event.stopImmediatePropagation();
},{capture:true});


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

const GV_SPACE_AGE_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf';
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
const RETICLE_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/artwork/compass/compass.png';

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

window.GV_NAV_BACKGROUND_SUSPENDED=false;
window.GV_NAV_HIPS_FETCH_SUSPENDED=false;
// BUILD 0031: gate only HiPS tile traffic independently of app polling.
// Restrict the gate to standard HiPS tile paths; survey metadata and app APIs remain available.
(function gvInstallTravelHiPSFetchGate(){
    if(window.__GV_TRAVEL_HIPS_FETCH_GATE__)return;
    const nativeFetch=window.fetch.bind(window);
    const tilePath=/\/Norder\d+\/Dir\d+\/Npix\d+(?:\.[a-z0-9]+)?(?:[?#]|$)/i;
    window.__GV_TRAVEL_HIPS_FETCH_GATE__={nativeFetch,blocked:0,lastBlocked:null};
    window.fetch=function(input,init){
        let url='';
        try{url=typeof input==='string'?input:(input?.url||'')}catch(_){}
        if(window.GV_NAV_HIPS_FETCH_SUSPENDED&&tilePath.test(url)){
            const state=window.__GV_TRAVEL_HIPS_FETCH_GATE__;
            state.blocked++;state.lastBlocked={url,at:performance.now()};
            return Promise.reject(new DOMException('HiPS tile fetch suspended during Galaxy Viewer travel','AbortError'));
        }
        return nativeFetch(input,init);
    };
})();
const updateDirectionalReticle=()=>{
    if(window.GV_NAV_BACKGROUND_SUSPENDED)return;
    const state=reticle.gvDirectional;
    if(!state)return;
    const northBearing=readCelestialNorthBearing(aladin,compassRoot);
    if(Number.isFinite(northBearing))setNorthMarker(northBearing);
    else if(Number.isFinite(state.lastNorthBearing))setNorthMarker(state.lastNorthBearing);
};

const directionalReticleTimer=setInterval(updateDirectionalReticle,40);
updateDirectionalReticle();

// ============================================================================
// SECTION 041B — EARTH BEARING POINTER / ARRIVAL DISTANCE
// ECO: GV200-028 BUILD 0001
// ============================================================================
const GV_EARTH_POINTER_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/artwork/compass/gv-earth-pointer-yellow-final-1080-crisp.png';
function gvInstallEarthBearingPointer(){
    if(document.getElementById('gv-earth-bearing-rotor'))return;
    const rotor=document.createElement('div');
    rotor.id='gv-earth-bearing-rotor';
    rotor.setAttribute('aria-hidden','true');
    Object.assign(rotor.style,{position:'absolute',inset:'0',width:'270px',height:'270px',pointerEvents:'none',transformOrigin:'50% 50%',willChange:'transform',zIndex:'10',overflow:'visible'});
    const pointer=document.createElement('img');
    pointer.id='gv-earth-bearing-pointer-image';
    pointer.src=fresh(GV_EARTH_POINTER_URL);
    pointer.alt='';
    pointer.width=270;
    pointer.height=270;
    Object.assign(pointer.style,{position:'absolute',inset:'0',width:'270px',height:'270px',objectFit:'contain',opacity:'1',filter:'none',imageRendering:'auto',pointerEvents:'none',userSelect:'none',WebkitUserDrag:'none',zIndex:'20'});
    rotor.appendChild(pointer);
    reticle.appendChild(rotor);
}
let gvEarthPointerActive=false;
let gvEarthPointerRa=HOME.ra,gvEarthPointerDec=HOME.dec;
let gvEarthLastValidBearing=null;
function gvSetEarthPointerPosition(ra,dec,activate=false){
    const r=Number(ra),d=Number(dec);
    if(Number.isFinite(r)&&Number.isFinite(d)){gvEarthPointerRa=r;gvEarthPointerDec=d}
    if(activate)gvEarthPointerActive=true;
}
function gvEarthScreenBearing(){
    try{
        if(!gvEarthPointerActive)return null;
        const ra=gvEarthPointerRa,dec=gvEarthPointerDec;
        if(!Number.isFinite(ra)||!Number.isFinite(dec))return gvEarthLastValidBearing;
        const rad=Math.PI/180,p1=dec*rad,p2=Number(HOME.dec)*rad,dl=(Number(HOME.ra)-ra)*rad;
        const celestialBearing=Math.atan2(Math.sin(dl)*Math.cos(p2),Math.cos(p1)*Math.sin(p2)-Math.sin(p1)*Math.cos(p2)*Math.cos(dl))*180/Math.PI;
        const screenBearing=((celestialBearing+readCelestialNorthBearing(aladin,compassRoot))%360+360)%360;
        if(Number.isFinite(screenBearing))gvEarthLastValidBearing=screenBearing;
        return gvEarthLastValidBearing;
    }catch(_){return gvEarthLastValidBearing}
}
function gvUpdateEarthBearingPointer(){
    if(window.GV_NAV_BACKGROUND_SUSPENDED)return;
    const rotor=document.getElementById('gv-earth-bearing-rotor');if(!rotor)return;
    try{
        const p=aladin.getRaDec?.(),ra=Number(Array.isArray(p)?p[0]:p?.ra),dec=Number(Array.isArray(p)?p[1]:p?.dec);
        if(Number.isFinite(ra)&&Number.isFinite(dec)){gvEarthPointerRa=ra;gvEarthPointerDec=dec}
        const liveRotation=Number(aladin.getRotation?.()??aladin.view?.rotation);
        if(Number.isFinite(liveRotation))gvAuthoritativeRotation=liveRotation;
    }catch(_){}
    const a=gvEarthScreenBearing();
    if(!gvEarthPointerActive){rotor.style.display='none';rotor.style.opacity='0';return}
    rotor.style.display='block';
    rotor.style.opacity='1';
    if(Number.isFinite(a))rotor.style.transform=`rotate(${a}deg)`;
}
gvInstallEarthBearingPointer();
const gvEarthBearingTimer=setInterval(gvUpdateEarthBearingPointer,40);
function gvResyncEarthPointerFromAladin(){
    try{
        if(!document.getElementById('gv-earth-bearing-rotor'))gvInstallEarthBearingPointer();
        const p=aladin.getRaDec?.(),ra=Number(Array.isArray(p)?p[0]:p?.ra),dec=Number(Array.isArray(p)?p[1]:p?.dec);
        if(Number.isFinite(ra)&&Number.isFinite(dec))gvSetEarthPointerPosition(ra,dec,true);
        const rotation=Number(aladin.getRotation?.()??aladin.view?.rotation);
        if(Number.isFinite(rotation)){gvAuthoritativeRotation=rotation;setNorthMarker(-rotation)}
        gvUpdateEarthBearingPointer();
    }catch(error){console.error('GV EARTH POINTER RESYNC FAILED',error)}
}
function gvRecoverViewerAfterNativeReturn(){
    const redraw=()=>{
        try{
            window.dispatchEvent(new Event('resize'));
            if(typeof aladin.resize==='function')aladin.resize();
            else if(typeof aladin.requestRedraw==='function')aladin.requestRedraw();
            else if(typeof aladin.redraw==='function')aladin.redraw();
        }catch(error){console.error('GV ALADIN RESUME REDRAW FAILED',error)}
    };
    requestAnimationFrame(()=>{
        try{
            redraw();
            gvResyncEarthPointerFromAladin();
            setTimeout(redraw,400);
        }catch(error){console.error('GV VIEWER RETURN RECOVERY FAILED',error)}
    });
}
// BUILD 0051 — Aladin WebGL context-loss guard.
// Android WebView can reclaim the GPU context during long sessions. Aladin Lite 3.8.2
// does not install its own webglcontextlost recovery, so a lost context can otherwise
// leave the HiPS canvas permanently black while the rest of the UI remains alive.
const GV_WEBGL_RECOVERY_WINDOW_MS=60000;
const GV_WEBGL_RECOVERY_DELAY_MS=900;
const gvWebglBoundCanvases=new WeakSet();
let gvWebglReloadTimer=0;
let gvWebglObserver=null;
window.GV_WEBGL_HEALTH=window.GV_WEBGL_HEALTH||{losses:0,restores:0,lastLoss:null,lastRestore:null,reloads:0,suppressedReloads:0};
function gvScheduleWebglHardRecovery(canvas){
    const now=Date.now();
    let previous=0;
    try{previous=Number(sessionStorage.getItem('gv-webgl-last-hard-recovery')||0)}catch(_){}
    if(previous>0&&now-previous<GV_WEBGL_RECOVERY_WINDOW_MS){
        window.GV_WEBGL_HEALTH.suppressedReloads++;
        console.error('GV WEBGL CONTEXT LOST AGAIN INSIDE RECOVERY WINDOW — RELOAD SUPPRESSED');
        return;
    }
    try{sessionStorage.setItem('gv-webgl-last-hard-recovery',String(now))}catch(_){}
    clearTimeout(gvWebglReloadTimer);
    gvWebglReloadTimer=setTimeout(()=>{
        window.GV_WEBGL_HEALTH.reloads++;
        console.warn('GV WEBGL HARD RECOVERY — RELOADING VIEWER');
        location.reload();
    },GV_WEBGL_RECOVERY_DELAY_MS);
}
function gvBindAladinWebglGuards(){
    const host=document.getElementById('aladin-cosmic-command-test');
    if(!host)return;
    for(const canvas of host.querySelectorAll('canvas')){
        if(gvWebglBoundCanvases.has(canvas))continue;
        gvWebglBoundCanvases.add(canvas);
        canvas.addEventListener('webglcontextlost',event=>{
            try{event.preventDefault()}catch(_){}
            window.GV_WEBGL_HEALTH.losses++;
            window.GV_WEBGL_HEALTH.lastLoss=new Date().toISOString();
            console.error('GV ALADIN WEBGL CONTEXT LOST',{losses:window.GV_WEBGL_HEALTH.losses,width:canvas.width,height:canvas.height});
            gvScheduleWebglHardRecovery(canvas);
        },false);
        canvas.addEventListener('webglcontextrestored',()=>{
            window.GV_WEBGL_HEALTH.restores++;
            window.GV_WEBGL_HEALTH.lastRestore=new Date().toISOString();
            console.warn('GV ALADIN WEBGL CONTEXT RESTORED',{restores:window.GV_WEBGL_HEALTH.restores});
            try{gvRecoverViewerAfterNativeReturn()}catch(_){}
        },false);
    }
}
(function gvInstallAladinWebglGuards(){
    const host=document.getElementById('aladin-cosmic-command-test');
    if(!host)return;
    gvBindAladinWebglGuards();
    gvWebglObserver=new MutationObserver(gvBindAladinWebglGuards);
    gvWebglObserver.observe(host,{childList:true,subtree:true});
})();

window.addEventListener('gv-native-viewer-resumed',gvRecoverViewerAfterNativeReturn);
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')gvRecoverViewerAfterNativeReturn()});
window.addEventListener('focus',gvRecoverViewerAfterNativeReturn);
window.addEventListener('pageshow',gvRecoverViewerAfterNativeReturn);

function gvFormatEarthDistance(destination){
    // Runtime catalog distance is Earth-relative MLY, matching destinationPresentation.distance().
    const v=Number(destination?.distanceMly??destination?.distance);
    if(!(v>0))return '';
    if(v>=1000)return `${(v/1000).toLocaleString('en-US',{maximumFractionDigits:2})} BLY`;
    if(v>=1)return `${v.toLocaleString('en-US',{maximumFractionDigits:v<10?1:0})} MLY`;
    return `${(v*1000).toLocaleString('en-US',{maximumFractionDigits:v<0.01?2:1})} KLY`;
}
function gvInstallEarthDistanceBanner(){
    if(document.getElementById('gv-earth-distance-banner'))return;
    const style=document.createElement('style');style.textContent=`
#gv-earth-distance-banner{position:fixed;left:50%;z-index:7362;transform:translateX(-50%);box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;gap:4px;width:max-content;max-width:calc(100vw - 24px);min-width:0;min-height:0;padding:3px 5px;border:1px solid #58BFFF;border-radius:5px;background:linear-gradient(145deg,rgba(4,20,48,.94),rgba(12,52,116,.94));box-shadow:0 0 5px rgba(88,191,255,.48);font:400 11px/1 "GV Space Age",sans-serif;letter-spacing:1px;white-space:nowrap;color:#FFD84A;text-align:center;text-shadow:0 0 3px rgba(255,216,74,.78);pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-earth-distance-banner .gv-earth-distance-icon{display:inline-block;font:11px/1 system-ui,sans-serif;letter-spacing:0;filter:drop-shadow(0 0 2px rgba(88,191,255,.55))}
#gv-earth-distance-banner.gv-visible{opacity:1;visibility:visible}
#gv-earth-distance-banner .gv-earth-distance-tick{display:inline-block;margin-left:7px;width:0;height:0;border-top:5px solid transparent;border-bottom:5px solid transparent;border-left:9px solid #FFD84A;filter:drop-shadow(0 0 4px rgba(255,216,74,.9));vertical-align:-1px}
#gv-live-physical-scale{position:fixed;left:50%;z-index:7362;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear;font:400 11px/1 "GV Space Age",sans-serif;letter-spacing:1px;color:#FFD84A;text-align:center;text-shadow:0 0 3px rgba(255,216,74,.78);white-space:nowrap}
#gv-live-physical-scale.gv-visible{opacity:1;visibility:visible}
#gv-live-physical-scale .gv-live-scale-label{margin-bottom:4px}
#gv-live-physical-scale .gv-live-scale-line{position:relative;height:1px;background:#FFD84A;box-shadow:0 0 4px rgba(255,216,74,.9);min-width:4px}
#gv-live-physical-scale .gv-live-scale-line::before,#gv-live-physical-scale .gv-live-scale-line::after{content:"";position:absolute;top:50%;width:1px;height:9px;background:#FFD84A;box-shadow:0 0 4px rgba(255,216,74,.9);transform:translateY(-50%)}
#gv-live-physical-scale .gv-live-scale-line::before{left:0}
#gv-live-physical-scale .gv-live-scale-line::after{right:0}`;document.head.appendChild(style);
    const b=document.createElement('div');b.id='gv-earth-distance-banner';document.body.appendChild(b);
    const s=document.createElement('div');s.id='gv-live-physical-scale';s.innerHTML='<span class="gv-live-scale-label"></span><span class="gv-live-scale-line"></span>';document.body.appendChild(s);
}
let gvLiveScaleValueLy=null;
const gvLiveScaleNominalPx=25*96/25.4;
function gvFormatLiveScale(ly){
    if(!(ly>0))return '';
    if(ly>=1e9)return `${(ly/1e9).toLocaleString('en-US',{maximumFractionDigits:2})} BLY`;
    if(ly>=1e6)return `${(ly/1e6).toLocaleString('en-US',{maximumFractionDigits:2})} MLY`;
    if(ly>=1e3)return `${(ly/1e3).toLocaleString('en-US',{maximumFractionDigits:2})} KLY`;
    return `${ly.toLocaleString('en-US',{maximumFractionDigits:2})} LY`;
}
function gvChooseLiveScaleValue(lyPerPx){
    const targetLy=lyPerPx*gvLiveScaleNominalPx;if(!(targetLy>0))return null;
    const exponent=Math.floor(Math.log10(targetLy)),candidates=[];
    for(let e=exponent-2;e<=exponent+2;e++)for(const m of [1,2,5])candidates.push(m*Math.pow(10,e));
    candidates.sort((a,b)=>Math.abs(a/lyPerPx-gvLiveScaleNominalPx)-Math.abs(b/lyPerPx-gvLiveScaleNominalPx));
    return candidates[0]||null;
}
function gvUpdateLivePhysicalScale(){
    if(window.GV_NAV_BACKGROUND_SUSPENDED)return;
    const s=document.getElementById('gv-live-physical-scale'),line=s?.querySelector('.gv-live-scale-line'),label=s?.querySelector('.gv-live-scale-label'),b=document.getElementById('gv-earth-distance-banner');
    if(!s||!line||!label||!b||!b.classList.contains('gv-visible')||!activeDestination){s?.classList.remove('gv-visible');return}
    const distanceMly=Number(activeDestination?.distanceMly??activeDestination?.distance),rawFov=aladin.getFov?.(),fovX=Number(Array.isArray(rawFov)?rawFov[0]:rawFov),viewportWidth=Number(document.getElementById('aladin-cosmic-command-test')?.clientWidth||innerWidth);
    if(!(distanceMly>0)||!(fovX>0)||!(viewportWidth>0)){s.classList.remove('gv-visible');return}
    const physicalWidthLy=2*distanceMly*1e6*Math.tan(fovX*Math.PI/360),lyPerPx=physicalWidthLy/viewportWidth;
    if(!(lyPerPx>0)||!Number.isFinite(lyPerPx)){s.classList.remove('gv-visible');return}
    let widthPx=gvLiveScaleValueLy>0?gvLiveScaleValueLy/lyPerPx:0;
    if(!(gvLiveScaleValueLy>0)||widthPx<gvLiveScaleNominalPx*.5||widthPx>gvLiveScaleNominalPx*2){
        gvLiveScaleValueLy=gvChooseLiveScaleValue(lyPerPx);widthPx=gvLiveScaleValueLy/lyPerPx;
    }
    line.style.width=`${Math.max(4,widthPx)}px`;label.textContent=gvFormatLiveScale(gvLiveScaleValueLy);
    const br=b.getBoundingClientRect();s.style.bottom=`${Math.max(0,innerHeight-br.top+8)}px`;s.classList.add('gv-visible');
}
function gvHideEarthDistance(){document.getElementById('gv-earth-distance-banner')?.classList.remove('gv-visible');document.getElementById('gv-live-physical-scale')?.classList.remove('gv-visible');gvLiveScaleValueLy=null}
function gvShowEarthDistance(destination){
    gvInstallEarthDistanceBanner();const b=document.getElementById('gv-earth-distance-banner'),text=gvFormatEarthDistance(destination);if(!b||!text)return;
    b.innerHTML=`<span class="gv-earth-distance-icon" aria-hidden="true">🌎</span><span>${text}</span><span class="gv-earth-distance-tick" aria-hidden="true"></span>`;
    const card=document.querySelector('.gvdp-card');const place=()=>{const r=card?.getBoundingClientRect();b.style.bottom=`${r&&r.height?Math.max(0,innerHeight-r.top+6):130}px`;gvUpdateLivePhysicalScale()};place();requestAnimationFrame(place);
    b.classList.add('gv-visible');gvLiveScaleValueLy=null;gvUpdateLivePhysicalScale();
}
gvInstallEarthDistanceBanner();
setInterval(gvUpdateLivePhysicalScale,80);

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
// BLD 0110: all immutable module URLs are commit-pinned, so do not append
// cache-busting query strings. Start the complete module set in parallel so a
// cold CDN fetch for one module cannot serialize the entire boot sequence.
await gvModuleLoadPromise;
if(window.GVProviderArtwork?.VERSION!=='0004')throw new Error('PROVIDER ARTWORK 0004 EXPORT MISSING');


// ============================================================================
// SECTION 019 — REQUIRED MODULE EXPORT VALIDATION
// ECO: GV200-001
// ============================================================================
if(window.GalaxyViewerHamburgerMenu?.version!=='0009')throw new Error('HAMBURGER 0009 EXPORT MISSING');
if(window.GalaxyCoordinateOverlay&&window.GalaxyCoordinateOverlay.VERSION!=='0006')console.error('COORDINATE 0006 EXPORT INVALID');
if(window.GalaxyViewerTargetSimbad?.version!=='0007')throw new Error('TARGET SURVEY 0007 EXPORT MISSING');
/* GV014: diagnostics intentionally not loaded. */
if(window.GalaxyRouteEngine?.VERSION!=='0002')throw new Error('GALAXY ROUTE ENGINE 002 EXPORT MISSING');
if(window.GalaxyNavigator?.VERSION!=='013'||typeof window.GalaxyNavigator.mount!=='function')throw new Error('GALAXY NAVIGATOR 013 EXPORT MISSING');
if(window.GalaxyViewerHeadsUpDisplay?.VERSION!=='0002'||typeof window.GalaxyViewerHeadsUpDisplay.mount!=='function')throw new Error('HEADS-UP DISPLAY 0002 EXPORT MISSING');
if(typeof window.GalaxyRandomTravelPresentation?.mount!=='function')throw new Error('RANDOM TRAVEL PRESENTATION EXPORT MISSING');
if(window.GalaxyDestinationPresentation?.VERSION!=='0034'||typeof window.GalaxyDestinationPresentation.mount!=='function')throw new Error('DESTINATION PRESENTATION 0034 EXPORT MISSING');
// Navigator is presentation: mount immediately. Route preparation must never block its appearance.
const earlyNavigationHost=document.getElementById('gv-navigation-host');
if(!earlyNavigationHost)throw new Error('REQUIRED HOST MISSING: navigation');
const galaxyNavigator=window.GalaxyNavigator.mount(earlyNavigationHost,{
    onBack:()=>navigateBack(),
    onRandom:()=>{gvSetTripCycle(true);return navigateRandom()},
    onForward:()=>navigateForward(),
    onSelectSurveyIndex:(index)=>gvNavigateSurveyIndex(Number(index)).catch(error=>console.error('GV SURVEY DIRECT SELECT FAILED',error))
});
// References acquired at immediate Navigator mount.
galaxyNavigator.setEnabled({back:false,random:false,forward:false});
galaxyNavigator.setBusy(true);
galaxyNavigator.setStart?.(true);

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
const GV_ABOUT_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/about/gv-about-presentation-0013.js';
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
    if(window.GV_NAV_BACKGROUND_SUSPENDED)return;
    try{
        const size=aladin.getSize?.(),center=Array.isArray(size)&&size.length>=2?aladin.pix2world?.(Number(size[0])/2,Number(size[1])/2):aladin.getRaDec?.();
        if(coordinate&&Array.isArray(center)&&Number.isFinite(Number(center[0]))&&Number.isFinite(Number(center[1])))coordinate.update(Number(center[0]),Number(center[1]));
    }catch(_){}
}
// BUILD 0013: coordinate readback does not need to poll Aladin every rendered frame.
// Limit getSize/pix2world/DOM updates to 10 Hz to reduce persistent main-thread work.
setInterval(gvSyncCoordinateFromAladin,100);


// ============================================================================
// SECTION 025 — TARGET / PROVIDER SURVEY 0006 INITIALIZATION
// ECO: GV200-001 BUILD 0070
// ============================================================================
const target=await window.GalaxyViewerTargetSimbad.init({
    host:hosts.target,
    aladin,
    onSelectProvider:(provider)=>gvSelectSurveyProvider(provider).catch(error=>console.error('GV SURVEY SELECT FAILED',error)),
    onExitSurvey:()=>gvExitSurveyMode()
});
if(typeof target.setProviders!=='function')throw new Error('TARGET SURVEY 0007 API MISMATCH: setProviders() MISSING');
target.button.style.pointerEvents='auto';
target.button.tabIndex=0;
target.button.setAttribute('aria-label','TARGET');
target.button.title='TARGET';

// Diagnostics module removed from the production runtime.



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

// BUILD 0070 — provider Survey source is the already-loaded release master catalog.
// Preserve catalog order by catalogKey/catalogIndex: no Monte Carlo shuffle in Survey mode.
const GV_SURVEY_PROVIDER_META=Object.freeze({
    HUBBLE:Object.freeze({label:'HUBBLE',icon:globalThis.GVProviderArtwork.icon('HUBBLE')}),
    JWST:Object.freeze({label:'JWST',icon:globalThis.GVProviderArtwork.icon('JWST')}),
    CHANDRA:Object.freeze({label:'CHANDRA',icon:globalThis.GVProviderArtwork.icon('CHANDRA')}),
    ESO:Object.freeze({label:'ESO',icon:globalThis.GVProviderArtwork.icon('ESO')}),
    NOIRLAB:Object.freeze({label:'NOIRLAB',icon:globalThis.GVProviderArtwork.icon('NOIRLAB')}),
    SPITZER:Object.freeze({label:'SPITZER',icon:globalThis.GVProviderArtwork.icon('SPITZER')})
});
const GV_SURVEY_PROVIDER_ORDER=Object.freeze(['HUBBLE','JWST','CHANDRA','ESO','NOIRLAB','SPITZER']);
const GV_SURVEY_RUNTIME_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0003.json';
const gvSurveyCatalog=new Map();
function gvSurveyProviderKey(record){
    const provider=[record?.provider,record?.providerKey,record?.catalogKey].filter(Boolean).join(' ').toUpperCase();
    if(/HUBBLE|HST/.test(provider))return 'HUBBLE';
    if(/SPITZER/.test(provider))return 'SPITZER';
    if(/JWST|JAMES WEBB/.test(provider))return 'JWST';
    if(/CHANDRA/.test(provider))return 'CHANDRA';
    if(/NOIRLAB|NOIR LAB/.test(provider))return 'NOIRLAB';
    if(/ESO|EUROPEAN SOUTHERN OBSERVATORY/.test(provider))return 'ESO';
    return provider;
}
const gvSurveyRuntimePayload=await fetch(fresh(GV_SURVEY_RUNTIME_CATALOG_URL),{cache:'force-cache'}).then(response=>{
    if(!response.ok)throw new Error('GV SURVEY RUNTIME CATALOG HTTP '+response.status);
    return response.json();
});
const gvSurveyRuntimeRecords=(Array.isArray(gvSurveyRuntimePayload)?gvSurveyRuntimePayload:gvSurveyRuntimePayload?.records);
if(!Array.isArray(gvSurveyRuntimeRecords)||gvSurveyRuntimeRecords.length===0)throw new Error('GV SURVEY RUNTIME CATALOG INVALID: expected non-empty records from 0003');
for(const provider of GV_SURVEY_PROVIDER_ORDER){
    const records=gvSurveyRuntimeRecords
        .map((record,index)=>Object.freeze({
            ...record,
            provider:String(record?.providerKey||record?.provider||'').toUpperCase(),
            providerLabel:String(record?.providerKey||record?.provider||'').toUpperCase(),
            selectedImageUrl:String(record?.imageUrl||'').trim(),
            catalogKey:String(record?.sourceCatalog||'').trim(),
            catalogIndex:Number.isFinite(Number(record?.sourceIndex))?Number(record.sourceIndex):index,
            fovDegrees:Number(record?.fovXDegrees??record?.fovDegrees),
            aladinRotation:Number(record?.aladinRotation??record?.spatialRotationDeg)
        }))
        .filter(record=>gvSurveyProviderKey(record)===provider&&Number.isFinite(Number(record?.ra))&&Number.isFinite(Number(record?.dec))&&Number.isFinite(Number(record?.fovDegrees))&&Number(record?.fovDegrees)>0&&String(record?.imageUrl||'').trim())
        .sort((a,b)=>String(a.catalogKey||'').localeCompare(String(b.catalogKey||''))||Number(a.catalogIndex||0)-Number(b.catalogIndex||0));
    if(records.length)gvSurveyCatalog.set(provider,Object.freeze(records));
}
target.setProviders(GV_SURVEY_PROVIDER_ORDER.filter(provider=>gvSurveyCatalog.has(provider)).map(provider=>({
    key:provider,
    label:GV_SURVEY_PROVIDER_META[provider].label,
    count:gvSurveyCatalog.get(provider).length,
    icon:GV_SURVEY_PROVIDER_META[provider].icon
})));
if(target.panel?.parentElement!==document.body)document.body.appendChild(target.panel);

/* BUILD 0001 — Galaxy-wide catalog search. */
const gvSearchStyle=document.createElement('style');
gvSearchStyle.id='gv-catalog-search-style';
gvSearchStyle.textContent=`
#gv-catalog-search-tile{position:relative;display:block;width:100%;box-sizing:border-box;margin:0 0 7px;padding:8px 9px 9px;border:1px solid rgba(124,203,255,.78);border-radius:9px;background:linear-gradient(145deg,rgba(8,30,62,.98),rgba(4,15,34,.98));box-shadow:inset 0 1px 1px rgba(225,251,255,.22),inset 0 -3px 7px rgba(0,0,0,.48),0 0 5px rgba(72,191,255,.20);z-index:20}
#gv-catalog-search-tile .gv-search-line{display:grid;grid-template-columns:minmax(0,1fr) 34px;align-items:center;column-gap:8px;height:34px}
#gv-catalog-search-tile .gv-search-icon{position:relative;display:grid;place-items:center;width:32px;height:32px;border:1px solid rgba(124,203,255,.45);border-radius:8px;background:rgba(5,22,47,.82);font:400 19px/1 "Segoe UI Symbol","Noto Sans Symbols 2",sans-serif;box-shadow:0 0 4px rgba(67,207,255,.22),0 0 11px rgba(67,207,255,.12);text-shadow:0 0 4px rgba(223,251,255,.95),0 0 9px rgba(67,207,255,.75);user-select:none}
#gv-catalog-search-tile .gv-search-icon::before{content:"";position:absolute;inset:5px;border-radius:50%;box-shadow:0 0 7px rgba(80,204,255,.28);pointer-events:none}
#gv-catalog-search-input{width:100%;height:32px;box-sizing:border-box;padding:0 9px;border:1px solid rgba(124,203,255,.52);border-radius:7px;outline:none;background:rgba(1,10,24,.90);color:#E9FBFF;font:400 11.5px/1 "GV Space Age",Arial,sans-serif;letter-spacing:.55px;text-transform:uppercase;box-shadow:inset 0 0 6px rgba(0,0,0,.55),0 0 4px rgba(67,207,255,.12);caret-color:#8DDEFF}
#gv-catalog-search-input::placeholder{color:rgba(189,228,245,.76);opacity:1}
#gv-catalog-search-input:focus{border-color:#9BE7FF;box-shadow:inset 0 0 7px rgba(0,0,0,.58),0 0 5px rgba(124,203,255,.38)}
#gv-catalog-search-results{display:none;max-height:min(55vh,420px);overflow-y:auto;margin-top:7px;padding-right:2px;scrollbar-width:thin}
.gv-search-group{margin:6px 0 0}
.gv-search-group-head{padding:4px 7px;color:#9CDEFF;font:400 9px/1 "GV Space Age",Arial,sans-serif;letter-spacing:.55px;text-transform:uppercase;text-shadow:0 0 5px rgba(67,207,255,.38)}
.gv-search-result{appearance:none;-webkit-appearance:none;position:relative;width:100%;display:grid;grid-template-columns:32px minmax(0,1fr) 30px;column-gap:7px;align-items:center;min-height:40px;margin:2px 0;padding:3px 6px 3px 3px;box-sizing:border-box;border:1px solid rgba(67,207,255,.72);border-radius:9px;background:linear-gradient(180deg,rgba(23,78,134,.86),rgba(4,27,62,.96) 58%,rgba(13,90,152,.78));color:#F4FDFF;text-align:left;cursor:pointer;touch-action:manipulation;overflow:hidden;box-shadow:inset 0 1px 2px rgba(225,251,255,.32),inset 0 -2px 4px rgba(0,0,0,.42),0 0 4px rgba(50,190,255,.26)}
.gv-search-result:active{transform:translateY(1px);filter:brightness(1.18)}
.gv-search-result-thumb{width:32px;height:32px;display:flex;align-items:center;justify-content:center;overflow:hidden;border:1px solid rgba(158,220,255,.66);border-radius:8px;background:radial-gradient(circle at 50% 45%,#0B2749 0%,#02070F 72%);box-shadow:inset 0 0 5px rgba(0,0,0,.52),0 0 4px rgba(88,191,255,.32)}
.gv-search-result-thumb img{display:block;width:100%;height:100%;object-fit:contain;object-position:center center;background:#000}
.gv-search-result-icon{width:30px;height:30px;object-fit:cover;object-position:center center;display:block;border:1px solid rgba(158,220,255,.66);border-radius:8px;background:#000;box-shadow:inset 0 0 5px rgba(0,0,0,.52),0 0 4px rgba(88,191,255,.32)}
.gv-search-result-name{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#EAFBFF;font:400 10.5px/13px "GV Space Age",Arial,sans-serif;letter-spacing:.25px}
.gv-search-empty{padding:10px 7px;color:rgba(181,222,241,.76);font:400 9px/13px "GV Space Age",Arial,sans-serif;letter-spacing:.35px;text-align:center}
`;
document.head.appendChild(gvSearchStyle);
const gvSearchTile=document.createElement('div');
gvSearchTile.id='gv-catalog-search-tile';
gvSearchTile.innerHTML='<div class="gv-search-line"><input id="gv-catalog-search-input" type="search" autocomplete="off" autocapitalize="none" spellcheck="false" aria-label="SEARCH GALAXIES" placeholder="SEARCH GALAXIES"><span class="gv-search-icon" aria-hidden="true">🔍</span></div><div id="gv-catalog-search-results" aria-live="polite"></div>';
const gvSearchInput=gvSearchTile.querySelector('#gv-catalog-search-input');
const gvSearchResults=gvSearchTile.querySelector('#gv-catalog-search-results');
const gvSearchIndex=Object.freeze(gvSurveyRuntimeRecords.map(record=>Object.freeze({
    record,
    text:Object.entries(record||{}).flatMap(([key,value])=>{
        if(value===null||value===undefined)return [];
        if(Array.isArray(value))return [key,...value.map(item=>String(item??''))];
        if(typeof value==='object')return [key,JSON.stringify(value)];
        return [key,String(value)];
    }).join(' ').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase()
})));
function gvSearchDisplayName(record){
    return String(record?.name||record?.commonName||record?.displayName||record?.designation||record?.archiveId||record?.id||record?.sourceIndex||'UNNAMED GALAXY').trim();
}
function gvSearchDesignation(record){
    const values=[record?.designation,record?.commonName,record?.pseudonym,record?.archiveId].map(v=>String(v||'').trim()).filter(Boolean);
    const name=gvSearchDisplayName(record);
    return values.find(v=>v.toLowerCase()!==name.toLowerCase())||'';
}
const GV_SEARCH_RESULT_LIMIT=12;
const GV_SEARCH_RENDER_DEBOUNCE_MS=120;
let gvSearchRenderTimer=0;

function gvClearSearchResultImages(){
    gvSearchResults.querySelectorAll('img').forEach(img=>{
        try{img.onload=null;img.onerror=null;img.removeAttribute('src');img.removeAttribute('srcset')}catch(_){}
    });
    gvSearchResults.replaceChildren();
}

function gvSearchRender(query){
    const q=String(query||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
    gvClearSearchResultImages();
    if(!q){gvSearchResults.style.display='none';return}
    const tokens=q.split(/\\s+/).filter(Boolean);
    const matches=gvSearchIndex
        .filter(item=>tokens.every(token=>item.text.includes(token)))
        .sort((a,b)=>{
            const an=gvSearchDisplayName(a.record).toLowerCase();
            const bn=gvSearchDisplayName(b.record).toLowerCase();
            const ap=tokens.every(token=>an.includes(token)),bp=tokens.every(token=>bn.includes(token));
            const as=tokens.every(token=>an.startsWith(token)),bs=tokens.every(token=>bn.startsWith(token));
            if(as!==bs)return bs-as;
            if(ap!==bp)return bp-ap;
            return an.localeCompare(bn);
        });
    gvSearchResults.style.display='block';
    if(!matches.length){
        const empty=document.createElement('div');empty.className='gv-search-empty';empty.textContent='NO GALAXIES FOUND';gvSearchResults.appendChild(empty);return;
    }
    const visibleMatches=matches.slice(0,GV_SEARCH_RESULT_LIMIT);
    const groups=new Map();
    for(const item of visibleMatches){
        const provider=gvSurveyProviderKey(item.record)||'OTHER';
        if(!groups.has(provider))groups.set(provider,[]);
        groups.get(provider).push(item.record);
    }
    const orderedProviders=[...GV_SURVEY_PROVIDER_ORDER,...[...groups.keys()].filter(key=>!GV_SURVEY_PROVIDER_ORDER.includes(key))];
    for(const provider of orderedProviders){
        const records=groups.get(provider);if(!records?.length)continue;
        const group=document.createElement('section');group.className='gv-search-group';
        const head=document.createElement('div');head.className='gv-search-group-head';
        head.textContent=(GV_SURVEY_PROVIDER_META[provider]?.label||provider)+' — '+records.length+' '+(records.length===1?'MATCH':'MATCHES');
        group.appendChild(head);
        for(const record of records){
            const row=document.createElement('button');row.type='button';row.className='gv-search-result';
            const thumbWrap=document.createElement('span');thumbWrap.className='gv-search-result-thumb';
            const thumb=document.createElement('img');
            thumb.alt='';thumb.draggable=false;thumb.loading='lazy';thumb.decoding='async';thumb.fetchPriority='low';
            const candidates=gvSurveyThumbnailCandidates(record,provider);
            let thumbIndex=0;
            const loadThumb=()=>{
                const src=candidates[thumbIndex++];
                if(!src){thumb.removeAttribute('src');return}
                thumb.src=src;
            };
            thumb.onerror=loadThumb;loadThumb();thumbWrap.appendChild(thumb);
            const icon=document.createElement('img');icon.className='gv-search-result-icon';
            icon.src=GV_SURVEY_PROVIDER_META[provider]?.icon||'';icon.alt=provider+' provider';icon.draggable=false;
            const name=document.createElement('span');name.className='gv-search-result-name';name.textContent=gvSearchDisplayName(record);
            row.append(thumbWrap,name,icon);
            row.addEventListener('click',()=>gvNavigateSearchResult(record).catch(error=>console.error('GV GALAXY SEARCH SELECT FAILED',error)));
            group.appendChild(row);
        }
        gvSearchResults.appendChild(group);
    }
    if(matches.length>GV_SEARCH_RESULT_LIMIT){
        console.info('GV SEARCH RESULT CAP',{query:q,total:matches.length,rendered:GV_SEARCH_RESULT_LIMIT});
    }
}

function gvQueueSearchRender(query){
    if(gvSearchRenderTimer)clearTimeout(gvSearchRenderTimer);
    gvSearchRenderTimer=setTimeout(()=>{
        gvSearchRenderTimer=0;
        gvSearchRender(query);
    },GV_SEARCH_RENDER_DEBOUNCE_MS);
}

gvSearchInput.addEventListener('input',()=>gvQueueSearchRender(gvSearchInput.value));
gvSearchInput.addEventListener('keydown',event=>{
    if(event.key==='Escape'){
        if(gvSearchRenderTimer)clearTimeout(gvSearchRenderTimer);
        gvSearchRenderTimer=0;
        gvSearchInput.value='';gvSearchRender('');gvSearchInput.blur();
    }
});
gvSearchTile.addEventListener('pointerdown',event=>event.stopPropagation());
gvSearchTile.addEventListener('click',event=>event.stopPropagation());
const gvSearchPanel=target.panel;
if(gvSearchPanel&&!gvSearchPanel.querySelector('#gv-catalog-search-tile')){
    gvSearchPanel.prepend(gvSearchTile);
    gvSearchPanel.style.overflowY='auto';
    gvSearchPanel.style.maxHeight='min(70vh,560px)';
}


// BUILD 0012 — Survey thumbnail lookup bridge.
// The bridge/index remains remote because it is metadata. Native APK image requests do NOT.
// In GVNative mode, thumbnail candidates are rewritten to the WebViewAssetLoader appassets
// origin and therefore resolve directly from assets/survey-thumbnails/* inside the APK.
// Browser mode continues to use the immutable jsDelivr pack URLs.
const GV_SURVEY_THUMBNAIL_BRIDGE_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/artwork/runtime/gv-survey-thumbnail-bridge-0001.json';
let gvSurveyThumbnailPack=null;
let gvSurveyThumbnailWarmPromise=null;
let gvSurveyThumbnailWarmState={phase:'BRIDGE',loaded:0,failed:0,total:0,bytes:0,packCommit:''};

async function gvWarmSurveyThumbnailPack(pack){
    if(gvSurveyThumbnailWarmPromise)return gvSurveyThumbnailWarmPromise;
    const metas=Object.values(pack?.records||{});
    const urls=[...new Set(metas.map(meta=>String(meta?.path||'').trim()).filter(Boolean).map(path=>pack.baseUrl+path))];
    gvSurveyThumbnailWarmState={phase:'WARMING',loaded:0,failed:0,total:urls.length,bytes:Number(pack?.bridge?.totalThumbnailBytes)||0,packCommit:pack.commit};
    let cursor=0;
    const worker=async()=>{
        for(;;){
            const index=cursor++;
            if(index>=urls.length)return;
            const url=urls[index];
            try{
                const response=await fetch(url,{cache:'force-cache'});
                if(!response.ok)throw new Error('HTTP '+response.status);
                await response.blob();
                gvSurveyThumbnailWarmState.loaded++;
            }catch(error){
                gvSurveyThumbnailWarmState.failed++;
                if(gvSurveyThumbnailWarmState.failed<=6)console.warn('GV SURVEY THUMBNAIL WARM FAILED',url,error);
            }
            const done=gvSurveyThumbnailWarmState.loaded+gvSurveyThumbnailWarmState.failed;
            if(done&&done%250===0)console.info('GV SURVEY THUMBNAIL CACHE',done+'/'+urls.length);
        }
    };
    gvSurveyThumbnailWarmPromise=Promise.all(Array.from({length:6},worker)).then(()=>{
        gvSurveyThumbnailWarmState.phase=gvSurveyThumbnailWarmState.failed?'READY_WITH_ERRORS':'READY';
        console.info('GV SURVEY THUMBNAIL CACHE READY',Object.freeze({...gvSurveyThumbnailWarmState}));
        return gvSurveyThumbnailWarmState;
    });
    return gvSurveyThumbnailWarmPromise;
}

const gvSurveyThumbnailPackReady=(async()=>{
    try{
        const response=await fetch(GV_SURVEY_THUMBNAIL_BRIDGE_URL,{cache:'force-cache'});
        if(!response.ok)throw new Error('THUMBNAIL BRIDGE HTTP '+response.status);
        const bridge=await response.json();
        const commit=String(bridge?.packCommit||'').trim();
        const records=bridge?.records&&typeof bridge.records==='object'?bridge.records:{};
        if(!/^[0-9a-f]{40}$/i.test(commit)||!Object.keys(records).length)throw new Error('THUMBNAIL BRIDGE INVALID');
        const baseUrl='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@'+commit+'/';
        const nativeBaseUrl='https://appassets.androidplatform.net/assets/';
        gvSurveyThumbnailPack=Object.freeze({commit,baseUrl,nativeBaseUrl,bridge:Object.freeze(bridge),records:Object.freeze(records)});
        const recordTotal=Object.keys(records).length;
        gvSurveyThumbnailWarmState={phase:window.GVNative?'READY_LOCAL':'INDEX_READY',loaded:window.GVNative?recordTotal:0,failed:0,total:recordTotal,bytes:Number(bridge?.totalThumbnailBytes)||0,packCommit:commit};
        // BUILD 0004: never pre-warm the entire thumbnail pack in browser mode.
// That downloaded hundreds/thousands of images into the renderer cache before a search.
// Search thumbnails are now lazy, capped, and released when the search changes.
if(!window.GVNative)console.info('GV SURVEY THUMBNAILS LAZY MODE');
        console.info('GV SURVEY THUMBNAIL BRIDGE READY',{records:recordTotal,packCommit:commit,native:Boolean(window.GVNative)});
        return gvSurveyThumbnailPack;
    }catch(error){
        gvSurveyThumbnailWarmState={phase:'FALLBACK',loaded:0,failed:1,total:0,bytes:0,packCommit:''};
        console.error('GV SURVEY THUMBNAIL BRIDGE FAILED',error);
        return null;
    }
})();
window.GalaxySurveyThumbnailCache=Object.freeze({
    ready:gvSurveyThumbnailPackReady,
    get state(){return Object.freeze({...gvSurveyThumbnailWarmState})},
    get packCommit(){return gvSurveyThumbnailPack?.commit||''}
});



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
let gvSurveyMode=null;
const gvSurveyCursors=new Map();

const gvSurveySelectStyle=document.createElement('style');
gvSurveySelectStyle.id='gv-survey-select-galaxy-style';
gvSurveySelectStyle.textContent=`
#gv-survey-select-group{
  position:fixed;z-index:8902;display:none;align-items:center;
  height:38px;margin:0;pointer-events:auto;transform:translateX(-50%)
}
.gv-survey-control-button{
  appearance:none;-webkit-appearance:none;position:relative;height:38px;width:100%;margin:0;overflow:hidden;
  display:grid;grid-template-columns:34px minmax(0,1fr);align-items:center;column-gap:16px;padding:2px;box-sizing:border-box;
  border:1px solid #FFB45A;border-radius:11px;
  background:linear-gradient(180deg,#B96512 0%,#873700 17%,#481600 58%,#A84600 100%);
  color:#FFF0D0;
  box-shadow:inset 0 2px 2px rgba(255,236,198,.55),inset 0 -3px 5px rgba(45,10,0,.66),inset 0 0 10px rgba(255,140,35,.22),0 0 3px rgba(255,226,170,.92),0 0 9px rgba(255,137,28,.68),0 0 18px rgba(255,97,0,.28);
  pointer-events:auto;touch-action:manipulation;outline:none;
  font:400 12.6px/1 "GV Space Age",sans-serif;letter-spacing:.65px;text-transform:uppercase;
  text-shadow:0 0 4px rgba(255,245,220,.95),0 0 10px rgba(255,153,55,.85)
}
.gv-survey-control-button::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.24) 0%,rgba(255,205,128,.08) 29%,transparent 48%);pointer-events:none}
.gv-survey-control-button:active:not(:disabled){transform:translateY(1px) scale(.985);filter:brightness(1.13)}
.gv-survey-control-button:disabled{opacity:1!important;filter:saturate(.82) brightness(.88);cursor:default}
.gv-survey-provider-tile{position:relative;z-index:1;display:grid;place-items:center;width:34px;height:34px;grid-column:1;box-sizing:border-box;border:1px solid rgba(67,207,255,.9);border-radius:8px;background:linear-gradient(145deg,#0B2749 0%,#06214A 52%,#02070F 100%);box-shadow:inset 0 1px 1px rgba(225,251,255,.42),inset 0 -2px 4px rgba(0,0,0,.58),0 0 4px rgba(67,207,255,.48)}
.gv-survey-provider-tile::after{content:"";position:absolute;inset:1px;border-radius:7px;background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(118,225,255,.04) 35%,transparent 52%);pointer-events:none}
.gv-survey-provider-icon{position:relative;z-index:2;display:block;width:27px;height:27px;grid-column:1;object-fit:contain;filter:drop-shadow(0 0 3px rgba(255,205,120,.72))}
.gv-survey-select-label{position:relative;z-index:1;display:block;grid-column:2;min-width:0;padding-left:0;padding-right:0;white-space:nowrap;text-align:left;transform:none}
.gv-survey-selector{width:var(--gv-survey-control-width,236px)!important;max-width:calc(100vw - 28px)!important;box-sizing:border-box!important}
#gv-target-host .gv-target-survey-button.gv-open,#gv-target-host .gv-target-survey-button.gv-selected{
  border-color:#7CCBFF!important;
  background:linear-gradient(145deg,#081B3A 0%,#0B3177 42%,#1484DB 76%,#296DBD 100%)!important;
  box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72),0 0 18px rgba(20,116,219,.35)!important
}
`;
document.head.appendChild(gvSurveySelectStyle);
const GV_SURVEY_SATELLITE_ICON_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/artwork/runtime/navigation/gv-survey-satellite-icon.png';
const gvSurveySelectGroup=document.createElement('div');
gvSurveySelectGroup.id='gv-survey-select-group';
const gvSurveySelectButton=document.createElement('button');
gvSurveySelectButton.id='gv-survey-select-galaxy';
gvSurveySelectButton.className='gv-survey-control-button';
gvSurveySelectButton.type='button';
gvSurveySelectButton.setAttribute('aria-label','SELECT SURVEY');
gvSurveySelectButton.innerHTML=`<span class="gv-survey-provider-tile"><img class="gv-survey-provider-icon" src="${GV_SURVEY_SATELLITE_ICON_URL}" alt="" aria-hidden="true" draggable="false"></span><span class="gv-survey-select-label">SELECT SURVEY</span>`;
gvSurveySelectGroup.append(gvSurveySelectButton);
document.body.appendChild(gvSurveySelectGroup);
function gvHideSurveySelectButton(){gvSurveySelectGroup.style.display='none'}
function gvSurveySelectLabel(){
    const provider=String(gvSurveyMode?.provider||'').toUpperCase();
    const label=provider?(GV_SURVEY_PROVIDER_META[provider]?.label||provider)+' SURVEY':'SELECT SURVEY';
    const e=gvSurveySelectButton.querySelector('.gv-survey-select-label');
    if(e)e.textContent=label;
    gvSurveySelectButton.setAttribute('aria-label',label);
}
function gvSyncSurveyProviderIcon(){
    const img=gvSurveySelectButton.querySelector('.gv-survey-provider-icon');
    if(!img)return;
    const provider=String(gvSurveyMode?.provider||'').toUpperCase();
    const icon=GV_SURVEY_PROVIDER_META[provider]?.icon||GV_SURVEY_SATELLITE_ICON_URL;
    if(img.src!==icon)img.src=icon;
    gvSurveySelectButton.setAttribute('aria-label',provider?provider+' SURVEY':'SELECT SURVEY');
}
function gvPositionProviderSurveyPanel(){
    const panel=target?.panel;
    if(!panel)return;
    if(panel.parentElement!==document.body)document.body.appendChild(panel);
    const r=gvSurveySelectGroup.getBoundingClientRect();
    panel.style.position='fixed';
    panel.style.boxSizing='border-box';
    panel.style.width=Math.round(r.width)+'px';
    panel.style.left=Math.round(r.left+r.width/2)+'px';
    panel.style.right='auto';
    panel.style.top=Math.round(r.bottom+4)+'px';
    panel.style.transform='translateX(-50%)';
    panel.style.zIndex='8901';
}
function gvSyncSurveySelectButton(){
    const coord=document.getElementById('gv-coordinate-host');
    if(!coord){gvHideSurveySelectButton();return}
    const r=coord.getBoundingClientRect();
    if(!r.width||!r.height){gvHideSurveySelectButton();return}
    gvSurveySelectLabel();
    gvSyncSurveyProviderIcon();
    const center=Math.round(r.left+r.width/2);
    const top=Math.round(r.bottom+5);
    const groupWidth=236;
    gvSurveySelectGroup.style.left=center+'px';
    gvSurveySelectGroup.style.top=top+'px';
    gvSurveySelectGroup.style.width=groupWidth+'px';
    document.documentElement.style.setProperty('--gv-survey-control-width',groupWidth+'px');
    // The selector is a navigation control, not a navigation action. Never
    // leave it disabled by a stale in-flight flag; provider selection itself
    // still checks navigationInFlight before changing survey state.
    gvSurveySelectButton.disabled=false;
    gvSurveySelectGroup.style.display='grid';
    if(target?.open)gvPositionProviderSurveyPanel();
}
const gvToggleSurveyProviderMenu=()=>{
    // Keep the provider dropdown independently actuable even if a travel state
    // is still settling. Close the galaxy-list overlay, then explicitly open
    // or close this menu rather than relying on a chained toggle call.
    try{galaxyNavigator.closeSurveySelector?.()}catch(error){console.warn('GV GALAXY SELECTOR CLOSE FAILED',error)}
    // The target module exposes both a Boolean getter and an open() method
    // under the same property name; the method wins in its API object, so
    // target.open is always truthy. Use the module's internal-state-aware toggle.
    target?.toggle?.();
    if(target?.open)requestAnimationFrame(gvPositionProviderSurveyPanel);
};
gvSurveySelectButton.addEventListener('click',gvToggleSurveyProviderMenu);
window.addEventListener('resize',()=>requestAnimationFrame(()=>{gvSyncSurveySelectButton();if(target?.open)gvPositionProviderSurveyPanel()}),{passive:true});
requestAnimationFrame(gvSyncSurveySelectButton);
const randomGalaxyBridge=Object.freeze({
    get activeDestination(){return activeDestination},
    get currentDestination(){return activeDestination},
    getState(){return {
        activeDestination,
        currentDestination:activeDestination,
        surveyProvider:gvSurveyMode?.provider||'',
        surveyRecords:gvSurveyMode?.records||null,
        surveyIndex:Number.isInteger(gvSurveyMode?.index)?gvSurveyMode.index:-1
    }}
});
window.GalaxyRandomGalaxy=randomGalaxyBridge;
const travelPresentation=window.GalaxyRandomTravelPresentation.mount(document.getElementById('aladin-cosmic-command-test'));
const destinationPresentation=window.GalaxyDestinationPresentation.mount(document.getElementById('aladin-cosmic-command-test'),{onBackToSky:()=>requestAnimationFrame(()=>{gvResyncEarthPointerFromAladin();gvSyncSurveySelectButton()})});

const headsUpDisplay=window.GalaxyViewerHeadsUpDisplay.mount(document.getElementById('aladin-cosmic-command-test'),{
    routeEngine:navigationRuntime,
    randomGalaxy:randomGalaxyBridge
});
// GV028: move the existing five-row HUD as one untouched unit and add TRIP as a sibling.
// The HUD's render() owns its children, so the label must never be inserted inside the HUD.
const gvTripHud=headsUpDisplay.root;
if(gvTripHud){
    // The HUD module stylesheet owns top:128px. Override that class rule explicitly.
    const gvTripGeometry=document.createElement('style');
    gvTripGeometry.id='gv028-trip-geometry';
    gvTripGeometry.textContent='.gv-heads-up-display{top:118px!important}.gv-hud-row{min-height:16px!important}';
    document.head.appendChild(gvTripGeometry);
    const gvTripLabel=document.createElement('div');
    gvTripLabel.id='gv-trip-label';
    gvTripLabel.textContent='TRIP';
    Object.assign(gvTripLabel.style,{
        position:'absolute',
        right:'8px',
        top:'105px',
        zIndex:'7211',
        width:'48px',
        textAlign:'center',
        color:'#DDF8FF',
        font:'400 8px/8px "GV Space Age",Arial,sans-serif',
        letterSpacing:'1px',
        textShadow:'0 0 5px rgba(88,191,255,.65)',
        pointerEvents:'none',
        userSelect:'none'
    });
    gvTripHud.parentElement?.appendChild(gvTripLabel);

    // GV028 TRIP cue — exact UHD provider-prompt sequence adapted horizontally.
    // Same directional cascade: first -> second -> third -> destination flash -> reset.
    // Same approved cyan/white double-chevron visual; only uniformly scaled and rotated horizontal.
    const gvTripPointerStyle=document.createElement('style');
    gvTripPointerStyle.id='gv028-trip-pointer-style';
    gvTripPointerStyle.textContent='#gv-trip-pointer .gv-trip-chevron{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}#gv-trip-pointer.gv-traveling .gv-trip-chevron:nth-child(1){animation:gv028TripChevron1 2000ms ease-in-out infinite}#gv-trip-pointer.gv-traveling .gv-trip-chevron:nth-child(2){animation:gv028TripChevron2 2000ms ease-in-out infinite}#gv-trip-pointer.gv-traveling .gv-trip-chevron:nth-child(3){animation:gv028TripChevron3 2000ms ease-in-out infinite}.gv-heads-up-display.gv-trip-destination-cycle .gv-hud-row[data-state="current"]{animation:gv028TripDestination 2000ms ease-in-out infinite}@keyframes gv028TripChevron1{0%,100%{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}8%{opacity:1;filter:drop-shadow(0 0 3px rgba(223,251,255,.96)) drop-shadow(0 0 7px rgba(88,191,255,.95))}25%{opacity:.34;filter:drop-shadow(0 0 2px rgba(88,191,255,.38))}42%{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}}@keyframes gv028TripChevron2{0%,17%,100%{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}25%{opacity:1;filter:drop-shadow(0 0 3px rgba(223,251,255,.96)) drop-shadow(0 0 7px rgba(88,191,255,.95))}42%{opacity:.34;filter:drop-shadow(0 0 2px rgba(88,191,255,.38))}59%{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}}@keyframes gv028TripChevron3{0%,34%,100%{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}42%{opacity:1;filter:drop-shadow(0 0 3px rgba(223,251,255,.96)) drop-shadow(0 0 7px rgba(88,191,255,.95))}59%{opacity:.34;filter:drop-shadow(0 0 2px rgba(88,191,255,.38))}76%{opacity:0;filter:drop-shadow(0 0 0 rgba(88,191,255,0))}}@keyframes gv028TripDestination{0%,70%,75%,95%,100%{filter:none}83%{filter:brightness(1.48) drop-shadow(0 0 5px rgba(221,248,255,.94)) drop-shadow(0 0 10px rgba(88,191,255,.88))}89%{filter:none}}';
    document.head.appendChild(gvTripPointerStyle);
    const gvTripPointer=document.createElement('div');
    gvTripPointer.id='gv-trip-pointer';
    gvTripPointer.setAttribute('aria-hidden','true');
    Object.assign(gvTripPointer.style,{
        position:'absolute',
        right:'61px',
        top:'121px',
        zIndex:'7212',
        display:'none',
        alignItems:'center',
        gap:'0px',
        width:'18px',
        height:'12px',
        visibility:'hidden',
        pointerEvents:'none',
        userSelect:'none'
    });
    for(let i=0;i<3;i++){
        const tooth=document.createElement('span');
        tooth.className='gv-trip-chevron';
        Object.assign(tooth.style,{position:'relative',display:'block',width:'6px',height:'6px',boxSizing:'border-box'});
        const outer=document.createElement('i');
        const inner=document.createElement('b');
        Object.assign(outer.style,{position:'absolute',left:'50%',top:'50%',width:'5.1px',height:'5.1px',borderStyle:'solid',borderLeft:'0',borderBottom:'0',borderWidth:'1.8px',borderColor:'#7CCBFF',boxSizing:'border-box',filter:'drop-shadow(0 0 1.2px rgba(88,191,255,.90))',transform:'translate(-38%,-50%) rotate(45deg)'});
        Object.assign(inner.style,{position:'absolute',left:'50%',top:'50%',width:'3.9px',height:'3.9px',borderStyle:'solid',borderLeft:'0',borderBottom:'0',borderWidth:'1.2px',borderColor:'#DFFBFF',boxSizing:'border-box',filter:'drop-shadow(0 0 .9px rgba(98,216,255,.80))',transform:'translate(-34%,-50%) rotate(45deg)'});
        tooth.append(outer,inner);
        gvTripPointer.appendChild(tooth);
    }
    document.getElementById('aladin-cosmic-command-test')?.appendChild(gvTripPointer);
}
function gvSetTripCycle(active){
    const p=document.getElementById('gv-trip-pointer');
    if(!p)return;
    const on=Boolean(active);
    if(on){
        p.style.visibility='visible';
        p.style.display='flex';
        p.classList.remove('gv-traveling');
        void p.offsetWidth;
        p.classList.add('gv-traveling');
    }else{
        p.classList.remove('gv-traveling');
        p.style.visibility='hidden';
        p.style.display='none';
    }
    document.querySelector('.gv-heads-up-display')?.classList.toggle('gv-trip-destination-cycle',on);
}
// GV028 FIRST-TRIP GUARANTEE: start the TRIP cue directly from the physical
// Random/START button press, before the click callback enters navigation.
galaxyNavigator?.random?.addEventListener('pointerdown',event=>{
    if(event.button!==undefined&&event.button!==0)return;
    if(galaxyNavigator.random.disabled)return;
    gvSetTripCycle(true);
},true);

// ============================================================================
// SECTION 033A — DIRECT ARRIVAL HD OVERLAY / VIGNETTE LAB
// ECO: GV200-001 BUILD 0037
// Presentation only: vignette + CROSS FADE + spring-loaded ZOOM.
// Navigation remains sole owner of destination RA/Dec/FOV/orientation.
// ============================================================================
const DIRECT_HD_LAYER='GV_DIRECT_HD_0056';
let directHdLayerSequence=0;
let directHdLayerName=DIRECT_HD_LAYER;
const CANVAS_IMAGE_PROXY='https://gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev/api/image?url=';
const MAX_BLEND_DIMENSION=1536;
const VIGNETTE=Object.freeze({diameter:1.04,core:0.72,mid1:0.42,mid2:0.72,mid3:0.90,alpha1:0.90,alpha2:0.52,alpha3:0.16});
const GV_VIGNETTE_EXCEPTIONS=Object.freeze({
    potw1947a:Object.freeze({mode:'edge-only',edgeBlend:0.10,decay:1.25})
});
function gvVignetteException(destination,record){
    const values=[
        record?.archiveId,record?.id,record?.imageUrl,record?.selectedImageUrl,record?.sourceUrl,
        destination?.archiveId,destination?.id,destination?.imageUrl,destination?.selectedImageUrl,destination?.sourceUrl
    ].map(value=>String(value||'').toLowerCase());
    for(const [key,config] of Object.entries(GV_VIGNETTE_EXCEPTIONS)){
        if(values.some(value=>value===key||value.includes(key)))return config;
    }
    return null;
}
let directHdOverlay=null;
let directHdDestination=null;
let directHdObjectUrl=null;
const GV_HD_RETIRE_FOV=50;
let gvHdTravelRetired=false;
// BUILD 0004 — bounded HD resource ownership: maximum three tracked object URLs; stale resources are explicitly revoked.
// Navigation/catalog history remains unlimited and lightweight; this bank never retains blobs or Aladin layers.
const GV_HD_RESOURCE_WINDOW=2;
let directHdDisplayWcs=null;
const gvHdObjectUrls=[];
function gvTrackHdObjectUrl(url){
    const value=String(url||'').trim();
    if(!value||gvHdObjectUrls.includes(value))return;
    gvHdObjectUrls.push(value);
    while(gvHdObjectUrls.length>GV_HD_RESOURCE_WINDOW){
        const staleIndex=gvHdObjectUrls.findIndex(item=>item!==directHdObjectUrl);
        if(staleIndex<0)break;
        const [stale]=gvHdObjectUrls.splice(staleIndex,1);
        try{URL.revokeObjectURL(stale)}catch(_){}
    }
}
function gvHdResourceSnapshot(){
    return Object.freeze({
        window:GV_HD_RESOURCE_WINDOW,
        tracked:gvHdObjectUrls.length,
        current:directHdObjectUrl?1:0,
        overlay:directHdOverlay?1:0
    });
}
function gvReleaseHdObjectUrl(url){
    const value=String(url||'').trim();
    if(!value)return;
    const index=gvHdObjectUrls.indexOf(value);
    if(index>=0)gvHdObjectUrls.splice(index,1);
    try{URL.revokeObjectURL(value)}catch(_){}
    if(directHdObjectUrl===value)directHdObjectUrl=null;
}
const GV_MASTER_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/gv-master-catalog.json';
const GV_AVM_RUNTIME_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0003.json';
let gvAvmRuntimePromise=null;
async function gvLoadAvmRuntimeCatalog(){
    if(!gvAvmRuntimePromise){
        gvAvmRuntimePromise=fetch(fresh(GV_AVM_RUNTIME_CATALOG_URL),{cache:'force-cache'})
            .then(response=>{if(!response.ok)throw new Error('GV AVM RUNTIME CATALOG HTTP '+response.status);return response.json()})
            .then(payload=>{
                const records=Array.isArray(payload)?payload:payload?.records;
                if(!Array.isArray(records)||records.length===0)throw new Error('GV AVM RUNTIME CATALOG INVALID: expected non-empty records from 0003');
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
    const record=catalog.byUrl.get(url)||catalog.byId.get(id);
    if(!record)throw new Error('GV AVM RUNTIME RECORD MISSING: '+(url||id));
    const recordUrl=String(record?.imageUrl||'').trim().toLowerCase();
    if(url&&recordUrl!==url)throw new Error('GV AVM RUNTIME IMAGE MISMATCH: destination='+url+' record='+recordUrl);
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
function gvRegisteredTravelStateFromRecord(record){
    const ra=Number(record?.ra),dec=Number(record?.dec);
    const fovX=Number(record?.fovXDegrees??record?.fovDegrees);
    const fovY=Number(record?.fovYDegrees??record?.fovDegrees);
    const rotation=Number(record?.aladinRotation??record?.spatialRotationDeg);
    if(!Number.isFinite(ra)||!Number.isFinite(dec)||!Number.isFinite(fovX)||fovX<=0||!Number.isFinite(fovY)||fovY<=0||!Number.isFinite(rotation))throw new Error('GV REGISTERED TRAVEL METADATA INVALID');
    let imageCenter=[ra,dec];
    const dims=record?.referenceDimension,width=Number(dims?.[0]),height=Number(dims?.[1]);
    if(Number.isFinite(width)&&width>0&&Number.isFinite(height)&&height>0){
        const wcs=gvSyntheticWcsFromRuntimeRecord(record,width,height);
        imageCenter=gvTanPixelToWorld(wcs,(width+1)/2,(height+1)/2);
    }
    return {imageCenter,finalFov:Math.max(fovX,fovY)*1.0,rotation};
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
function directHdSliderOpacity(){
    const slider=Number(crossFadeInput.value);
    return 1-(Math.max(0,Math.min(100,Number.isFinite(slider)?slider:0))/100);
}
function directHdOpacity(){return gvHdTravelRetired?0:directHdSliderOpacity()}
function gvHdEffectiveOpacity(){return directHdOpacity()}
function updateCrossFadeThumb(){
    const v=Math.max(0,Math.min(100,Number(crossFadeInput.value||0)));
    crossFadeControl.thumb.style.top=`${crossFadeControl.rail.offsetTop+((100-v)/100)*crossFadeControl.rail.offsetHeight}px`;
}
function applyDirectHdOpacity(){
    const sliderValue=Math.max(0,Math.min(100,Number(crossFadeInput.value)||0));
    const value=gvHdTravelRetired?0:directHdSliderOpacity();
    let registered=null;
    try{registered=aladin.getOverlayImageLayer?.(directHdLayerName)||null}
    catch(error){console.warn('GV CROSSFADE LAYER LOOKUP FAILED',error)}
    const targets=[];
    if(registered)targets.push(registered);
    if(directHdOverlay&&directHdOverlay!==registered)targets.push(directHdOverlay);
    const results=[];
    for(const target of targets){
        if(!target)continue;
        try{
            let method='none';
            if(typeof target.setOpacity==='function'){target.setOpacity(value);method='setOpacity'}
            else if(typeof target.setAlpha==='function'){target.setAlpha(value);method='setAlpha'}
            else if(typeof target.setOptions==='function'){target.setOptions({opacity:value});method='setOptions'}
            const readback=typeof target.getOpacity==='function'?target.getOpacity():
                (typeof target.getAlpha==='function'?target.getAlpha():target.opacity??null);
            results.push({registered:target===registered,method,requested:value,readback,layerName:directHdLayerName});
        }catch(error){console.warn('GV CROSSFADE OPACITY APPLY FAILED',{layer:directHdLayerName,value,error})}
    }
    const detail={build:GV200001_BUILD,slider:sliderValue,requestedOpacity:value,travelRetired:gvHdTravelRetired,registeredFound:!!registered,retainedFound:!!directHdOverlay,results};
    if(!results.length||results.some(result=>result.readback!==null&&Math.abs(Number(result.readback)-value)>0.001)){
        console.warn('GV CROSSFADE OPACITY READBACK MISMATCH',detail);
    }else{console.info('GV CROSSFADE OPACITY APPLIED',detail)}
    updateCrossFadeThumb();
    return value;
}
function setCrossFadeFromY(clientY){
    const r=crossFadeControl.rail.getBoundingClientRect();
    if(!r.height)return;
    const sliderValue=Math.max(0,Math.min(100,Math.round(((r.bottom-clientY)/r.height)*100)));
    crossFadeInput.value=String(sliderValue);
    console.info('GV CROSSFADE INPUT',{build:GV200001_BUILD,pointerY:clientY,slider:sliderValue,railTop:r.top,railBottom:r.bottom});
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
Object.assign(gvFovReadout.style,{position:'absolute',right:'2px',top:'calc(50% - 108px)',zIndex:'7313',width:'74.4px',height:'19.44px',padding:'0',border:'1px solid rgba(124,203,255,.92)',borderRadius:'4.8px',background:'linear-gradient(145deg,rgba(4,20,48,.96),rgba(12,52,116,.96))',boxShadow:'0 0 5px rgba(158,230,255,.95),0 0 12px rgba(46,172,255,.72)',font:'400 10.32px/19.44px "GV Space Age","Space Age",Arial,sans-serif',letterSpacing:'.36px',color:'#8fe7ff',textShadow:'0 0 3px #d8f8ff,0 0 8px rgba(66,195,255,.95)',whiteSpace:'nowrap',pointerEvents:'none'});Object.assign(gvFovReadout.querySelector('#gv-fov-title').style,{position:'absolute',left:'50%',top:'-16.8px',transform:'translateX(-50%)',lineHeight:'10.8px',fontSize:'8.64px',color:'#8fe7ff'});Object.assign(gvFovReadout.querySelector('#gv-fov-f').style,{position:'relative',left:'4.8px'});Object.assign(gvFovReadout.querySelector('#gv-fov-rest').style,{position:'relative',left:'4.8px'});Object.assign(gvFovReadout.querySelector('#gv-fov-int').style,{position:'absolute',right:'38.4px',width:'30.24px',textAlign:'right',fontVariantNumeric:'tabular-nums'});Object.assign(gvFovReadout.querySelector('#gv-fov-dot').style,{position:'absolute',left:'34.8px',width:'4.8px',textAlign:'center'});Object.assign(gvFovReadout.querySelector('#gv-fov-frac').style,{position:'absolute',left:'39.6px',width:'25.92px',textAlign:'left',fontVariantNumeric:'tabular-nums'});
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
const GV_FOV_REPORT_MS=100;
const GV_FOV_REPORT_HYSTERESIS=0.001;
function gvSyncFovReadout(){
    // Keep the FOV readout live during the motion-suspended flight phases.
    try{
        const raw=aladin.getFov?.(),fov=Number(Array.isArray(raw)?raw[0]:raw);
        if(Number.isFinite(fov)&&fov>=0){
            if(gvDisplayedFov===null||Math.abs(fov-gvDisplayedFov)>=GV_FOV_REPORT_HYSTERESIS)gvDisplayedFov=Number(fov.toFixed(3));
            const parts=gvDisplayedFov.toFixed(3).split('.');
            gvSetFovDigits(gvFovReadout.querySelector('#gv-fov-int'),parts[0].padStart(3,' '),'10.08px');
            gvSetFovDigits(gvFovReadout.querySelector('#gv-fov-frac'),parts[1],'8.64px');
        }
    }catch(_){}
}
gvSyncFovReadout();
setInterval(gvSyncFovReadout,GV_FOV_REPORT_MS);

let zoomCommand=0;
let zoomFrame=0;
let gvAutoZoom=null;
// SINGLE HD TRAVEL AUTHORITY — keep the active raster registered during
// Random Galaxy travel. Visibility is retired only by the 55° FOV rule below.
let gvHdTravelHoldAt=0;
function gvHoldDirectHdDuringTravel(now){
    if(!directHdOverlay)return;
    // BUILD 0018: a registered Aladin image layer must not be re-added as a
    // keep-alive. setOverlayImageLayer() replaces/reprocesses the image layer.
    // Keep the existing layer registered; only refresh its opacity.
    try{applyDirectHdOpacity()}catch(_){ }
}
function gvSetZoomCommand(command){
    zoomCommand=Math.max(-1,Math.min(1,Number(command)||0));
    zoomControl.thumb.style.top=`${zoomControl.rail.offsetTop+((zoomCommand+1)/2)*zoomControl.rail.offsetHeight}px`;
}
function zoomStep(){
    zoomFrame=0;
    if(!zoomCommand)return;
    try{
        const now=performance.now();
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

async function gvLoadGate2MImage(url,destination=null,record=null){
    if(typeof createImageBitmap!=='function')throw new Error('createImageBitmap unavailable');
    const attempts=[url,CANVAS_IMAGE_PROXY+encodeURIComponent(url)+'&consumer=gv0037'];
    let last='';
    for(const source of attempts){
        try{
            const response=await fetch(source,{mode:'cors',credentials:'omit',cache:'no-store',redirect:'follow'});
            if(!response.ok)throw new Error('HTTP '+response.status);
            let blob=await response.blob();
            if(!blob||blob.size<=0)throw new Error('EMPTY IMAGE BLOB');
            let bitmap=await createImageBitmap(blob);blob=null;
            let workingBitmap=null,canvas=null,resizeCanvas=null;
            try{
                const sourceW=bitmap.width,sourceH=bitmap.height,sourceMax=Math.max(sourceW,sourceH);
                workingBitmap=bitmap;let w=sourceW,h=sourceH;
                if(sourceMax>MAX_BLEND_DIMENSION){
                    const scale=MAX_BLEND_DIMENSION/sourceMax;
                    const targetW=Math.max(1,Math.round(sourceW*scale));
                    const targetH=Math.max(1,Math.round(sourceH*scale));
                    try{
                        workingBitmap=await createImageBitmap(bitmap,{resizeWidth:targetW,resizeHeight:targetH,resizeQuality:'high'});
                    }catch(_){
                        resizeCanvas=document.createElement('canvas');resizeCanvas.width=targetW;resizeCanvas.height=targetH;
                        const resizeCtx=resizeCanvas.getContext('2d');if(!resizeCtx)throw new Error('HARD 1536 RESIZE CONTEXT UNAVAILABLE');
                        resizeCtx.drawImage(bitmap,0,0,targetW,targetH);
                        workingBitmap=await createImageBitmap(resizeCanvas);
                        resizeCanvas.width=0;resizeCanvas.height=0;
                    }
                    try{bitmap.close?.()}catch(_){}
                    w=targetW;h=targetH;
                    console.info('GV HD HARD 1536 RESIZE',{source:[sourceW,sourceH],target:[w,h]});
                }
                canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;
                const ctx=canvas.getContext('2d');if(!ctx)throw new Error('VIGNETTE 2D CONTEXT UNAVAILABLE');
                ctx.drawImage(workingBitmap,0,0,w,h);
                const exception=gvVignetteException(destination,record);
                const p=VIGNETTE,cx=w/2,cy=h/2,actualAspect=Math.max(w/h,h/w),highAspect=actualAspect>1.3;
                if(exception?.mode==='edge-only'){
                    const imageData=ctx.getImageData(0,0,w,h),d=imageData.data;
                    const edgePixels=Math.max(1,Math.min(w,h)*Number(exception.edgeBlend||0));
                    const decay=Math.max(.1,Number(exception.decay||1));
                    for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++){
                        const i=(yy*w+xx)*4,edgePx=Math.min(xx,yy,w-1-xx,h-1-yy);
                        const t=Math.max(0,Math.min(1,edgePx/edgePixels));
                        const smooth=t*t*(3-2*t);
                        const expTail=(1-Math.exp(-decay*t))/(1-Math.exp(-decay));
                        const alpha=.72*smooth+.28*expTail;
                        d[i+3]=Math.round(d[i+3]*Math.max(0,Math.min(1,alpha)));
                    }
                    ctx.putImageData(imageData,0,0);
                }else if(highAspect){
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
            }finally{
                if(workingBitmap&&workingBitmap!==bitmap){try{workingBitmap.close?.()}catch(_){}}
                if(bitmap){try{bitmap.close?.()}catch(_){}}
                for(const tempCanvas of [canvas,resizeCanvas]){if(tempCanvas){try{tempCanvas.width=0;tempCanvas.height=0}catch(_){}}}
            }
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
    const prepStarted=performance.now();
    const raster=await gvLoadGate2MImage(url,destination,record);
    const imageObjectUrl=URL.createObjectURL(raster.blob);gvTrackHdObjectUrl(imageObjectUrl);
    const displayWcs=gvSyntheticWcsFromRuntimeRecord(record,raster.width,raster.height);
    const imageCenter=gvTanPixelToWorld(displayWcs,(raster.width+1)/2,(raster.height+1)/2);
    const prepared={destination,record,imageUrl:url,imageObjectUrl,displayWcs,imageCenter,rotation,finalFov:Math.max(fovX,fovY)*1.0};
    console.info('GV HD PREPARED',{ms:Math.round(performance.now()-prepStarted),name:destination?.name||destination?.objectName||'',resources:gvHdResourceSnapshot()});
    return prepared;
}
function gvInstallPreparedHd(prepared){
    const {destination,imageObjectUrl,displayWcs}=prepared;
    if(!imageObjectUrl)return Promise.reject(new Error('GV PREPARED HD OBJECT URL MISSING'));
    gvHdTravelRetired=false;
    const previous={overlay:directHdOverlay,destination:directHdDestination,objectUrl:directHdObjectUrl,displayWcs:directHdDisplayWcs,layerName:directHdLayerName};
    const layerName=DIRECT_HD_LAYER+'_'+(++directHdLayerSequence);
    let resolveReady,rejectReady;
    const ready=new Promise((resolve,reject)=>{resolveReady=resolve;rejectReady=reject});
    let settled=false;
    const retirePrevious=()=>{
        if(previous.layerName&&previous.overlay){try{aladin.removeImageLayer?.(previous.layerName)}catch(_){}}
        if(previous.objectUrl&&previous.objectUrl!==imageObjectUrl)gvReleaseHdObjectUrl(previous.objectUrl);
    };
    const layer=A.image(imageObjectUrl,{
        name:layerName,imgFormat:'png',wcs:displayWcs,opacity:directHdOpacity(),
        successCallback:()=>{
            if(settled)return;settled=true;
            if(activeDestination!==destination){
                try{aladin.removeImageLayer?.(layerName)}catch(_){}
                gvReleaseHdObjectUrl(imageObjectUrl);
                resolveReady(false);
                return;
            }
            directHdOverlay=layer;
            directHdDestination=destination;
            directHdObjectUrl=imageObjectUrl;
            directHdDisplayWcs=displayWcs;
            directHdLayerName=layerName;
            applyDirectHdOpacity();
            retirePrevious();
            console.info('GV HD LAYER HANDOFF COMPLETE',{layer:layerName,previousLayer:previous.layerName||null});
            resolveReady(true);
        },
        errorCallback:error=>{
            if(settled)return;settled=true;
            try{aladin.removeImageLayer?.(layerName)}catch(_){}
            gvReleaseHdObjectUrl(imageObjectUrl);
            rejectReady(error);
            console.error('GV DIRECT HD JSON-WCS LAYER LOAD FAILED',error);
        }
    });
    aladin.setOverlayImageLayer(layer,layerName);
    return ready;
}
function gvRestoreDirectHd(){
    if(!directHdObjectUrl||!directHdDestination||activeDestination!==directHdDestination)return false;
    try{
        if(directHdOverlay){
            aladin.setOverlayImageLayer(directHdOverlay,directHdLayerName);
            gvHdTravelRetired=false;
            applyDirectHdOpacity();
            console.info('GV HD RESTORED — EXISTING ALADIN LAYER REATTACHED');
            return true;
        }
        if(!directHdDisplayWcs)return false;
        const destination=directHdDestination,objectUrl=directHdObjectUrl;
        const layer=A.image(objectUrl,{name:directHdLayerName,imgFormat:'png',wcs:directHdDisplayWcs,opacity:directHdOpacity(),successCallback:()=>{if(directHdObjectUrl!==objectUrl)return;directHdOverlay=layer;gvHdTravelRetired=false;applyDirectHdOpacity();console.info('GV HD RESTORED — EXISTING OBJECT URL REINSTALLED')},errorCallback:error=>console.warn('GV HD RESTORE FAILED',error)});
        directHdOverlay=layer;
        aladin.setOverlayImageLayer(layer,directHdLayerName);
        return true;
    }catch(error){console.warn('GV HD RESTORE SKIPPED',error);return false}
}
window.addEventListener('focus',()=>{if(document.visibilityState==='visible')setTimeout(gvRestoreDirectHd,0)});
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')setTimeout(gvRestoreDirectHd,0)});
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
async function gvFly130H(prepared,{firstHomeTrip=false,onZoomInStart=null,onZoomOutComplete=null,registeredPromise=null,switchToSphericalAtApex=false}={}){
    const initialCenter=prepared?.imageCenter;let ra1=Number(initialCenter?.[0]),dec1=Number(initialCenter?.[1]),finalFov=Number(prepared?.finalFov),targetRotation=Number(prepared?.rotation);
    if(!Number.isFinite(ra1)||!Number.isFinite(dec1)||!Number.isFinite(finalFov)||finalFov<=0||!Number.isFinite(targetRotation))throw new Error('GV 130H DESTINATION STATE INVALID');
    const startRaDec=aladin.getRaDec?.()||[HOME.ra,HOME.dec],ra0=Number(startRaDec[0]),dec0=Number(startRaDec[1]),rawFov=aladin.getFov?.(),startFov=Number(Array.isArray(rawFov)?rawFov[0]:rawFov);
    let startRotation=0;try{startRotation=Number(aladin.getRotation?.()??aladin.view?.rotation??0)||0}catch(_){}
    if(firstHomeTrip){
        if(registeredPromise){
            try{
                const registered=await registeredPromise;
                const center=registered?.imageCenter,nra=Number(center?.[0]),ndec=Number(center?.[1]),nfov=Number(registered?.finalFov),nrotation=Number(registered?.rotation);
                if(Number.isFinite(nra)&&Number.isFinite(ndec)&&Number.isFinite(nfov)&&nfov>0&&Number.isFinite(nrotation)){
                    ra1=nra;dec1=ndec;finalFov=nfov;targetRotation=nrotation;
                }
            }catch(error){console.error('GV 130H FIRST-TRIP REGISTERED DESTINATION PREPARE FAILED',error)}
        }
        const translateSeconds=3.0,zoomSeconds=6.0,durationSeconds=translateSeconds+zoomSeconds;
        const rotationDelta=gvFlightNormalizeRotationDelta(targetRotation-startRotation);
        const translateStarted=performance.now();let lastSample=-1;
        await new Promise((resolve,reject)=>{
            const frame=now=>{try{
                const elapsed=Math.min(translateSeconds*1000,now-translateStarted),u=gvFlightNavigationSmootherstep(elapsed/(translateSeconds*1000)),sample=Math.floor(elapsed/10);
                if(sample!==lastSample){
                    const pos=gvFlightGreatCirclePosition(ra0,dec0,ra1,dec1,u),rotation=startRotation+rotationDelta*u;
                    if(elapsed>0)gvSetEarthPointerPosition(pos[0],pos[1],true);
                    aladin.gotoRaDec(pos[0],pos[1]);coordinate?.update(pos[0],pos[1]);
                    aladin.setRotation(rotation);
                    lastSample=sample;
                }
                if(elapsed<translateSeconds*1000){requestAnimationFrame(frame);return}resolve();
            }catch(error){reject(error)}};requestAnimationFrame(frame);
        });
        aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1);gvSetEarthPointerPosition(ra1,dec1,true);
        aladin.setRotation(targetRotation);
        try{onZoomInStart?.()}catch(error){console.error('GV 130H FIRST-TRIP ZOOM-IN CALLBACK FAILED',error)}
        const zoomStarted=performance.now(),zoomStartRaw=aladin.getFov?.(),zoomStartFov=Number(Array.isArray(zoomStartRaw)?zoomStartRaw[0]:zoomStartRaw);lastSample=-1;
        await new Promise((resolve,reject)=>{
            const frame=now=>{try{
                const elapsed=Math.min(zoomSeconds*1000,now-zoomStarted),p=gvFlightNavigationSmootherstep(elapsed/(zoomSeconds*1000)),sample=Math.floor(elapsed/10);
                if(sample!==lastSample){const fov=gvFlightLogLerp(zoomStartFov,finalFov,p);gvHoldDirectHdDuringTravel(now);aladin.setFov(fov);lastSample=sample}
                if(elapsed<zoomSeconds*1000){requestAnimationFrame(frame);return}resolve();
            }catch(error){reject(error)}};requestAnimationFrame(frame);
        });
        aladin.setFov(finalFov);
        return prepared;
    }
    if(registeredPromise)registeredPromise.then(registered=>{const center=registered?.imageCenter,nra=Number(center?.[0]),ndec=Number(center?.[1]),nfov=Number(registered?.finalFov),nrotation=Number(registered?.rotation);if(Number.isFinite(nra)&&Number.isFinite(ndec)&&Number.isFinite(nfov)&&nfov>0&&Number.isFinite(nrotation)){ra1=nra;dec1=ndec;finalFov=nfov;targetRotation=nrotation}}).catch(error=>console.error('GV 130H REGISTERED DESTINATION PREPARE FAILED',error));
    const durationSeconds=17,duration=durationSeconds*1000,started=performance.now(),zoomInThreshold=.50,zoomOutCompleteThreshold=.30;let lastSample=-1,destinationCenterApplied=false,birdseyeSettled=false,zoomInStarted=false,zoomOutCompleted=false,projectionSwitchedAtApex=false;
    await new Promise((resolve,reject)=>{
        const frame=now=>{try{
            const elapsedMs=now-started,t=Math.min(1,elapsedMs/duration),sample=Math.floor(elapsedMs/10);
            // BUILD 0028: only FOV changes during 0–30% and 70–100%.
            // Suspend application polling in both phases; the FOV readout stays live.
            window.GV_NAV_BACKGROUND_SUSPENDED=true; // Keep application polling suspended for the entire flight.
            window.GV_NAV_HIPS_FETCH_SUSPENDED=(t<Math.max(0,1-8/durationSeconds)); // BUILD 0053: preserve T-minus-eight HiPS tile fetching.

            if(t>=zoomOutCompleteThreshold&&!zoomOutCompleted){
                zoomOutCompleted=true;
                try{onZoomOutComplete?.()}catch(error){console.error('GV 130H ZOOM-OUT COMPLETE CALLBACK FAILED',error)}
            }
            if(switchToSphericalAtApex&&!projectionSwitchedAtApex&&t>=zoomInThreshold){projectionSwitchedAtApex=true;try{aladin.setFov(55);hamburger?.selectProjection?.('SPHERICAL');console.info('GV PROJECTION AUTO-SWITCH MOL→SIN AT 55° APEX')}catch(error){console.error('GV SPHERICAL APEX SWITCH FAILED',error)}}
            if(!zoomInStarted&&t>=zoomInThreshold){
                zoomInStarted=true;
                try{
                    console.info('GV HD HANDOFF REQUESTED — ZOOM-IN START');
                    onZoomInStart?.();
                }catch(error){console.error('GV 130H ZOOM-IN CALLBACK FAILED',error)}
            }
            if(t<1&&sample!==lastSample){
                const state=gvFlightStateAt(t*durationSeconds,{firstHomeTrip:false,startFov,finalFov,maxFov:55,startRotation,targetRotation});
                if(t<zoomOutCompleteThreshold){
                    // Phase 1 (0–30%): FOV is the only changing view property.
                    aladin.setFov(state.fov);
                    lastSample=sample;
                }else if(t>=.70){
                    // Phase 3 (70–100%): settle the bird's-eye view once, then
                    // issue FOV commands only until arrival.
                    if(!birdseyeSettled){
                        gvSetEarthPointerPosition(ra1,dec1,true);
                        aladin.gotoRaDec(ra1,dec1);
                        coordinate?.update(ra1,dec1);
                        aladin.setRotation(targetRotation);
                        destinationCenterApplied=true;
                        birdseyeSettled=true;
                    }
                    aladin.setFov(state.fov);
                    lastSample=sample;
                }else{
                    // Phase 2 (30–70%): normal travel motion and app updates resume.
                    if(t<=zoomInThreshold&&state.fov>=GV_HD_RETIRE_FOV&&!gvHdTravelRetired){gvHdTravelRetired=true;applyDirectHdOpacity();console.info('GV HD RETIRED — 50° FOV THRESHOLD',{fov:Number(state.fov.toFixed(2))});}
                    aladin.setFov(state.fov);
                    if(state.translation>0&&state.translation<1){const pos=gvFlightGreatCirclePosition(ra0,dec0,ra1,dec1,state.translation);gvSetEarthPointerPosition(pos[0],pos[1],true);aladin.gotoRaDec(pos[0],pos[1]);coordinate?.update(pos[0],pos[1])}
                    else if(state.translation>=1&&!destinationCenterApplied){gvSetEarthPointerPosition(ra1,dec1,true);aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1);destinationCenterApplied=true}
                    if(Math.abs(state.rotation-startRotation)>0.0001)aladin.setRotation(state.rotation);
                    lastSample=sample;
                }
            }
            if(t<1){requestAnimationFrame(frame);return}
            if(!destinationCenterApplied){gvSetEarthPointerPosition(ra1,dec1,true);aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1)}
            aladin.setFov(finalFov);if(!birdseyeSettled)aladin.setRotation(targetRotation);gvHdTravelRetired=false;applyDirectHdOpacity();console.info('GV HD CROSSFADE RESTORED AT ARRIVAL');window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;resolve(prepared);
        }catch(error){window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;reject(error)}};requestAnimationFrame(frame);
    });
    return prepared;
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
const GV_PRESENTATION_PROVIDER_BY_CATALOG=Object.freeze({hubble:'HUBBLE',jwst:'JWST',eso:'ESO',chandra:'CHANDRA',spitzer:'SPITZER',noirlab:'NOIRLAB'});
const GV_PRESENTATION_ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/';
let gvPresentationMasterPromise=null;
const gvPresentationCatalogPromises=new Map();
const gvPresentationCatalogs=new Map();
async function gvLoadPresentationCatalog(key){
    const catalogKey=String(key||'').trim().toLowerCase();
    if(!catalogKey)return null;
    if(gvPresentationCatalogs.has(catalogKey))return gvPresentationCatalogs.get(catalogKey);
    if(gvPresentationCatalogPromises.has(catalogKey))return gvPresentationCatalogPromises.get(catalogKey);
    const promise=(async()=>{
        if(!gvPresentationMasterPromise){
            gvPresentationMasterPromise=fetch(fresh(GV_MASTER_CATALOG_URL),{cache:'force-cache'})
                .then(response=>{if(!response.ok)throw new Error('GV PRESENTATION MASTER CATALOG HTTP '+response.status);return response.json()});
        }
        const master=await gvPresentationMasterPromise;
        const relative=String(master?.catalogs?.[catalogKey]||'').trim();
        if(!relative)throw new Error('GV PRESENTATION SOURCE CATALOG MISSING: '+catalogKey);
        const response=await fetch(fresh(GV_PRESENTATION_ROOT+relative),{cache:'force-cache'});
        if(!response.ok)throw new Error('GV PRESENTATION SOURCE CATALOG HTTP '+response.status+': '+catalogKey);
        const payload=await response.json();
        const entries=Array.isArray(payload)?payload:(Array.isArray(payload?.entries)?payload.entries:[]);
        if(!entries.length)throw new Error('GV PRESENTATION SOURCE CATALOG EMPTY: '+catalogKey);
        const byId=new Map(),byUrl=new Map();
        entries.forEach((entry,index)=>{
            const id=String(entry?.archiveId||entry?.id||'').trim().toLowerCase();
            const urls=[entry?.selectedImageUrl,entry?.imageUrl,entry?.hdUrl,entry?.sourceUrl].map(v=>String(v||'').trim().toLowerCase()).filter(Boolean);
            if(id)byId.set(id,{entry,index});
            for(const url of urls)byUrl.set(url,{entry,index});
        });
        const catalog=Object.freeze({entries,byId,byUrl});
        gvPresentationCatalogs.set(catalogKey,catalog);
        return catalog;
    })().catch(error=>{
        gvPresentationCatalogPromises.delete(catalogKey);
        throw error;
    });
    gvPresentationCatalogPromises.set(catalogKey,promise);
    return promise;
}
async function gvPresentationDestination(destination){
    const rawCatalogKey=String(destination?.catalogKey||'').trim().toLowerCase();
    const providerKey=String(destination?.providerKey||destination?.provider||'').trim().toLowerCase();
    const key=GV_PRESENTATION_PROVIDER_BY_CATALOG[rawCatalogKey]?rawCatalogKey:(GV_PRESENTATION_PROVIDER_BY_CATALOG[providerKey]?providerKey:'');
    const provider=GV_PRESENTATION_PROVIDER_BY_CATALOG[key];
    const enriched=provider&&String(destination?.provider||'').trim().toUpperCase()!==provider
        ? Object.freeze({...destination,provider})
        : destination;
    // Display/science metadata must come from the matching individual provider catalog.
    // Never substitute another row by catalogIndex or fall back to route/runtime values.
    const blankCatalogMetadata=()=>Object.freeze({
        ...enriched,
        designation:'',
        name:'',
        commonName:'',
        pseudonym:'',
        constellation:'',
        distanceMly:null,
        distance:'',
        sizeKly:Object.freeze([]),
        physicalSizeLy:null,
        ageYears:null,
        age:'',
        imageType:'',
        title:'',
        description:''
    });
    try{
        if(!key)throw new Error('PROVIDER CATALOG KEY MISSING');
        const catalog=await gvLoadPresentationCatalog(key);
        const id=String(destination?.archiveId||destination?.id||destination?.providerId||'').trim().toLowerCase();
        const url=String(destination?.imageUrl||destination?.selectedImageUrl||destination?.hdUrl||'').trim().toLowerCase();
        const match=(id&&catalog?.byId.get(id))||(url&&catalog?.byUrl.get(url));
        const source=match?.entry;
        if(!source){
            console.warn('GV PRESENTATION CATALOG IDENTITY MATCH MISSING; SCIENCE METADATA CLEARED',{
                catalogKey:key,archiveId:id,imageUrl:url,catalogIndex:destination?.catalogIndex
            });
            return blankCatalogMetadata();
        }
        const science=source?.science||{};
        const validNumber=value=>value!==null&&value!==undefined&&value!==''&&Number.isFinite(Number(value));
        // 3C 321 has one canonical science record across providers. Hubble's
        // image-specific row carries a conflicting 1.25 BLY / lookback-derived
        // age, so preserve the verified Chandra distance and cosmological age
        // regardless of which telescope supplies the displayed image.
        const is3C321=[source?.archiveId,source?.id,source?.name,source?.designation,source?.displayName,source?.title,destination?.archiveId,destination?.id,destination?.name,destination?.designation,destination?.displayName,destination?.title]
            .some(value=>/3c\s*[- ]?321/i.test(String(value||'')));
        const canonicalDistanceMly=is3C321?1400:(validNumber(science?.distanceMly)?Number(science.distanceMly):null);
        const canonicalCosmicAgeYears=is3C321?12.1334e9:(validNumber(science?.cosmicAgeGyr)?Number(science.cosmicAgeGyr)*1e9:(validNumber(science?.ageGyr)?Math.max(0,13.4667-Number(science.ageGyr))*1e9:null));
        const sizeKly=Array.isArray(science?.sizeKly)
            ?science.sizeKly.filter(validNumber).map(Number)
            :(Array.isArray(source?.sizeKly)?source.sizeKly.filter(validNumber).map(Number):[]);
        const physicalSizeLy=validNumber(source?.physicalSizeLy)
            ?Number(source.physicalSizeLy)
            :(sizeKly.length?Math.max(...sizeKly)*1000:null);
        return Object.freeze({
            ...enriched,
            sourceUrl:source?.sourceUrl||'',
            archiveId:source?.archiveId||source?.id||'',
            designation:source?.designation||source?.name||'',
            name:source?.displayName||source?.name||'',
            commonName:source?.displayName||source?.name||'',
            pseudonym:source?.pseudonym||source?.commonName||source?.displayName||source?.name||'',
            constellation:source?.constellation||'',
            distanceMly:canonicalDistanceMly,
            distance:is3C321?'1.4 billion light-years':(science?.distanceDisplay||source?.distance||''),
            sizeKly:Object.freeze(sizeKly),
            physicalSizeLy,
            ageYears:canonicalCosmicAgeYears,
            age:is3C321?'EST. 12.13 GYR':(science?.ageDisplay||source?.ageDisplay||''),
            imageType:source?.imageType||'',
            title:source?.title||'',
            description:source?.description||''
        });
    }catch(error){
        console.warn('GV PRESENTATION METADATA HYDRATION FAILED; SCIENCE METADATA CLEARED',key,error);
        return blankCatalogMetadata();
    }
}

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


function gvCancelProviderAll(){
    try{
        if(window.GVNative&&typeof window.GVNative.cancelProviderAll==='function'){
            window.GVNative.cancelProviderAll();
            console.info('GV PROVIDER WORK FULLY CANCELLED BEFORE SKY NAVIGATION');
        }else if(window.GVNative&&typeof window.GVNative.cancelProvider==='function'){
            window.GVNative.cancelProvider();
            console.info('GV PROVIDER WORK CANCELLED THROUGH LEGACY BRIDGE BEFORE SKY NAVIGATION');
        }
    }catch(error){console.warn('GV PROVIDER FULL CANCEL SKIPPED',error)}
}
const GV_PROVIDER_PORTAL_WINDOW=3;
const gvProviderPortalOrigins=[];
function gvReleaseProviderPortalOrigin(origin){
    const value=String(origin||'').trim();
    if(!value)return;
    for(const rel of ['dns-prefetch','preconnect']){
        document.querySelectorAll('link[data-gv-provider-warm="'+rel+'"]').forEach(link=>{
            try{if(String(link.href||'').replace(/\/$/,'')===value)link.remove()}catch(_){}
        });
    }
}
function gvTrackProviderPortal(origin){
    const value=String(origin||'').trim().replace(/\/$/,'');
    if(!value)return;
    const existing=gvProviderPortalOrigins.indexOf(value);
    if(existing>=0)gvProviderPortalOrigins.splice(existing,1);
    gvProviderPortalOrigins.push(value);
    while(gvProviderPortalOrigins.length>GV_PROVIDER_PORTAL_WINDOW){
        const stale=gvProviderPortalOrigins.shift();
        gvReleaseProviderPortalOrigin(stale);
        try{
            if(window.GVNative&&typeof window.GVNative.releaseProviderPortal==='function'){
                window.GVNative.releaseProviderPortal(stale);
            }
        }catch(_){}
    }
}
function gvPrewarmProviderWebsite(destination){
    const url=String(destination?.sourceUrl||'').trim();
    if(!url.startsWith('https://'))return;
    try{
        const origin=new URL(url).origin;
        gvTrackProviderPortal(origin);
        if(window.GVNative&&typeof window.GVNative.prewarm==='function'){
            window.GVNative.prewarm(url);
            console.info('GV PROVIDER NATIVE PRERENDER REQUESTED',url);
        }
        for(const rel of ['dns-prefetch','preconnect']){
            const selector='link[data-gv-provider-warm="'+rel+'"][href="'+CSS.escape(origin)+'"]';
            if(!document.querySelector(selector)){
                const link=document.createElement('link');
                link.rel=rel;link.href=origin;link.dataset.gvProviderWarm=rel;
                if(rel==='preconnect')link.crossOrigin='anonymous';
                document.head.appendChild(link);
            }
        }
    }catch(error){console.warn('GV PROVIDER PREWARM SKIPPED',error)}
}

let gvFirstDestinationPreload=null;
function gvStartFirstDestinationPreload(){
    if(gvFirstDestinationPreload)return gvFirstDestinationPreload;
    const destination=activeRoute[0];
    if(!destination)return Promise.reject(new Error('GV FIRST DESTINATION MISSING'));
    const started=performance.now();
    // BUILD 0029: prepare the first HD image without warming its provider website.
    // Provider prewarming is strictly post-arrival.
    gvFirstDestinationPreload=gvPrepareDirectHd(destination).then(prepared=>{
        console.info('GV FIRST DESTINATION PREPARED',{ms:Math.round(performance.now()-started),name:destination?.name||destination?.objectName||'',resources:gvHdResourceSnapshot()});
        return {destination,prepared};
    }).catch(error=>{gvFirstDestinationPreload=null;throw error});
    return gvFirstDestinationPreload;
}
// IMPORTANT: start only after the AVM/HD preparation functions and their let/const dependencies are initialized.
const gvFirstDestinationPreloadKick=gvStartFirstDestinationPreload().catch(error=>console.error('GV FIRST DESTINATION PRELOAD FAILED',error));

// ============================================================================
// SECTION 036 — DESTINATION → ALADIN HANDOFF
// ECO: GV200-001
// ============================================================================
async function showDestination(destination,{firstTrip=false,preloadedPrepared=null,switchToSphericalAtApex=false}={}){
    gvHdTravelRetired=false;
    const v=validateDestination(destination),sourceDestination=activeDestination;
    let recordPromise=null,preparedPromise=null,presentationStarted=false,travelCardStarted=false,resolveRegisteredTravel,rejectRegisteredTravel;
    const registeredTravelPromise=new Promise((resolve,reject)=>{resolveRegisteredTravel=resolve;rejectRegisteredTravel=reject});
    const startRecordLookup=()=>{
        if(!recordPromise){
            recordPromise=gvRuntimeAvmRecord(v.destination);
            recordPromise.then(gvRegisteredTravelStateFromRecord).then(resolveRegisteredTravel,rejectRegisteredTravel);
        }
        return recordPromise;
    };
    const ensurePrepared=()=>{
        const record=startRecordLookup();
        if(!preparedPromise){
            preparedPromise=(firstTrip&&gvFirstDestinationPreload)?gvFirstDestinationPreload.then(warm=>warm?.destination===v.destination?warm.prepared:gvPrepareDirectHd(v.destination,record)):preloadedPrepared?Promise.resolve(preloadedPrepared):gvPrepareDirectHd(v.destination,record);
        }
        return preparedPromise;
    };
    const startTravelCard=()=>{
        if(travelCardStarted)return;
        travelCardStarted=true;
        if(!firstTrip){
            gvHideEarthDistance();
            destinationPresentation.depart();
        }
        travelPresentation.begin(presentationDestination,{source:sourceDestination,firstHomeTrip:firstTrip,durationSeconds:firstTrip?9:11.9});
    };
    const startTravelWork=()=>{
        if(presentationStarted)return;
        presentationStarted=true;
        gvHideEarthDistance();gvEarthPointerActive=true;gvUpdateEarthBearingPointer();
        if(firstTrip)destinationPresentation.depart();
        destinationPresentation.preview(presentationDestination,{imageUrl:String(directHdUrl(v.destination)).trim()});
        if(firstTrip)startTravelCard();
        // Provider prewarming is deferred until after 100% arrival.
        ensurePrepared();
    };
    activeDestination=v.destination;
    const presentationDestination=await gvPresentationDestination(v.destination);
    // The destination card, HD info port, and live distance display share the catalog-authoritative record.
    activeDestination=presentationDestination;
    // Build 0028: show the travel card before starting the FOV-only phase.
    // Provider/HD preparation and pointer work remain deferred until 30%.
    if(firstTrip)startTravelWork();
    else startTravelCard();
    let installed=false;
    const installWhenReady=prepared=>{
        if(!prepared?.imageObjectUrl)return Promise.reject(new Error('GV PREPARED HD OBJECT URL MISSING'));
        if(activeDestination!==presentationDestination||installed){
            gvReleaseHdObjectUrl(prepared.imageObjectUrl);
            return Promise.resolve(false);
        }
        try{
            const ready=gvInstallPreparedHd(prepared);
            installed=true;
            return ready;
        }catch(error){
            gvReleaseHdObjectUrl(prepared.imageObjectUrl);
            console.error('GV DIRECT HD INSTALL START FAILED',error);
            return Promise.reject(error);
        }
    };
    // BUILD 0011: the current galaxy HD remains visible through zoom-out,
    // translation and rotation. At zoom-in start the current HD is retired,
    // then the next galaxy HD is installed and activated.
    if(firstTrip){
        const provisional={imageCenter:[v.ra,v.dec],finalFov:v.fov,rotation:v.rotation};
        const travelPromise=gvFly130H(provisional,{firstHomeTrip:true,registeredPromise:registeredTravelPromise,onZoomInStart:()=>{ensurePrepared().then(installWhenReady).catch(error=>console.error('GV FIRST-TRIP HD PREPARE FAILED',error))}});
        await travelPromise;
        if(activeDestination!==presentationDestination)return v.destination;
        travelPresentation.end();
        destinationPresentation.arrive(presentationDestination,{imageUrl:String(directHdUrl(v.destination)).trim(),preparedImageUrl:directHdObjectUrl});
        // BUILD 0029: let the arrival presentation paint before noncritical work.
        // The identity guard prevents stale post-arrival work if another trip starts.
        requestAnimationFrame(()=>requestAnimationFrame(()=>{
            if(activeDestination!==presentationDestination)return;
            headsUpDisplay.render();
            gvShowEarthDistance(v.destination);
            gvPrewarmProviderWebsite(v.destination);
        }));
        return v.destination;
    }
    const provisional={imageCenter:[v.ra,v.dec],finalFov:v.fov,rotation:v.rotation};
    const travelPromise=gvFly130H(provisional,{firstHomeTrip:false,registeredPromise:registeredTravelPromise,switchToSphericalAtApex,onZoomOutComplete:startTravelWork,onZoomInStart:()=>{ensurePrepared().then(installWhenReady).catch(error=>console.error('GV DIRECT HD ZOOM-IN INSTALL FAILED',error))}});
    await travelPromise;
    if(activeDestination!==presentationDestination)return v.destination;
    travelPresentation.end();
    destinationPresentation.arrive(presentationDestination,{imageUrl:String(directHdUrl(v.destination)).trim(),preparedImageUrl:directHdObjectUrl});
    // BUILD 0029: let the arrival presentation paint before noncritical work.
    // The identity guard prevents stale post-arrival work if another trip starts.
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
        if(activeDestination!==presentationDestination)return;
        headsUpDisplay.render();
        gvShowEarthDistance(v.destination);
        gvPrewarmProviderWebsite(v.destination);
    }));
    return v.destination;
}
// ============================================================================
// SECTION 036A — PROVIDER SURVEY MODE
// ECO: GV200-001 BUILD 0075
// ============================================================================
function gvSurveyThumbnailCandidates(record,provider=''){
    const out=[];
    const add=value=>{const v=String(value||'').trim();if(v&&!out.includes(v))out.push(v)};
    const catalogKey=String(record?.catalogKey||'').trim();
    const catalogIndex=Number.isFinite(Number(record?.catalogIndex))?Number(record.catalogIndex):0;
    const packKey=String(provider||record?.provider||'').toUpperCase()+'|'+catalogKey+'|'+catalogIndex;
    const packed=gvSurveyThumbnailPack?.records?.[packKey];
    if(window.GVNative){
        // The immutable pack URL is the request key for shouldInterceptRequest().
        // If the lookup bridge is unavailable, fall through to the ordinary image
        // candidates rather than producing an empty selector.
        if(packed?.path){
            const packedPath=String(packed.path); const localPrefix='viewer/artwork/runtime/survey-thumbnails/'; const localPath=packedPath.startsWith(localPrefix)?'survey-thumbnails/'+packedPath.slice(localPrefix.length):packedPath;
            add(gvSurveyThumbnailPack.nativeBaseUrl+localPath);
            return Object.freeze(out);
        }
        console.error('GV SURVEY THUMBNAIL LOOKUP MISS',packKey);
    }
    if(packed?.path)add(gvSurveyThumbnailPack.baseUrl+packed.path);
    const base=String(record?.imageUrl||record?.githubImageUrl||record?.hdUrl||'').trim();
    if(base){
        try{
            const u=new URL(base,location.href),host=u.hostname.toLowerCase(),path=u.pathname;
            if((host==='cdn.esawebb.org'||host==='cdn.esahubble.org')&&path.includes('/archives/images/screen/'))add(base.replace('/archives/images/screen/','/archives/images/thumb300y/'));
            if((host==='www.eso.org'||host==='cdn.eso.org')&&path.includes('/public/archives/images/screen/'))add(base.replace('/public/archives/images/screen/','/public/archives/images/thumb300y/'));
            if(host==='storage.noirlab.edu'&&path.includes('/media/archives/images/screen/'))add(base.replace('/media/archives/images/screen/','/media/archives/images/thumb300y/'));
        }catch(_){}
    }
    add(base);add(record?.githubImageUrl);add(record?.hdUrl);
    return Object.freeze(out);
}
async function gvSelectSurveyProvider(provider){
    if(navigationInFlight)return false;
    const key=String(provider||'').toUpperCase();
    await gvSurveyThumbnailPackReady;
    const records=gvSurveyCatalog.get(key);
    if(!records?.length)return false;
    const remembered=gvSurveyCursors.get(key);
    const resumeIndex=Number.isInteger(remembered)&&remembered>=0&&remembered<records.length?remembered:0;
    const items=Object.freeze(records.map(record=>Object.freeze({
        name:String(record?.commonName||record?.name||record?.designation||'').trim(),
        designation:String(record?.designation||record?.name||'').trim(),
        constellation:String(record?.constellation||'').trim(),
        imageType:String(record?.imageType||'').trim(),
        thumbnails:gvSurveyThumbnailCandidates(record,key)
    })));
    gvSurveyMode={provider:key,providerIcon:GV_SURVEY_PROVIDER_META[key]?.icon||'',records,items,index:-1,pendingIndex:resumeIndex};
    target.close?.();
    gvSyncSurveySelectButton();
    history.length=0;historyIndex=-1;
    target.setActiveProvider(key,{index:resumeIndex+1,total:records.length});
    galaxyNavigator.setSurvey?.({provider:key,providerIcon:gvSurveyMode.providerIcon,current:resumeIndex+1,total:records.length,items,displaying:false});
    updateNavigationAvailability();
    requestAnimationFrame(()=>{gvSyncSurveySelectButton();galaxyNavigator.openSurveySelector?.(gvSurveySelectGroup)});
    return true;
}
function gvExitSurveyMode(){
    if(navigationInFlight)return false;
    gvSurveyMode=null;
    history.length=0;historyIndex=-1;
    target.setActiveProvider('',{index:0,total:0});
    galaxyNavigator.clearSurvey?.();
    headsUpDisplay?.render?.();
    gvSyncSurveySelectButton();
    updateNavigationAvailability();
    return true;
}

async function gvNavigateSearchResult(destination){
    if(navigationInFlight||!destination)return false;
    gvCancelProviderAll();
    document.getElementById('gv-universe-context')?.remove();
    document.getElementById('gv-we-are-here')?.remove();
    navigationInFlight=true;
    gvSetTripCycle(true);
    galaxyNavigator.setBusy(true);
    galaxyNavigator.setTraveling?.(true);
    updateNavigationAvailability();
    try{
        const prepared={...destination,providerKey:gvSurveyProviderKey(destination),provider:gvSurveyProviderKey(destination),fovDegrees:Number(destination?.fovXDegrees??destination?.fovDegrees),aladinRotation:Number(destination?.aladinRotation??destination?.spatialRotationDeg)};
        if(target?.open)target.close?.();
        galaxyNavigator.closeSurveySelector?.();
        gvSearchInput.value='';gvSearchRender('');
        gvExitSurveyMode();
        if(historyIndex<history.length-1)history.splice(historyIndex+1);
        history.push(prepared);historyIndex=history.length-1;
        const firstTrip=routeIndex===0;
        const switchToSphericalAtApex=routeIndex===1;
        routeIndex++;
        await showDestination(prepared,{firstTrip,switchToSphericalAtApex});
        requestAnimationFrame(gvSyncSurveySelectButton);
        return true;
    }finally{
        navigationInFlight=false;
        gvSetTripCycle(false);
        galaxyNavigator.setTraveling?.(false);
        galaxyNavigator.setBusy(false);
        updateNavigationAvailability();
        requestAnimationFrame(gvSyncSurveySelectButton);
    }
}

async function gvNavigateSurveyIndex(nextIndex){
    if(navigationInFlight||!gvSurveyMode)return false;
    const index=Number(nextIndex);
    if(!Number.isInteger(index)||index<0||index>=gvSurveyMode.records.length)return false;
    if(index===gvSurveyMode.index)return true;
    const previousIndex=gvSurveyMode.index;
    const previousPendingIndex=Number.isInteger(gvSurveyMode.pendingIndex)?gvSurveyMode.pendingIndex:Math.max(0,previousIndex);
    const destination=gvSurveyMode.records[index];
    gvCancelProviderAll();
    document.getElementById('gv-universe-context')?.remove();
    document.getElementById('gv-we-are-here')?.remove();
    navigationInFlight=true;
    gvSurveyMode.pendingIndex=index;
    gvSyncSurveySelectButton();
    gvSetTripCycle(true);
    galaxyNavigator.setBusy(true);
    target.setActiveProvider(gvSurveyMode.provider,{index:index+1,total:gvSurveyMode.records.length});
    galaxyNavigator.setSurvey?.({provider:gvSurveyMode.provider,providerIcon:gvSurveyMode.providerIcon,current:index+1,total:gvSurveyMode.records.length,items:gvSurveyMode.items,displaying:false});
    galaxyNavigator.setTraveling?.(true);
    updateNavigationAvailability();
    try{
        const firstTrip=routeIndex===0;
        const switchToSphericalAtApex=routeIndex===1;
        routeIndex++;
        await showDestination(destination,{firstTrip,switchToSphericalAtApex});
        gvSurveyMode.index=index;
        gvSurveyMode.pendingIndex=index;
        gvSurveyCursors.set(gvSurveyMode.provider,index);
        target.setActiveProvider(gvSurveyMode.provider,{index:index+1,total:gvSurveyMode.records.length});
        galaxyNavigator.setSurvey?.({provider:gvSurveyMode.provider,providerIcon:gvSurveyMode.providerIcon,current:index+1,total:gvSurveyMode.records.length,items:gvSurveyMode.items,displaying:true});
        requestAnimationFrame(()=>{gvSyncSurveySelectButton();setTimeout(gvSyncSurveySelectButton,180)});
        return true;
    }catch(error){
        gvSurveyMode.index=previousIndex;
        gvSurveyMode.pendingIndex=previousPendingIndex;
        const restoreIndex=previousIndex>=0?previousIndex:previousPendingIndex;
        target.setActiveProvider(gvSurveyMode.provider,{index:restoreIndex+1,total:gvSurveyMode.records.length});
        galaxyNavigator.setSurvey?.({provider:gvSurveyMode.provider,providerIcon:gvSurveyMode.providerIcon,current:restoreIndex+1,total:gvSurveyMode.records.length,items:gvSurveyMode.items,displaying:previousIndex>=0});
        throw error;
    }finally{
        navigationInFlight=false;
        gvSyncSurveySelectButton();
        gvSetTripCycle(false);
        galaxyNavigator.setTraveling?.(false);
        galaxyNavigator.setBusy(false);
        updateNavigationAvailability();
    }
}


// ============================================================================
// SECTION 037 — RANDOM GALAXY ACTION
// ECO: GV200-001
// ============================================================================
async function navigateRandom(){
    if(gvSurveyMode){
        if(navigationInFlight)return;
        if(gvSurveyMode.index<0)return gvNavigateSurveyIndex(Number.isInteger(gvSurveyMode.pendingIndex)?gvSurveyMode.pendingIndex:0);
        if(gvSurveyMode.index>=gvSurveyMode.records.length-1)return;
        return gvNavigateSurveyIndex(gvSurveyMode.index+1);
    }
    if(navigationInFlight)return;
    gvCancelProviderAll();
    document.getElementById('gv-universe-context')?.remove();
    document.getElementById('gv-we-are-here')?.remove();
    navigationInFlight=true;
    gvSetTripCycle(true);
    galaxyNavigator.setBusy(true);
    galaxyNavigator.setTraveling?.(true);
    updateNavigationAvailability();
    try{
        const destination=await navigationRuntime.nextDestination();
        let preloadedPrepared=null;
        if(routeIndex===0&&gvFirstDestinationPreload){
            gvFirstDestinationPreload.then(warm=>{if(warm?.destination===destination)console.info('GV FIRST DESTINATION PRELOAD READY FOR ACTIVE TRIP')}).catch(error=>console.error('GV FIRST DESTINATION PRELOAD UNAVAILABLE',error));
        }
        if(historyIndex<history.length-1)history.splice(historyIndex+1);
        history.push(destination);
        historyIndex=history.length-1;
        const firstTrip=routeIndex===0;
        const switchToSphericalAtApex=routeIndex===1;
        routeIndex++;
        await showDestination(destination,{firstTrip,preloadedPrepared,switchToSphericalAtApex});
    }finally{
        navigationInFlight=false;
        gvSetTripCycle(false);
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
    if(gvSurveyMode){
        if(navigationInFlight||gvSurveyMode.index<=0)return;
        return gvNavigateSurveyIndex(gvSurveyMode.index-1);
    }
    if(navigationInFlight||historyIndex<=0)return;
    gvCancelProviderAll();
    navigationInFlight=true;gvSetTripCycle(true);galaxyNavigator.setBusy(true);galaxyNavigator.setTraveling?.(true);historyIndex--;updateNavigationAvailability();
    try{await showDestination(history[historyIndex])}finally{navigationInFlight=false;gvSetTripCycle(false);galaxyNavigator.setTraveling?.(false);galaxyNavigator.setBusy(false);updateNavigationAvailability()}
}


// ============================================================================
// SECTION 039 — FORWARD ACTION
// ECO: GV200-001
// ============================================================================
async function navigateForward(){
    if(gvSurveyMode){
        if(navigationInFlight||gvSurveyMode.index>=gvSurveyMode.records.length-1)return;
        return gvNavigateSurveyIndex(gvSurveyMode.index+1);
    }
    if(navigationInFlight||historyIndex>=history.length-1)return;
    gvCancelProviderAll();
    navigationInFlight=true;gvSetTripCycle(true);galaxyNavigator.setBusy(true);galaxyNavigator.setTraveling?.(true);historyIndex++;updateNavigationAvailability();
    try{await showDestination(history[historyIndex])}finally{navigationInFlight=false;gvSetTripCycle(false);galaxyNavigator.setTraveling?.(false);galaxyNavigator.setBusy(false);updateNavigationAvailability()}
}

function updateNavigationAvailability(){
    if(gvSurveyMode){
        if(gvSurveyMode.index<0){
            galaxyNavigator.setEnabled({back:false,random:true,forward:false});
            return;
        }
        const hasNext=gvSurveyMode.index<gvSurveyMode.records.length-1;
        galaxyNavigator.setEnabled({
            back:gvSurveyMode.index>0,
            random:hasNext,
            forward:hasNext
        });
        return;
    }
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
    get surveyProvider(){return gvSurveyMode?.provider||''},
    get surveyIndex(){return Number.isInteger(gvSurveyMode?.index)?gvSurveyMode.index:-1},
    get surveyPendingIndex(){return Number.isInteger(gvSurveyMode?.pendingIndex)?gvSurveyMode.pendingIndex:-1},
    get surveyLength(){return gvSurveyMode?.records?.length||0},
    get surveyCursors(){return Object.freeze(Object.fromEntries([...gvSurveyCursors].map(([provider,index])=>[provider,index+1])))},
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