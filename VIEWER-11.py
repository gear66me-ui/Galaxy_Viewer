from __future__ import annotations

import csv
import io
import json
import math
import random
import urllib.parse
import urllib.request
from collections import deque

from google.colab import output
from IPython.display import HTML, Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

_RECENT_PGC: deque[str] = deque(maxlen=50)


def _query_random_galaxy() -> dict:
    errors: list[str] = []

    for _ in range(20):
        ra0 = random.uniform(0.0, 360.0)
        dec0 = math.degrees(math.asin(random.uniform(-1.0, 1.0)))

        query = urllib.parse.urlencode(
            {
                "-source": "VII/237/pgc",
                "-c": f"{ra0:.8f} {dec0:.8f}",
                "-c.rm": "90",
                "-out": "PGC,RAJ2000,DEJ2000,logD25",
                "-out.max": "200",
            }
        )
        url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?" + query

        try:
            with urllib.request.urlopen(url, timeout=35) as response:
                text = response.read().decode("utf-8", errors="replace")
        except Exception as exc:
            errors.append(str(exc))
            continue

        lines = [line for line in text.splitlines() if line and not line.startswith("#")]
        if len(lines) < 2:
            continue

        try:
            rows = list(csv.DictReader(io.StringIO("\n".join(lines)), delimiter="\t"))
        except Exception as exc:
            errors.append(str(exc))
            continue

        candidates: list[dict] = []
        for row in rows:
            pgc = str(row.get("PGC", "")).strip()
            if not pgc or pgc in _RECENT_PGC:
                continue

            try:
                from astropy.coordinates import SkyCoord
                import astropy.units as u

                coord = SkyCoord(
                    f'{row["RAJ2000"]} {row["DEJ2000"]}',
                    unit=(u.hourangle, u.deg),
                    frame="icrs",
                )
                ra = float(coord.ra.deg)
                dec = float(coord.dec.deg)
            except Exception:
                continue

            fov = 0.18
            try:
                log_d25 = float(row.get("logD25", ""))
                diameter_arcmin = 0.1 * (10.0 ** log_d25)
                if diameter_arcmin > 0:
                    fov = max(0.035, min(2.5, diameter_arcmin / 60.0 * 3.2))
            except Exception:
                pass

            candidates.append(
                {
                    "ok": True,
                    "name": f"PGC {pgc}",
                    "ra": ra,
                    "dec": dec,
                    "fov": fov,
                    "survey_id": "P/DSS2/color",
                    "source": "HyperLEDA via VizieR random-sky cone",
                }
            )

        if candidates:
            chosen = random.choice(candidates)
            _RECENT_PGC.append(chosen["name"].replace("PGC ", "", 1))
            return chosen

    raise RuntimeError(
        "No non-repeating HyperLEDA galaxy was returned after 20 random-sky searches. "
        + " | ".join(errors[-3:])
    )


def viewer11_random_callback() -> str:
    try:
        result = _query_random_galaxy()
    except Exception as exc:
        result = {"ok": False, "error": str(exc)}
    return json.dumps(result, ensure_ascii=False)


output.register_callback("viewer11.randomGalaxy", viewer11_random_callback)

page = r'''
<div id="viewer11-root">
<style>
#viewer11-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#viewer11-root h3{color:#35c6ff;margin:12px 0 9px}
#viewer11-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#viewer11-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#viewer11-root input{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#viewer11-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#viewer11-root button:disabled{opacity:.55;cursor:wait}
#viewer11-root .fetch-btn{background:#159447}
#viewer11-root .random-btn{background:#8a4fd4}
#viewer11-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
#viewer11-root .survey-menu-wrap{position:relative;display:inline-block;min-width:290px}
#viewer11-root .survey-menu-button{width:100%;text-align:left;background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;font-weight:400}
#viewer11-root .survey-menu{display:none;position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:999999;background:#000;border:1px solid #169ac7;border-radius:8px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.75)}
#viewer11-root .survey-menu.open{display:block}
#viewer11-root .survey-option{display:block;width:100%;text-align:left;background:#000;color:#7FDBFF;border:0;border-bottom:1px solid #0b526f;border-radius:0;padding:12px;font-size:16px;font-weight:400}
#viewer11-root .survey-option:last-child{border-bottom:0}
#viewer11-root .survey-option:active{background:#063047}
</style>
<h3>Galaxy Viewer — VIEWER-11</h3>
<div class="viewer-shell"><div id="viewer11-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button id="viewer11RandomButton" class="random-btn" onclick="viewer11RandomGalaxy()">Random Galaxy</button>
<button class="fetch-btn" onclick="viewer11FetchCoords()">Fetch Coordinates</button>
<input id="viewer11CoordBox" type="text" value="53.162500 -27.791667" readonly style="min-width:280px">
</div>
<div class="controls">
<label>Displayed survey:</label>
<div class="survey-menu-wrap">
<input type="hidden" id="viewer11SurveySelect">
<button type="button" id="viewer11SurveyButton" class="survey-menu-button" onclick="viewer11ToggleSurveyMenu(event)">DSS2 Color ▾</button>
<div id="viewer11SurveyMenu" class="survey-menu"></div>
</div>
</div>
<div id="viewer11Status" class="status">Viewer loading…</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const VIEWER11_SURVEYS=[
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"JWST Outreach Color",id:"CDS/P/JWST/EPO"},
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];
const VIEWER11_KEY="galaxy-viewer-viewer11-state";
function viewer11State0(){return{ra:53.1625,dec:-27.791667,survey:"P/DSS2/color",fov:1}}
function viewer11Norm(id){return VIEWER11_SURVEYS.some(s=>s.id===id)?id:viewer11State0().survey}
function viewer11Load(){try{const p=JSON.parse(localStorage.getItem(VIEWER11_KEY)||"null")||{},d=viewer11State0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:viewer11Norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov}}catch(e){return viewer11State0()}}
function viewer11Capture(){const d=viewer11Load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.viewer11Aladin.getRaDec()}catch(e){}try{const z=+window.viewer11Aladin.getFov();if(z>0)fov=z}catch(e){}return{ra:+ra,dec:+dec,survey:viewer11Norm(document.getElementById("viewer11SurveySelect")?.value||d.survey),fov}}
function viewer11Save(o={}){const s={...viewer11State0(),...viewer11Capture(),...o};s.survey=viewer11Norm(s.survey);localStorage.setItem(VIEWER11_KEY,JSON.stringify(s));window.VIEWER11_STATE=s;return s}
function viewer11Status(t){document.getElementById("viewer11Status").textContent=t}
function viewer11Setup(){document.getElementById("viewer11SurveyMenu").innerHTML=VIEWER11_SURVEYS.map(s=>`<button type="button" class="survey-option" onclick="viewer11ChooseSurvey('${s.id}',event)">${s.name}</button>`).join("")}
function viewer11Survey(id){id=viewer11Norm(id);document.getElementById("viewer11SurveySelect").value=id;const item=VIEWER11_SURVEYS.find(s=>s.id===id);document.getElementById("viewer11SurveyButton").textContent=(item?item.name:id)+" ▾";window.viewer11Aladin.setImageSurvey(id)}
function viewer11ToggleSurveyMenu(e){e.stopPropagation();document.getElementById("viewer11SurveyMenu").classList.toggle("open")}
function viewer11ChooseSurvey(id,e){e.stopPropagation();viewer11Survey(id);viewer11Save({survey:id});document.getElementById("viewer11SurveyMenu").classList.remove("open");viewer11Status("Loaded survey: "+id)}
document.addEventListener("click",()=>{const m=document.getElementById("viewer11SurveyMenu");if(m)m.classList.remove("open")})
function viewer11Parse(v){if(v==null)return v;if(typeof v!=="string")return v;v=v.trim();if(v.startsWith("'")&&v.endsWith("'"))v=v.slice(1,-1).replace(/\\'/g,"'").replace(/\\\\/g,"\\");try{return JSON.parse(v)}catch(_){return v}}
function viewer11Result(r){const d=r?.data??r;if(d&&typeof d==="object"&&d.ok!==undefined)return d;if(d&&typeof d==="object")return viewer11Parse(d["application/json"]??d["text/plain"]??Object.values(d)[0]);return viewer11Parse(d)}
function viewer11ShowGalaxy(g,message="Random galaxy loaded"){const ra=Number(g.ra),dec=Number(g.dec),fov=Number(g.fov),survey=viewer11Norm(g.survey_id||"P/DSS2/color");document.getElementById("viewer11CoordBox").value=`${ra.toFixed(6)} ${dec.toFixed(6)}`;viewer11Survey(survey);window.viewer11Aladin.gotoRaDec(ra,dec);const z=()=>{try{window.viewer11Aladin.setFoV(fov)}catch(e){}};z();setTimeout(z,150);setTimeout(z,500);viewer11Save({ra,dec,survey,fov});viewer11Status(`${message}: ${g.name} | ICRS ${ra.toFixed(6)} ${dec.toFixed(6)} | FOV ${fov.toFixed(3)}° | ${g.source}`)}
async function viewer11RandomGalaxy(message="Random galaxy loaded"){const b=document.getElementById("viewer11RandomButton");b.disabled=true;viewer11Status("Searching random sky regions in HyperLEDA/VizieR…");try{const r=await google.colab.kernel.invokeFunction("viewer11.randomGalaxy",[],{});const g=viewer11Result(r);if(!g||g.ok!==true)throw Error(g?.error||"Lookup failed");viewer11ShowGalaxy(g,message)}catch(e){viewer11Status("Random galaxy failed: "+String(e?.message||e))}finally{b.disabled=false}}
function viewer11FetchCoords(){const c=window.viewer11Aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("viewer11CoordBox").value=t;viewer11Save({ra:c[0],dec:c[1]});viewer11Status("Coordinates fetched: "+t)}
function viewer11Restore(m=""){if(!window.viewer11Aladin)return;const s=viewer11Load();document.getElementById("viewer11CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;viewer11Survey(s.survey);window.viewer11Aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.viewer11Aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)viewer11Status(m)}
(async()=>{viewer11Setup();const s=viewer11Load();document.getElementById("viewer11CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("viewer11SurveySelect").value=s.survey;await A.init;window.viewer11Aladin=A.aladin("#viewer11-aladin",{target:`${s.ra} ${s.dec}`,survey:s.survey,fov:s.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});await viewer11RandomGalaxy("Launch random galaxy")})().catch(e=>viewer11Status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>document.hidden?viewer11Save():viewer11Restore("Viewer restored from saved tab state."));
window.addEventListener("pagehide",()=>viewer11Save());
window.addEventListener("blur",()=>viewer11Save());
</script>
'''

display(HTML(page))
