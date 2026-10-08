/* Galaxy Viewer CPU/GPU Diagnostics 0002
   Idle-by-default diagnostics with reliable long-press and explicit enable/disable.
*/
(()=>{"use strict";
const VERSION="0004",ROOT_ID="gv-cpu-gpu-diagnostics";
let root=null,button=null,statusButton=null,pressTimer=0,armed=false,raf=0,enabled=false,collecting=false,pointerId=null;
const frames=[],events=[],MAX=900;
let lastFrame=performance.now(),longTasks=[],eventLoopLag=[],longObserver=null,lagTimer=null;
function now(){return performance.now()}
function sampleFrame(t){const dt=t-lastFrame;lastFrame=t;if(dt>0)frames.push({t:Math.round(t),ms:+dt.toFixed(2),fps:+(1000/dt).toFixed(1)});if(frames.length>MAX)frames.shift();raf=requestAnimationFrame(sampleFrame)}
function resourceCounts(){const imgs=[...document.images],canvases=[...document.querySelectorAll("canvas")],scripts=[...document.scripts],links=[...document.querySelectorAll("link")];return{images:imgs.length,imagesComplete:imgs.filter(x=>x.complete).length,canvases:canvases.length,scripts:scripts.length,stylesheets:links.filter(x=>x.rel==="stylesheet").length,resourceEntries:performance.getEntriesByType("resource").length}}
function memory(){const m=performance.memory;return m?{usedJSHeapSize:m.usedJSHeapSize,totalJSHeapSize:m.totalJSHeapSize,jsHeapSizeLimit:m.jsHeapSizeLimit}:null}
function webgl(){try{const c=document.createElement("canvas"),g=c.getContext("webgl2")||c.getContext("webgl")||c.getContext("experimental-webgl");if(!g)return null;const d=g.getExtension("WEBGL_debug_renderer_info");return{version:g.getParameter(g.VERSION),shadingLanguage:g.getParameter(g.SHADING_LANGUAGE_VERSION),vendor:d?g.getParameter(d.UNMASKED_VENDOR_WEBGL):g.getParameter(g.VENDOR),renderer:d?g.getParameter(d.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER),maxTextureSize:g.getParameter(g.MAX_TEXTURE_SIZE),maxTextureUnits:g.getParameter(g.MAX_TEXTURE_IMAGE_UNITS)}}catch(e){return{error:String(e)}}}
function appState(){const o={urlCount:null,hdWindow:null,currentHd:null,hdOverlay:null,destination:null,travelRetired:null};try{if(typeof gvHdResourceSnapshot==="function"){const s=gvHdResourceSnapshot();o.hdWindow=s.window;o.urlCount=s.tracked;o.currentHd=s.current;o.hdOverlay=s.overlay}}catch(_){}try{o.destination=typeof directHdDestination!=="undefined"?String(directHdDestination?.name||directHdDestination?.archiveId||""):null}catch(_){}try{o.travelRetired=typeof gvHdTravelRetired!=="undefined"?!!gvHdTravelRetired:null}catch(_){}return o}
function esc(s){return String(s??"").replace(/[&<>"]/g,x=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[x]))}
function stats(){const a=frames.slice(-300).map(x=>x.ms).filter(x=>x>0).sort((a,b)=>a-b),n=a.length,at=p=>n?+a[Math.min(n-1,Math.floor(n*p))].toFixed(2):null,avg=n?+(a.reduce((x,y)=>x+y,0)/n).toFixed(2):null;return{samples:n,avgFrameMs:avg,p50FrameMs:at(.5),p95FrameMs:at(.95),p99FrameMs:at(.99),maxFrameMs:n?a[n-1]:null,fps:avg?+(1000/avg).toFixed(1):null,framesOver16_7:a.filter(x=>x>16.7).length,framesOver33:a.filter(x=>x>33).length,framesOver50:a.filter(x=>x>50).length,framesOver100:a.filter(x=>x>100).length}}
function report(){const c=document.createElement("canvas");return{schema:"GV-CPU-GPU-DIAGNOSTIC-0002",diagnosticsVersion:VERSION,timestamp:new Date().toISOString(),uptimeMs:Math.round(performance.now()),userAgent:navigator.userAgent,devicePixelRatio:devicePixelRatio,viewport:{width:innerWidth,height:innerHeight},hardware:{cores:navigator.hardwareConcurrency||null,deviceMemory:navigator.deviceMemory||null},memory:memory(),webgl:webgl(),rendering:stats(),app:appState(),capabilities:{performanceMemory:!!performance.memory,performanceObserver:!!window.PerformanceObserver,webgl2:!!c.getContext("webgl2")},resources:resourceCounts(),longTasks:longTasks.slice(-100),eventLoopLagMs:eventLoopLag.slice(-100),rollingFrameHistory:frames.slice(-300),events:events.slice(-100),enabled}}
async function copyReport(){const text=JSON.stringify(report(),null,2);try{await navigator.clipboard.writeText(text);return true}catch(_){const ta=document.createElement("textarea");ta.value=text;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();return true}}
function stopCollection(){if(!collecting)return;collecting=false;cancelAnimationFrame(raf);raf=0;clearInterval(lagTimer);lagTimer=null;longObserver?.disconnect();longObserver=null}
function setEnabled(value){enabled=!!value;try{localStorage.setItem("gvDiagnosticsEnabled0004",enabled?"1":"0")}catch(_){}if(!enabled){armed=false;clearTimeout(pressTimer);stopCollection()}else{startCollection()}updateStatusButton();if(root)renderPanel()}
function updateStatusButton(){if(!statusButton){statusButton=document.createElement("button");statusButton.id=ROOT_ID+"-status";statusButton.type="button";statusButton.style.cssText="position:fixed;left:8px;top:56px;z-index:2147483647;padding:7px 9px;border:2px solid;border-radius:7px;font:700 10px monospace;letter-spacing:.3px;box-shadow:0 2px 10px rgba(0,0,0,.55);cursor:pointer";statusButton.addEventListener("click",()=>{setEnabled(!enabled);open()});document.body.appendChild(statusButton)}statusButton.textContent=enabled?"DIAGNOSTICS: ON":"DIAGNOSTICS: OFF";statusButton.style.background=enabled?"#087a36":"#a71925";statusButton.style.color="#ffffff";statusButton.style.borderColor=enabled?"#7dffad":"#ff9da5";statusButton.setAttribute("aria-label",enabled?"Diagnostics on. Tap to turn off":"Diagnostics off. Tap to turn on");statusButton.setAttribute("aria-pressed",String(enabled))}\nfunction renderPanel(){if(!root)return;updateStatusButton();const r=report(),m=r.memory,w=r.webgl,s=r.rendering,a=r.app;root.innerHTML="<b>CPU / GPU DIAGNOSTICS</b>  "+esc(r.timestamp)+"\n"+ "Status: <b>"+(enabled?"ENABLED":"DISABLED")+"</b> (idle unless sampling)\n"+"FPS "+esc(s.fps)+" | avg "+esc(s.avgFrameMs)+" ms | P95 "+esc(s.p95FrameMs)+" ms | MAX "+esc(s.maxFrameMs)+" ms\n"+">16.7ms "+esc(s.framesOver16_7)+" | >33ms "+esc(s.framesOver33)+" | >50ms "+esc(s.framesOver50)+" | >100ms "+esc(s.framesOver100)+"\n"+"JS heap "+esc(m?Math.round(m.usedJSHeapSize/1048576)+" / "+Math.round(m.jsHeapSizeLimit/1048576)+" MB":"unavailable")+"\n"+"HD resources "+esc(a.urlCount)+" / window "+esc(a.hdWindow)+" | layer "+esc(a.hdOverlay)+" | current "+esc(a.currentHd)+"\n"+"GPU "+esc(w?.renderer||"unavailable")+"\n"+"<button id='"+ROOT_ID+"-toggle' style='margin-top:8px;padding:7px 10px;border:2px solid; border-radius:6px;background:"+(enabled?"#087a36":"#a71925")+";color:#fff;font-weight:bold'>"+(enabled?"DIAGNOSTICS: ON":"DIAGNOSTICS: OFF")+"</button> <button id='"+ROOT_ID+"-copy' style='margin:8px 4px 0;padding:7px 10px'>COPY REPORT</button> <button id='"+ROOT_ID+"-close' style='margin-top:8px;padding:7px 10px'>CLOSE</button>";
root.querySelector("#"+ROOT_ID+"-toggle").onclick=()=>setEnabled(!enabled);
root.querySelector("#"+ROOT_ID+"-copy").onclick=async()=>{await copyReport();const b=root?.querySelector("#"+ROOT_ID+"-copy");if(b){b.textContent="COPIED";setTimeout(()=>{const x=root?.querySelector("#"+ROOT_ID+"-copy");if(x)x.textContent="COPY REPORT"},1200)}};
root.querySelector("#"+ROOT_ID+"-close").onclick=()=>{root.remove();root=null}}
function open(){if(!root){root=document.createElement("div");root.id=ROOT_ID;root.style.cssText="position:fixed;left:8px;right:8px;top:56px;z-index:2147483647;padding:10px;border:1px solid rgba(120,255,180,.8);border-radius:8px;background:rgba(0,8,12,.96);color:#eafff2;font:12px monospace;box-shadow:0 4px 20px rgba(0,0,0,.5);white-space:pre-wrap";document.body.appendChild(root)}renderPanel()}
function startCollection(){if(!enabled||collecting)return;collecting=true;lastFrame=now();raf=requestAnimationFrame(sampleFrame);if("PerformanceObserver"in window){try{longObserver=new PerformanceObserver(list=>{for(const e of list.getEntries())longTasks.push({start:e.startTime,duration:e.duration});if(longTasks.length>100)longTasks=longTasks.slice(-100)});longObserver.observe({type:"longtask",buffered:true})}catch(_){}}let expected=now()+250;lagTimer=setInterval(()=>{const t=now(),lag=Math.max(0,t-expected);eventLoopLag.push(+lag.toFixed(2));if(eventLoopLag.length>100)eventLoopLag.shift();expected+=250},250)}
function finishHold(){armed=false;clearTimeout(pressTimer);stopCollection();try{if(pointerId!==null)button?.releasePointerCapture?.(pointerId)}catch(_){}pointerId=null}
function toggleFromLongPress(){
  if(!armed)return;
  finishHold();
  if(!enabled){
    setEnabled(true);
    events.push({t:new Date().toISOString(),type:"long-press-enabled"});
    startCollection();
    open();
    return;
  }
  events.push({t:new Date().toISOString(),type:"long-press-disabled"});
  setEnabled(false);
  open();
}
function onDown(e){
  if(e.isPrimary===false||(e.button!==undefined&&e.button!==0))return;
  clearTimeout(pressTimer);armed=true;pointerId=e.pointerId??null;
  try{if(pointerId!==null)button?.setPointerCapture?.(pointerId)}catch(_){}
  // Do not sample while the user is deciding whether to activate diagnostics.
  pressTimer=setTimeout(toggleFromLongPress,3000);
}
function onUp(){if(!armed)return;finishHold()}
function keyDown(e){
  if(!(e.key==="Enter"||e.key===" "||e.key==="Spacebar")||e.repeat)return;
  armed=true;clearTimeout(pressTimer);pressTimer=setTimeout(toggleFromLongPress,3000)
}
function keyUp(e){if(e.key==="Enter"||e.key===" "||e.key==="Spacebar")onUp()}

function attach(){const b=document.querySelector("button.gv-target-survey-button");if(!b||b===button)return;if(button){button.removeEventListener("pointerdown",onDown,true);button.removeEventListener("pointerup",onUp,true);button.removeEventListener("pointercancel",onUp,true);button.removeEventListener("keydown",keyDown,true);button.removeEventListener("keyup",keyUp,true)}button=b;b.addEventListener("pointerdown",onDown,true);b.addEventListener("pointerup",onUp,true);b.addEventListener("pointercancel",onUp,true);b.addEventListener("keydown",keyDown,true);b.addEventListener("keyup",keyUp,true)}
function mount(){attach();updateStatusButton();if(enabled)startCollection();window.addEventListener("beforeunload",unmount,{once:true});console.log("GV CPU/GPU DIAGNOSTICS 0002 MOUNTED — STATUS BUTTON VISIBLE; green ON / red OFF")}
function unmount(){finishHold();stopCollection();if(button){button.removeEventListener("pointerdown",onDown,true);button.removeEventListener("pointerup",onUp,true);button.removeEventListener("pointercancel",onUp,true);button.removeEventListener("keydown",keyDown,true);button.removeEventListener("keyup",keyUp,true);button=null}root?.remove();root=null;statusButton?.remove();statusButton=null}
try{enabled=localStorage.getItem("gvDiagnosticsEnabled0004")==="1"}catch(_){}
const api={version:VERSION,mount,unmount,open,snapshot:report,copy:copyReport,setEnabled,get enabled(){return enabled}};
globalThis.GV_CPU_GPU_DIAGNOSTICS=api;window.GalaxyViewerDiagnostics=api;
})();