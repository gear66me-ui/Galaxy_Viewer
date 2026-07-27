from IPython.display import HTML, display

# GV-beta-0004B
# Standalone startup diagnostic for the GV-beta-0004A loading path.
# Tests the same local Aladin module URL and reports each startup stage visibly.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML(r'''
<div id="gv-0004b-diagnostic" style="background:#05080d;color:#d9f7ff;border:1px solid #45E7FF;border-radius:8px;padding:12px;font-family:Roboto Mono,Consolas,monospace;font-size:13px;line-height:1.45;white-space:pre-wrap;max-height:260px;overflow:auto;margin-bottom:8px">GV-beta-0004B Python started</div>
<div id="aladin-cosmic-command-test" style="width:100%;height:650px;position:relative"></div>
<script type="module">
const panel=document.getElementById("gv-0004b-diagnostic");
const started=performance.now();
const stamp=()=>`${((performance.now()-started)/1000).toFixed(3)} s`;
const log=(message,error=false)=>{
  const line=document.createElement("div");
  line.textContent=`[${stamp()}] ${message}`;
  if(error) line.style.color="#FF7C91";
  panel.appendChild(line);
  panel.scrollTop=panel.scrollHeight;
  console[error?"error":"log"]("GV-beta-0004B",message);
};
window.addEventListener("error",event=>log(`WINDOW ERROR: ${event.message} at ${event.filename||"unknown"}:${event.lineno||0}:${event.colno||0}`,true));
window.addEventListener("unhandledrejection",event=>log(`PROMISE ERROR: ${event.reason?.stack||event.reason||"unknown rejection"}`,true));

log("HTML injected");
log("Local Aladin module import requested");

try {
  const moduleUrl="https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/dist/aladin.js";
  const A=await import(moduleUrl);
  log("Local Aladin module imported");
  log(`Export check: init=${typeof A.init}, aladin=${typeof A.aladin}`);

  log("A.init waiting");
  await A.init;
  log("A.init completed");

  log("Viewer creation started");
  const viewer=A.aladin("#aladin-cosmic-command-test",{
    target:"M 31",
    survey:"P/DSS2/color",
    fov:1.5,
    cooFrame:"ICRSd",
    projection:"TAN",
    reticleColor:"#62D8FF",
    reticleSize:22,
    showReticle:true,
    showZoomControl:true,
    showFullscreenControl:true,
    showLayersControl:true,
    showGotoControl:true,
    showCooGridControl:true,
    showSimbadPointerControl:true,
    showProjectionControl:true
  });
  window.aladin_cosmic_command_test=viewer;
  log("Viewer object created");

  const inspect=label=>{
    const root=document.getElementById("aladin-cosmic-command-test");
    const canvasCount=root.querySelectorAll("canvas").length;
    const imageCount=root.querySelectorAll("img").length;
    const childCount=root.children.length;
    const rect=root.getBoundingClientRect();
    log(`${label}: children=${childCount}, canvases=${canvasCount}, images=${imageCount}, size=${Math.round(rect.width)}x${Math.round(rect.height)}`);
  };

  [250,1000,3000,10000,30000,60000].forEach(delay=>setTimeout(()=>inspect(`DOM check after ${delay} ms`),delay));
  log("Survey loading observation started");
} catch(error) {
  log(`STARTUP FAILURE: ${error?.stack||error}`,true);
}
</script>
'''))

print("GV-beta-0004B diagnostic HTML injected")
