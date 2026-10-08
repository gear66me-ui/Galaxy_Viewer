/* Galaxy Viewer CPU/GPU Diagnostics 0002 — status UI and sampling restore
   Idle-by-default diagnostics with reliable long-press and explicit enable/disable.
*/
(()=>{"use strict";
const VERSION="0008",ROOT_ID="gv-cpu-gpu-diagnostics";
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
function setEnabled(value){enabled=!!value;if(!enabled){armed=false;clearTimeout(pressTimer);stopCollection()}else{startCollection()}updateStatusButton();if(root)renderPanel()}
function updateStatusButton(){if(!statusButton){statusButton=document.createElement("button");statusButton.id=ROOT_ID+"-status";statusButton.type="button";statusButton.style.cssText="position:fixed;left:8px;top:56px;z-index:2147483647;padding:8px 11px;border:1px solid;border-radius:9px;font:800 10px system-ui,sans-serif;letter-spacing:.6px;box-shadow:0 3px 14px rgba(0,0,0,.45);cursor:pointer";statusButton.addEventListener("click",()=>{if(enabled){setEnabled(false);open()}else open()});document.body.appendChild(statusButton)}statusButton.textContent=enabled?"● DIAGNOSTICS ON":"● DIAGNOSTICS OFF";statusButton.style.background=enabled?"#087a36":"#8f1d2b";statusButton.style.color="#ffffff";statusButton.style.borderColor=enabled?"#7dffad":"#ff9da5";statusButton.setAttribute("aria-label",enabled?"Diagnostics on. Tap to turn off":"Diagnostics off. Tap to open manual controls");statusButton.setAttribute("aria-pressed",String(enabled))}
function renderPanel(){
if(!root)return;
updateStatusButton();
const r=report(),m=r.memory,w=r.webgl,s=r.rendering,a=r.app;
const metric=(label,value,unit,sub)=>"<article class='gv-metric'><div class='gv-metric-label'>"+label+"</div><div class='gv-metric-value'>"+esc(value??"—")+"<small>"+(unit||"")+"</small></div><div class='gv-metric-sub'>"+sub+"</div></article>";
root.innerHTML="<div class='gv-dash'>"+
"<header class='gv-head'><div class='gv-brand'><div class='gv-orbit'>✦</div><div><div class='gv-kicker'>GALAXY VIEWER / SYSTEM TOOLS</div><h2>Performance Diagnostics</h2><p>Live rendering, memory and resource telemetry</p></div></div><button class='gv-x' id='"+ROOT_ID+"-close' aria-label='Close diagnostics'>×</button></header>"+
"<section class='gv-state "+(enabled?"gv-on":"gv-off")+"'><span class='gv-led'></span><div class='gv-state-copy'><strong>"+(enabled?"DIAGNOSTICS ACTIVE":"DIAGNOSTICS OFF")+"</strong><span>"+(enabled?"Sampling is running. Turn it off when finished.":"Nothing is being sampled. Enable manually when you want a test.")+"</span></div><button class='gv-switch' id='"+ROOT_ID+"-toggle'>"+(enabled?"TURN OFF":"ENABLE MANUALLY")+"</button></section>"+
"<div class='gv-section-title'>RENDERING PERFORMANCE <span>"+esc(s.samples)+" samples</span></div><section class='gv-metrics'>"+
metric("FRAME RATE",s.fps,"FPS","Average from sampled frames")+
metric("AVERAGE FRAME",s.avgFrameMs,"ms","Lower is smoother")+
metric("P95 FRAME TIME",s.p95FrameMs,"ms","Slowest 5% threshold")+
metric("MAX FRAME TIME",s.maxFrameMs,"ms","Largest sampled frame")+
"</section><section class='gv-latency'><div class='gv-latency-head'><strong>FRAME DELAYS</strong><span>Counts by threshold</span></div><div class='gv-delay-grid'>"+
"<div><b>"+esc(s.framesOver16_7)+"</b><span>Over 16.7 ms</span></div><div><b>"+esc(s.framesOver33)+"</b><span>Over 33 ms</span></div><div><b>"+esc(s.framesOver50)+"</b><span>Over 50 ms</span></div><div><b>"+esc(s.framesOver100)+"</b><span>Over 100 ms</span></div></div>"+
(s.samples?"":"<div class='gv-empty'>No frame samples yet. Enable diagnostics, run a galaxy-to-galaxy trip, then copy the report.</div>")+"</section>"+
"<div class='gv-section-title'>DEVICE & GRAPHICS</div><section class='gv-info-grid'>"+
"<div class='gv-info'><span>GPU RENDERER</span><strong>"+esc(w?.renderer||"Unavailable")+"</strong><small>"+esc(w?.version||"WebGL details unavailable")+"</small></div>"+
"<div class='gv-info'><span>JAVASCRIPT HEAP</span><strong>"+esc(m?Math.round(m.usedJSHeapSize/1048576)+" MB":"Unavailable")+"</strong><small>"+esc(m?"Heap limit "+Math.round(m.jsHeapSizeLimit/1048576)+" MB":"Browser memory API unavailable")+"</small></div>"+
"<div class='gv-info'><span>DEVICE</span><strong>"+esc(r.hardware.cores||"—")+" cores · "+esc(r.hardware.deviceMemory||"—")+" GB</strong><small>"+esc(r.viewport.width)+" × "+esc(r.viewport.height)+" · DPR "+esc(r.devicePixelRatio)+"</small></div>"+
"<div class='gv-info'><span>RESOURCES</span><strong>"+esc(r.resources.imagesComplete)+" / "+esc(r.resources.images)+" images loaded</strong><small>"+esc(r.resources.scripts)+" scripts · "+esc(r.resources.canvases)+" canvases · "+esc(r.resources.resourceEntries)+" requests</small></div>"+
"</section><div class='gv-section-title'>GALAXY VIEWER STATE</div><section class='gv-info-grid'>"+
"<div class='gv-info'><span>HD RESOURCES</span><strong>"+esc(a.urlCount??"—")+" tracked</strong><small>Window: "+esc(a.hdWindow??"—")+" · Current: "+esc(a.currentHd??"—")+"</small></div>"+
"<div class='gv-info'><span>TRAVEL DESTINATION</span><strong>"+esc(a.destination||"Not reported")+"</strong><small>HD overlay: "+esc(a.hdOverlay??"—")+" · Retired: "+esc(a.travelRetired??"—")+"</small></div>"+
"</section><footer class='gv-foot'><div><span>DIAGNOSTICS "+VERSION+"</span><span>Updated "+esc(r.timestamp)+"</span></div><div class='gv-actions'><button class='gv-copy' id='"+ROOT_ID+"-copy'>COPY FULL REPORT</button><button class='gv-close' id='"+ROOT_ID+"-close2'>CLOSE</button></div></footer></div>";
root.querySelector("#"+ROOT_ID+"-toggle").onclick=()=>setEnabled(!enabled);
root.querySelector("#"+ROOT_ID+"-copy").onclick=async()=>{const b=root?.querySelector("#"+ROOT_ID+"-copy");if(b){b.textContent="COPYING…";}await copyReport();const x=root?.querySelector("#"+ROOT_ID+"-copy");if(x){x.textContent="REPORT COPIED ✓";setTimeout(()=>{const y=root?.querySelector("#"+ROOT_ID+"-copy");if(y)y.textContent="COPY FULL REPORT"},1400)}};
root.querySelector("#"+ROOT_ID+"-close").onclick=()=>{root.remove();root=null};
root.querySelector("#"+ROOT_ID+"-close2").onclick=()=>{root.remove();root=null};
}
function open(){
if(!root){
const style=document.createElement("style");style.id=ROOT_ID+"-style";
style.textContent=".gv-dash{box-sizing:border-box;color:#eaf4ff;font:13px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;background:radial-gradient(ellipse at 85% 0%,rgba(28,89,150,.25),transparent 38%),#07111f;border:1px solid #29415e;border-radius:18px;overflow:hidden;box-shadow:0 18px 55px #000b;max-height:calc(100dvh - 120px);overflow-y:auto}.gv-dash *{box-sizing:border-box}.gv-head{display:flex;align-items:center;justify-content:space-between;padding:17px 16px 15px;background:linear-gradient(115deg,#0e2037,#101a2c);border-bottom:1px solid #233851}.gv-brand{display:flex;align-items:center;gap:12px;min-width:0}.gv-orbit{width:42px;height:42px;display:grid;place-items:center;border:1px solid #53b8ff;border-radius:14px;color:#a4e1ff;font-size:23px;background:linear-gradient(145deg,#173c63,#101d34);box-shadow:inset 0 0 18px #42b8ff22,0 0 18px #37aaff16}.gv-kicker{font-size:9px;font-weight:800;letter-spacing:1.6px;color:#77caff}.gv-head h2{font-size:19px;line-height:1.2;margin:3px 0 4px;color:#f4f9ff;font-weight:750}.gv-head p{margin:0;color:#8fa8c3;font-size:11px}.gv-x{align-self:flex-start;border:1px solid #314862;border-radius:10px;background:#14253a;color:#cfe3f8;font-size:23px;line-height:28px;width:34px;height:34px}.gv-state{display:flex;align-items:center;gap:10px;margin:13px 13px 18px;padding:12px;border:1px solid;border-radius:13px}.gv-off{background:#35141b;border-color:#853440}.gv-on{background:#0c3028;border-color:#23856a}.gv-led{width:10px;height:10px;flex:0 0 10px;border-radius:50%;background:#ff4f61;box-shadow:0 0 12px #ff4f6177}.gv-on .gv-led{background:#39f2a1;box-shadow:0 0 12px #39f2a177}.gv-state-copy{display:flex;flex:1;min-width:0;flex-direction:column;gap:2px}.gv-state-copy strong{font-size:11px;letter-spacing:.7px}.gv-off .gv-state-copy strong{color:#ff8994}.gv-on .gv-state-copy strong{color:#61f3b4}.gv-state-copy span{font-size:10px;color:#b5c5d6}.gv-switch,.gv-copy,.gv-close{border:1px solid #429ce1;border-radius:9px;background:#173f64;color:#eaf7ff;font-size:10px;font-weight:800;letter-spacing:.3px;padding:9px 10px;white-space:nowrap}.gv-off .gv-switch{background:#9d2636;border-color:#ff7380}.gv-on .gv-switch{background:#087a52;border-color:#4ce6ac}.gv-section-title{display:flex;justify-content:space-between;align-items:center;margin:18px 14px 9px;color:#7ecaff;font-size:9px;font-weight:850;letter-spacing:1.2px}.gv-section-title span{color:#7f96af;font-weight:600;letter-spacing:0;text-transform:none}.gv-metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:0 13px}.gv-metric{min-width:0;border:1px solid #253a52;border-radius:12px;padding:12px;background:linear-gradient(145deg,#12253a,#0d1929)}.gv-metric-label{font-size:9px;font-weight:800;letter-spacing:.9px;color:#8ca6c0}.gv-metric-value{font-size:26px;font-weight:800;line-height:1.3;letter-spacing:-.8px;color:#f4f9ff;margin-top:3px;overflow-wrap:anywhere}.gv-metric-value small{font-size:11px;letter-spacing:0;color:#7ecaff;margin-left:4px}.gv-metric-sub{font-size:10px;color:#8298b0;margin-top:3px}.gv-latency{margin:9px 13px 0;border:1px solid #253a52;border-radius:12px;padding:12px;background:#0c1929}.gv-latency-head{display:flex;justify-content:space-between;gap:8px;font-size:10px}.gv-latency-head strong{color:#e1efff;letter-spacing:.7px}.gv-latency-head span{color:#8298b0}.gv-delay-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px;margin-top:11px}.gv-delay-grid div{display:flex;flex-direction:column;gap:4px;min-width:0;padding:8px 4px;border-radius:8px;background:#14243a;text-align:center}.gv-delay-grid b{font-size:18px;color:#ffbd77}.gv-delay-grid span{font-size:9px;line-height:1.25;color:#9db0c5}.gv-empty{margin-top:10px;padding:9px;border-radius:8px;background:#182b40;color:#a9c0d8;font-size:11px}.gv-info-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:0 13px}.gv-info{min-width:0;padding:11px;border:1px solid #253a52;border-radius:11px;background:#0d1a2a}.gv-info>span{display:block;font-size:9px;font-weight:800;letter-spacing:.8px;color:#86a5c3}.gv-info strong{display:block;margin-top:5px;font-size:12px;color:#eaf4ff;overflow-wrap:anywhere}.gv-info small{display:block;margin-top:4px;color:#8198b2;font-size:10px;overflow-wrap:anywhere}.gv-foot{margin-top:18px;padding:12px 13px 14px;border-top:1px solid #233851;background:#0b1726;display:flex;flex-direction:column;gap:10px}.gv-foot>div:first-child{display:flex;justify-content:space-between;gap:8px;color:#7089a4;font-size:9px}.gv-actions{display:flex;gap:8px}.gv-copy{flex:1;background:#155c8e;border-color:#50baff}.gv-close{background:#17283b;border-color:#354b62}.gv-dash button{cursor:pointer}.gv-dash button:active{transform:translateY(1px)}@media(max-width:360px){.gv-state{flex-wrap:wrap}.gv-state-copy{flex-basis:calc(100% - 25px)}.gv-switch{margin-left:20px}.gv-head h2{font-size:17px}.gv-metric-value{font-size:23px}.gv-delay-grid span{font-size:8px}}";
document.head.appendChild(style);
root=document.createElement("div");root.id=ROOT_ID;root.style.cssText="position:fixed;left:7px;right:7px;top:100px;z-index:2147483646;max-width:620px;margin:0 auto";
document.body.appendChild(root)
}
renderPanel()
}
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
function mount(){enabled=false;stopCollection();updateStatusButton();attach();window.addEventListener("beforeunload",unmount,{once:true});console.log("GV CPU/GPU DIAGNOSTICS 0008 MOUNTED — OFF BY DEFAULT; MANUAL ACTIVATION ONLY; TARGET LONG-PRESS RESTORED")}
function unmount(){finishHold();stopCollection();if(button){button.removeEventListener("pointerdown",onDown,true);button.removeEventListener("pointerup",onUp,true);button.removeEventListener("pointercancel",onUp,true);button.removeEventListener("keydown",keyDown,true);button.removeEventListener("keyup",keyUp,true);button=null}root?.remove();root=null;statusButton?.remove();statusButton=null}
enabled=false;
const api={version:VERSION,mount,unmount,open,snapshot:report,copy:copyReport,setEnabled,get enabled(){return enabled}};
globalThis.GV_CPU_GPU_DIAGNOSTICS=api;window.GalaxyViewerDiagnostics=api;
})();