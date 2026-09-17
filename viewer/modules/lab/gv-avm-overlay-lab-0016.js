(()=>{
'use strict';
const VERSION="0016";
const WATCH_MS=180;
const LAYER_NAME="Galaxy Viewer AVM Overlay";
const PANEL_ID="gv-avm-overlay-lab";
const STYLE_ID="gv-avm-overlay-lab-style-0016";
const DEFAULT_SLIDER="0";
const PROCESSED_QUALITY=0.92;
let ARef=null;
let aladinRef=null;
let randomRef=null;
let rootRef=null;
let overlay=null;
let watchTimer=null;
let retryTimers=[];
let lastKey="";
let loadingKey="";
let processedLoadingKey="";
let processedReady=new Map();
let lastContext=null;
let suppressUntil=0;
let travelOldKey="";
let travelMinUntil=0;
function clamp(n,min,max){n=Number(n);if(!Number.isFinite(n))n=min;return Math.max(min,Math.min(max,n))}
function panel(){return document.getElementById(PANEL_ID)}
function hdOpen(){return document.body?.classList?.contains('gv-hd-open')||document.documentElement?.classList?.contains('gv-hd-open')}
function slider(){return panel()?.querySelector('input[type="range"]')||null}
function opacityNow(){const sl=slider();const raw=sl?sl.value:DEFAULT_SLIDER;const v=clamp(raw,0,100);return clamp(1-(v/100),0,1)}
function applyOpacity(){const op=opacityNow();try{if(overlay&&typeof overlay.setOpacity==="function")overlay.setOpacity(op)}catch(_){}try{if(overlay&&typeof overlay.setAlpha==="function")overlay.setAlpha(op)}catch(_){}return op}
function setPanelVisible(on){const p=panel();if(!p)return;if(hdOpen())on=false;p.dataset.on=on?'1':'0';p.style.display=on?'block':'none'}
function ensureStyle(){if(document.getElementById(STYLE_ID))return;const st=document.createElement('style');st.id=STYLE_ID;st.textContent=`
#${PANEL_ID}{position:fixed;left:10px;top:620px;width:92px;height:184px;z-index:7312;display:none;pointer-events:none;font-family:"Space Age",sans-serif;color:#9eefff;filter:drop-shadow(0 0 10px rgba(76,205,255,.82))}
#${PANEL_ID}[data-on="1"]{display:block}
body.gv-hd-open #${PANEL_ID},html.gv-hd-open #${PANEL_ID}{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#${PANEL_ID} .gv-avm-touch-shield{position:absolute;inset:0;border-radius:24px;background:rgba(0,22,54,.16);pointer-events:auto;touch-action:none;overscroll-behavior:contain}
#${PANEL_ID} .gv-avm-title{position:absolute;left:-12px;top:50%;transform:translateY(-50%);height:144px;display:flex;align-items:center;justify-content:center;writing-mode:vertical-rl;text-orientation:mixed;font:400 10px/1 "Space Age",sans-serif;letter-spacing:3px;color:#6feaff;text-shadow:0 0 4px rgba(190,250,255,.96),0 0 10px rgba(35,190,255,.9);user-select:none;pointer-events:none;white-space:nowrap}
#${PANEL_ID} .gv-avm-slider-wrap{position:absolute;left:32px;top:8px;width:48px;height:168px;display:flex;align-items:center;justify-content:center;pointer-events:auto;touch-action:none}
#${PANEL_ID} input[type="range"]{position:absolute;width:164px;height:34px;transform:rotate(-90deg);appearance:none;-webkit-appearance:none;background:linear-gradient(90deg,rgba(4,18,58,.82),rgba(18,187,255,.95));border-radius:999px;outline:none;box-shadow:0 0 8px rgba(100,226,255,.88),0 0 18px rgba(18,157,255,.72);pointer-events:auto;touch-action:none}
#${PANEL_ID} input[type="range"]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:36px;height:36px;border-radius:50%;background:#72e8ff;border:2px solid rgba(224,255,255,.98);box-shadow:0 0 10px rgba(185,250,255,.98),0 0 25px rgba(20,176,255,.8)}
#${PANEL_ID} input[type="range"]::-moz-range-thumb{width:36px;height:36px;border-radius:50%;background:#72e8ff;border:2px solid rgba(224,255,255,.98);box-shadow:0 0 10px rgba(185,250,255,.98),0 0 25px rgba(20,176,255,.8)}
@media(max-height:740px){#${PANEL_ID}{top:520px;height:164px}#${PANEL_ID} .gv-avm-slider-wrap{height:150px}#${PANEL_ID} input[type="range"]{width:148px}}
`;document.head.appendChild(st)}
function ensurePanel(){ensureStyle();let p=panel();if(p)return p;p=document.createElement('div');p.id=PANEL_ID;p.dataset.on='0';p.innerHTML='<div class="gv-avm-touch-shield" aria-hidden="true"></div><div class="gv-avm-title">CROSS FADE</div><div class="gv-avm-slider-wrap"><input aria-label="CROSS FADE" type="range" min="0" max="100" step="1" value="'+DEFAULT_SLIDER+'"></div>';document.body.appendChild(p);const sl=slider();if(sl){sl.addEventListener('input',()=>{applyOpacity();setPanelVisible(!!lastKey)},{passive:true});sl.addEventListener('change',()=>{applyOpacity();setPanelVisible(!!lastKey)},{passive:true})}return p}
function swallowPanelTouches(){const p=ensurePanel();for(const el of [p,p.querySelector('.gv-avm-touch-shield'),p.querySelector('input')]){if(!el||el.dataset.gvAvmShield0016)return;el.dataset.gvAvmShield0016='1';for(const ev of ['pointerdown','pointermove','pointerup','touchstart','touchmove','touchend','mousedown','mousemove','mouseup','click']){el.addEventListener(ev,e=>{if(ev!=='click')e.stopPropagation();},{capture:true,passive:true})}}}
function stateOf(rg){try{return rg?.getState?.()||{}}catch(_){return {}}}
function avmUrlFor(d){if(!d)return '';return d.selectedImageUrl||d.imageUrl||d.screenUrl||d.hdUrl||d.largeUrl||d.url||d.thumbnailUrl||''}
function destinationKey(d,url){if(!d&&!url)return '';return String(d?.id||d?.archiveId||d?.sourceId||d?.designation||d?.name||url||'').trim()+'|'+String(url||avmUrlFor(d)||'').trim()}
function addCandidate(out,d){const url=avmUrlFor(d);if(!url)return;const key=destinationKey(d,url);if(!key)return;if(out.some(x=>x.key===key))return;out.push({d,url,key})}
function liveCandidates(randomGalaxy){const s=stateOf(randomGalaxy);const g=globalThis.GalaxyRandomGalaxy||{};const out=[];for(const d of [s.activeDestination,s.currentDestination,randomGalaxy?.activeDestination,randomGalaxy?.currentDestination,g.activeDestination,g.currentDestination])addCandidate(out,d);return out}
function bestDestination(randomGalaxy){const c=liveCandidates(randomGalaxy);return c[0]||null}
function currentKey(){return bestDestination(randomRef)?.key||''}
function destinationStillCurrent(key){return !!key&&key===currentKey()}
function clearOverlay(){try{if(aladinRef&&typeof aladinRef.removeOverlayImageLayer==='function')aladinRef.removeOverlayImageLayer(LAYER_NAME)}catch(_){}overlay=null;lastKey='';loadingKey='';setPanelVisible(false)}
function suppressed(){return Date.now()<suppressUntil}
function hideOverlayForTravel(){const old=currentKey();travelOldKey=old;travelMinUntil=Date.now()+450;suppressUntil=Date.now()+26000;clearOverlay();const waits=[250,500,850,1250,1800,2600,3600,5000,7000,9300,12000,15500,19500,23500];for(const ms of waits)retryTimers.push(setTimeout(()=>loadForBestDestination('travel-poll-'+ms),ms))}
function installTravelButtonGuard(){const buttons=document.querySelectorAll('#gv-random-galaxy,.gv-galaxy-history');for(const b of buttons){if(!b||b.dataset.gvAvmGuard0016)continue;b.dataset.gvAvmGuard0016='1';for(const ev of ['pointerdown','touchstart','click'])b.addEventListener(ev,hideOverlayForTravel,{capture:true,passive:true})}}
function imageFormatFor(url){return /\.png(?:[?#]|$)/i.test(url)?'png':'jpeg'}
function setExactImageFov(ra,dec,fov,d){try{if(Number.isFinite(ra)&&Number.isFinite(dec)&&typeof aladinRef.gotoRaDec==='function')aladinRef.gotoRaDec(ra,dec)}catch(_){}try{const x=Number(d?.imageFovXDeg);const y=Number(d?.imageFovYDeg);const scalar=Number(d?.imageFovDeg||d?.fovDegrees||d?.fov||fov);let target=scalar;if(Number.isFinite(x)&&x>0&&Number.isFinite(y)&&y>0){const rect=(rootRef||document.body).getBoundingClientRect?.();const aspect=(rect&&rect.height>0)?rect.width/rect.height:1;target=Math.max(x,y*aspect)}if(Number.isFinite(target)&&target>0){if(typeof aladinRef.setFoV==='function')aladinRef.setFoV(target);else if(typeof aladinRef.setFov==='function')aladinRef.setFov(target)}}catch(e){try{console.warn('GV AVM LAB 0016 FOV WARNING',e)}catch(_){}}}
async function fetchImageBlob(url){const res=await fetch(url,{mode:'cors',cache:'force-cache',credentials:'omit'});if(!res.ok)throw new Error('fetch image failed '+res.status);return await res.blob()}
function loadHtmlImage(url){return new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=()=>reject(new Error('image decode failed'));img.src=url})}
async function createVignettedUrl(originalUrl,key,reason){const blob=await fetchImageBlob(originalUrl);const rawUrl=URL.createObjectURL(blob);let img=null;try{img=await loadHtmlImage(rawUrl)}finally{try{URL.revokeObjectURL(rawUrl)}catch(_){}}const w=img.naturalWidth||img.width;const h=img.naturalHeight||img.height;if(!(w>0&&h>0))throw new Error('invalid image size');const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;const ctx=canvas.getContext('2d');ctx.drawImage(img,0,0,w,h);const g=ctx.createRadialGradient(w/2,h/2,Math.min(w,h)*0.18,w/2,h/2,Math.max(w,h)*0.73);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(.55,'rgba(0,0,0,0)');g.addColorStop(.82,'rgba(2,12,35,.22)');g.addColorStop(1,'rgba(0,2,12,.70)');ctx.globalCompositeOperation='source-over';ctx.fillStyle=g;ctx.fillRect(0,0,w,h);const outBlob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',PROCESSED_QUALITY));if(!outBlob)throw new Error('canvas toBlob failed');return {url:URL.createObjectURL(outBlob),key,originalUrl,reason,width:w,height:h,createdAt:Date.now()}}
function processCurrentAfterVisible(candidate,why){if(!candidate||processedReady.has(candidate.key)||processedLoadingKey===candidate.key)return;processedLoadingKey=candidate.key;setTimeout(()=>{createVignettedUrl(candidate.url,candidate.key,why).then(item=>{processedLoadingKey='';processedReady.set(candidate.key,item);try{console.info('GV AVM LAB 0016 IMAGE VIGNETTE READY',item)}catch(_){}if(destinationStillCurrent(candidate.key))swapToProcessed(candidate,item,'processed-current-ready')}).catch(error=>{processedLoadingKey='';try{console.warn('GV AVM LAB 0016 IMAGE VIGNETTE FAILED',{key:candidate.key,url:candidate.url,error})}catch(_){}})},650)}
function swapToProcessed(candidate,item,reason){if(!candidate||!item||!destinationStillCurrent(candidate.key)||hdOpen())return false;try{const op=opacityNow();const proc=ARef.image(item.url,{name:LAYER_NAME,imgFormat:'jpeg',opacity:op,successCallback:(ra,dec,fov,image)=>{setExactImageFov(ra,dec,fov,candidate.d);lastKey=candidate.key;loadingKey='';setPanelVisible(true);lastContext={version:VERSION,mode:'processed-current-only',reason,destination:candidate.d,url:item.url,originalUrl:candidate.url,opacity:opacityNow(),ra,dec,fov,image,overlay:proc};globalThis.GalaxyViewerAvmOverlayLab.lastContext=lastContext;try{console.info('GV AVM LAB 0016 PROCESSED CURRENT LOADED',lastContext)}catch(_){}}});if(!proc)return false;overlay=proc;if(typeof aladinRef.setOverlayImageLayer==='function')aladinRef.setOverlayImageLayer(proc,LAYER_NAME);applyOpacity();return true}catch(e){try{console.warn('GV AVM LAB 0016 PROCESSED SWAP FAILED',e)}catch(_){}return false}}
function loadForBestDestination(reason){installTravelButtonGuard();swallowPanelTouches();if(hdOpen()){setPanelVisible(false);return false}const candidate=bestDestination(randomRef);if(!candidate)return false;const key=candidate.key;if(suppressed()){if(Date.now()<travelMinUntil)return false;if(travelOldKey&&key===travelOldKey)return false;suppressUntil=0;travelOldKey='';travelMinUntil=0}if(!key)return false;if(key===lastKey){setPanelVisible(true);processCurrentAfterVisible(candidate,'same-current');return true}if(key===loadingKey)return true;loadingKey=key;try{const op=opacityNow();const url=candidate.url;overlay=ARef.image(url,{name:LAYER_NAME,imgFormat:imageFormatFor(url),opacity:op,successCallback:(ra,dec,fov,image)=>{setExactImageFov(ra,dec,fov,candidate.d);lastKey=key;loadingKey='';setPanelVisible(true);lastContext={version:VERSION,mode:'original-immediate-active-only',reason,destination:candidate.d,url,opacity:opacityNow(),ra,dec,fov,image,overlay};globalThis.GalaxyViewerAvmOverlayLab.lastContext=lastContext;try{console.info('GV AVM LAB 0016 ORIGINAL CURRENT LOADED',lastContext)}catch(_){}processCurrentAfterVisible(candidate,'after-original-visible')},errorCallback:(error)=>{loadingKey='';try{console.warn('GV AVM LAB 0016 IMAGE LOAD FAILED',{reason,key,url,error})}catch(_){}}});if(!overlay)throw new Error('A.image returned empty overlay');if(typeof aladinRef.setOverlayImageLayer!=='function')throw new Error('ALADIN setOverlayImageLayer unavailable');aladinRef.setOverlayImageLayer(overlay,LAYER_NAME);applyOpacity();return true}catch(e){loadingKey='';try{console.error('GV AVM LAB 0016 FAILED',e)}catch(_){}return false}}
function install({A,aladin,viewerRoot,randomGalaxy}={}){if(!A)throw new Error('ALADIN A NAMESPACE MISSING');if(!aladin)throw new Error('ALADIN INSTANCE MISSING');ARef=A;aladinRef=aladin;randomRef=randomGalaxy;rootRef=viewerRoot||document.body;ensurePanel();swallowPanelTouches();installTravelButtonGuard();setPanelVisible(false);retryTimers.push(setTimeout(()=>loadForBestDestination('install-delay-1'),300));retryTimers.push(setTimeout(()=>loadForBestDestination('install-delay-2'),850));retryTimers.push(setTimeout(()=>loadForBestDestination('install-delay-3'),1600));if(!watchTimer)watchTimer=setInterval(()=>{if(hdOpen())setPanelVisible(false);else loadForBestDestination('watch')},WATCH_MS);try{console.info('GV AVM LAB 0016 INSTALLED active-only no-upcoming-display')}catch(_){}return {version:VERSION,panel:panel(),loadForBestDestination}}
function uninstall(){for(const t of retryTimers){try{clearTimeout(t)}catch(_){}}retryTimers=[];if(watchTimer){clearInterval(watchTimer);watchTimer=null}clearOverlay();try{panel()?.remove()}catch(_){}try{document.getElementById(STYLE_ID)?.remove()}catch(_){}}
globalThis.GalaxyViewerAvmOverlayLab={VERSION,install,uninstall,loadForBestDestination,get lastContext(){return lastContext},get cacheSize(){return processedReady.size}};
})();
