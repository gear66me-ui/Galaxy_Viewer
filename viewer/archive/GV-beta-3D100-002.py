from IPython.display import HTML, Javascript, display

# Galaxy Viewer AVM3D Series 100 — minimal AVM-first viewer
display(HTML(r"""
<link rel="stylesheet" href="https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css">
<style>
@font-face{font-family:"Space Age";src:url("https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf") format("opentype")}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#gv-avm3d{position:relative;width:100vw;height:100dvh;background:#000;overflow:hidden}
#gv-hamburger-host{position:absolute;inset:0;z-index:7200;pointer-events:none}
#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;pointer-events:auto}
#gv-target-host{position:absolute;left:342px;top:12px;z-index:7210;width:36px;height:36px;pointer-events:auto}
#gv-random-galaxy-host{position:absolute;inset:0;z-index:7300;pointer-events:none}
#gv-galaxy-nav{position:absolute;left:50%;bottom:12px;z-index:7100;display:flex;gap:5px;transform:translateX(-50%);pointer-events:auto}
#gv-galaxy-nav button{font-family:"Space Age",sans-serif}
#gv-version-label{position:absolute;left:50%;bottom:52px;z-index:7100;transform:translateX(-50%);color:#58bfff;font:8px "Space Age",sans-serif}
#gv-avm-slider-wrap{display:none;position:absolute;left:50%;bottom:92px;z-index:7600;width:min(72vw,520px);transform:translateX(-50%);pointer-events:auto}
#gv-avm-slider{width:100%}
</style>
<div id="gv-avm3d"></div>
"""))

display(Javascript(r"""
(async()=>{
'use strict';
const VERSION='AVM3D-100-001';
const ROOT='https://gear66me-ui.github.io/Galaxy_Viewer/';
const RAW='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
const ALADIN='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
const MASTER=RAW+'viewer/image-databases/master-database/gv-master-catalog.json';
const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
const scripts=[
 ALADIN,
 ROOT+'viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js',
 ROOT+'viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js',
 ROOT+'viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js',
 ROOT+'viewer/modules/target-simbad/gv-target-simbad-0004.js',
 ROOT+'viewer/modules/navigation/gv-navigation-0018.js',
 ROOT+'viewer/modules/random-galaxy/gv-random-galaxy-0131.js'
];
function loadScript(src){return new Promise((ok,fail)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=()=>fail(new Error('LOAD FAILED '+src));document.head.appendChild(s)})}
for(const src of scripts)await loadScript(src);
await A.init;
const root=document.getElementById('gv-avm3d');
const aladin=A.aladin('#gv-avm3d',{target:`${HOME.ra} ${HOME.dec}`,survey:'P/DSS2/color',fov:180,projection:'AIT',cooFrame:'ICRSd',showReticle:false,showZoomControl:false,showFullscreenControl:false,showLayersControl:false,showGotoControl:false,showCooGridControl:false,showSettingsControl:false,showSelectionModeControl:false,showColorPickerControl:false,showShareControl:false,showSimbadPointerControl:true,showProjectionControl:false,showStatusBar:false,showFrame:false,showFov:false,showCooLocation:false,showContextMenu:false});
window.aladin_cosmic_command_test=aladin;
function host(id){const e=document.createElement('div');e.id=id;root.appendChild(e);return e}
const hamburgerHost=host('gv-hamburger-host'),coordinateHost=host('gv-coordinate-host'),targetHost=host('gv-target-host'),randomHost=host('gv-random-galaxy-host');
const nav=document.createElement('div');nav.id='gv-galaxy-nav';
const back=document.createElement('button');back.type='button';back.textContent='‹';back.disabled=true;
const random=document.createElement('button');random.type='button';random.textContent='✨ RANDOM GALAXY ✨';
const forward=document.createElement('button');forward.type='button';forward.textContent='›';forward.disabled=true;
nav.append(back,random,forward);root.appendChild(nav);
const version=document.createElement('div');version.id='gv-version-label';version.textContent='GV '+VERSION;root.appendChild(version);
const sliderWrap=document.createElement('div');sliderWrap.id='gv-avm-slider-wrap';sliderWrap.innerHTML='<input id="gv-avm-slider" aria-label="AVM IMAGE TRANSPARENCY" type="range" min="0" max="1" step="0.01" value="1">';root.appendChild(sliderWrap);
const slider=sliderWrap.querySelector('#gv-avm-slider');
slider.addEventListener('input',()=>{try{aladin.getOverlayImageLayer()?.setOpacity(Number(slider.value))}catch(e){console.warn('AVM OPACITY',e)}});
function screenUrl(c){const a=[...(Array.isArray(c?.jpegCandidates)?c.jpegCandidates:[]),c?.selectedImageUrl,c?.hdUrl].map(x=>String(x||'').trim()).filter(Boolean);return a.find(x=>/\/screen\//i.test(x))||a[0]||''}
function distance(c){const n=Number(c?.science?.distanceMly??c?.distanceMly);if(Number.isFinite(n)&&n>0)return n;const m=String(c?.distance||'').match(/[\d.]+/);return m?Number(m[0]):null}
function normalize(c,i,key){
 const ra=Number(c?.ra),dec=Number(c?.dec),fov=Number(c?.fovDegrees),rot=Number(c?.aladinRotation),d=distance(c),hd=screenUrl(c);
 if(!String(c?.name||'').trim()||![ra,dec,fov,rot,d].every(Number.isFinite)||!hd||!c?.sourceUrl)return null;
 return Object.freeze({source:key,provider:String(c.provider||key).toUpperCase(),archiveId:String(c.archiveId||c.id||''),name:String(c.name),ra,dec,distance:d,constellation:String(c.constellation||''),designation:String(c.designation||c.name||''),commonName:String(c.displayName||c.title||c.name||''),age:String(c.science?.ageDisplay||''),ageYears:null,physicalSizeLy:null,fovDegrees:fov,hdUrl:hd,sourceUrl:String(c.sourceUrl),aladinRotation:rot,credit:String(c.credit||''),imageType:String(c.imageType||'Observation'),category:String(c.category||'Galaxies'),telescope:String(c.telescope||c.provider||key),githubImageUrl:String(c.githubImageUrl||''),sha256:String(c.sha256||''),catalogIndex:i});
}
async function fetchJson(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status+' '+url);return r.json()}
async function loadCatalog(){
 const master=await fetchJson(MASTER),out=[];
 await Promise.all(Object.entries(master.catalogs||{}).map(async([key,path])=>{try{const p=await fetchJson(new URL(path,RAW).href);(p.entries||[]).forEach((c,i)=>{const g=normalize(c,i,key);if(g)out.push(g)})}catch(e){console.warn('CATALOG '+key,e)}}));
 if(!out.length)throw new Error('NO TARGETABLE GALAXIES');return out;
}
const catalog=await loadCatalog();
function currentRaDec(){try{return aladin.getRaDec()}catch(_){return [HOME.ra,HOME.dec]}}
const hamburger=window.GalaxyViewerHamburgerMenu.init({host:hamburgerHost,onMenuAction(action){if(action==='SURVEY')aladin.setBaseImageLayer('P/DSS2/color')},onProjectionSelected(_name,detail){if(detail?.code)aladin.setProjection(detail.code)}});
hamburger.root.style.position='absolute';hamburger.root.style.inset='0';hamburger.root.style.pointerEvents='none';hamburger.menuButton.style.pointerEvents='auto';
let coordinate=null,last=[HOME.ra,HOME.dec];
coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(){aladin.setFrame('ICRSd');coordinate?.setFrame('ICRSd')}});await coordinate.ready;coordinate.setFrame('ICRSd');
setInterval(()=>{const p=currentRaDec();if(p&&Number.isFinite(+p[0])&&Number.isFinite(+p[1])&&(p[0]!==last[0]||p[1]!==last[1])){last=[+p[0],+p[1]];coordinate.update(last[0],last[1])}},120);
const target=await window.GalaxyViewerTargetSimbad.init({host:targetHost,aladin});
if(window.GalaxyViewerNavigation?.VERSION!=='0018')throw new Error('NAVIGATION 0018 MISSING');
if(window.GalaxyRandomGalaxy?.VERSION!=='0131')throw new Error('RANDOM GALAXY 0131 MISSING');
let avmToken=0;
function showAvm(destination){
 const token=++avmToken;sliderWrap.style.display='none';slider.value='1';
 if(!destination?.hdUrl)return;
 try{
  aladin.setOverlayImageLayer(A.image(destination.hdUrl,{name:'GV AVM '+destination.name,successCallback:(ra,dec,fov)=>{if(token!==avmToken)return false;sliderWrap.style.display='block';requestAnimationFrame(()=>{try{aladin.getOverlayImageLayer()?.setOpacity(1)}catch(_){}});return true}}));
 }catch(e){console.warn('AVM LOAD FAILED',destination?.name,e)}
}
const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomHost,{aladin,viewerRoot:root,randomButton:random,bindClick:true,prefetch:false,provider:null,currentGalaxy:HOME,catalogCount:catalog.length,getCatalogCount:()=>catalog.length,onArrival(destination){showAvm(destination)},onError(error){console.error('RANDOM GALAXY FAILURE',error)}});
window.GalaxyViewerRandomGalaxy=randomGalaxy;
const windowNav=randomGalaxy.installNavigationWindow({futureTarget:10,historyTarget:10,hotTarget:5,keyOf:d=>String(d?.archiveId||d?.name||'').toLowerCase(),current:HOME});
const engine=randomGalaxy.installPreparationEngine({aladinUrl:ALADIN,home:HOME,galaxyCatalog:catalog,aladin,A});
randomGalaxy.provider=engine.randomGalaxyProvider;
engine.fillPrefetchQueue();
await randomGalaxy.ready;
try{
 const hd=randomGalaxy.installHdArchiveIntegration({bottom:{version,nav,random,back,forward},targetIconUrl:ROOT+'viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg',getPrefetchReady:()=>engine.getPrefetchReady(),isBackgroundWorkSuspended:()=>engine.getBackgroundWorkSuspended(),isNavigationPending:()=>Boolean(window.GalaxyRandomGalaxy?.isNavigationPending?.()),getActiveTargetKey:()=>engine.getActiveTargetKey()});
 const originalSync=hd.syncHdProviderPresentation?.bind(hd);if(originalSync)window.__gvAvmHdSync=originalSync;
}catch(e){console.warn('HD INTEGRATION WARNING',e)}
window.GalaxyViewerCore=Object.freeze({version:VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomNavigationWindow:windowNav,getGalaxyCatalog:()=>Object.freeze([...catalog])});
document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,catalogCount:catalog.length}}));
})().catch(error=>{console.error('GALAXY VIEWER AVM3D STARTUP FAILURE',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}))});
"""))

# HTML tail
display(HTML("""
"""))
