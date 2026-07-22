from __future__ import annotations

import base64
import json
import urllib.request

BASE_BLOB = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/62096681b8b997d6f4b53fcd95bb1f6b94f7e3a4"
with urllib.request.urlopen(BASE_BLOB, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
wrapper = base64.b64decode(payload["content"]).decode("utf-8")

old_exec = 'exec(compile(source, "VIEWER-6.py", "exec"))'
insert = r'''
source = source.replace("Galaxy Viewer — VIEWER-6", "Galaxy Viewer — VIEWER-11", 1)

marker = "page = r'''"
backend = r'''import csv as _v11_csv
import io as _v11_io
import json as _v11_json
import math as _v11_math
import random as _v11_random
import urllib.parse as _v11_parse
import urllib.request as _v11_request

_V11_FALLBACK = [
    ("M 31",10.684708,41.268750,3.6),("M 33",23.462083,30.660194,1.5),
    ("M 51",202.469575,47.195258,0.22),("M 81",148.888221,69.065295,0.42),
    ("M 82",148.968458,69.679703,0.24),("M 83",204.253833,-29.865417,0.42),
    ("M 101",210.802267,54.348950,0.42),("M 104",189.997633,-11.623054,0.20),
    ("NGC 253",11.888000,-25.288167,0.55),("NGC 1365",53.401667,-36.140556,0.22),
]

def _v11_random_real_galaxy():
    for _ in range(15):
        recno = _v11_random.randint(1, 983261)
        query = _v11_parse.urlencode({
            "-source":"VII/237/pgc","recno":str(recno),
            "-out":"PGC,RAJ2000,DEJ2000,logD25","-out.max":"1",
        })
        url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?" + query
        with _v11_request.urlopen(url, timeout=30) as response:
            text = response.read().decode("utf-8", errors="replace")
        lines = [line for line in text.splitlines() if line and not line.startswith("#")]
        if len(lines) < 2:
            continue
        row = next(_v11_csv.DictReader(_v11_io.StringIO("\n".join(lines)), delimiter="\t"))
        try:
            from astropy.coordinates import SkyCoord
            import astropy.units as u
            c = SkyCoord(f'{row["RAJ2000"]} {row["DEJ2000"]}', unit=(u.hourangle,u.deg), frame="icrs")
            ra, dec = float(c.ra.deg), float(c.dec.deg)
        except Exception:
            continue
        fov = 0.18
        try:
            d = 0.1 * (10.0 ** float(row.get("logD25", "")))
            if d > 0:
                fov = max(0.035, min(2.5, d / 60.0 * 3.2))
        except Exception:
            pass
        return {"ok":True,"name":"PGC "+str(row.get("PGC","")).strip(),"ra":ra,"dec":dec,"fov":fov,"survey_id":"P/DSS2/color","source":"HyperLEDA via VizieR"}
    raise RuntimeError("No usable HyperLEDA row returned.")

def viewer11_random_callback():
    try:
        result = _v11_random_real_galaxy()
    except Exception as exc:
        name,ra,dec,fov = _v11_random.choice(_V11_FALLBACK)
        result = {"ok":True,"name":name,"ra":ra,"dec":dec,"fov":fov,"survey_id":"P/DSS2/color","source":"verified fallback","warning":str(exc)}
    return _v11_json.dumps(result)

output.register_callback("viewer11.randomGalaxy", viewer11_random_callback)

'''
if source.count(marker) != 1:
    raise RuntimeError("VIEWER-11 backend marker missing")
source = source.replace(marker, backend + marker, 1)

old = 'const VIEWER1_SURVEYS=[\n{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},'
new = 'const VIEWER1_SURVEYS=[\n{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},\n{name:"JWST Outreach Color",id:"CDS/P/JWST/EPO"},'
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 survey token missing")
source = source.replace(old, new, 1)

old = '<div class="controls">\n<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">\n<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>\n</div>'
new = '<div class="controls">\n<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" readonly style="min-width:280px">\n</div>'
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 controls token missing")
source = source.replace(old, new, 1)

start = source.find('const VIEWER1_GALAXIES=[')
end_token = '];\nconst VIEWER1_KEY="galaxy-viewer-viewer1-state";'
end = source.find(end_token)
if start < 0 or end < 0:
    raise RuntimeError("VIEWER-11 fixed catalog missing")
source = source[:start] + 'const VIEWER1_KEY="galaxy-viewer-viewer1-state";' + source[end + len(end_token):]

old = 'function viewer1PickRandom(){return VIEWER1_GALAXIES[Math.floor(Math.random()*VIEWER1_GALAXIES.length)]}'
new = '''function viewer11Parse(v){if(v==null)return v;if(typeof v!=="string")return v;v=v.trim();if(v.startsWith("'")&&v.endsWith("'"))v=v.slice(1,-1).replace(/\\\\'/g,"'").replace(/\\\\\\\\/g,"\\\\");try{return JSON.parse(v)}catch(_){return v}}
function viewer11Result(r){const d=r?.data??r;if(d&&typeof d==="object"&&d.ok!==undefined)return d;if(d&&typeof d==="object")return viewer11Parse(d["application/json"]??d["text/plain"]??Object.values(d)[0]);return viewer11Parse(d)}'''
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 picker token missing")
source = source.replace(old, new, 1)

old = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;window.viewer1Aladin.setImageSurvey("P/DSS2/color");window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:"P/DSS2/color",fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}'
new = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){const ra=Number(g.ra),dec=Number(g.dec),fov=Number(g.fov);document.getElementById("viewer1CoordBox").value=`${ra.toFixed(6)} ${dec.toFixed(6)}`;viewer1Survey(g.survey_id||"P/DSS2/color");window.viewer1Aladin.gotoRaDec(ra,dec);const z=()=>{try{window.viewer1Aladin.setFoV(fov)}catch(e){}};z();setTimeout(z,150);setTimeout(z,500);viewer1Save({ra,dec,survey:g.survey_id||"P/DSS2/color",fov});viewer1Status(`${message}: ${g.name} | ICRS ${ra.toFixed(6)} ${dec.toFixed(6)} | FOV ${fov.toFixed(3)}° | ${g.source}`)}'
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 display token missing")
source = source.replace(old, new, 1)

old = '(async()=>{viewer1Setup();const g=viewer1PickRandom();document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;document.getElementById("viewer1SurveySelect").value="P/DSS2/color";await A.init;window.viewer1Aladin=A.aladin("#viewer1-aladin",{target:`${g.ra} ${g.dec}`,survey:"P/DSS2/color",fov:g.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});viewer1ShowGalaxy(g,"Launch galaxy")})().catch(e=>viewer1Status("Viewer initialization failed: "+e.message));'
new = '(async()=>{viewer1Setup();const s=viewer1Load();document.getElementById("viewer1CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("viewer1SurveySelect").value=s.survey;await A.init;window.viewer1Aladin=A.aladin("#viewer1-aladin",{target:`${s.ra} ${s.dec}`,survey:s.survey,fov:s.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});await viewer1RandomGalaxy("Launch random galaxy")})().catch(e=>viewer1Status("Viewer initialization failed: "+e.message));'
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 launch token missing")
source = source.replace(old, new, 1)

old = 'function viewer1RandomGalaxy(){viewer1ShowGalaxy(viewer1PickRandom())}'
new = 'async function viewer1RandomGalaxy(message="Random galaxy loaded"){viewer1Status("Searching HyperLEDA/VizieR for a real random galaxy…");try{const r=await google.colab.kernel.invokeFunction("viewer11.randomGalaxy",[],{});const g=viewer11Result(r);if(!g||g.ok!==true)throw Error(g?.error||"Lookup failed");viewer1ShowGalaxy(g,message)}catch(e){viewer1Status("Random galaxy failed: "+String(e?.message||e))}}'
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 random token missing")
source = source.replace(old, new, 1)

old = 'function viewer1FindGalaxy(){try{const c=viewer1Coords(document.getElementById("viewer1CoordBox").value);window.VIEWER1_FIND_REQUEST={ra:c.ra,dec:c.dec,timestamp:Date.now()};viewer1Save({ra:c.ra,dec:c.dec});viewer1Status(`Find request ready for the next module: ${c.ra.toFixed(6)} ${c.dec.toFixed(6)}`)}catch(e){viewer1Status("Find request failed: "+e.message)}}'
if source.count(old) != 1:
    raise RuntimeError("VIEWER-11 find function token missing")
source = source.replace(old, '', 1)

for required in ['Random Galaxy','Fetch Coordinates','viewer11.randomGalaxy','VII/237/pgc','CDS/P/JWST/EPO','viewer1SurveyMenu','viewer1ChooseSurvey','viewer1FetchCoords()']:
    if required not in source:
        raise RuntimeError("VIEWER-11 required behavior missing: "+required)
for forbidden in ['Find Galaxy / Star','viewer1FindGalaxy()','const VIEWER1_GALAXIES=[']:
    if forbidden in source:
        raise RuntimeError("VIEWER-11 forbidden behavior present: "+forbidden)

exec(compile(source, "VIEWER-11.py", "exec"))
'''

if wrapper.count(old_exec) != 1:
    raise RuntimeError("VIEWER-11 execution token missing")
wrapper = wrapper.replace(old_exec, insert, 1)
compile(wrapper, "VIEWER-11-wrapper.py", "exec")
exec(compile(wrapper, "VIEWER-11-wrapper.py", "exec"))
