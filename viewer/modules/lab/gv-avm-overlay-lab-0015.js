(()=>{
'use strict';
const global=window;
const VERSION="0015";
const WATCH_MS=220;
const PRELOAD_LIMIT=4;
const LAYER_NAME="Galaxy Viewer AVM Overlay";
const FOV_PAD=1.0;
let ARef=null;
let aladinRef=null;
let randomRef=null;
let watchTimer=null;
let preloadTimer=null;
let overlay=null;
let lastKey="";
let loadingKey="";
let lastContext=null;
let panelEverEnabled=false;
let travelOldKey="";
let travelMinUntil=0;
let suppressUntil=0;
const processedReady=new Map();
const processedLoading=new Set();
const keepAlive=[];

function finite(v){v=Number(v);return Number.isFinite(v)?v:null}
function stateOf(r){try{return r?.getState?.()||{}}catch(_){return {}}}
function clean(v){return String(v??"").trim()}
function avmUrlFor(d){return clean(d?.selectedImageUrl||d?.screenUrl||d?.imageUrl||d?.hdUrl||d?.largeUrl||d?.url)}
function destinationKey(d,url){return clean(d?.archiveId||d?.id||d?.name||d?.title||url)}
function isUsableAvmDestination(d,url){return !!(d&&url&&/^https?:\/\//i.test(url)&&!String(url).includes('placeholder'))}
function opacityNow(){const sl=document.getElementById('gv-avm-overlay-opacity');return Math.max(0,Math.min(1,(Number(sl?.value)||100)/100))}
function applyOpacity(){
  const op=opacityNow();
  try{overlay?.setOpacity?.(op)}catch(_){}
  try{overlay?.setAlpha?.(op)}catch(_){}
  try{overlay?.setOptions?.({opacity:op})}catch(_){}
  paintSlider();
}
function injectStyle(){
  if(document.getElementById('gv-avm-overlay-lab-style-0015'))return;
  const style=document.createElement('style');
  style.id='gv-avm-overlay-lab-style-0015';
  style.textContent=`
#gv-avm-overlay-lab{position:fixed;left:0;top:172px;z-index:2147482000;width:92px;height:164px;transform:none;background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;pointer-events:none;display:none}
#gv-avm-overlay-lab[data-on="1"]{display:block}
#gv-avm-touch-shield{position:absolute;left:0;top:0;width:92px;height:164px;border-radius:19px;background:rgba(0,18,60,.10);pointer-events:auto;touch-action:none;user-select:none;-webkit-user-select:none;overscroll-behavior:contain}
#gv-avm-fader-label{position:absolute;left:4px;top:50%;height:116px;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;text-orientation:mixed;font:400 7px/1 "Space Age",sans-serif;letter-spacing:.85px;color:#68E0FF;text-shadow:0 0 7px rgba(104,224,255,.92),0 0 13px rgba(0,140,255,.58);pointer-events:none}
#gv-avm-overlay-opacity{--gv-avm-pct:100%;-webkit-appearance:none;appearance:none;position:absolute;left:-30px;top:68px;width:126px;height:24px;margin:0;background:transparent!important;outline:none;display:block;transform:rotate(-90deg);transform-origin:center;direction:rtl;touch-action:none;pointer-events:auto}
#gv-avm-overlay-opacity::-webkit-slider-runnable-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#0050B8 0%,#007BE8 50%,#32C7FF 80%,#9AF0FF 100%);box-shadow:0 0 8px rgba(104,224,255,.78),0 0 15px rgba(0,140,255,.52),inset 0 0 5px rgba(221,248,255,.34)}
#gv-avm-overlay-opacity::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:19px;height:19px;border-radius:50%;background:#68E0FF;border:1px solid rgba(221,248,255,.98);margin-top:-5.5px;box-shadow:0 0 11px rgba(104,224,255,.96),0 0 21px rgba(0,140,255,.68)}
#gv-avm-overlay-opacity::-moz-range-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#0050B8 0%,#007BE8 50%,#32C7FF 80%,#9AF0FF 100%);box-shadow:0 0 8px rgba(104,224,255,.78),0 0 15px rgba(0,140,255,.52),inset 0 0 5px rgba(221,248,255,.34)}
#gv-avm-overlay-opacity::-moz-range-thumb{width:19px;height:19px;border-radius:50%;background:#68E0FF;border:1px solid rgba(221,248,255,.98);box-shadow:0 0 11px rgba(104,224,255,.96),0 0 21px rgba(0,140,255,.68)}
@media(max-height:720px){#gv-avm-overlay-lab{top:158px;width:88px;height:152px}#gv-avm-touch-shield{width:88px;height:152px}#gv-avm-fader-label{height:108px}#gv-avm-overlay-opacity{left:-27px;top:62px;width:116px}}
@media(max-width:430px){#gv-avm-overlay-lab{left:0;top:166px;width:90px;height:158px}#gv-avm-touch-shield{width:90px;height:158px}#gv-avm-overlay-opacity{left:-28px;top:65px;width:120px}}
`;
  document.head.appendChild(style);
}
function panel(){
  injectStyle();
  let p=document.getElementById('gv-avm-overlay-lab');
  if(p)return p;
  p=document.createElement('div');
  p.id='gv-avm-overlay-lab';
  p.innerHTML='<div id="gv-avm-touch-shield"><div id="gv-avm-fader-label">CROSS FADE</div><input id="gv-avm-overlay-opacity" aria-label="AVM cross fade" type="range" min="0" max="100" value="100" dir="rtl"></div>';
  document.body.appendChild(p);
  return p;
}
function slider(){return panel().querySelector('#gv-avm-overlay-opacity')}
function paintSlider(){const sl=slider();const val=Math.max(0,Math.min(100,Number(sl.value)||0));sl.style.setProperty('--gv-avm-pct',val+'%')}
function setPanelVisible(on){try{const p=panel();if(on)panelEverEnabled=true;p.dataset.on=panelEverEnabled?'1':'0'}catch(_){}}
function swallowPanelTouches(){
  const p=panel();
  if(p.dataset.gvTouchShield0015)return;
  p.dataset.gvTouchShield0015='1';
  const stop=e=>{try{e.stopPropagation()}catch(_){}try{if(e.target?.id!=='gv-avm-overlay-opacity')e.preventDefault()}catch(_){}};
  for(const ev of ['pointerdown','pointermove','pointerup','pointercancel','touchstart','touchmove','touchend','touchcancel','mousedown','mousemove','mouseup','wheel','click'])p.addEventListener(ev,stop,{capture:true,passive:false});
}
function addCandidate(out,item){if(!item)return;const d=item.destination||item.record||item;const url=avmUrlFor(d);if(isUsableAvmDestination(d,url))out.push(d)}
function liveCandidates(randomGalaxy){
  const s=stateOf(randomGalaxy), g=global.GalaxyRandomGalaxy||{}, out=[];
  for(const d of [s.activeDestination,s.currentDestination,randomGalaxy?.activeDestination,randomGalaxy?.currentDestination,g.activeDestination,g.currentDestination])addCandidate(out,d);
  return out;
}
function collectCandidates(root,out,seen,depth){
  if(!root||typeof root!=='object'||depth>4||seen.has(root))return;
  seen.add(root);
  addCandidate(out,root);
  if(Array.isArray(root)){for(const x of root)collectCandidates(x,out,seen,depth+1);return}
  for(const key of ['future','route','navigationQueue','preparedQueue','prefetchReady','prefetchQueued','activePreparedItem'])collectCandidates(root[key],out,seen,depth+1);
}
function upcomingCandidates(randomGalaxy){
  const s=stateOf(randomGalaxy), g=global.GalaxyRandomGalaxy||{}, out=[], seen=new WeakSet();
  collectCandidates(s,out,seen,0); collectCandidates(g,out,seen,0);
  for(const key of ['future','route','navigationQueue','preparedQueue','prefetchReady','prefetchQueued','activePreparedItem'])collectCandidates(randomGalaxy?.[key],out,seen,0);
  const unique=[], keys=new Set();
  for(const d of out){const url=avmUrlFor(d), key=destinationKey(d,url); if(!key||keys.has(key))continue; keys.add(key); unique.push(d)}
  return unique;
}
function bestDestination(randomGalaxy){for(const d of liveCandidates(randomGalaxy)){const url=avmUrlFor(d), key=destinationKey(d,url); if(key&&isUsableAvmDestination(d,url))return {d,url,key}} return null}
function currentKey(){const c=bestDestination(randomRef);return c?.key||''}
function suppressed(){return Date.now()<suppressUntil}
function hideOverlayForTravel(){
  travelOldKey=lastKey||loadingKey||currentKey()||'';
  travelMinUntil=Date.now()+350;
  suppressUntil=Date.now()+26000;
  loadingKey='';
  lastKey='';
  try{overlay?.setOpacity?.(0)}catch(_){}
  try{overlay?.setAlpha?.(0)}catch(_){}
  try{overlay?.setOptions?.({opacity:0})}catch(_){}
  for(const ms of [250,500,850,1200,1700,2400,3400,4800,6600,8800,11200,14000,17200,20800,24400])setTimeout(()=>loadForBestDestination('travel-poll-'+ms),ms);
}
function installTravelButtonGuard(){
  const buttons=document.querySelectorAll('#gv-random-galaxy,.gv-galaxy-history');
  for(const b of buttons){
    if(!b||b.dataset.gvAvmGuard0015)continue;
    b.dataset.gvAvmGuard0015='1';
    for(const ev of ['pointerdown','touchstart','click'])b.addEventListener(ev,hideOverlayForTravel,{capture:true,passive:true});
  }
}
async function fetchBlob(url){const res=await fetch(url,{mode:'cors',cache:'force-cache',credentials:'omit'}); if(!res.ok)throw new Error('fetch image failed '+res.status); return await res.blob()}
function loadImageFromBlob(blob){return new Promise((resolve,reject)=>{const u=URL.createObjectURL(blob); const img=new Image(); img.onload=()=>{URL.revokeObjectURL(u);resolve(img)}; img.onerror=e=>{URL.revokeObjectURL(u);reject(e)}; img.src=u})}
async function createVignettedUrl(url,key,reason){
  const blob=await fetchBlob(url);
  const img=await loadImageFromBlob(blob);
  const w=img.naturalWidth||img.width, h=img.naturalHeight||img.height;
  if(!(w>0&&h>0))throw new Error('invalid image size');
  const canvas=document.createElement('canvas'); canvas.width=w; canvas.height=h;
  const ctx=canvas.getContext('2d'); ctx.drawImage(img,0,0,w,h);
  const rx=w*0.50, ry=h*0.50;
  const g=ctx.createRadialGradient(w/2,h/2,Math.min(w,h)*0.18,w/2,h/2,Math.max(w,h)*0.72);
  g.addColorStop(0,'rgba(0,0,0,0)'); g.addColorStop(0.56,'rgba(0,0,0,0)'); g.addColorStop(0.82,'rgba(3,14,36,.16)'); g.addColorStop(1,'rgba(0,3,14,.55)');
  ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
  const outBlob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',0.92));
  if(!outBlob)throw new Error('canvas toBlob failed');
  return {displayUrl:URL.createObjectURL(outBlob),key,originalUrl:url,reason,w,h,readyAt:Date.now()};
}
function preloadProcessed(d,reason){
  const url=avmUrlFor(d), key=destinationKey(d,url);
  if(!isUsableAvmDestination(d,url)||!key||processedReady.has(key)||processedLoading.has(key))return false;
  processedLoading.add(key);
  createVignettedUrl(url,key,reason).then(item=>{processedLoading.delete(key);processedReady.set(key,item);keepAlive.push(item.displayUrl);if(keepAlive.length>40){const old=keepAlive.shift();try{URL.revokeObjectURL(old)}catch(_){}};console.info('GV AVM LAB 0015 IMAGE VIGNETTE PRELOAD READY',{reason,key,url})}).catch(error=>{processedLoading.delete(key);console.warn('GV AVM LAB 0015 IMAGE VIGNETTE PRELOAD FAILED',{reason,key,url,error})});
  return true;
}
function preloadUpcoming(reason){let count=0;for(const d of upcomingCandidates(randomRef)){if(preloadProcessed(d,reason))count++; if(count>=PRELOAD_LIMIT)break} if(count)console.info('GV AVM LAB 0015 PRELOAD STARTED',{reason,count})}
function fitFovFor(d,fallback){
  const scalar=finite(d?.imageFovDeg)||finite(d?.imageFovDegrees)||finite(d?.fovDegrees)||finite(fallback);
  const x=finite(d?.imageFovXDeg)||((finite(d?.imageFovXArcmin)||0)/60)||null;
  const y=finite(d?.imageFovYDeg)||((finite(d?.imageFovYArcmin)||0)/60)||null;
  let f=scalar;
  const va=(window.innerWidth>0&&window.innerHeight>0)?window.innerWidth/window.innerHeight:1;
  if(x&&y&&va>0)f=Math.max(x,y*va,f||0);
  return finite(f);
}
function destinationStillCurrent(d){const c=bestDestination(randomRef);const url=avmUrlFor(d);return !!(c&&c.key===destinationKey(d,url))}
function applyExactImageFov(ra,dec,fov,destination,tag){
  const r=finite(ra), decv=finite(dec); if(r!==null&&decv!==null){try{aladinRef.gotoRaDec?.(r,decv)}catch(_){}}
  const fit=fitFovFor(destination,fov); if(fit&&fit>0){try{if(typeof aladinRef.setFoV==='function')aladinRef.setFoV(fit*FOV_PAD);else aladinRef.setFov?.(fit*FOV_PAD)}catch(_){} }
}
function setExactImageFov(ra,dec,fov,destination){applyExactImageFov(ra,dec,fov,destination,'immediate');for(const ms of [160,420,900,1500])setTimeout(()=>{if(destinationStillCurrent(destination))applyExactImageFov(ra,dec,fov,destination,'delayed-'+ms)},ms)}
function chooseUrl(candidate){const p=processedReady.get(candidate.key);return p?{url:p.displayUrl,source:'processed-canvas-cache',originalUrl:candidate.url}:{url:candidate.url,source:'original-immediate',originalUrl:candidate.url}}
function loadForBestDestination(reason){
  installTravelButtonGuard(); swallowPanelTouches();
  const candidate=bestDestination(randomRef); if(!candidate)return false;
  const {d,key}=candidate;
  if(suppressed()){
    if(Date.now()<travelMinUntil)return false;
    if(travelOldKey&&key===travelOldKey)return false;
    suppressUntil=0;travelOldKey='';travelMinUntil=0;
  }
  if(!key)return false;
  if(key===lastKey){setPanelVisible(true);return true}
  if(key===loadingKey)return true;
  const chosen=chooseUrl(candidate);
  loadingKey=key;
  try{
    const op=opacityNow();
    overlay=ARef.image(chosen.url,{name:LAYER_NAME,imgFormat:/\.png(?:[?#]|$)/i.test(chosen.url)?'png':'jpeg',opacity:op,
      successCallback:(ra,dec,fov,image)=>{setExactImageFov(ra,dec,fov,d);lastKey=key;loadingKey='';setPanelVisible(true);preloadUpcoming('after-live-load');lastContext={version:VERSION,mode:chosen.source,reason,destination:d,url:chosen.url,originalUrl:chosen.originalUrl,opacity:opacityNow(),ra,dec,fov,image,overlay};global.GalaxyViewerAvmOverlayLab.lastContext=lastContext;console.info('GV AVM LAB 0015 AUTO LOADED',lastContext)},
      errorCallback:error=>{loadingKey='';console.warn('GV AVM LAB 0015 IMAGE LOAD FAILED',{reason,key,url:chosen.url,source:chosen.source,error});if(chosen.source!=='original-immediate'){processedReady.delete(key);setTimeout(()=>loadForBestDestination('fallback-original'),50)}}
    });
    if(!overlay)throw new Error('A.image returned empty overlay');
    if(typeof aladinRef.setOverlayImageLayer!=='function')throw new Error('ALADIN setOverlayImageLayer unavailable');
    aladinRef.setOverlayImageLayer(overlay,LAYER_NAME); applyOpacity(); return true;
  }catch(e){loadingKey='';console.error('GV AVM LAB 0015 FAILED',e);return false}
}
function install({aladin,A,randomGalaxy,viewerRoot}={}){
  ARef=A; aladinRef=aladin; randomRef=randomGalaxy;
  try{panel();setPanelVisible(false);swallowPanelTouches();installTravelButtonGuard()}catch(error){console.warn('GV AVM LAB 0015 PANEL SETUP WARNING',error)}
  try{const sl=slider();sl.addEventListener('input',applyOpacity,{passive:true});sl.addEventListener('change',applyOpacity,{passive:true});paintSlider()}catch(error){console.warn('GV AVM LAB 0015 SLIDER SETUP WARNING',error)}
  if(!preloadTimer)preloadTimer=setInterval(()=>preloadUpcoming('background'),1500);
  if(!watchTimer)watchTimer=setInterval(()=>loadForBestDestination('watch'),WATCH_MS);
  setTimeout(()=>loadForBestDestination('install-delay-1'),250);
  setTimeout(()=>preloadUpcoming('install-delay-preload'),1200);
  global.GalaxyViewerAvmOverlayLab.instance={VERSION,panel:panel(),load:()=>loadForBestDestination('manual-api'),preload:()=>preloadUpcoming('manual-api')};
  return global.GalaxyViewerAvmOverlayLab.instance;
}
function uninstall(){if(watchTimer){clearInterval(watchTimer);watchTimer=null} if(preloadTimer){clearInterval(preloadTimer);preloadTimer=null}}
global.GalaxyViewerAvmOverlayLab={VERSION,install,uninstall,loadForBestDestination,preloadUpcoming,get lastContext(){return lastContext},get cacheSize(){return processedReady.size}};
})();
