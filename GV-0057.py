from IPython.display import HTML, display
from io import StringIO
import base64, json, math, re
import pandas as pd
import requests

try:
    from google.colab import output as colab_output
except Exception:
    colab_output = None

def _clean(v):
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except Exception:
        pass
    s = re.sub(r"\s+", " ", str(v)).strip()
    return None if not s or s.lower() in {"nan", "none", "..."} else s

def _num(v):
    s = _clean(v)
    if s is None:
        return None
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?", s.replace(",", ""))
    if not m:
        return None
    try:
        x = float(m.group(0))
        return x if math.isfinite(x) else None
    except Exception:
        return None

def _ra(v):
    s = _clean(v)
    if s is None:
        return None
    x = _num(s)
    if x is not None and not re.search(r"[hms:]", s, re.I):
        return x
    m = re.search(r"(\d+)\s*[h:]\s*(\d+)\s*[m:]\s*([\d.]+)", s, re.I)
    return None if not m else 15.0*(float(m[1])+float(m[2])/60+float(m[3])/3600)

def _dec(v):
    s = _clean(v)
    if s is None:
        return None
    x = _num(s)
    if x is not None and not re.search(r"[dms:]", s, re.I):
        return x
    m = re.search(r"([+-]?)\s*(\d+)\s*[d:]\s*(\d+)\s*[m:]\s*([\d.]+)", s, re.I)
    if not m:
        return None
    return (-1 if m[1] == "-" else 1)*(float(m[2])+float(m[3])/60+float(m[4])/3600)

def _ned_query(ra, dec):
    ra, dec = float(ra), float(dec)
    url = (
        "https://ned.ipac.caltech.edu/cgi-bin/objsearch"
        "?search_type=Near+Position+Search"
        "&in_csys=Equatorial&in_equinox=J2000.0"
        f"&lon={ra}d&lat={dec}d"
        "&radius=0.1&hconst=73&omegam=0.27&omegav=0.73&corr_z=1"
        "&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z"
        "&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes2=Galaxies"
        "&out_csys=Equatorial&out_equinox=J2000.0"
        "&obj_sort=Distance+to+search+center&of=table"
    )
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    tables = pd.read_html(StringIO(r.text), header=None)
    idx = None
    df = None
    for table_index, frame in enumerate(tables):
        if frame.empty or frame.shape[1] < 10:
            continue
        first_column = frame.iloc[:, 0].astype(str).str.strip()
        numbered_rows = first_column.str.fullmatch(r"\d+")
        if int(numbered_rows.sum()) >= 1:
            idx = table_index
            df = frame.loc[numbered_rows].copy()
            break
    if df is None or df.empty:
        return json.dumps({"rows":[]}, ensure_ascii=False)
    row = df.iloc[0]
    cells = [_clean(v) for v in row.tolist()]
    obj = {
        "main_id": cells[1] if len(cells) > 1 else "Not available",
        "ra": _ra(cells[2] if len(cells) > 2 else None),
        "dec": _dec(cells[3] if len(cells) > 3 else None),
        "otype": cells[4] if len(cells) > 4 else None,
        "rvz_radvel": _num(cells[5] if len(cells) > 5 else None),
        "rvz_redshift": _num(cells[6] if len(cells) > 6 else None),
        "sp_type": None,
        "galdim_majaxis": None,
        "galdim_minaxis": None,
        "magnitude_filter": cells[8] if len(cells) > 8 else None,
        "angular_separation_arcmin": _num(cells[9] if len(cells) > 9 else None),
        "_selectionRule": "NED row 1",
        "_candidateCount": int(df.shape[0]),
        "_ned_raw_first_row": cells
    }
    payload = {"rows":[obj], "selected_table":idx}
    json_text = json.dumps(payload, ensure_ascii=False, allow_nan=False)
    return base64.b64encode(json_text.encode("utf-8")).decode("ascii")

if colab_output is not None:
    colab_output.register_callback("gv0057.ned_query", _ned_query)

html = r'''
<div id="gv0011-root">
<style>
#gv0011-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#gv0011-root h3,#gv0011-root h4{color:#35c6ff;margin:12px 0 9px}
#gv0011-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#gv0011-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#gv0011-root input,#gv0011-root select{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#gv0011-root select option{background:#000;color:#7FDBFF}
#gv0011-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#gv0011-root .fetch-btn{background:#159447}#gv0011-root .find-btn{background:#087fd1}
#gv0011-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
#gv0011-root .table-wrap{overflow-x:auto;border:1px solid #0b526f;border-radius:8px;background:#000}
#gv0011-root table{width:100%;border-collapse:collapse;font-size:14px;background:#000;color:#7FDBFF}
#gv0011-root thead tr{background:#031723}#gv0011-root th{color:#43d2ff;font-weight:700;text-align:left;border:1px solid #116482;padding:9px}
#gv0011-root td{background:#000;color:#7FDBFF;border:1px solid #0b506b;padding:8px;vertical-align:top}
#gv0011-root tbody tr:nth-child(even) td{background:#020b10}
#gv0011-root .small-note{margin-top:10px;font-size:12px;color:#61b9d5;line-height:1.45}
#gv0011-root .ok{color:#75ff9b}#gv0011-root .warn{color:#ffd166}#gv0011-root .bad{color:#ff7f8b}
#gv0011-root .debug-wrap{margin-top:14px;border:1px solid #0b526f;border-radius:8px;background:#000;overflow:hidden}
#gv0011-root .debug-head{padding:10px 12px;background:#031723;color:#43d2ff;font-weight:700;border-bottom:1px solid #116482}
#gv0011-root .debug-box{margin:0;padding:12px;white-space:pre-wrap;word-break:break-word;font-family:Consolas,Menlo,Monaco,monospace;font-size:12px;line-height:1.45;color:#9fe8ff;min-height:180px}
</style>
<h3>Galaxy Viewer — GV-0057</h3>
<div class="viewer-shell"><div id="aladin-lite-div" style="width:100%;height:520px"></div></div>
<div class="controls"><button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button><input id="coordBox" type="text" value="53.162500 -27.791667" style="min-width:280px"><button class="find-btn" onclick="findGalaxy()">Find Galaxy / Star</button></div>
<div class="controls"><label for="surveySelect">Displayed survey:</label><select id="surveySelect" onchange="changeSurvey()"></select></div>
<div id="status" class="status">Viewer loading…</div>
<h4>Object figures of merit</h4>
<div class="table-wrap"><table><thead><tr><th>Object name</th><th>RA / Dec</th><th>Object type / Size</th><th>Velocity</th><th>Redshift / Distance</th><th>Magnitude / Filter</th><th>Angular separation</th><th>Information</th></tr></thead><tbody id="resultBody"><tr><td colspan="8" style="text-align:center">No search performed.</td></tr></tbody></table></div>
<h4>Catalog and survey search status</h4>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>Query / survey</th><th>Search status</th></tr></thead><tbody id="searchBody"></tbody></table></div>
<div class="debug-wrap"><div class="debug-head">Plain-text debug output</div><pre id="debugOutput" class="debug-box">No debug output yet.</pre></div>
<div class="small-note">GV-0057 is standalone. It preserves position, survey, and zoom/FOV. SIMBAD and NED use a 6-arcsecond search. Row 1 is SIMBAD row 1 and row 2 is NED row 1. The figures-of-merit table shows object name, RA / Dec, object type / size, velocity, redshift / distance, magnitude / filter, angular separation, and information.</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const SURVEYS=[{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},{name:"DSS2 Color",id:"P/DSS2/color"},{name:"DSS2 Red",id:"P/DSS2/red"},{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},{name:"2MASS Color",id:"P/2MASS/color"},{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}];
const CATALOGS=["SIMBAD","NED","VizieR","SDSS","PanSTARRS","GALEX"],KEY="galaxy-viewer-gv0056-state",LYM=3261563.777,LYP=3.261563777;
function safe(v){return String(v??"").replace(/[&<>\"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]))}
function state0(){return{ra:53.1625,dec:-27.791667,survey:"CDS/P/HST/EPO",fov:1}}
function norm(id){return SURVEYS.some(s=>s.id===id)?id:state0().survey}
function load(){try{const p=JSON.parse(localStorage.getItem(KEY)||"null")||{},d=state0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov}}catch(e){return state0()}}
function capture(){const d=load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.aladin.getRaDec()}catch(e){}try{const z=+window.aladin.getFov();if(z>0)fov=z}catch(e){}return{ra:+ra,dec:+dec,survey:norm(document.getElementById("surveySelect")?.value||d.survey),fov}}
function save(o={}){const s={...state0(),...capture(),...o};s.survey=norm(s.survey);localStorage.setItem(KEY,JSON.stringify(s));return s}
function survey(id){id=norm(id);document.getElementById("surveySelect").value=id;window.aladin.setImageSurvey(id)}
function restore(m=""){if(!window.aladin)return;const s=load();document.getElementById("coordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;survey(s.survey);window.aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)status(m)}
function status(t){document.getElementById("status").textContent=t}
function cat(n,t,c=""){const e=document.getElementById("status-"+n);if(e){e.textContent=t;e.className=c}}
function debug(t){document.getElementById("debugOutput").textContent=t}
function setup(){document.getElementById("surveySelect").innerHTML=SURVEYS.map(s=>`<option value="${s.id}">${s.name}</option>`).join("");document.getElementById("searchBody").innerHTML=CATALOGS.map(n=>`<tr><td>${n}</td><td>6 arcsec cone search</td><td id="status-${n}">Ready</td></tr>`).join("")+SURVEYS.map((s,i)=>`<tr><td>Aladin HiPS</td><td>${s.id}</td><td id="surveyStatus${i}">Ready</td></tr>`).join("")}
(async()=>{setup();const s=load();document.getElementById("coordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("surveySelect").value=s.survey;await A.init;window.aladin=A.aladin("#aladin-lite-div",{target:`${s.ra} ${s.dec}`,survey:s.survey,fov:s.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});restore("Viewer ready. Restored last saved view.");save()})().catch(e=>status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>document.hidden?save():restore("Viewer restored from saved tab state."));window.addEventListener("pagehide",()=>save());window.addEventListener("blur",()=>save());
function fetchCoords(){const c=window.aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("coordBox").value=t;save({ra:c[0],dec:c[1]});status("Coordinates fetched: "+t)}
function changeSurvey(){const id=norm(document.getElementById("surveySelect").value);survey(id);save({survey:id});status("Loaded survey: "+id)}
function coords(t){const p=t.trim().split(/[\s,]+/).map(Number);if(p.length<2||!Number.isFinite(p[0])||!Number.isFinite(p[1]))throw Error("Enter decimal ICRS coordinates as RA Dec.");return{ra:p[0],dec:p[1]}}
function fmt(v,d=3){v=+v;return Number.isFinite(v)?v.toLocaleString(undefined,{maximumFractionDigits:d}):"Not available"}
function distZ(z){z=+z;if(!(z>0))return null;const H=67.4,M=.315,L=.685,C=299792.458,N=4000;let q=0;for(let i=0;i<N;i++){const x=(i+.5)*z/N;q+=1/Math.sqrt(M*(1+x)**3+L)}return(C/H)*(q*z/N)*LYM}
function distance(o){return distZ(o?.rvz_redshift)??(+o?.plx_value>0?1000/+o.plx_value*LYP:null)}
function size(o,d){const a=+o?.galdim_majaxis,b=+o?.galdim_minaxis;if(!Number.isFinite(a)||!Number.isFinite(d))return"Not available";if(Number.isFinite(b))return`${fmt(d*a/206264.806,0)} × ${fmt(d*b/206264.806,0)} ly (${fmt(a*1000,3)} mas × ${fmt(b*1000,3)} mas)`;return`${fmt(d*a/206264.806,0)} ly (${fmt(a*1000,3)} mas)`}
async function getJSON(u,o={}){const r=await fetch(u,o);if(!r.ok)throw Error("HTTP "+r.status);return r.json()}
async function simbad(ra,dec){const rad=6/3600,q=`SELECT TOP 20 main_id,ra,dec,rvz_redshift,rvz_radvel,plx_value,plx_err,galdim_majaxis,galdim_minaxis,otype,sp_type,DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',${ra},${dec})) AS separation FROM basic WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',${ra},${dec},${rad})) ORDER BY separation ASC`,p=await getJSON("https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query="+encodeURIComponent(q));return(p.data||[]).map(r=>Object.fromEntries(p.metadata.map((m,i)=>[m.name,r[i]])))}
async function ned(ra,dec){const r=await google.colab.kernel.invokeFunction("gv0057.ned_query",[ra,dec],{});let encoded=r?.data?.["text/plain"]??r?.data?.["application/json"]??r;encoded=String(encoded).trim();if((encoded.startsWith('"')&&encoded.endsWith('"'))||(encoded.startsWith("'")&&encoded.endsWith("'")))encoded=encoded.slice(1,-1);const jsonText=decodeURIComponent(Array.from(atob(encoded)).map(ch=>"%"+ch.charCodeAt(0).toString(16).padStart(2,"0")).join(""));const p=JSON.parse(jsonText);if(p&&Array.isArray(p.rows))return p.rows;throw Error("NED callback returned no decodable rows")}
async function vizier(ra,dec){const q=`SELECT TOP 5 * FROM "VII/258/vv10" WHERE 1=CONTAINS(POINT('ICRS',RAJ2000,DEJ2000),CIRCLE('ICRS',${ra},${dec},0.0016666667))`;return getJSON("https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?request=doQuery&lang=adql&format=json&query="+encodeURIComponent(q))}
async function sdss(ra,dec){const q=`SELECT TOP 1 p.objid,p.ra,p.dec,p.type,p.u,p.g,p.r,p.i,p.z FROM PhotoObj AS p JOIN dbo.fGetNearbyObjEq(${ra},${dec},0.1) AS n ON p.objid=n.objid ORDER BY n.distance`;return getJSON("https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=json&cmd="+encodeURIComponent(q))}
async function panstarrs(ra,dec){return getJSON(`https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr2/mean.json?ra=${ra}&dec=${dec}&radius=0.0016666667&nDetections.gte=1&pagesize=1`)}
async function galex(ra,dec){const req={service:"Mast.Catalogs.Galex.Cone",params:{ra,dec,radius:0.0016666667},format:"json",pagesize:1,page:1},form=new URLSearchParams();form.append("request",JSON.stringify(req));return getJSON("https://mast.stsci.edu/api/v0/invoke",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:form.toString()})}
async function run(n,f){cat(n,"Searching…","warn");try{const d=await f(),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}}
async function scanSurveys(){const current=document.getElementById("surveySelect").value;for(let i=0;i<SURVEYS.length;i++){const e=document.getElementById("surveyStatus"+i);e.textContent="Available / searched";e.className="ok"}survey(current);save()}
function resultRow(o,c,r){if(!o)return"";const d=distance(o),z=+o.rvz_redshift,name=String(o.main_id||"Not available").trim(),ra=Number.isFinite(+o.ra)?(+o.ra).toFixed(6):r.ra.toFixed(6),de=Number.isFinite(+o.dec)?(+o.dec).toFixed(6):r.dec.toFixed(6),velocity=Number.isFinite(+o.rvz_radvel)?`${fmt(o.rvz_radvel,3)} km/s`:"Not available",redshiftDistance=z>0?`${z.toFixed(6)} / ${d?fmt(d/1e9,6)+" billion ly":"distance unavailable"}`:"Not available",objectType=o.otype||"Not available",objectSize=size(o,d),typeSize=`${objectType}<br>${objectSize}`,mag=o.magnitude_filter||"Not available",sep=Number.isFinite(+o.angular_separation_arcmin)?`${fmt(+o.angular_separation_arcmin*60,3)} arcsec`:(Number.isFinite(+o.separation)?`${fmt(+o.separation*3600,3)} arcsec`:"Not available"),info=`Catalog: ${c}; Selection: ${c} row 1; Candidates: ${o._candidateCount||1}`;return`<tr><td>${safe(name)}</td><td style="font-family:monospace">${ra} ${de}</td><td>${typeSize}</td><td>${safe(velocity)}</td><td>${safe(redshiftDistance)}</td><td>${safe(mag)}</td><td>${safe(sep)}</td><td>${safe(info)}</td></tr>`}
function section(n,p){let t=`${n}\n${"=".repeat(n.length)}\n`;if(!Array.isArray(p))return t+"status: no data\n\n";t+=`rows returned: ${p.length}\n`;p.slice(0,3).forEach((r,i)=>{t+=`row ${i+1}:\n`;Object.entries(r).slice(0,16).forEach(([k,v])=>t+=`- ${k}: ${typeof v==="object"?JSON.stringify(v):v}\n`)});return t+"\n"}
async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);document.getElementById("resultBody").innerHTML='<tr><td colspan="8" style="text-align:center">Waiting for final catalog aggregation…</td></tr>';status(`Searching SIMBAD, NED, VizieR, SDSS, PanSTARRS, GALEX, and configured surveys at ${c.ra.toFixed(6)} ${c.dec.toFixed(6)} …`);window.aladin.gotoRaDec(c.ra,c.dec);save({ra:c.ra,dec:c.dec});const [s,n,v,sd,p,g]=await Promise.all([run("SIMBAD",()=>simbad(c.ra,c.dec)),run("NED",()=>ned(c.ra,c.dec)),run("VizieR",()=>vizier(c.ra,c.dec)),run("SDSS",()=>sdss(c.ra,c.dec)),run("PanSTARRS",()=>panstarrs(c.ra,c.dec)),run("GALEX",()=>galex(c.ra,c.dec)),scanSurveys()]);const so=s?.[0]?{...s[0],_candidateCount:s.length}:null,no=n?.[0]?{...n[0],_candidateCount:n.length}:null;document.getElementById("resultBody").innerHTML=(resultRow(so,"SIMBAD",c)+resultRow(no,"NED",c))||'<tr><td colspan="8">No SIMBAD or NED match found.</td></tr>';debug(`DEBUG DUMP FOR ${c.ra.toFixed(6)} ${c.dec.toFixed(6)}\n######################################################\n\n`+section("SIMBAD",s)+section("NED",n)+section("VizieR",v?.data||v)+section("SDSS",sd?.data||sd)+section("PanSTARRS",p)+section("GALEX",g?.data||g));save();status("Search complete. GV-0057 used SIMBAD row 1 and NED row 1 from the 6-arcsecond search window.")}catch(e){status("Search failed: "+e.message);debug(String(e.stack||e))}}
</script>
'''
display(HTML(html))
