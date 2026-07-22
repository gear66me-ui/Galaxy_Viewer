from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request

from google.colab import output as colab_output

try:
    from google.colab import userdata
except Exception:
    userdata = None

VIEWER6_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/62096681b8b997d6f4b53fcd95bb1f6b94f7e3a4"


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
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it in Colab: left sidebar > Secrets > "
            "OPENAI_API_KEY, then enable notebook access."
        )

    model = _secret("OPENAI_MODEL", "gpt-5")
    body = {
        "model": model,
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
        raise RuntimeError(f"OpenAI API error {exc.code}: {detail[:1200]}") from exc

    text = _response_text(payload)
    if not text:
        raise RuntimeError("OpenAI returned no structured text output.")
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
        "reason": {"type": "string"},
    },
    "required": ["name", "ra", "dec", "fov", "survey_id", "reason"],
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
    prompt = """
Choose one real, visually interesting galaxy anywhere in the sky. Use web search to
verify its identity and ICRS decimal coordinates. Return a field of view in degrees
that frames the complete visible galaxy comfortably in Aladin Lite, not a tiny
thumbnail and not an excessively wide field.

Choose exactly one survey_id from this supported list:
CDS/P/HST/EPO
P/DSS2/color
P/DSS2/red
P/PanSTARRS/DR1/color-z-zg-g
P/DECaLS/DR5/color
P/2MASS/color
P/GALEXGR6/AIS/color

Prefer a broad-coverage color survey that actually contains useful imagery at the
chosen coordinates. Use DSS2 Color when uncertain. Return only the requested JSON.
"""
    return _openai_json(prompt, "random_galaxy", RANDOM_SCHEMA)


def viewer9_get_info(name: str, ra: float, dec: float):
    prompt = f"""
Research the galaxy currently displayed in the viewer.

Displayed name: {name}
ICRS coordinates: RA {float(ra):.8f} degrees, Dec {float(dec):.8f} degrees.

Use web search. Identify the object SIMBAD-first using a 30 arcsecond cone and treat
the first SIMBAD match as primary. Use NED and other authoritative astronomy
catalogs to supplement missing values. Do not invent unavailable measurements.

Return exactly ten rows, in this exact order:
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

For unavailable values write "Not available". Keep each source field concise,
naming the database, catalog, observatory, or paper rather than returning a raw URL.
Write a concise executive summary grounded in the researched facts. Return only the
requested JSON.
"""
    return _openai_json(prompt, "galaxy_information", INFO_SCHEMA)


colab_output.register_callback("viewer9.randomGalaxyAI", viewer9_random_ai)
colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_get_info)

with urllib.request.urlopen(VIEWER6_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
wrapper = base64.b64decode(payload["content"]).decode("utf-8")

old_exec = 'exec(compile(source, "VIEWER-6.py", "exec"))'

insert = r"""
source = source.replace("Galaxy Viewer — VIEWER-6", "Galaxy Viewer — VIEWER-9", 1)

old_css = '#viewer1-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}'
new_css = old_css + '#viewer1-root .info-btn{background:#c87916}#viewer1-root .galaxy-name{min-width:320px;flex:1}#viewer1-root .info-panel{margin-top:16px;background:#01070b;border:1px solid #0d668a;border-radius:9px;overflow:hidden}#viewer1-root .info-head{padding:16px 18px;background:#03131d;border-bottom:1px solid rgba(53,198,255,.22)}#viewer1-root .info-title{font-size:21px;font-weight:700;color:#35c6ff;margin:0 0 6px}#viewer1-root .info-summary{color:#a9e8ff;line-height:1.5;margin:0}#viewer1-root .info-table{width:100%;border-collapse:collapse;background:#000}#viewer1-root .info-table th{padding:12px 14px;text-align:left;color:#35c6ff;background:#020d14;border-bottom:1px solid rgba(53,198,255,.25);font-size:14px}#viewer1-root .info-table td{padding:12px 14px;color:#b9edff;border-bottom:1px solid rgba(127,219,255,.10);vertical-align:top;line-height:1.4}#viewer1-root .info-table tr:last-child td{border-bottom:0}#viewer1-root .info-table td:first-child{width:24%;font-weight:700;color:#7FDBFF}#viewer1-root .info-loading{padding:18px;color:#8be0ff;font-family:monospace}#viewer1-root .info-error{padding:18px;color:#ff9f9f;font-family:monospace}'
if source.count(old_css) != 1:
    raise RuntimeError("VIEWER-9 CSS token not found exactly once")
source = source.replace(old_css, new_css, 1)

old_controls = '<div class="controls">\n<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">\n<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>\n</div>'
new_controls = '<div class="controls">\n<button class="random-btn" id="viewer1RandomButton" onclick="viewer9RandomGalaxy()">Random Galaxy</button>\n<button class="info-btn" id="viewer1InfoButton" onclick="viewer9GetInfo()">Get Info</button>\n<input id="viewer1GalaxyName" class="galaxy-name" type="text" value="" readonly aria-label="Selected galaxy name">\n<input id="viewer1CoordBox" type="hidden" value="53.162500 -27.791667">\n</div>'
if source.count(old_controls) != 1:
    raise RuntimeError("VIEWER-9 controls token not found exactly once")
source = source.replace(old_controls, new_controls, 1)

old_status = '<div id="viewer1Status" class="status">Viewer loading…</div>'
new_status = '<div id="viewer1Status" class="status">Viewer loading…</div>\n<div id="viewer1InfoPanel" class="info-panel"><div class="info-loading">Press Get Info to research the displayed galaxy.</div></div>'
if source.count(old_status) != 1:
    raise RuntimeError("VIEWER-9 status token not found exactly once")
source = source.replace(old_status, new_status, 1)

old_show = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;window.viewer1Aladin.setImageSurvey("P/DSS2/color");window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:"P/DSS2/color",fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}'
new_show = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;document.getElementById("viewer1GalaxyName").value=g.name||"";const survey=viewer1Norm(g.survey_id||"P/DSS2/color");viewer1Survey(survey);window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:survey,fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}'
if source.count(old_show) != 1:
    raise RuntimeError("VIEWER-9 galaxy display token not found exactly once")
source = source.replace(old_show, new_show, 1)

old_random = 'function viewer1RandomGalaxy(){viewer1ShowGalaxy(viewer1PickRandom())}'
new_random = '''function viewer1RandomGalaxy(){viewer1ShowGalaxy(viewer1PickRandom())}
function viewer9Esc(v){const d=document.createElement("div");d.textContent=String(v??"");return d.innerHTML}
function viewer9SetBusy(id,busy,label){const b=document.getElementById(id);if(!b)return;b.disabled=busy;b.textContent=busy?label:b.dataset.normal}
async function viewer9RandomGalaxy(){
 const b=document.getElementById("viewer1RandomButton");b.dataset.normal="Random Galaxy";viewer9SetBusy("viewer1RandomButton",true,"Searching...");
 viewer1Status("AI is selecting and verifying a galaxy...");
 try{
  const r=await google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});
  const g=r.data["application/json"];
  if(!g||!Number.isFinite(+g.ra)||!Number.isFinite(+g.dec)||!Number.isFinite(+g.fov))throw Error("AI returned invalid galaxy data.");
  viewer1ShowGalaxy({name:g.name,ra:+g.ra,dec:+g.dec,fov:+g.fov,survey_id:g.survey_id},"AI galaxy loaded");
  document.getElementById("viewer1InfoPanel").innerHTML='<div class="info-loading">Press Get Info to research '+viewer9Esc(g.name)+'.</div>';
 }catch(e){viewer1Status("Random Galaxy failed: "+e.message)}
 finally{viewer9SetBusy("viewer1RandomButton",false,"")}
}
async function viewer9GetInfo(){
 const b=document.getElementById("viewer1InfoButton");b.dataset.normal="Get Info";viewer9SetBusy("viewer1InfoButton",true,"Researching...");
 const panel=document.getElementById("viewer1InfoPanel");panel.innerHTML='<div class="info-loading">Searching SIMBAD, NED, and authoritative astronomy sources...</div>';
 try{
  const c=window.viewer1Aladin.getRaDec();const name=document.getElementById("viewer1GalaxyName").value||"Displayed galaxy";
  const r=await google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",[name,+c[0],+c[1]],{});
  const d=r.data["application/json"];if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("AI returned an incomplete information table.");
  const rows=d.rows.map(x=>`<tr><td>${viewer9Esc(x.parameter)}</td><td>${viewer9Esc(x.value)}</td><td>${viewer9Esc(x.notes)}</td><td>${viewer9Esc(x.source)}</td></tr>`).join("");
  panel.innerHTML=`<div class="info-head"><div class="info-title">${viewer9Esc(d.title)}</div><p class="info-summary">${viewer9Esc(d.summary)}</p></div><table class="info-table"><thead><tr><th>Parameter</th><th>Value</th><th>Notes</th><th>Source</th></tr></thead><tbody>${rows}</tbody></table>`;
  viewer1Status("Galaxy information populated from AI-assisted web research.");
 }catch(e){panel.innerHTML='<div class="info-error">'+viewer9Esc(e.message)+'</div>';viewer1Status("Get Info failed: "+e.message)}
 finally{viewer9SetBusy("viewer1InfoButton",false,"")}
}'''
if source.count(old_random) != 1:
    raise RuntimeError("VIEWER-9 random function token not found exactly once")
source = source.replace(old_random, new_random, 1)

required = [
    'viewer1SurveyMenu',
    'viewer1ChooseSurvey',
    'viewer9RandomGalaxy()',
    'viewer9GetInfo()',
    'id="viewer1InfoPanel"',
    'viewer9.randomGalaxyAI',
    'viewer9.getGalaxyInfo',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"VIEWER-9 required behavior missing: {token}")

exec(compile(source, "VIEWER-9.py", "exec"))
"""

if wrapper.count(old_exec) != 1:
    raise RuntimeError("VIEWER-9 VIEWER-6 execution token not found exactly once")
wrapper = wrapper.replace(old_exec, insert, 1)

compile(wrapper, "VIEWER-9-wrapper.py", "exec")
exec(compile(wrapper, "VIEWER-9-wrapper.py", "exec"))
