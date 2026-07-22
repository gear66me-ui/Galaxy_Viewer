from __future__ import annotations

import base64
import json
import urllib.request

VIEWER95_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/12427692fb4797bfdb3ba4c1e3ca1651f9f1d89a"

with urllib.request.urlopen(VIEWER95_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-9-5", "Galaxy Viewer — VIEWER-9-6", 1)

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

old_random_result = '''const g=r.data["application/json"];if(!g)throw Error("No galaxy data returned.");gv91ShowGalaxy(g,"AI galaxy loaded");'''
new_random_result = '''const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"OpenAI request failed.");const g=out.payload??out;if(!g||!Number.isFinite(+g.ra)||!Number.isFinite(+g.dec)||!Number.isFinite(+g.fov))throw Error("OpenAI returned invalid galaxy data.");gv91ShowGalaxy(g,"AI galaxy loaded");'''
if source.count(old_random_result) != 1:
    raise RuntimeError("VIEWER-9-6 random result token not found exactly once")
source = source.replace(old_random_result, new_random_result, 1)

old_info_result = '''const d=r.data["application/json"];if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("Incomplete information table.");'''
new_info_result = '''const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"OpenAI request failed.");const d=out.payload??out;if(!d||!Array.isArray(d.rows)||d.rows.length!==10)throw Error("OpenAI returned an incomplete information table.");'''
if source.count(old_info_result) != 1:
    raise RuntimeError("VIEWER-9-6 Get Info result token not found exactly once")
source = source.replace(old_info_result, new_info_result, 1)

old_compile = 'compile(source, "VIEWER-9-5-wrapper.py", "exec")\nexec(compile(source, "VIEWER-9-5-wrapper.py", "exec"))'
new_compile = '''for required in [
    'return {"ok": True, "payload": viewer9_random_ai()}',
    'return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}',
    'raw["application/json"]??raw["text/plain"]??Object.values(raw)[0]',
    'OpenAI returned invalid galaxy data.',
    'id="gv91-survey-menu"',
    'id="gv91-panel"',
]:
    if required not in source:
        raise RuntimeError(f"VIEWER-9-6 required behavior missing: {required}")

compile(source, "VIEWER-9-6.py", "exec")
exec(compile(source, "VIEWER-9-6.py", "exec"))'''
if source.count(old_compile) != 1:
    raise RuntimeError("VIEWER-9-6 execution token not found exactly once")
source = source.replace(old_compile, new_compile, 1)

compile(source, "VIEWER-9-6-wrapper.py", "exec")
exec(compile(source, "VIEWER-9-6-wrapper.py", "exec"))
