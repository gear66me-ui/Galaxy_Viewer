from IPython.display import HTML, Javascript, display
import json

# ============================================================================
# SECTION 001 — FILE IDENTITY / PYTHON IMPORTS
# ECO: GV200-001
# ============================================================================
VIEWER_VERSION = "GV-beta-200-001"

# ============================================================================
# SECTION 002 — ALADIN MIRROR POINTERS
# ECO: GV200-001
# ============================================================================
ALADIN_VERSION = "3.8.2"
ALADIN_CSS_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css"
ALADIN_JS_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/dist/aladin.js"

# ============================================================================
# SECTION 003 — GALAXY VIEWER MODULE POINTERS
# ECO: GV200-001
# ============================================================================
HAMBURGER_BASE_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js"
HAMBURGER_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js"
COORDINATE_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js"
TARGET_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/target-simbad/gv-target-simbad-0004.js"
DIAGNOSTICS_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0019.js"
GALAXY_ROUTE_ENGINE_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-001.js"
GALAXY_NAVIGATOR_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js"
AVM_OVERLAY_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/lab/gv-avm-overlay-lab-0055.js"

# ============================================================================
# SECTION 004 — HTML APPLICATION ROOT
# ECO: GV200-001
# ============================================================================
display(HTML("""
<link rel="stylesheet" href="https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css" />
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
#aladin-cosmic-command-test{position:relative;width:100%;height:100vh;overflow:hidden;background:#000}
</style>

<!-- =======================================================================
     SECTION 007 — MODULE HOST LAYOUT
     ECO: GV200-001
     ======================================================================= -->
<style>
#gv-hamburger-host{position:absolute;inset:0;z-index:7200;pointer-events:none}
#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;pointer-events:auto}
#gv-target-host{position:absolute;left:342px;top:12px;z-index:7210;width:36px;height:36px;pointer-events:auto}
#gv-navigation-host{position:absolute;left:50%;bottom:12px;z-index:7300;display:flex;gap:5px;transform:translateX(-50%);pointer-events:auto}
#gv-navigation-host button{height:36px;padding:0 10px;border:1px solid #7CCBFF;border-radius:6px;background:#0B3177;color:#DDF8FF;font:11px sans-serif}
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
const VERSION='GV-beta-200-001';
const GV200001_BUILD='0006';
const fresh=url=>`${url}?v=GV200001-${GV200001_BUILD}`;
window.GV_BOOT_CONFIG=Object.freeze({
    viewerVersion:'GV-beta-200-001',
    aladinVersion:'3.8.2',
    aladinCssUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css',
    aladinJsUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/dist/aladin.js',
    hamburgerBaseUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js',
    hamburgerUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js',
    coordinateUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js',
    targetUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/target-simbad/gv-target-simbad-0004.js',
    diagnosticsUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0019.js',
    galaxyRouteEngineUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-001.js',
    galaxyNavigatorUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js',
    avmOverlayUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/lab/gv-avm-overlay-lab-0055.js'
});


// ============================================================================
// SECTION 009 — SCRIPT LOADER
// ECO: GV200-001
// ============================================================================
function loadScript(url){
    return new Promise((resolve,reject)=>{
        const requested=new URL(url,window.location.href).href;
        const existing=[...document.scripts].find(s=>new URL(s.src||'',window.location.href).href===requested);
        if(existing){
            if(existing.dataset.gvReady==='1')return resolve(existing);
            existing.addEventListener('load',()=>resolve(existing),{once:true});
            existing.addEventListener('error',()=>reject(new Error(`SCRIPT LOAD FAILED: ${url}`)),{once:true});
            return;
        }
        const script=document.createElement('script');
        script.src=url;
        script.async=true;
        script.addEventListener('load',()=>{script.dataset.gvReady='1';resolve(script)},{once:true});
        script.addEventListener('error',()=>reject(new Error(`SCRIPT LOAD FAILED: ${url}`)),{once:true});
        document.head.appendChild(script);
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
    'diagnosticsUrl','galaxyRouteEngineUrl','galaxyNavigatorUrl','avmOverlayUrl'
]){
    if(!config?.[key])throw new Error(`BOOT CONFIG MISSING: ${key}`);
}


// ============================================================================
// SECTION 013 — ALADIN JAVASCRIPT LOAD
// ECO: GV200-001
// ============================================================================
const aladinModule=await import(config.aladinJsUrl);
const A=aladinModule.default;
if(!A?.init)throw new Error('ALADIN MIRROR DEFAULT EXPORT MISSING: A.init');
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


// ============================================================================
// SECTION 018 — GALAXY VIEWER MODULE LOAD
// ECO: GV200-001
// ============================================================================
await loadScript(fresh(config.hamburgerBaseUrl));
await loadScript(fresh(config.hamburgerUrl));
await Promise.all([
    loadScript(fresh(config.coordinateUrl)),
    loadScript(fresh(config.targetUrl)),
    loadScript(fresh(config.diagnosticsUrl)),
    loadScript(fresh(config.galaxyRouteEngineUrl)),
    loadScript(fresh(config.galaxyNavigatorUrl)),
    loadScript(fresh(config.avmOverlayUrl))
]);


// ============================================================================
// SECTION 019 — REQUIRED MODULE EXPORT VALIDATION
// ECO: GV200-001
// ============================================================================
if(window.GalaxyViewerHamburgerMenu?.version!=='0007')throw new Error('HAMBURGER 0007 EXPORT MISSING');
if(window.GalaxyCoordinateOverlay?.VERSION!=='0006')throw new Error('COORDINATE 0006 EXPORT MISSING');
if(window.GalaxyViewerTargetSimbad?.version!=='0004')throw new Error('TARGET 0004 EXPORT MISSING');
if(window.GalaxyViewerDiagnostics?.VERSION!=='0019')throw new Error('DIAGNOSTICS 0019 EXPORT MISSING');
if(window.GalaxyRouteEngine?.VERSION!=='0001')throw new Error('GALAXY ROUTE ENGINE 001 EXPORT MISSING');
if(window.GalaxyNavigator?.VERSION!=='001'||typeof window.GalaxyNavigator.mount!=='function')throw new Error('GALAXY NAVIGATOR 001 EXPORT MISSING');
for(let i=0;i<100&&!window.GalaxyViewerAvmOverlayLab;i++)await new Promise(resolve=>setTimeout(resolve,50));
if(!window.GalaxyViewerAvmOverlayLab?.install)throw new Error('AVM OVERLAY 0055 EXPORT MISSING');


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
const hamburger=window.GalaxyViewerHamburgerMenu.init({
    host:hosts.hamburger,
    onMenuAction(action){
        if(action==='DIAGNOSTICS')window.GalaxyViewerDiagnostics?.open?.();
        if(action==='SURVEY'&&typeof aladin.setBaseImageLayer==='function'){
            aladin.setBaseImageLayer('https://alaskybis.unistra.fr/DSS/DSSColor');
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
const coordinate=window.GalaxyCoordinateOverlay.mount(hosts.coordinate,{});
await coordinate.ready;
coordinate.setFrame('ICRSd');
coordinate.update(HOME.ra,HOME.dec);


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
const diagnostics=window.GalaxyViewerDiagnostics;


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
hosts.navigation.replaceChildren();


// ============================================================================
// SECTION 032 — NAVIGATION CONTROL REFERENCES
// ECO: GV200-001
// ============================================================================
// Galaxy Navigator controls intentionally not mounted during UI rebuild.


// ============================================================================
// SECTION 033 — TEST HISTORY STATE
// ECO: GV200-001
// ============================================================================
const history=[];
let historyIndex=-1;
let routeIndex=0;
let activeDestination=null;
const randomGalaxyBridge=Object.freeze({
    get activeDestination(){return activeDestination},
    get currentDestination(){return activeDestination},
    getState(){return {activeDestination,currentDestination:activeDestination}}
});
window.GalaxyRandomGalaxy=randomGalaxyBridge;
const avmOverlay=window.GalaxyViewerAvmOverlayLab.install({
    A,
    aladin,
    viewerRoot:document.getElementById('aladin-cosmic-command-test'),
    randomGalaxy:randomGalaxyBridge
});


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
    if(!Number.isFinite(ra))throw new Error('DESTINATION RA INVALID');
    if(!Number.isFinite(dec))throw new Error('DESTINATION DEC INVALID');
    if(!Number.isFinite(fov)||fov<=0)throw new Error('DESTINATION FOV INVALID');
    return Object.freeze({destination,ra,dec,fov});
}


// ============================================================================
// SECTION 036 — DESTINATION → ALADIN HANDOFF
// ECO: GV200-001
// ============================================================================
function showDestination(destination){
    const v=validateDestination(destination);
    activeDestination=v.destination;
    aladin.gotoRaDec(v.ra,v.dec);
    aladin.setFov(v.fov);
    coordinate.update(v.ra,v.dec);
    window.GalaxyViewerAvmOverlayLab?.loadForBestDestination?.('gv200-001-navigation-arrival');
    return v.destination;
}


// ============================================================================
// SECTION 037 — RANDOM GALAXY ACTION
// ECO: GV200-001
// ============================================================================
// Control action intentionally dormant until the new Galaxy Navigator tile is mounted.


// ============================================================================
// SECTION 038 — BACK ACTION
// ECO: GV200-001
// ============================================================================
// Control action intentionally dormant until the new Galaxy Navigator tile is mounted.


// ============================================================================
// SECTION 039 — FORWARD ACTION
// ECO: GV200-001
// ============================================================================
// Control action intentionally dormant until the new Galaxy Navigator tile is mounted.


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
    navigationRuntime,
    get routeIndex(){return routeIndex},
    get historyIndex(){return historyIndex},
    get historyLength(){return history.length},
    get navigationState(){return navigationRuntime.snapshot()}
});

console.info(`${VERSION} — TRIAL READY`,{
    routeLength:activeRoute.length,
    navigation:navigationRuntime.snapshot()
});
})().catch(error=>{
    console.error('GV200-001 BOOT FAILURE',error);
});
"""))
