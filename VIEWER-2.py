from __future__ import annotations

from google.colab import output
from IPython.display import HTML, Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

page = r'''
<div id="viewer2-root">
<style>
#viewer2-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#viewer2-root h3{color:#35c6ff;margin:12px 0 9px}
#viewer2-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#viewer2-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#viewer2-root input,#viewer2-root select{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#viewer2-root select option{background:#000;color:#7FDBFF}
#viewer2-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#viewer2-root .fetch-btn{background:#159447}
#viewer2-root .find-btn{background:#087fd1}
#viewer2-root .random-btn{background:#8a4fd4}
#viewer2-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
</style>
<h3>Galaxy Viewer — VIEWER-2</h3>
<div class="viewer-shell"><div id="viewer2-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button class="random-btn" onclick="viewer2RandomGalaxy()">Random Galaxy</button>
<button class="fetch-btn" onclick="viewer2FetchCoords()">Fetch Coordinates</button>
<input id="viewer2CoordBox" type="text" value="10.684708 41.268750" style="min-width:280px">
<button class="find-btn" onclick="viewer2FindGalaxy()">Find Galaxy / Star</button>
</div>
<div class="controls">
<label for="viewer2SurveySelect">Displayed survey:</label>
<select id="viewer2SurveySelect" onchange="viewer2ChangeSurvey()"></select>
</div>
<div id="viewer2Status" class="status">Viewer loading…</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const VIEWER2_SURVEYS=[
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"JWST First Images",id:"CDS/P/JWST/First-Images"},
{name:"JWST OPEN",id:"CDS/P/JWST/OPEN"},
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"},
{name:"AllWISE Color",id:"P/allWISE/color"}
];

const VIEWER2_GALAXIES=[
{name:"Andromeda Galaxy (M31)",ra:10.684708,dec:41.268750,fov:3.2},
{name:"Triangulum Galaxy (M33)",ra:23.462083,dec:30.660194,fov:1.8},
{name:"Whirlpool Galaxy (M51)",ra:202.469575,dec:47.195258,fov:0.35},
{name:"Sombrero Galaxy (M104)",ra:189.997633,dec:-11.623054,fov:0.28},
{name:"Pinwheel Galaxy (M101)",ra:210.802267,dec:54.348950,fov:0.55},
{name:"Bode's Galaxy (M81)",ra:148.888221,dec:69.065295,fov:0.55},
{name:"Cigar Galaxy (M82)",ra:148.968458,dec:69.679703,fov:0.35},
{name:"Black Eye Galaxy (M64)",ra:194.182067,dec:21.682658,fov:0.28},
{name:"Sunflower Galaxy (M63)",ra:198.955542,dec:42.029289,fov:0.30},
{name:"Southern Pinwheel Galaxy (M83)",ra:204.253833,dec:-29.865417,fov:0.55},
{name:"Sculptor Galaxy (NGC 253)",ra:11.888000,dec:-25.288167,fov:0.65},
{name:"Centaurus A (NGC 5128)",ra:201.365063,dec:-43.019112,fov:0.60},
{name:"Cartwheel Galaxy",ra:9.421250,dec:-33.716111,fov:0.12},
{name:"Antennae Galaxies",ra:180.470833,dec:-18.867500,fov:0.20},
{name:"Tadpole Galaxy",ra:241.760417,dec:55.424722,fov:0.10},
{name:"Hoag's Object",ra:229.179167,dec:21.585833,fov:0.08},
{name:"NGC 1300",ra:49.920833,dec:-19.411667,fov:0.22},
{name:"NGC 1365",ra:53.401667,dec:-36.140556,fov:0.28},
{name:"NGC 1672",ra:71.427083,dec:-59.247778,fov:0.22},
{name:"NGC 1566",ra:65.001667,dec:-54.937778,fov:0.28},
{name:"NGC 6744",ra:287.442083,dec:-63.857500,fov:0.45},
{name:"NGC 6946 Fireworks Galaxy",ra:308.718333,dec:60.153889,fov:0.42},
{name:"NGC 4565 Needle Galaxy",ra:189.086583,dec:25.987694,fov:0.45},
{name:"NGC 891",ra:35.639208,dec:42.349139,fov:0.38},
{name:"NGC 4631 Whale Galaxy",ra:190.533375,dec:32.541472,fov:0.42},
{name:"NGC 4656 Hockey Stick Galaxy",ra:190.990833,dec:32.168056,fov:0.35},
{name:"NGC 3628 Hamburger Galaxy",ra:170.070917,dec:13.589722,fov:0.35},
{name:"Leo Triplet",ra:170.066667,dec:13.000000,fov:1.0},
{name:"Markarian's Chain",ra:187.705833,dec:12.391111,fov:1.4},
{name:"Virgo Galaxy M87",ra:187.705930,dec:12.391123,fov:0.30},
{name:"M49",ra:187.444992,dec:8.000412,fov:0.30},
{name:"M60",ra:190.916700,dec:11.552700,fov:0.28},
{name:"M84",ra:186.265597,dec:12.886983,fov:0.25},
{name:"M86",ra:186.549225,dec:12.946160,fov:0.25},
{name:"M87",ra:187.705930,dec:12.391123,fov:0.25},
{name:"M89",ra:188.915863,dec:12.556342,fov:0.22},
{name:"M90",ra:189.207608,dec:13.162900,fov:0.30},
{name:"M94",ra:192.721100,dec:41.120153,fov:0.30},
{name:"M95",ra:160.990542,dec:11.703667,fov:0.25},
{name:"M96",ra:161.690583,dec:11.819944,fov:0.28},
{name:"M105",ra:161.956667,dec:12.581667,fov:0.22},
{name:"M108",ra:167.879042,dec:55.674111,fov:0.30},
{name:"M109",ra:179.399933,dec:53.374519,fov:0.28},
{name:"Stephan's Quintet",ra:338.990833,dec:33.960833,fov:0.16},
{name:"NGC 7319",ra:339.014167,dec:33.975278,fov:0.08},
{name:"NGC 7331",ra:339.267083,dec:34.415556,fov:0.30},
{name:"NGC 2775",ra:137.583333,dec:7.037778,fov:0.24},
{name:"NGC 2841",ra:140.510417,dec:50.976389,fov:0.30},
{name:"NGC 2903",ra:143.042125,dec:21.500833,fov:0.30},
{name:"NGC 3190",ra:154.523125,dec:21.832778,fov:0.22},
{name:"NGC 3344",ra:160.879167,dec:24.922222,fov:0.30},
{name:"NGC 3521",ra:166.452500,dec:-0.035833,fov:0.32},
{name:"NGC 4038",ra:180.470833,dec:-18.867500,fov:0.16},
{name:"NGC 4258 (M106)",ra:184.739583,dec:47.303889,fov:0.38},
{name:"NGC 4302",ra:185.426250,dec:14.598889,fov:0.24},
{name:"NGC 4414",ra:186.612917,dec:31.223889,fov:0.24},
{name:"NGC 4449",ra:187.046250,dec:44.093611,fov:0.28},
{name:"NGC 4490 Cocoon Galaxy",ra:187.651667,dec:41.643889,fov:0.28},
{name:"NGC 4725",ra:192.610000,dec:25.500000,fov:0.34},
{name:"NGC 4826",ra:194.182067,dec:21.682658,fov:0.26},
{name:"NGC 5033",ra:198.364583,dec:36.593611,fov:0.30},
{name:"NGC 5055",ra:198.955542,dec:42.029289,fov:0.32},
{name:"NGC 5194",ra:202.469575,dec:47.195258,fov:0.25},
{name:"NGC 5457",ra:210.802267,dec:54.348950,fov:0.45},
{name:"NGC 5866 Spindle Galaxy",ra:226.623333,dec:55.763333,fov:0.22},
{name:"NGC 5907 Splinter Galaxy",ra:228.974167,dec:56.328889,fov:0.32},
{name:"NGC 660",ra:25.759167,dec:13.645833,fov:0.22},
{name:"NGC 772",ra:29.533333,dec:19.007778,fov:0.25},
{name:"NGC 1097",ra:41.579167,dec:-30.274722,fov:0.32},
{name:"NGC 1232",ra:47.438333,dec:-20.579722,fov:0.28},
{name:"NGC 1512",ra:60.975000,dec:-43.348889,fov:0.30},
{name:"NGC 2207 and IC 2163",ra:94.091667,dec:-21.372222,fov:0.24},
{name:"NGC 2442 Meathook Galaxy",ra:114.096250,dec:-69.530833,fov:0.28},
{name:"NGC 300",ra:13.722833,dec:-37.684389,fov:0.65},
{name:"Large Magellanic Cloud",ra:80.894167,dec:-69.756111,fov:7.0},
{name:"Small Magellanic Cloud",ra:13.186667,dec:-72.828611,fov:4.5},
{name:"Barnard's Galaxy (NGC 6822)",ra:296.240583,dec:-14.803333,fov:0.75},
{name:"IC 342 Hidden Galaxy",ra:56.702083,dec:68.096111,fov:0.48},
{name:"Maffei 1",ra:39.147083,dec:59.654722,fov:0.30},
{name:"Maffei 2",ra:40.479167,dec:59.604167,fov:0.30},
{name:"Sextans A",ra:152.753333,dec:-4.692778,fov:0.38},
{name:"Sextans B",ra:150.000000,dec:5.332222,fov:0.35},
{name:"WLM Galaxy",ra:0.492083,dec:-15.460833,fov:0.45},
{name:"NGC 55",ra:3.723333,dec:-39.196667,fov:0.60},
{name:"NGC 247",ra:11.785000,dec:-20.760278,fov:0.50},
{name:"NGC 2403",ra:114.214167,dec:65.602500,fov:0.48},
{name:"NGC 4214",ra:183.913333,dec:36.326944,fov:0.30},
{name:"NGC 5253",ra:204.982083,dec:-31.640000,fov:0.24},
{name:"NGC 1316 Fornax A",ra:50.673333,dec:-37.208333,fov:0.38},
{name:"NGC 1399",ra:54.621250,dec:-35.450556,fov:0.24},
{name:"NGC 1404",ra:54.716250,dec:-35.594444,fov:0.22},
{name:"NGC 4261",ra:184.846250,dec:5.825000,fov:0.22},
{name:"NGC 1275 Perseus A",ra:49.950667,dec:41.511696,fov:0.22},
{name:"Cygnus A",ra:299.868153,dec:40.733916,fov:0.18},
{name:"Hercules A",ra:252.784167,dec:4.992500,fov:0.18},
{name:"3C 273 Host Galaxy",ra:187.277917,dec:2.052389,fov:0.10},
{name:"Einstein Cross Host Galaxy",ra:340.126250,dec:3.358611,fov:0.08},
{name:"MACS J1149.5+2223",ra:177.398750,dec:22.398611,fov:0.20},
{name:"Abell 2744 Pandora's Cluster",ra:3.588333,dec:-30.400278,fov:0.28},
{name:"El Gordo Cluster",ra:15.724167,dec:-49.255833,fov:0.24},
{name:"Cosmic Cliffs NGC 3324",ra:159.150000,dec:-58.620000,fov:0.25},
{name:"Phantom Galaxy M74",ra:24.174083,dec:15.783611,fov:0.34},
{name:"Southern Ring Nebula NGC 3132",ra:151.756250,dec:-40.436389,fov:0.12}
];

const VIEWER2_KEY="galaxy-viewer-viewer2-state";
function viewer2State0(){return{ra:10.684708,dec:41.268750,survey:"CDS/P/HST/EPO",fov:1,name:"Andromeda Galaxy (M31)"}}
function viewer2Norm(id){return VIEWER2_SURVEYS.some(s=>s.id===id)?id:viewer2State0().survey}
function viewer2Load(){try{const p=JSON.parse(localStorage.getItem(VIEWER2_KEY)||"null")||{},d=viewer2State0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:viewer2Norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov,name:p.name||d.name}}catch(e){return viewer2State0()}}
function viewer2Capture(){const d=viewer2Load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.viewer2Aladin.getRaDec()}catch(e){}try{const z=window.viewer2Aladin.getFov(),q=Array.isArray(z)?+z[0]:+z;if(q>0)fov=q}catch(e){}return{ra:+ra,dec:+dec,survey:viewer2Norm(document.getElementById("viewer2SurveySelect")?.value||d.survey),fov,name:d.name}}
function viewer2Save(o={}){const s={...viewer2State0(),...viewer2Capture(),...o};s.survey=viewer2Norm(s.survey);localStorage.setItem(VIEWER2_KEY,JSON.stringify(s));window.VIEWER2_STATE=s;return s}
function viewer2Survey(id){id=viewer2Norm(id);document.getElementById("viewer2SurveySelect").value=id;window.viewer2Aladin.setImageSurvey(id)}
function viewer2Status(t){document.getElementById("viewer2Status").textContent=t}
function viewer2Setup(){document.getElementById("viewer2SurveySelect").innerHTML=VIEWER2_SURVEYS.map(s=>`<option value="${s.id}">${s.name}</option>`).join("")}
function viewer2PickRandom(){return VIEWER2_GALAXIES[Math.floor(Math.random()*VIEWER2_GALAXIES.length)]}
function viewer2ShowGalaxy(g,message="Random galaxy loaded"){
 document.getElementById("viewer2CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;
 window.viewer2Aladin.gotoRaDec(g.ra,g.dec);
 const applyFov=()=>{try{window.viewer2Aladin.setFoV(g.fov)}catch(e){}};
 applyFov();setTimeout(applyFov,150);setTimeout(applyFov,500);
 viewer2Save({ra:g.ra,dec:g.dec,fov:g.fov,name:g.name});
 viewer2Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`);
}
(async()=>{
 viewer2Setup();
 const previous=viewer2Load();
 document.getElementById("viewer2SurveySelect").value=previous.survey;
 const launchGalaxy=viewer2PickRandom();
 document.getElementById("viewer2CoordBox").value=`${launchGalaxy.ra.toFixed(6)} ${launchGalaxy.dec.toFixed(6)}`;
 await A.init;
 window.viewer2Aladin=A.aladin("#viewer2-aladin",{target:`${launchGalaxy.ra} ${launchGalaxy.dec}`,survey:previous.survey,fov:launchGalaxy.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});
 viewer2ShowGalaxy(launchGalaxy,"Launch galaxy");
})().catch(e=>viewer2Status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>{if(document.hidden)viewer2Save()});
window.addEventListener("pagehide",()=>viewer2Save());
window.addEventListener("blur",()=>viewer2Save());
function viewer2RandomGalaxy(){viewer2ShowGalaxy(viewer2PickRandom())}
function viewer2FetchCoords(){const c=window.viewer2Aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("viewer2CoordBox").value=t;viewer2Save({ra:c[0],dec:c[1],name:"Browsed position"});viewer2Status("Coordinates fetched: "+t)}
function viewer2ChangeSurvey(){const id=viewer2Norm(document.getElementById("viewer2SurveySelect").value);viewer2Survey(id);viewer2Save({survey:id});viewer2Status("Loaded survey: "+id)}
function viewer2Coords(t){const p=t.trim().split(/[\s,]+/).map(Number);if(p.length<2||!Number.isFinite(p[0])||!Number.isFinite(p[1]))throw Error("Enter decimal ICRS coordinates as RA Dec.");return{ra:p[0],dec:p[1]}}
function viewer2FindGalaxy(){try{const c=viewer2Coords(document.getElementById("viewer2CoordBox").value);window.VIEWER2_FIND_REQUEST={ra:c.ra,dec:c.dec,timestamp:Date.now()};viewer2Save({ra:c.ra,dec:c.dec,name:"Find request"});viewer2Status(`Find request ready for the next module: ${c.ra.toFixed(6)} ${c.dec.toFixed(6)}`)}catch(e){viewer2Status("Find request failed: "+e.message)}}
</script>
'''

display(HTML(page))
