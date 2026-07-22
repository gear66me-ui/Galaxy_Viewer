from __future__ import annotations

import csv
import io
import json
import math
import random
import time
import urllib.parse
import urllib.request
from collections import deque
from typing import Any

from google.colab import output
from IPython.display import HTML, Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

C_KMS = 299792.458
RECENT_KEYS: deque[str] = deque(maxlen=100)


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _float(value: Any) -> float | None:
    try:
        text = _clean(value)
        if not text or text in {"?", "nan", "NaN", "9.99", "999", "999.0", "--"}:
            return None
        number = float(text)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def _pick(row: dict[str, Any], *names: str) -> str:
    lowered = {str(key).lower(): value for key, value in row.items()}
    for name in names:
        value = lowered.get(name.lower())
        if _clean(value):
            return _clean(value)
    return ""


def _table_rows(url: str, *, data: bytes | None = None, timeout: int = 12) -> list[dict[str, str]]:
    request = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": "GalaxyViewer/14", "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if len(lines) < 2:
        return []
    return list(csv.DictReader(io.StringIO("\n".join(lines))))


def _vizier_rows(params: dict[str, str], timeout: int = 12) -> list[dict[str, str]]:
    query = urllib.parse.urlencode(params)
    url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?" + query
    request = urllib.request.Request(url, headers={"User-Agent": "GalaxyViewer/14"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if len(lines) < 2:
        return []
    return list(csv.DictReader(io.StringIO("\n".join(lines)), delimiter="\t"))


def _coord_from_row(row: dict[str, Any]) -> tuple[float, float]:
    ra_text = _pick(row, "_RAJ2000", "RAJ2000", "RA2000", "ra")
    dec_text = _pick(row, "_DEJ2000", "DEJ2000", "DE2000", "dec")
    if not ra_text or not dec_text:
        raise ValueError("No usable J2000/ICRS coordinates returned.")
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    if ":" in ra_text or " " in ra_text:
        coord = SkyCoord(f"{ra_text} {dec_text}", unit=(u.hourangle, u.deg), frame="icrs")
    else:
        coord = SkyCoord(float(ra_text) * u.deg, float(dec_text) * u.deg, frame="icrs")
    return float(coord.ra.deg), float(coord.dec.deg)


def _diameters_from_log(log_d25: float | None, log_r25: float | None) -> tuple[float | None, float | None]:
    if log_d25 is None or log_d25 >= 9:
        return None, None
    major = 0.1 * (10.0 ** log_d25)
    if log_r25 is None or log_r25 >= 9:
        return major, None
    return major, major / (10.0 ** log_r25)


def _distance_from_redshift(z: float | None) -> tuple[float | None, str]:
    if z is None or z <= 0:
        return None, "Not available"
    try:
        from astropy.cosmology import Planck18
        distance_mpc = float(Planck18.luminosity_distance(z).value)
        distance_bly = distance_mpc * 3.26156e6 / 1.0e9
        return distance_mpc, f"{distance_bly:.6f} billion ly"
    except Exception:
        distance_mpc = (C_KMS * z) / 67.66
        distance_bly = distance_mpc * 3.26156e6 / 1.0e9
        return distance_mpc, f"{distance_bly:.6f} billion ly (low-z estimate)"


def _physical_size_kly(major: float | None, minor: float | None, distance_mpc: float | None) -> str:
    if major is None or distance_mpc is None or distance_mpc <= 0:
        return "Not available"

    def axis_kly(arcmin: float) -> float:
        return distance_mpc * 1.0e3 * math.tan(math.radians(arcmin / 60.0)) * 3.26156

    if minor is None:
        return f"{axis_kly(major):,.1f} thousand ly — derived"
    return f"{axis_kly(major):,.1f} × {axis_kly(minor):,.1f} thousand ly — derived"


def _format_size(major: float | None, minor: float | None) -> str:
    if major is None:
        return "Not available"
    if minor is None:
        return f"{major:.3f} arcmin"
    return f"{major:.3f} × {minor:.3f} arcmin"


def _fov_for_size(major: float | None, fallback: float = 0.18) -> float:
    if major is None or major <= 0:
        return fallback
    return max(0.035, min(4.0, major * 3.2 / 60.0))


def _row_to_result(
    row: dict[str, Any],
    *,
    catalog: str,
    name: str,
    source: str,
    major_arcmin: float | None,
    minor_arcmin: float | None,
    morphology: str,
    magnitude: float | None,
    velocity_kms: float | None,
    attempts: int,
    elapsed: float,
) -> dict[str, Any]:
    ra, dec = _coord_from_row(row)
    z = velocity_kms / C_KMS if velocity_kms is not None and velocity_kms > 0 else None
    distance_mpc, distance_text = _distance_from_redshift(z)
    redshift_distance = f"{z:.8f} / {distance_text}" if z is not None else "Not available / Not available"
    key = f"{catalog}:{name}:{ra:.6f}:{dec:.6f}"
    return {
        "ok": True,
        "key": key,
        "name": name or "Unnamed galaxy",
        "catalog": catalog,
        "source": source,
        "ra": ra,
        "dec": dec,
        "fov": _fov_for_size(major_arcmin),
        "survey_id": "P/DSS2/color",
        "morphology": morphology or "Not available",
        "angular_size": _format_size(major_arcmin, minor_arcmin),
        "redshift_distance": redshift_distance,
        "velocity_kms": velocity_kms,
        "physical_size": _physical_size_kly(major_arcmin, minor_arcmin, distance_mpc),
        "magnitude": "Not available" if magnitude is None else f"{magnitude:.3f}",
        "attempts": attempts,
        "elapsed_seconds": elapsed,
    }


def _query_hyperleda() -> dict[str, Any]:
    started = time.monotonic()
    errors: list[str] = []
    for attempt in range(1, 9):
        ra0 = random.uniform(0.0, 360.0)
        dec0 = math.degrees(math.asin(random.uniform(-1.0, 1.0)))
        try:
            rows = _vizier_rows(
                {
                    "-source": "VII/237/pgc",
                    "-c": f"{ra0:.8f} {dec0:.8f}",
                    "-c.rm": "90",
                    "-out": "PGC,RAJ2000,DEJ2000,OType,MType,logD25,logR25",
                    "-out.max": "120",
                }
            )
        except Exception as exc:
            errors.append(str(exc))
            continue
        candidates: list[dict[str, Any]] = []
        for row in rows:
            pgc = _pick(row, "PGC")
            if not pgc:
                continue
            major, minor = _diameters_from_log(
                _float(_pick(row, "logD25")),
                _float(_pick(row, "logR25")),
            )
            try:
                result = _row_to_result(
                    row,
                    catalog="HyperLEDA",
                    name=f"PGC {pgc}",
                    source="HyperLEDA VII/237 via VizieR random-sky cone",
                    major_arcmin=major,
                    minor_arcmin=minor,
                    morphology=_pick(row, "MType", "OType"),
                    magnitude=None,
                    velocity_kms=None,
                    attempts=attempt,
                    elapsed=time.monotonic() - started,
                )
            except Exception:
                continue
            if result["key"] not in RECENT_KEYS:
                candidates.append(result)
        if candidates:
            return random.choice(candidates)
    raise RuntimeError("HyperLEDA returned no usable non-repeating galaxy. " + " | ".join(errors[-3:]))


def _query_rc3() -> dict[str, Any]:
    started = time.monotonic()
    errors: list[str] = []
    for attempt in range(1, 9):
        recno = random.randint(1, 23011)
        try:
            rows = _vizier_rows(
                {
                    "-source": "VII/155/rc3",
                    "recno": str(recno),
                    "-out.all": "",
                    "-out.max": "1",
                }
            )
        except Exception as exc:
            errors.append(str(exc))
            continue
        if not rows:
            continue
        row = rows[0]
        major, minor = _diameters_from_log(
            _float(_pick(row, "D25", "logD25")),
            _float(_pick(row, "R25", "logR25")),
        )
        velocity = _float(_pick(row, "V3K", "cz", "V21"))
        name = _pick(row, "name", "altname", "PGC") or f"RC3 record {recno}"
        if name.isdigit():
            name = f"PGC {name}"
        try:
            result = _row_to_result(
                row,
                catalog="RC3",
                name=name,
                source="Third Reference Catalogue of Bright Galaxies VII/155 via VizieR",
                major_arcmin=major,
                minor_arcmin=minor,
                morphology=_pick(row, "type", "T"),
                magnitude=_float(_pick(row, "BT", "Bmag")),
                velocity_kms=velocity,
                attempts=attempt,
                elapsed=time.monotonic() - started,
            )
        except Exception as exc:
            errors.append(str(exc))
            continue
        if result["key"] not in RECENT_KEYS:
            return result
    raise RuntimeError("RC3 returned no usable non-repeating galaxy. " + " | ".join(errors[-3:]))


def _query_arp() -> dict[str, Any]:
    started = time.monotonic()
    errors: list[str] = []
    for attempt in range(1, 9):
        recno = random.randint(1, 592)
        try:
            rows = _vizier_rows(
                {
                    "-source": "VII/192/arplist",
                    "recno": str(recno),
                    "-out.all": "",
                    "-out.max": "1",
                }
            )
        except Exception as exc:
            errors.append(str(exc))
            continue
        if not rows:
            continue
        row = rows[0]
        arp = _pick(row, "Arp")
        common = _pick(row, "Name")
        name = f"Arp {arp}" + (f" — {common}" if common else "")
        try:
            result = _row_to_result(
                row,
                catalog="Arp",
                name=name,
                source="Arp Peculiar Galaxies VII/192 via VizieR",
                major_arcmin=_float(_pick(row, "dim1")),
                minor_arcmin=_float(_pick(row, "dim2")),
                morphology=_pick(row, "MType") or "Peculiar galaxy",
                magnitude=_float(_pick(row, "VT")),
                velocity_kms=None,
                attempts=attempt,
                elapsed=time.monotonic() - started,
            )
        except Exception as exc:
            errors.append(str(exc))
            continue
        if result["key"] not in RECENT_KEYS:
            return result
    raise RuntimeError("Arp returned no usable non-repeating galaxy. " + " | ".join(errors[-3:]))


def _catalog_callback(catalog: str) -> str:
    try:
        result = _query_arp() if catalog == "Arp" else _query_rc3() if catalog == "RC3" else _query_hyperleda()
        RECENT_KEYS.append(result["key"])
    except Exception as exc:
        result = {"ok": False, "catalog": catalog, "error": str(exc)}
    return json.dumps(result, ensure_ascii=False)


def viewer14_arp_callback() -> str:
    return _catalog_callback("Arp")


def viewer14_rc3_callback() -> str:
    return _catalog_callback("RC3")


def viewer14_hyperleda_callback() -> str:
    return _catalog_callback("HyperLEDA")


def viewer14_get_info_callback(ra: float, dec: float) -> str:
    started = time.monotonic()
    try:
        ra = float(ra)
        dec = float(dec)
        radius_deg = 30.0 / 3600.0
        query = (
            "SELECT TOP 1 main_id, ra, dec, otype, rvz_redshift, rvz_radvel\n"
            "FROM basic\n"
            f"WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {ra:.10f}, {dec:.10f}, {radius_deg:.12f})) = 1"
        )
        payload = urllib.parse.urlencode(
            {"request": "doQuery", "lang": "adql", "format": "csv", "query": query}
        ).encode("utf-8")
        rows = _table_rows(
            "https://simbad.cds.unistra.fr/simbad/sim-tap/sync",
            data=payload,
            timeout=20,
        )
        if not rows:
            raise RuntimeError("SIMBAD returned no object within 30 arcseconds.")
        row = rows[0]
        obj_ra = _float(_pick(row, "ra"))
        obj_dec = _float(_pick(row, "dec"))
        if obj_ra is None or obj_dec is None:
            raise RuntimeError("SIMBAD returned an object without usable coordinates.")
        z = _float(_pick(row, "rvz_redshift"))
        velocity = _float(_pick(row, "rvz_radvel"))
        if z is None and velocity is not None and velocity > 0:
            z = velocity / C_KMS
        distance_mpc, distance_text = _distance_from_redshift(z)
        redshift_distance = f"{z:.8f} / {distance_text}" if z is not None else "Not available / Not available"
        result = {
            "ok": True,
            "name": _pick(row, "main_id") or "Unnamed SIMBAD object",
            "catalog": "SIMBAD",
            "source": "SIMBAD first row in a 30 arcsecond ICRS cone",
            "ra": obj_ra,
            "dec": obj_dec,
            "fov": 0.18,
            "survey_id": "P/DSS2/color",
            "morphology": _pick(row, "otype") or "Not available",
            "angular_size": "Not available",
            "redshift_distance": redshift_distance,
            "velocity_kms": velocity,
            "physical_size": "Not available",
            "magnitude": "Not available",
            "attempts": 1,
            "elapsed_seconds": time.monotonic() - started,
            "distance_mpc": distance_mpc,
        }
    except Exception as exc:
        result = {"ok": False, "catalog": "SIMBAD", "error": str(exc)}
    return json.dumps(result, ensure_ascii=False)


output.register_callback("viewer14.randomArp", viewer14_arp_callback)
output.register_callback("viewer14.randomRC3", viewer14_rc3_callback)
output.register_callback("viewer14.randomHyperLEDA", viewer14_hyperleda_callback)
output.register_callback("viewer14.getInfo", viewer14_get_info_callback)

page = r'''<div id="viewer14-root">
<style>
#viewer14-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#viewer14-root h3{color:#35c6ff;margin:12px 0 9px}
#viewer14-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#viewer14-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#viewer14-root input,#viewer14-root select{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#viewer14-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#viewer14-root button:disabled{opacity:.55;cursor:wait}
#viewer14-root .fetch-btn{background:#159447}
#viewer14-root .info-btn{background:#0b78b5}
#viewer14-root .random-btn{background:#8a4fd4}
#viewer14-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
#viewer14-root .survey-menu-wrap{position:relative;display:inline-block;min-width:290px}
#viewer14-root .survey-menu-button{width:100%;text-align:left;background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;font-weight:400}
#viewer14-root .survey-menu{display:none;position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:999999;background:#000;border:1px solid #169ac7;border-radius:8px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.75)}
#viewer14-root .survey-menu.open{display:block}
#viewer14-root .survey-option{display:block;width:100%;text-align:left;background:#000;color:#7FDBFF;border:0;border-bottom:1px solid #0b526f;border-radius:0;padding:12px;font-size:16px;font-weight:400}
#viewer14-root .survey-option:last-child{border-bottom:0}
#viewer14-root .catalog-progress{display:flex;flex-direction:column;gap:5px;flex:1;min-width:260px;max-width:430px}
#viewer14-root .progress-track{height:13px;background:#031018;border:1px solid #0d668a;border-radius:8px;overflow:hidden}
#viewer14-root .progress-fill{height:100%;width:0;background:linear-gradient(90deg,#159447,#35c6ff);transition:width .22s linear}
#viewer14-root .progress-fill.active{animation:viewer14pulse 1.15s ease-in-out infinite}
#viewer14-root .progress-text{color:#ffd84d;font-family:monospace;font-size:14px;min-height:17px}
@keyframes viewer14pulse{0%{filter:brightness(.7)}50%{filter:brightness(1.5)}100%{filter:brightness(.7)}}
</style>
<h3>Galaxy Viewer — VIEWER-14</h3>
<div class="viewer-shell"><div id="viewer14-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button id="viewer14RandomButton" class="random-btn" onclick="viewer14RandomGalaxy()">Random Galaxy</button>
<button class="fetch-btn" onclick="viewer14FetchCoords()">Fetch Coordinates</button>
<input id="viewer14CoordBox" type="text" value="53.162500 -27.791667" readonly style="min-width:280px">
<button id="viewer14InfoButton" class="info-btn" onclick="viewer14GetInfo()">Get Info</button>
</div>
<div class="controls">
<label>Random galaxy library:</label>
<select id="viewer14CatalogMode" onchange="viewer14Save({catalogMode:this.value})">
<option value="interesting">Interesting Mix — 70% interesting / 30% random</option>
<option value="all">All Catalogs — equal random</option>
<option value="Arp">Arp peculiar galaxies</option>
<option value="RC3">RC3 bright galaxies</option>
<option value="HyperLEDA">HyperLEDA deep random</option>
</select>
</div>
<div class="controls">
<label>Displayed survey:</label>
<div class="survey-menu-wrap">
<input type="hidden" id="viewer14SurveySelect">
<button type="button" id="viewer14SurveyButton" class="survey-menu-button" onclick="viewer14ToggleSurveyMenu(event)">DSS2 Color ▾</button>
<div id="viewer14SurveyMenu" class="survey-menu"></div>
</div>
<div class="catalog-progress">
<div class="progress-track"><div id="viewer14ProgressFill" class="progress-fill"></div></div>
<div id="viewer14ProgressText" class="progress-text">Catalog fetch idle.</div>
</div>
</div>
<div id="viewer14Status" class="status">Viewer loading…</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const VIEWER14_SURVEYS=[
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"JWST Outreach Color",id:"CDS/P/JWST/EPO"},
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];
const VIEWER14_KEY="galaxy-viewer-viewer14-state";
function viewer14State0(){return{ra:53.1625,dec:-27.791667,survey:"P/DSS2/color",fov:1,catalogMode:"interesting"}}
function viewer14Norm(id){return VIEWER14_SURVEYS.some(s=>s.id===id)?id:viewer14State0().survey}
function viewer14Load(){try{const p=JSON.parse(localStorage.getItem(VIEWER14_KEY)||"null")||{},d=viewer14State0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:viewer14Norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov,catalogMode:["interesting","all","Arp","RC3","HyperLEDA"].includes(p.catalogMode)?p.catalogMode:d.catalogMode}}catch(e){return viewer14State0()}}
function viewer14Capture(){const d=viewer14Load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.viewer14Aladin.getRaDec()}catch(e){}try{const z=+window.viewer14Aladin.getFov();if(z>0)fov=z}catch(e){}return{ra:+ra,dec:+dec,survey:viewer14Norm(document.getElementById("viewer14SurveySelect")?.value||d.survey),fov,catalogMode:document.getElementById("viewer14CatalogMode")?.value||d.catalogMode}}
function viewer14Save(o={}){const s={...viewer14State0(),...viewer14Capture(),...o};s.survey=viewer14Norm(s.survey);localStorage.setItem(VIEWER14_KEY,JSON.stringify(s));window.VIEWER14_STATE=s;return s}
function viewer14Status(t){document.getElementById("viewer14Status").textContent=t}
function viewer14Setup(){document.getElementById("viewer14SurveyMenu").innerHTML=VIEWER14_SURVEYS.map(s=>`<button type="button" class="survey-option" onclick="viewer14ChooseSurvey('${s.id}',event)">${s.name}</button>`).join("")}
function viewer14Survey(id){id=viewer14Norm(id);document.getElementById("viewer14SurveySelect").value=id;const item=VIEWER14_SURVEYS.find(s=>s.id===id);document.getElementById("viewer14SurveyButton").textContent=(item?item.name:id)+" ▾";window.viewer14Aladin.setImageSurvey(id)}
function viewer14ToggleSurveyMenu(e){e.stopPropagation();document.getElementById("viewer14SurveyMenu").classList.toggle("open")}
function viewer14ChooseSurvey(id,e){e.stopPropagation();viewer14Survey(id);viewer14Save({survey:id});document.getElementById("viewer14SurveyMenu").classList.remove("open");viewer14Status("Loaded survey: "+id)}
document.addEventListener("click",()=>{const m=document.getElementById("viewer14SurveyMenu");if(m)m.classList.remove("open")})
function viewer14Parse(v){if(v==null)return v;if(typeof v!=="string")return v;v=v.trim();if(v.startsWith("'")&&v.endsWith("'"))v=v.slice(1,-1).replace(/\\'/g,"'").replace(/\\\\/g,"\\");try{return JSON.parse(v)}catch(_){return v}}
function viewer14Result(r){const d=r?.data??r;if(d&&typeof d==="object"&&d.ok!==undefined)return d;if(d&&typeof d==="object")return viewer14Parse(d["application/json"]??d["text/plain"]??Object.values(d)[0]);return viewer14Parse(d)}
function viewer14ProgressStart(catalog){const fill=document.getElementById("viewer14ProgressFill"),text=document.getElementById("viewer14ProgressText");clearInterval(window.viewer14ProgressTimer);fill.classList.add("active");fill.style.width="8%";text.textContent=`Fetching data from ${catalog}…`;let p=8;window.viewer14ProgressTimer=setInterval(()=>{p=Math.min(92,p+(p<55?7:p<80?3:1));fill.style.width=p+"%"},350)}
function viewer14ProgressDone(catalog,detail){clearInterval(window.viewer14ProgressTimer);const fill=document.getElementById("viewer14ProgressFill"),text=document.getElementById("viewer14ProgressText");fill.classList.remove("active");fill.style.width="100%";text.textContent=`${catalog} complete${detail?" — "+detail:""}`;setTimeout(()=>{fill.style.width="0%"},1200)}
function viewer14ProgressFail(catalog){clearInterval(window.viewer14ProgressTimer);const fill=document.getElementById("viewer14ProgressFill"),text=document.getElementById("viewer14ProgressText");fill.classList.remove("active");fill.style.width="100%";text.textContent=`${catalog} failed; trying another catalog…`}
function viewer14Panel(g,survey,fov){const v=(g.velocity_kms!==null&&g.velocity_kms!==undefined&&Number.isFinite(Number(g.velocity_kms)))?`${Number(g.velocity_kms).toLocaleString(undefined,{maximumFractionDigits:1})} km/s`:"Not available";return `RANDOM GALAXY FIGURES OF MERIT\n\nObject: ${g.name}\nSource catalog: ${g.catalog}\nICRS coordinates: ${Number(g.ra).toFixed(6)} ${Number(g.dec).toFixed(6)}\nMorphological type: ${g.morphology||"Not available"}\nAngular size: ${g.angular_size||"Not available"}\nRedshift / Distance: ${g.redshift_distance||"Not available / Not available"}\nRadial velocity: ${v}\nPhysical size: ${g.physical_size||"Not available"}\nMagnitude: ${g.magnitude||"Not available"}\nDisplayed survey: ${survey}\nField of view: ${fov.toFixed(3)}°\nCatalog requests: ${g.attempts||1}\nCatalog elapsed time: ${Number(g.elapsed_seconds||0).toFixed(2)} s\nData source: ${g.source}`}
function viewer14ShowGalaxy(g){const ra=Number(g.ra),dec=Number(g.dec),fov=Number(g.fov),survey=viewer14Norm(g.survey_id||"P/DSS2/color");document.getElementById("viewer14CoordBox").value=`${ra.toFixed(6)} ${dec.toFixed(6)}`;viewer14Survey(survey);window.viewer14Aladin.gotoRaDec(ra,dec);const z=()=>{try{window.viewer14Aladin.setFoV(fov)}catch(e){}};z();setTimeout(z,150);setTimeout(z,500);viewer14Save({ra,dec,survey,fov});viewer14Status(viewer14Panel(g,survey,fov))}
function viewer14CatalogOrder(){const mode=document.getElementById("viewer14CatalogMode").value;if(["Arp","RC3","HyperLEDA"].includes(mode))return[mode];if(mode==="all")return[...['Arp','RC3','HyperLEDA']].sort(()=>Math.random()-.5);const r=Math.random();const first=r<.45?"Arp":r<.70?"RC3":"HyperLEDA";return[first,...["Arp","RC3","HyperLEDA"].filter(x=>x!==first).sort(()=>Math.random()-.5)]}
function viewer14CallbackName(c){return c==="Arp"?"viewer14.randomArp":c==="RC3"?"viewer14.randomRC3":"viewer14.randomHyperLEDA"}
async function viewer14RandomGalaxy(){const b=document.getElementById("viewer14RandomButton");b.disabled=true;const failures=[];try{for(const catalog of viewer14CatalogOrder()){viewer14ProgressStart(catalog);viewer14Status(`Fetching a random galaxy from ${catalog}…`);try{const r=await google.colab.kernel.invokeFunction(viewer14CallbackName(catalog),[],{});const g=viewer14Result(r);if(!g||g.ok!==true)throw Error(g?.error||"Lookup failed");viewer14ProgressDone(catalog,`${Number(g.elapsed_seconds||0).toFixed(2)} s, ${g.attempts||1} request(s)`);viewer14ShowGalaxy(g);return}catch(e){failures.push(`${catalog}: ${String(e?.message||e)}`);viewer14ProgressFail(catalog)}}throw Error(failures.join(" || "))}catch(e){viewer14Status("Random galaxy failed: "+String(e?.message||e))}finally{b.disabled=false}}
function viewer14FetchCoords(){const c=window.viewer14Aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("viewer14CoordBox").value=t;viewer14Save({ra:c[0],dec:c[1]});viewer14Status("Coordinates fetched: "+t)}
async function viewer14GetInfo(){const b=document.getElementById("viewer14InfoButton"),parts=document.getElementById("viewer14CoordBox").value.trim().split(/\s+/).map(Number);if(parts.length<2||!Number.isFinite(parts[0])||!Number.isFinite(parts[1])){viewer14Status("Get Info failed: fetch valid coordinates first.");return}b.disabled=true;viewer14ProgressStart("SIMBAD 30 arcsecond cone");viewer14Status(`Fetching SIMBAD information for ${parts[0].toFixed(6)} ${parts[1].toFixed(6)}…`);try{const r=await google.colab.kernel.invokeFunction("viewer14.getInfo",[parts[0],parts[1]],{});const g=viewer14Result(r);if(!g||g.ok!==true)throw Error(g?.error||"SIMBAD lookup failed");viewer14ProgressDone("SIMBAD",`${Number(g.elapsed_seconds||0).toFixed(2)} s`);viewer14ShowGalaxy(g)}catch(e){viewer14ProgressFail("SIMBAD");viewer14Status("Get Info failed: "+String(e?.message||e))}finally{b.disabled=false}}
function viewer14Restore(m=""){if(!window.viewer14Aladin)return;const s=viewer14Load();document.getElementById("viewer14CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("viewer14CatalogMode").value=s.catalogMode;viewer14Survey(s.survey);window.viewer14Aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.viewer14Aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)viewer14Status(m)}
(async()=>{viewer14Setup();const s=viewer14Load();document.getElementById("viewer14CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("viewer14CatalogMode").value=s.catalogMode;document.getElementById("viewer14SurveySelect").value=s.survey;await A.init;window.viewer14Aladin=A.aladin("#viewer14-aladin",{target:`${s.ra} ${s.dec}`,survey:s.survey,fov:s.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});await viewer14RandomGalaxy()})().catch(e=>viewer14Status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>document.hidden?viewer14Save():viewer14Restore("Viewer restored from saved tab state."));
window.addEventListener("pagehide",()=>viewer14Save());
window.addEventListener("blur",()=>viewer14Save());
</script>'''

display(HTML(page))
