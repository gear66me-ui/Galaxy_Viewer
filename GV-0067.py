from __future__ import annotations

import ast
import base64
import json
import urllib.request

from google.colab import output
from IPython.display import Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

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
    ('SIMBAD and NED use a 6-arcsecond search.', 'SIMBAD, NED, and VizieR use a 30-arcsecond search.'),
    ('Row 1 is SIMBAD row 1 and row 2 is NED row 1.', 'Row 1 is SIMBAD row 1, row 2 is NED row 1, and row 3 is the closest VizieR row.'),
    ('from the 6-arcsecond search window.', 'from the 30-arcsecond search window.'),
]
for old, new in replacements:
    if source.count(old) != 1:
        raise RuntimeError(f"GV-0067 expected search token not found exactly once: {old}")
    source = source.replace(old, new, 1)

# Port the GV-0066 visible full-search progress display and thumbnail/link styling.
old_css = '#gv0011-root .fetch-btn{background:#159447}#gv0011-root .find-btn{background:#087fd1}'
new_css = old_css + '#gv0011-root .progress-shell{display:flex;align-items:center;gap:10px;margin-top:10px;padding:9px 11px;background:#02080d;border:1px solid #0d668a;border-radius:7px}#gv0011-root .progress-spinner{width:18px;height:18px;border:3px solid #164d63;border-top-color:#43d2ff;border-radius:50%;animation:gv0067spin .8s linear infinite;display:none;flex:0 0 auto}#gv0011-root .progress-track{height:12px;flex:1;background:#031723;border:1px solid #116482;border-radius:8px;overflow:hidden}#gv0011-root .progress-fill{width:0%;height:100%;background:#159447;transition:width .25s ease}#gv0011-root .progress-text{min-width:150px;color:#8be0ff;font-family:monospace;font-size:12px}@keyframes gv0067spin{to{transform:rotate(360deg)}}#gv0011-root .object-link{display:inline-block;color:#58d7ff;font-weight:700;text-decoration:none;border-bottom:1px dotted rgba(88,215,255,.65)}#gv0011-root .thumbnail-container{margin-top:10px}#gv0011-root .catalog-thumbnail{display:block;width:150px;height:105px;object-fit:cover;background:#02080d;border:1px solid #137aa3;border-radius:7px}'
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

old_result = 'function resultRow(o,c,r){if(!o)return"";const d=distance(o),z=+o.rvz_redshift,name=`${String(o.main_id||"Not available").trim()} — ${c}`,ra=Number.isFinite(+o.ra)?(+o.ra).toFixed(6):r.ra.toFixed(6),de=Number.isFinite(+o.dec)?(+o.dec).toFixed(6):r.dec.toFixed(6),zd=z>0?`${z.toFixed(6)} / ${d?fmt(d/1e9,6)+" BLY":"distance unavailable"}`:"Not available",ts=[o.otype,o.sp_type].filter(Boolean).join(" / ")||"Not available",info=`Catalog: ${c}; Selection: ${c} row 1; Candidates: ${o._candidateCount||1}`;return`<tr><td>${safe(name)}</td><td style="font-family:monospace">${ra} ${de}</td><td>${safe(zd)}</td><td>${safe(size(o,d))}</td><td>Not available in ${c}</td><td>${safe(ts)}</td><td>${safe(info)}</td></tr>`}'
new_result = '''function catalogUrl(c,name,ra,de){if(c==="SIMBAD")return"https://simbad.cds.unistra.fr/simbad/sim-id?Ident="+encodeURIComponent(name);if(c==="NED")return"https://ned.ipac.caltech.edu/byname?objname="+encodeURIComponent(name);return`https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=VII/258/vv10&-c=${ra}%20${de}&-c.rs=30&-out.max=100&-out.add=_r&-sort=_r`}
function thumbnailUrl(ra,de){return`https://alasky.cds.unistra.fr/hips-image-services/hips2fits?hips=CDS/P/DSS2/color&width=220&height=160&fov=0.03&projection=TAN&coordsys=icrs&format=jpg&ra=${ra}&dec=${de}`}
function vizierRow(v,r){if(!v||!Array.isArray(v.data)||!v.data.length)return null;const names=(v.metadata||[]).map(m=>m.name),row=v.data[0],o=Object.fromEntries(names.map((n,i)=>[n,row[i]])),pick=(...ks)=>{for(const k of ks)if(o[k]!=null)return o[k];return null};return{main_id:pick("Name","Source","ID","recno")||"VizieR row 1",ra:pick("RAJ2000","RA_ICRS","RAdeg","RA")??r.ra,dec:pick("DEJ2000","DE_ICRS","DEdeg","DEC","Dec")??r.dec,otype:pick("Type","otype","Class"),rvz_redshift:pick("z","Redshift"),rvz_radvel:pick("Velocity"),galdim_majaxis:null,galdim_minaxis:null,sp_type:null,_selectionRule:"Closest VizieR row",_candidateCount:v.data.length}}
function resultRow(o,c,r){if(!o)return"";const d=distance(o),z=+o.rvz_redshift,name=String(o.main_id||"Not available").trim(),ra=Number.isFinite(+o.ra)?(+o.ra).toFixed(6):r.ra.toFixed(6),de=Number.isFinite(+o.dec)?(+o.dec).toFixed(6):r.dec.toFixed(6),zd=z>0?`${z.toFixed(6)} / ${d?fmt(d/1e9,6)+" BLY":"distance unavailable"}`:"Not available",ts=[o.otype,o.sp_type].filter(Boolean).join(" / ")||"Not available",info=`Catalog: ${c}; Selection: ${safe(o._selectionRule||c+" row 1")}; Candidates: ${o._candidateCount||1}`,url=catalogUrl(c,name,ra,de),thumb=thumbnailUrl(ra,de);return`<tr><td><a class="object-link" href="${safe(url)}" target="_blank" rel="noopener noreferrer">${safe(name)} — ${safe(c)}</a><div class="thumbnail-container"><a href="${safe(url)}" target="_blank" rel="noopener noreferrer"><img class="catalog-thumbnail" src="${safe(thumb)}" alt="${safe(c)} preview"></a></div></td><td style="font-family:monospace">${ra} ${de}</td><td>${safe(zd)}</td><td>${safe(size(o,d))}</td><td>Not available in ${c}</td><td>${safe(ts)}</td><td>${info}</td></tr>`}'''
if source.count(old_result) != 1:
    raise RuntimeError("GV-0067 original result-row renderer was not found exactly once.")
source = source.replace(old_result, new_result, 1)

old_find = 'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);'
new_find = 'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);searchProgressStart();'
if source.count(old_find) != 1:
    raise RuntimeError("GV-0067 findGalaxy start was not found exactly once.")
source = source.replace(old_find, new_find, 1)

old_rows = 'const so=s?.[0]?{...s[0],_candidateCount:s.length}:null,no=n?.[0]?{...n[0],_candidateCount:n.length}:null;document.getElementById("resultBody").innerHTML=(resultRow(so,"SIMBAD",c)+resultRow(no,"NED",c))||\'<tr><td colspan="7">No SIMBAD or NED match found.</td></tr>\';'
new_rows = 'const so=s?.[0]?{...s[0],_candidateCount:s.length,_selectionRule:"SIMBAD row 1"}:null,no=n?.[0]?{...n[0],_candidateCount:n.length,_selectionRule:"NED row 1"}:null,vo=vizierRow(v,c);document.getElementById("resultBody").innerHTML=(resultRow(so,"SIMBAD",c)+resultRow(no,"NED",c)+resultRow(vo,"VizieR",c))||\'<tr><td colspan="7">No SIMBAD, NED, or VizieR match found.</td></tr>\';'
if source.count(old_rows) != 1:
    raise RuntimeError("GV-0067 two-row aggregation block was not found exactly once.")
source = source.replace(old_rows, new_rows, 1)

old_complete = 'save();status("Search complete. GV-0067 used SIMBAD row 1 and NED row 1 from the 30-arcsecond search window.")'
new_complete = 'save();searchProgressDone();status("Search complete. GV-0067 used SIMBAD row 1, NED row 1, and the closest VizieR row from the 30-arcsecond search window.")'
if source.count(old_complete) != 1:
    raise RuntimeError("GV-0067 completion status was not found exactly once.")
source = source.replace(old_complete, new_complete, 1)

old_fail = '}catch(e){status("Search failed: "+e.message);debug(String(e.stack||e))}}'
new_fail = '}catch(e){searchProgressDone(true);status("Search failed: "+e.message);debug(String(e.stack||e))}}'
if source.count(old_fail) != 1:
    raise RuntimeError("GV-0067 failure handler was not found exactly once.")
source = source.replace(old_fail, new_fail, 1)

# Verify required preserved and restored behavior remains in the generated file.
required = [
    '<select id="surveySelect" onchange="changeSurvey()"></select>',
    'window.aladin.setImageSurvey(id)',
    'document.addEventListener("visibilitychange",()=>document.hidden?save():restore("Viewer restored from saved tab state."))',
    'Waiting for final catalog aggregation…',
    '<div class="debug-wrap">',
    'SIMBAD row 1',
    'NED row 1',
    'Closest VizieR row',
    'class="object-link"',
    'class="catalog-thumbnail"',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"GV-0067 required preserved behavior missing: {token}")

if 'output.no_vertical_scroll()' not in globals() and output is None:
    raise RuntimeError("GV-0067 Colab no-scroll configuration is unavailable.")

ast.parse(source, filename="GV-0067-generated.py")
exec(compile(source, "GV-0067.py", "exec"))
