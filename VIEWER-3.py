from __future__ import annotations

from google.colab import output
from IPython.display import HTML, Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

page = r'''
<div id="viewer3-root">
<style>
#viewer3-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#viewer3-root h3{color:#35c6ff;margin:12px 0 9px}
#viewer3-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#viewer3-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#viewer3-root input,#viewer3-root select{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#viewer3-root select option{background:#000;color:#7FDBFF}
#viewer3-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#viewer3-root .fetch-btn{background:#159447}
#viewer3-root .find-btn{background:#087fd1}
#viewer3-root .random-btn{background:#8a4fd4}
#viewer3-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
</style>
<h3>Galaxy Viewer — VIEWER-3</h3>
<div class="viewer-shell"><div id="viewer3-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button class="random-btn" onclick="viewer3RandomGalaxy()">Random Galaxy</button>
<button class="fetch-btn" onclick="viewer3FetchCoords()">Fetch Coordinates</button>
<input id="viewer3CoordBox" type="text" value="10.684708 41.268750" style="min-width:280px">
<button class="find-btn" onclick="viewer3FindGalaxy()">Find Galaxy / Star</button>
</div>
<div class="controls">
<label for="viewer3SurveySelect">Displayed survey:</label>
<select id="viewer3SurveySelect" onchange="viewer3ChangeSurvey()"></select>
</div>
<div id="viewer3Status" class="status">Viewer loading…</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const VIEWER3_SURVEYS=[
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"JWST First Images",id:"CDS/P/JWST/First-Images"},
{name:"JWST OPEN",id:"CDS/P/JWST/OPEN"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];

const VIEWER3_GALAXIES=[
{name:"Andromeda Galaxy (M31)",ra:10.684708,dec:41.268750,fov:3.6},
{name:"Triangulum Galaxy (M33)",ra:23.462083,dec:30.660194,fov:1.5},
{name:"Whirlpool Galaxy (M51)",ra:202.469575,dec:47.195258,fov:0.22},
{name:"Sombrero Galaxy (M104)",ra:189.997633,dec:-11.623054,fov:0.20},
{name:"Pinwheel Galaxy (M101)",ra:210.802267,dec:54.348950,fov:0.42},
{name:"Bode's Galaxy (M81)",ra:148.888221,dec:69.065295,fov:0.42},
{name:"Cigar Galaxy (M82)",ra:148.968458,dec:69.679703,fov:0.24},
{name:"Black Eye Galaxy (M64)",ra:194.182067,dec:21.682658,fov:0.18},
{name:"Sunflower Galaxy (M63)",ra:198.955542,dec:42.029289,fov:0.22},
{name:"Southern Pinwheel Galaxy (M83)",ra:204.253833,dec:-29.865417,fov:0.42},
{name:"Sculptor Galaxy (NGC 253)",ra:11.888000,dec:-25.288167,fov:0.55},
{name:"Centaurus A (NGC 5128)",ra:201.365063,dec:-43.019112,fov:0.48},
{name:"Cartwheel Galaxy",ra:9.421250,dec:-33.716111,fov:0.10},
{name:"Antennae Galaxies",ra:180.470833,dec:-18.867500,fov:0.15},
{name:"Hoag's Object",ra:229.179167,dec:21.585833,fov:0.055},
{name:"NGC 1300",ra:49.920833,dec:-19.411667,fov:0.16},
{name:"NGC 1365",ra:53.401667,dec:-36.140556,fov:0.22},
{name:"NGC 1566",ra:65.001667,dec:-54.937778,fov:0.20},
{name:"NGC 6744",ra:287.442083,dec:-63.857500,fov:0.34},
{name:"Fireworks Galaxy (NGC 6946)",ra:308.718333,dec:60.153889,fov:0.32},
{name:"Needle Galaxy (NGC 4565)",ra:189.086583,dec:25.987694,fov:0.34},
{name:"NGC 891",ra:35.639208,dec:42.349139,fov:0.28},
{name:"Whale Galaxy (NGC 4631)",ra:190.533375,dec:32.541472,fov:0.32},
{name:"Hamburger Galaxy (NGC 3628)",ra:170.070917,dec:13.589722,fov:0.26},
{name:"Phantom Galaxy (M74)",ra:24.174083,dec:15.783611,fov:0.24},
{name:"NGC 7331",ra:339.267083,dec:34.415556,fov:0.22},
{name:"Hidden Galaxy (IC 342)",ra:56.702083,dec:68.096111,fov:0.38},
{name:"Barnard's Galaxy (NGC 6822)",ra:296.240583,dec:-14.803333,fov:0.60},
{name:"NGC 300",ra:13.722833,dec:-37.684389,fov:0.52},
{name:"NGC 2403",ra:114.214167,dec:65.602500,fov:0.36}
];

const VIEWER3_KEY="galaxy-viewer-viewer3-state";
function viewer3State0(){return{ra:10.684708,dec:41.268750,survey:"P/DSS2/color",fov:1,name:"Andromeda Galaxy (M31)"}}
function viewer3Norm(id){return VIEWER3_SURVEYS.some(s=>s.id===id)?id:viewer3State0().survey}
function viewer3Load(){try{const p=JSON.parse(localStorage.getItem(VIEWER3_KEY)||"null")||{},d=viewer3State0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:viewer3Norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov,name:p.name||d.name}}catch(e){return viewer3State0()}}
function viewer3Capture(){const d=viewer3Load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.viewer3Aladin.getRaDec()}catch(e){}try{const z=window.viewer3Aladin.getFov(),q=Array.isArray(z)?+z[0]:+z;if(q>0)fov=q}catch(e){}return{ra:+ra,dec:+dec,survey:viewer3Norm(document.getElementById("viewer3SurveySelect")?.value||d.survey),fov,name:d.name}}
function viewer3Save(o={}){const s={...viewer3State0(),...viewer3Capture(),...o};s.survey=viewer3Norm(s.survey);localStorage.setItem(VIEWER3_KEY,JSON.stringify(s));window.VIEWER3_STATE=s;return s}
function viewer3Survey(id){id=viewer3Norm(id);document.getElementById("viewer3SurveySelect").value=id;window.viewer3Aladin.setImageSurvey(id)}
function viewer3Restore(m=""){if(!window.viewer3Aladin)return;const s=viewer3Load();document.getElementById("viewer3CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;viewer3Survey(s.survey);window.viewer3Aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.viewer3Aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)viewer3Status(m)}
function viewer3Status(t){document.getElementById("viewer3Status").textContent=t}
function viewer3Setup(){document.getElementById("viewer3SurveySelect").innerHTML=VIEWER3_SURVEYS.map(s=>`<option value="${s.id}">${s.name}</option>`).join("")}
function viewer3PickRandom(){return VIEWER3_GALAXIES[Math.floor(Math.random()*VIEWER3_GALAXIES.length)]}
function viewer3ShowGalaxy(g,message="Random galaxy loaded"){
 document.getElementById("viewer3CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;
 viewer3Survey("P/DSS2/color");
 window.viewer3Aladin.gotoRaDec(g.ra,g.dec);
 const applyFov=()=>{try{window.viewer3Aladin.setFoV(g.fov)}catch(e){}};
 applyFov();setTimeout(applyFov,180);setTimeout(applyFov,600);
 viewer3Save({ra:g.ra,dec:g.dec,fov:g.fov,name:g.name,survey:"P/DSS2/color"});
 viewer3Status(`${message}: ${g.name} | DSS2 Color | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`);
}
(async()=>{
 viewer3Setup();
 const launchGalaxy=viewer3PickRandom();
 document.getElementById("viewer3SurveySelect").value="P/DSS2/color";
 document.getElementById("viewer3CoordBox").value=`${launchGalaxy.ra.toFixed(6)} ${launchGalaxy.dec.toFixed(6)}`;
 await A.init;
 window.viewer3Aladin=A.aladin("#viewer3-aladin",{target:`${launchGalaxy.ra} ${launchGalaxy.dec}`,survey:"P/DSS2/color",fov:launchGalaxy.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});
 viewer3ShowGalaxy(launchGalaxy,"Launch galaxy");
})().catch(e=>viewer3Status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>document.hidden?viewer3Save():viewer3Restore("Viewer restored from saved tab state."));
window.addEventListener("pagehide",()=>viewer3Save());
window.addEventListener("blur",()=>viewer3Save());
function viewer3RandomGalaxy(){viewer3ShowGalaxy(viewer3PickRandom())}
function viewer3FetchCoords(){const c=window.viewer3Aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("viewer3CoordBox").value=t;viewer3Save({ra:c[0],dec:c[1],name:"Browsed position"});viewer3Status("Coordinates fetched: "+t)}
function viewer3ChangeSurvey(){const id=viewer3Norm(document.getElementById("viewer3SurveySelect").value);viewer3Survey(id);viewer3Save({survey:id});viewer3Status("Loaded survey: "+id)}
function viewer3Coords(t){const p=t.trim().split(/[\s,]+/).map(Number);if(p.length<2||!Number.isFinite(p[0])||!Number.isFinite(p[1]))throw Error("Enter decimal ICRS coordinates as RA Dec.");return{ra:p[0],dec:p[1]}}
function viewer3FindGalaxy(){try{const c=viewer3Coords(document.getElementById("viewer3CoordBox").value);window.VIEWER3_FIND_REQUEST={ra:c.ra,dec:c.dec,timestamp:Date.now()};viewer3Save({ra:c.ra,dec:c.dec,name:"Find request"});viewer3Status(`Find request ready for the next module: ${c.ra.toFixed(6)} ${c.dec.toFixed(6)}`)}catch(e){viewer3Status("Find request failed: "+e.message)}}
</script>
'''

display(HTML(page))
