from __future__ import annotations

from google.colab import output
from IPython.display import HTML, Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

page = r'''
<div id="viewer1-root">
<style>
#viewer1-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#viewer1-root h3{color:#35c6ff;margin:12px 0 9px}
#viewer1-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#viewer1-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#viewer1-root input,#viewer1-root select{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#viewer1-root select option{background:#000;color:#7FDBFF}
#viewer1-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#viewer1-root .fetch-btn{background:#159447}
#viewer1-root .find-btn{background:#087fd1}
#viewer1-root .random-btn{background:#8a4fd4}
#viewer1-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
</style>
<h3>Galaxy Viewer — VIEWER-5</h3>
<div class="viewer-shell"><div id="viewer1-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>
<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>
<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">
<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>
</div>
<div class="controls">
<label for="viewer1SurveySelect">Displayed survey:</label>
<select id="viewer1SurveySelect" onchange="viewer1ChangeSurvey()"></select>
</div>
<div id="viewer1Status" class="status">Viewer loading…</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const VIEWER1_SURVEYS=[
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];
const VIEWER1_GALAXIES=[
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
const VIEWER1_KEY="galaxy-viewer-viewer1-state";
function viewer1State0(){return{ra:53.1625,dec:-27.791667,survey:"CDS/P/HST/EPO",fov:1}}
function viewer1Norm(id){return VIEWER1_SURVEYS.some(s=>s.id===id)?id:viewer1State0().survey}
function viewer1Load(){try{const p=JSON.parse(localStorage.getItem(VIEWER1_KEY)||"null")||{},d=viewer1State0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:viewer1Norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov}}catch(e){return viewer1State0()}}
function viewer1Capture(){const d=viewer1Load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.viewer1Aladin.getRaDec()}catch(e){}try{const z=+window.viewer1Aladin.getFov();if(z>0)fov=z}catch(e){}return{ra:+ra,dec:+dec,survey:viewer1Norm(document.getElementById("viewer1SurveySelect")?.value||d.survey),fov}}
function viewer1Save(o={}){const s={...viewer1State0(),...viewer1Capture(),...o};s.survey=viewer1Norm(s.survey);localStorage.setItem(VIEWER1_KEY,JSON.stringify(s));window.VIEWER1_STATE=s;return s}
function viewer1Survey(id){id=viewer1Norm(id);document.getElementById("viewer1SurveySelect").value=id;window.viewer1Aladin.setImageSurvey(id)}
function viewer1Restore(m=""){if(!window.viewer1Aladin)return;const s=viewer1Load();document.getElementById("viewer1CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;viewer1Survey(s.survey);window.viewer1Aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.viewer1Aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)viewer1Status(m)}
function viewer1Status(t){document.getElementById("viewer1Status").textContent=t}
function viewer1Setup(){document.getElementById("viewer1SurveySelect").innerHTML=VIEWER1_SURVEYS.map(s=>`<option value="${s.id}">${s.name}</option>`).join("")}
function viewer1PickRandom(){return VIEWER1_GALAXIES[Math.floor(Math.random()*VIEWER1_GALAXIES.length)]}
function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;window.viewer1Aladin.setImageSurvey("P/DSS2/color");window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:"P/DSS2/color",fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}
(async()=>{viewer1Setup();const g=viewer1PickRandom();document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;document.getElementById("viewer1SurveySelect").value="P/DSS2/color";await A.init;window.viewer1Aladin=A.aladin("#viewer1-aladin",{target:`${g.ra} ${g.dec}`,survey:"P/DSS2/color",fov:g.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});viewer1ShowGalaxy(g,"Launch galaxy")})().catch(e=>viewer1Status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>document.hidden?viewer1Save():viewer1Restore("Viewer restored from saved tab state."));
window.addEventListener("pagehide",()=>viewer1Save());
window.addEventListener("blur",()=>viewer1Save());
function viewer1RandomGalaxy(){viewer1ShowGalaxy(viewer1PickRandom())}
function viewer1FetchCoords(){const c=window.viewer1Aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("viewer1CoordBox").value=t;viewer1Save({ra:c[0],dec:c[1]});viewer1Status("Coordinates fetched: "+t)}
function viewer1ChangeSurvey(){const id=viewer1Norm(document.getElementById("viewer1SurveySelect").value);viewer1Survey(id);viewer1Save({survey:id});viewer1Status("Loaded survey: "+id)}
function viewer1Coords(t){const p=t.trim().split(/[\s,]+/).map(Number);if(p.length<2||!Number.isFinite(p[0])||!Number.isFinite(p[1]))throw Error("Enter decimal ICRS coordinates as RA Dec.");return{ra:p[0],dec:p[1]}}
function viewer1FindGalaxy(){try{const c=viewer1Coords(document.getElementById("viewer1CoordBox").value);window.VIEWER1_FIND_REQUEST={ra:c.ra,dec:c.dec,timestamp:Date.now()};viewer1Save({ra:c.ra,dec:c.dec});viewer1Status(`Find request ready for the next module: ${c.ra.toFixed(6)} ${c.dec.toFixed(6)}`)}catch(e){viewer1Status("Find request failed: "+e.message)}}
</script>
'''

display(HTML(page))
