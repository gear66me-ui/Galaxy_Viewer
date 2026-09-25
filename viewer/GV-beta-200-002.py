from IPython.display import HTML, Javascript, display
import json

# ============================================================================
# SECTION 001 — FILE IDENTITY / PYTHON IMPORTS
# ECO: GV200-001
# ============================================================================
VIEWER_VERSION = "GV-beta-200-002"

# ============================================================================
# SECTION 002 — ALADIN MIRROR POINTERS
# ECO: GV200-001
# ============================================================================
ALADIN_VERSION = "3.8.2"
ALADIN_CSS_URL = "https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css"
ALADIN_JS_URL = "https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js"

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
const VERSION='GV-beta-200-002';
const GV200001_BUILD='0004';
const GV_RUNTIME='0072';
const fresh=url=>`${url}?v=GV200001-${GV200001_BUILD}`;
window.GV_BOOT_CONFIG=Object.freeze({
    viewerVersion:'GV-beta-200-002',
    aladinVersion:'3.8.2',
    aladinCssUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css',
    aladinJsUrl:'https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js',
    hamburgerBaseUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js',
    hamburgerUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js',
    coordinateUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js',
    targetUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/target-simbad/gv-target-simbad-0004.js',
    diagnosticsUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0019.js',
    galaxyRouteEngineUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-001.js?v=0027',
    galaxyNavigatorUrl:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js?v=0027',
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
    'diagnosticsUrl','galaxyRouteEngineUrl','galaxyNavigatorUrl','headsUpDisplayUrl'
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
    style.id='gv200001-universe-context-style';    style.textContent=`
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
    const COSMIC_BLUE_SOFT='rgba(88,191,255,.64)';
    const NORTH_RED='#FF3B3B';
    const SIZE=270;
    const CENTER=SIZE/2;
    const RING_RADIUS=125;
    const NORTH_POINTER_RADIUS=RING_RADIUS+6;
    const NORTH_LABEL_RADIUS=RING_RADIUS+27;

    const reticle=document.createElement('div');
    reticle.id='gv-center-reticle';
    reticle.setAttribute('aria-hidden','true');

    const northRotor=document.createElement('div');
    northRotor.id='gv-north-rotor';
    Object.assign(northRotor.style,{
        position:'absolute',left:'0',top:'0',width:`${SIZE}px`,height:`${SIZE}px`,
        transform:'rotate(0deg)',transformOrigin:`${CENTER}px ${CENTER}px`,
        pointerEvents:'none',willChange:'transform'
    });
    reticle.appendChild(northRotor);

    const northGrid=document.createElement('div');
    northGrid.id='gv-north-grid';
    Object.assign(northGrid.style,{position:'absolute',left:'0',top:'0',width:`${SIZE}px`,height:`${SIZE}px`,pointerEvents:'none'});
    northRotor.appendChild(northGrid);

    const ring=document.createElement('div');
    ring.id='gv-direction-ring';
    Object.assign(ring.style,{
        position:'absolute',left:'50%',top:'50%',width:`${RING_RADIUS*2}px`,height:`${RING_RADIUS*2}px`,
        transform:'translate(-50%,-50%)',border:`0.7px solid ${COSMIC_BLUE_SOFT}`,borderRadius:'50%',
        boxShadow:'0 0 4px rgba(88,191,255,.20), inset 0 0 3px rgba(88,191,255,.08)',boxSizing:'border-box'
    });
    northGrid.appendChild(ring);

    const crosshair=document.createElement('div');
    crosshair.id='gv-cardinal-crosshair';
    Object.assign(crosshair.style,{position:'absolute',inset:'0',pointerEvents:'none'});
    for(const angle of [0,90,180,270]){
        const line=document.createElement('div');
        Object.assign(line.style,{
            position:'absolute',left:`${CENTER}px`,top:`${CENTER}px`,width:'0.5px',height:'27px',
            background:NORTH_RED,boxShadow:'0 0 1px rgba(255,59,59,.22)',
            transform:`translate(-50%,-100%) rotate(${angle}deg) translateY(-57.5px)`,transformOrigin:'50% 100%'
        });
        crosshair.appendChild(line);
    }
    northGrid.appendChild(crosshair);

    const centerTarget=document.createElement('img');
    centerTarget.id='gv-center-target';
    centerTarget.src=RETICLE_URL;
    centerTarget.alt='';
    centerTarget.width=32;
    centerTarget.height=32;
    Object.assign(centerTarget.style,{position:'absolute',left:'50%',top:'50%',transform:'translate(-50%,-50%)'});
    reticle.appendChild(centerTarget);

    for(let angle=0;angle<360;angle+=30){
        const major=angle%90===0;
        const length=major?13:7;
        const radians=angle*Math.PI/180;
        const radius=RING_RADIUS-length/2;
        const tick=document.createElement('div');
        tick.className=major?'gv-reticle-tick gv-reticle-tick-major':'gv-reticle-tick gv-reticle-tick-minor';
        Object.assign(tick.style,{
            position:'absolute',left:`${CENTER+Math.sin(radians)*radius}px`,top:`${CENTER-Math.cos(radians)*radius}px`,
            width:major?'1.35px':'0.55px',height:major?'16px':`${length}px`,
            transform:`translate(-50%,-50%) rotate(${angle}deg)`,transformOrigin:'50% 50%',
            background:major?NORTH_RED:COSMIC_BLUE,
            boxShadow:major?'0 0 3px rgba(255,59,59,.70),0 0 6px rgba(255,59,59,.24)':'0 0 2px rgba(88,191,255,.30)',
            borderRadius:major?'0':'1px'
        });
        northGrid.appendChild(tick);
    }

    const northPointer=document.createElement('div');
    northPointer.id='gv-north-pointer';
    Object.assign(northPointer.style,{
        position:'absolute',left:`${CENTER}px`,top:`${CENTER-NORTH_POINTER_RADIUS}px`,width:'10px',height:'12px',
        background:NORTH_RED,clipPath:'polygon(50% 0,100% 100%,0 100%)',
        transform:'translate(-50%,-50%) rotate(0deg)',
        filter:'drop-shadow(0 0 3px rgba(255,59,59,.95)) drop-shadow(0 0 7px rgba(255,59,59,.48))',display:'block'
    });
    northRotor.appendChild(northPointer);

    const northLabel=document.createElement('div');
    northLabel.id='gv-north-label';
    northLabel.textContent='N';
    Object.assign(northLabel.style,{
        position:'absolute',display:'block',left:`${CENTER}px`,top:`${CENTER-NORTH_LABEL_RADIUS}px`,
        transform:'translate(-50%,-50%) rotate(0deg)',color:NORTH_RED,font:'700 15px/1 Arial,sans-serif',
        letterSpacing:'0px',textShadow:'0 0 3px rgba(221,248,255,.92),0 0 7px rgba(88,191,255,.72)',
        whiteSpace:'nowrap',textAlign:'center'
    });
    northRotor.appendChild(northLabel);

    reticle.gvDirectional={center:CENTER,northRotor,northGrid,ring,northPointerRadius:NORTH_POINTER_RADIUS,northLabelRadius:NORTH_LABEL_RADIUS,northPointer,northLabel,lastNorthBearing:null};
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
gvVersionReadout.textContent='200-002   BLD 0004   RT 0072';
Object.assign(gvVersionReadout.style,{display:'block',width:'100%',font:'9px/1.2 monospace',letterSpacing:'.3px',color:'#9edcff',textAlign:'center',margin:'0 0 3px',padding:'0',border:'0',background:'transparent',boxShadow:'none',pointerEvents:'none'});
earlyNavigationHost.insertBefore(gvVersionReadout,earlyNavigationHost.firstChild);


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
const GV_MASTER_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
const GV_AVM_RUNTIME_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0001.json';
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
    return {
        NAXIS:2,CTYPE1:'RA---TAN',CTYPE2:'DEC--TAN',EQUINOX:2000,LONPOLE:180,LATPOLE:dec,CUNIT1:'deg',CUNIT2:'deg',
        CRVAL1:ra,CRVAL2:dec,CRPIX1:(width+1)/2,CRPIX2:(height+1)/2,
        CD1_1:-sx*c,CD1_2:-sy*s,CD2_1:-sx*s,CD2_2:sy*c,
        NAXIS1:width,NAXIS2:height
    };
}
const gvDiagnosticStrip=document.createElement('div');
Object.assign(gvDiagnosticStrip.style,{position:'absolute',left:'8px',right:'8px',bottom:'92px',zIndex:'7313',padding:'8px 10px',borderRadius:'8px',background:'rgba(0,0,0,.80)',color:'#dff8ff',font:'10px/1.35 monospace',overflowWrap:'normal',pointerEvents:'none',display:'grid',gridTemplateColumns:'1fr 1fr',gap:'12px',boxShadow:'0 0 14px rgba(88,191,255,.18)'});
const gvAvmDiagnostic=document.createElement('div'),gvLiveDiagnostic=document.createElement('div');
gvAvmDiagnostic.style.whiteSpace=gvLiveDiagnostic.style.whiteSpace='pre-wrap';gvDiagnosticStrip.append(gvAvmDiagnostic,gvLiveDiagnostic);document.getElementById('aladin-cosmic-command-test').appendChild(gvDiagnosticStrip);
function gvCatalogJsonUrl(destination){const key=String(destination?.catalogKey||'').trim().toLowerCase();const paths={hubble:'viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json',jwst:'viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json',eso:'viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json',chandra:'viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0007.json',spitzer:'viewer/image-databases/Spitzer/databases/gv-spitzer-galaxies-full-0011.json',noirlab:'viewer/image-databases/NoirLab/databases/gv-noirlab-galaxies-full-0001.json'};return paths[key]?new URL(paths[key],GV_MASTER_CATALOG_URL).href:'UNKNOWN'}
function gvWcsValue(wcs,...keys){for(const key of keys){const v=wcs?.[key]??wcs?.[key.toLowerCase()];if(v!==undefined&&v!==null)return v}return '?'}
function gvColorLine(label,value,color){const row=document.createElement('div');const key=document.createElement('span'),val=document.createElement('span');Object.assign(row.style,{display:'grid',gridTemplateColumns:'92px 1fr',gap:'8px',alignItems:'baseline'});key.textContent=label;val.textContent=value;key.style.color=color;val.style.color='#ffffff';key.style.opacity='.92';val.style.fontWeight='600';row.append(key,val);return row}
function gvPanelTitle(text){const row=document.createElement('div');row.textContent=text;Object.assign(row.style,{color:'#7CCBFF',fontWeight:'700',letterSpacing:'.5px',marginBottom:'3px',textTransform:'uppercase'});return row}
function gvSetDiagnostic(el,rows){el.replaceChildren(...rows)}
function gvFmt(v,d=6){const n=Number(v);return Number.isFinite(n)?n.toFixed(d):'?'}
function gvPublishCatalogWcs(destination,record,wcs){gvSetDiagnostic(gvAvmDiagnostic,[gvPanelTitle('JSON CATALOG'),gvColorLine('Galaxy',String(record?.name||destination?.name||record?.archiveId||'?'),'#7CCBFF'),gvColorLine('RA',gvFmt(record?.ra,8),'#ff8b8b'),gvColorLine('Dec',gvFmt(record?.dec,8),'#ff8b8b'),gvColorLine('Rotation',gvFmt(record?.aladinRotation??record?.spatialRotationDeg,4)+'°','#62ff72'),gvColorLine('Image FoV X',gvFmt(record?.fovXDegrees??record?.fovDegrees,8)+'°','#5ca9ff'),gvColorLine('Image FoV Y',gvFmt(record?.fovYDegrees??record?.fovDegrees,8)+'°','#5ca9ff'),gvColorLine('Viewport target','2.500 × image max FoV (intentional)','#ffe45c')])}
function gvPublishDiagnostic(destination){gvSetDiagnostic(gvAvmDiagnostic,[gvPanelTitle('JSON CATALOG'),gvColorLine('Galaxy',String(destination?.name||destination?.archiveId||destination?.id||'?'),'#7CCBFF'),gvColorLine('Status','loading catalog record','#ffe45c')])}
function gvReadAladinRaDec(){let v=null;try{v=aladin.getRaDec?.()}catch(_){}if(Array.isArray(v))return [v[0],v[1]];if(v&&typeof v==='object')return [v.ra??v.RA??v.lon??v.lng??v[0],v.dec??v.DE??v.lat??v[1]];for(const c of [aladin.view?.center,aladin.view?.viewCenter,aladin.view?.cooCenter,aladin.view?.radec]){if(Array.isArray(c))return [c[0],c[1]];if(c&&typeof c==='object')return [c.ra??c.RA??c.lon??c.lng??c.x,c.dec??c.DE??c.lat??c.y]}return []}
function gvReadAladinFov(){let v=null;try{v=aladin.getFov?.()}catch(_){}if(Array.isArray(v))return v;if(Number.isFinite(Number(v)))return [v,v];try{const f=aladin.view?.fov;if(Array.isArray(f))return f;if(Number.isFinite(Number(f)))return [f,f]}catch(_){}return []}
function gvPublishLiveAladin(){let r=gvReadAladinRaDec(),f=gvReadAladinFov(),rot='?',p='?',frame='?';try{rot=aladin.getRotation?.()??aladin.view?.rotation??'?'}catch(_){}try{p=aladin.getProjectionName?.()??aladin.getProjection?.()?.name??aladin.view?.projection?.name??'?'}catch(_){}try{frame=aladin.getFrame?.()??aladin.view?.cooFrame??'?'}catch(_){}gvSetDiagnostic(gvLiveDiagnostic,[gvPanelTitle('ALADIN LIVE'),gvColorLine('RA',gvFmt(r[0],8),'#ff8b8b'),gvColorLine('Dec',gvFmt(r[1],8),'#ff8b8b'),gvColorLine('Rotation',gvFmt(rot,4)+'°','#62ff72'),gvColorLine('Viewport FoV X',gvFmt(f[0],8)+'°','#5ca9ff'),gvColorLine('Viewport FoV Y',gvFmt(f[1]??f[0],8)+'°','#5ca9ff'),gvColorLine('Projection',String(p),'#ffe45c'),gvColorLine('Frame',String(frame),'#ffffff')])}
gvPublishLiveAladin();setInterval(gvPublishLiveAladin,100);

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

function directHdUrl(destination){return String(destination?.imageUrl??destination?.selectedImageUrl??destination?.hdUrl??'').trim()}
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
let zoomCommand=0;
let zoomFrame=0;
function zoomStep(){
    zoomFrame=0;
    if(!zoomCommand)return;
    try{
        const raw=aladin.getFov?.();
        const current=Number(Array.isArray(raw)?raw[0]:raw);
        if(Number.isFinite(current)&&current>0){
            const next=Math.max(0.0001,Math.min(180,current*Math.exp(-zoomCommand*0.018)));
            aladin.setFov(next);
        }
    }catch(_){}
    zoomFrame=requestAnimationFrame(zoomStep);
}
function setZoomCommandFromY(clientY){
    const r=zoomControl.rail.getBoundingClientRect();
    if(!r.height)return;
    zoomCommand=Math.max(-1,Math.min(1,((clientY-(r.top+r.height/2))/(r.height/2))));
    zoomControl.thumb.style.top=`${zoomControl.rail.offsetTop+((zoomCommand+1)/2)*zoomControl.rail.offsetHeight}px`;
    if(!zoomFrame)zoomFrame=requestAnimationFrame(zoomStep);
}
function releaseZoom(){
    zoomCommand=0;
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
            try{return {blob,width:bitmap.width,height:bitmap.height}}
            finally{try{bitmap.close?.()}catch(_){}}
        }catch(error){last=String(error?.message||error||'')}
    }
    throw new Error('GATE 2M IMAGE SOURCE FAILED: '+last);
}
async function loadDirectHdOnArrival(destination){
    directHdDestination=destination;
    try{aladin.removeImageLayer?.(DIRECT_HD_LAYER)}catch(_){}
    directHdOverlay=null;
    let imageObjectUrl='';
    try{
        const record=await gvRuntimeAvmRecord(destination);
        const url=String(record.imageUrl||'').trim();
        if(!url)throw new Error('GV JSON IMAGE URL MISSING');
        const ra=Number(record.ra),dec=Number(record.dec);
        const fovX=Number(record.fovXDegrees??record.fovDegrees);
        const fovY=Number(record.fovYDegrees??record.fovDegrees);
        const rotation=Number(record.aladinRotation??record.spatialRotationDeg);
        const previewWcs={CRVAL1:ra,CRVAL2:dec,NAXIS1:'?',NAXIS2:'?',CRPIX1:'?',CRPIX2:'?',CDELT1:'?',CDELT2:'?'};
        gvPublishCatalogWcs(destination,record,previewWcs);
        const raster=await gvLoadGate2MImage(url);
        if(directHdDestination!==destination)return false;
        imageObjectUrl=URL.createObjectURL(raster.blob);
        const displayWcs=gvSyntheticWcsFromRuntimeRecord(record,raster.width,raster.height);
        aladin.setProjection('TAN');
        aladin.gotoRaDec(ra,dec);
        aladin.setFoV(Math.max(fovX,fovY)*2.5);
        aladin.setRotation(rotation);
        coordinate.update(ra,dec);
        const layer=A.image(imageObjectUrl,{
            name:DIRECT_HD_LAYER,
            imgFormat:'jpeg',
            wcs:displayWcs,
            opacity:directHdOpacity(),
            successCallback:()=>{
                if(directHdDestination!==destination)return;
                directHdOverlay=layer;
                applyDirectHdOpacity();
                gvPublishCatalogWcs(destination,record,displayWcs);
                setTimeout(()=>URL.revokeObjectURL(imageObjectUrl),30000);
            },
            errorCallback:error=>{console.error('GV DIRECT HD JSON-WCS LAYER LOAD FAILED',error);gvSetDiagnostic(gvAvmDiagnostic,[gvPanelTitle('JSON CATALOG'),gvColorLine('Image load','FAILED: '+String(error),'#ff6666')])}
        });
        directHdOverlay=layer;
        aladin.setOverlayImageLayer(layer,DIRECT_HD_LAYER);
        return true;
    }catch(error){
        console.error('GV DIRECT HD JSON-WCS PREP FAILED',error);
        if(imageObjectUrl)try{URL.revokeObjectURL(imageObjectUrl)}catch(_){}
        return false;
    }
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


// ============================================================================
// SECTION 036 — DESTINATION → ALADIN HANDOFF
// ECO: GV200-001
// ============================================================================
function showDestination(destination){
    const v=validateDestination(destination);
    activeDestination=v.destination;
    aladin.setProjection('TAN');
    aladin.gotoRaDec(v.ra,v.dec);
    aladin.setFoV(v.fov);
    aladin.setRotation(v.rotation);
    coordinate.update(v.ra,v.dec);
    gvPublishDiagnostic(v.destination);
    loadDirectHdOnArrival(v.destination);
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