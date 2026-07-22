from __future__ import annotations

import base64
import json
import urllib.request

VIEWER94_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/5eaa4364ad2cafbafe430c9f32e5db1e16850076"

with urllib.request.urlopen(VIEWER94_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-9-4", "Galaxy Viewer — VIEWER-9-5", 1)

old_compile = 'compile(source, "VIEWER-9-4.py", "exec")\nexec(compile(source, "VIEWER-9-4.py", "exec"))'
new_compile = '''source = source.replace('_secret("OPENAI_MODEL", "gpt-5")', '_secret("OPENAI_MODEL", "gpt-5-mini")', 1)
source = source.replace('"tools": [{"type": "web_search"}],', '"tools": [{"type": "web_search", "search_context_size": "low"}],', 1)
source = source.replace('urllib.request.urlopen(request, timeout=180)', 'urllib.request.urlopen(request, timeout=60)', 1)

old_random_wait = 'const r=await parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs);'
new_random_wait = 'const r=await Promise.race([parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs),new Promise((_,reject)=>setTimeout(()=>reject(new Error("OpenAI search timed out after 75 seconds.")),75000))]);'
if source.count(old_random_wait) != 1:
    raise RuntimeError("VIEWER-9-5 random wait token not found exactly once")
source = source.replace(old_random_wait, new_random_wait, 1)

old_info_wait = 'const r=await parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs);'
new_info_wait = 'const r=await Promise.race([parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs),new Promise((_,reject)=>setTimeout(()=>reject(new Error("OpenAI research timed out after 75 seconds.")),75000))]);'
if source.count(old_info_wait) != 1:
    raise RuntimeError("VIEWER-9-5 Get Info wait token not found exactly once")
source = source.replace(old_info_wait, new_info_wait, 1)

for required in [
    '_secret("OPENAI_MODEL", "gpt-5-mini")',
    '"search_context_size": "low"',
    'urllib.request.urlopen(request, timeout=60)',
    'OpenAI search timed out after 75 seconds.',
    'OpenAI research timed out after 75 seconds.',
    'id="gv91-survey-menu"',
    'id="gv91-panel"',
]:
    if required not in source:
        raise RuntimeError(f"VIEWER-9-5 required behavior missing: {required}")

compile(source, "VIEWER-9-5.py", "exec")
exec(compile(source, "VIEWER-9-5.py", "exec"))'''

if source.count(old_compile) != 1:
    raise RuntimeError("VIEWER-9-5 execution token not found exactly once")
source = source.replace(old_compile, new_compile, 1)

compile(source, "VIEWER-9-5-wrapper.py", "exec")
exec(compile(source, "VIEWER-9-5-wrapper.py", "exec"))
