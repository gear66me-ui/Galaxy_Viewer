from __future__ import annotations

import csv
import io
import json
import math
import random
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
CATALOGS = ("HyperLEDA", "RC3", "Arp")


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _float(value: Any) -> float | None:
    try:
        text = _clean(value)
        if not text or text in {"?", "nan", "NaN", "9.99", "999", "999.0"}:
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


def _vizier_rows(params: dict[str, str], timeout: int = 35) -> list[dict[str, str]]:
    query = urllib.parse.urlencode(params)
    url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?" + query
    with urllib.request.urlopen(url, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")

    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if len(lines) < 2:
        return []
    return list(csv.DictReader(io.StringIO("\n".join(lines)), delimiter="\t"))


def _coord_from_row(row: dict[str, Any]) -> tuple[float, float]:
    ra_text = _pick(row, "_RAJ2000", "RAJ2000", "RA2000")
    dec_text = _pick(row, "_DEJ2000", "DEJ2000", "DE2000")

    if ra_text and dec_text:
        try:
            from astropy.coordinates import SkyCoord
            import astropy.units as u

            if ":" in ra_text or " " in ra_text:
                coord = SkyCoord(
                    f"{ra_text} {dec_text}",
                    unit=(u.hourangle, u.deg),
                    frame="icrs",
                )
            else:
                coord = SkyCoord(float(ra_text) * u.deg, float(dec_text) * u.deg, frame="icrs")
            return float(coord.ra.deg), float(coord.dec.deg)
        except Exception:
            pass

    rah = _float(_pick(row, "RAh"))
    ram = _float(_pick(row, "RAm"))
    ras = _float(_pick(row, "RAs"))
    ded = _float(_pick(row, "DEd"))
    dem = _float(_pick(row, "DEm"))
    des = _float(_pick(row, "DEs"))
    sign = -1.0 if _pick(row, "DE-", "DEsign").startswith("-") else 1.0
    if None not in (rah, ram, ras, ded, dem, des):
        ra = 15.0 * (rah + ram / 60.0 + ras / 3600.0)
        dec = sign * (abs(ded) + dem / 60.0 + des / 3600.0)
        return ra, dec

    raise ValueError("No usable J2000/ICRS coordinates returned.")


def _diameters_from_log(log_d25: float | None, log_r25: float | None) -> tuple[float | None, float | None]:
    if log_d25 is None or log_d25 >= 9:
        return None, None
    major = 0.1 * (10.0 ** log_d25)
    if log_r25 is None or log_r25 >= 9:
        return major, None
    minor = major / (10.0 ** log_r25)
    return major, minor


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


def _physical_size_kly(major_arcmin: float | None, minor_arcmin: float | None, distance_mpc: float | None) -> str:
    if major_arcmin is None or distance_mpc is None or distance_mpc <= 0:
        return "Not available"

    def axis_kly(arcmin: float) -> float:
        radians = math.radians(arcmin / 60.0)
        return distance_mpc * 1.0e3 * math.tan(radians) * 3.26156

    major_kly = axis_kly(major_arcmin)
    if minor_arcmin is None:
        return f"{major_kly:,.1f} thousand ly — derived"
    return f"{major_kly:,.1f} × {axis_kly(minor_arcmin):,.1f} thousand ly — derived"


def _format_size(major: float | None, minor: float | None) -> str:
    if major is None:
        return "Not available"
    if minor is None:
        return f"{major:.3f} arcmin"
    return f"{major:.3f} × {minor:.3f} arcmin"


def _fov_for_size(major_arcmin: float | None, fallback: float = 0.18) -> float:
    if major_arcmin is None or major_arcmin <= 0:
        return fallback
    return max(0.035, min(4.0, major_arcmin * 3.2 / 60.0))


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
) -> dict[str, Any]:
    ra, dec = _coord_from_row(row)
    z = velocity_kms / C_KMS if velocity_kms is not None and velocity_kms > 0 else None
    distance_mpc, distance_text = _distance_from_redshift(z)
    redshift_distance = (
        f"{z:.8f} / {distance_text}" if z is not None else "Not available / Not available"
    )
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
        "major_arcmin": major_arcmin,
        "minor_arcmin": minor_arcmin,
        "redshift_distance": redshift_distance,
        "redshift": z,
        "velocity_kms": velocity_kms,
        "distance_mpc": distance_mpc,
        "distance_text": distance_text,
        "physical_size": _physical_size_kly(major_arcmin, minor_arcmin, distance_mpc),
        "magnitude": "Not available" if magnitude is None else f"{magnitude:.3f}",
    }


def _query_hyperleda() -> dict[str, Any]:
    errors: list[str] = []
    for _ in range(20):
        ra0 = random.uniform(0.0, 360.0)
        dec0 = math.degrees(math.asin(random.uniform(-1.0, 1.0)))
        try:
            rows = _vizier_rows(
                {
                    "-source": "VII/237/pgc",
                    "-c": f"{ra0:.8f} {dec0:.8f}",
                    "-c.rm": "90",
                    "-out": "PGC,RAJ2000,DEJ2000,OType,MType,logD25,logR25",
                    "-out.max": "200",
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
                )
            except Exception:
                continue
            if result["key"] not in RECENT_KEYS:
                candidates.append(result)

        if candidates:
            return random.choice(candidates)

    raise RuntimeError("HyperLEDA returned no usable non-repeating galaxy. " + " | ".join(errors[-3:]))


def _query_rc3() -> dict[str, Any]:
    errors: list[str] = []
    for _ in range(30):
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
            _float(_pick(row, "D25")),
            _float(_pick(row, "R25")),
        )
        velocity = (
            _float(_pick(row, "V3K"))
            or _float(_pick(row, "cz"))
            or _float(_pick(row, "V21"))
        )
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
            )
        except Exception as exc:
            errors.append(str(exc))
            continue

        if result["key"] not in RECENT_KEYS:
            return result

    raise RuntimeError("RC3 returned no usable non-repeating galaxy. " + " | ".join(errors[-3:]))


def _query_arp() -> dict[str, Any]:
    errors: list[str] = []
    for _ in range(30):
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
        major = _float(_pick(row, "dim1"))
        minor = _float(_pick(row, "dim2"))

        try:
            result = _row_to_result(
                row,
                catalog="Arp",
                name=name,
                source="Arp Peculiar Galaxies VII/192 via VizieR",
                major_arcmin=major,
                minor_arcmin=minor,
                morphology=_pick(row, "MType") or "Peculiar galaxy",
                magnitude=_float(_pick(row, "VT")),
                velocity_kms=None,
            )
        except Exception as exc:
            errors.append(str(exc))
            continue

        if result["key"] not in RECENT_KEYS:
            return result

    raise RuntimeError("Arp returned no usable non-repeating galaxy. " + " | ".join(errors[-3:]))


def _random_catalog_galaxy() -> dict[str, Any]:
    order = list(CATALOGS)
    random.shuffle(order)
    failures: list[str] = []

    for catalog in order:
        try:
            if catalog == "HyperLEDA":
                result = _query_hyperleda()
            elif catalog == "RC3":
                result = _query_rc3()
            else:
                result = _query_arp()

            RECENT_KEYS.append(result["key"])
            return result
        except Exception as exc:
            failures.append(f"{catalog}: {exc}")

    raise RuntimeError("All three random catalog queries failed. " + " || ".join(failures))


def viewer12_random_callback() -> str:
    try:
        result = _random_catalog_galaxy()
    except Exception as exc:
        result = {"ok": False, "error": str(exc)}
    return json.dumps(result, ensure_ascii=False)


output.register_callback("viewer12.randomGalaxy", viewer12_random_callback)

page = r'''
<div id="viewer12-root">
<style>
#viewer12-root{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}
#viewer12-root h3{color:#35c6ff;margin:12px 0 9px}
#viewer12-root .viewer-shell{background:#000;border:1px solid #137aa3;border-radius:8px;overflow:hidden}
#viewer12-root .controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px}
#viewer12-root input{background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;outline:none}
#viewer12-root button{padding:14px 24px;font-size:17px;font-weight:700;color:#fff;border:0;border-radius:9px;cursor:pointer}
#viewer12-root button:disabled{opacity:.55;cursor:wait}
#viewer12-root .fetch-btn{background:#159447}
#viewer12-root .random-btn{background:#8a4fd4}
#viewer12-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}
#viewer12-root .survey-menu-wrap{position:relative;display:inline-block;min-width:290px}
#viewer12-root .survey-menu-button{width:100%;text-align:left;background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;font-weight:400}
#viewer12-root .survey-menu{display:none;position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:999999;background:#000;border:1px solid #169ac7;border-radius:8px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.75)}
#viewer12-root .survey-menu.open{display:block}
#viewer12-root .survey-option{display:block;width:100%;text-align:left;background:#000;color:#7FDBFF;border:0;border-bottom:1px solid #0b526f;border-radius:0;padding:12px;font-size:16px;font-weight:400}
#viewer12-root .survey-option:last-child{border-bottom:0}
#viewer12-root .survey-option:active{background:#063047}
</style>
<h3>Galaxy Viewer — VIEWER-12</h3>
<div class="viewer-shell"><div id="viewer12-aladin" style="width:100%;height:520px"></div></div>
<div class="controls">
<button id="viewer12RandomButton" class="random-btn" onclick="viewer12RandomGalaxy()">Random Galaxy</button>
<button class="fetch-btn" onclick="viewer12FetchCoords()">Fetch Coordinates</button>
<input id="viewer12CoordBox" type="text" value="53.162500 -27.791667" readonly style="min-width:280px">
</div>
<div class="controls">
<label>Displayed survey:</label>
<div class="survey-menu-wrap">
<input type="hidden" id="viewer12SurveySelect">
<button type="button" id="viewer12SurveyButton" class="survey-menu-button" onclick="viewer12ToggleSurveyMenu(event)">DSS2 Color ▾</button>
<div id="viewer12SurveyMenu" class="survey-menu"></div>
</div>
</div>
<div id="viewer12Status" class="status">Viewer loading…</div>
</div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
const VIEWER12_SURVEYS=[
{name:"Hubble Outreach Color",id:"CDS/P/HST/EPO"},
{name:"JWST Outreach Color",id:"CDS/P/JWST/EPO"},
{name:"DSS2 Color",id:"P/DSS2/color"},
{name:"DSS2 Red",id:"P/DSS2/red"},
{name:"Pan-STARRS DR1 Color",id:"P/PanSTARRS/DR1/color-z-zg-g"},
{name:"DECaLS DR5 Color",id:"P/DECaLS/DR5/color"},
{name:"2MASS Color",id:"P/2MASS/color"},
{name:"GALEX GR6/7 Color",id:"P/GALEXGR6/AIS/color"}
];
const VIEWER12_KEY="galaxy-viewer-viewer12-state";
function viewer12State0(){return{ra:53.1625,dec:-27.791667,survey:"P/DSS2/color",fov:1}}
function viewer12Norm(id){return VIEWER12_SURVEYS.some(s=>s.id===id)?id:viewer12State0().survey}
function viewer12Load(){try{const p=JSON.parse(localStorage.getItem(VIEWER12_KEY)||"null")||{},d=viewer12State0();return{ra:Number.isFinite(+p.ra)?+p.ra:d.ra,dec:Number.isFinite(+p.dec)?+p.dec:d.dec,survey:viewer12Norm(p.survey),fov:Number.isFinite(+p.fov)&&+p.fov>0?+p.fov:d.fov}}catch(e){return viewer12State0()}}
function viewer12Capture(){const d=viewer12Load();let ra=d.ra,dec=d.dec,fov=d.fov;try{[ra,dec]=window.viewer12Aladin.getRaDec()}catch(e){}try{const z=+window.viewer12Aladin.getFov();if(z>0)fov=z}catch(e){}return{ra:+ra,dec:+dec,survey:viewer12Norm(document.getElementById("viewer12SurveySelect")?.value||d.survey),fov}}
function viewer12Save(o={}){const s={...viewer12State0(),...viewer12Capture(),...o};s.survey=viewer12Norm(s.survey);localStorage.setItem(VIEWER12_KEY,JSON.stringify(s));window.VIEWER12_STATE=s;return s}
function viewer12Status(t){document.getElementById("viewer12Status").textContent=t}
function viewer12Setup(){document.getElementById("viewer12SurveyMenu").innerHTML=VIEWER12_SURVEYS.map(s=>`<button type="button" class="survey-option" onclick="viewer12ChooseSurvey('${s.id}',event)">${s.name}</button>`).join("")}
function viewer12Survey(id){id=viewer12Norm(id);document.getElementById("viewer12SurveySelect").value=id;const item=VIEWER12_SURVEYS.find(s=>s.id===id);document.getElementById("viewer12SurveyButton").textContent=(item?item.name:id)+" ▾";window.viewer12Aladin.setImageSurvey(id)}
function viewer12ToggleSurveyMenu(e){e.stopPropagation();document.getElementById("viewer12SurveyMenu").classList.toggle("open")}
function viewer12ChooseSurvey(id,e){e.stopPropagation();viewer12Survey(id);viewer12Save({survey:id});document.getElementById("viewer12SurveyMenu").classList.remove("open");viewer12Status("Loaded survey: "+id)}
document.addEventListener("click",()=>{const m=document.getElementById("viewer12SurveyMenu");if(m)m.classList.remove("open")})
function viewer12Parse(v){if(v==null)return v;if(typeof v!=="string")return v;v=v.trim();if(v.startsWith("'")&&v.endsWith("'"))v=v.slice(1,-1).replace(/\\'/g,"'").replace(/\\\\/g,"\\");try{return JSON.parse(v)}catch(_){return v}}
function viewer12Result(r){const d=r?.data??r;if(d&&typeof d==="object"&&d.ok!==undefined)return d;if(d&&typeof d==="object")return viewer12Parse(d["application/json"]??d["text/plain"]??Object.values(d)[0]);return viewer12Parse(d)}
function viewer12Panel(g,survey,fov){
const velocity=Number.isFinite(Number(g.velocity_kms))?`${Number(g.velocity_kms).toLocaleString(undefined,{maximumFractionDigits:1})} km/s`:"Not available";
return `RANDOM GALAXY FIGURES OF MERIT

Object: ${g.name}
Source catalog: ${g.catalog}
ICRS coordinates: ${Number(g.ra).toFixed(6)} ${Number(g.dec).toFixed(6)}
Morphological type: ${g.morphology||"Not available"}
Angular size: ${g.angular_size||"Not available"}
Redshift / Distance: ${g.redshift_distance||"Not available / Not available"}
Radial velocity: ${velocity}
Physical size: ${g.physical_size||"Not available"}
Magnitude: ${g.magnitude||"Not available"}
Displayed survey: ${survey}
Field of view: ${fov.toFixed(3)}°
Data source: ${g.source}`;
}
function viewer12ShowGalaxy(g,message="Random galaxy loaded"){const ra=Number(g.ra),dec=Number(g.dec),fov=Number(g.fov),survey=viewer12Norm(g.survey_id||"P/DSS2/color");document.getElementById("viewer12CoordBox").value=`${ra.toFixed(6)} ${dec.toFixed(6)}`;viewer12Survey(survey);window.viewer12Aladin.gotoRaDec(ra,dec);const z=()=>{try{window.viewer12Aladin.setFoV(fov)}catch(e){}};z();setTimeout(z,150);setTimeout(z,500);viewer12Save({ra,dec,survey,fov});viewer12Status(viewer12Panel(g,survey,fov))}
async function viewer12RandomGalaxy(message="Random galaxy loaded"){const b=document.getElementById("viewer12RandomButton");b.disabled=true;viewer12Status("Randomly selecting HyperLEDA, RC3, or Arp…");try{const r=await google.colab.kernel.invokeFunction("viewer12.randomGalaxy",[],{});const g=viewer12Result(r);if(!g||g.ok!==true)throw Error(g?.error||"Lookup failed");viewer12ShowGalaxy(g,message)}catch(e){viewer12Status("Random galaxy failed: "+String(e?.message||e))}finally{b.disabled=false}}
function viewer12FetchCoords(){const c=window.viewer12Aladin.getRaDec(),t=`${c[0].toFixed(6)} ${c[1].toFixed(6)}`;document.getElementById("viewer12CoordBox").value=t;viewer12Save({ra:c[0],dec:c[1]});viewer12Status("Coordinates fetched: "+t)}
function viewer12Restore(m=""){if(!window.viewer12Aladin)return;const s=viewer12Load();document.getElementById("viewer12CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;viewer12Survey(s.survey);window.viewer12Aladin.gotoRaDec(s.ra,s.dec);const f=()=>{try{window.viewer12Aladin.setFoV(s.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);if(m)viewer12Status(m)}
(async()=>{viewer12Setup();const s=viewer12Load();document.getElementById("viewer12CoordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;document.getElementById("viewer12SurveySelect").value=s.survey;await A.init;window.viewer12Aladin=A.aladin("#viewer12-aladin",{target:`${s.ra} ${s.dec}`,survey:s.survey,fov:s.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});await viewer12RandomGalaxy("Launch random galaxy")})().catch(e=>viewer12Status("Viewer initialization failed: "+e.message));
document.addEventListener("visibilitychange",()=>document.hidden?viewer12Save():viewer12Restore("Viewer restored from saved tab state."));
window.addEventListener("pagehide",()=>viewer12Save());
window.addEventListener("blur",()=>viewer12Save());
</script>
'''

display(HTML(page))
