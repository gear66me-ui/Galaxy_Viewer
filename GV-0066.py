from __future__ import annotations

import urllib.request

from google.colab import output
from IPython.display import Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

SOURCE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/f085610ad94f22bacb30f23ea5a3bc605a9d619f/GV-0062_DECODED_TMP.py"

with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace("gv0062", "gv0066")
source = source.replace("GV-0062", "GV-0066")
source = source.replace('fov:3.0', 'fov:0.05')
source = source.replace('The default field of view is 3 degrees.', 'The default field of view is 3 arcminutes.')

source = source.replace(
    'function restore(m=""){if(!window.aladin)return;const s=load();document.getElementById("coordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;',
    'function restore(m=""){if(!window.aladin||window.gv0066CoordDirty||window.gv0066SurveySelecting)return;const s=load();'
)
source = source.replace(
    '(async()=>{setup();const s=load();',
    'document.addEventListener("input",e=>{if(e.target&&e.target.id==="coordBox")window.gv0066CoordDirty=true});document.addEventListener("pointerdown",e=>{if(e.target&&e.target.id==="surveySelect")window.gv0066SurveySelecting=true});document.addEventListener("touchstart",e=>{if(e.target&&e.target.id==="surveySelect")window.gv0066SurveySelecting=true},{passive:true});document.addEventListener("blur",e=>{if(e.target&&e.target.id==="surveySelect")setTimeout(()=>window.gv0066SurveySelecting=false,700)},true);(async()=>{setup();const s=load();'
)
source = source.replace(
    'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);',
    'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);window.gv0066CoordDirty=false;searchProgressStart();'
)

old_ned = '''    if ra_col and dec_col:
        coords = SkyCoord(table[ra_col], table[dec_col], unit=(u.deg, u.deg), frame="icrs")
        table["_gv_sep"] = center.separation(coords).arcsec
        table.sort("_gv_sep")'''
new_ned = '''    if ra_col and dec_col:
        separations = []
        for ned_row in table:
            ned_ra = _number(ned_row[ra_col])
            ned_dec = _number(ned_row[dec_col])
            if ned_ra is None or ned_dec is None:
                separations.append(float("inf"))
            else:
                ned_coord = SkyCoord(ned_ra * u.deg, ned_dec * u.deg, frame="icrs")
                separations.append(center.separation(ned_coord).arcsec)
        table["_gv_sep"] = separations
        table.sort("_gv_sep")'''
if source.count(old_ned) != 1:
    raise RuntimeError("GV-0066 NED block was not found exactly once.")
source = source.replace(old_ned, new_ned, 1)

if source.count('    service.ROW_LIMIT = 20') != 1:
    raise RuntimeError("GV-0066 SIMBAD row limit was not found exactly once.")
source = source.replace('    service.ROW_LIMIT = 20', '    service.ROW_LIMIT = -1', 1)
source = source.replace('"_candidateCount": len(table), "_selectionRule": "SIMBAD row 1",', '"_candidateCount": len(table), "_selectionRule": "Nearest SIMBAD row",', 1)

source = source.replace(
    '#gv0066-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}#gv0066-root .fetch-btn{background:#159447}#gv0066-root .find-btn{background:#087fd1}',
    '#gv0066-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}#gv0066-root .fetch-btn{background:#159447}#gv0066-root .find-btn{background:#087fd1}#gv0066-root .progress-shell{display:flex;align-items:center;gap:10px;margin-top:10px;padding:9px 11px;background:#02080d;border:1px solid #0d668a;border-radius:7px}#gv0066-root .progress-spinner{width:18px;height:18px;border:3px solid #164d63;border-top-color:#43d2ff;border-radius:50%;animation:gv0066spin .8s linear infinite;display:none;flex:0 0 auto}#gv0066-root .progress-track{height:12px;flex:1;background:#031723;border:1px solid #116482;border-radius:8px;overflow:hidden}#gv0066-root .progress-fill{width:0%;height:100%;background:#159447;transition:width .25s ease}#gv0066-root .progress-text{min-width:150px;color:#8be0ff;font-family:monospace;font-size:12px}@keyframes gv0066spin{to{transform:rotate(360deg)}}',
    1
)
source = source.replace(
    '<div class="controls"><button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button><input id="coordBox" type="text" value="53.162500 -27.791667" style="min-width:280px"><button class="find-btn" onclick="findGalaxy()">Find Galaxy / Star</button></div>',
    '<div class="controls"><button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button><input id="coordBox" type="text" value="53.162500 -27.791667" style="min-width:280px"><button class="find-btn" onclick="findGalaxy()">Find Galaxy / Star</button></div><div class="progress-shell"><div id="searchSpinner" class="progress-spinner"></div><div class="progress-track"><div id="searchProgressFill" class="progress-fill"></div></div><div id="searchProgressText" class="progress-text">Search idle</div></div>',
    1
)
source = source.replace(
    'function status(t){document.getElementById("status").textContent=t}',
    'let gv0066ProgressDone=0;const gv0066ProgressTotal=6;function searchProgressStart(){gv0066ProgressDone=0;document.getElementById("searchSpinner").style.display="block";document.getElementById("searchProgressFill").style.width="0%";document.getElementById("searchProgressText").textContent="Searching: 0 / 6"}function searchProgressStep(){gv0066ProgressDone=Math.min(gv0066ProgressTotal,gv0066ProgressDone+1);document.getElementById("searchProgressFill").style.width=`${100*gv0066ProgressDone/gv0066ProgressTotal}%`;document.getElementById("searchProgressText").textContent=`Searching: ${gv0066ProgressDone} / ${gv0066ProgressTotal}`}function searchProgressDone(failed=false){document.getElementById("searchSpinner").style.display="none";document.getElementById("searchProgressFill").style.width="100%";document.getElementById("searchProgressText").textContent=failed?"Search stopped with an error":"Search complete"}function status(t){document.getElementById("status").textContent=t}',
    1
)
source = source.replace(
    'function fetchCoords(){const c=window.aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("coordBox").value=t;save({ra:c[0],dec:c[1]});status("Coordinates fetched: "+t)}function changeSurvey(){const id=norm(document.getElementById("surveySelect").value);survey(id);save({survey:id});status("Loaded survey: "+id)}',
    'function fetchCoords(){const c=window.aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("coordBox").value=t;save({ra:c[0],dec:c[1]});status("Coordinates fetched: "+t)}function changeSurvey(){window.gv0066SurveySelecting=true;const id=norm(document.getElementById("surveySelect").value);survey(id);save({survey:id});status("Loaded survey: "+id);setTimeout(()=>window.gv0066SurveySelecting=false,700)}',
    1
)
if source.count('window.gv0066SurveySelecting=true;const id=norm(document.getElementById("surveySelect").value)') != 1:
    raise RuntimeError("GV-0066 survey selection lock was not applied exactly once.")

original_run = 'async function run(n,f){cat(n,"Searching…","warn");try{const d=await f(),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}}'
old_timed_run = 'async function run(n,f){cat(n,"Searching…","warn");try{const d=await Promise.race([f(),new Promise((_,reject)=>setTimeout(()=>reject(Error("Timed out after 45 seconds")),45000))]),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}finally{searchProgressStep()}}'
new_timed_run = 'async function run(n,f){cat(n,"Searching…","warn");try{const timeoutMs=n==="VizieR"?180000:45000;const d=await Promise.race([f(),new Promise((_,reject)=>setTimeout(()=>reject(Error(`Timed out after ${timeoutMs/1000} seconds`)),timeoutMs))]),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}finally{searchProgressStep()}}'
if source.count(original_run) == 1:
    source = source.replace(original_run, new_timed_run, 1)
elif source.count(old_timed_run) == 1:
    source = source.replace(old_timed_run, new_timed_run, 1)
else:
    raise RuntimeError("GV-0066 search timeout function was not found exactly once.")
if source.count('n==="VizieR"?180000:45000') != 1:
    raise RuntimeError("GV-0066 VizieR 180-second timeout was not applied exactly once.")

source = source.replace(
    'save();status("Search complete. GV-0066 used SIMBAD row 1, NED row 1, and the closest VizieR row from the 30-arcsecond search window.")',
    'save();searchProgressDone();window.gv0066CoordDirty=true;status("Search complete. GV-0066 used the nearest SIMBAD row, NED row 1, and the closest VizieR row from the 30-arcsecond search window.")',
    1
)
if source.count('searchProgressDone();window.gv0066CoordDirty=true;status("Search complete.') != 1:
    raise RuntimeError("GV-0066 post-search coordinate register release was not applied exactly once.")
source = source.replace(
    '}catch(e){status("Search failed: "+e.message);debug(String(e.stack||e))}}',
    '}catch(e){searchProgressDone(true);status("Search failed: "+e.message);debug(String(e.stack||e))}}',
    1
)

exec(compile(source, "GV-0066.py", "exec"))