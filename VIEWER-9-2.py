from __future__ import annotations

import base64
import json
import urllib.request

from IPython.display import HTML, Javascript, display

VIEWER91_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/2e2829d05c5fba6bd5b0ffc431987612eebe1aee"

with urllib.request.urlopen(VIEWER91_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-9-1", "Galaxy Viewer — VIEWER-9-2", 1)

old_random = '''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const r=await google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+e.message)}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
new_random = '''const GV91_FALLBACK_GALAXIES=[
{name:"Andromeda Galaxy (M31)",ra:10.684708,dec:41.268750,fov:3.6,survey_id:"P/DSS2/color"},
{name:"Triangulum Galaxy (M33)",ra:23.462083,dec:30.660194,fov:1.5,survey_id:"P/DSS2/color"},
{name:"Whirlpool Galaxy (M51)",ra:202.469575,dec:47.195258,fov:0.22,survey_id:"P/DSS2/color"},
{name:"Sombrero Galaxy (M104)",ra:189.997633,dec:-11.623054,fov:0.20,survey_id:"P/DSS2/color"},
{name:"Pinwheel Galaxy (M101)",ra:210.802267,dec:54.348950,fov:0.50,survey_id:"P/DSS2/color"},
{name:"Bode's Galaxy (M81)",ra:148.888221,dec:69.065295,fov:0.42,survey_id:"P/DSS2/color"},
{name:"Cigar Galaxy (M82)",ra:148.968458,dec:69.679703,fov:0.24,survey_id:"P/DSS2/color"},
{name:"Southern Pinwheel Galaxy (M83)",ra:204.253833,dec:-29.865417,fov:0.42,survey_id:"P/DSS2/color"},
{name:"Sculptor Galaxy (NGC 253)",ra:11.888000,dec:-25.288167,fov:0.55,survey_id:"P/DSS2/color"},
{name:"Centaurus A (NGC 5128)",ra:201.365063,dec:-43.019112,fov:0.48,survey_id:"P/DSS2/color"},
{name:"Needle Galaxy (NGC 4565)",ra:189.086583,dec:25.987694,fov:0.34,survey_id:"P/DSS2/color"},
{name:"Phantom Galaxy (M74)",ra:24.174083,dec:15.783611,fov:0.24,survey_id:"P/DSS2/color"}
];
async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("Selecting a galaxy...");try{let g=null;try{const r=await parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});g=r.data["application/json"]}catch(apiError){g=GV91_FALLBACK_GALAXIES[Math.floor(Math.random()*GV91_FALLBACK_GALAXIES.length)];gv91Status("AI key unavailable; loaded a verified built-in galaxy instead.")}if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,g.reason?"AI galaxy loaded":"Random galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+e.message)}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
if source.count(old_random) != 1:
    raise RuntimeError("VIEWER-9-2 random function token not found exactly once")
source = source.replace(old_random, new_random, 1)

source = source.replace('google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo"', 'parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo"', 1)
source = source.replace('google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI"', 'parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI"', 1)

old_info_catch = '''}catch(e){p.innerHTML='<div class="info-error">'+gv91Esc(e.message)+'</div>';gv91Status("Get Info failed: "+e.message)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
new_info_catch = '''}catch(e){const missing=String(e.message||e).includes("OPENAI_API_KEY");const text=missing?"Get Info requires an OpenAI API key in Colab Secrets. Add OPENAI_API_KEY and enable notebook access.":String(e.message||e);p.innerHTML='<div class="info-error">'+gv91Esc(text)+'</div>';gv91Status(text)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
if source.count(old_info_catch) != 1:
    raise RuntimeError("VIEWER-9-2 info error token not found exactly once")
source = source.replace(old_info_catch, new_info_catch, 1)

old_display = "display(HTML(page))"
new_display = '''import html as _html
iframe = f'<iframe srcdoc="{_html.escape(page, quote=True)}" style="width:100%;height:1250px;border:0;background:#000" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>'
display(HTML(iframe))'''
if source.count(old_display) != 1:
    raise RuntimeError("VIEWER-9-2 display token not found exactly once")
source = source.replace(old_display, new_display, 1)

compile(source, "VIEWER-9-2.py", "exec")
exec(compile(source, "VIEWER-9-2.py", "exec"))
