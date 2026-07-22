from __future__ import annotations

import base64
import json
import urllib.request

VIEWER91_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/2e2829d05c5fba6bd5b0ffc431987612eebe1aee"

with urllib.request.urlopen(VIEWER91_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-9-1", "Galaxy Viewer — VIEWER-9-4", 1)

old_random = '''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const r=await google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+e.message)}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
new_random = '''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const kwargs=parent.JSON.parse("{}");const args=parent.JSON.parse("[]");const r=await parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs);const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+String(e.message||e))}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
if source.count(old_random) != 1:
    raise RuntimeError("VIEWER-9-4 random callback token not found exactly once")
source = source.replace(old_random, new_random, 1)

old_info_call = 'const r=await google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",[n,+c[0],+c[1]],{});'
new_info_call = 'const kwargs=parent.JSON.parse("{}");const args=parent.JSON.parse(JSON.stringify([n,+c[0],+c[1]]));const r=await parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs);'
if source.count(old_info_call) != 1:
    raise RuntimeError("VIEWER-9-4 Get Info callback token not found exactly once")
source = source.replace(old_info_call, new_info_call, 1)

old_info_catch = '''}catch(e){p.innerHTML='<div class="info-error">'+gv91Esc(e.message)+'</div>';gv91Status("Get Info failed: "+e.message)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
new_info_catch = '''}catch(e){const text=String(e.message||e);p.innerHTML='<div class="info-error">'+gv91Esc(text)+'</div>';gv91Status("Get Info failed: "+text)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
if source.count(old_info_catch) != 1:
    raise RuntimeError("VIEWER-9-4 Get Info error token not found exactly once")
source = source.replace(old_info_catch, new_info_catch, 1)

old_display = "display(HTML(page))"
new_display = '''import html as _html
iframe = f'<iframe srcdoc="{_html.escape(page, quote=True)}" style="width:100%;height:1250px;border:0;background:#000" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>'
display(HTML(iframe))'''
if source.count(old_display) != 1:
    raise RuntimeError("VIEWER-9-4 display token not found exactly once")
source = source.replace(old_display, new_display, 1)

for forbidden in ["GV91_FALLBACK_GALAXIES", "verified built-in galaxy", "Math.random()*GV91_FALLBACK_GALAXIES.length"]:
    if forbidden in source:
        raise RuntimeError(f"VIEWER-9-4 forbidden fallback behavior present: {forbidden}")

for required in [
    'parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs)',
    'parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs)',
    'parent.JSON.parse("{}")',
    'id="gv91-survey-menu"',
    'id="gv91-panel"',
]:
    if required not in source:
        raise RuntimeError(f"VIEWER-9-4 required behavior missing: {required}")

compile(source, "VIEWER-9-4.py", "exec")
exec(compile(source, "VIEWER-9-4.py", "exec"))
