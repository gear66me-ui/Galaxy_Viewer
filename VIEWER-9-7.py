from __future__ import annotations
import base64, json, re, urllib.error, urllib.request

BASE_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/2e2829d05c5fba6bd5b0ffc431987612eebe1aee"
with urllib.request.urlopen(BASE_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")
source = source.replace("Galaxy Viewer — VIEWER-9-1", "Galaxy Viewer — VIEWER-9-7 GEMINI", 1)

gemini_backend = r'''def _openai_json(prompt: str, schema_name: str, schema: dict) -> dict:
    api_key = _secret("Gemini API Key") or _secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError('Add the Colab secret named exactly "Gemini API Key" and enable notebook access.')
    prompt = prompt + "\nReturn only one valid JSON object with no Markdown fences. Follow this schema exactly:\n" + json.dumps(schema, separators=(",", ":"))
    body = {"contents":[{"parts":[{"text":prompt}]}],"tools":[{"google_search":{}}],"generationConfig":{"temperature":0.9 if schema_name=="random_galaxy" else 0.2}}
    request = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",data=json.dumps(body).encode("utf-8"),headers={"x-goog-api-key":api_key,"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(request, timeout=75) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API error {exc.code}: {detail[:1200]}") from exc
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed: {exc}") from exc
    candidates = result.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidate: " + json.dumps(result.get("promptFeedback") or {})[:800])
    parts = ((candidates[0].get("content") or {}).get("parts") or [])
    text = "".join(str(x.get("text","")) for x in parts if x.get("text")).strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"): text = text[4:].strip()
    a,b=text.find("{"),text.rfind("}")
    if a<0 or b<a: raise RuntimeError(f"Gemini returned non-JSON text: {text[:1000]}")
    try:
        return json.loads(text[a:b+1])
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini returned invalid JSON: {text[:1000]}") from exc'''

source,n=re.subn(r'def _openai_json\(prompt: str, schema_name: str, schema: dict\) -> dict:\n.*?\n    return json\.loads\(text\)',gemini_backend,source,count=1,flags=re.S)
if n!=1: raise RuntimeError("Gemini backend replacement failed")

callbacks = '''def viewer9_random_callback():
    try: return {"ok": True, "payload": viewer9_random_ai()}
    except Exception as exc: return {"ok": False, "error": str(exc)}

def viewer9_info_callback(name: str, ra: float, dec: float):
    try: return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}
    except Exception as exc: return {"ok": False, "error": str(exc)}

colab_output.register_callback("viewer9.randomGalaxyAI", viewer9_random_callback)
colab_output.register_callback("viewer9.getGalaxyInfo", viewer9_info_callback)'''
source,n=re.subn(r'colab_output\.register_callback\("viewer9\.randomGalaxyAI".*?\ncolab_output\.register_callback\("viewer9\.getGalaxyInfo".*?\)',callbacks,source,count=1,flags=re.S)
if n!=1: raise RuntimeError("Callback replacement failed")

random_js='''async function gv91RandomGalaxy(){gv91Busy("gv91-random",true,"Searching...","Random Galaxy");gv91Status("Gemini Search is selecting and verifying a random galaxy...");try{const args=parent.JSON.parse("[]"),kwargs=parent.JSON.parse("{}");const r=await parent.google.colab.kernel.invokeFunction("viewer9.randomGalaxyAI",args,kwargs);const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"Gemini random search failed.");const g=out.payload??out;if(!g||!Number.isFinite(+g.ra)||!Number.isFinite(+g.dec)||!Number.isFinite(+g.fov))throw Error("Gemini returned invalid galaxy data.");gv91ShowGalaxy(g,"Gemini random galaxy loaded");document.getElementById("gv91-panel").innerHTML='<div class="info-loading">Press Get Info to research '+gv91Esc(g.name)+'.</div>'}catch(e){gv91Status("Random Galaxy failed: "+String(e.message||e))}finally{gv91Busy("gv91-random",false,"","Random Galaxy")}}'''
source,n=re.subn(r'async function gv91RandomGalaxy\(\)\{.*?\}\nasync function gv91GetInfo',random_js+'\nasync function gv91GetInfo',source,count=1,flags=re.S)
if n!=1: raise RuntimeError("Random replacement failed")

info_js='''async function gv91GetInfo(){gv91Busy("gv91-info",true,"Researching...","Get Info");const p=document.getElementById("gv91-panel");p.innerHTML='<div class="info-loading">Gemini Search is checking SIMBAD, NED, and astronomy sources...</div>';try{const c=window.gv91Aladin.getRaDec(),n=document.getElementById("gv91-name").value||"Displayed galaxy";const args=parent.JSON.parse(JSON.stringify([n,+c[0],+c[1]])),kwargs=parent.JSON.parse("{}");const r=await parent.google.colab.kernel.invokeFunction("viewer9.getGalaxyInfo",args,kwargs);const raw=r&&r.data?r.data:{};let out=raw["application/json"]??raw["text/plain"]??Object.values(raw)[0];if(typeof out==="string"){try{out=JSON.parse(out)}catch(_){}}if(!out)throw Error("Colab returned no callback payload.");if(out.ok===false)throw Error(out.error||"Gemini Get Info failed.");const d=out.payload??out;if(!d||!Array.isArray(d.rows))throw Error("Gemini returned no information rows.");const rows=d.rows.map(x=>`<tr><td>${gv91Esc(x.parameter)}</td><td>${gv91Esc(x.value)}</td><td>${gv91Esc(x.notes)}</td><td>${gv91Esc(x.source)}</td></tr>`).join("");p.innerHTML=`<div class="info-head"><div class="info-title">${gv91Esc(d.title||n)}</div><p class="info-summary">${gv91Esc(d.summary||"")}</p></div><table class="info-table"><thead><tr><th>Parameter</th><th>Value</th><th>Notes</th><th>Source</th></tr></thead><tbody>${rows}</tbody></table>`;gv91Status("Galaxy information populated by Gemini Search.")}catch(e){const text=String(e.message||e);p.innerHTML='<div class="info-error">'+gv91Esc(text)+'</div>';gv91Status("Get Info failed: "+text)}finally{gv91Busy("gv91-info",false,"","Get Info")}}'''
source,n=re.subn(r'async function gv91GetInfo\(\)\{.*?\}\n\(async\(\)=>',info_js+'\n(async()=>',source,count=1,flags=re.S)
if n!=1: raise RuntimeError("Info replacement failed")

source=source.replace('gv91Status("Viewer ready.")})().catch','gv91Status("Viewer ready. Loading a Gemini random galaxy...");setTimeout(gv91RandomGalaxy,300)})().catch',1)
source=source.replace("display(HTML(page))",'''import html as _html
iframe=f'<iframe srcdoc="{_html.escape(page,quote=True)}" style="width:100%;height:1250px;border:0;background:#000" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>'
display(HTML(iframe))''',1)

for forbidden in ["OPENAI_API_KEY","api.openai.com","GV97_GALAXIES","Incomplete information table."]:
    if forbidden in source: raise RuntimeError(f"Forbidden behavior remains: {forbidden}")
for required in ['"Gemini API Key"',"gemini-2.5-flash:generateContent",'"google_search": {}','invokeFunction("viewer9.randomGalaxyAI"','invokeFunction("viewer9.getGalaxyInfo"',"setTimeout(gv91RandomGalaxy,300)"]:
    if required not in source: raise RuntimeError(f"Required behavior missing: {required}")

compile(source,"VIEWER-9-7.py","exec")
exec(compile(source,"VIEWER-9-7.py","exec"))
