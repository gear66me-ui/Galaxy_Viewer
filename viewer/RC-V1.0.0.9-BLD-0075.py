from IPython.display import HTML, Javascript, display
import json

# ============================================================================
# SECTION 001 — FILE IDENTITY / PYTHON IMPORTS
# ECO: GV200-001
# ============================================================================
VIEWER_VERSION = "RC-V1.0.0.9"
# BUILD 0031 THREE-ROW HUD TRIP PLANNER: minimal transient caches and hidden-page polling suspension; preserve 0027 zoom behavior.
BUILD_NUMBER = "0075"
# Build 0022: canonical emission age computed from redshift with one flat-LCDM cosmic-age equation for every galaxy.
# BUILD 0013 — live Earth-distance match constrained to current field of view
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
HAMBURGER_BASE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@f7740afe20a1dccd0e58644e8c154f4e6396ed83/viewer/modules/hamburger-menu/gv-hamburger-menu-0012.js?v=GV200001-0120-HAMBURGER-CONST-FOV-TEST"
HAMBURGER_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@f7740afe20a1dccd0e58644e8c154f4e6396ed83/viewer/modules/hamburger-menu/gv-hamburger-menu-0012.js?v=GV200001-0120-HAMBURGER-CONST-FOV-TEST"
COORDINATE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@e38bfcc36a2f156517f9a77865da0c1c13d49175/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0008.js"
TARGET_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@7dcd8a191372e112b07bb20d0518a739a7c05865/viewer/modules/target-simbad/gv-target-simbad-0007.js"
DIAGNOSTICS_URL = ""
GALAXY_ROUTE_ENGINE_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@f5b26bd7a317a57a76a4b68adc05b50ec3f0567e/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js?v=0003"
GALAXY_NAVIGATOR_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@34d6f9b9417438afd56317bc838b93eb655c7d15/viewer/modules/galaxy-navigator/gv-galaxy-navigator-014.js"
HEADS_UP_DISPLAY_URL = "https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@acd66e473d4d3021b5f7915bb12898d863a489b8/viewer/modules/hud/gv-heads-up-display-0005.js"

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
#aladin-cosmic-command-test{position:relative;width:100%;height:100dvh;max-height:100%;overflow:hidden;background:radial-gradient(ellipse at 50% 44%,#123d78 0%,#0a2855 42%,#04152f 76%,#011813 100%);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box;touch-action:none}#aladin-cosmic-command-test .aladin-container,#aladin-cosmic-command-test .aladin-box{background:radial-gradient(ellipse at 50% 44%,#123d78 0%,#0a2855 42%,#04152f 76%,#011813 100%)!important}
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
const VERSION='RC-V1.0.0.9';
const GV200001_BUILD='0075'
const GV_RUNTIME='0137';
const fresh=url=>`${url}${url.includes('?')?'&':'?'}v=GV200001-${GV200001_BUILD}-RELEASE-1.0.0.9-BUILD-${GV200001_BUILD}`;
const requestPortraitLock=()=>{try{const lock=screen?.orientation?.lock;if(typeof lock==='function')Promise.resolve(lock.call(screen.orientation,'portrait-primary')).catch(()=>{})}catch(_){}};
requestPortraitLock();
document.addEventListener('pointerdown',requestPortraitLock,{once:true,passive:true});
window.GV_BOOT_CONFIG=Object.freeze({
    viewerVersion:'RC-V1.0.0.9',
    aladinVersion:'3.8.2',
    aladinCssUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/aladin-source-clone/src/css/aladin.css',
    aladinJsUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/vendor/aladin-lite/3.8.2/aladin.js',
    hamburgerBaseUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@f7740afe20a1dccd0e58644e8c154f4e6396ed83/viewer/modules/hamburger-menu/gv-hamburger-menu-0012.js?v=GV200001-0120-HAMBURGER-CONST-FOV-TEST',
    hamburgerUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@f7740afe20a1dccd0e58644e8c154f4e6396ed83/viewer/modules/hamburger-menu/gv-hamburger-menu-0012.js?v=GV200001-0120-HAMBURGER-CONST-FOV-TEST',
    constellationOverlayUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@92b371d69e6a3966e2915b9decfa2132acccaf48/viewer/modules/constellation-overlay/gv-constellation-overlay-0001.js',
    constellationOverlayFallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/92b371d69e6a3966e2915b9decfa2132acccaf48/viewer/modules/constellation-overlay/gv-constellation-overlay-0001.js',
    coordinateUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@e38bfcc36a2f156517f9a77865da0c1c13d49175/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0008.js',
    targetUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@7dcd8a191372e112b07bb20d0518a739a7c05865/viewer/modules/target-simbad/gv-target-simbad-0007.js',
    galaxyRouteEngineUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@f5b26bd7a317a57a76a4b68adc05b50ec3f0567e/viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js',
    galaxyNavigatorUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@d85d91201ea52aa6524a62394fc81b450b15ac23/viewer/modules/galaxy-navigator/gv-galaxy-navigator-013.js',
    headsUpDisplayUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@acd66e473d4d3021b5f7915bb12898d863a489b8/viewer/modules/hud/gv-heads-up-display-0005.js',
    providerArtworkUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@c824f16398ec8aae39885c101545173e7846ad33/viewer/modules/provider-artwork/gv-provider-artwork-0005.js',
    providerArtworkFallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/c824f16398ec8aae39885c101545173e7846ad33/viewer/modules/provider-artwork/gv-provider-artwork-0005.js',
    travelPresentationUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@4fe85d199bdd9bc3b9f9bd18c0bc10a17e1a59d9/viewer/modules/random-galaxy/gv-random-travel-presentation-005.js',
    destinationPresentationUrl:'https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@25e3a5367630bf93f6759dd18a67f91958a44e3e/viewer/modules/destination-presentation/gv-destination-presentation-0061.js'
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

// PROVIDER ARTWORK 0007 EMBEDDED FALLBACK: keep boot independent of third-party script CDN availability.
(()=>{'use strict';
const VERSION='0007';
const ART='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/artwork/';
const CDN_ART='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/';
const PAGES_ART='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/';
const PROVIDER_ARTWORK=Object.freeze({
  HUBBLE:'Hubble/Hubble.jpg',
  JWST:'JWST/JWST.jpeg',
  CHANDRA:'Chandra/Chandra.jpg',
  ESO:'ESO/ESO.jpg',
  NOIRLAB:'NoirLabs/NOIRLab.jpg',
  SPITZER:'Spitzer/Spitzer.jpg',
  EUCLID:'Euclid/Euclid.jpg',
  HERSCHEL:'Herschel/Herschel.jpg',
  GALEX:'GALEX/GALEX.jpg',
  NUSTAR:'NuSTAR/NuSTAR.jpg',
  NRAO:'NRAO/NRAO.jpg'
});
const ALIASES=Object.freeze({
  'HUBBLE SPACE TELESCOPE':'HUBBLE',
  'JAMES WEBB SPACE TELESCOPE':'JWST',
  'CHANDRA X-RAY OBSERVATORY':'CHANDRA',
  'NSF NOIRLAB':'NOIRLAB',
  'SPITZER SPACE TELESCOPE':'SPITZER'
});
function key(provider){
  const raw=String(provider??'').trim().toUpperCase();
  return ALIASES[raw]||raw;
}
function path(provider){
  const k=key(provider);
  return Object.prototype.hasOwnProperty.call(PROVIDER_ARTWORK,k)?PROVIDER_ARTWORK[k]:'';
}
function icon(provider){
  const p=path(provider);
  return p?CDN_ART+p:'';
}
function iconSources(provider){
  const p=path(provider);
  return p?[CDN_ART+p,ART+p,PAGES_ART+p]:[];
}
const CONSTELLATION_ALIASES=Object.freeze({
AND:'ANDROMEDA',ANT:'ANTLIA',APS:'APUS',AQR:'AQUARIUS',AQL:'AQUILA',ARA:'ARA',ARI:'ARIES',AUR:'AURIGA',BOO:'BOOTES',CAE:'CAELUM',CAM:'CAMELOPARDALIS',CNC:'CANCER',CVN:'CANES_VENATICI',CMA:'CANIS_MAJOR',CMI:'CANIS_MINOR',CAP:'CAPRICORNUS',CAR:'CARINA',CAS:'CASSIOPEIA',CEN:'CENTAURUS',CEP:'CEPHEUS',CET:'CETUS',CHA:'CHAMAELEON',CIR:'CIRCINUS',COL:'COLUMBA',COM:'COMA_BERENICES',CRA:'CORONA_AUSTRALIS',CRB:'CORONA_BOREALIS',CRV:'CORVUS',CRT:'CRATER',CRU:'CRUX',CYG:'CYGNUS',DEL:'DELPHINUS',DOR:'DORADO',DRA:'DRACO',EQU:'EQUULEUS',ERI:'ERIDANUS',FOR:'FORNAX',GEM:'GEMINI',GRU:'GRUS',HER:'HERCULES',HOR:'HOROLOGIUM',HYA:'HYDRA',HYI:'HYDRUS',IND:'INDUS',LAC:'LACERTA',LEO:'LEO',LMI:'LEO_MINOR',LEP:'LEPUS',LIB:'LIBRA',LUP:'LUPUS',LYN:'LYNX',LYR:'LYRA',MEN:'MENSA',MIC:'MICROSCOPIUM',MON:'MONOCEROS',MUS:'MUSCA',NOR:'NORMA',OCT:'OCTANS',OPH:'OPHIUCHUS',ORI:'ORION',PAV:'PAVO',PEG:'PEGASUS',PER:'PERSEUS',PHE:'PHOENIX',PIC:'PICTOR',PSC:'PISCES',PSA:'PISCIS_AUSTRINUS',PUP:'PUPPIS',PYX:'PYXIS',RET:'RETICULUM',SGE:'SAGITTA',SGR:'SAGITTARIUS',SCO:'SCORPIUS',SCL:'SCULPTOR',SCT:'SCUTUM',SER:'SERPENS',SEX:'SEXTANS',TAU:'TAURUS',TEL:'TELESCOPIUM',TRI:'TRIANGULUM',TRA:'TRIANGULUM_AUSTRALE',TUC:'TUCANA',UMA:'URSA_MAJOR',UMI:'URSA_MINOR',VEL:'VELA',VIR:'VIRGO',VOL:'VOLANS',VUL:'VULPECULA'
});
function constellationSources(name){
  const raw=String(name??'').trim().toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9]+/g,'_').replace(/^_+|_+$/g,'');
  if(!raw)return[];
  const k=CONSTELLATION_ALIASES[raw]||raw;
  const p='Constellations/'+encodeURIComponent(k)+'.SVG';
  return [CDN_ART+p,PAGES_ART+p,ART+p];
}
// Bounded LRU cache for successful and in-flight artwork image probes.
const IMAGE_CACHE_LIMIT=36;
const imageCache=new Map();
function trimImageCache(){while(imageCache.size>IMAGE_CACHE_LIMIT)imageCache.delete(imageCache.keys().next().value)}
function loadSource(url){
  if(imageCache.has(url)){const cached=imageCache.get(url);imageCache.delete(url);imageCache.set(url,cached);return cached;}
  const promise=new Promise((resolve,reject)=>{
    const probe=new Image();
    let settled=false;
    // Bound stalled CDN requests so a dead primary source cannot hold up the
    // constellation fallback chain indefinitely.
    const timeout=setTimeout(()=>{
      if(settled)return;
      settled=true;
      if(imageCache.get(url)===promise)imageCache.delete(url);
      reject(new Error('GV ARTWORK LOAD TIMEOUT '+url));
    },900);
    probe.onload=()=>{
      if(settled)return;
      settled=true;clearTimeout(timeout);resolve(url);
    };
    probe.onerror=()=>{
      if(settled)return;
      settled=true;clearTimeout(timeout);if(imageCache.get(url)===promise)imageCache.delete(url);
      reject(new Error('GV ARTWORK LOAD FAILED '+url));
    };
    probe.src=url;
    if(probe.complete&&probe.naturalWidth>0){
      settled=true;clearTimeout(timeout);resolve(url);
    }
  });
  imageCache.set(url,promise);trimImageCache();
  return promise;
}
const imageRequestTokens=new WeakMap();
// Promise.any is not available in every Android WebView used by Galaxy Viewer.
function firstSuccessful(promises){
  return new Promise((resolve,reject)=>{
    let pending=promises.length;
    const errors=[];
    if(!pending){reject(new Error('GV ARTWORK HAS NO SOURCES'));return}
    promises.forEach(promise=>Promise.resolve(promise).then(resolve,error=>{
      errors.push(error);
      if(--pending===0)reject(new Error('GV ARTWORK SOURCES ALL FAILED: '+errors.map(e=>String(e?.message||e)).join(' | ')));
    }));
  });
}
function loadImage(img,sources,onReady,onFail){
  const urls=[...new Set((sources||[]).filter(Boolean))];
  const token=(imageRequestTokens.get(img)||0)+1;
  imageRequestTokens.set(img,token);
  const active=()=>imageRequestTokens.get(img)===token;
  let index=0,finished=false;
  img.onload=null;
  img.onerror=null;
  const fail=()=>{
    if(!active()||finished)return;
    if(index>=urls.length){
      finished=true;
      img.removeAttribute('src');
      console.error('GV ARTWORK ALL SOURCES FAILED',{alt:img.alt||'',sources:urls});
      onFail?.();
      return;
    }
    const url=urls[index++];
    img.onload=()=>{
      if(!active()||finished)return;
      finished=true;
      onReady?.(url);
    };
    img.onerror=()=>{
      if(!active()||finished)return;
      console.warn('GV ARTWORK IMAGE REQUEST FAILED',{alt:img.alt||'',url,remaining:urls.length-index});
      fail();
    };
    // Assign directly to the displayed image. This avoids probing with a
    // separate Image object and then relying on a second request/cache hit.
    img.src=url;
    if(img.complete&&img.naturalWidth>0){
      finished=true;
      onReady?.(url);
    }
  };
  if(!urls.length){onFail?.();return}
  fail();
}
globalThis.GVProviderArtwork=Object.freeze({VERSION,ART,CDN_ART,PAGES_ART,PROVIDER_ARTWORK,key,path,icon,iconSources,constellationSources,loadImage,cacheDiagnostics:()=>Object.freeze({entries:imageCache.size,limit:IMAGE_CACHE_LIMIT})});
})();
const gvModuleLoadPromise=Promise.all([
    loadScript(config.hamburgerBaseUrl).catch(error=>{console.error('HAMBURGER MODULE LOAD FAILED',error)}),
    loadScript(config.constellationOverlayUrl).catch(error=>{console.error('CONSTELLATION CDN LOAD FAILED; RETRYING RAW GITHUB',error);return loadScript(config.constellationOverlayFallbackUrl)}).catch(error=>{console.error('CONSTELLATION MODULE LOAD FAILED ON BOTH SOURCES',error)}),
    loadScript(config.providerArtworkUrl).then(()=>{if(window.GVProviderArtwork?.VERSION!=='0007')throw new Error('PROVIDER ARTWORK CDN EXPORT MISSING');}).catch(error=>{console.warn('REMOTE PROVIDER ARTWORK LOAD FAILED; USING EMBEDDED 0007 MODULE',error);if(window.GVProviderArtwork?.VERSION!=='0007')return loadScript(config.providerArtworkFallbackUrl).then(()=>{if(window.GVProviderArtwork?.VERSION!=='0007')throw new Error('PROVIDER ARTWORK 0007 EXPORT MISSING AFTER ALL FALLBACKS');});}),
    loadScript(config.coordinateUrl).catch(error=>console.error('COORDINATE OVERLAY LOAD FAILED',error)),
    loadScript(config.targetUrl).then(()=>{if(window.GalaxyViewerTargetSimbad?.version!=='0007')throw new Error('TARGET MODULE LOADED WITHOUT 0007 EXPORT');}).catch(error=>{console.error('TARGET MODULE LOAD FAILED; RETRYING IMMUTABLE TARGET PIN',error);return loadScript(config.targetUrl+'?gv-target-retry=0007').then(()=>{if(window.GalaxyViewerTargetSimbad?.version!=='0007')throw new Error('TARGET SURVEY 0007 EXPORT STILL MISSING AFTER RETRY');});}),
    loadScript(config.galaxyRouteEngineUrl).catch(error=>{console.error('ROUTE ENGINE LOAD FAILED',error)}),
    loadScript(config.galaxyNavigatorUrl).catch(error=>{console.error('GALAXY NAVIGATOR LOAD FAILED',error)}),
    loadScript(config.headsUpDisplayUrl).catch(error=>{console.error('HEADS-UP DISPLAY LOAD FAILED',error)}),
    loadScript(config.travelPresentationUrl).catch(error=>{console.error('TRAVEL PRESENTATION LOAD FAILED',error)}),
    loadScript(fresh(config.destinationPresentationUrl)).then(()=>{if(window.GalaxyDestinationPresentation?.VERSION!=='0061'||typeof window.GalaxyDestinationPresentation.mount!=='function')throw new Error('DESTINATION PRESENTATION CDN EXPORT MISSING');}).catch(error=>{console.warn('DESTINATION PRESENTATION CDN LOAD/EXPORT FAILED; RETRYING GITHUB PAGES',error);return loadScript(fresh('https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/destination-presentation/gv-destination-presentation-0061.js')).then(()=>{if(window.GalaxyDestinationPresentation?.VERSION!=='0061'||typeof window.GalaxyDestinationPresentation.mount!=='function')throw new Error('DESTINATION PRESENTATION 0061 EXPORT MISSING AFTER GITHUB PAGES RETRY');});}),
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
    backgroundColor:'rgb(5, 22, 52)',
    survey:'https://stpubdata.s3.us-east-1.amazonaws.com/mast/skybackgrounds/DSSColor',
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

// Aladin 3.8.2 dispatches background changes to the WASM renderer asynchronously.
// Re-apply after construction and after renderer startup so the first background
// request cannot be lost during WASM initialization.
const GV_SKY_BACKGROUND='rgb(5, 22, 52)';
const gvApplySkyBackground=()=>{
    try{aladin.setBackgroundColor(GV_SKY_BACKGROUND)}catch(error){
        console.warn('GV SKY BACKGROUND APPLY FAILED',error);
    }
};
requestAnimationFrame(gvApplySkyBackground);
setTimeout(gvApplySkyBackground,500);
setTimeout(gvApplySkyBackground,1500);

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
window.GV_NAV_HIPS_ZOOM_SUSPENDED=false;
window.GV_NAV_HIPS_ZOOM_RESUME_TIMER=0;
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
        if((window.GV_NAV_HIPS_FETCH_SUSPENDED||window.GV_NAV_HIPS_ZOOM_SUSPENDED)&&tilePath.test(url)){
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
let gvStartupMollweideScreen=true;
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
        if(Number.isFinite(ra)&&Number.isFinite(dec))gvSetEarthPointerPosition(ra,dec,gvEarthPointerActive);
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
    // BUILD 0053 — sole distance source: AVM runtime catalog 0004 records[].distanceMly.
    const v=Number(destination?.distanceMly);
    if(!(v>0)||!Number.isFinite(v))throw new Error('AVM runtime distanceMly missing or invalid');
    if(v>=1000)return (v/1000).toFixed(2)+' BLY';
    if(v>=1)return v.toFixed(2)+' MLY';
    return (v*1000).toFixed(2)+' KLY';
}
function gvFormatEarthRedshift(destination){
    // Sole source: AVM runtime catalog 0004 records[].redshift, FLRW-derived upstream.
    const z=Number(destination?.redshift);
    if(!Number.isFinite(z)||z<0)throw new Error('AVM runtime redshift missing or invalid');
    return 'Z='+z.toFixed(6);
}
function gvInstallEarthDistanceBanner(){
    if(document.getElementById('gv-earth-distance-banner')&&document.getElementById('gv-live-physical-scale'))return;
    const style=document.createElement('style');style.textContent=`
#gv-earth-distance-banner{position:fixed;left:50%;z-index:7362;transform:translateX(-50%);box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;gap:4px;width:max-content;max-width:calc(100vw - 24px);min-width:0;min-height:0;padding:3px 5px;border:1px solid #58BFFF;border-radius:5px;background:linear-gradient(145deg,rgba(4,20,48,.94),rgba(12,52,116,.94));box-shadow:0 0 5px rgba(88,191,255,.48);font:400 11px/1 "GV Space Age",sans-serif;letter-spacing:1px;white-space:nowrap;color:#FFD84A;text-align:center;text-shadow:0 0 3px rgba(255,216,74,.78);pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-earth-distance-banner .gv-earth-distance-icon{display:inline-block;font:11px/1 system-ui,sans-serif;letter-spacing:0;filter:drop-shadow(0 0 2px rgba(88,191,255,.55))}
#gv-earth-distance-banner.gv-visible{opacity:1;visibility:visible}
#gv-earth-distance-banner .gv-earth-distance-tick{display:inline-block;margin-left:7px;width:0;height:0;border-top:5px solid transparent;border-bottom:5px solid transparent;border-left:9px solid #FFD84A;filter:drop-shadow(0 0 4px rgba(255,216,74,.9));vertical-align:-1px}
#gv-live-physical-scale{position:fixed;left:50%;z-index:7362;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear;font:400 11px/1 "GV Space Age",sans-serif;letter-spacing:1px;color:#FFD84A;text-align:center;text-shadow:0 0 3px rgba(255,216,74,.78);white-space:normal;width:min(50vw,60%);max-width:60%;overflow:hidden}
#gv-live-physical-scale.gv-visible{opacity:1;visibility:visible}
#gv-live-physical-scale .gv-live-scale-label{margin-bottom:4px}
#gv-live-physical-scale .gv-live-scale-line{position:relative;height:1px;background:#FFD84A;box-shadow:0 0 4px rgba(255,216,74,.9);min-width:4px}
#gv-live-physical-scale .gv-live-scale-line::before,#gv-live-physical-scale .gv-live-scale-line::after{content:"";position:absolute;top:50%;width:1px;height:9px;background:#FFD84A;box-shadow:0 0 4px rgba(255,216,74,.9);transform:translateY(-50%)}
#gv-live-physical-scale .gv-live-scale-line::before{left:0}
#gv-live-physical-scale .gv-live-scale-line::after{right:0}`;document.head.appendChild(style);
    const b=document.createElement('div');b.id='gv-earth-distance-banner';document.body.appendChild(b);
    const s=document.createElement('div');s.id='gv-live-physical-scale';s.innerHTML='<span class="gv-live-scale-label"></span><span class="gv-live-scale-line"></span>';document.body.appendChild(s);
}
let gvNavigationTravelActive=false;
let gvLiveScaleValueLy=null;
let gvEarthDistanceTarget=null;
let gvEarthDistanceTargetKey='';
const gvLiveScaleNominalPx=25*96/25.4;
function gvEarthDistanceIdentity(destination){
    return String(destination?.archiveId||destination?.id||destination?.imageUrl||destination?.designation||destination?.name||[destination?.ra,destination?.dec].join(',')).trim().toLowerCase();
}
function gvFormatLiveScale(ly){
 if(!(ly>0))return '';
 if(ly>=1e9)return `${(ly/1e9).toLocaleString('en-US',{maximumFractionDigits:2})} BLY`;
 if(ly>=1e6)return `${(ly/1e6).toLocaleString('en-US',{maximumFractionDigits:2})} MLY`;
 if(ly>=1e3)return `${(ly/1e3).toLocaleString('en-US',{maximumFractionDigits:2})} KLY`;
 return `${ly.toLocaleString('en-US',{maximumFractionDigits:2})} LY`;
}
function gvChooseLiveScaleValue(lyPerPx){
 const target=lyPerPx*gvLiveScaleNominalPx;if(!(target>0))return null;
 const e=Math.floor(Math.log10(target)),values=[];
 for(let n=e-2;n<=e+2;n++)for(const m of [1,2,5])values.push(m*Math.pow(10,n));
 values.sort((x,y)=>Math.abs(x/lyPerPx-gvLiveScaleNominalPx)-Math.abs(y/lyPerPx-gvLiveScaleNominalPx));
 return values[0]||null;
}
function gvUpdateLivePhysicalScale(){
 // Keep the physical ruler live during travel too; other background polling remains suspended.
 const s=document.getElementById('gv-live-physical-scale'),line=s?.querySelector('.gv-live-scale-line'),label=s?.querySelector('.gv-live-scale-label'),banner=document.getElementById('gv-earth-distance-banner');
 if(!s||!line||!label)return;
 if(gvStartupMollweideScreen||!gvEarthPointerActive){s.classList.remove('gv-visible');return;}
 if(gvNavigationTravelActive){s.classList.remove('gv-visible');return;}
 const size=aladin.getSize?.(),width=Number(size?.[0]||document.getElementById('aladin-cosmic-command-test')?.clientWidth||innerWidth),height=Number(size?.[1]||document.getElementById('aladin-cosmic-command-test')?.clientHeight||innerHeight),fov=aladin.getFov?.();
 const fovX=Number(Array.isArray(fov)?fov[0]:fov?.x??fov?.fovX);
 const distanceSource=gvEarthDistanceTarget;
 const distanceMly=Number(distanceSource?.distanceMly);
 if(!(width>1)||!(height>1)||!(fovX>0)||fovX>180||!Number.isFinite(fovX)||!(distanceMly>0)||!Number.isFinite(distanceMly)){
  s.classList.remove('gv-visible');console.error('GV0120 AVM FOV ruler needs viewport, live FOV, and catalog distance',{width,height,fovX,distanceMly});return;
 }
 // Aladin Lite 3.8.2 pix2world(x,y,'icrs') maps viewport pixels to sky coordinates.
 // Physical size uses the explicitly defined transverse small-angle model: D × angular separation in radians.
 const physicalSpanLy=px=>{
  if(!(px>0)||!Number.isFinite(px)||px>width*.9)return null;
  const x1=(width-px)/2,x2=(width+px)/2,y=height/2;
  let a,b;
  try{a=aladin.pix2world(x1,y,'icrs');b=aladin.pix2world(x2,y,'icrs')}catch(e){return null}
  if(!Array.isArray(a)||!Array.isArray(b)||a.length<2||b.length<2||![a[0],a[1],b[0],b[1]].every(Number.isFinite))return null;
  const rad=Math.PI/180,lat1=a[1]*rad,lat2=b[1]*rad,dLat=lat2-lat1,dLon=((b[0]-a[0]+540)%360-180)*rad;
  const q=Math.sin(dLat/2)**2+Math.cos(lat1)*Math.cos(lat2)*Math.sin(dLon/2)**2;
  if(!Number.isFinite(q)||q<0||q>1)return null;
  const angle=2*Math.asin(Math.sqrt(q)),ly=2*distanceMly*1e6*Math.sin(angle/2);
  return ly>0&&Number.isFinite(ly)?ly:null;
 };
 const onePx=physicalSpanLy(1);
 if(!(onePx>0)||!Number.isFinite(onePx)){
  s.classList.remove('gv-visible');console.error('GV0121 ALADIN PIXEL-TO-SKY SCALE UNAVAILABLE',{fovXDegrees:fovX,viewportWidth:width,viewportHeight:height,distanceMly,method:'pix2world endpoint separation'});return;
 }
 gvLiveScaleValueLy=gvChooseLiveScaleValue(onePx);
 if(!(gvLiveScaleValueLy>0)||!Number.isFinite(gvLiveScaleValueLy))return;
 // Solve the actual endpoint geometry for the chosen 1–2–5 physical scale.
 let lo=1,hi=width*.9,barPx=null;
 const maxSpan=physicalSpanLy(hi);
 if(maxSpan&&maxSpan>=gvLiveScaleValueLy){
  for(let i=0;i<36;i++){const mid=(lo+hi)/2,span=physicalSpanLy(mid);if(!(span>0)){hi=mid;continue}if(span<gvLiveScaleValueLy)lo=mid;else hi=mid}
  barPx=(lo+hi)/2;
 }
 if(!Number.isFinite(barPx)||barPx<8||barPx>width*.9){
  barPx=Math.min(width*.8,Math.max(8,gvLiveScaleNominalPx));
  const actual=physicalSpanLy(barPx);
  if(!(actual>0)||!Number.isFinite(actual)){s.classList.remove('gv-visible');console.error('GV0122 ALADIN PIXEL-TO-SKY ENDPOINTS INVALID',{barPx,width,height,fovXDegrees:fovX});return}
  gvLiveScaleValueLy=actual;
 }else{
  const actual=physicalSpanLy(barPx);
  if(!(actual>0)||!Number.isFinite(actual)){s.classList.remove('gv-visible');console.error('GV0122 ALADIN PIXEL-TO-SKY ENDPOINTS INVALID',{barPx,width,height,fovXDegrees:fovX});return}
  gvLiveScaleValueLy=actual;
 }
 line.style.width=`${barPx}px`;label.textContent=gvFormatLiveScale(gvLiveScaleValueLy);
 if(banner?.classList.contains('gv-visible'))s.style.bottom=`${Math.max(8,innerHeight-banner.getBoundingClientRect().top+8)}px`;
 else s.style.bottom='calc(100% - 72px)';
 s.classList.add('gv-visible');
 console.info('GV0123 ALADIN PIXEL-TO-SKY PHYSICAL SCALE',{fovXDegrees:fovX,viewportWidth:width,viewportHeight:height,distanceMly,scaleValueLy:gvLiveScaleValueLy,widthPx:barPx,method:'Aladin pix2world endpoint separation; transverse D×angle(rad)'});
}
function gvHideEarthDistance(){document.getElementById('gv-earth-distance-banner')?.classList.remove('gv-visible');document.getElementById('gv-live-physical-scale')?.classList.remove('gv-visible');gvLiveScaleValueLy=null;gvEarthDistanceTarget=null;gvEarthDistanceTargetKey=''}
let gvEarthDistanceDisplayGeneration=0;
async function gvShowEarthDistance(destination,alreadyResolvedRuntimeRecord=false){
    gvInstallEarthDistanceBanner();
    const b=document.getElementById('gv-earth-distance-banner');
    if(!b||gvNavigationTravelActive)return;
    if(gvStartupMollweideScreen||!gvEarthPointerActive){gvHideEarthDistance();return;}
    const generation=++gvEarthDistanceDisplayGeneration;
    try{
        // Resolve navigation destinations by exact image identity. Live-center matches are already exact records from this same runtime catalog; do not remap them by a possibly colliding archive ID.
        const record=alreadyResolvedRuntimeRecord?destination:await gvRuntimeAvmRecord(destination);
        const distanceMly=Number(record?.distanceMly),redshift=Number(record?.redshift);
        if(!(distanceMly>0)||!Number.isFinite(distanceMly))throw new Error('AVM runtime distanceMly missing or invalid');
        if(!Number.isFinite(redshift)||redshift<0)throw new Error('AVM runtime redshift missing or invalid');
        if(generation!==gvEarthDistanceDisplayGeneration||gvNavigationTravelActive)return;
        const runtimeDestination={...record,distanceMly,redshift};
        const text=gvFormatEarthDistance(runtimeDestination);
        const key=gvEarthDistanceIdentity(runtimeDestination);
        const previousText=gvEarthDistanceTarget
            ?gvFormatEarthDistance(gvEarthDistanceTarget)
            :'';
        const selectionChanged=key!==gvEarthDistanceTargetKey||text!==previousText;
        gvEarthDistanceTarget=runtimeDestination;
        gvEarthDistanceTargetKey=key;
        if(selectionChanged||!b.querySelector('.gv-earth-distance-icon')){
            b.innerHTML=`<span class="gv-earth-distance-icon" aria-hidden="true">🌎</span><span>${text}</span><span class="gv-earth-distance-tick" aria-hidden="true"></span>`;
            gvLiveScaleValueLy=null;
            console.info('GV0009 AVM RUNTIME DISTANCE UPDATED',{key,distanceMly,redshift,display:text,source:'gv-avm-runtime-catalog-0006.json'});
        }
        const card=document.querySelector('.gvdp-card');
        const place=()=>{const r=card?.getBoundingClientRect();b.style.bottom=`${r&&r.height?Math.max(0,innerHeight-r.top+6):130}px`;gvUpdateLivePhysicalScale()};
        place();
        if(!b.classList.contains('gv-visible'))b.classList.add('gv-visible');
    }catch(error){
        if(generation!==gvEarthDistanceDisplayGeneration)return;
        b.classList.remove('gv-visible');
        gvEarthDistanceTarget=null;gvEarthDistanceTargetKey='';gvLiveScaleValueLy=null;
        console.error('GV AVM RUNTIME DISTANCE/REDSHIFT DISPLAY FAILED — NO FALLBACK',error);
    }
}
gvInstallEarthDistanceBanner();
// BUILD 0036 STUTTER FIX: skip repeated ruler layout/scale work while the zoom slider is driving setFov.
// The zoom release path schedules one final distance/scale sync.
setInterval(()=>{if(document.visibilityState==='visible'&&!gvZoomInteractionActive&&!gvNavigationTravelActive)gvUpdateLivePhysicalScale()},120);

// BUILD 0130 — resolve the galaxy nearest Aladin's live center coordinate.
// Distance comes from that galaxy's catalog record; the physical ruler then
// recomputes from its distance and Aladin's current FOV. Never mutate activeDestination.
let gvZoomInteractionActive=false;
let gvZoomSyncTimer=0;
function gvScheduleEarthDistanceAfterZoom(){
    if(gvZoomSyncTimer)clearTimeout(gvZoomSyncTimer);
    gvZoomSyncTimer=setTimeout(()=>{gvZoomSyncTimer=0;gvSyncEarthDistanceToCenter();gvUpdateLivePhysicalScale()},140);
}
let gvEarthDistanceTouchGestureActive=false;
let gvEarthDistanceTouchSyncTimer=0;
let gvEarthDistanceSyncBusy=false;
let gvEarthDistanceSyncGeneration=0;
let gvEarthDistanceSyncPending=false;
let gvEarthDistanceSyncLastError='';
// Preserve the catalog-authoritative arrival distance until the user actually changes the sky view.
let gvEarthDistanceArrivalDestination=null;
let gvEarthDistanceUserAdjustedView=false;
let gvEarthDistanceLastObservedCenter=null;
let gvEarthDistanceInteractionListenersInstalled=false;
async function gvSyncEarthDistanceToCenter(){
    // Do not invalidate an in-flight catalog match on every 300 ms poll.
    // A busy request is allowed to finish; the next poll then samples the latest center.
    if(gvEarthDistanceSyncBusy){
        // Keep the latest gesture refresh instead of dropping it while a catalog read is in flight.
        gvEarthDistanceSyncPending=true;
        return;
    }
    const syncGeneration=++gvEarthDistanceSyncGeneration;
    const banner=document.getElementById('gv-earth-distance-banner');
    if(!banner)return;
    if(gvNavigationTravelActive){gvHideEarthDistance();return;}
    // BUILD 0015: during native Android touch/pinch, Aladin's center and FOV are transient.
    // Do not run catalog matching until all fingers are lifted; otherwise a temporary no-match
    // clears the Earth pointer mid-pinch. One settled sync runs after the gesture ends.
    if(gvEarthDistanceTouchGestureActive)return;
    // BUILD 0013 FIX: arrival is authoritative until the user actually pans/zooms.
    // Prevent the background center poll from immediately replacing the HD-card distance
    // with a nearby catalog record. Gesture listeners set this flag on user interaction.
    if(gvEarthDistanceArrivalDestination&&!gvEarthDistanceUserAdjustedView)return;
    // Poll the actual Aladin sky center before trusting event handlers. This catches
    // WebView touch pans even when Aladin's positionChanged callback is missed.
    const observedSize=aladin.getSize?.();
    const observedWidth=Number(observedSize?.[0]||document.getElementById('aladin-cosmic-command-test')?.clientWidth||innerWidth);
    const observed=typeof aladin.getRaDec==='function'
        ? aladin.getRaDec()
        : (observedWidth>1&&typeof aladin.pix2world==='function'
            ? aladin.pix2world(observedWidth/2,Number(observedSize?.[1]||innerHeight)/2)
            : null);
    if(observed){
        const observedRa=Number(Array.isArray(observed)?observed[0]:(observed?.ra??observed?.[0]));
        const observedDec=Number(Array.isArray(observed)?observed[1]:(observed?.dec??observed?.[1]));
        if(Number.isFinite(observedRa)&&Number.isFinite(observedDec)){
            // Center drift alone is not proof of a deliberate user pan; arrival animation
            // and settling can emit position changes. Only explicit sky gestures unlock live matching.
            gvEarthDistanceLastObservedCenter={ra:observedRa,dec:observedDec};
        }
    }
    // BUILD 0009: arrival is authoritative until the user deliberately pans the sky.
    // Do not let the periodic live-center poll replace the just-arrived galaxy with
    // a nearby/previous catalog record when travel finishes.
    if(gvEarthDistanceArrivalDestination&&!gvEarthDistanceUserAdjustedView)return;
    gvEarthDistanceSyncBusy=true;
    try{
        const size=aladin.getSize?.();
        const width=Number(size?.[0]||document.getElementById('aladin-cosmic-command-test')?.clientWidth||innerWidth);
        const height=Number(size?.[1]||innerHeight);
        if(!(width>1)||!(height>1))return;
        // Aladin Lite's public getRaDec() API is the canonical live ICRS view center.
        // pix2world is retained only as a compatibility fallback for older runtimes.
        const center=typeof aladin.getRaDec==='function'
            ? aladin.getRaDec()
            : (typeof aladin.pix2world==='function'?aladin.pix2world(width/2,height/2):null);
        const centerRa=Number(Array.isArray(center)?center[0]:(center?.ra??center?.[0]));
        const centerDec=Number(Array.isArray(center)?center[1]:(center?.dec??center?.[1]));
        if(!Number.isFinite(centerRa)||!Number.isFinite(centerDec))return;
        if(!Number.isFinite(centerRa)||!Number.isFinite(centerDec))return;
        const rawFov=aladin.getFov?.();
        const fovX=Number(Array.isArray(rawFov)?rawFov[0]:(rawFov?.x??rawFov?.fovX));
        const fovY=Number(Array.isArray(rawFov)?rawFov[1]:(rawFov?.y??rawFov?.fovY));
        const catalog=await gvLoadAvmRuntimeCatalog();
        // Reject stale asynchronous work after any newer pan/zoom refresh.
        if(gvNavigationTravelActive)return;
        if(syncGeneration!==gvEarthDistanceSyncGeneration)return;
        const rad=Math.PI/180,ra0=centerRa*rad,dec0=centerDec*rad;
        const safeFovX=Number.isFinite(fovX)&&fovX>0?fovX:0;
        const safeFovY=Number.isFinite(fovY)&&fovY>0?fovY:(safeFovX>0?safeFovX*height/width:0);
        if(!(safeFovX>0)||!(safeFovY>0))return;
        let nearest=null,nearestDeg=Infinity;
        for(const record of catalog.records){
            const ra=Number(record?.ra),dec=Number(record?.dec);
            const distanceMly=Number(record?.distanceMly);
            if(!Number.isFinite(ra)||!Number.isFinite(dec)||!(distanceMly>0)||!Number.isFinite(distanceMly))continue;
            // Wrap RA across 0/360, then reject catalog records outside the live rectangular FOV.
            let deltaRa=((ra-centerRa+540)%360)-180;
            const dx=deltaRa*Math.cos(dec0),dy=dec-centerDec;
            const fieldX=Math.abs(dx)/(safeFovX/2),fieldY=Math.abs(dy)/(safeFovY/2);
            if(fieldX>1||fieldY>1)continue;
            const r=ra*rad,d=dec*rad,sd=Math.sin((d-dec0)/2),sr=Math.sin((r-ra0)/2);
            const h=Math.max(0,Math.min(1,sd*sd+Math.cos(dec0)*Math.cos(d)*sr*sr));
            const separation=2*Math.asin(Math.sqrt(h))/rad;
            if(separation<nearestDeg){nearestDeg=separation;nearest=record}
        }
        // On pan/zoom, resolve the closest galaxy inside the live RA/Dec field,
        // rather than requiring a match inside a fixed-radius center tolerance.
        if(syncGeneration!==gvEarthDistanceSyncGeneration)return;
        if(!nearest){
            // BUILD 0006: never reuse another galaxy's distance when the current
            // sky field has no catalog match. Clear the badge and ruler until a
            // valid match for the current field is available.
            gvEarthDistanceDisplayGeneration++;
            gvHideEarthDistance();
            console.info('GV0007 EARTH DISTANCE NO CATALOG MATCH — CLEARED STALE DISTANCE',{ra:centerRa,dec:centerDec,fovXDegrees:safeFovX,fovYDegrees:safeFovY});
            return;
        }
        const key=gvEarthDistanceIdentity(nearest);
        // Destination-card distance formatting is shared by gvFormatEarthDistance.
        // Only switch the displayed value when the live-center galaxy changes.
        const matchedDistance=gvFormatEarthDistance(nearest);
        const selectionChanged=key!==gvEarthDistanceTargetKey||matchedDistance!==gvFormatEarthDistance(gvEarthDistanceTarget);
        gvShowEarthDistance(nearest,true);
        if(selectionChanged)console.info('GV0008 EARTH DISTANCE LIVE CENTER MATCH',{designation:nearest.designation||nearest.name||nearest.archiveId||nearest.id||'',ra:centerRa,dec:centerDec,matchedRa:Number(nearest.ra),matchedDec:Number(nearest.dec),separationDeg:nearestDeg,distanceMly:Number(nearest.distanceMly),fovXDegrees:fovX,fovYDegrees:fovY});
        gvEarthDistanceSyncLastError='';
    }catch(error){
        const message=String(error?.message||error);
        if(message!==gvEarthDistanceSyncLastError){console.warn('GV0130 EARTH DISTANCE COORDINATE SYNC FAILED',error);gvEarthDistanceSyncLastError=message}
    }finally{
        gvEarthDistanceSyncBusy=false;
        if(gvEarthDistanceSyncPending){
            gvEarthDistanceSyncPending=false;
            queueMicrotask(()=>{if(!gvNavigationTravelActive)gvSyncEarthDistanceToCenter()});
        }
    }
}
// The Earth-distance banner follows the nearest catalog target in Aladin's live center/FOV.
// Zoom and pan refresh the target match and physical ruler independently.
function gvInstallEarthDistanceInteractionListeners(){
    if(gvEarthDistanceInteractionListenersInstalled)return;
    const host=document.getElementById('aladin-cosmic-command-test');
    if(!host)return;
    gvEarthDistanceInteractionListenersInstalled=true;
    const isHdViewport=event=>!!event?.target?.closest?.('.gvdp-viewport');
    const userChangedView=event=>{
        if(gvNavigationTravelActive||isHdViewport(event))return;
        const type=String(event?.type||'');
        if(type==='touchstart'){
            gvEarthDistanceUserAdjustedView=true;
            gvEarthDistanceTouchGestureActive=true;
            if(gvEarthDistanceTouchSyncTimer){clearTimeout(gvEarthDistanceTouchSyncTimer);gvEarthDistanceTouchSyncTimer=0;}
            return;
        }
        if(type==='touchmove'){
            gvEarthDistanceUserAdjustedView=true;
            // Native Aladin pinch/pan is still in progress; defer center matching.
            gvEarthDistanceTouchGestureActive=true;
            return;
        }
        if(type==='touchend'||type==='touchcancel'){
            if(event?.touches?.length)return;
            gvEarthDistanceTouchGestureActive=false;
            if(gvEarthDistanceTouchSyncTimer)clearTimeout(gvEarthDistanceTouchSyncTimer);
            gvEarthDistanceTouchSyncTimer=setTimeout(()=>{
                gvEarthDistanceTouchSyncTimer=0;
                if(!gvNavigationTravelActive){
                    gvSyncEarthDistanceToCenter();
                    gvUpdateLivePhysicalScale();
                }
            },220);
            return;
        }
        const pointerGesture=type==='pointermove'&&Number(event?.buttons)>0;
        if(!pointerGesture&&type!=='wheel')return;
        gvEarthDistanceUserAdjustedView=true;
        gvSyncEarthDistanceToCenter();
        gvUpdateLivePhysicalScale();
    };
    // Capture at the sky root so canvas handlers cannot swallow gesture updates.
    // Touchmove is explicit for Android WebViews that do not deliver useful pointer moves.
    // HD gestures remain excluded and use their own independent transform/scale equation.
    const capturePassive={capture:true,passive:true};
    host.addEventListener('pointerdown',userChangedView,capturePassive);
    host.addEventListener('pointermove',userChangedView,capturePassive);
    host.addEventListener('pointerup',userChangedView,capturePassive);
    host.addEventListener('touchstart',userChangedView,capturePassive);
    host.addEventListener('touchmove',userChangedView,capturePassive);
    host.addEventListener('touchend',userChangedView,capturePassive);
    host.addEventListener('wheel',userChangedView,capturePassive);
}
// Update immediately on Aladin sky position/zoom events and poll every 100 ms.
// HD pan/pinch is intentionally isolated in the destination module.
try{aladin.on('positionChanged',()=>{if(gvZoomInteractionActive||gvNavigationTravelActive)return;gvSyncEarthDistanceToCenter()})}catch(error){console.warn('GV0005 EARTH POSITION EVENT REGISTRATION FAILED',error)}
try{aladin.on('zoomChanged',()=>{if(gvZoomInteractionActive||gvNavigationTravelActive)return;gvSyncEarthDistanceToCenter();gvUpdateLivePhysicalScale()})}catch(error){console.warn('GV0005 EARTH ZOOM EVENT REGISTRATION FAILED',error)}
// Install once; retain a lower-frequency center fallback only while visible.
gvInstallEarthDistanceInteractionListeners();
setInterval(()=>{if(document.visibilityState==='visible'&&!gvZoomInteractionActive&&!gvNavigationTravelActive)gvSyncEarthDistanceToCenter()},250);

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
// BLD 0121: all immutable module URLs are commit-pinned, so do not append
// cache-busting query strings. Start the complete module set in parallel so a
// cold CDN fetch for one module cannot serialize the entire boot sequence.
await gvModuleLoadPromise;
if(window.GVProviderArtwork?.VERSION!=='0007')throw new Error('PROVIDER ARTWORK 0007 EXPORT MISSING');


// ============================================================================
// SECTION 019 — REQUIRED MODULE EXPORT VALIDATION
// ECO: GV200-001
// ============================================================================
if(window.GalaxyViewerHamburgerMenu?.version!=='0012')throw new Error('HAMBURGER 0012 EXPORT MISSING');
if(window.GalaxyViewerConstellationOverlay?.VERSION!=='0020'||typeof window.GalaxyViewerConstellationOverlay.mount!=='function')throw new Error('CONSTELLATION OVERLAY 0020 EXPORT MISSING');
if(!window.GalaxyCoordinateOverlay||window.GalaxyCoordinateOverlay.VERSION!=='0008'||typeof window.GalaxyCoordinateOverlay.mount!=='function')throw new Error('COORDINATE OVERLAY 0008 EXPORT MISSING');
if(window.GalaxyViewerTargetSimbad?.version!=='0007')throw new Error('TARGET SURVEY 0007 EXPORT MISSING');
/* GV014: diagnostics intentionally not loaded. */
if(window.GalaxyRouteEngine?.VERSION!=='0002')throw new Error('GALAXY ROUTE ENGINE 002 EXPORT MISSING');
if(window.GalaxyNavigator?.VERSION!=='013'||typeof window.GalaxyNavigator.mount!=='function')throw new Error('GALAXY NAVIGATOR 013 EXPORT MISSING');

/* GV IAU CONSTELLATION REGION POLYGONS — BUILD 0042
 * Bundle pinned, closed IAU constellation polygon GeoJSON in the viewer: no runtime fetch/CORS dependency.
 * GeoJSON coordinates are sky longitude/latitude in degrees, longitude [-180,180].
 * Convert longitude to Aladin RA [0,360) only; do not apply a second precession.
 */
(function gvLoadIauConstellationRegions(){
  const GV_IAU_BOUNDARY_COLOR='#ff0000';
  const GV_IAU_BOUNDARY_WIDTH=0.5;
  const GV_IAU_BOUNDARY_OPACITY=0.58;
  const data=JSON.parse("{\"type\":\"FeatureCollection\",\"features\":[{\"type\":\"Feature\",\"id\":\"And\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-15.5347,35.1682],[-15.6571,53.168],[-8.5471,53.187],[-8.5343,50.687],[-4.7294,50.6929],[-4.7239,48.6929],[4.1464,48.6949],[4.1433,46.6949],[14.7761,46.6758],[14.7889,48.6757],[18.5884,48.6633],[18.6059,50.6632],[22.4079,50.6479],[26.9685,50.6257],[26.9314,47.6258],[32.6215,47.5928],[32.6738,51.0926],[39.8855,51.0424],[39.6793,37.2932],[31.8711,37.3471],[31.8543,35.5971],[22.9108,35.6453],[22.8974,33.6454],[12.4431,33.6819],[12.4135,24.4319],[14.4241,24.4266],[14.4148,21.6766],[3.7399,21.6952],[3.7406,22.6952],[2.61,22.6958],[2.6128,28.6958],[1.6062,28.696],[1.607,32.0294],[-2.1713,32.0285],[-2.1719,32.7785],[-5.9508,32.7746],[-5.9558,35.1913],[-15.5347,35.1682]]]}},{\"type\":\"Feature\",\"id\":\"Ant\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[141.9043,-24.5425],[141.7716,-37.292],[141.7341,-40.2919],[166.4565,-40.4246],[166.4794,-35.6747],[163.9585,-35.6665],[163.9779,-31.8332],[160.2014,-31.8186],[160.2129,-29.8186],[155.1813,-29.7948],[155.1993,-27.1282],[147.6593,-27.0835],[147.6797,-24.5836],[141.9043,-24.5425]]]}},{\"type\":\"Feature\",\"id\":\"Aps\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-150.8889,-83.1201],[-83.134,-82.4583],[-85.8049,-74.9745],[-86.7199,-67.4801],[-94.2243,-67.5711],[-101.7575,-67.6611],[-101.5293,-70.1597],[-135.8336,-70.5115],[-152.5391,-70.6244],[-152.2186,-75.6236],[-150.8889,-83.1201]]]}},{\"type\":\"Feature\",\"id\":\"Aqr\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-50.4012,0.4362],[-50.4201,2.4361],[-45.9189,2.4773],[-38.4165,2.5394],[-36.4157,2.5544],[-36.4213,3.3044],[-33.4198,3.3257],[-33.4129,2.3257],[-28.4112,2.3576],[-28.4127,2.6076],[-17.1578,2.6622],[-17.1503,0.6622],[-17.1353,-3.3378],[-0.8978,-3.3042],[-0.8967,-6.3042],[-0.8894,-24.8042],[-13.319,-24.825],[-30.2297,-24.904],[-30.3438,-8.4044],[-38.3316,-8.4603],[-38.2835,-14.4601],[-50.2561,-14.5631],[-50.3154,-8.5634],[-50.4012,0.4362]]]}},{\"type\":\"Feature\",\"id\":\"Aql\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-79.6498,0.1155],[-79.6738,2.1153],[-75.4236,2.1659],[-75.474,6.4156],[-78.5414,6.3792],[-78.612,12.1288],[-75.5437,12.1652],[-75.6264,18.6647],[-73.6245,18.6882],[-73.5945,16.3551],[-61.0788,16.4957],[-61.074,16.0791],[-56.441,16.1275],[-56.3633,8.8779],[-53.986,8.9018],[-53.9209,2.4021],[-50.4201,2.4361],[-50.4012,0.4362],[-50.3154,-8.5634],[-58.3063,-8.6431],[-58.2736,-11.6762],[-75.2559,-11.8664],[-75.3527,-3.8337],[-79.6018,-3.8842],[-79.6498,0.1155]]]}},{\"type\":\"Feature\",\"id\":\"Ara\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-110.9653,-60.2645],[-111.4294,-45.7671],[-90.1907,-45.5163],[-87.691,-45.486],[-87.3277,-56.9838],[-94.8318,-57.0748],[-94.2243,-67.5711],[-101.7575,-67.6611],[-104.275,-67.6906],[-104.4576,-65.1916],[-105.7165,-65.2063],[-105.8049,-63.7901],[-108.3237,-63.819],[-108.4622,-61.2365],[-110.9184,-61.2642],[-110.9653,-60.2645]]]}},{\"type\":\"Feature\",\"id\":\"Ari\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[31.6652,10.5144],[26.6557,10.5432],[26.7447,25.6263],[30.5137,25.6051],[30.5306,27.855],[38.0701,27.8048],[38.1032,31.2213],[42.6284,31.1865],[52.4267,31.1004],[52.2906,19.4343],[51.0372,19.4461],[50.9464,10.3632],[31.6652,10.5144]]]}},{\"type\":\"Feature\",\"id\":\"Aur\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[69.4869,30.9219],[69.5738,36.2547],[72.4573,36.2219],[72.8403,52.7196],[77.4848,52.6656],[77.6068,56.1648],[94.1311,55.9658],[94.0574,53.9663],[100.046,53.8938],[99.9195,49.8946],[104.4064,49.841],[104.2653,44.3418],[112.7341,44.2435],[112.5607,35.2445],[100.0903,35.3906],[99.9657,27.8913],[90.2211,28.0093],[90.2289,28.5092],[73.2125,28.7124],[73.2353,30.2123],[69.4768,30.2553],[69.4869,30.9219]]]}},{\"type\":\"Feature\",\"id\":\"Boo\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-132.2185,7.5254],[-155.9362,7.3606],[-155.9711,14.3605],[-156.0461,27.8603],[-149.2112,27.8977],[-149.2291,30.1476],[-148.1111,30.1545],[-148.3013,47.9039],[-148.4156,54.9036],[-142.7488,54.9422],[-130.4089,55.0449],[-130.3426,52.5452],[-122.9155,52.6175],[-122.8754,51.1177],[-122.6346,39.6189],[-127.3563,39.5721],[-127.253,32.5726],[-130.9841,32.5377],[-130.9005,25.5381],[-132.3945,25.5246],[-132.2185,7.5254]]]}},{\"type\":\"Feature\",\"id\":\"Cae\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[65.0764,-39.7007],[64.8824,-48.6997],[68.3622,-48.7384],[68.4241,-46.2388],[73.4021,-46.2959],[73.4824,-42.7964],[75.9744,-42.8256],[76.2549,-27.0772],[73.7593,-27.048],[71.7633,-27.0249],[71.7224,-29.7746],[69.9767,-29.7547],[69.8624,-36.754],[65.1299,-36.701],[65.0764,-39.7007]]]}},{\"type\":\"Feature\",\"id\":\"Cam\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[94.1311,55.9658],[77.6068,56.1648],[77.4848,52.6656],[72.8403,52.7196],[52.3131,52.9366],[52.3819,55.4363],[49.854,55.4597],[49.9135,57.4594],[48.9009,57.4685],[49.3955,68.4663],[54.237,68.4214],[55.3087,77.4163],[56.7262,77.4026],[57.5305,80.3987],[80.4889,80.1479],[84.5361,85.1239],[127.9536,84.6104],[130.4028,86.0975],[-146.977,85.9308],[-143.2171,79.445],[-156.1908,79.3629],[-155.843,76.3638],[-164.1794,76.3289],[174.4348,76.3084],[174.5316,79.3083],[162.8186,79.3402],[163.1054,81.3396],[142.1912,81.4678],[140.6155,72.9741],[123.0862,73.1384],[122.1291,59.6434],[107.7532,59.8037],[107.8516,61.8031],[94.4075,61.9641],[94.1311,55.9658]]]}},{\"type\":\"Feature\",\"id\":\"Cnc\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[140.4043,6.4701],[122.9214,6.6302],[120.5483,6.655],[120.5807,9.6548],[118.8325,9.6734],[118.8716,13.1732],[118.9475,19.6728],[120.0701,19.6608],[120.1716,27.6603],[121.916,27.6419],[121.9932,33.1415],[140.646,32.9691],[140.4043,6.4701]]]}},{\"type\":\"Feature\",\"id\":\"CVn\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-178.4055,33.304],[-178.4086,44.304],[-177.1736,44.3043],[-177.1815,52.3043],[-156.2576,52.3598],[-156.2049,47.8599],[-148.3013,47.9039],[-148.1111,30.1545],[-149.2291,30.1476],[-149.2112,27.8977],[-156.0461,27.8603],[-159.7734,27.8438],[-159.7923,31.3437],[-173.4423,31.3074],[-173.4457,33.3074],[-178.4055,33.304]]]}},{\"type\":\"Feature\",\"id\":\"CMa\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[93.2156,-11.0302],[111.9734,-11.2521],[111.6772,-33.2505],[99.9039,-33.1128],[92.8991,-33.0282],[92.9926,-27.2788],[93.2156,-11.0302]]]}},{\"type\":\"Feature\",\"id\":\"CMi\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[122.849,-0.3694],[109.5997,-0.2243],[109.6169,1.2756],[106.8674,1.3074],[106.9143,5.3072],[106.6643,5.3101],[106.7179,9.8098],[106.7482,12.3096],[114.241,12.2239],[114.2527,13.2238],[118.8716,13.1732],[118.8325,9.6734],[120.5807,9.6548],[120.5483,6.655],[122.9214,6.6302],[122.849,-0.3694]]]}},{\"type\":\"Feature\",\"id\":\"Cap\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-50.3154,-8.5634],[-58.3063,-8.6431],[-58.2736,-11.6762],[-58.084,-27.6419],[-53.102,-27.5913],[-38.1684,-27.4597],[-38.1922,-24.9598],[-30.2297,-24.904],[-30.3438,-8.4044],[-38.3316,-8.4603],[-38.2835,-14.4601],[-50.2561,-14.5631],[-50.3154,-8.5634]]]}},{\"type\":\"Feature\",\"id\":\"Car\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[170.1559,-57.1843],[166.3373,-57.1744],[133.3237,-56.974],[133.3802,-54.9742],[127.5671,-54.9205],[127.6093,-53.4207],[123.3201,-53.3782],[123.3811,-51.1285],[120.8617,-51.1026],[90.7489,-50.7545],[90.6937,-52.5042],[93.1944,-52.5346],[93.1074,-55.034],[98.1143,-55.0946],[97.9951,-58.0938],[103.0111,-58.1537],[102.7033,-64.1519],[136.0947,-64.499],[135.2437,-75.4955],[169.857,-75.684],[170.0848,-64.6843],[170.1559,-57.1843]]]}},{\"type\":\"Feature\",\"id\":\"Cas\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-15.6571,53.168],[-15.696,56.918],[-15.7309,59.7512],[-11.1403,59.7647],[-11.1835,63.6813],[-4.7824,63.6929],[-4.8021,66.6929],[6.7638,66.6924],[6.9229,77.6923],[55.3087,77.4163],[54.237,68.4214],[49.3955,68.4663],[48.9009,57.4685],[38.7623,57.5513],[38.8024,59.0512],[30.7956,59.1046],[30.7736,58.1047],[27.5952,58.1227],[27.5336,54.6229],[22.456,54.6478],[22.4079,50.6479],[18.6059,50.6632],[18.5884,48.6633],[14.7889,48.6757],[14.7761,46.6758],[4.1433,46.6949],[4.1464,48.6949],[-4.7239,48.6929],[-4.7294,50.6929],[-8.5343,50.687],[-8.5471,53.187],[-15.6571,53.168]]]}},{\"type\":\"Feature\",\"id\":\"Cen\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[166.4794,-35.6747],[166.4565,-40.4246],[166.3373,-57.1744],[170.1559,-57.1843],[170.0848,-64.6843],[179.0574,-64.6958],[179.0708,-55.6958],[-165.6655,-55.6771],[-165.5616,-64.677],[-155.3197,-64.6379],[-139.485,-64.539],[-139.7655,-55.5401],[-145.3432,-55.58],[-145.5497,-42.5806],[-134.2037,-42.4942],[-134.3692,-29.9949],[-169.5826,-30.1864],[-169.5728,-33.6864],[-174.6126,-33.6939],[-174.6097,-35.6939],[166.4794,-35.6747]]]}},{\"type\":\"Feature\",\"id\":\"Cep\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-59.4267,59.8511],[-59.5148,61.8506],[-53.1881,61.9144],[-53.4826,67.413],[-49.666,67.449],[-50.427,75.4455],[-58.1266,75.3709],[-59.3262,80.3648],[-46.2941,80.4868],[-51.279,86.4656],[-51.6686,86.6306],[-16.4893,86.8369],[-20.739,88.6639],[0.9483,88.6092],[24.7077,88.3564],[57.6647,88.0063],[135.8325,87.5689],[130.4028,86.0975],[127.9536,84.6104],[84.5361,85.1239],[80.4889,80.1479],[57.5305,80.3987],[56.7262,77.4026],[55.3087,77.4163],[6.9229,77.6923],[6.7638,66.6924],[-4.8021,66.6929],[-4.7824,63.6929],[-11.1835,63.6813],[-11.1403,59.7647],[-15.7309,59.7512],[-15.696,56.918],[-24.0891,56.8826],[-24.0687,55.6326],[-26.8624,55.6178],[-26.8253,53.3679],[-29.3608,53.3533],[-29.3978,55.4365],[-50.1686,55.2753],[-50.3762,61.3577],[-51.3392,61.3486],[-51.2834,59.9322],[-59.4267,59.8511]]]}},{\"type\":\"Feature\",\"id\":\"Cet\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[6.6013,0.6925],[6.6038,2.6925],[31.6153,2.5979],[31.6652,10.5144],[50.9464,10.3632],[50.853,0.447],[50.8367,-1.303],[41.3392,-1.221],[41.1488,-23.8536],[26.466,-23.7563],[26.4589,-24.8729],[-0.8894,-24.8042],[-0.8967,-6.3042],[6.5927,-6.3075],[6.6013,0.6925]]]}},{\"type\":\"Feature\",\"id\":\"Cha\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[111.6521,-82.7759],[-150.8889,-83.1201],[-152.2186,-75.6236],[169.857,-75.684],[135.2437,-75.4955],[114.2147,-75.2899],[111.6521,-82.7759]]]}},{\"type\":\"Feature\",\"id\":\"Cir\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-155.3197,-64.6379],[-155.2925,-65.6379],[-152.732,-65.625],[-152.5391,-70.6244],[-135.8336,-70.5115],[-135.9964,-68.0122],[-133.4429,-67.9909],[-133.6465,-64.0751],[-129.8334,-64.0416],[-129.9454,-61.4587],[-127.4102,-61.4353],[-127.4501,-60.4355],[-127.6181,-55.4363],[-131.9165,-55.4755],[-139.7655,-55.5401],[-139.485,-64.539],[-155.3197,-64.6379]]]}},{\"type\":\"Feature\",\"id\":\"Col\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[75.9744,-42.8256],[76.2549,-27.0772],[92.9926,-27.2788],[92.8991,-33.0282],[99.9039,-33.1128],[99.7089,-43.1116],[90.9518,-43.0058],[75.9744,-42.8256]]]}},{\"type\":\"Feature\",\"id\":\"Com\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[179.6045,13.304],[179.6089,28.304],[-178.4043,28.304],[-178.4055,33.304],[-173.4457,33.3074],[-173.4423,31.3074],[-159.7923,31.3437],[-159.7734,27.8438],[-156.0461,27.8603],[-155.9711,14.3605],[-165.9409,14.3225],[-165.938,13.3225],[179.6045,13.304]]]}},{\"type\":\"Feature\",\"id\":\"CrA\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-90.3745,-37.0175],[-70.4037,-36.7786],[-70.2304,-45.2776],[-87.691,-45.486],[-90.1907,-45.5163],[-90.3745,-37.0175]]]}},{\"type\":\"Feature\",\"id\":\"CrB\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-130.9005,25.5381],[-130.9841,32.5377],[-127.253,32.5726],[-127.3563,39.5721],[-122.6346,39.6189],[-113.9281,39.7117],[-113.7202,26.7129],[-116.2133,26.6855],[-116.1998,25.6856],[-118.1943,25.6641],[-130.9005,25.5381]]]}},{\"type\":\"Feature\",\"id\":\"Crv\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-165.8669,-11.6774],[179.0968,-11.6958],[179.0913,-25.1958],[-169.5955,-25.1864],[-169.6015,-22.6864],[-165.8331,-22.6773],[-165.8669,-11.6774]]]}},{\"type\":\"Feature\",\"id\":\"Crt\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[162.8271,-6.6622],[162.8079,-11.6621],[162.7755,-19.6621],[164.0306,-19.6666],[164.0081,-25.1666],[179.0913,-25.1958],[179.0968,-11.6958],[179.0986,-6.6958],[174.3423,-6.6917],[162.8271,-6.6622]]]}},{\"type\":\"Feature\",\"id\":\"Cru\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[179.0708,-55.6958],[179.0574,-64.6958],[-165.5616,-64.677],[-165.6655,-55.6771],[179.0708,-55.6958]]]}},{\"type\":\"Feature\",\"id\":\"Cyg\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-69.8674,27.7324],[-69.9047,30.2322],[-68.4012,30.2493],[-68.5074,36.7487],[-67.8803,36.7558],[-68.0165,43.755],[-71.5297,43.7149],[-71.6245,47.7144],[-72.8794,47.6999],[-73.1235,55.6984],[-68.0954,55.756],[-68.1904,58.2555],[-62.8994,58.3139],[-62.9608,59.8135],[-59.4267,59.8511],[-51.2834,59.9322],[-51.3392,61.3486],[-50.3762,61.3577],[-50.1686,55.2753],[-29.3978,55.4365],[-29.3608,53.3533],[-29.2373,44.6036],[-30.1214,44.5983],[-30.1184,44.3483],[-30.6234,44.3451],[-30.539,36.5954],[-32.68,36.5815],[-32.6048,28.5818],[-37.3798,28.5481],[-44.9161,28.4872],[-44.9274,29.4871],[-63.7491,29.3011],[-63.7278,27.8012],[-69.8674,27.7324]]]}},{\"type\":\"Feature\",\"id\":\"Del\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-50.4201,2.4361],[-53.9209,2.4021],[-53.986,8.9018],[-56.3633,8.8779],[-56.441,16.1275],[-54.8131,16.144],[-54.866,20.8937],[-50.1031,20.9399],[-50.0923,19.94],[-42.8212,20.0046],[-42.7516,12.3383],[-45.3814,12.3158],[-45.3289,6.4827],[-45.9545,6.4772],[-45.9189,2.4773],[-50.4201,2.4361]]]}},{\"type\":\"Feature\",\"id\":\"Dor\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[58.3188,-52.7968],[60.7979,-52.8228],[60.6929,-56.1556],[65.6505,-56.2094],[65.5546,-58.7089],[69.2745,-58.7507],[68.794,-67.2479],[68.5815,-69.7467],[98.4544,-70.1041],[98.9372,-64.107],[90.1736,-64.0011],[90.3451,-61.0021],[82.8576,-60.9113],[83.0188,-57.4123],[75.5477,-57.323],[75.677,-53.8238],[68.2177,-53.7376],[68.3622,-48.7384],[64.8824,-48.6997],[62.1499,-48.67],[62.0986,-50.6697],[58.3772,-50.6305],[58.3188,-52.7968]]]}},{\"type\":\"Feature\",\"id\":\"Dra\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[140.6155,72.9741],[142.1912,81.4678],[163.1054,81.3396],[162.8186,79.3402],[174.5316,79.3083],[174.4348,76.3084],[-164.1794,76.3289],[-163.9025,69.3294],[-149.3492,69.3991],[-149.1794,65.3997],[-124.6704,65.6023],[-124.9494,69.6009],[-112.1589,69.7383],[-112.7793,74.7348],[-98.4634,74.9033],[-99.7821,79.8953],[-92.344,79.9857],[-98.2778,85.9496],[-51.279,86.4656],[-46.2941,80.4868],[-59.3262,80.3648],[-58.1266,75.3709],[-50.427,75.4455],[-49.666,67.449],[-53.4826,67.413],[-53.1881,61.9144],[-59.5148,61.8506],[-59.4267,59.8511],[-62.9608,59.8135],[-62.8994,58.3139],[-68.1904,58.2555],[-68.0954,55.756],[-73.1235,55.6984],[-72.8794,47.6999],[-85.6576,47.5476],[-85.7423,50.5471],[-104.2136,50.3244],[-104.2432,51.3243],[-122.8754,51.1177],[-122.9155,52.6175],[-130.3426,52.5452],[-130.4089,55.0449],[-142.7488,54.9422],[-142.9547,62.4415],[-156.4264,62.3594],[-156.4495,63.3593],[-178.4184,63.304],[-178.4207,65.804],[171.8493,65.8126],[171.9614,72.8125],[140.6155,72.9741]]]}},{\"type\":\"Feature\",\"id\":\"Equ\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-45.9189,2.4773],[-45.9545,6.4772],[-45.3289,6.4827],[-45.3814,12.3158],[-42.7516,12.3383],[-41.7497,12.3466],[-41.7555,13.0132],[-38.4989,13.0391],[-38.4165,2.5394],[-45.9189,2.4773]]]}},{\"type\":\"Feature\",\"id\":\"Eri\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[55.3529,0.4037],[70.8524,0.2375],[71.6023,0.2289],[71.5564,-3.7708],[77.8044,-3.8437],[77.72,-10.8432],[75.2218,-10.8138],[75.1787,-14.3136],[73.9298,-14.299],[73.7593,-27.048],[71.7633,-27.0249],[71.7224,-29.7746],[69.9767,-29.7547],[69.8624,-36.754],[65.1299,-36.701],[65.0764,-39.7007],[59.1059,-39.6368],[59.0314,-43.6364],[52.3268,-43.5694],[52.289,-45.5692],[46.0908,-45.5125],[46.0345,-48.5122],[41.0853,-48.471],[41.0477,-50.4709],[37.3412,-50.4426],[37.2833,-53.4424],[33.5841,-53.4165],[33.4894,-57.9162],[21.2062,-57.8484],[21.2733,-52.8486],[24.9674,-52.8659],[24.9938,-50.8659],[28.6933,-50.8859],[28.7383,-47.5527],[36.1529,-47.6005],[36.264,-39.4342],[46.1873,-39.5129],[46.1933,-39.0963],[53.6443,-39.1651],[53.6996,-35.582],[57.4305,-35.6192],[57.5889,-24.0034],[41.1488,-23.8536],[41.3392,-1.221],[50.8367,-1.303],[55.3356,-1.3462],[55.3529,0.4037]]]}},{\"type\":\"Feature\",\"id\":\"For\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[26.466,-23.7563],[41.1488,-23.8536],[57.5889,-24.0034],[57.4305,-35.6192],[53.6996,-35.582],[53.6443,-39.1651],[46.1933,-39.0963],[46.1873,-39.5129],[36.264,-39.4342],[26.3507,-39.3726],[26.4589,-24.8729],[26.466,-23.7563]]]}},{\"type\":\"Feature\",\"id\":\"Gem\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[96.3728,11.9333],[96.4439,17.4329],[95.0696,17.4495],[95.1241,21.4492],[90.1252,21.5099],[90.144,22.8431],[90.2211,28.0093],[99.9657,27.8913],[100.0903,35.3906],[112.5607,35.2445],[118.2897,35.1811],[118.2581,33.1812],[121.9932,33.1415],[121.916,27.6419],[120.1716,27.6603],[120.0701,19.6608],[118.9475,19.6728],[118.8716,13.1732],[114.2527,13.2238],[114.241,12.2239],[106.7482,12.3096],[106.7179,9.8098],[105.7185,9.8215],[105.7428,11.8213],[96.3728,11.9333]]]}},{\"type\":\"Feature\",\"id\":\"Gru\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-38.0719,-36.4593],[-37.9577,-44.9589],[-37.8826,-49.4586],[-28.0012,-49.3912],[-27.8863,-56.3908],[-8.2315,-56.3127],[-8.3073,-39.3128],[-8.3166,-36.3128],[-13.2725,-36.325],[-38.0719,-36.4593]]]}},{\"type\":\"Feature\",\"id\":\"Her\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-114.4414,3.7034],[-117.1903,3.6735],[-117.3234,15.6728],[-119.8189,15.6463],[-119.889,21.646],[-118.1434,21.6644],[-118.1943,25.6641],[-116.1998,25.6856],[-116.2133,26.6855],[-113.7202,26.7129],[-113.9281,39.7117],[-122.6346,39.6189],[-122.8754,51.1177],[-104.2432,51.3243],[-104.2136,50.3244],[-85.7423,50.5471],[-85.6576,47.5476],[-86.5331,47.537],[-86.1756,30.0392],[-83.2992,30.074],[-83.2371,26.0744],[-75.7301,26.1641],[-75.7228,25.6641],[-75.6609,21.2478],[-75.6264,18.6647],[-75.5437,12.1652],[-78.612,12.1288],[-84.7969,12.0543],[-84.8267,14.3875],[-99.8231,14.206],[-99.8042,12.7061],[-107.2985,12.6179],[-107.1941,3.7852],[-114.4414,3.7034]]]}},{\"type\":\"Feature\",\"id\":\"Hor\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[65.0764,-39.7007],[64.8824,-48.6997],[62.1499,-48.67],[62.0986,-50.6697],[58.3772,-50.6305],[58.3188,-52.7968],[53.365,-52.7471],[53.2368,-57.0798],[48.7911,-57.0378],[48.3627,-67.0358],[33.2024,-66.9152],[33.4894,-57.9162],[33.5841,-53.4165],[37.2833,-53.4424],[37.3412,-50.4426],[41.0477,-50.4709],[41.0853,-48.471],[46.0345,-48.5122],[46.0908,-45.5125],[52.289,-45.5692],[52.3268,-43.5694],[59.0314,-43.6364],[59.1059,-39.6368],[65.0764,-39.7007]]]}},{\"type\":\"Feature\",\"id\":\"Hya\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[122.849,-0.3694],[122.9214,6.6302],[140.4043,6.4701],[145.3984,6.4328],[145.3489,-0.5671],[145.2703,-11.5668],[162.8079,-11.6621],[162.7755,-19.6621],[164.0306,-19.6666],[164.0081,-25.1666],[179.0913,-25.1958],[-169.5955,-25.1864],[-169.6015,-22.6864],[-165.8331,-22.6773],[-144.4869,-22.5728],[-144.4663,-25.0727],[-134.4234,-24.9951],[-134.3692,-29.9949],[-169.5826,-30.1864],[-169.5728,-33.6864],[-174.6126,-33.6939],[-174.6097,-35.6939],[166.4794,-35.6747],[163.9585,-35.6665],[163.9779,-31.8332],[160.2014,-31.8186],[160.2129,-29.8186],[155.1813,-29.7948],[155.1993,-27.1282],[147.6593,-27.0835],[147.6797,-24.5836],[141.9043,-24.5425],[137.6368,-24.5086],[137.685,-19.5088],[130.1635,-19.4424],[130.1843,-17.4425],[126.9271,-17.4113],[126.9898,-11.4116],[122.7342,-11.3688],[122.849,-0.3694]]]}},{\"type\":\"Feature\",\"id\":\"Hyi\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[68.794,-67.2479],[68.5815,-69.7467],[67.9575,-74.7432],[52.0758,-74.5741],[50.0917,-82.0645],[1.5334,-81.804],[1.5663,-74.304],[12.3324,-74.3186],[12.2954,-75.3185],[20.6541,-75.3472],[21.2062,-57.8484],[33.4894,-57.9162],[33.2024,-66.9152],[48.3627,-67.0358],[68.794,-67.2479]]]}},{\"type\":\"Feature\",\"id\":\"Ind\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-36.8152,-74.4545],[-8.0022,-74.3125],[-8.1386,-66.8126],[-27.6014,-66.89],[-27.8863,-56.3908],[-28.0012,-49.3912],[-37.8826,-49.4586],[-37.9577,-44.9589],[-52.8307,-45.09],[-52.5412,-56.5886],[-52.4352,-59.5881],[-37.6513,-59.4577],[-36.8152,-74.4545]]]}},{\"type\":\"Feature\",\"id\":\"Lac\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-30.539,36.5954],[-30.6234,44.3451],[-30.1184,44.3483],[-30.1214,44.5983],[-29.2373,44.6036],[-29.3608,53.3533],[-26.8253,53.3679],[-26.8624,55.6178],[-24.0687,55.6326],[-24.0891,56.8826],[-15.696,56.918],[-15.6571,53.168],[-15.5347,35.1682],[-16.2908,35.1656],[-16.2935,35.6656],[-28.6404,35.6069],[-28.6495,36.6069],[-30.539,36.5954]]]}},{\"type\":\"Feature\",\"id\":\"Leo\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[162.8497,-0.6622],[162.876,6.3377],[145.3984,6.4328],[140.4043,6.4701],[140.646,32.9691],[150.0844,32.9023],[150.0423,27.9024],[159.2384,27.8529],[159.2109,22.853],[162.9425,22.8376],[162.9515,24.8376],[166.6809,24.825],[166.694,28.325],[179.6089,28.304],[179.6045,13.304],[179.6037,10.304],[174.3657,10.3083],[174.3505,-0.6917],[174.3423,-6.6917],[162.8271,-6.6622],[162.8497,-0.6622]]]}},{\"type\":\"Feature\",\"id\":\"LMi\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[140.646,32.9691],[140.7216,39.2188],[145.682,39.1818],[145.7092,41.4317],[154.3782,41.3774],[154.3594,39.3774],[163.5232,39.3356],[163.4894,33.3357],[166.7142,33.325],[166.694,28.325],[166.6809,24.825],[162.9515,24.8376],[162.9425,22.8376],[159.2109,22.853],[159.2384,27.8529],[150.0423,27.9024],[150.0844,32.9023],[140.646,32.9691]]]}},{\"type\":\"Feature\",\"id\":\"Lep\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[73.7593,-27.048],[76.2549,-27.0772],[92.9926,-27.2788],[93.2156,-11.0302],[88.9658,-10.9785],[77.72,-10.8432],[75.2218,-10.8138],[75.1787,-14.3136],[73.9298,-14.299],[73.7593,-27.048]]]}},{\"type\":\"Feature\",\"id\":\"Lib\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-132.147,-0.4743],[-138.3969,-0.5269],[-138.3329,-8.5267],[-144.5915,-8.5731],[-144.4869,-22.5728],[-144.4663,-25.0727],[-134.4234,-24.9951],[-134.3692,-29.9949],[-123.07,-29.8896],[-123.1869,-20.3902],[-119.4282,-20.3516],[-119.5627,-8.3523],[-119.613,-3.6026],[-132.118,-3.7242],[-132.147,-0.4743]]]}},{\"type\":\"Feature\",\"id\":\"Lup\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-145.3432,-55.58],[-139.7655,-55.5401],[-131.9165,-55.4755],[-131.9433,-54.4756],[-127.6466,-54.4364],[-127.7928,-48.4371],[-122.7527,-48.388],[-122.8754,-42.3886],[-117.8472,-42.3367],[-118.0523,-29.8378],[-123.07,-29.8896],[-134.3692,-29.9949],[-134.2037,-42.4942],[-145.5497,-42.5806],[-145.3432,-55.58]]]}},{\"type\":\"Feature\",\"id\":\"Lyn\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[112.5607,35.2445],[112.7341,44.2435],[104.2653,44.3418],[104.4064,49.841],[99.9195,49.8946],[100.046,53.8938],[94.0574,53.9663],[94.1311,55.9658],[94.4075,61.9641],[107.8516,61.8031],[107.7532,59.8037],[122.1291,59.6434],[128.7991,59.576],[128.4401,46.5777],[139.5907,46.4783],[139.5125,41.4786],[145.7092,41.4317],[145.682,39.1818],[140.7216,39.2188],[140.646,32.9691],[121.9932,33.1415],[118.2581,33.1812],[118.2897,35.1811],[112.5607,35.2445]]]}},{\"type\":\"Feature\",\"id\":\"Lyr\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-75.7228,25.6641],[-75.7301,26.1641],[-83.2371,26.0744],[-83.2992,30.074],[-86.1756,30.0392],[-86.5331,47.537],[-85.6576,47.5476],[-72.8794,47.6999],[-71.6245,47.7144],[-71.5297,43.7149],[-68.0165,43.755],[-67.8803,36.7558],[-68.5074,36.7487],[-68.4012,30.2493],[-69.9047,30.2322],[-69.8674,27.7324],[-69.8387,25.7326],[-75.7228,25.6641]]]}},{\"type\":\"Feature\",\"id\":\"Men\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[109.0197,-85.2614],[48.2329,-84.5554],[50.0917,-82.0645],[52.0758,-74.5741],[67.9575,-74.7432],[68.5815,-69.7467],[98.4544,-70.1041],[97.7707,-75.1],[114.2147,-75.2899],[111.6521,-82.7759],[109.0197,-85.2614]]]}},{\"type\":\"Feature\",\"id\":\"Mic\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-53.102,-27.5913],[-38.1684,-27.4597],[-38.0719,-36.4593],[-37.9577,-44.9589],[-52.8307,-45.09],[-53.102,-27.5913]]]}},{\"type\":\"Feature\",\"id\":\"Mon\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[95.2257,-0.0537],[95.348,9.9455],[96.3477,9.9334],[96.3728,11.9333],[105.7428,11.8213],[105.7185,9.8215],[106.7179,9.8098],[106.6643,5.3101],[106.9143,5.3072],[106.8674,1.3074],[109.6169,1.2756],[109.5997,-0.2243],[122.849,-0.3694],[122.7342,-11.3688],[111.9734,-11.2521],[93.2156,-11.0302],[88.9658,-10.9785],[89.0524,-3.9791],[95.1771,-4.0534],[95.2257,-0.0537]]]}},{\"type\":\"Feature\",\"id\":\"Mus\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[170.0848,-64.6843],[169.857,-75.684],[-152.2186,-75.6236],[-152.5391,-70.6244],[-152.732,-65.625],[-155.2925,-65.6379],[-155.3197,-64.6379],[-165.5616,-64.677],[179.0574,-64.6958],[170.0848,-64.6843]]]}},{\"type\":\"Feature\",\"id\":\"Nor\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-127.4501,-60.4355],[-110.9653,-60.2645],[-111.4294,-45.7671],[-111.5052,-42.2675],[-117.8472,-42.3367],[-122.8754,-42.3886],[-122.7527,-48.388],[-127.7928,-48.4371],[-127.6466,-54.4364],[-131.9433,-54.4756],[-131.9165,-55.4755],[-127.6181,-55.4363],[-127.4501,-60.4355]]]}},{\"type\":\"Feature\",\"id\":\"Oct\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[1.5334,-81.804],[50.0917,-82.0645],[48.2329,-84.5554],[109.0197,-85.2614],[111.6521,-82.7759],[-150.8889,-83.1201],[-83.134,-82.4583],[-85.8049,-74.9745],[-36.8152,-74.4545],[-8.0022,-74.3125],[1.5663,-74.304],[1.5334,-81.804]]]}},{\"type\":\"Feature\",\"id\":\"Oph\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-114.3974,-0.2964],[-114.4414,3.7034],[-107.1941,3.7852],[-107.2985,12.6179],[-99.8042,12.7061],[-99.8231,14.206],[-84.8267,14.3875],[-84.7969,12.0543],[-78.612,12.1288],[-78.5414,6.3792],[-84.7254,6.3048],[-84.704,4.5549],[-82.0789,4.5866],[-82.0608,3.0867],[-84.6858,3.055],[-84.6494,0.0552],[-90.899,-0.0206],[-90.8503,-4.0204],[-88.8503,-3.9961],[-88.7763,-9.9956],[-93.2762,-10.0502],[-93.2553,-11.7168],[-94.5056,-11.7319],[-94.5265,-10.0654],[-100.7779,-10.1404],[-100.7026,-16.14],[-94.1998,-16.0619],[-93.9982,-30.0607],[-106.7647,-30.2123],[-106.8443,-24.7961],[-114.1086,-24.8781],[-114.177,-19.5452],[-112.5493,-19.5272],[-112.5618,-18.5272],[-114.1893,-18.5452],[-114.3088,-8.2959],[-119.5627,-8.3523],[-119.613,-3.6026],[-114.3616,-3.5462],[-114.3974,-0.2964]]]}},{\"type\":\"Feature\",\"id\":\"Ori\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[70.8524,0.2375],[71.034,15.7365],[76.2889,15.6755],[76.2953,16.1755],[81.7987,16.1101],[81.7922,15.6101],[85.7936,15.5619],[85.7551,12.5622],[88.2554,12.5319],[88.3272,18.0314],[87.327,18.0435],[87.3938,22.8765],[90.144,22.8431],[90.1252,21.5099],[95.1241,21.4492],[95.0696,17.4495],[96.4439,17.4329],[96.3728,11.9333],[96.3477,9.9334],[95.348,9.9455],[95.2257,-0.0537],[95.1771,-4.0534],[89.0524,-3.9791],[88.9658,-10.9785],[77.72,-10.8432],[77.8044,-3.8437],[71.5564,-3.7708],[71.6023,0.2289],[70.8524,0.2375]]]}},{\"type\":\"Feature\",\"id\":\"Pav\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-85.8049,-74.9745],[-36.8152,-74.4545],[-37.6513,-59.4577],[-52.4352,-59.5881],[-52.5412,-56.5886],[-87.3277,-56.9838],[-94.8318,-57.0748],[-94.2243,-67.5711],[-86.7199,-67.4801],[-85.8049,-74.9745]]]}},{\"type\":\"Feature\",\"id\":\"Peg\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-38.4165,2.5394],[-38.4989,13.0391],[-41.7555,13.0132],[-41.7497,12.3466],[-42.7516,12.3383],[-42.8212,20.0046],[-39.8116,20.0291],[-39.8483,24.0289],[-37.338,24.0482],[-37.3798,28.5481],[-32.6048,28.5818],[-32.68,36.5815],[-30.539,36.5954],[-28.6495,36.6069],[-28.6404,35.6069],[-16.2935,35.6656],[-16.2908,35.1656],[-15.5347,35.1682],[-5.9558,35.1913],[-5.9508,32.7746],[-2.1719,32.7785],[-2.1713,32.0285],[1.607,32.0294],[1.6062,28.696],[2.6128,28.6958],[2.61,22.6958],[3.7406,22.6952],[3.7399,21.6952],[3.7341,13.1952],[1.6032,13.196],[1.6027,10.696],[-0.9029,10.6958],[-0.902,8.1958],[-17.1786,8.1622],[-17.1578,2.6622],[-28.4127,2.6076],[-28.4112,2.3576],[-33.4129,2.3257],[-33.4198,3.3257],[-36.4213,3.3044],[-36.4157,2.5544],[-38.4165,2.5394]]]}},{\"type\":\"Feature\",\"id\":\"Per\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[42.6284,31.1865],[42.6665,34.5197],[40.4024,34.5375],[40.4347,37.2874],[39.6793,37.2932],[39.8855,51.0424],[32.6738,51.0926],[32.6215,47.5928],[26.9314,47.6258],[26.9685,50.6257],[22.4079,50.6479],[22.456,54.6478],[27.5336,54.6229],[27.5952,58.1227],[30.7736,58.1047],[30.7956,59.1046],[38.8024,59.0512],[38.7623,57.5513],[48.9009,57.4685],[49.9135,57.4594],[49.854,55.4597],[52.3819,55.4363],[52.3131,52.9366],[72.8403,52.7196],[72.4573,36.2219],[69.5738,36.2547],[69.4869,30.9219],[52.4267,31.1004],[42.6284,31.1865]]]}},{\"type\":\"Feature\",\"id\":\"Phe\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-8.3073,-39.3128],[-8.2315,-56.3127],[-8.2216,-57.8127],[21.2062,-57.8484],[21.2733,-52.8486],[24.9674,-52.8659],[24.9938,-50.8659],[28.6933,-50.8859],[28.7383,-47.5527],[36.1529,-47.6005],[36.264,-39.4342],[26.3507,-39.3726],[0.6029,-39.3039],[-8.3073,-39.3128]]]}},{\"type\":\"Feature\",\"id\":\"Pic\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[90.9518,-43.0058],[75.9744,-42.8256],[73.4824,-42.7964],[73.4021,-46.2959],[68.4241,-46.2388],[68.3622,-48.7384],[68.2177,-53.7376],[75.677,-53.8238],[75.5477,-57.323],[83.0188,-57.4123],[82.8576,-60.9113],[90.3451,-61.0021],[90.1736,-64.0011],[98.9372,-64.107],[102.7033,-64.1519],[103.0111,-58.1537],[97.9951,-58.0938],[98.1143,-55.0946],[93.1074,-55.034],[93.1944,-52.5346],[90.6937,-52.5042],[90.7489,-50.7545],[90.9518,-43.0058]]]}},{\"type\":\"Feature\",\"id\":\"Psc\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-17.1503,0.6622],[-17.1578,2.6622],[-17.1786,8.1622],[-0.902,8.1958],[-0.9029,10.6958],[1.6027,10.696],[1.6032,13.196],[3.7341,13.1952],[3.7399,21.6952],[14.4148,21.6766],[14.4241,24.4266],[12.4135,24.4319],[12.4431,33.6819],[22.8974,33.6454],[22.8664,28.6454],[26.7647,28.6263],[26.7447,25.6263],[26.6557,10.5432],[31.6652,10.5144],[31.6153,2.5979],[6.6038,2.6925],[6.6013,0.6925],[6.5927,-6.3075],[-0.8967,-6.3042],[-0.8978,-3.3042],[-17.1353,-3.3378],[-17.1503,0.6622]]]}},{\"type\":\"Feature\",\"id\":\"PsA\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-13.319,-24.825],[-30.2297,-24.904],[-38.1922,-24.9598],[-38.1684,-27.4597],[-38.0719,-36.4593],[-13.2725,-36.325],[-13.319,-24.825]]]}},{\"type\":\"Feature\",\"id\":\"Pup\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[111.9734,-11.2521],[111.6772,-33.2505],[99.9039,-33.1128],[99.7089,-43.1116],[90.9518,-43.0058],[90.7489,-50.7545],[120.8617,-51.1026],[121.0383,-43.3535],[126.5723,-43.4095],[126.6778,-37.16],[126.9271,-17.4113],[126.9898,-11.4116],[122.7342,-11.3688],[111.9734,-11.2521]]]}},{\"type\":\"Feature\",\"id\":\"Pyx\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[126.9271,-17.4113],[130.1843,-17.4425],[130.1635,-19.4424],[137.685,-19.5088],[137.6368,-24.5086],[141.9043,-24.5425],[141.7716,-37.292],[126.6778,-37.16],[126.9271,-17.4113]]]}},{\"type\":\"Feature\",\"id\":\"Ret\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[48.3627,-67.0358],[68.794,-67.2479],[69.2745,-58.7507],[65.5546,-58.7089],[65.6505,-56.2094],[60.6929,-56.1556],[60.7979,-52.8228],[58.3188,-52.7968],[53.365,-52.7471],[53.2368,-57.0798],[48.7911,-57.0378],[48.3627,-67.0358]]]}},{\"type\":\"Feature\",\"id\":\"Sge\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-75.6264,18.6647],[-75.6609,21.2478],[-69.9037,21.3148],[-69.8787,19.3983],[-61.1143,19.4955],[-61.1397,21.5787],[-54.8746,21.6437],[-54.866,20.8937],[-54.8131,16.144],[-56.441,16.1275],[-61.074,16.0791],[-61.0788,16.4957],[-73.5945,16.3551],[-73.6245,18.6882],[-75.6264,18.6647]]]}},{\"type\":\"Feature\",\"id\":\"Sgr\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-75.2559,-11.8664],[-75.2063,-15.8328],[-84.4505,-15.9436],[-94.1998,-16.0619],[-93.9982,-30.0607],[-90.4972,-30.0182],[-90.3745,-37.0175],[-70.4037,-36.7786],[-70.2304,-45.2776],[-52.8307,-45.09],[-53.102,-27.5913],[-58.084,-27.6419],[-58.2736,-11.6762],[-75.2559,-11.8664]]]}},{\"type\":\"Feature\",\"id\":\"Sco\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-119.5627,-8.3523],[-114.3088,-8.2959],[-114.1893,-18.5452],[-112.5618,-18.5272],[-112.5493,-19.5272],[-114.177,-19.5452],[-114.1086,-24.8781],[-106.8443,-24.7961],[-106.7647,-30.2123],[-93.9982,-30.0607],[-90.4972,-30.0182],[-90.3745,-37.0175],[-90.1907,-45.5163],[-111.4294,-45.7671],[-111.5052,-42.2675],[-117.8472,-42.3367],[-118.0523,-29.8378],[-123.07,-29.8896],[-123.1869,-20.3902],[-119.4282,-20.3516],[-119.5627,-8.3523]]]}},{\"type\":\"Feature\",\"id\":\"Scl\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-13.319,-24.825],[-0.8894,-24.8042],[26.4589,-24.8729],[26.3507,-39.3726],[0.6029,-39.3039],[-8.3073,-39.3128],[-8.3166,-36.3128],[-13.2725,-36.325],[-13.319,-24.825]]]}},{\"type\":\"Feature\",\"id\":\"Sct\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-84.4505,-15.9436],[-75.2063,-15.8328],[-75.2559,-11.8664],[-75.3527,-3.8337],[-79.6018,-3.8842],[-84.6009,-3.9445],[-84.4505,-15.9436]]]}},{\"type\":\"Feature\",\"id\":\"Ser\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-132.147,-0.4743],[-132.2185,7.5254],[-132.3945,25.5246],[-130.9005,25.5381],[-118.1943,25.6641],[-118.1434,21.6644],[-119.889,21.646],[-119.8189,15.6463],[-117.3234,15.6728],[-117.1903,3.6735],[-114.4414,3.7034],[-114.3974,-0.2964],[-114.3616,-3.5462],[-119.613,-3.6026],[-132.118,-3.7242],[-132.147,-0.4743]]]}},{\"type\":\"Feature\",\"id\":\"Ser\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-84.6494,0.0552],[-84.6858,3.055],[-82.0608,3.0867],[-82.0789,4.5866],[-84.704,4.5549],[-84.7254,6.3048],[-78.5414,6.3792],[-75.474,6.4156],[-75.4236,2.1659],[-79.6738,2.1153],[-79.6498,0.1155],[-79.6018,-3.8842],[-84.6009,-3.9445],[-84.4505,-15.9436],[-94.1998,-16.0619],[-100.7026,-16.14],[-100.7779,-10.1404],[-94.5265,-10.0654],[-94.5056,-11.7319],[-93.2553,-11.7168],[-93.2762,-10.0502],[-88.7763,-9.9956],[-88.8503,-3.9961],[-90.8503,-4.0204],[-90.899,-0.0206],[-84.6494,0.0552]]]}},{\"type\":\"Feature\",\"id\":\"Sex\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[145.3489,-0.5671],[145.3984,6.4328],[162.876,6.3377],[162.8497,-0.6622],[162.8271,-6.6622],[162.8079,-11.6621],[145.2703,-11.5668],[145.3489,-0.5671]]]}},{\"type\":\"Feature\",\"id\":\"Tau\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[50.8367,-1.303],[50.853,0.447],[50.9464,10.3632],[51.0372,19.4461],[52.2906,19.4343],[52.4267,31.1004],[69.4869,30.9219],[69.4768,30.2553],[73.2353,30.2123],[73.2125,28.7124],[90.2289,28.5092],[90.2211,28.0093],[90.144,22.8431],[87.3938,22.8765],[87.327,18.0435],[88.3272,18.0314],[88.2554,12.5319],[85.7551,12.5622],[85.7936,15.5619],[81.7922,15.6101],[81.7987,16.1101],[76.2953,16.1755],[76.2889,15.6755],[71.034,15.7365],[70.8524,0.2375],[55.3529,0.4037],[55.3356,-1.3462],[50.8367,-1.303]]]}},{\"type\":\"Feature\",\"id\":\"Tel\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-52.5412,-56.5886],[-52.8307,-45.09],[-70.2304,-45.2776],[-87.691,-45.486],[-87.3277,-56.9838],[-52.5412,-56.5886]]]}},{\"type\":\"Feature\",\"id\":\"Tri\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[26.7447,25.6263],[26.7647,28.6263],[22.8664,28.6454],[22.8974,33.6454],[22.9108,35.6453],[31.8543,35.5971],[31.8711,37.3471],[39.6793,37.2932],[40.4347,37.2874],[40.4024,34.5375],[42.6665,34.5197],[42.6284,31.1865],[38.1032,31.2213],[38.0701,27.8048],[30.5306,27.855],[30.5137,25.6051],[26.7447,25.6263]]]}},{\"type\":\"Feature\",\"id\":\"TrA\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-135.8336,-70.5115],[-135.9964,-68.0122],[-133.4429,-67.9909],[-133.6465,-64.0751],[-129.8334,-64.0416],[-129.9454,-61.4587],[-127.4102,-61.4353],[-127.4501,-60.4355],[-110.9653,-60.2645],[-110.9184,-61.2642],[-108.4622,-61.2365],[-108.3237,-63.819],[-105.8049,-63.7901],[-105.7165,-65.2063],[-104.4576,-65.1916],[-104.275,-67.6906],[-101.7575,-67.6611],[-101.5293,-70.1597],[-135.8336,-70.5115]]]}},{\"type\":\"Feature\",\"id\":\"Tuc\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-8.0022,-74.3125],[1.5663,-74.304],[12.3324,-74.3186],[12.2954,-75.3185],[20.6541,-75.3472],[21.2062,-57.8484],[-8.2216,-57.8127],[-8.2315,-56.3127],[-27.8863,-56.3908],[-27.6014,-66.89],[-8.1386,-66.8126],[-8.0022,-74.3125]]]}},{\"type\":\"Feature\",\"id\":\"UMa\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[145.7092,41.4317],[139.5125,41.4786],[139.5907,46.4783],[128.4401,46.5777],[128.7991,59.576],[122.1291,59.6434],[123.0862,73.1384],[140.6155,72.9741],[171.9614,72.8125],[171.8493,65.8126],[-178.4207,65.804],[-178.4184,63.304],[-156.4495,63.3593],[-156.4264,62.3594],[-142.9547,62.4415],[-142.7488,54.9422],[-148.4156,54.9036],[-148.3013,47.9039],[-156.2049,47.8599],[-156.2576,52.3598],[-177.1815,52.3043],[-177.1736,44.3043],[-178.4086,44.304],[-178.4055,33.304],[-178.4043,28.304],[179.6089,28.304],[166.694,28.325],[166.7142,33.325],[163.4894,33.3357],[163.5232,39.3356],[154.3594,39.3774],[154.3782,41.3774],[145.7092,41.4317]]]}},{\"type\":\"Feature\",\"id\":\"UMi\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-164.1794,76.3289],[-163.9025,69.3294],[-149.3492,69.3991],[-149.1794,65.3997],[-124.6704,65.6023],[-124.9494,69.6009],[-112.1589,69.7383],[-112.7793,74.7348],[-98.4634,74.9033],[-99.7821,79.8953],[-92.344,79.9857],[-98.2778,85.9496],[-51.279,86.4656],[-51.6686,86.6306],[-16.4893,86.8369],[-20.739,88.6639],[0.9483,88.6092],[24.7077,88.3564],[57.6647,88.0063],[135.8325,87.5689],[130.4028,86.0975],[-146.977,85.9308],[-143.2171,79.445],[-156.1908,79.3629],[-155.843,76.3638],[-164.1794,76.3289]]]}},{\"type\":\"Feature\",\"id\":\"Vel\",\"properties\":{\"rank\":\"2\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[166.3373,-57.1744],[166.4565,-40.4246],[141.7341,-40.2919],[141.7716,-37.292],[126.6778,-37.16],[126.5723,-43.4095],[121.0383,-43.3535],[120.8617,-51.1026],[123.3811,-51.1285],[123.3201,-53.3782],[127.6093,-53.4207],[127.5671,-54.9205],[133.3802,-54.9742],[133.3237,-56.974],[166.3373,-57.1744]]]}},{\"type\":\"Feature\",\"id\":\"Vir\",\"properties\":{\"rank\":\"1\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[174.3505,-0.6917],[174.3657,10.3083],[179.6037,10.304],[179.6045,13.304],[-165.938,13.3225],[-165.9409,14.3225],[-155.9711,14.3605],[-155.9362,7.3606],[-132.2185,7.5254],[-132.147,-0.4743],[-138.3969,-0.5269],[-138.3329,-8.5267],[-144.5915,-8.5731],[-144.4869,-22.5728],[-165.8331,-22.6773],[-165.8669,-11.6774],[179.0968,-11.6958],[179.0986,-6.6958],[174.3423,-6.6917],[174.3505,-0.6917]]]}},{\"type\":\"Feature\",\"id\":\"Vol\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[98.9372,-64.107],[98.4544,-70.1041],[97.7707,-75.1],[114.2147,-75.2899],[135.2437,-75.4955],[136.0947,-64.499],[102.7033,-64.1519],[98.9372,-64.107]]]}},{\"type\":\"Feature\",\"id\":\"Vul\",\"properties\":{\"rank\":\"3\"},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[-75.6609,21.2478],[-75.7228,25.6641],[-69.8387,25.7326],[-69.8674,27.7324],[-63.7278,27.8012],[-63.7491,29.3011],[-44.9274,29.4871],[-44.9161,28.4872],[-37.3798,28.5481],[-37.338,24.0482],[-39.8483,24.0289],[-39.8116,20.0291],[-42.8212,20.0046],[-50.0923,19.94],[-50.1031,20.9399],[-54.866,20.8937],[-54.8746,21.6437],[-61.1397,21.5787],[-61.1143,19.4955],[-69.8787,19.3983],[-69.9037,21.3148],[-75.6609,21.2478]]]}}]}")
  const wrapRa=ra=>((ra%360)+360)%360;
  try{
    if(data.type!=='FeatureCollection'||!Array.isArray(data.features)||data.features.length!==89)
      throw new Error('Bundled IAU boundary dataset failed validation');
    const overlay=A.graphicOverlay({color:GV_IAU_BOUNDARY_COLOR,lineWidth:GV_IAU_BOUNDARY_WIDTH});
    aladin.addOverlay(overlay);
    let rendered=0,vertices=0,validFeatures=0;
    const addBoundaryLine=line=>{
      let part=[];
      const flush=()=>{
        if(part.length>=2){
          overlay.add(A.polyline(part,{color:GV_IAU_BOUNDARY_COLOR,lineWidth:GV_IAU_BOUNDARY_WIDTH,opacity:GV_IAU_BOUNDARY_OPACITY}));
          rendered++;
        }
        part=[];
      };
      for(const point of line){
        if(!Array.isArray(point)||point.length<2)continue;
        const longitude=Number(point[0]),dec=Number(point[1]);
        if(!Number.isFinite(longitude)||!Number.isFinite(dec)||longitude < -180||longitude > 180||dec < -90||dec > 90)continue;
        const ra=wrapRa(longitude);
        if(part.length){
          const prev=part[part.length-1];
          const delta=ra-prev[0];
          if(Math.abs(delta)>180){
            // Preserve each edge crossing the 0h/24h seam instead of dropping it.
            const crossesEast=delta < -180;
            const seam=crossesEast?360:0;
            const otherSeam=crossesEast?0:360;
            const adjustedRa=crossesEast?ra+360:ra-360;
            const fraction=(seam-prev[0])/(adjustedRa-prev[0]);
            const seamDec=prev[1]+fraction*(dec-prev[1]);
            part.push([seam,seamDec]);
            flush();
            part.push([otherSeam,seamDec],[ra,dec]);
          }else part.push([ra,dec]);
        }else part.push([ra,dec]);
        vertices++;
      }
      flush();
    };
    let closedRingCount=0,openRingCount=0;
    const addClosedRing=ring=>{
      if(!Array.isArray(ring)||ring.length<4)return;
      const first=ring[0],last=ring[ring.length-1];
      if(!Array.isArray(first)||!Array.isArray(last))return;
      const isClosed=Math.abs(Number(first[0])-Number(last[0]))<1e-8&&Math.abs(Number(first[1])-Number(last[1]))<1e-8;
      if(isClosed)closedRingCount++;else openRingCount++;
      const closed=ring.slice();
      if(!isClosed)closed.push(first);
      addBoundaryLine(closed);
    };
    for(const feature of data.features){
      const geometry=feature&&feature.geometry;
      if(!geometry||!Array.isArray(geometry.coordinates))continue;
      if(geometry.type==='Polygon'){
        const before=rendered;
        geometry.coordinates.forEach(addClosedRing);
        if(rendered>before)validFeatures++;
      }else if(geometry.type==='MultiPolygon'){
        const before=rendered;
        geometry.coordinates.forEach(poly=>Array.isArray(poly)&&poly.forEach(addClosedRing));
        if(rendered>before)validFeatures++;
      }
    }
    if(rendered<80||vertices<1000||validFeatures<80||closedRingCount<80)
      throw new Error('IAU constellation polygons failed closure/geometry validation: segments='+rendered+', vertices='+vertices+', features='+validFeatures+', closedRings='+closedRingCount);
    overlay.show();
    const overlays=typeof aladin.getOverlays==='function'?aladin.getOverlays():null;
    const registered=Array.isArray(overlays)?overlays.includes(overlay):null;
    if(registered===false)throw new Error('Aladin did not register the constellation polygon overlay');
    const visibleProbe=data.features.slice(0,20).flatMap(feature=>{
      const rings=feature.geometry?.coordinates||[];
      return rings.flatMap(ring=>ring.map(point=>aladin.world2pix(wrapRa(Number(point[0])),Number(point[1]))).filter(Boolean));
    }).length;
    window.GalaxyViewerConstellationRegions=Object.freeze({
      VERSION:'0005',featureCount:data.features.length,renderedFeatureCount:validFeatures,
      segmentCount:rendered,vertexCount:vertices,closedRingCount,openRingCount,
      visibleProbeCount:visibleProbe,coordinateFrame:'J2000/ICRS',
      geometryType:'closed IAU constellation polygons',lineWidth:GV_IAU_BOUNDARY_WIDTH,
      opacity:GV_IAU_BOUNDARY_OPACITY,overlayRegistered:registered,overlay
    });
    console.info('GV IAU CONSTELLATION POLYGONS RENDERED',window.GalaxyViewerConstellationRegions);
    if(visibleProbe===0)console.info('GV IAU BOUNDARIES: attached successfully; sample points are outside the current field of view. Zoom out to see the full-sky boundaries.');
  }catch(error){
    window.GalaxyViewerConstellationRegions={VERSION:'0003',error:String(error)};
    console.error('GV IAU CONSTELLATION REGIONS FAILED',error);
  }
})();

if(window.GalaxyViewerHeadsUpDisplay?.VERSION!=='0005'||typeof window.GalaxyViewerHeadsUpDisplay.mount!=='function')throw new Error('HEADS-UP DISPLAY 0004 EXPORT MISSING');
if(typeof window.GalaxyRandomTravelPresentation?.mount!=='function')throw new Error('RANDOM TRAVEL PRESENTATION EXPORT MISSING');
if(window.GalaxyDestinationPresentation?.VERSION!=='0061'||typeof window.GalaxyDestinationPresentation.mount!=='function')throw new Error('DESTINATION PRESENTATION 0061 EXPORT MISSING');
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
let gvConstellationPromise=null;
function gvSetConstellationsEnabled(enabled){
    if(!gvConstellationPromise)gvConstellationPromise=window.GalaxyViewerConstellationOverlay.mount(aladin).catch(error=>{gvConstellationPromise=null;console.error('CONSTELLATION OVERLAY INIT FAILED',error);throw error});
    gvConstellationPromise.then(layer=>layer.setEnabled(!!enabled)).catch(error=>console.error('CONSTELLATION TOGGLE FAILED',error));
}
const hamburger=window.GalaxyViewerHamburgerMenu.init({
    host:hosts.hamburger,
    onMenuAction(action){
        if(action==='CONSTELLATIONS ON'||action==='CONSTELLATIONS OFF'){
            gvSetConstellationsEnabled(action==='CONSTELLATIONS ON');
        }
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
// BUILD 0096: constellation overlay is enabled on first launch by default.
hamburger.root.__gvConstellationsEnabled=true;
hamburger.root.querySelector('[data-gv-menu-action="CONSTELLATIONS"] .gv-reticle-mini')?.classList.add('gv-on');
hamburger.root.querySelector('[data-gv-menu-action="CONSTELLATIONS"] .gv-viewer-menu-label')?.setAttribute('aria-pressed','true');
gvSetConstellationsEnabled(true);

// ============================================================================
// SECTION 024 — COORDINATE OVERLAY 0008 INITIALIZATION
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
// BUILD 0036 REPAIR REVISION 2: keep coordinate readback out of the zoom animation hot path.
// Release validation now requires the active coordinate overlay 0008 pin.
// Build identity is validated against the active release pointer 0036.
// Coordinate readback is throttled and suspended while the zoom slider is driving FOV.
setInterval(()=>{if(document.visibilityState!=='visible'||gvZoomInteractionActive||window.GV_NAV_BACKGROUND_SUSPENDED)return;gvSyncCoordinateFromAladin()},250);


// ============================================================================
// SECTION 025 — TARGET / PROVIDER SURVEY 0006 INITIALIZATION
// ECO: GV200-001 BUILD 0072
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
const GV_SURVEY_RUNTIME_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0006.json';
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
const gvSurveyRuntimePayload=await fetch(fresh(GV_SURVEY_RUNTIME_CATALOG_URL)+'&gv-json-integrity=20261023-0006',{cache:'no-store'}).then(response=>{
    if(!response.ok)throw new Error('GV SURVEY RUNTIME CATALOG HTTP '+response.status);
    return response.json();
});
const gvSurveyRuntimeRecords=(Array.isArray(gvSurveyRuntimePayload)?gvSurveyRuntimePayload:gvSurveyRuntimePayload?.records);
if(!Array.isArray(gvSurveyRuntimeRecords)||gvSurveyRuntimeRecords.length===0)throw new Error('GV SURVEY RUNTIME CATALOG INVALID: expected non-empty records from 0004');
for(const provider of GV_SURVEY_PROVIDER_ORDER){
    const records=gvSurveyRuntimeRecords
        .map((record,index)=>Object.freeze({
            ...record,
            provider:String(record?.providerKey||record?.provider||'').toUpperCase(),
            providerLabel:String(record?.providerKey||record?.provider||'').toUpperCase(),
            imageUrl:gvCanonicalAvmImageUrl(record?.imageUrl||''),
            selectedImageUrl:gvCanonicalAvmImageUrl(record?.imageUrl||''),
            catalogKey:String(record?.sourceCatalog||'').trim(),
            catalogIndex:Number.isFinite(Number(record?.sourceIndex))?Number(record.sourceIndex):index,
            // NGC 7331's Spitzer AVM registration has authoritative rectangular FOV 2.68 x 2.01 arcmin.
            // The runtime scalar fovDegrees is not valid for both axes; force the published AVM footprint for this asset only.
            fovXDegrees:(String(record?.archiveId||record?.id||'').toLowerCase()==='ssc2004-12a1'||(/NGC\s*7331/i.test(String(record?.name||record?.commonName||record?.designation||''))&&/SPITZER/i.test(String(record?.providerKey||record?.provider||record?.sourceCatalog||''))))?0.21:Number(record?.fovXDegrees??record?.fieldOfViewDegrees?.widthDegrees??record?.fovDegrees),
            fovYDegrees:(String(record?.archiveId||record?.id||'').toLowerCase()==='ssc2004-12a1'||(/NGC\s*7331/i.test(String(record?.name||record?.commonName||record?.designation||''))&&/SPITZER/i.test(String(record?.providerKey||record?.provider||record?.sourceCatalog||''))))?0.13666666666666666:Number(record?.fieldOfViewDegrees?.heightDegrees??record?.fovYDegrees??record?.fovHeightDegrees??record?.fovDegrees),
            fovDegrees:(String(record?.archiveId||record?.id||'').toLowerCase()==='ssc2004-12a1'||(/NGC\s*7331/i.test(String(record?.name||record?.commonName||record?.designation||''))&&/SPITZER/i.test(String(record?.providerKey||record?.provider||record?.sourceCatalog||''))))?0.21:Number(record?.fovXDegrees??record?.fovDegrees),
            avmHorizontalFovDegrees:Number(record?.fovXDegrees??record?.fovDegrees),
            avmVerticalFovDegrees:Number(record?.fovYDegrees??record?.fovDegrees),
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
#gv-catalog-search-input{width:100%;height:32px;box-sizing:border-box;padding:0 9px;border:1px solid rgba(124,203,255,.52);border-radius:7px;outline:none;background:rgba(1,10,24,.90);color:#E9FBFF;font:400 11.5px/1 "GV Space Age",sans-serif;letter-spacing:.55px;text-transform:uppercase;box-shadow:inset 0 0 6px rgba(0,0,0,.55),0 0 4px rgba(67,207,255,.12);caret-color:#8DDEFF}
#gv-catalog-search-input::placeholder{color:rgba(189,228,245,.76);opacity:1}
#gv-catalog-search-input:focus{border-color:#9BE7FF;box-shadow:inset 0 0 7px rgba(0,0,0,.58),0 0 5px rgba(124,203,255,.38)}
#gv-catalog-search-results{display:none;max-height:min(55vh,420px);overflow-y:auto;margin-top:7px;padding-right:2px;scrollbar-width:thin}
.gv-search-group{margin:6px 0 0}
.gv-search-group-head{padding:4px 7px;color:#9CDEFF;font:400 9px/1 "GV Space Age",sans-serif;letter-spacing:.55px;text-transform:uppercase;text-shadow:0 0 5px rgba(67,207,255,.38)}
.gv-search-result{appearance:none;-webkit-appearance:none;position:relative;width:100%;display:grid;grid-template-columns:32px minmax(0,1fr) 30px;column-gap:7px;align-items:center;min-height:40px;margin:2px 0;padding:3px 6px 3px 3px;box-sizing:border-box;border:1px solid rgba(67,207,255,.72);border-radius:9px;background:linear-gradient(180deg,rgba(23,78,134,.86),rgba(4,27,62,.96) 58%,rgba(13,90,152,.78));color:#F4FDFF;text-align:left;cursor:pointer;touch-action:manipulation;overflow:hidden;box-shadow:inset 0 1px 2px rgba(225,251,255,.32),inset 0 -2px 4px rgba(0,0,0,.42),0 0 4px rgba(50,190,255,.26)}
.gv-search-result:active{transform:translateY(1px);filter:brightness(1.18)}
.gv-search-result-thumb{width:32px;height:32px;display:flex;align-items:center;justify-content:center;overflow:hidden;border:1px solid rgba(158,220,255,.66);border-radius:8px;background:radial-gradient(circle at 50% 45%,#0B2749 0%,#02070F 72%);box-shadow:inset 0 0 5px rgba(0,0,0,.52),0 0 4px rgba(88,191,255,.32)}
.gv-search-result-thumb img{display:block;width:100%;height:100%;object-fit:contain;object-position:center center;background:#000}
.gv-search-result-icon{width:30px;height:30px;object-fit:cover;object-position:center center;display:block;border:1px solid rgba(158,220,255,.66);border-radius:8px;background:#000;box-shadow:inset 0 0 5px rgba(0,0,0,.52),0 0 4px rgba(88,191,255,.32)}
.gv-search-result-copy{min-width:0;display:flex;flex-direction:column;justify-content:center;gap:2px;overflow:hidden}
.gv-search-result-name{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#EAFBFF;font:400 10.5px/13px "GV Space Age",sans-serif;letter-spacing:.25px}
.gv-search-result-match{display:-webkit-box;min-width:0;max-height:20px;overflow:hidden;color:rgba(193,226,245,.88);font:400 8px/10px "GV Space Age",sans-serif;letter-spacing:.25px;white-space:normal;overflow-wrap:anywhere;-webkit-box-orient:vertical;-webkit-line-clamp:2}
.gv-search-empty{padding:10px 7px;color:rgba(181,222,241,.76);font:400 9px/13px "GV Space Age",sans-serif;letter-spacing:.35px;text-align:center}
`;
document.head.appendChild(gvSearchStyle);
const gvSearchTile=document.createElement('div');
gvSearchTile.id='gv-catalog-search-tile';
gvSearchTile.innerHTML='<div class="gv-search-line"><input id="gv-catalog-search-input" type="search" autocomplete="off" autocapitalize="none" spellcheck="false" aria-label="SEARCH GALAXIES" placeholder="SEARCH GALAXIES"><span class="gv-search-icon" aria-hidden="true">🔍</span></div><div id="gv-catalog-search-results" aria-live="polite"></div>';
const gvSearchInput=gvSearchTile.querySelector('#gv-catalog-search-input');
const gvSearchResults=gvSearchTile.querySelector('#gv-catalog-search-results');
let gvSearchIndex=Object.freeze(gvSurveyRuntimeRecords.map(record=>Object.freeze({
    record,
    displayRecord:record,
    text:Object.entries(record||{}).flatMap(([key,value])=>{
        if(value===null||value===undefined)return [];
        if(Array.isArray(value))return [key,...value.map(item=>String(item??''))];
        if(typeof value==='object')return [key,JSON.stringify(value)];
        return [key,String(value)];
    }).join(' ').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase()
})));
let gvFullSearchIndexPromise=null;
function gvSearchFlatten(value,keyPath=''){
    if(value===null||value===undefined)return [];
    if(Array.isArray(value))return [keyPath,...value.flatMap((item,index)=>gvSearchFlatten(item,keyPath+' '+index))];
    if(typeof value==='object')return Object.entries(value).flatMap(([key,child])=>gvSearchFlatten(child,keyPath+' '+key));
    return [keyPath,String(value)];
}
function gvSearchDisplayName(record){
    return String(record?.name||record?.commonName||record?.displayName||record?.designation||record?.archiveId||record?.id||record?.sourceIndex||'UNNAMED GALAXY').trim();
}
function gvSearchRecordId(record){
    return String(record?.archiveId||record?.id||record?.sourceId||'').trim().toLowerCase();
}
function gvSearchRecordNames(record){
    return [record?.designation,record?.name,record?.displayName,record?.commonName,record?.title,record?.pseudonym]
        .map(value=>String(value||'').trim().toLowerCase()).filter(Boolean);
}
let gvFullSearchIndexError=null;
function gvSearchCoordinateValues(record){
    const ra=[],dec=[],seen=new Set();
    const walk=(value,path='')=>{
        if(value===null||value===undefined)return;
        if(typeof value==='object'){
            if(seen.has(value))return;seen.add(value);
            if(Array.isArray(value)){value.forEach((child,index)=>walk(child,path+' '+index));return}
            for(const [key,child] of Object.entries(value))walk(child,path+' '+key);
            return;
        }
        const key=String(path.split(/\s+/).pop()||'').toLowerCase().replace(/[^a-z]/g,'');
        const raw=String(value).trim();if(!raw)return;
        const isRa=/^(ra|radeg|radegree|radegrees|rightascension|rightascensiondeg|rightascensiondegrees|alpha)$/.test(key);
        const isDec=/^(dec|decdeg|decdegree|decdegrees|declination|declinationdeg|declinationdegrees|delta)$/.test(key);
        if(!isRa&&!isDec)return;
        let numeric=Number(raw);
        if(!Number.isFinite(numeric)){
            const sex=raw.match(/^\s*([+-]?\d+(?:\.\d+)?)\s*[:h°]\s*(\d+(?:\.\d+)?)?\s*(?:[:m'′]\s*(\d+(?:\.\d+)?)?)?/i);
            if(sex){
                const sign=Number(sex[1])<0?-1:1;
                numeric=sign*(Math.abs(Number(sex[1]))+Number(sex[2]||0)/60+Number(sex[3]||0)/3600);
                if(isRa)numeric*=15;
            }
        }
        if(!Number.isFinite(numeric))return;
        if(isRa&&/(rahours|rightascensionhours|rahour)/.test(key))numeric*=15;
        (isRa?ra:dec).push(numeric);
    };
    walk(record);return {ra,dec};
}
function gvSearchNumericPrefix(value,query){
    if(!Number.isFinite(value))return false;
    const q=String(query).replace(/^\+/,'');
    return [String(value),value.toFixed(2),value.toFixed(3),value.toFixed(4),value.toFixed(5),value.toFixed(6)]
        .some(candidate=>candidate.startsWith(q));
}
function gvSearchCoordinatePairMatches(record,tokens){
    if(tokens.length!==2||!tokens.every(token=>/^[+-]?\d+(?:\.\d*)?$/.test(token)))return false;
    const {ra,dec}=gvSearchCoordinateValues(record);
    return (ra.some(r=>gvSearchNumericPrefix(r,tokens[0]))&&dec.some(d=>gvSearchNumericPrefix(d,tokens[1])))||
        (dec.some(d=>gvSearchNumericPrefix(d,tokens[0]))&&ra.some(r=>gvSearchNumericPrefix(r,tokens[1])));
}
async function gvEnsureFullSearchIndex(){
    if(gvFullSearchIndexPromise)return gvFullSearchIndexPromise;
    gvFullSearchIndexError=null;
    gvFullSearchIndexPromise=(async()=>{
        const catalogKeys=['hubble','jwst','chandra','eso','noirlab','spitzer'];
        const providerByCatalog={hubble:'HUBBLE',jwst:'JWST',chandra:'CHANDRA',eso:'ESO',noirlab:'NOIRLAB',spitzer:'SPITZER'};
        const root='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/';
        const cdnRoot='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/87f05f4a703b58d9ee02fdd5fee365b339f41075/';
        const masterUrl=root+'viewer/image-databases/master-database/gv-master-catalog.json';
        const fetchSearchJson=async(url,fallbackUrl,label)=>{
            let firstError=null;
            try{
                const response=await fetch(fresh(url),{cache:'no-cache'});
                if(response.ok)return await response.json();
                firstError=new Error(label+' HTTP '+response.status);
            }catch(error){firstError=error}
            if(!fallbackUrl)throw firstError||new Error(label+' unavailable');
            const fallback=await fetch(fresh(fallbackUrl),{cache:'no-cache'});
            if(!fallback.ok)throw new Error(label+' failed on primary and CDN fallback ('+fallback.status+')');
            return await fallback.json();
        };
        const master=await fetchSearchJson(masterUrl,cdnRoot+'viewer/image-databases/master-database/gv-master-catalog.json','GV SEARCH MASTER');
        if(!master?.catalogs)throw new Error('GV SEARCH MASTER POINTER MAP MISSING');
        const runtimeById=new Map(),runtimeByName=new Map();
        for(const record of gvSurveyRuntimeRecords){
            const provider=gvSurveyProviderKey(record),id=gvSearchRecordId(record);
            if(id&&!runtimeById.has(provider+'|'+id))runtimeById.set(provider+'|'+id,record);
            for(const name of gvSearchRecordNames(record)){
                const key=provider+'|'+name;if(!runtimeByName.has(key))runtimeByName.set(key,record);
            }
        }
        const loaded=await Promise.allSettled(catalogKeys.map(async key=>{
            const relative=String(master.catalogs[key]||'').trim();
            if(!relative)throw new Error('Catalog path missing: '+key);
            const primaryUrl=new URL(relative,root).href;
            const payload=await fetchSearchJson(primaryUrl,cdnRoot+relative,'Catalog '+key);
            const entries=Array.isArray(payload)?payload:(Array.isArray(payload?.entries)?payload.entries:[]);
            if(!entries.length)throw new Error('Catalog entries missing: '+key);
            const provider=providerByCatalog[key];
            return entries.map((entry,index)=>{
                const id=gvSearchRecordId(entry);let record=(id&&runtimeById.get(provider+'|'+id))||null;
                if(!record)for(const name of gvSearchRecordNames(entry)){record=runtimeByName.get(provider+'|'+name)||null;if(record)break}
                const navigable=record||Object.freeze({
                    ...entry,provider,providerKey:provider,providerLabel:provider,catalogKey:key,catalogIndex:index,
                    imageUrl:String(entry?.imageUrl||entry?.selectedImageUrl||entry?.hdUrl||entry?.sourceUrl||'').trim(),
                    ra:entry?.ra??entry?.raDeg??entry?.raDegrees??entry?.rightAscension,
                    dec:entry?.dec??entry?.decDeg??entry?.decDegrees??entry?.declination,
                    fovDegrees:Number(entry?.fovXDegrees??entry?.fovDegrees??entry?.fieldOfView),
                    aladinRotation:Number(entry?.aladinRotation??entry?.spatialRotationDeg)
                });
                const allText=(JSON.stringify(entry)+' '+JSON.stringify(record||{}))
                    .normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
                const thumbnailRecord=Object.freeze({...navigable,provider,providerKey:provider,catalogKey:key,catalogIndex:index});
                return Object.freeze({record:navigable,thumbnailRecord,displayRecord:entry,provider,text:allText,matchRecords:Object.freeze([entry,...(record&&record!==entry?[record]:[])])});
            });
        }));
        const full=[],failed=[];
        loaded.forEach((result,index)=>{if(result.status==='fulfilled')full.push(...result.value);else failed.push(catalogKeys[index]+': '+String(result.reason?.message||result.reason))});
        if(failed.length)throw new Error('Catalog load incomplete; no partial search results shown: '+failed.join('; '));
        if(!full.length)throw new Error('All individual survey catalogs failed: '+failed.join('; '));
        const uniqueById=new Map(),unique=[];
        for(const item of full){
            const id=gvSearchRecordId(item.displayRecord);if(!id){unique.push(item);continue}
            const key=item.provider+'|'+id,prior=uniqueById.get(key);
            if(prior)uniqueById.set(key,Object.freeze({...prior,text:prior.text+' '+item.text,matchRecords:Object.freeze([...(prior.matchRecords||[prior.displayRecord,prior.record]),...(item.matchRecords||[item.displayRecord,item.record])])}));
            else{uniqueById.set(key,item);unique.push(item)}
        }
        for(let index=0;index<unique.length;index++){const item=unique[index],id=gvSearchRecordId(item.displayRecord);if(id)unique[index]=uniqueById.get(item.provider+'|'+id)}
        gvSearchIndex=Object.freeze(unique);
        console.info('GV FULL CATALOG SEARCH INDEX READY',{records:unique.length,catalogsLoaded:catalogKeys.length-failed.length,failures:failed});
        if(failed.length)console.warn('GV FULL CATALOG SEARCH PARTIAL',failed);
    })().catch(error=>{gvFullSearchIndexPromise=null;gvFullSearchIndexError=error;console.error('GV FULL CATALOG SEARCH INDEX ERROR',error)});
    return gvFullSearchIndexPromise;
}

function gvSearchNormalizeMatchText(value){
    return String(value??'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
}
function gvSearchMatchedStrings(item,tokens){
    const found=new Map(),records=item?.matchRecords||[item?.displayRecord,item?.record];
    const walk=(value,path='')=>{
        if(value===null||value===undefined)return;
        if(typeof value==='object'){
            if(Array.isArray(value)){value.forEach((child,index)=>walk(child,path?path+'['+index+']':'['+index+']'));return}
            for(const [key,child] of Object.entries(value)){
                const next=path?path+'.'+key:key;
                walk(child,next);
            }
            return;
        }
        if(typeof value!=='string'&&typeof value!=='number'&&typeof value!=='boolean')return;
        const raw=String(value).trim();if(!raw)return;
        const matchingTokens=tokens.filter(token=>gvSearchNormalizeMatchText(raw).includes(token));
        const pathMatches=tokens.some(token=>gvSearchNormalizeMatchText(path).includes(token));
        if(!matchingTokens.length&&!pathMatches)return;
        const label=path?path+': '+raw:raw;
        const key=gvSearchNormalizeMatchText(label);
        if(!found.has(key))found.set(key,{label,score:matchingTokens.length});
    };
    records.forEach(record=>walk(record));
    return [...found.values()].sort((a,b)=>b.score-a.score||a.label.length-b.label.length)
        .slice(0,3).map(item=>item.label);
}

const GV_SEARCH_RESULT_LIMIT=24;
const GV_SEARCH_RENDER_DEBOUNCE_MS=120;
let gvSearchRenderTimer=0;
let gvSearchRenderGeneration=0;

function gvClearSearchResultImages(){
    gvSearchResults.querySelectorAll('img').forEach(img=>{
        try{img.onload=null;img.onerror=null;img.removeAttribute('src');img.removeAttribute('srcset')}catch(_){}
    });
    gvSearchResults.replaceChildren();
}

async function gvSearchRender(query){
    const renderGeneration=++gvSearchRenderGeneration;
    const q=String(query||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
    gvClearSearchResultImages();
    if(!q){gvSearchResults.style.display='none';return}
    gvSearchResults.style.display='block';
    const loading=document.createElement('div');loading.className='gv-search-empty';loading.textContent='SEARCHING ALL SURVEY CATALOGS…';gvSearchResults.appendChild(loading);
    await gvEnsureFullSearchIndex();
    if(renderGeneration!==gvSearchRenderGeneration)return;
    await gvSurveyThumbnailPackReady;
    if(renderGeneration!==gvSearchRenderGeneration)return;
    gvClearSearchResultImages();
    if(gvFullSearchIndexError){
        const failed=document.createElement('div');failed.className='gv-search-empty';
        failed.textContent='SEARCH CATALOGS FAILED: '+String(gvFullSearchIndexError.message||'CHECK CONNECTION AND RETRY').slice(0,150);
        gvSearchResults.appendChild(failed);
        console.error('GV SEARCH NOT READY; no false NO GALAXIES FOUND message shown');
        return;
    }
    const tokens=q.split(/\s+/).filter(Boolean);
    const matches=gvSearchIndex
        .filter(item=>tokens.every(token=>item.text.includes(token)||JSON.stringify(item.displayRecord||{}).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(token)||JSON.stringify(item.record||{}).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(token))||gvSearchCoordinatePairMatches(item.displayRecord,tokens)||gvSearchCoordinatePairMatches(item.record,tokens))
        .sort((a,b)=>{
            const rank=item=>{
                const record=item.displayRecord||item.record;
                const primary=[record?.name,record?.commonName,record?.displayName,record?.title,record?.designation,record?.description,record?.caption,record?.objectName].map(value=>String(value||'').toLowerCase()).join(' ');
                const allNames=gvSearchRecordNames(record).join(' ');
                let score=0;
                if(tokens.every(token=>primary.includes(token)))score+=1000;
                else score+=tokens.filter(token=>primary.includes(token)).length*100;
                if(tokens.every(token=>allNames.includes(token)))score+=200;
                if(tokens.every(token=>gvSearchDisplayName(record).toLowerCase().startsWith(token)))score+=100;
                return score;
            };
            const scoreDiff=rank(b)-rank(a);
            if(scoreDiff)return scoreDiff;
            return gvSearchDisplayName(a.displayRecord||a.record).localeCompare(gvSearchDisplayName(b.displayRecord||b.record));
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
            const searchItem=visibleMatches.find(item=>item.record===record);
            const candidates=gvSurveyThumbnailCandidates(searchItem?.thumbnailRecord||record,provider);
            let thumbIndex=0;
            const loadThumb=()=>{
                if(renderGeneration!==gvSearchRenderGeneration)return;
                const src=candidates[thumbIndex++];
                if(!src){thumb.removeAttribute('src');thumb.style.visibility='hidden';return}
                thumb.style.visibility='visible';
                thumb.src=src;
            };
            thumb.onerror=loadThumb;loadThumb();thumbWrap.appendChild(thumb);
            const icon=document.createElement('img');icon.className='gv-search-result-icon';
            icon.src=GV_SURVEY_PROVIDER_META[provider]?.icon||'';icon.alt=provider+' provider';icon.draggable=false;
            const matchedItem=visibleMatches.find(item=>item.record===record);
            const copy=document.createElement('span');copy.className='gv-search-result-copy';
            const name=document.createElement('span');name.className='gv-search-result-name';name.textContent=gvSearchDisplayName(matchedItem?.displayRecord||record);
            const matchLine=document.createElement('span');matchLine.className='gv-search-result-match';
            const matchedStrings=gvSearchMatchedStrings(matchedItem,tokens);
            matchLine.textContent=matchedStrings.length?matchedStrings.join(' • '):(tokens.length===2&&gvSearchCoordinatePairMatches(matchedItem?.displayRecord||record,tokens)?'MATCHED COORDINATES':'MATCHED CATALOG RECORD');
            matchLine.title=matchLine.textContent;
            copy.append(name,matchLine);
            row.append(thumbWrap,copy,icon);
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
        gvSearchRender(query).catch(error=>{
            gvClearSearchResultImages();
            gvSearchResults.style.display='block';
            const failed=document.createElement('div');
            failed.className='gv-search-empty';
            failed.textContent='SEARCH FAILED: '+String(error?.message||error||'UNKNOWN ERROR').slice(0,150);
            gvSearchResults.appendChild(failed);
            console.error('GV SEARCH RENDER FAILED',error);
        });
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
if(gvSearchPanel){
    // Replace any prior tile with this invocation's tile so the visible input
    // always owns the input listener attached above (never a detached input).
    const previousSearchTile=gvSearchPanel.querySelector('#gv-catalog-search-tile');
    if(previousSearchTile)previousSearchTile.remove();
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
                const response=await fetch(url,{cache:'no-store'});
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
// GV028: move the existing three-row HUD as one untouched unit and add TRIP as a sibling.
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
const DIRECT_HD_LAYER='GV_DIRECT_HD_0059';
let directHdLayerSequence=0;
let directHdLayerName=DIRECT_HD_LAYER;
const CANVAS_IMAGE_PROXY='https://gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev/api/image?url=';
const MAX_BLEND_DIMENSION=1024;
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
// BUILD 0007 — capture Android touch gestures at document level so Aladin's
// canvas handlers cannot swallow the second pointer before Galaxy Viewer sees it.
const gvSkyPinch={startGap:0,startFov:0,active:false};
function gvSkyTouchGap(touches){
    if(!touches||touches.length<2)return 0;
    return Math.hypot(touches[0].clientX-touches[1].clientX,touches[0].clientY-touches[1].clientY);
}
function gvSkyReadFov(){
    const value=aladin.getFov?.();
    return Number(Array.isArray(value)?value[0]:(value?.x??value?.fovX??value));
}
// BUILD 0012 ROOT-CAUSE FIX: do not capture and stopImmediatePropagation on
// touchstart/touchmove. Aladin Lite 3.8.2 already implements native pinch zoom;
// the previous document-capture handler intercepted both touch events before
// Aladin could process them, and the custom path did not reliably reach the
// active HD image surface. Keep touch gestures enabled for Aladin's own handler.
if(gvSkyRoot){
    gvSkyRoot.style.touchAction='none';
    gvSkyRoot.querySelectorAll('canvas').forEach(canvas=>{canvas.style.touchAction='none'});
}
console.info('GV0012 PINCH HANDLER: delegated to Aladin Lite native touch implementation');

let directHdObjectUrl=null;
let directHdStaged=null;
let directHdPresentationObjectUrl=null;
// BUILD 0031: three-row HUD limits image readiness probes to three galaxies; these are not in the HD overlay URL registry.
const gvCleanImageObjectUrls=[];
function gvTrackCleanImageObjectUrl(url){
    const value=String(url||'').trim();if(!value||gvCleanImageObjectUrls.includes(value))return value;
    gvCleanImageObjectUrls.push(value);
    while(gvCleanImageObjectUrls.length>2){
        const staleIndex=gvCleanImageObjectUrls.findIndex(item=>item!==directHdPresentationObjectUrl);
        if(staleIndex<0)break;
        const [stale]=gvCleanImageObjectUrls.splice(staleIndex,1);
        try{URL.revokeObjectURL(stale)}catch(_){}
    }
    return value;
}
function gvReleaseCleanImageObjectUrl(url){
    const value=String(url||'').trim();if(!value)return;
    const index=gvCleanImageObjectUrls.indexOf(value);if(index>=0)gvCleanImageObjectUrls.splice(index,1);
    try{URL.revokeObjectURL(value)}catch(_){}
    if(directHdPresentationObjectUrl===value)directHdPresentationObjectUrl=null;
}
const GV_HD_RETIRE_FOV=50;
let gvHdTravelRetired=false;
// BUILD 0004 — bounded HD resource ownership: maximum three tracked object URLs; stale resources are explicitly revoked.
// BUILD 0091: HD URLs are bounded and navigation history is capped below.
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
// BUILD 0032 — mandatory bounded image cleanup, targeted CacheStorage purge, and per-arrival memory diagnostics.
const GV_MEMORY_DIAGNOSTIC_MS=30*1000;
let gvMemoryDiagnosticTimer=0;
function gvMemoryDiagnosticSnapshot(reason='periodic'){
    let heap=null;
    try{const m=performance?.memory;if(m&&Number.isFinite(m.usedJSHeapSize))heap={usedMB:Math.round(m.usedJSHeapSize/1048576),totalMB:Math.round(m.totalJSHeapSize/1048576),limitMB:Math.round(m.jsHeapSizeLimit/1048576)}}catch(_){}
    let imageNodes=0,canvasNodes=0,searchThumbnails=0;
    try{imageNodes=document.querySelectorAll('img').length;canvasNodes=document.querySelectorAll('canvas').length;searchThumbnails=document.querySelectorAll('.gv-search-result-thumb img').length}catch(_){}
    let pendingPrewarm=!!gvNextTripPrewarm;
    let navigatorThumbnails=null,providerArtworkCache=null;try{if(typeof window.GV_NAVIGATOR_MEMORY_SNAPSHOT==='function')navigatorThumbnails=window.GV_NAVIGATOR_MEMORY_SNAPSHOT()}catch(_){}try{if(window.GVProviderArtwork&&typeof window.GVProviderArtwork.cacheDiagnostics==='function')providerArtworkCache=window.GVProviderArtwork.cacheDiagnostics()}catch(_){}const snapshot={build:GV200001_BUILD,reason,at:Math.round(performance.now()),heap,hd:typeof gvHdResourceSnapshot==='function'?gvHdResourceSnapshot():null,prewarm:pendingPrewarm,prewarmGeneration:typeof gvNextTripPrewarmGeneration!=='undefined'?gvNextTripPrewarmGeneration:null,prewarmPrepared:typeof gvNextTripPrewarm!=='undefined'&&!!gvNextTripPrewarm?.preparedValue,objectUrls:typeof gvHdObjectUrls!=='undefined'?gvHdObjectUrls.length:null,cleanObjectUrls:typeof gvCleanImageObjectUrls!=='undefined'?gvCleanImageObjectUrls.length:null,constellationArtwork:typeof gvConstellationArtworkPrewarm!=='undefined'?gvConstellationArtworkPrewarm.size:null,providerOrigins:typeof gvProviderPortalOrigins!=='undefined'?gvProviderPortalOrigins.length:null,images:imageNodes,searchThumbnails,canvases:canvasNodes,navigatorThumbnails,providerArtworkCache,travel:!!gvNavigationTravelActive,hipsSuspended:!!window.GV_NAV_HIPS_FETCH_SUSPENDED};
    console.info('GV MEMORY WORKLOAD SNAPSHOT',snapshot);
    return snapshot;
}

const GV_IMAGE_CACHE_NAME_RE=/(survey|thumbnail|galaxy[-_]?image|image[-_]?cache|avm[-_]?image)/i;
let gvImageCachePurgePromise=Promise.resolve();
async function gvClearObsoleteImageCaches(reason='galaxy-arrival'){
    // CacheStorage is script-managed storage; the browser's private HTTP cache is not exposed to page JavaScript.
    if(!('caches' in window)||typeof caches.keys!=='function')return {supported:false,deleted:0,reason};
    const run=async()=>{
        let deleted=0;
        try{
            const names=await caches.keys();
            for(const name of names){
                if(!GV_IMAGE_CACHE_NAME_RE.test(name))continue;
                try{if(await caches.delete(name))deleted++}catch(error){console.warn('GV IMAGE CACHE DELETE FAILED',name,error)}
            }
        }catch(error){console.warn('GV IMAGE CACHE ENUMERATION FAILED',error)}
        const result={supported:true,deleted,reason,at:Math.round(performance.now())};
        console.info('GV IMAGE CACHE PURGE',result);
        return result;
    };
    gvImageCachePurgePromise=gvImageCachePurgePromise.then(run,run);
    return gvImageCachePurgePromise;
}
function gvMandatoryImageMemorySweep(reason='galaxy-arrival'){
    // Transient canvases are zeroed; decoded bitmaps are closed in gvLoadGate2MImage's finally block.
    try{
        for(const canvas of document.querySelectorAll('canvas[data-gv-transient="1"]')){canvas.width=0;canvas.height=0;canvas.remove()}
    }catch(_){}
    gvMemoryDiagnosticSnapshot('arrival:'+reason);
    gvClearObsoleteImageCaches(reason).then(result=>console.info('GV MEMORY SWEEP CACHE OUTCOME',{reason,...result})).catch(error=>console.warn('GV MEMORY SWEEP CACHE OUTCOME FAILED',{reason,error:String(error)}));
}

function gvStartMemoryDiagnostics(){
    if(gvMemoryDiagnosticTimer)return;
    gvMemoryDiagnosticSnapshot('startup');
    gvMemoryDiagnosticTimer=setInterval(()=>gvMemoryDiagnosticSnapshot('30-second'),GV_MEMORY_DIAGNOSTIC_MS);
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
const GV_AVM_RUNTIME_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0006.json';
let gvAvmRuntimePromise=null;
function gvCanonicalAvmImageUrl(value){
    return String(value??'').trim().replace(/^https?:\/\/www\.eso\.org\/public\/archives\/images\/screen\//i,'https://cdn.eso.org/images/screen/');
}
async function gvLoadAvmRuntimeCatalog(){
    if(!gvAvmRuntimePromise){
        gvAvmRuntimePromise=fetch(fresh(GV_AVM_RUNTIME_CATALOG_URL)+'&gv-json-integrity=20261023-0006',{cache:'no-store'})
            .then(response=>{if(!response.ok)throw new Error('GV AVM RUNTIME CATALOG HTTP '+response.status);return response.json()})
            .then(payload=>{
                const records=Array.isArray(payload)?payload:payload?.records;
                if(!Array.isArray(records)||records.length===0)throw new Error('GV AVM RUNTIME CATALOG INVALID: expected non-empty records from 0004');
                const byUrl=new Map(),byId=new Map();
                for(const record of records){
                    const url=gvCanonicalAvmImageUrl(record?.imageUrl).toLowerCase();
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
    const url=gvCanonicalAvmImageUrl(directHdUrl(destination)).toLowerCase();
    const id=String(destination?.archiveId||destination?.id||destination?.providerId||'').trim().toLowerCase();
    const record=catalog.byUrl.get(url)||catalog.byId.get(id);
    if(!record)throw new Error('GV AVM RUNTIME RECORD MISSING: '+(url||id));
    // BUILD 0035 targeted correction: ESO potw1007a / NGC 4945 is rendered 90 deg off.
    // Apply the camera-convention correction only to this archive image.
    // NGC 7331 Spitzer ssc2004-12a1: published source image is 1239x805 px and 12.6x8.2 arcmin.
    // The catalog's 2.68x2.01 arcmin describes the galaxy footprint, not the full image footprint;
    // the runtime scalar FOV had been copied to both axes, causing a horizontally compressed registration.
    const effectiveRecord=id==='potw1007a'
        ?{...record,aladinRotation:45}
        :(id==='ssc2004-12a1'||/ssc2004-12a1/i.test(url))
            ?{...record,fovXDegrees:0.21,fovYDegrees:8.2/60,fovDegrees:0.21,
                fieldOfViewDegrees:{widthDegrees:0.21,heightDegrees:8.2/60,effectiveDegrees:Math.sqrt(0.21*(8.2/60))},
                referenceDimension:[1239,805]}
            :record;
    const recordUrl=gvCanonicalAvmImageUrl(effectiveRecord?.imageUrl).toLowerCase();
    if(url&&recordUrl!==url)throw new Error('GV AVM RUNTIME IMAGE MISMATCH: destination='+url+' record='+recordUrl);
    return effectiveRecord;
}
function gvSyntheticWcsFromRuntimeRecord(record,width,height){
    const ra=Number(record?.ra),dec=Number(record?.dec);
    const fovX=Number(record?.fovXDegrees??record?.fieldOfViewDegrees?.widthDegrees??record?.fovDegrees);
    const fovY=Number(record?.fieldOfViewDegrees?.heightDegrees??record?.fovYDegrees??record?.fovHeightDegrees??record?.fovDegrees);
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
    const fovX=Number(record?.fovXDegrees??record?.fieldOfViewDegrees?.widthDegrees??record?.fovDegrees);
    const fovY=Number(record?.fieldOfViewDegrees?.heightDegrees??record?.fovYDegrees??record?.fovHeightDegrees??record?.fovDegrees);
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

function directHdUrl(destination){return gvCanonicalAvmImageUrl(destination?.selectedImageUrl??destination?.imageUrl??destination?.hdUrl??'')}
function gvCrossfadeOpacity(){
    const raw=Number(crossFadeInput.value);
    const slider=Math.max(0,Math.min(100,Number.isFinite(raw)?raw:0));
    return 1-slider/100;
}
function updateCrossFadeThumb(){
    const v=Math.max(0,Math.min(100,Number(crossFadeInput.value||0)));
    crossFadeControl.thumb.style.top=`${crossFadeControl.rail.offsetTop+((100-v)/100)*crossFadeControl.rail.offsetHeight}px`;
}
function applyDirectHdOpacity(){
    const raw=Number(crossFadeInput.value);
    const sliderValue=Math.max(0,Math.min(100,Number.isFinite(raw)?raw:0));
    const value=gvCrossfadeOpacity();
    const target=directHdOverlay;
    let method='none',readback=null;
    if(target){
        try{
            if(typeof target.setOpacity==='function'){target.setOpacity(value);method='setOpacity'}
            else if(typeof target.setAlpha==='function'){target.setAlpha(value);method='setAlpha'}
            else if(typeof target.setOptions==='function'){target.setOptions({opacity:value});method='setOptions'}
            readback=typeof target.getOpacity==='function'?target.getOpacity():
                (typeof target.getAlpha==='function'?target.getAlpha():target.opacity??null);
        }catch(error){console.warn('GV CROSSFADE OPACITY APPLY FAILED',{layer:directHdLayerName,value,error})}
    }
    const detail={build:GV200001_BUILD,slider:sliderValue,requestedOpacity:value,layerName:directHdLayerName,activeLayerFound:!!target,method,readback};
    if(!target||(readback!==null&&Math.abs(Number(readback)-value)>0.001))console.warn('GV CROSSFADE OPACITY READBACK MISMATCH',detail);
    else console.info('GV CROSSFADE OPACITY APPLIED',detail);
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
// ROLL 0062 — ZOOM TOUCH NO-MAN'S-LAND.
// Extend the zoom control's hit target by 2/3 of its measured height above and below.
// The shield only arbitrates touches in the corridor; it does not cover the slider's visual UI.
(function gvInstallZoomTouchCorridor(){
    const host=document.getElementById('aladin-cosmic-command-test');
    if(!host||!zoomControl?.panel)return;
    const panel=zoomControl.panel;
    const shield=document.createElement('div');
    shield.id='gv-zoom-touch-corridor';
    Object.assign(shield.style,{position:'absolute',zIndex:'7311',background:'transparent',pointerEvents:'auto',touchAction:'none'});
    const place=()=>{
        const h=panel.getBoundingClientRect().height||158;
        const extra=h*(2/3);
        const hostRect=host.getBoundingClientRect(),r=panel.getBoundingClientRect();
        shield.style.left=(r.left-hostRect.left)+'px';
        shield.style.top=(r.top-hostRect.top-extra)+'px';
        shield.style.width=r.width+'px';
        shield.style.height=(h+2*extra)+'px';
    };
    // Keep the transparent corridor behind the actual control so the slider remains usable.
    host.insertBefore(shield,panel);
    shield.addEventListener('pointerdown',e=>{
        if(panel.contains(e.target))return;
        e.preventDefault();e.stopPropagation();
    },{capture:true});
    shield.addEventListener('touchstart',e=>{
        if(panel.contains(e.target))return;
        e.preventDefault();e.stopPropagation();
    },{capture:true,passive:false});
    window.addEventListener('resize',place,{passive:true});
    place();
    console.info('GV0062 ZOOM TOUCH CORRIDOR INSTALLED',{extraFraction:2/3});
})();
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
setInterval(()=>{if(document.visibilityState==='visible')gvSyncFovReadout()},250);

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
// RELEASE BUILD 0018: suspend HiPS tile traffic synchronously at navigation start and for slider, wheel, and pinch zoom.
// BUILD 0026 TEST: archive-style manual zoom behavior.
// Keep expensive distance/ruler work quiet during a native or custom zoom gesture,
// but do not suspend HiPS traffic or force an artificial FOV nudge on release.
function gvSuspendHiPSForManualZoom(){
    if(window.GV_NAV_HIPS_ZOOM_RESUME_TIMER){clearTimeout(window.GV_NAV_HIPS_ZOOM_RESUME_TIMER);window.GV_NAV_HIPS_ZOOM_RESUME_TIMER=0;}
    gvZoomInteractionActive=true;
}
function gvResumeHiPSAfterManualZoom(){
    if(window.GV_NAV_HIPS_ZOOM_RESUME_TIMER)clearTimeout(window.GV_NAV_HIPS_ZOOM_RESUME_TIMER);
    window.GV_NAV_HIPS_ZOOM_RESUME_TIMER=setTimeout(()=>{
        window.GV_NAV_HIPS_ZOOM_RESUME_TIMER=0;
        gvZoomInteractionActive=false;
        gvScheduleEarthDistanceAfterZoom();
    },350);
}
function gvSetZoomCommand(command){
    const requested=Math.max(-1,Math.min(1,Number(command)||0));
    // BUILD 0030: zoom-out is 30% gentler; preserve the full zoom-in range.
    zoomCommand=requested;
    zoomControl.thumb.style.top=`${zoomControl.rail.offsetTop+((zoomCommand+1)/2)*zoomControl.rail.offsetHeight}px`;
}
// BUILD 0026 TEST: archive-style fixed exponential step per animation frame.
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
                    aladin.setFov(a.target);const done=a.resolve;gvAutoZoom=null;gvSetZoomCommand(0);gvZoomInteractionActive=false;gvScheduleEarthDistanceAfterZoom();done(true);return;
                }
            }
            // BUILD 0026 TEST: restore the archived RC-V1.0.0.3 per-frame exponential FOV step.
            aladin.setFov(Math.max(.0001,Math.min(360,current*Math.exp(-zoomCommand*.018))));
        }
    }catch(error){console.error('GV ZOOM SLIDER FRAME FAILED',{build:GV200001_BUILD,command:zoomCommand,error:String(error)});}
    zoomFrame=requestAnimationFrame(zoomStep);
}
function gvSettleAutoZoom(result=false){
    if(!gvAutoZoom)return;
    const done=gvAutoZoom.resolve;gvAutoZoom=null;gvZoomInteractionActive=false;gvScheduleEarthDistanceAfterZoom();
    try{done(result)}catch(_){}
}
function gvEnergizeZoomJoystick(command,targetFov,{attackMs=500,landingMs=2500,approachMs=500,linearLanding=true,onApproach=null}={}){
    const target=Number(targetFov),direction=Math.sign(Number(command));
    if(!Number.isFinite(target)||target<=0||!direction)return Promise.resolve(false);
    const raw=aladin.getFov?.(),start=Number(Array.isArray(raw)?raw[0]:raw);
    if(!Number.isFinite(start)||start<=0)return Promise.resolve(false);
    gvSettleAutoZoom(false);
    gvZoomInteractionActive=true;
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
        gvZoomInteractionActive=true;
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
            aladin.setFov(elapsed>=totalMs?target:start*Math.exp(Math.log(target/start)*progress));
            if(elapsed<totalMs)requestAnimationFrame(frame);
            else{gvSetZoomCommand(0);gvZoomInteractionActive=false;gvScheduleEarthDistanceAfterZoom();resolve(true)}
        }
        requestAnimationFrame(frame);
    });
}
function setZoomCommandFromY(clientY){
    gvSuspendHiPSForManualZoom();
    gvZoomInteractionActive=true;
    const r=zoomControl.rail.getBoundingClientRect();
    if(!r.height)return;
    gvSettleAutoZoom(false);
    gvSetZoomCommand(((clientY-(r.top+r.height/2))/(r.height/2)));
    if(!zoomFrame)zoomFrame=requestAnimationFrame(zoomStep);
}
function releaseZoom(){
    gvResumeHiPSAfterManualZoom();
    gvSettleAutoZoom(false);
    gvZoomInteractionActive=false;
    gvScheduleEarthDistanceAfterZoom();
    gvSetZoomCommand(0);
    if(zoomFrame){cancelAnimationFrame(zoomFrame);zoomFrame=0}
    zoomControl.thumb.style.top=`${zoomControl.rail.offsetTop+zoomControl.rail.offsetHeight/2}px`;
}
for(const ev of ['pointerdown','pointermove'])zoomControl.hit.addEventListener(ev,e=>{if(ev==='pointermove'&&e.buttons===0)return;e.preventDefault();e.stopPropagation();setZoomCommandFromY(e.clientY)},{passive:false});
for(const ev of ['pointerup','pointercancel','pointerleave'])zoomControl.hit.addEventListener(ev,e=>{e.stopPropagation();releaseZoom()},{passive:true});

// BUILD 0018: extend the existing HiPS fetch gate to native Aladin wheel and pinch zoom.
// Capture only zoom gestures inside the Aladin viewer; do not intercept clicks or panning.
// Debounced resume is handled by gvResumeHiPSAfterManualZoom() (350 ms after the last gesture).
let gvNativePinchZoomActive=false;
compassRoot.addEventListener('wheel',e=>{
    if(!compassRoot.contains(e.target))return;
    gvSuspendHiPSForManualZoom();
    gvResumeHiPSAfterManualZoom();
},{capture:true,passive:true});
compassRoot.addEventListener('touchstart',e=>{
    if(e.touches&&e.touches.length>=2){
        gvNativePinchZoomActive=true;
        gvSuspendHiPSForManualZoom();
    }
},{capture:true,passive:true});
compassRoot.addEventListener('touchmove',e=>{
    if(e.touches&&e.touches.length>=2){
        gvNativePinchZoomActive=true;
        gvSuspendHiPSForManualZoom();
        gvResumeHiPSAfterManualZoom();
    }
},{capture:true,passive:true});
const gvFinishNativePinchZoom=e=>{
    if(gvNativePinchZoomActive&&(!e.touches||e.touches.length<2)){
        gvNativePinchZoomActive=false;
        gvResumeHiPSAfterManualZoom();
    }
};
compassRoot.addEventListener('touchend',gvFinishNativePinchZoom,{capture:true,passive:true});
compassRoot.addEventListener('touchcancel',gvFinishNativePinchZoom,{capture:true,passive:true});


// Parse common raster dimensions from headers before allocating decoded pixels.
async function gvEncodedImageDimensions(blob){
    const buffer=await blob.slice(0,Math.min(blob.size,2*1024*1024)).arrayBuffer();
    const b=new Uint8Array(buffer),n=b.length;
    if(n>=24&&b[0]===137&&b[1]===80&&b[2]===78&&b[3]===71){
        const v=new DataView(buffer);return {width:v.getUint32(16),height:v.getUint32(20)};
    }
    if(n>=30&&b[0]===82&&b[1]===73&&b[2]===70&&b[3]===70&&b[8]===87&&b[9]===69&&b[10]===66&&b[11]===80){
        const tag=String.fromCharCode(b[12],b[13],b[14],b[15]);
        if(tag==='VP8X')return {width:1+b[24]+(b[25]<<8)+(b[26]<<16),height:1+b[27]+(b[28]<<8)+(b[29]<<16)};
        if(tag==='VP8L'&&n>=25){const bits=(b[21]|(b[22]<<8)|(b[23]<<16)|(b[24]<<24))>>>0;return {width:(bits&0x3fff)+1,height:((bits>>>14)&0x3fff)+1};}
        if(tag==='VP8 '&&n>=30){for(let i=20;i<n-9;i++)if(b[i]===0x9d&&b[i+1]===0x01&&b[i+2]===0x2a)return {width:((b[i+3]|(b[i+4]<<8))&0x3fff),height:((b[i+5]|(b[i+6]<<8))&0x3fff)};}
    }
    if(n>=4&&b[0]===0xff&&b[1]===0xd8){
        let i=2;
        while(i+4<n){
            if(b[i]!==0xff){i++;continue;}
            while(i<n&&b[i]===0xff)i++;
            if(i>=n)break;
            const marker=b[i++];
            if(marker===0xd8||marker===0xd9||(marker>=0xd0&&marker<=0xd7))continue;
            if(i+2>n)break;
            const length=(b[i]<<8)|b[i+1];
            if(length<2||i+length>n)break;
            if([0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf].includes(marker)&&length>=7)
                return {height:(b[i+3]<<8)|b[i+4],width:(b[i+5]<<8)|b[i+6]};
            i+=length;
        }
    }
    throw new Error('UNSUPPORTED OR UNREADABLE IMAGE DIMENSIONS; refusing full-size decode');
}
async function gvLoadGate2MImage(url,destination=null,record=null,signal=null){
    if(typeof createImageBitmap!=='function')throw new Error('createImageBitmap unavailable');
    const attempts=[url,CANVAS_IMAGE_PROXY+encodeURIComponent(url)+'&consumer=gv0037'];
    let last='';
    for(const source of attempts){
        try{
            if(signal?.aborted)throw new DOMException('PREWARM ABORTED','AbortError');
            const response=await fetch(source,{mode:'cors',credentials:'omit',cache:'no-store',redirect:'follow',signal:signal||undefined});
            if(!response.ok)throw new Error('HTTP '+response.status);
            const originalBlob=await response.blob();
            if(!originalBlob||originalBlob.size<=0)throw new Error('EMPTY IMAGE BLOB');
            const encoded=await gvEncodedImageDimensions(originalBlob);
            const sourceW=Number(encoded.width),sourceH=Number(encoded.height);
            if(!(sourceW>0&&sourceH>0))throw new Error('INVALID ENCODED IMAGE DIMENSIONS');
            const sourceMax=Math.max(sourceW,sourceH);
            const scale=Math.min(1,MAX_BLEND_DIMENSION/sourceMax);
            const targetW=Math.max(1,Math.round(sourceW*scale)),targetH=Math.max(1,Math.round(sourceH*scale));
            // Decode directly to the bounded dimensions; never create a full-size RGBA bitmap first.
            let bitmap=await createImageBitmap(originalBlob,scale<1?{resizeWidth:targetW,resizeHeight:targetH,resizeQuality:'high'}:undefined);
            let workingBitmap=null,canvas=null,resizeCanvas=null;
            try{
                workingBitmap=bitmap;let w=bitmap.width,h=bitmap.height;
                if(sourceMax>MAX_BLEND_DIMENSION){
                    if(w>MAX_BLEND_DIMENSION||h>MAX_BLEND_DIMENSION)throw new Error('DECODE RESIZE LIMIT NOT HONORED');
                    console.info('GV HD DECODE-BOUNDED',{source:[sourceW,sourceH],target:[w,h]});
                }
                // Decode-time resize already enforced the pixel budget; no second bitmap copy.

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
                return {blob:vignetteBlob,originalBlob,width:w,height:h};
            }finally{
                if(workingBitmap&&workingBitmap!==bitmap){try{workingBitmap.close?.()}catch(_){}}
                if(bitmap){try{bitmap.close?.()}catch(_){}}
                for(const tempCanvas of [canvas,resizeCanvas]){if(tempCanvas){try{tempCanvas.width=0;tempCanvas.height=0}catch(_){}}}
            }
        }catch(error){if(signal?.aborted||error?.name==='AbortError')throw error;last=String(error?.message||error||'')}
    }
    throw new Error('GATE 2M IMAGE SOURCE FAILED: '+last);
}
let gvHdPreparationQueue=Promise.resolve();
async function gvPrepareDirectHd(destination,recordPromise=gvRuntimeAvmRecord(destination),signal=null){
    const run=()=>{if(signal?.aborted)throw new DOMException('PREWARM ABORTED','AbortError');return gvPrepareDirectHdUnlocked(destination,recordPromise,signal)};
    const pending=gvHdPreparationQueue.then(run,run);
    gvHdPreparationQueue=pending.then(()=>undefined,()=>undefined);
    return pending;
}
async function gvPrepareDirectHdUnlocked(destination,recordPromise=gvRuntimeAvmRecord(destination),signal=null){
    if(signal?.aborted)throw new DOMException('PREWARM ABORTED','AbortError');
    const record=await recordPromise;
    const url=directHdUrl(destination);
    if(!url)throw new Error('GV DESTINATION IMAGE URL MISSING');
    const fovX=Number(record.fovXDegrees??record.fieldOfViewDegrees?.widthDegrees??record.fovDegrees);
    const fovY=Number(record.fieldOfViewDegrees?.heightDegrees??record.fovYDegrees??record.fovHeightDegrees??record.fovDegrees);
    const rotation=Number(record.aladinRotation??record.spatialRotationDeg);
    const prepStarted=performance.now();
    const raster=await gvLoadGate2MImage(url,destination,record,signal);
    if(signal?.aborted)throw new DOMException('PREWARM ABORTED','AbortError');
    const imageObjectUrl=URL.createObjectURL(raster.blob);gvTrackHdObjectUrl(imageObjectUrl);
    const cleanImageObjectUrl=gvTrackCleanImageObjectUrl(URL.createObjectURL(raster.originalBlob));
    const displayWcs=gvSyntheticWcsFromRuntimeRecord(record,raster.width,raster.height);
    const imageCenter=gvTanPixelToWorld(displayWcs,(raster.width+1)/2,(raster.height+1)/2);
    const prepared={destination,record,imageUrl:url,imageObjectUrl,cleanImageObjectUrl,displayWcs,imageCenter,rotation,finalFov:Math.max(fovX,fovY)*1.0};
    console.info('GV HD PREPARED',{ms:Math.round(performance.now()-prepStarted),name:destination?.name||destination?.objectName||'',resources:gvHdResourceSnapshot()});
    return prepared;
}
function gvInstallPreparedHd(prepared,{stage=false}={}){
    if(!stage&&prepared?.cleanImageObjectUrl)directHdPresentationObjectUrl=prepared.cleanImageObjectUrl;
    if(stage&&directHdStaged&&directHdStaged.destination!==prepared?.destination){
        const stale=directHdStaged;directHdStaged=null;
        try{aladin.removeImageLayer?.(stale.layerName)}catch(_){}
        if(stale.objectUrl!==directHdObjectUrl)gvReleaseHdObjectUrl(stale.objectUrl);
    }
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
        name:layerName,imgFormat:'png',wcs:displayWcs,opacity:stage?0:1,
        successCallback:()=>{
            if(settled)return;settled=true;
            if(activeDestination!==destination){
                try{aladin.removeImageLayer?.(layerName)}catch(_){}
                gvReleaseHdObjectUrl(imageObjectUrl);
                resolveReady(false);
                return;
            }
            if(stage){
                directHdStaged={overlay:layer,destination,objectUrl:imageObjectUrl,cleanImageObjectUrl:prepared?.cleanImageObjectUrl||null,displayWcs,layerName,previous};
                console.info('GV HD LAYER STAGED BEFORE TRAVEL',{layer:layerName,previousLayer:previous.layerName||null});
                resolveReady(true);return;
            }
            directHdOverlay=layer;
            directHdDestination=destination;
            directHdObjectUrl=imageObjectUrl;
            directHdDisplayWcs=displayWcs;
            directHdLayerName=layerName;
            applyDirectHdOpacity();
            retirePrevious();
            console.info('GV HD LAYER HANDOFF COMPLETE',{layer:layerName,previousLayer:previous.layerName||null});
            gvMandatoryImageMemorySweep('hd-layer-handoff');
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
function gvActivateStagedHd(destination){
    const staged=directHdStaged;
    if(!staged||staged.destination!==destination)return false;
    try{
        if(typeof staged.overlay?.setOpacity==='function')staged.overlay.setOpacity(1);
        else if(typeof staged.overlay?.setAlpha==='function')staged.overlay.setAlpha(1);
        directHdOverlay=staged.overlay;
        directHdPresentationObjectUrl=staged.cleanImageObjectUrl||directHdPresentationObjectUrl;
        directHdDestination=staged.destination;
        directHdObjectUrl=staged.objectUrl;
        directHdDisplayWcs=staged.displayWcs;
        directHdLayerName=staged.layerName;
        directHdStaged=null;
        gvHdTravelRetired=false;
        applyDirectHdOpacity();
        const previous=staged.previous;
        if(previous?.layerName&&previous?.overlay&&previous.layerName!==staged.layerName){try{aladin.removeImageLayer?.(previous.layerName)}catch(_){}}
        if(previous?.objectUrl&&previous.objectUrl!==staged.objectUrl)gvReleaseHdObjectUrl(previous.objectUrl);
        console.info('GV HD STAGED LAYER ACTIVATED AT ARRIVAL',{layer:staged.layerName,previousLayer:previous?.layerName||null});
        gvMandatoryImageMemorySweep('staged-hd-arrival');
        return true;
    }catch(error){console.error('GV HD STAGED LAYER ACTIVATION FAILED',error);return false}
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
        const layer=A.image(objectUrl,{name:directHdLayerName,imgFormat:'png',wcs:directHdDisplayWcs,opacity:1,successCallback:()=>{if(directHdObjectUrl!==objectUrl)return;directHdOverlay=layer;gvHdTravelRetired=false;applyDirectHdOpacity();console.info('GV HD RESTORED — EXISTING OBJECT URL REINSTALLED')},errorCallback:error=>console.warn('GV HD RESTORE FAILED',error)});
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
function gvSetTravelConstellationGlow(constellationName,ra,dec,active){
    // Travel beacons must not depend on the user opening the CONSTELLATIONS menu.
    // Lazily mount the overlay on the first trip; keep its ordinary line layer off.
    if(!gvConstellationPromise){
        if(!window.GalaxyViewerConstellationOverlay?.mount){
            console.error('GV CONSTELLATION TRAVEL GLOW UNAVAILABLE: overlay export missing');
            return;
        }
        gvConstellationPromise=window.GalaxyViewerConstellationOverlay.mount(aladin).then(layer=>{
            layer.setEnabled(false);
            return layer;
        }).catch(error=>{
            gvConstellationPromise=null;
            console.error('GV CONSTELLATION OVERLAY INIT FAILED DURING TRAVEL',error);
            throw error;
        });
    }
    gvConstellationPromise.then(layer=>{
        if(!active){layer.clearTravelGlow?.();return;}
        const name=String(constellationName||'').trim();
        let matched=false;
        if(name&&typeof layer.setTravelGlowByName==='function')matched=layer.setTravelGlowByName(name,true)===true;
        if(!matched){
            console.warn('GV CONSTELLATION ARCHIVE NAME DID NOT MATCH; using coordinate fallback',{constellationName,ra,dec});
            matched=layer.setTravelGlowAt?.(ra,dec,true)===true;
        }
        if(!matched)console.error('GV CONSTELLATION TRAVEL BEACON COULD NOT BE ACTIVATED',{constellationName,ra,dec});
    }).catch(error=>console.warn('GV CONSTELLATION TRAVEL GLOW FAILED',error));
}
async function gvFly130H(prepared,{firstHomeTrip=false,onZoomInStart=null,onZoomOutComplete=null,onTMinusEight=null,onArrival=null,registeredPromise=null,switchToSphericalAtApex=false,constellationName=''}={}){
    const initialCenter=prepared?.imageCenter;let ra1=Number(initialCenter?.[0]),dec1=Number(initialCenter?.[1]),finalFov=Number(prepared?.finalFov),targetRotation=Number(prepared?.rotation);
    if(!Number.isFinite(ra1)||!Number.isFinite(dec1)||!Number.isFinite(finalFov)||finalFov<=0||!Number.isFinite(targetRotation))throw new Error('GV 130H DESTINATION STATE INVALID');
    gvNavigationTravelActive=true;
    // Stop new HiPS tile fetches synchronously before any await or animation frame.
    window.GV_NAV_BACKGROUND_SUSPENDED=true;
    window.GV_NAV_HIPS_FETCH_SUSPENDED=true;
    gvSetTravelConstellationGlow(constellationName,ra1,dec1,true);
    gvHideEarthDistance();
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
        const translateStarted=performance.now();let lastSample=-1,tMinusEightStarted=false;
        window.GV_NAV_BACKGROUND_SUSPENDED=true;window.GV_NAV_HIPS_FETCH_SUSPENDED=true;
        await new Promise((resolve,reject)=>{
            const frame=now=>{try{
                const elapsed=Math.min(translateSeconds*1000,now-translateStarted),u=gvFlightNavigationSmootherstep(elapsed/(translateSeconds*1000)),sample=Math.floor(elapsed/10),t=Math.min(1,(now-translateStarted)/(durationSeconds*1000)),tMinusEightThreshold=Math.max(0,1-8/durationSeconds);
                window.GV_NAV_BACKGROUND_SUSPENDED=true;window.GV_NAV_HIPS_FETCH_SUSPENDED=t<(1-9/durationSeconds);
                if(!tMinusEightStarted&&t>=tMinusEightThreshold){tMinusEightStarted=true;try{console.info('GV T-MINUS-EIGHT WORK WINDOW OPEN',{remainingSeconds:8,firstHomeTrip:true});onTMinusEight?.()}catch(error){console.error('GV T-MINUS-EIGHT CALLBACK FAILED',error)}}
                if(sample!==lastSample){
                    const pos=gvFlightGreatCirclePosition(ra0,dec0,ra1,dec1,u),rotation=startRotation+rotationDelta*u;
                    if(elapsed>0)gvSetEarthPointerPosition(pos[0],pos[1],true);
                    aladin.gotoRaDec(pos[0],pos[1]);coordinate?.update(pos[0],pos[1]);
                    aladin.setRotation(rotation);
                    lastSample=sample;
                }
                if(elapsed<translateSeconds*1000){requestAnimationFrame(frame);return}resolve();
            }catch(error){gvNavigationTravelActive=false;gvSetTravelConstellationGlow(constellationName,ra1,dec1,false);window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;reject(error)}};requestAnimationFrame(frame);
        });
        aladin.gotoRaDec(ra1,dec1);coordinate?.update(ra1,dec1);gvSetEarthPointerPosition(ra1,dec1,true);
        aladin.setRotation(targetRotation);
        try{onZoomInStart?.()}catch(error){console.error('GV 130H FIRST-TRIP ZOOM-IN CALLBACK FAILED',error)}
        const zoomStarted=performance.now(),zoomStartRaw=aladin.getFov?.(),zoomStartFov=Number(Array.isArray(zoomStartRaw)?zoomStartRaw[0]:zoomStartRaw);lastSample=-1;
        await new Promise((resolve,reject)=>{
            const frame=now=>{try{
                const elapsed=Math.min(zoomSeconds*1000,now-zoomStarted),p=gvFlightNavigationSmootherstep(elapsed/(zoomSeconds*1000)),sample=Math.floor(elapsed/10);
                if(sample!==lastSample){const fov=gvFlightLogLerp(zoomStartFov,finalFov,p);gvHoldDirectHdDuringTravel(now);aladin.setFov(fov);lastSample=sample}
                if(elapsed<zoomSeconds*1000){requestAnimationFrame(frame);return}window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;gvNavigationTravelActive=false;resolve();
            }catch(error){gvNavigationTravelActive=false;gvSetTravelConstellationGlow(ra1,dec1,false);window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;reject(error)}};requestAnimationFrame(frame);
        });
        aladin.setFov(finalFov);
        gvNavigationTravelActive=false;gvSetTravelConstellationGlow(ra1,dec1,false);
        try{onArrival?.()}catch(error){console.error('GV 130H ARRIVAL CALLBACK FAILED',error)}
        return prepared;
    }
    if(registeredPromise)registeredPromise.then(registered=>{const center=registered?.imageCenter,nra=Number(center?.[0]),ndec=Number(center?.[1]),nfov=Number(registered?.finalFov),nrotation=Number(registered?.rotation);if(Number.isFinite(nra)&&Number.isFinite(ndec)&&Number.isFinite(nfov)&&nfov>0&&Number.isFinite(nrotation)){ra1=nra;dec1=ndec;finalFov=nfov;targetRotation=nrotation}}).catch(error=>console.error('GV 130H REGISTERED DESTINATION PREPARE FAILED',error));
    const durationSeconds=17,duration=durationSeconds*1000,started=performance.now(),zoomInThreshold=.50,zoomOutCompleteThreshold=.30,tMinusEightThreshold=Math.max(0,1-8/durationSeconds);let lastSample=-1,destinationCenterApplied=false,birdseyeSettled=false,zoomInStarted=false,zoomOutCompleted=false,projectionSwitchedAtApex=false,tMinusEightStarted=false;
    await new Promise((resolve,reject)=>{
        const frame=now=>{try{
            const elapsedMs=now-started,t=Math.min(1,elapsedMs/duration),sample=Math.floor(elapsedMs/10);
            // BUILD 0028: only FOV changes during 0–30% and 70–100%.
            // Suspend application polling in both phases; the FOV readout stays live.
            window.GV_NAV_BACKGROUND_SUSPENDED=true; // Preserve the verified zero-stutter rule: app polling stays paused through arrival.
            window.GV_NAV_HIPS_FETCH_SUSPENDED=(t<(1-9/durationSeconds));
            if(!tMinusEightStarted&&t>=tMinusEightThreshold){tMinusEightStarted=true;try{console.info('GV T-MINUS-EIGHT WORK WINDOW OPEN',{remainingSeconds:8,firstHomeTrip:false});onTMinusEight?.()}catch(error){console.error('GV T-MINUS-EIGHT CALLBACK FAILED',error)}}

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
            aladin.setFov(finalFov);if(!birdseyeSettled)aladin.setRotation(targetRotation);gvHdTravelRetired=false;applyDirectHdOpacity();gvNavigationTravelActive=false;try{onArrival?.()}catch(error){console.error('GV 130H ARRIVAL CALLBACK FAILED',error)}console.info('GV HD CROSSFADE RESTORED AT ARRIVAL');window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;resolve(prepared);
        }catch(error){gvNavigationTravelActive=false;gvSetTravelConstellationGlow(ra1,dec1,false);window.GV_NAV_HIPS_FETCH_SUSPENDED=false;window.GV_NAV_BACKGROUND_SUSPENDED=false;reject(error)}};requestAnimationFrame(frame);
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
        const byId=new Map(),byUrl=new Map(),byDesignation=new Map();
        entries.forEach((entry,index)=>{
            const id=String(entry?.archiveId||entry?.id||'').trim().toLowerCase();
            const urls=[entry?.selectedImageUrl,entry?.imageUrl,entry?.hdUrl,entry?.sourceUrl].map(v=>String(v||'').trim().toLowerCase()).filter(Boolean);
            const names=[entry?.designation,entry?.name,entry?.displayName,entry?.title].map(v=>String(v||'').trim().toLowerCase()).filter(Boolean);
            if(id)byId.set(id,{entry,index});
            for(const url of urls)byUrl.set(url,{entry,index});
            for(const name of names){if(!byDesignation.has(name))byDesignation.set(name,{entry,index});else byDesignation.set(name,null)}
        });
        const catalog=Object.freeze({entries,byId,byUrl,byDesignation});
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
    const validNumber=value=>value!==null&&value!==undefined&&value!==''&&Number.isFinite(Number(value));
    const formatDistanceMly=value=>{const v=Number(value);if(!Number.isFinite(v)||v<=0)return '';if(v>=1000)return (v/1000).toFixed(2)+' billion light-years';if(v>=1)return v.toFixed(2)+' million light-years';return (v*1000).toFixed(2)+' thousand light-years'};
    let runtimeDistanceMly=null,runtimeRedshift=null;
    // Provider catalogs may supply descriptive metadata only. Runtime catalog 0004 owns distanceMly and its derived redshift.
    // If runtime identity/distance/redshift is missing, leave those fields blank; never fall back to provider/route values.
    const blankCatalogMetadata=()=>Object.freeze({
        ...enriched,
        designation:String(enriched?.designation||enriched?.name||enriched?.displayName||enriched?.title||'').trim(),
        name:String(enriched?.name||enriched?.commonName||enriched?.pseudonym||enriched?.designation||enriched?.displayName||'').trim(),
        commonName:String(enriched?.commonName||enriched?.pseudonym||enriched?.name||enriched?.designation||'').trim(),
        pseudonym:String(enriched?.pseudonym||enriched?.commonName||enriched?.name||enriched?.designation||'').trim(),
        constellation:String(enriched?.constellation||'').trim(),
        distanceMly:runtimeDistanceMly,
        redshift:runtimeRedshift,
        distance:runtimeDistanceMly===null?'':formatDistanceMly(runtimeDistanceMly),
        sizeKly:Array.isArray(enriched?.sizeKly)?enriched.sizeKly:Object.freeze([]),
        physicalSizeLy:enriched?.physicalSizeLy??null,
        ageYears:enriched?.ageYears??null,
        age:enriched?.age??'',
        imageType:String(enriched?.imageType||'').trim(),
        title:String(enriched?.title||enriched?.designation||enriched?.name||'').trim(),
        description:String(enriched?.description||'').trim()
    });
    try{
        const runtimeDistanceRecord=await gvRuntimeAvmRecord(destination);
        if(!validNumber(runtimeDistanceRecord?.distanceMly)||Number(runtimeDistanceRecord.distanceMly)<=0)throw new Error('GV AVM RUNTIME DISTANCE MISSING: '+String(destination?.archiveId||destination?.id||destination?.name||''));
        if(!validNumber(runtimeDistanceRecord?.redshift))throw new Error('GV AVM RUNTIME REDSHIFT MISSING: '+String(destination?.archiveId||destination?.id||destination?.name||''));
        runtimeDistanceMly=Number(runtimeDistanceRecord.distanceMly);
        runtimeRedshift=Number(runtimeDistanceRecord.redshift);
        if(!key)throw new Error('PROVIDER CATALOG KEY MISSING');
        const catalog=await gvLoadPresentationCatalog(key);
        const id=String(destination?.archiveId||destination?.id||destination?.providerId||'').trim().toLowerCase();
        const url=String(destination?.imageUrl||destination?.selectedImageUrl||destination?.hdUrl||'').trim().toLowerCase();
        const designation=String(destination?.designation||destination?.name||destination?.displayName||destination?.title||'').trim().toLowerCase();
        const match=(id&&catalog?.byId.get(id))||(url&&catalog?.byUrl.get(url))||(designation&&catalog?.byDesignation.get(designation));
        const source=match?.entry;
        if(!source){
            console.warn('GV PRESENTATION CATALOG IDENTITY MATCH MISSING; SCIENCE METADATA CLEARED',{
                catalogKey:key,archiveId:id,imageUrl:url,catalogIndex:destination?.catalogIndex
            });
            return blankCatalogMetadata();
        }
        const science=source?.science||{};
        // Distance always comes from the single top-level distanceMly field in runtime catalog 0004.
        // Canonical emission age for every galaxy: cosmic age of the Universe at the observed redshift.
        // One equation for all records; distance and provider-specific age fields are not inputs.
        // Flat Lambda-CDM parameters: H0=67.6 km/s/Mpc, Omega_m=0.315, Omega_Lambda=0.685.
        // Catalog redshifts may be model-derived from distance; the resulting age is then an estimate.
        const emissionAgeGyrFromRedshift=z=>{
            const redshift=Number(z);
            if(!Number.isFinite(redshift)||redshift<0)return null;
            const H0=67.6;
            const omegaM=0.315;
            const omegaLambda=0.685;
            const mpcKm=3.0856775814913673e19;
            const secondsPerGyr=365.25*24*60*60*1e9;
            const hubblePerSecond=H0/mpcKm;
            const argument=Math.sqrt(omegaLambda/omegaM)/Math.pow(1+redshift,1.5);
            const asinh=Math.log(argument+Math.sqrt(argument*argument+1));
            const ageSeconds=(2/(3*hubblePerSecond*Math.sqrt(omegaLambda)))*asinh;
            const ageGyr=ageSeconds/secondsPerGyr;
            return Number.isFinite(ageGyr)&&ageGyr>0?ageGyr:null;
        };
        const canonicalCosmicAgeGyr=emissionAgeGyrFromRedshift(runtimeRedshift);
        const canonicalCosmicAgeYears=canonicalCosmicAgeGyr===null?null:canonicalCosmicAgeGyr*1e9;
        const formatCosmicAgeGyr=value=>value===null?'UNAVAILABLE':('EST. '+value.toFixed(2)+' GYR');
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
            // A matched provider row can omit constellation metadata even when the selected route record has it.
            // Keep the selected destination's value in that case; all three cards share this hydrated object.
            constellation:String(source?.constellation||enriched?.constellation||'').trim(),
            distanceMly:runtimeDistanceMly,
            redshift:runtimeRedshift,
            distance:formatDistanceMly(runtimeDistanceMly),
            sizeKly:Object.freeze(sizeKly),
            physicalSizeLy,
            ageYears:canonicalCosmicAgeYears,
            age:formatCosmicAgeGyr(canonicalCosmicAgeGyr),
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
const GV_PROVIDER_PORTAL_WINDOW=2;
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
        // RESTORED in Build 0090: preserve the existing APK's provider prewarming.
        // This is essential to fast provider handoff; no native cache-clearing is claimed.
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
let gvNextTripPrewarm=null;
let gvNextTripPrewarmGeneration=0;
/* Memory diagnostics start after resource registries are initialized below. */
function gvDisposeNextTripPrewarm(warm,reason='invalidated'){
    if(!warm)return;
    console.info('GV NEXT DESTINATION PREWARM INVALIDATED',{reason,name:warm.destination?.name||warm.destination?.designation||''});
    const prepared=warm.preparedValue;
    if(prepared?.imageObjectUrl&&prepared.imageObjectUrl!==directHdObjectUrl)gvReleaseHdObjectUrl(prepared.imageObjectUrl);
    if(prepared?.cleanImageObjectUrl&&prepared.cleanImageObjectUrl!==directHdPresentationObjectUrl){gvReleaseCleanImageObjectUrl(prepared.cleanImageObjectUrl)}
}
function gvInvalidateNextTripPrewarm(reason='navigation mode changed'){
    const old=gvNextTripPrewarm;gvNextTripPrewarm=null;gvNextTripPrewarmGeneration++;
    try{old?.controller?.abort()}catch(_){}
    gvDisposeNextTripPrewarm(old,reason);
}
function gvStartNextTripPrewarm(){
    if(gvSurveyMode||navigationInFlight||gvNavigationTravelActive||gvNextTripPrewarm)return;
    const generation=++gvNextTripPrewarmGeneration;
    const controller=new AbortController();
    const warm={destination:null,presentationReady:false,prepared:null,preparedValue:null,generation,controller};gvNextTripPrewarm=warm;
    console.info('GV NEXT DESTINATION PREWARM START');
    warm.prepared=(async()=>{
        try{
            const selected=await navigationRuntime.nextDestination();
            if(generation!==gvNextTripPrewarmGeneration||gvNextTripPrewarm!==warm)throw new Error('PREWARM INVALIDATED AFTER DESTINATION SELECTION');
            warm.destination=selected;
            const presentation=await gvPresentationDestination(selected);
            if(generation!==gvNextTripPrewarmGeneration||gvNextTripPrewarm!==warm)throw new Error('PREWARM INVALIDATED BEFORE METADATA READY');
            warm.destination=presentation;warm.presentationReady=true;
            console.info('GV NEXT DESTINATION METADATA READY',{name:presentation?.name||presentation?.designation||''});
            const record=await gvRuntimeAvmRecord(presentation);
            if(generation!==gvNextTripPrewarmGeneration||gvNextTripPrewarm!==warm)throw new Error('PREWARM INVALIDATED BEFORE IMAGE PREPARATION');
            const prepared=await gvPrepareDirectHd(presentation,Promise.resolve(record),controller.signal);
            if(generation!==gvNextTripPrewarmGeneration||gvNextTripPrewarm!==warm){
                if(prepared.imageObjectUrl)gvReleaseHdObjectUrl(prepared.imageObjectUrl);
                if(prepared.cleanImageObjectUrl)gvReleaseCleanImageObjectUrl(prepared.cleanImageObjectUrl)
                throw new Error('PREWARM INVALIDATED AFTER IMAGE PREPARATION');
            }
            warm.preparedValue=prepared;
            console.info('GV NEXT DESTINATION IMAGE READY',{name:presentation?.name||presentation?.designation||'',resources:gvHdResourceSnapshot()});
            return prepared;
        }catch(error){
            if(gvNextTripPrewarm===warm)console.warn('GV NEXT DESTINATION PREWARM FAILED; SAFE FALLBACK ENABLED',String(error?.message||error));
            throw error;
        }
    })();
    warm.prepared.catch(()=>{});
}
function gvStartFirstDestinationPreload(){
    if(gvFirstDestinationPreload)return gvFirstDestinationPreload;
    const destination=activeRoute[0];
    if(!destination)return Promise.reject(new Error('GV FIRST DESTINATION MISSING'));
    const started=performance.now();
    // BUILD 0030: prepare the first HD image without warming its provider website.
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
// Keep image objects alive while their constellation artwork warms in parallel.
const gvConstellationArtworkPrewarm=new Map();
gvStartMemoryDiagnostics();
const GV_CONSTELLATION_ARTWORK_CACHE_LIMIT=2;
function gvReleaseConstellationArtwork(url){
    const image=gvConstellationArtworkPrewarm.get(url);if(!image)return;
    try{image.onload=null;image.onerror=null;image.removeAttribute?.('src')}catch(_){}
    gvConstellationArtworkPrewarm.delete(url);
}
function gvTrimConstellationArtworkCache(){
    while(gvConstellationArtworkPrewarm.size>GV_CONSTELLATION_ARTWORK_CACHE_LIMIT){
        const stale=gvConstellationArtworkPrewarm.keys().next().value;
        if(stale===undefined)break;
        gvReleaseConstellationArtwork(stale);
    }
}

// ROLL 0025 — release transient renderer resources when Android backgrounds the viewer.
// This does not pretend to clear Android's private HTTP cache. It releases live resources
// owned by this page, including the HD GPU layer, staged/prewarmed blobs and provider prewarm.
let gvBackgroundReleaseInProgress=false;
function gvReleaseTransientResourcesForBackground(reason='page-hidden'){
    if(gvBackgroundReleaseInProgress)return;
    gvBackgroundReleaseInProgress=true;
    const before={hdLayer:!!directHdOverlay,staged:!!directHdStaged,hdObjectUrls:gvHdObjectUrls.length,cleanObjectUrls:gvCleanImageObjectUrls.length,artwork:gvConstellationArtworkPrewarm.size,providerOrigins:gvProviderPortalOrigins.length,prewarm:!!gvNextTripPrewarm};
    try{
        try{gvInvalidateNextTripPrewarm('viewer backgrounded: '+reason)}catch(error){console.warn('GV ROLL 0025 PREWARM RELEASE FAILED',error)}
        if(directHdStaged){
            const staged=directHdStaged;directHdStaged=null;
            try{if(staged.layerName)aladin.removeImageLayer?.(staged.layerName)}catch(_){}
            if(staged.objectUrl&&staged.objectUrl!==directHdObjectUrl)try{gvReleaseHdObjectUrl(staged.objectUrl)}catch(_){}
        }
        // Detach the current HD layer from Aladin's GPU texture pool while preserving its
        // Blob URL/WCS so the existing gvRestoreDirectHd() path can reattach it on return.
        if(directHdOverlay){
            try{aladin.removeImageLayer?.(directHdLayerName)}catch(error){console.warn('GV ROLL 0025 HD GPU LAYER RELEASE FAILED',error)}
            directHdOverlay=null;
        }
        for(const url of [...gvHdObjectUrls])if(url!==directHdObjectUrl)try{gvReleaseHdObjectUrl(url)}catch(_){}
        for(const url of [...gvCleanImageObjectUrls])if(url!==directHdPresentationObjectUrl)try{gvReleaseCleanImageObjectUrl(url)}catch(_){}
        for(const url of [...gvConstellationArtworkPrewarm.keys()])try{gvReleaseConstellationArtwork(url)}catch(_){}
        for(const origin of [...gvProviderPortalOrigins]){
            try{gvReleaseProviderPortalOrigin(origin)}catch(_){}
            try{if(window.GVNative&&typeof window.GVNative.releaseProviderPortal==='function')window.GVNative.releaseProviderPortal(origin)}catch(_){}
        }
        gvProviderPortalOrigins.splice(0,gvProviderPortalOrigins.length);
    }finally{
        const after={hdLayer:!!directHdOverlay,staged:!!directHdStaged,hdObjectUrls:gvHdObjectUrls.length,cleanObjectUrls:gvCleanImageObjectUrls.length,artwork:gvConstellationArtworkPrewarm.size,providerOrigins:gvProviderPortalOrigins.length,prewarm:!!gvNextTripPrewarm};
        console.info('GV ROLL 0025 BACKGROUND RESOURCE RELEASE',{reason,before,after});
        try{gvMemoryDiagnosticSnapshot('roll-0025-'+reason)}catch(_){}
        gvBackgroundReleaseInProgress=false;
    }
}
document.addEventListener('visibilitychange',()=>{
    if(document.visibilityState==='hidden'){
        gvReleaseTransientResourcesForBackground('hidden');
    }else{
        // Existing resume handlers reattach the preserved HD image; capture a post-return snapshot.
        setTimeout(()=>{try{gvMemoryDiagnosticSnapshot('roll-0025-visible-return')}catch(_){}},250);
    }
});

async function showDestination(destination,{firstTrip=false,preloadedPrepared=null,switchToSphericalAtApex=false,prewarmedPresentationDestination=null}={}){
    gvHdTravelRetired=false;
    const v=validateDestination(destination),sourceDestination=activeDestination;
    if(directHdStaged){const stale=directHdStaged;directHdStaged=null;try{aladin.removeImageLayer?.(stale.layerName)}catch(_){}if(stale.objectUrl!==directHdObjectUrl)gvReleaseHdObjectUrl(stale.objectUrl)}
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
        gvStartupMollweideScreen=false;gvHideEarthDistance();gvEarthPointerActive=true;gvUpdateEarthBearingPointer();
        if(firstTrip)destinationPresentation.depart();
        if(directHdPresentationObjectUrl)gvReleaseCleanImageObjectUrl(directHdPresentationObjectUrl)
        destinationPresentation.preview(presentationDestination,{imageUrl:String(directHdUrl(v.destination)).trim()});
        if(firstTrip)startTravelCard();
        // BUILD 0100: catalog-record lookup drives navigation registration; HD preparation stays deferred.
        // Preserve the catalog-record/navigation handshake without preparing HD during translation.
        startRecordLookup();
        // HD image preparation starts at zoom-in, not during the translation phase.
        // Provider prewarming is deferred until after 100% arrival.
    };
    activeDestination=v.destination;
    const presentationBase=prewarmedPresentationDestination||await gvPresentationDestination(v.destination);
    // Warm the selected constellation art while the AVM record and HD image are
    // being prepared, so the travel banner can reveal it from cache at takeoff.
    try{
        const constellationName=String(presentationBase?.constellation||'').trim();
        const constellationUrls=window.GVProviderArtwork?.constellationSources?.(constellationName)||[];
        for(const url of constellationUrls){
            if(!url||gvConstellationArtworkPrewarm.has(url))continue;
            const image=new Image();
            image.decoding='async';
            image.onload=()=>{if(gvConstellationArtworkPrewarm.get(url)!==image)return;console.info('GV CONSTELLATION ART PREWARMED',{name:constellationName,url});};
            image.onerror=()=>{if(gvConstellationArtworkPrewarm.get(url)!==image)return;console.warn('GV CONSTELLATION ART PREWARM MISSED',{name:constellationName,url});gvReleaseConstellationArtwork(url);};
            gvConstellationArtworkPrewarm.set(url,image);
            gvTrimConstellationArtworkCache();
            image.src=url;
        }
    }catch(error){console.warn('GV CONSTELLATION ART PREWARM SKIPPED',error)}
    // ROLL 0021: propagate the image-matched AVM FOV axes to every presentation surface.
    // The exact same AVM runtime record drives HD WCS construction; never collapse Y to X when Y exists.
    const presentationAvmRecord=await gvRuntimeAvmRecord(v.destination);
    const presentationFovX=Number(presentationAvmRecord?.fovXDegrees??presentationAvmRecord?.fovDegrees);
    const presentationFovY=Number(presentationAvmRecord?.fovYDegrees??presentationAvmRecord?.fovDegrees);
    if(!(presentationFovX>0&&presentationFovX<360&&presentationFovY>0&&presentationFovY<360))throw new Error('GV ROLL 0021 AVM FOVX/FOVY INVALID');
    const presentationDistanceMly=Number(presentationAvmRecord?.distanceMly),presentationRedshift=Number(presentationAvmRecord?.redshift);
    if(!(presentationDistanceMly>0)||!Number.isFinite(presentationDistanceMly)||!Number.isFinite(presentationRedshift)||presentationRedshift<0)throw new Error('GV ARRIVAL DISTANCE/REDSHIFT INVALID');
    const presentationDestination=Object.freeze({...presentationBase,distanceMly:presentationDistanceMly,redshift:presentationRedshift,distance:presentationAvmRecord.distance,fovXDegrees:presentationFovX,fovYDegrees:presentationFovY,avmHorizontalFovDegrees:presentationFovX,avmVerticalFovDegrees:presentationFovY});
    // The destination card, HD banner, HD viewport and live distance display share the AVM-authoritative FOV record.
    activeDestination=presentationDestination;
    headsUpDisplay.render();
    // BUILD 0130: preserve BUILD 0129 travel behavior; make Earth distance coordinate-aware and ruler FOV-live.
    // This keeps image preparation out of the 17-second flight, eliminating late arrival
    // handoff and avoiding CPU/network decode work during the smooth FOV choreography.
    // If preflight fails, retry at T-minus-eight rather than aborting navigation.
    let preflightPrepared=null,installed=false,stagedInstallPromise=null;
    const installWhenReady=(prepared,{stage=true}={})=>{
        if(!prepared?.imageObjectUrl)return Promise.reject(new Error('GV PREPARED HD OBJECT URL MISSING'));
        if(activeDestination!==presentationDestination||installed)return Promise.resolve(false);
        try{
            stagedInstallPromise=gvInstallPreparedHd({...prepared,destination:presentationDestination},{stage});
            installed=true;
            return stagedInstallPromise;
        }catch(error){
            gvReleaseHdObjectUrl(prepared.imageObjectUrl);
            console.error('GV DIRECT HD STAGE START FAILED',error);
            return Promise.reject(error);
        }
    };
    try{
        const preflightStarted=performance.now();
        preflightPrepared=await ensurePrepared();
        console.info('GV TRAVEL PREFLIGHT HD READY',{ms:Math.round(performance.now()-preflightStarted),name:presentationDestination?.name||presentationDestination?.objectName||''});
        await installWhenReady(preflightPrepared,{stage:true});
        console.info('GV TRAVEL AVM LAYER REGISTERED BEFORE MOTION',{name:presentationDestination?.name||presentationDestination?.objectName||''});
    }catch(error){
        installed=false;stagedInstallPromise=null;
        preparedPromise=null;
        recordPromise=null;
        if(firstTrip)gvFirstDestinationPreload=null;
        console.warn('GV TRAVEL PREFLIGHT/STAGING FAILED; RETRYING AT T-MINUS-EIGHT',error);
    }
    // Register the image and prepare presentation artwork before camera motion.
    // This keeps image decode, Aladin layer registration, provider icons, and constellation work out of the flight.
    startTravelCard();
    startTravelWork();
    // BUILD 0011: the current galaxy HD remains visible through zoom-out,
    // translation and rotation. At zoom-in start the current HD is retired,
    // then the next galaxy HD is installed and activated.
    if(firstTrip){
        const provisional={imageCenter:[v.ra,v.dec],finalFov:v.fov,rotation:v.rotation};
        const travelPromise=gvFly130H(provisional,{firstHomeTrip:true,constellationName:presentationDestination?.constellation||presentationBase?.constellation||'',registeredPromise:registeredTravelPromise,onTMinusEight:()=>{if(!installed)ensurePrepared().then(prepared=>installWhenReady(prepared,{stage:true})).catch(error=>console.error('GV FIRST-TRIP T-MINUS-EIGHT STAGE FAILED',error))},onArrival:()=>gvActivateStagedHd(presentationDestination)});
        await travelPromise;
        if(activeDestination!==presentationDestination)return v.destination;
        if(stagedInstallPromise)await stagedInstallPromise.catch(error=>console.error('GV FIRST-TRIP STAGED LAYER SETTLE FAILED',error));
        gvActivateStagedHd(presentationDestination);
        travelPresentation.end();
        const arrivedPrepared=await ensurePrepared();
        directHdPresentationObjectUrl=arrivedPrepared.cleanImageObjectUrl;
        destinationPresentation.arrive(presentationDestination,{imageUrl:String(directHdUrl(v.destination)).trim(),preparedImageUrl:arrivedPrepared.cleanImageObjectUrl});
        // BUILD 0030: let the arrival presentation paint before noncritical work.
        // The identity guard prevents stale post-arrival work if another trip starts.
        requestAnimationFrame(()=>requestAnimationFrame(()=>{
            if(activeDestination!==presentationDestination)return;
            gvEarthDistanceArrivalDestination=presentationDestination;
            gvEarthDistanceUserAdjustedView=false;
            gvEarthDistanceLastObservedCenter=null;
            gvEarthDistanceSyncGeneration++;
            gvEarthDistanceSyncPending=false;
            headsUpDisplay.render();
            gvShowEarthDistance(presentationDestination,true);
            gvPrewarmProviderWebsite(v.destination);
            gvStartNextTripPrewarm();
        }));
        return v.destination;
    }
    const provisional={imageCenter:[v.ra,v.dec],finalFov:v.fov,rotation:v.rotation};
    const travelPromise=gvFly130H(provisional,{firstHomeTrip:false,constellationName:presentationDestination?.constellation||presentationBase?.constellation||'',registeredPromise:registeredTravelPromise,switchToSphericalAtApex,onTMinusEight:()=>{if(!installed)ensurePrepared().then(prepared=>installWhenReady(prepared,{stage:true})).catch(error=>console.error('GV DIRECT HD T-MINUS-EIGHT STAGE FAILED',error))},onArrival:()=>gvActivateStagedHd(presentationDestination)});
    await travelPromise;
    if(activeDestination!==presentationDestination)return v.destination;
    if(stagedInstallPromise)await stagedInstallPromise.catch(error=>console.error('GV STAGED LAYER SETTLE FAILED',error));
    gvActivateStagedHd(presentationDestination);
    travelPresentation.end();
    const arrivedPrepared=await ensurePrepared();
        directHdPresentationObjectUrl=arrivedPrepared.cleanImageObjectUrl;
        destinationPresentation.arrive(presentationDestination,{imageUrl:String(directHdUrl(v.destination)).trim(),preparedImageUrl:arrivedPrepared.cleanImageObjectUrl});
    // BUILD 0030: let the arrival presentation paint before noncritical work.
    // The identity guard prevents stale post-arrival work if another trip starts.
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
        if(activeDestination!==presentationDestination)return;
        gvEarthDistanceArrivalDestination=presentationDestination;
        gvEarthDistanceUserAdjustedView=false;
        gvEarthDistanceLastObservedCenter=null;
        gvEarthDistanceSyncGeneration++;
        gvEarthDistanceSyncPending=false;
        headsUpDisplay.render();
        gvShowEarthDistance(presentationDestination,true);
        gvPrewarmProviderWebsite(v.destination);
        gvStartNextTripPrewarm();
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
    const providerKey=String(provider||record?.provider||'').toUpperCase();
    const rawCatalogKey=String(record?.catalogKey||'').trim();
    // The thumbnail index uses canonical short catalog names (for example ESO|eso|0),
    // while runtime sourceCatalog may contain the full JSON path. Normalize only the
    // lookup key; preserve the original catalogKey on the destination record.
    const catalogKey=rawCatalogKey.includes('/')?({
        HUBBLE:'hubble',JWST:'jwst',CHANDRA:'chandra',ESO:'eso',NOIRLAB:'noirlab',SPITZER:'spitzer'
    }[providerKey]||rawCatalogKey):rawCatalogKey;
    const catalogIndex=Number.isFinite(Number(record?.catalogIndex))?Number(record.catalogIndex):0;
    const packKey=providerKey+'|'+catalogKey+'|'+catalogIndex;
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
    gvInvalidateNextTripPrewarm('survey provider selected');
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
    gvInvalidateNextTripPrewarm('survey mode exited');
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
    gvInvalidateNextTripPrewarm('search result selected');
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
        history.push(prepared);if(history.length>130)history.shift();historyIndex=history.length-1;
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
        let nextWarm=gvNextTripPrewarm;gvNextTripPrewarm=null;
        let destination,preloadedPrepared=null,prewarmedPresentationDestination=null;
        if(nextWarm){
            try{preloadedPrepared=nextWarm.prepared?await nextWarm.prepared:null}catch(error){console.warn('GV NEXT DESTINATION PREWARM FALLBACK',String(error?.message||error));preloadedPrepared=null}
            destination=nextWarm.destination;
            if(!destination){console.warn('GV NEXT DESTINATION PREWARM DESTINATION MISSING; SELECTING FRESH');destination=await navigationRuntime.nextDestination()}
            else {prewarmedPresentationDestination=nextWarm.presentationReady?destination:null;console.info(preloadedPrepared?'GV NEXT DESTINATION PREWARM CACHE HIT':'GV NEXT DESTINATION PREWARM CACHE MISS',{name:destination?.name||destination?.designation||''})}
        }else destination=await navigationRuntime.nextDestination();
        if(routeIndex===0&&gvFirstDestinationPreload){
            gvFirstDestinationPreload.then(warm=>{if(warm?.destination===destination)console.info('GV FIRST DESTINATION PRELOAD READY FOR ACTIVE TRIP')}).catch(error=>console.error('GV FIRST DESTINATION PRELOAD UNAVAILABLE',error));
        }
        if(historyIndex<history.length-1)history.splice(historyIndex+1);
        history.push(destination);if(history.length>130)history.shift();
        historyIndex=history.length-1;
        const firstTrip=routeIndex===0;
        const switchToSphericalAtApex=routeIndex===1;
        routeIndex++;
        await showDestination(destination,{firstTrip,preloadedPrepared,switchToSphericalAtApex,prewarmedPresentationDestination});
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
    gvInvalidateNextTripPrewarm('back navigation');
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
    gvInvalidateNextTripPrewarm('forward navigation');
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