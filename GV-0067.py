from __future__ import annotations

import ast
import base64
import json
import urllib.request

GV0055_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/bc0df8ddebb8a230a6709c51c893bbd67a228f2d"

with urllib.request.urlopen(GV0055_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

# Version namespace only.
source = source.replace("gv0055", "gv0067")
source = source.replace("GV-0055", "GV-0067")

# Port GV-0066 search radii to the working GV-0055 viewer.
replacements = [
    ('"&radius=0.1&hconst=73', '"&radius=0.5&hconst=73'),
    ('6 arcsec cone search', '30 arcsec cone search'),
    ('const rad=6/3600', 'const rad=30/3600'),
    ("CIRCLE('ICRS',${ra},${dec},0.0016666667)", "CIRCLE('ICRS',${ra},${dec},0.0083333333)"),
    ('dbo.fGetNearbyObjEq(${ra},${dec},0.1)', 'dbo.fGetNearbyObjEq(${ra},${dec},0.5)'),
    ('radius=0.0016666667&nDetections.gte=1', 'radius=0.0083333333&nDetections.gte=1'),
    ('params:{ra,dec,radius:0.0016666667}', 'params:{ra,dec,radius:0.0083333333}'),
    ('SIMBAD and NED use a 6-arcsecond search.', 'SIMBAD and NED use a 30-arcsecond search.'),
    ('from the 6-arcsecond search window.', 'from the 30-arcsecond search window.'),
]
for old, new in replacements:
    if source.count(old) != 1:
        raise RuntimeError(f"GV-0067 expected search token not found exactly once: {old}")
    source = source.replace(old, new, 1)

# Port the GV-0066 visible full-search progress display.
old_css = '#gv0011-root .fetch-btn{background:#159447}#gv0011-root .find-btn{background:#087fd1}'
new_css = old_css + '#gv0011-root .progress-shell{display:flex;align-items:center;gap:10px;margin-top:10px;padding:9px 11px;background:#02080d;border:1px solid #0d668a;border-radius:7px}#gv0011-root .progress-spinner{width:18px;height:18px;border:3px solid #164d63;border-top-color:#43d2ff;border-radius:50%;animation:gv0067spin .8s linear infinite;display:none;flex:0 0 auto}#gv0011-root .progress-track{height:12px;flex:1;background:#031723;border:1px solid #116482;border-radius:8px;overflow:hidden}#gv0011-root .progress-fill{width:0%;height:100%;background:#159447;transition:width .25s ease}#gv0011-root .progress-text{min-width:150px;color:#8be0ff;font-family:monospace;font-size:12px}@keyframes gv0067spin{to{transform:rotate(360deg)}}'
if source.count(old_css) != 1:
    raise RuntimeError("GV-0067 button CSS block was not found exactly once.")
source = source.replace(old_css, new_css, 1)

old_controls = '<div class="controls"><button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button><input id="coordBox" type="text" value="53.162500 -27.791667" style="min-width:280px"><button class="find-btn" onclick="findGalaxy()">Find Galaxy / Star</button></div>'
new_controls = old_controls + '<div class="progress-shell"><div id="searchSpinner" class="progress-spinner"></div><div class="progress-track"><div id="searchProgressFill" class="progress-fill"></div></div><div id="searchProgressText" class="progress-text">Search idle</div></div>'
if source.count(old_controls) != 1:
    raise RuntimeError("GV-0067 search controls block was not found exactly once.")
source = source.replace(old_controls, new_controls, 1)

old_status = 'function status(t){document.getElementById("status").textContent=t}'
new_status = 'let gv0067ProgressDone=0;const gv0067ProgressTotal=6;function searchProgressStart(){gv0067ProgressDone=0;document.getElementById("searchSpinner").style.display="block";document.getElementById("searchProgressFill").style.width="0%";document.getElementById("searchProgressText").textContent="Searching: 0 / 6"}function searchProgressStep(){gv0067ProgressDone=Math.min(gv0067ProgressTotal,gv0067ProgressDone+1);document.getElementById("searchProgressFill").style.width=`${100*gv0067ProgressDone/gv0067ProgressTotal}%`;document.getElementById("searchProgressText").textContent=`Searching: ${gv0067ProgressDone} / ${gv0067ProgressTotal}`}function searchProgressDone(failed=false){document.getElementById("searchSpinner").style.display="none";document.getElementById("searchProgressFill").style.width="100%";document.getElementById("searchProgressText").textContent=failed?"Search stopped with an error":"Search complete"}function status(t){document.getElementById("status").textContent=t}'
if source.count(old_status) != 1:
    raise RuntimeError("GV-0067 status function was not found exactly once.")
source = source.replace(old_status, new_status, 1)

old_run = 'async function run(n,f){cat(n,"Searching…","warn");try{const d=await f(),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}}'
new_run = 'async function run(n,f){cat(n,"Searching…","warn");try{const timeoutMs=n==="VizieR"?180000:45000;const d=await Promise.race([f(),new Promise((_,reject)=>setTimeout(()=>reject(Error(`Timed out after ${timeoutMs/1000} seconds`)),timeoutMs))]),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}finally{searchProgressStep()}}'
if source.count(old_run) != 1:
    raise RuntimeError("GV-0067 catalog run function was not found exactly once.")
source = source.replace(old_run, new_run, 1)

old_find = 'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);'
new_find = 'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);searchProgressStart();'
if source.count(old_find) != 1:
    raise RuntimeError("GV-0067 findGalaxy start was not found exactly once.")
source = source.replace(old_find, new_find, 1)

old_complete = 'save();status("Search complete. GV-0067 used SIMBAD row 1 and NED row 1 from the 30-arcsecond search window.")'
new_complete = 'save();searchProgressDone();status("Search complete. GV-0067 used SIMBAD row 1 and NED row 1 from the 30-arcsecond search window.")'
if source.count(old_complete) != 1:
    raise RuntimeError("GV-0067 completion status was not found exactly once.")
source = source.replace(old_complete, new_complete, 1)

old_fail = '}catch(e){status("Search failed: "+e.message);debug(String(e.stack||e))}}'
new_fail = '}catch(e){searchProgressDone(true);status("Search failed: "+e.message);debug(String(e.stack||e))}}'
if source.count(old_fail) != 1:
    raise RuntimeError("GV-0067 failure handler was not found exactly once.")
source = source.replace(old_fail, new_fail, 1)

# Verify required preserved behavior remains in the generated file.
required = [
    '<select id="surveySelect" onchange="changeSurvey()"></select>',
    'window.aladin.setImageSurvey(id)',
    'document.addEventListener("visibilitychange",()=>document.hidden?save():restore("Viewer restored from saved tab state."))',
    'Waiting for final catalog aggregation…',
    '<div class="debug-wrap">',
    'SIMBAD row 1',
    'NED row 1',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"GV-0067 required preserved behavior missing: {token}")

ast.parse(source, filename="GV-0067-generated.py")
exec(compile(source, "GV-0067.py", "exec"))
