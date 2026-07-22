from __future__ import annotations

import base64
import json
import urllib.request

BASE_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/2e2829d05c5fba6bd5b0ffc431987612eebe1aee"

with urllib.request.urlopen(BASE_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-9-1", "Galaxy Viewer — VIEWER-9-6", 1)
source = source.replace('_secret("OPENAI_MODEL", "gpt-5")', '_secret("OPENAI_MODEL", "gpt-5-mini")', 1)
source = source.replace('"tools": [{"type": "web_search"}],', '"tools": [{"type": "web_search", "search_context_size": "low"}],', 1)
source = source.replace('urllib.request.urlopen(request, timeout=180)', 'urllib.request.urlopen(request, timeout=60)', 1)

old_register = '''colab_output.register_callback("viewer9.randomGalaxyAI", viewer9_random_ai)
colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_get_info)'''
new_register = '''def viewer9_random_callback():
    try:
        return {"ok": True, "payload": viewer9_random_ai()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def viewer9_info_callback(name: str, ra: float, dec: float):
    try:
        return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


colab_output.register_callback("viewer9.randomGalaxyAI", viewer9_random_callback)
colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_info_callback)'''
if source.count(old_register) != 1:
    raise RuntimeError("VIEWER-9-6 callback registration token not found exactly once")
source = source.replace(old_register, new_register, 1)

old_random = '''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const r=await google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",[],{});const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+e.message)}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
new_random = '''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("AI is selecting and verifying a galaxy...");try{const args=parent.JSON.parse("[]");const kwargs=parent.JSON.parse("{}");const r=await Promise.race([parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs),new Promise((_,reject)=>setTimeout(()=>reject(new Error("OpenAI search timed out after 75 seconds.")),75000))]);const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"OpenAI request failed.");const g=out.payload??out;if(!g||!Number.isFinite(+g.ra)||!Number.isFinite(+g.dec)||!Number.isFinite(+g.fov))throw Error("OpenAI returned invalid galaxy data.");gv91ShowGalaxy(g,"AI galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+String(e.message||e))}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
if source.count(old_random) != 1:
    raise RuntimeError("VIEWER-9-6 random function token not found exactly once")
source = source.replace(old_random, new_random, 1)

old_info_call = 'const r=await google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",[n,+c[0],+c[1]],{});const d=r.data["application/json"];if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("Incomplete information table.");'
new_info_call = 'const args=parent.JSON.parse(JSON.stringify([n,+c[0],+c[1]]));const kwargs=parent.JSON.parse("{}");const r=await Promise.race([parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs),new Promise((_,reject)=>setTimeout(()=>reject(new Error("OpenAI research timed out after 75 seconds.")),75000))]);const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"OpenAI request failed.");const d=out.payload??out;if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("OpenAI returned an incomplete information table.");'
if source.count(old_info_call) != 1:
    raise RuntimeError("VIEWER-9-6 Get Info callback token not found exactly once")
source = source.replace(old_info_call, new_info_call, 1)

old_info_catch = '''}catch(e){p.innerHTML='<div class="info-error">'+gv91Esc(e.message)+'</div>';gv91Status("Get Info failed: "+e.message)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
new_info_catch = '''}catch(e){const text=String(e.message||e);p.innerHTML='<div class="info-error">'+gv91Esc(text)+'</div>';gv91Status("Get Info failed: "+text)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
if source.count(old_info_catch) != 1:
    raise RuntimeError("VIEWER-9-6 Get Info error token not found exactly once")
source = source.replace(old_info_catch, new_info_catch, 1)

old_display = "display(HTML(page))"
new_display = '''import html as _html
iframe = f'<iframe srcdoc="{_html.escape(page, quote=True)}" style="width:100%;height:1250px;border:0;background:#000" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>'
display(HTML(iframe))'''
if source.count(old_display) != 1:
    raise RuntimeError("VIEWER-9-6 display token not found exactly once")
source = source.replace(old_display, new_display, 1)

for forbidden in ["GV91_FALLBACK_GALAXIES", "No galaxy data returned."]:
    if forbidden in source:
        raise RuntimeError(f"VIEWER-9-6 forbidden behavior present: {forbidden}")

for required in [
    'return {"ok": True, "payload": viewer9_random_ai()}',
    'return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}',
    'raw["application/json"]??raw["text/plain"]??Object.values(raw)[0]',
    'parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs)',
    'parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs)',
    'id="gv91-survey-menu"',
    'id="gv91-panel"',
]:
    if required not in source:
        raise RuntimeError(f"VIEWER-9-6 required behavior missing: {required}")

compile(source, "VIEWER-9-6.py", "exec")
exec(compile(source, "VIEWER-9-6.py", "exec"))
