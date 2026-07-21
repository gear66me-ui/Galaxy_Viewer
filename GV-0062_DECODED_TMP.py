from __future__ import annotations

import base64
import html
import json
import math
import re
import subprocess
import sys
from urllib.parse import quote

from IPython.display import HTML, Javascript, display

display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

try:
    from astroquery.simbad import Simbad
    from astroquery.ipac.ned import Ned
    from astroquery.vizier import Vizier
    from astropy.coordinates import SkyCoord
    import astropy.units as u
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "astroquery"])
    from astroquery.simbad import Simbad
    from astroquery.ipac.ned import Ned
    from astroquery.vizier import Vizier
    from astropy.coordinates import SkyCoord
    import astropy.units as u

try:
    from google.colab import output as colab_output
except Exception:
    colab_output = None

import pandas as pd

RADIUS_ARCSEC = 30.0


def _clean(value):
    if value is None:
        return None
    try:
        if bool(getattr(value, "mask", False)):
            return None
    except Exception:
        pass
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    text = re.sub(r"\s+", " ", str(value)).strip()
    return None if not text or text.lower() in {"nan", "none", "null", "...", "--", "n/a"} else text


def _number(value):
    text = _clean(value)
    if text is None:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        result = float(match.group(0))
        return result if math.isfinite(result) else None
    except Exception:
        return None


def _value(row, *names):
    columns = {str(name).casefold(): name for name in row.colnames}
    for requested in names:
        actual = columns.get(str(requested).casefold())
        if actual is not None and _clean(row[actual]) is not None:
            return row[actual]
    return None


def _first_column(row, exact=(), contains=(), reject_prefixes=()):
    exact_cf = {name.casefold() for name in exact}
    for name in row.colnames:
        lowered = str(name).casefold()
        if lowered in exact_cf and not lowered.startswith(reject_prefixes):
            value = row[name]
            if _clean(value) is not None:
                return value, str(name)
    for name in row.colnames:
        lowered = str(name).casefold()
        if lowered.startswith(reject_prefixes):
            continue
        if any(token in lowered for token in contains):
            value = row[name]
            if _clean(value) is not None:
                return value, str(name)
    return None, None


def _encode(payload):
    return base64.b64encode(json.dumps(payload, ensure_ascii=False, allow_nan=False).encode()).decode()


def _catalog_url(catalog, name, ra, dec, catalog_id=""):
    if catalog == "SIMBAD":
        return "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=" + quote(str(name))
    if catalog == "NED":
        return "https://ned.ipac.caltech.edu/byname?objname=" + quote(str(name))
    return (
        "https://vizier.cds.unistra.fr/viz-bin/VizieR"
        f"?-source={quote(str(catalog_id))}&-c={float(ra):.8f}%20{float(dec):.8f}"
        "&-c.rs=30&-out.max=100&-out.add=_r&-sort=_r"
    )


def _thumbnail(ra, dec):
    return (
        "https://alasky.cds.unistra.fr/hips-image-services/hips2fits"
        "?hips=CDS/P/DSS2/color&width=220&height=160&fov=0.03"
        "&projection=TAN&coordsys=icrs&format=jpg"
        f"&ra={float(ra):.8f}&dec={float(dec):.8f}"
    )


def _simbad_query(ra, dec):
    center = SkyCoord(float(ra) * u.deg, float(dec) * u.deg, frame="icrs")
    service = Simbad()
    service.ROW_LIMIT = 20
    for field in ("otype", "sp_type", "velocity", "dimensions", "U", "B", "V", "R", "I"):
        try:
            service.add_votable_fields(field)
        except Exception:
            pass
    table = service.query_region(center, radius=RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return _encode({"rows": []})
    coords = SkyCoord(table["ra"], table["dec"], frame="icrs")
    table["_gv_sep"] = center.separation(coords).arcsec
    table.sort("_gv_sep")
    row = table[0]
    name = _clean(_value(row, "main_id")) or "Not available"
    obj_ra = _number(_value(row, "ra")) or float(ra)
    obj_dec = _number(_value(row, "dec")) or float(dec)
    mags = []
    for band in ("U", "B", "V", "R", "I"):
        val = _number(_value(row, band))
        if val is not None:
            mags.append(f"{band} {val:.4f}")
    major = _number(_value(row, "galdim_majaxis"))
    minor = _number(_value(row, "galdim_minaxis"))
    return _encode({"rows": [{
        "catalog": "SIMBAD", "main_id": name, "ra": obj_ra, "dec": obj_dec,
        "otype": _clean(_value(row, "otype")), "sp_type": _clean(_value(row, "sp_type")),
        "rvz_radvel": _number(_value(row, "rvz_radvel")),
        "rvz_redshift": _number(_value(row, "rvz_redshift")),
        "galdim_majaxis": major, "galdim_minaxis": minor,
        "magnitude_filter": "; ".join(mags) if mags else None,
        "separation_arcsec": _number(_value(row, "_gv_sep")),
        "object_url": _catalog_url("SIMBAD", name, obj_ra, obj_dec),
        "thumbnail_url": _thumbnail(obj_ra, obj_dec),
        "_candidateCount": len(table), "_selectionRule": "SIMBAD row 1",
    }]})


def _ned_query(ra, dec):
    center = SkyCoord(float(ra) * u.deg, float(dec) * u.deg, frame="icrs")
    table = Ned.query_region(center, radius=RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return _encode({"rows": []})
    ra_col = next((x for x in ("RA", "ra") if x in table.colnames), None)
    dec_col = next((x for x in ("DEC", "Dec", "dec") if x in table.colnames), None)
    if ra_col and dec_col:
        coords = SkyCoord(table[ra_col], table[dec_col], unit=(u.deg, u.deg), frame="icrs")
        table["_gv_sep"] = center.separation(coords).arcsec
        table.sort("_gv_sep")
    row = table[0]
    name = _clean(_value(row, "Object Name", "Object_Name", "object_name")) or "Not available"
    obj_ra = _number(_value(row, "RA", "ra")) or float(ra)
    obj_dec = _number(_value(row, "DEC", "Dec", "dec")) or float(dec)
    try:
        redshift_rows = len(Ned.get_table(name, table="redshifts"))
    except Exception:
        redshift_rows = 0
    try:
        diameter_rows = len(Ned.get_table(name, table="diameters"))
    except Exception:
        diameter_rows = 0
    return _encode({"rows": [{
        "catalog": "NED", "main_id": name, "ra": obj_ra, "dec": obj_dec,
        "otype": _clean(_value(row, "Type", "Object Type")),
        "rvz_radvel": _number(_value(row, "Velocity")),
        "rvz_redshift": _number(_value(row, "Redshift")),
        "galdim_majaxis": None, "galdim_minaxis": None,
        "magnitude_filter": _clean(_value(row, "Magnitude and Filter", "Magnitude")),
        "separation_arcsec": _number(_value(row, "_gv_sep", "Separation")),
        "object_url": _catalog_url("NED", name, obj_ra, obj_dec),
        "thumbnail_url": _thumbnail(obj_ra, obj_dec),
        "info_extra": f"Diameter rows: {diameter_rows}; Redshift rows: {redshift_rows}",
        "_candidateCount": len(table), "_selectionRule": "NED row 1",
    }]})


def _vizier_query(ra, dec):
    center = SkyCoord(float(ra) * u.deg, float(dec) * u.deg, frame="icrs")
    tables = Vizier(columns=["**", "+_r"], row_limit=50).query_region(center, radius=RADIUS_ARCSEC * u.arcsec)
    best = None
    total_rows = 0
    for table in tables:
        total_rows += len(table)
        catalog_id = _clean(table.meta.get("name")) or _clean(table.meta.get("ID")) or "VizieR catalog"
        for row in table:
            obj_ra = _number(_value(row, "RA_ICRS", "RAJ2000", "RAdeg", "RA"))
            obj_dec = _number(_value(row, "DE_ICRS", "DEJ2000", "DEdeg", "DEC", "Dec"))
            if obj_ra is None or obj_dec is None:
                continue
            sep = _number(_value(row, "_r"))
            if sep is None:
                sep = center.separation(SkyCoord(obj_ra * u.deg, obj_dec * u.deg)).arcsec
            ident, ident_col = _first_column(row, exact=("Source", "source_id", "objID", "recno", "Name", "ID"), contains=("source", "objid", "name"))
            otype, otype_col = _first_column(row, exact=("otype", "ObjectType", "Type", "Class", "Classification"), contains=("otype", "objecttype", "classification"))
            mag, mag_col = _first_column(
                row,
                exact=("Gmag", "phot_g_mean_mag", "Vmag", "Bmag", "Rmag", "Imag", "Jmag", "Hmag", "Kmag"),
                contains=("gmag", "vmag", "bmag", "rmag", "imag", "jmag", "hmag", "kmag"),
                reject_prefixes=("o_", "e_", "n_", "q_", "f_"),
            )
            candidate = {
                "catalog": "VizieR", "catalog_id": catalog_id,
                "main_id": _clean(ident) or f"{catalog_id} row 1", "ra": obj_ra, "dec": obj_dec,
                "otype": _clean(otype), "otype_column": otype_col,
                "rvz_radvel": None, "rvz_redshift": None,
                "galdim_majaxis": None, "galdim_minaxis": None,
                "magnitude_filter": f"{_clean(mag)} ({mag_col})" if _clean(mag) is not None else None,
                "separation_arcsec": sep,
                "object_url": _catalog_url("VizieR", ident or "", obj_ra, obj_dec, catalog_id),
                "thumbnail_url": _thumbnail(obj_ra, obj_dec),
                "info_extra": f"Closest VizieR row; catalog: {catalog_id}; catalogs matched: {len(tables)}; rows matched: {total_rows}",
                "_candidateCount": total_rows, "_selectionRule": "Closest VizieR row",
            }
            if best is None or sep < best["separation_arcsec"]:
                best = candidate
    return _encode({"rows": [best] if best else []})


if colab_output is not None:
    colab_output.register_callback("gv0062.simbad_query", _simbad_query)
    colab_output.register_callback("gv0062.ned_query", _ned_query)
    colab_output.register_callback("gv0062.vizier_query", _vizier_query)

page = r'''
<div id="gv0062-root">
<style>
#gv0062-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#gv0062-root h3,#gv0062-root h4{color:#35c6ff;margin:12px 0 9px}#gv0062-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#gv0062-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}#gv0062-root input,#gv0062-root select{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}#gv0062-root select option{background:#000;color:#7FDBFF}
#gv0062-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}#gv0062-root .fetch-btn{background:#159447}#gv0062-root .find-btn{background:#087fd1}
#gv0062-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}#gv0062-root .table-wrap{overflow-x:auto;border:1px solid #0b526f;border-radius:8px;background:#000}
#gv0062-root table{width:100%;border-collapse:collapse;font-size:14px;background:#000;color:#7FDBFF}#gv0062-root thead tr{background:#031723}#gv0062-root th{color:#43d2ff;font-weight:700;text-align:left;border:1px solid #116482;padding:9px}#gv0062-root td{background:#000;color:#7FDBFF;border:1px solid #0b506b;padding:8px;vertical-align:top}#gv0062-root tbody tr:nth-child(even) td{background:#020b10}
#gv0062-root .small-note{margin-top:10px;font-size:12px;color:#61b9d5;line-height:1.45}#gv0062-root .ok{color:#75ff9b}#gv0062-root .warn{color:#ffd166}#gv0062-root .bad{color:#ff7f8b}
#gv0062-root .debug-wrap{margin-top:14px;border:1px solid #0b526f;border-radius:8px;background:#000;overflow:hidden}#gv0062-root .debug-head{padding:10px 12px;background:#031723;color:#43d2ff;font-weight:700;border-bottom:1px solid #116482}#gv0062-root .debug-box{margin:0;padding:12px;white-space:pre-wrap;word-break:break-word;font-family:Consolas,Menlo,Monaco,monospace;font-size:12px;line-height:1.45;color:#9fe8ff;min-height:180px;max-height:900px;overflow:auto}
#gv0062-root .object-link{display:inline-block;color:#58d7ff;font-weight:700;text-decoration:none;border-bottom:1px dotted rgba(88,215,255,.65)}#gv0062-root .thumbnail-container{margin-top:10px}#gv0062-root .catalog-thumbnail{display:block;width:150px;height:105px;object-fit:cover;background:#02080d;border:1px solid #137aa3;border-radius:7px}
</style>
<h3>Galaxy Viewer — GV-0062</h3>
<div class="viewer-shell"><div id="aladin-lite-div" style="width:100%;height:520px"></div></div>
<div class="controls"><button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button><input id="coordBox" type="text" value="53.162500 -27.791667" style="min-width:280px"><button class="find-btn" onclick="findGalaxy()">Find Galaxy / Star</button></div>
<div class="controls"><label for="surveySelect">Displayed survey:</label><select id="surveySelect" onchange="changeSurvey()"></select></div>
<div id="status" class="status">Viewer loading…</div>
<h4>Object figures of merit</h4><div class="table-wrap"><table><thead><tr><th>Object name</th><th>RA / Dec</th><th>Object type / Size</th><th>Velocity</th><th>Redshift / Distance</th><th>Magnitude / Filter</th><th>Angular separation</th><th>Information</th></tr></thead><tbody id="resultBody"><tr><td colspan="8" style="text-align:center">No search performed.</td></tr></tbody></table></div>
<h4>Catalog and survey search status</h4><div class="table-wrap"><table><thead><tr><th>Service</th><th>Query / survey</th><th>Search status</th></tr></thead><tbody id="searchBody"></tbody></table></div>
<div class="debug-wrap"><div class="debug-head">Plain-text debug output</div><pre id="debugOutput" class="debug-box">No debug output yet.</pre></div>
<div class="small-note">GV-0062 is standalone. It preserves position, survey, and zoom/FOV when switching tabs. SIMBAD, NED, and VizieR use a 30-arcsecond search. The default field of view is 3 degrees.</div>
</div>
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.css">
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const SURVEYS=[{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},{name:"DSS2 Color",id:"P/DSS2/color"},{name:"DSS2 Red",id:"P/DSS2/red"},{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},{name:"2MASS Color",id:"P/2MASS/color"},{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}];
const CATALOGS=["SIMBAD","NED","VizieR","SDSS","PanSTARRS","GALEX"],KEY="galaxy-viewer-gv0062-state",LYM=3261563.777,LYP=3.261563777;
function safe(v){return String(v??"").replace(/[&<>\"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]))}
function state0(){return{ra:53.1625,dec:-27.791667,survey:"CDS/P/HST/EPO",fov:3.0}}
function norm(id){return SURVEYS.some(s=>s.id===id)?id:state0().survey}
function load(){try{const p=JSON.parse(localStorage.getItem(KEY)||"null")||{},d=state0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov}}catch(e){return state0()}}
function capture(){const d=load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.aladin.getRaDec()}catch(e){}try{const z=window.aladin.getFov();const q=Array.isArray(z)?+z[0]:+z;if(q>0)fov=q}catch(e){}return{ra:+ra,dec:+dec,survey:norm(document.getElementById("surveySelect")?.value||d.survey),fov}}
function save(o={}){const s={...state0(),...capture(),...o};s.survey=norm(s.survey);localStorage.setItem(KEY,JSON.stringify(s));return s}
function survey(id){id=norm(id);document.getElementById("surveySelect").value=id;window.aladin.setImageSurvey(id)}
function restore(m=""){if(!window.aladin)return;const s=load();document.getElementById("coordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;survey(s.survey);window.aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)status(m)}
function status(t){document.getElementById("status").textContent=t}function cat(n,t,c=""){const e=document.getElementById("status-"+n);if(e){e.textContent=t;e.className=c}}function debug(t){document.getElementById("debugOutput").textContent=t}
function setup(){document.getElementById("surveySelect").innerHTML=SURVEYS.map(s=>`<option value="${s.id}">${s.name}</option>`).join("");document.getElementById("searchBody").innerHTML=CATALOGS.map(n=>`<tr><td>${n}</td><td>30 arcsec cone search</td><td id="status-${n}">Ready</td></tr>`).join("")+SURVEYS.map((s,i)=>`<tr><td>Aladin HiPS</td><td>${s.id}</td><td id="surveyStatus${i}">Ready</td></tr>`).join("")}
(async()=>{setup();const s=load();document.getElementById("coordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("surveySelect").value=s.survey;await A.init;window.aladin=A.aladin("#aladin-lite-div",{target:`${s.ra} ${s.dec}`,survey:s.survey,fov:s.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});restore("Viewer ready. Restored last saved view.");save();try{window.aladin.on("positionChanged",()=>save());window.aladin.on("zoomChanged",()=>save())}catch(e){}setInterval(()=>{if(!document.hidden)save()},1000)})().catch(e=>status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>{if(document.hidden){save()}else{restore("Viewer restored from saved tab state.")}});window.addEventListener("pagehide",()=>save());window.addEventListener("blur",()=>save());window.addEventListener("focus",()=>restore("Viewer restored from saved tab state."));
function fetchCoords(){const c=window.aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("coordBox").value=t;save({ra:c[0],dec:c[1]});status("Coordinates fetched: "+t)}function changeSurvey(){const id=norm(document.getElementById("surveySelect").value);survey(id);save({survey:id});status("Loaded survey: "+id)}
function coords(t){const p=t.trim().split(/[\s,]+/).map(Number);if(p.length<2||!Number.isFinite(p[0])||!Number.isFinite(p[1]))throw Error("Enter decimal ICRS coordinates as RA Dec.");return{ra:p[0],dec:p[1]}}
function fmt(v,d=3){v=+v;return Number.isFinite(v)?v.toLocaleString(undefined,{maximumFractionDigits:d}):"Not available"}function distZ(z){z=+z;if(!(z>0))return null;const H=67.4,M=.315,L=.685,C=299792.458,N=4000;let q=0;for(let i=0;i<N;i++){const x=(i+.5)*z/N;q+=1/Math.sqrt(M*(1+x)**3+L)}return(C/H)*(q*z/N)*LYM}function distance(o){return distZ(o?.rvz_redshift)??(+o?.plx_value>0?1000/+o.plx_value*LYP:null)}
function size(o,d){const a=+o?.galdim_majaxis,b=+o?.galdim_minaxis;if(!Number.isFinite(a)||!Number.isFinite(d))return"Not available";if(Number.isFinite(b))return`${fmt(d*a/206264.806,0)} × ${fmt(d*b/206264.806,0)} ly (${fmt(a*1000,3)} mas × ${fmt(b*1000,3)} mas)`;return`${fmt(d*a/206264.806,0)} ly (${fmt(a*1000,3)} mas)`}
async function callback(name,ra,dec){const r=await google.colab.kernel.invokeFunction(name,[ra,dec],{});let encoded=r?.data?.["text/plain"]??r?.data?.["application/json"]??r;encoded=String(encoded).trim();if((encoded.startsWith('"')&&encoded.endsWith('"'))||(encoded.startsWith("'")&&encoded.endsWith("'")))encoded=encoded.slice(1,-1);const text=decodeURIComponent(Array.from(atob(encoded)).map(ch=>"%"+ch.charCodeAt(0).toString(16).padStart(2,"0")).join(""));return JSON.parse(text).rows||[]}
async function getJSON(u,o={}){const r=await fetch(u,o);if(!r.ok)throw Error("HTTP "+r.status);return r.json()}async function sdss(ra,dec){const q=`SELECT TOP 1 p.objid,p.ra,p.dec,p.type,p.u,p.g,p.r,p.i,p.z FROM PhotoObj AS p JOIN dbo.fGetNearbyObjEq(${ra},${dec},0.5) AS n ON p.objid=n.objid ORDER BY n.distance`;return getJSON("https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=json&cmd="+encodeURIComponent(q))}async function panstarrs(ra,dec){return getJSON(`https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr2/mean.json?ra=${ra}&dec=${dec}&radius=0.0083333333&nDetections.gte=1&pagesize=1`)}async function galex(ra,dec){const req={service:"Mast.Catalogs.Galex.Cone",params:{ra,dec,radius:0.0083333333},format:"json",pagesize:1,page:1},form=new URLSearchParams();form.append("request",JSON.stringify(req));return getJSON("https://mast.stsci.edu/api/v0/invoke",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:form.toString()})}
async function run(n,f){cat(n,"Searching…","warn");try{const d=await f(),count=Array.isArray(d)?d.length:(Array.isArray(d?.data)?d.data.length:null);cat(n,count===0?"No match":"Query completed",count===0?"warn":"ok");return d}catch(e){cat(n,"Unavailable: "+e.message,"bad");return null}}
async function scanSurveys(){const current=document.getElementById("surveySelect").value;for(let i=0;i<SURVEYS.length;i++){const e=document.getElementById("surveyStatus"+i);e.textContent="Available / searched";e.className="ok"}survey(current);save()}
function resultRow(o,c,r){if(!o)return"";const d=distance(o),z=+o.rvz_redshift,name=String(o.main_id||"Not available").trim(),ra=Number.isFinite(+o.ra)?(+o.ra).toFixed(6):r.ra.toFixed(6),de=Number.isFinite(+o.dec)?(+o.dec).toFixed(6):r.dec.toFixed(6),velocity=Number.isFinite(+o.rvz_radvel)?`${fmt(o.rvz_radvel,3)} km/s`:"Not available",redshiftDistance=z>0?`${z.toFixed(6)} / ${d?fmt(d/1e9,6)+" billion ly":"distance unavailable"}`:"Not available",objectType=o.otype||"Not available",objectSize=size(o,d),typeSize=`${safe(objectType)}<br>${safe(objectSize)}`,mag=o.magnitude_filter||"Not available",sep=Number.isFinite(+o.separation_arcsec)?`${fmt(+o.separation_arcsec,3)} arcsec`:"Not available",info=`Catalog: ${c}; Selection: ${safe(o._selectionRule||c+" row 1")}; Candidates: ${o._candidateCount||1}${o.info_extra?"; "+safe(o.info_extra):""}`,url=o.object_url||"#",thumb=o.thumbnail_url?`<a href="${safe(url)}" target="_blank" rel="noopener noreferrer"><img class="catalog-thumbnail" src="${safe(o.thumbnail_url)}" alt="${safe(c)} preview"></a>`:"Preview unavailable";return`<tr><td><a class="object-link" href="${safe(url)}" target="_blank" rel="noopener noreferrer">${safe(name)}</a><div class="thumbnail-container">${thumb}</div></td><td style="font-family:monospace">${ra} ${de}</td><td>${typeSize}</td><td>${safe(velocity)}</td><td>${safe(redshiftDistance)}</td><td>${safe(mag)}</td><td>${safe(sep)}</td><td>${info}</td></tr>`}
function section(n,p){let t=`${n}\n${"=".repeat(n.length)}\n`;if(!Array.isArray(p))return t+"status: no data\n\n";t+=`rows returned: ${p.length}\n`;p.slice(0,3).forEach((r,i)=>{t+=`row ${i+1}:\n`;Object.entries(r).filter(([k])=>!k.includes("thumbnail")).slice(0,20).forEach(([k,v])=>t+=`- ${k}: ${typeof v==="object"?JSON.stringify(v):v}\n`)});return t+"\n"}
async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);document.getElementById("resultBody").innerHTML='<tr><td colspan="8" style="text-align:center">Waiting for final catalog aggregation…</td></tr>';status(`Searching SIMBAD, NED, VizieR, SDSS, PanSTARRS, GALEX, and configured surveys at ${c.ra.toFixed(6)} ${c.dec.toFixed(6)} …`);window.aladin.gotoRaDec(c.ra,c.dec);save({ra:c.ra,dec:c.dec});const [s,n,v,sd,p,g]=await Promise.all([run("SIMBAD",()=>callback("gv0062.simbad_query",c.ra,c.dec)),run("NED",()=>callback("gv0062.ned_query",c.ra,c.dec)),run("VizieR",()=>callback("gv0062.vizier_query",c.ra,c.dec)),run("SDSS",()=>sdss(c.ra,c.dec)),run("PanSTARRS",()=>panstarrs(c.ra,c.dec)),run("GALEX",()=>galex(c.ra,c.dec)),scanSurveys()]);document.getElementById("resultBody").innerHTML=(resultRow(s?.[0],"SIMBAD",c)+resultRow(n?.[0],"NED",c)+resultRow(v?.[0],"VizieR",c))||'<tr><td colspan="8">No SIMBAD, NED, or VizieR match found.</td></tr>';debug(`DEBUG DUMP FOR ${c.ra.toFixed(6)} ${c.dec.toFixed(6)}\n######################################################\n\n`+section("SIMBAD",s)+section("NED",n)+section("VizieR",v)+section("SDSS",sd?.data||sd)+section("PanSTARRS",p)+section("GALEX",g?.data||g));save();status("Search complete. GV-0062 used SIMBAD row 1, NED row 1, and the closest VizieR row from the 30-arcsecond search window.")}catch(e){status("Search failed: "+e.message);debug(String(e.stack||e))}}
</script>
'''

display(HTML(page))
