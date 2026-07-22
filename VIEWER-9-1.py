from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from google.colab import output as colab_output
from IPython.display import HTML, Javascript, display

try:
    from google.colab import userdata
except Exception:
    userdata = None


def _secret(name: str, default: str = "") -> str:
    if userdata is not None:
        try:
            value = userdata.get(name)
            if value:
                return str(value)
        except Exception:
            pass
    return os.environ.get(name, default)


def _response_text(payload: dict) -> str:
    for item in payload.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    return part.get("text", "")
    return payload.get("output_text", "")


def _openai_json(prompt: str, schema_name: str, schema: dict) -> dict:
    api_key = _secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from Colab Secrets.")

    body = {
        "model": _secret("OPENAI_MODEL", "gpt-5"),
        "store": False,
        "tools": [{"type": "web_search"}],
        "input": prompt,
        "text": {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "strict": True,
                "schema": schema,
            }
        },
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {detail[:1000]}") from exc

    text = _response_text(payload)
    if not text:
        raise RuntimeError("OpenAI returned no structured output.")
    return json.loads(text)


RANDOM_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "ra": {"type": "number"},
        "dec": {"type": "number"},
        "fov": {"type": "number"},
        "survey_id": {"type": "string"},
    },
    "required": ["name", "ra", "dec", "fov", "survey_id"],
}

INFO_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "rows": {
            "type": "array",
            "minItems": 10,
            "maxItems": 10,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "parameter": {"type": "string"},
                    "value": {"type": "string"},
                    "notes": {"type": "string"},
                    "source": {"type": "string"},
                },
                "required": ["parameter", "value", "notes", "source"],
            },
        },
    },
    "required": ["title", "summary", "rows"],
}


def viewer9_random_ai():
    return _openai_json(
        """
Choose one real, visually interesting galaxy. Verify its ICRS decimal coordinates with web search.
Return an Aladin Lite field of view in degrees that frames the complete visible galaxy comfortably.
Choose exactly one survey_id from:
CDS/P/HST/EPO
P/DSS2/color
P/DSS2/red
P/PanSTARRS/DR1/color-z-zg-g
P/DECaLS/DR5/color
P/2MASS/color
P/GALEXGR6/AIS/color
Prefer DSS2 Color when uncertain. Return only the requested JSON.
""",
        "random_galaxy",
        RANDOM_SCHEMA,
    )


def viewer9_get_info(name: str, ra: float, dec: float):
    return _openai_json(
        f"""
Research the galaxy currently displayed.
Name: {name}
ICRS coordinates: RA {float(ra):.8f} deg, Dec {float(dec):.8f} deg.
Use SIMBAD-first identification and NED plus authoritative astronomy sources to supplement missing values.
Return exactly ten rows in this exact order:
1. Common designations
2. Constellation
3. Morphological type
4. ICRS coordinates
5. Distance
6. Diameter / physical size
7. Redshift and radial velocity
8. Apparent magnitude
9. Stellar mass or estimated star count
10. Estimated stellar age
Use Not available when unsupported. Return only the requested JSON.
""",
        "galaxy_information",
        INFO_SCHEMA,
    )


colab_output.register_callback("viewer9.randomGalaxyAI", viewer9_random_ai)
colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_get_info)

colab_output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

page = r'''
<div id="gv91-root">
<style>
#gv91-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#gv91-root h3{color:#35c6ff;margin:8px 0 10px}
#gv91-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#gv91-root .controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:12px}
#gv91-root button{padding:13px 20px;font-size:16px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#gv91-root button:disabled{opacity:.55;cursor:wait}
#gv91-root .random-btn{background:#8a4fd4}
#gv91-root .info-btn{background:#c87916}
#gv91-root input{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#gv91-root .galaxy-name{min-width:300px;flex:1}
#gv91-root .survey-menu-wrap{position:relative;display:inline-block;min-width:290px}
#gv91-root .survey-menu-button{width:100%;text-align:left;background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;font-weight:400}
#gv91-root .survey-menu{display:none;position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:999999;background:#000;border:1px solid #169ac7;border-radius:8px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.75)}
#gv91-root .survey-menu.open{display:block}
#gv91-root .survey-option{display:block;width:100%;text-align:left;background:#000;color:#7FDBFF;border:0;border-bottom:1px solid #0b526f;border-radius:0;padding:12px;font-size:16px;font-weight:400}
#gv91-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
#gv91-root .info-panel{margin-top:16px;background:#01070b;border:1px solid #0d668a;border-radius:9px;overflow:hidden}
#gv91-root .info-head{padding:16px 18px;background:#03131d;border-bottom:1px solid rgba(53,198,255,.22)}
#gv91-root .info-title{font-size:21px;font-weight:700;color:#35c6ff;margin:0 0 6px}
#gv91-root .info-summary{color:#a9e8ff;line-height:1.5;margin:0}
#gv91-root .info-table{width:100%;border-collapse:collapse;background:#000}
#gv91-root .info-table th{padding:12px 14px;text-align:left;color:#35c6ff;background:#020d14;border-bottom:1px solid rgba(53,198,255,.25);font-size:14px}
#gv91-root .info-table td{padding:12px 14px;color:#b9edff;border-bottom:1px solid rgba(127,219,255,.10);vertical-align:top;line-height:1.4}
#gv91-root .info-table tr:last-child td{border-bottom:0}
#gv91-root .info-table td:first-child{width:24%;font-weight:700;color:#7FDBFF}
#gv91-root .info-loading,#gv91-root .info-error{padding:18px;font-family:monospace}
#gv91-root .info-loading{color:#8be0ff}
#gv91-root .info-error{color:#ff9f9f}
</style>
<h3>Galaxy Viewer — VIEWER-9-1</h3>
<div class="viewer-shell"><div id="gv91-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button class="random-btn" id="gv91-random" onclick="gv91RandomGalaxy()">Random Galaxy</button>
<button class="info-btn" id="gv91-info" onclick="gv91GetInfo()">Get Info</button>
<input id="gv91-name" class="galaxy-name" type="text" value="Pinwheel Galaxy (M101)" readonly>
</div>
<div class="controls">
<label>Displayed survey:</label>
<div class="survey-menu-wrap">
<input type="hidden" id="gv91-survey" value="P/DSS2/color">
<button type="button" id="gv91-survey-button" class="survey-menu-button" onclick="gv91ToggleSurveyMenu(event)">DSS2 Color ▾</button>
<div id="gv91-survey-menu" class="survey-menu"></div>
</div>
</div>
<div id="gv91-status" class="status">Viewer loading...</div>
<div id="gv91-panel" class="info-panel"><div class="info-loading">Press Get Info to research the displayed galaxy.</div></div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const GV91_SURVEYS=[
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];
const GV91_KEY="galaxy-viewer-viewer91-state";
function gv91Status(t){document.getElementById("gv91-status").textContent=t}
function gv91Esc(v){const d=document.createElement("div");d.textContent=String(v??"");return d.innerHTML}
function gv91Norm(id){return GV91_SURVEYS.some(s=>s.id===id)?id:"P/DSS2/color"}
function gv91SetupMenu(){document.getElementById("gv91-survey-menu").innerHTML=GV91_SURVEYS.map(s=>`<button type="button" class="survey-option" onclick="gv91ChooseSurvey('${s.id}',event)">${s.name}</button>`).join("")}
function gv91ToggleSurveyMenu(e){e.stopPropagation();document.getElementById("gv91-survey-menu").classList.toggle("open")}
function gv91ChooseSurvey(id,e){e.stopPropagation();gv91SetSurvey(id);document.getElementById("gv91-survey-menu").classList.remove("open");gv91Save();gv91Status("Loaded survey: "+id)}
function gv91SetSurvey(id){id=gv91Norm(id);document.getElementById("gv91-survey").value=id;const x=GV91_SURVEYS.find(s=>s.id===id);document.getElementById("gv91-survey-button").textContent=(x?x.name:id)+" ▾";window.gv91Aladin.setImageSurvey(id)}
function gv91Save(){if(!window.gv91Aladin)return;let c=[210.802267,54.348950],f=0.5;try{c=window.gv91Aladin.getRaDec()}catch(e){}try{const z=window.gv91Aladin.getFov();f=Array.isArray(z)?+z[0]:+z}catch(e){}localStorage.setItem(GV91_KEY,JSON.stringify({ra:+c[0],dec:+c[1],fov:+f,survey:document.getElementById("gv91-survey").value,name:document.getElementById("gv91-name").value}))}
function gv91Load(){try{return JSON.parse(localStorage.getItem(GV91_KEY)||"null")}catch(e){return null}}
function gv91ShowGalaxy(g,msg){document.getElementById("gv91-name").value=g.name||"";gv91SetSurvey(gv91Norm(g.survey_id));window.gv91Aladin.gotoRaDec(+g.ra,+g.dec);const f=()=>{try{window.gv91Aladin.setFoV(+g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);gv91Save();gv91Status(`${msg}: ${g.name} | ICRS ${(+g.ra).toFixed(6)} ${(+g.dec).toFixed(6)} | FOV ${g.fov}°`)}
function gv91Busy(id,on,text,normal){const b=document.getElementById(id);b.disabled=on;b.textContent=on?text:normal}
async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const r=await google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+e.message)}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}
async function gv91GetInfo(){gv91Busy("gv91-info",true,"Researching...","Get Info");const p=document.getElementById("gv91-panel");p.innerHTML='<div class="info-loading">Searching SIMBAD, NED, and authoritative astronomy sources...</div>';try{const c=window.gv91Aladin.getRaDec();const n=document.getElementById("gv91-name").value||"Displayed galaxy";const r=await google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",[n,+c[0],+c[1]],{});const d=r.data["application/json"];if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("Incomplete information table.");const rows=d.rows.map(x=>`<tr><td>${gv91Esc(x.parameter)}</td><td>${gv91Esc(x.value)}</td><td>${gv91Esc(x.notes)}</td><td>${gv91Esc(x.source)}</td></tr>`).join("");p.innerHTML=`<div class="info-head"><div class="info-title">${gv91Esc(d.title)}</div><p class="info-summary">${gv91Esc(d.summary)}</p></div><table class="info-table"><thead><tr><th>Parameter</th><th>Value</th><th>Notes</th><th>Source</th></tr></thead><tbody>${rows}</tbody></table>`;gv91Status("Galaxy information populated.")}catch(e){p.innerHTML='<div class="info-error">'+gv91Esc(e.message)+'</div>';gv91Status("Get Info failed: "+e.message)}finally{gv91Busy("gv91-info",false,"","Get Info")}}
(async()=>{gv91SetupMenu();await A.init;const s=gv91Load()||{ra:210.802267,dec:54.348950,fov:0.5,survey:"P/DSS2/color",name:"Pinwheel Galaxy (M101)"};document.getElementById("gv91-name").value=s.name||"Pinwheel Galaxy (M101)";window.gv91Aladin=A.aladin("#gv91-aladin",{target:`${s.ra} ${s.dec}`,survey:gv91Norm(s.survey),fov:+s.fov||0.5,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});gv91SetSurvey(gv91Norm(s.survey));gv91Status("Viewer ready.")})().catch(e=>gv91Status("Viewer initialization failed: "+e.message));
document.addEventListener("click",()=>{const m=document.getElementById("gv91-survey-menu");if(m)m.classList.remove("open")});
document.addEventListener("visibilitychange",()=>{if(document.hidden)gv91Save()});
window.addEventListener("pagehide",gv91Save);
</script>
'''

display(HTML(page))
