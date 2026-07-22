from __future__ import annotations

import base64
import json
import urllib.request

BASE_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/2e2829d05c5fba6bd5b0ffc431987612eebe1aee"

with urllib.request.urlopen(BASE_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-9-1", "Galaxy Viewer — VIEWER-9-7", 1)
source = source.replace('_secret("OPENAI_MODEL", "gpt-5")', '_secret("OPENAI_MODEL", "gpt-5-mini")', 1)
source = source.replace('"tools": [{"type": "web_search"}],', '"tools": [{"type": "web_search", "search_context_size": "low"}],', 1)
source = source.replace('urllib.request.urlopen(request, timeout=180)', 'urllib.request.urlopen(request, timeout=60)', 1)

old_register = '''colab_output.register_callback("viewer9.randomGalaxyAI", viewer9_random_ai)
colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_get_info)'''
new_register = '''def viewer9_info_callback(name: str, ra: float, dec: float):
    try:
        return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_info_callback)'''
if source.count(old_register) != 1:
    raise RuntimeError("VIEWER-9-7 callback registration token not found exactly once")
source = source.replace(old_register, new_register, 1)

old_surveys_end = '''{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];'''
new_surveys_end = '''{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];
const GV97_GALAXIES=[
{name:"Andromeda Galaxy (M31)",ra:10.6847083,dec:41.2687500,fov:4.2,survey_id:"P/DSS2/color"},
{name:"Triangulum Galaxy (M33)",ra:23.4620833,dec:30.6601944,fov:1.8,survey_id:"P/DSS2/color"},
{name:"Whirlpool Galaxy (M51)",ra:202.4695750,dec:47.1952583,fov:0.30,survey_id:"P/DSS2/color"},
{name:"Sombrero Galaxy (M104)",ra:189.9976333,dec:-11.6230556,fov:0.35,survey_id:"P/DSS2/color"},
{name:"Bode's Galaxy (M81)",ra:148.8882208,dec:69.0652944,fov:0.70,survey_id:"P/DSS2/color"},
{name:"Cigar Galaxy (M82)",ra:148.9684583,dec:69.6797028,fov:0.35,survey_id:"P/DSS2/color"},
{name:"Sculptor Galaxy (NGC 253)",ra:11.8880000,dec:-25.2882222,fov:0.65,survey_id:"P/DSS2/color"},
{name:"Centaurus A (NGC 5128)",ra:201.3650625,dec:-43.0191125,fov:0.65,survey_id:"P/DSS2/color"},
{name:"Southern Pinwheel Galaxy (M83)",ra:204.2538292,dec:-29.8657611,fov:0.55,survey_id:"P/DSS2/color"},
{name:"Black Eye Galaxy (M64)",ra:194.1820667,dec:21.6826583,fov:0.30,survey_id:"P/DSS2/color"},
{name:"Sunflower Galaxy (M63)",ra:198.9555375,dec:42.0292889,fov:0.30,survey_id:"P/DSS2/color"},
{name:"Needle Galaxy (NGC 4565)",ra:189.0866250,dec:25.9876944,fov:0.45,survey_id:"P/DSS2/color"},
{name:"Silver Coin Galaxy (NGC 4945)",ra:196.3644875,dec:-49.4682125,fov:0.55,survey_id:"P/DSS2/color"},
{name:"Fireworks Galaxy (NGC 6946)",ra:308.7180000,dec:60.1538889,fov:0.45,survey_id:"P/DSS2/color"},
{name:"Cartwheel Galaxy",ra:9.4210833,dec:-33.7101944,fov:0.12,survey_id:"P/DSS2/color"},
{name:"NGC 1365",ra:53.4015500,dec:-36.1404000,fov:0.35,survey_id:"P/DSS2/color"},
{name:"NGC 1300",ra:49.9208333,dec:-19.4116667,fov:0.22,survey_id:"P/DSS2/color"},
{name:"NGC 6744",ra:287.4420833,dec:-63.8575000,fov:0.45,survey_id:"P/DSS2/color"},
{name:"NGC 2903",ra:143.0421250,dec:21.5008333,fov:0.35,survey_id:"P/DSS2/color"},
{name:"NGC 7331",ra:339.2670833,dec:34.4155556,fov:0.30,survey_id:"P/DSS2/color"}
];
function gv97PickGalaxy(excludeName=""){const choices=GV97_GALAXIES.filter(g=>g.name!==excludeName);return choices[Math.floor(Math.random()*choices.length)]||GV97_GALAXIES[0]}
const GV97_PARAMETERS=["Common designations","Constellation","Morphological type","ICRS coordinates","Distance","Diameter / physical size","Redshift and radial velocity","Apparent magnitude","Stellar mass or estimated star count","Estimated stellar age"];
function gv97NormalizeInfo(d){d=(d&&typeof d==="object")?d:{};const incoming=Array.isArray(d.rows)?d.rows:[];const used=new Set();const rows=GV97_PARAMETERS.map((parameter,index)=>{let found=-1;const key=parameter.toLowerCase();for(let i=0;i<incoming.length;i++){if(used.has(i))continue;const p=String(incoming[i]?.parameter||"").toLowerCase();if(p===key||p.includes(key.split(" /")[0])||key.includes(p)){found=i;break}}if(found<0&&index<incoming.length&&!used.has(index))found=index;if(found>=0){used.add(found);const x=incoming[found]||{};return {parameter,value:String(x.value||"Not available"),notes:String(x.notes||""),source:String(x.source||"")}}return {parameter,value:"Not available",notes:"Not returned by the single API response.",source:""}});return {title:String(d.title||document.getElementById("gv91-name").value||"Galaxy information"),summary:String(d.summary||"Available information from the single API response."),rows}}
'''
if source.count(old_surveys_end) != 1:
    raise RuntimeError("VIEWER-9-7 survey insertion token not found exactly once")
source = source.replace(old_surveys_end, new_surveys_end, 1)

old_random = '''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const r=await google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+e.message)}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
new_random = '''function gv91RandomGalaxy(){const current=document.getElementById("gv91-name").value||"";const g=gv97PickGalaxy(current);gv91ShowGalaxy(g,"Random galaxy loaded — no API charge");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'. Random Galaxy does not call the OpenAI API.</div>'}'''
if source.count(old_random) != 1:
    raise RuntimeError("VIEWER-9-7 random function token not found exactly once")
source = source.replace(old_random, new_random, 1)

old_info = '''async function gv91GetInfo(){gv91Busy("gv91-info",true,"Researching...","Get Info");const p=document.getElementById("gv91-panel");p.innerHTML='<div class="info-loading">Searching SIMBAD, NED, and authoritative astronomy sources...</div>';try{const c=window.gv91Aladin.getRaDec();const n=document.getElementById("gv91-name").value||"Displayed galaxy";const r=await google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",[n,+c[0],+c[1]],{});const d=r.data["application/json"];if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("Incomplete information table.");const rows=d.rows.map(x=>`<tr><td>${gv91Esc(x.parameter)}</td><td>${gv91Esc(x.value)}</td><td>${gv91Esc(x.notes)}</td><td>${gv91Esc(x.source)}</td></tr>`).join("");p.innerHTML=`<div class="info-head"><div class="info-title">${gv91Esc(d.title)}</div><p class="info-summary">${gv91Esc(d.summary)}</p></div><table class="info-table"><thead><tr><th>Parameter</th><th>Value</th><th>Notes</th><th>Source</th></tr></thead><tbody>${rows}</tbody></table>`;gv91Status("Galaxy information populated.")}catch(e){p.innerHTML='<div class="info-error">'+gv91Esc(e.message)+'</div>';gv91Status("Get Info failed: "+e.message)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
new_info = '''async function gv91GetInfo(){gv91Busy("gv91-info",true,"Researching...","Get Info");const p=document.getElementById("gv91-panel");p.innerHTML='<div class="info-loading">One paid API request: searching SIMBAD, NED, and authoritative astronomy sources...</div>';try{const c=window.gv91Aladin.getRaDec();const n=document.getElementById("gv91-name").value||"Displayed galaxy";const args=parent.JSON.parse(JSON.stringify([n,+c[0],+c[1]]));const kwargs=parent.JSON.parse("{}");const r=await Promise.race([parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs),new Promise((_,reject)=>setTimeout(()=>reject(new Error("OpenAI research timed out after 75 seconds. No automatic retry was made.")),75000))]);const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"OpenAI request failed.");const d=gv97NormalizeInfo(out.payload??out);const rows=d.rows.map(x=>`<tr><td>${gv91Esc(x.parameter)}</td><td>${gv91Esc(x.value)}</td><td>${gv91Esc(x.notes)}</td><td>${gv91Esc(x.source)}</td></tr>`).join("");p.innerHTML=`<div class="info-head"><div class="info-title">${gv91Esc(d.title)}</div><p class="info-summary">${gv91Esc(d.summary)}</p></div><table class="info-table"><thead><tr><th>Parameter</th><th>Value</th><th>Notes</th><th>Source</th></tr></thead><tbody>${rows}</tbody></table>`;gv91Status("Galaxy information populated from one API request; missing fields were filled locally as Not available.")}catch(e){const text=String(e.message||e);p.innerHTML='<div class="info-error">'+gv91Esc(text)+'</div>';gv91Status("Get Info failed: "+text)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
if source.count(old_info) != 1:
    raise RuntimeError("VIEWER-9-7 Get Info function token not found exactly once")
source = source.replace(old_info, new_info, 1)

old_init = '''(async()=>{gv91SetupMenu();await A.init;const s=gv91Load()||{ra:210.802267,dec:54.348950,fov:0.5,survey:"P/DSS2/color",name:"Pinwheel Galaxy (M101)"};document.getElementById("gv91-name").value=s.name||"Pinwheel Galaxy (M101)";window.gv91Aladin=A.aladin("#gv91-aladin",{target:`${s.ra} ${s.dec}`,survey:gv91Norm(s.survey),fov:+s.fov||0.5,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});gv91SetSurvey(gv91Norm(s.survey));gv91Status("Viewer ready.")})().catch(e=>gv91Status("Viewer initialization failed: "+e.message));'''
new_init = '''(async()=>{gv91SetupMenu();await A.init;const previous=gv91Load();const s=gv97PickGalaxy(previous&&previous.name?previous.name:"");document.getElementById("gv91-name").value=s.name;window.gv91Aladin=A.aladin("#gv91-aladin",{target:`${s.ra} ${s.dec}`,survey:gv91Norm(s.survey_id),fov:+s.fov||0.5,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});gv91SetSurvey(gv91Norm(s.survey_id));gv91Save();gv91Status(`Random startup galaxy loaded — no API charge: ${s.name}`)})().catch(e=>gv91Status("Viewer initialization failed: "+e.message));'''
if source.count(old_init) != 1:
    raise RuntimeError("VIEWER-9-7 initialization token not found exactly once")
source = source.replace(old_init, new_init, 1)

old_display = "display(HTML(page))"
new_display = '''import html as _html
iframe = f'<iframe srcdoc="{_html.escape(page, quote=True)}" style="width:100%;height:1250px;border:0;background:#000" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>'
display(HTML(iframe))'''
if source.count(old_display) != 1:
    raise RuntimeError("VIEWER-9-7 display token not found exactly once")
source = source.replace(old_display, new_display, 1)

for required in [
    'const GV97_GALAXIES=[',
    'Random galaxy loaded — no API charge',
    'Random startup galaxy loaded — no API charge',
    'function gv97NormalizeInfo(d)',
    'return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}',
    'No automatic retry was made.',
    'id="gv91-survey-menu"',
    'id="gv91-panel"',
]:
    if required not in source:
        raise RuntimeError(f"VIEWER-9-7 required behavior missing: {required}")

for forbidden in [
    'viewer9.randomGalaxyAI',
    'Incomplete information table.',
    'No galaxy data returned.',
]:
    if forbidden in source:
        raise RuntimeError(f"VIEWER-9-7 forbidden behavior present: {forbidden}")

compile(source, "VIEWER-9-7.py", "exec")
exec(compile(source, "VIEWER-9-7.py", "exec"))
