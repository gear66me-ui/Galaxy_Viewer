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
GALAXY_ROUTE_ENGINE_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-001.js?v=0027"
GALAXY_NAVIGATOR_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js?v=0027"
AVM_OVERLAY_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/lab/gv-avm-overlay-lab-0055.js"
HEADS_UP_DISPLAY_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hud/gv-heads-up-display-0001.js"

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
#gv-navigation-host{position:absolute;left:50%;bottom:12px;z-index:7300;display:flex;gap:5px;width:min(430px,calc(100vw - 20px));transform:translateX(-50%);pointer-events:auto}
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
const VERSION='GV-beta-200-001';
const GV200001_BUILD='0032';
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
    galaxyRouteEngineUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-001.js?v=0027',
    galaxyNavigatorUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js?v=0027',
    avmOverlayUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/lab/gv-avm-overlay-lab-0055.js',
    headsUpDisplayUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hud/gv-heads-up-display-0001.js'
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
    'diagnosticsUrl','galaxyRouteEngineUrl','galaxyNavigatorUrl','avmOverlayUrl','headsUpDisplayUrl'
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

const GV_SPACE_AGE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf';
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
    style.id='gv200001-universe-context-style';
    style.textContent=`
#gv-universe-context{position:absolute;left:50%;top:auto;bottom:calc(50% + min(25vw,50dvh) + 67px);z-index:7095;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;width:min(240px,66vw);pointer-events:none;transition:opacity .2s ease;font-family:"GV Space Age",sans-serif}
#gv-universe-context .gv-universe-label{padding:8px 10px 9px;border:1px solid rgba(124,203,255,.78);border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.94),rgba(11,49,119,.88),rgba(41,109,189,.78)) padding-box,linear-gradient(135deg,#DDF8FF,#58BFFF,#296DBD) border-box;box-shadow:inset 0 0 7px rgba(221,248,255,.09),0 0 8px rgba(88,191,255,.24);color:#DDF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 6px rgba(88,191,255,.42);font:400 9px/1.35 "GV Space Age",sans-serif;letter-spacing:.65px}
#gv-universe-context .gv-universe-count{display:block;margin-top:2px;color:#7CCBFF;font-size:10px;letter-spacing:.8px}
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
const RETICLE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-reticle.svg';

function createCenterReticle(root){
    const COSMIC_BLUE='#58BFFF';
    const NORTH_RED='#FF3B3B';
    const SIZE=270;
    const CENTER=SIZE/2;
    const NORTH_POINTER_RADIUS=131;
    const NORTH_LABEL_RADIUS=152;

    const reticle=document.createElement('div');
    reticle.id='gv-center-reticle';
    reticle.setAttribute('aria-hidden','true');

    // Restore the original simplified icy-blue center reticle presentation.
    const centerTarget=document.createElement('img');
    centerTarget.id='gv-center-target';
    centerTarget.src=RETICLE_URL;
    centerTarget.alt='';
    centerTarget.width=32;
    centerTarget.height=32;
    Object.assign(centerTarget.style,{
        position:'absolute',left:'50%',top:'50%',
        transform:'translate(-50%,-50%)'
    });
    reticle.appendChild(centerTarget);

    // Keep only the live North compass authority around the simplified reticle.
    // No direction ring, cardinal crosshair, or graduated tick grid.
    const northRotor=document.createElement('div');
    northRotor.id='gv-north-rotor';
    Object.assign(northRotor.style,{
        position:'absolute',left:'0',top:'0',width:`${SIZE}px`,height:`${SIZE}px`,
        transform:'rotate(0deg)',transformOrigin:`${CENTER}px ${CENTER}px`,
        pointerEvents:'none',willChange:'transform'
    });
    reticle.appendChild(northRotor);

    const northPointer=document.createElement('div');
    northPointer.id='gv-north-pointer';
    Object.assign(northPointer.style,{
        position:'absolute',
        left:`${CENTER}px`,
        top:`${CENTER-NORTH_POINTER_RADIUS}px`,
        width:'10px',
        height:'12px',
        background:NORTH_RED,
        clipPath:'polygon(50% 0,100% 100%,0 100%)',
        transform:'translate(-50%,-50%) rotate(0deg)',
        filter:'drop-shadow(0 0 3px rgba(255,59,59,.95)) drop-shadow(0 0 7px rgba(255,59,59,.48))',
        display:'block'
    });
    northRotor.appendChild(northPointer);

    const northLabel=document.createElement('div');
    northLabel.id='gv-north-label';
    northLabel.textContent='N';
    Object.assign(northLabel.style,{
        position:'absolute',
        display:'block',
        left:`${CENTER}px`,
        top:`${CENTER-NORTH_LABEL_RADIUS}px`,
        transform:'translate(-50%,-50%) rotate(0deg)',
        color:NORTH_RED,
        font:'700 15px/1 Arial,sans-serif',
        letterSpacing:'0px',
        textShadow:'0 0 3px rgba(221,248,255,.92),0 0 7px rgba(88,191,255,.72)',
        whiteSpace:'nowrap',
        textAlign:'center'
    });
    northRotor.appendChild(northLabel);

    reticle.gvDirectional={
        center:CENTER,
        northRotor,
        northPointerRadius:NORTH_POINTER_RADIUS,
        northLabelRadius:NORTH_LABEL_RADIUS,
        northPointer,
        northLabel,
        lastNorthBearing:null
    };

    root.appendChild(reticle);
    return reticle;
}

function readCelestialNorthBearing(aladin,root){
    try{
        const liveRotation=Number(aladin.getRotation?.());
        if(Number.isFinite(liveRotation)){
            return ((liveRotation%360)+360)%360;
        }
    }catch(error){
        console.warn('GALAXY VIEWER NORTH ROTATION WARNING',error);
    }
    return 0;
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
    state.northPointer.dataset.northBearing=northBearing.toFixed(3);
    state.northLabel.dataset.northBearing=northBearing.toFixed(3);
    state.northPointer.style.display='block';
    state.northLabel.style.display='block';
}

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
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:75%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(124,203,255,.88);border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.94),rgba(11,49,119,.88),rgba(41,109,189,.78));color:#EAF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(88,191,255,.58);box-shadow:0 0 10px rgba(88,191,255,.24)}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#7CCBFF;font:400 15px/1.2 "GV Space Age",sans-serif;letter-spacing:1.25px}
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
        '<div class="gv-home-hint">TAP RANDOM GALAXY TO BEGIN</div>'+
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
    loadScript(fresh(config.avmOverlayUrl)),
    loadScript(fresh(config.headsUpDisplayUrl))
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
if(window.GalaxyViewerHeadsUpDisplay?.VERSION!=='0001'||typeof window.GalaxyViewerHeadsUpDisplay.mount!=='function')throw new Error('HEADS-UP DISPLAY 0001 EXPORT MISSING');
for(let i=0;i<100&&!window.GalaxyViewerAvmOverlayLab;i++)await new Promise(resolve=>setTimeout(resolve,50));

if(!window.GalaxyViewerAvmOverlayLab?.install)throw new Error('AVM OVERLAY 0055 EXPORT MISSING');

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
galaxyNavigator.setBusy(false);
galaxyNavigator.setEnabled({back:false,random:true,forward:false});


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
let activeDestination=null;
const randomGalaxyBridge=Object.freeze({
    get activeDestination(){return activeDestination},
    get currentDestination(){return activeDestination},
    getState(){return {activeDestination,currentDestination:activeDestination}}
});
window.GalaxyRandomGalaxy=randomGalaxyBridge;
const headsUpDisplay=window.GalaxyViewerHeadsUpDisplay.mount(document.getElementById('aladin-cosmic-command-test'),{
    routeEngine:navigationRuntime,
    randomGalaxy:randomGalaxyBridge
});
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
    headsUpDisplay.render();
    return v.destination;
}


// ============================================================================
// SECTION 037 — RANDOM GALAXY ACTION
// ECO: GV200-001
// ============================================================================
async function navigateRandom(){
    document.getElementById('gv-universe-context')?.remove();
    document.getElementById('gv-we-are-here')?.remove();
    galaxyNavigator.setBusy(true);
    try{
        const destination=await navigationRuntime.nextDestination();
        if(historyIndex<history.length-1)history.splice(historyIndex+1);
        history.push(destination);
        historyIndex=history.length-1;
        routeIndex++;
        showDestination(destination);
    }finally{
        galaxyNavigator.setBusy(false);
        updateNavigationAvailability();
    }
}


// ============================================================================
// SECTION 038 — BACK ACTION
// ECO: GV200-001
// ============================================================================
function navigateBack(){
    if(historyIndex<=0)return;
    historyIndex--;
    showDestination(history[historyIndex]);
    updateNavigationAvailability();
}


// ============================================================================
// SECTION 039 — FORWARD ACTION
// ECO: GV200-001
// ============================================================================
function navigateForward(){
    if(historyIndex>=history.length-1)return;
    historyIndex++;
    showDestination(history[historyIndex]);
    updateNavigationAvailability();
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
