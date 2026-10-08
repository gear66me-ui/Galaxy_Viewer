/* Galaxy Viewer CPU/GPU Diagnostics 0001
   Isolated diagnostics module. It does not modify the target scene.
*/
(()=>{"use strict";
const VERSION="0001",ROOT_ID="gv-cpu-gpu-diagnostics";
let root=null,button=null,pressTimer=null,pressStarted=0,armed=false,raf=0;
const frames=[],events=[],MAX=900;
let lastFrame=performance.now(),lastLong=0,longTasks=[],eventLoopLag=[];let longObserver=null;let lagTimer=null;
function now(){return performance.now()}
function sampleFrame(t){
  const dt=t-lastFrame; lastFrame=t;
  if(dt>0) frames.push({t:Math.round(t),ms:Number(dt.toFixed(2)),fps:Number((1000/dt).toFixed(1))});
  if(frames.length>MAX)frames.shift();
  raf=requestAnimationFrame(sampleFrame);
}
function resourceCounts(){const imgs=[...document.images],canvases=[...document.querySelectorAll('canvas')],scripts=[...document.scripts],links=[...document.querySelectorAll('link')];return {images:imgs.length,imagesComplete:imgs.filter(x=>x.complete).length,canvases:canvases.length,scripts:scripts.length,stylesheets:links.filter(x=>x.rel==='stylesheet').length,resourceEntries:performance.getEntriesByType('resource').length}}\nasync function cacheStorage(){try{if(!globalThis.caches)return null;const names=await caches.keys(),counts={};for(const n of names){try{counts[n]=(await caches.open(n)).length}catch(_){counts[n]=null}}return {cacheNames:names,entryCounts:counts}}catch(e){return {error:String(e)}}}\nfunction memory(){
  const m=performance.memory;
  return m?{usedJSHeapSize:m.usedJSHeapSize,totalJSHeapSize:m.totalJSHeapSize,jsHeapSizeLimit:m.jsHeapSizeLimit}:null;
}
function webgl(){
  try{
    const c=document.createElement("canvas"),g=c.getContext("webgl2")||c.getContext("webgl")||c.getContext("experimental-webgl");
    if(!g)return null;
    const dbg=g.getExtension("WEBGL_debug_renderer_info");
    return {version:g.getParameter(g.VERSION),shadingLanguage:g.getParameter(g.SHADING_LANGUAGE_VERSION),vendor:dbg?g.getParameter(dbg.UNMASKED_VENDOR_WEBGL):g.getParameter(g.VENDOR),renderer:dbg?g.getParameter(dbg.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER),maxTextureSize:g.getParameter(g.MAX_TEXTURE_SIZE),maxTextureUnits:g.getParameter(g.MAX_TEXTURE_IMAGE_UNITS)};
  }catch(e){return {error:String(e)}}
}
function appState(){
  const o={urlCount:null,hdWindow:null,currentHd:null,hdOverlay:null,destination:null,travelRetired:null};
  try{if(typeof gvHdResourceSnapshot==="function"){const s=gvHdResourceSnapshot();o.hdWindow=s.window;o.urlCount=s.tracked;o.currentHd=s.current;o.hdOverlay=s.overlay}}catch(_){}
  try{o.destination=typeof directHdDestination!=="undefined"?String(directHdDestination?.name||directHdDestination?.archiveId||""):null}catch(_){}
  try{o.travelRetired=typeof gvHdTravelRetired!=="undefined"?!!gvHdTravelRetired:null}catch(_){}
  return o;
}
function targetRoot(){return document.querySelector(".gv-target-survey-root")}
function targetButton(){return document.querySelector("button.gv-target-survey-button")}
function targetHandler(e){
  if(e.type==="pointerdown"){
    if(e.button!==undefined&&e.button!==0)return;
    clearTimeout(pressTimer);pressStarted=now();armed=true;
    pressTimer=setTimeout(()=>{if(armed)showReport()},3000);
  }else if(e.type==="pointerup"||e.type==="pointercancel"||e.type==="pointerleave"){armed=false;clearTimeout(pressTimer)}
}
function keyHandler(e){if(e.key==="Enter"||e.key===" "||e.key==="Spacebar"){clearTimeout(pressTimer);pressStarted=now();pressTimer=setTimeout(()=>showReport(),3000)}}
function attach(){
  const r=targetRoot(); if(!r||r===button)return;
  if(button){button.removeEventListener("pointerdown",targetHandler,true);button.removeEventListener("pointerup",targetHandler,true);button.removeEventListener("pointercancel",targetHandler,true);button.removeEventListener("pointerleave",targetHandler,true);button.removeEventListener("keydown",keyHandler,true)}
  button=r;
  r.addEventListener("pointerdown",targetHandler,true);r.addEventListener("pointerup",targetHandler,true);r.addEventListener("pointercancel",targetHandler,true);r.addEventListener("pointerleave",targetHandler,true);r.addEventListener("keydown",keyHandler,true);
}
function esc(s){return String(s??"").replace(/[&<>"]/g,x=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[x]))}
function stats(){
  const a=frames.slice(-300).map(x=>x.ms).filter(x=>x>0).sort((a,b)=>a-b),n=a.length;
  const at=p=>n?Number(a[Math.min(n-1,Math.floor(n*p))].toFixed(2)):null;
  const avg=n?Number((a.reduce((x,y)=>x+y,0)/n).toFixed(2)):null;
  return {samples:n,avgFrameMs:avg,p50FrameMs:at(.50),p95FrameMs:at(.95),p99FrameMs:at(.99),maxFrameMs:n?a[n-1]:null,fps:avg?Number((1000/avg).toFixed(1)):null,framesOver16_7:a.filter(x=>x>16.7).length,framesOver33:a.filter(x=>x>33).length,framesOver50:a.filter(x=>x>50).length,framesOver100:a.filter(x=>x>100).length};
}
function report(){
  const r={schema:"GV-CPU-GPU-DIAGNOSTIC-0001",diagnosticsVersion:VERSION,timestamp:new Date().toISOString(),uptimeMs:Math.round(performance.now()),userAgent:navigator.userAgent,devicePixelRatio:devicePixelRatio,viewport:{width:innerWidth,height:innerHeight},hardware:{cores:navigator.hardwareConcurrency||null,deviceMemory:navigator.deviceMemory||null},memory:memory(),webgl:webgl(),rendering:stats(),app:appState(),capabilities:{performanceMemory:!!performance.memory,performanceObserver:!!window.PerformanceObserver,webgl2:!!document.createElement("canvas").getContext("webgl2")},resources:resourceCounts(),longTasks:longTasks.slice(-100),eventLoopLagMs:eventLoopLag.slice(-100),rollingFrameHistory:frames.slice(-300),events:events.slice(-100)};
  return r;
}
async function copyReport(){
  const text=JSON.stringify(report(),null,2);
  try{await navigator.clipboard.writeText(text);return true}catch(_){
    const ta=document.createElement("textarea");ta.value=text;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();return true;
  }
}
function showReport(){
  armed=false;clearTimeout(pressTimer);events.push({t:new Date().toISOString(),type:"snapshot"});
  if(!root){root=document.createElement("div");root.id=ROOT_ID;root.style.cssText="position:fixed;left:8px;right:8px;top:56px;z-index:2147483647;padding:10px;border:1px solid rgba(120,255,180,.8);border-radius:8px;background:rgba(0,8,12,.94);color:#eafff2;font:12px monospace;box-shadow:0 4px 20px rgba(0,0,0,.5);white-space:pre-wrap";document.body.appendChild(root)}
  const r=report(),m=r.memory,w=r.webgl,s=r.rendering,a=r.app;
  root.innerHTML="<b>CPU / GPU DIAGNOSTICS</b>  "+esc(r.timestamp)+"\n"+
    "FPS "+esc(s.fps)+" | frame avg "+esc(s.avgFrameMs)+" ms | P95 "+esc(s.p95FrameMs)+" ms | MAX "+esc(s.maxFrameMs)+" ms\n"+
    ">16.7ms "+esc(s.framesOver16_7)+" | >33ms "+esc(s.framesOver33)+" | >50ms "+esc(s.framesOver50)+" | >100ms "+esc(s.framesOver100)+"\n"+
    "JS heap "+esc(m?Math.round(m.usedJSHeapSize/1048576)+" / "+Math.round(m.jsHeapSizeLimit/1048576)+" MB":"unavailable")+"\n"+
    "HD resources "+esc(a.urlCount)+" / window "+esc(a.hdWindow)+" | layer "+esc(a.hdOverlay)+" | current "+esc(a.currentHd)+"\n"+
    "GPU "+esc(w?.renderer||"unavailable")+"\n"+
    "<button id='"+ROOT_ID+"-copy' style='margin-top:8px;padding:6px 10px'>COPY FULL DIAGNOSTIC</button> <button id='"+ROOT_ID+"-close' style='margin-top:8px;padding:6px 10px'>CLOSE</button>";
  root.querySelector("#"+ROOT_ID+"-copy").onclick=async()=>{await copyReport();root.querySelector("#"+ROOT_ID+"-copy").textContent="COPIED";setTimeout(()=>root.querySelector("#"+ROOT_ID+"-copy").textContent="COPY FULL DIAGNOSTIC",1200)};
  root.querySelector("#"+ROOT_ID+"-close").onclick=()=>{root.remove();root=null};
}
function mount(){
  if(raf)return;
  raf=requestAnimationFrame(sampleFrame);
  if('PerformanceObserver' in window){try{longObserver=new PerformanceObserver(list=>{for(const e of list.getEntries())longTasks.push({start:e.startTime,duration:e.duration});if(longTasks.length>100)longTasks=longTasks.slice(-100)});longObserver.observe({type:'longtask',buffered:true})}catch(_){}}
  let expected=now()+250;lagTimer=setInterval(()=>{const t=now(),lag=Math.max(0,t-expected);eventLoopLag.push(Number(lag.toFixed(2)));if(eventLoopLag.length>100)eventLoopLag.shift();expected+=250},250);
  attach();
  window.addEventListener("beforeunload",unmount,{once:true});
  console.log("GV CPU/GPU DIAGNOSTICS 0001 MOUNTED — hold target 3 seconds");
}
function unmount(){
  cancelAnimationFrame(raf);raf=0;clearTimeout(pressTimer);armed=false;
  if(button){button.removeEventListener("pointerdown",targetHandler,true);button.removeEventListener("pointerup",targetHandler,true);button.removeEventListener("pointercancel",targetHandler,true);button.removeEventListener("pointerleave",targetHandler,true);button.removeEventListener("keydown",keyHandler,true);button=null}
  longObserver?.disconnect();longObserver=null;if(lagTimer){clearInterval(lagTimer);lagTimer=null}root?.remove();root=null;
}
globalThis.GV_CPU_GPU_DIAGNOSTICS={version:VERSION,mount,unmount,snapshot:report,copy:copyReport};
})();
