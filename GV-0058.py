from __future__ import annotations

import base64
import json
import math
import re
import subprocess
import sys
import urllib.request

import pandas as pd

try:
    from astroquery.simbad import Simbad
    from astroquery.ipac.ned import Ned
    from astropy.coordinates import SkyCoord
    import astropy.units as u
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "astroquery"])
    from astroquery.simbad import Simbad
    from astroquery.ipac.ned import Ned
    from astropy.coordinates import SkyCoord
    import astropy.units as u

try:
    from google.colab import output as colab_output
except Exception:
    colab_output = None

BASE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "886b38c031e3aef18b289a81bafa271c43f71830/GV-0057.py"
)

SEARCH_RADIUS_ARCSEC = 30.0


def _clean_value(value):
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
    if not text or text.lower() in {"nan", "none", "null", "...", "n/a", "--"}:
        return None
    return text


def _number_value(value):
    text = _clean_value(value)
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


def _row_value(row, *names):
    columns = {str(name).casefold(): name for name in row.colnames}
    for requested in names:
        actual = columns.get(str(requested).casefold())
        if actual is not None:
            value = row[actual]
            if _clean_value(value) is not None:
                return value
    return None


def _serial(value):
    number = _number_value(value)
    if number is not None:
        return number
    return _clean_value(value)


def _encode_rows(rows):
    text = json.dumps({"rows": rows}, ensure_ascii=False, allow_nan=False)
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def _simbad_query_official(ra, dec):
    ra = float(ra)
    dec = float(dec)
    center = SkyCoord(ra * u.deg, dec * u.deg, frame="icrs")

    simbad = Simbad()
    simbad.ROW_LIMIT = 20
    for field in ("otype", "sp_type", "velocity", "dimensions", "U", "B", "V", "R", "I"):
        try:
            simbad.add_votable_fields(field)
        except Exception:
            pass

    table = simbad.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return _encode_rows([])

    object_coords = SkyCoord(table["ra"], table["dec"], frame="icrs")
    table["_gv_separation_arcsec"] = center.separation(object_coords).arcsec
    table.sort("_gv_separation_arcsec")

    rows = []
    for row in table:
        bands = []
        for band in ("U", "B", "V", "R", "I"):
            value = _number_value(_row_value(row, band))
            if value is not None:
                bands.append(f"{band} {value:.4f}")

        rows.append({
            "main_id": _clean_value(_row_value(row, "main_id")),
            "ra": _number_value(_row_value(row, "ra")),
            "dec": _number_value(_row_value(row, "dec")),
            "otype": _clean_value(_row_value(row, "otype")),
            "sp_type": _clean_value(_row_value(row, "sp_type")),
            "rvz_redshift": _number_value(_row_value(row, "rvz_redshift")),
            "rvz_radvel": _number_value(_row_value(row, "rvz_radvel")),
            "galdim_majaxis": _number_value(_row_value(row, "galdim_majaxis")),
            "galdim_minaxis": _number_value(_row_value(row, "galdim_minaxis")),
            "magnitude_filter": "; ".join(bands) if bands else None,
            "separation_arcsec": _number_value(_row_value(row, "_gv_separation_arcsec")),
            "_selectionRule": "SIMBAD row 1",
            "_candidateCount": len(table),
        })
    return _encode_rows(rows)


def _safe_len(value):
    try:
        return len(value)
    except Exception:
        return 0


def _ned_query_official(ra, dec):
    ra = float(ra)
    dec = float(dec)
    center = SkyCoord(ra * u.deg, dec * u.deg, frame="icrs")
    table = Ned.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return _encode_rows([])

    ra_column = next((name for name in ("RA", "ra") if name in table.colnames), None)
    dec_column = next((name for name in ("DEC", "Dec", "dec") if name in table.colnames), None)
    if ra_column and dec_column:
        try:
            object_coords = SkyCoord(table[ra_column], table[dec_column], frame="icrs")
        except Exception:
            object_coords = SkyCoord(
                [_number_value(value) for value in table[ra_column]],
                [_number_value(value) for value in table[dec_column]],
                unit=(u.deg, u.deg),
                frame="icrs",
            )
        table["_gv_separation_arcsec"] = center.separation(object_coords).arcsec
        table.sort("_gv_separation_arcsec")

    row = table[0]
    name = _clean_value(_row_value(row, "Object Name", "Object_Name", "object_name", "main_id")) or "Not available"

    details = {}
    for table_name in ("photometry", "diameters", "redshifts", "positions", "references", "object_notes"):
        try:
            details[table_name] = Ned.get_table(name, table=table_name)
        except Exception:
            details[table_name] = None
    try:
        image_urls = Ned.get_image_list(name)
    except Exception:
        image_urls = []
    try:
        spectrum_urls = Ned.get_image_list(name, item="spectra", file_format="fits")
    except Exception:
        spectrum_urls = []

    magnitude = _clean_value(_row_value(row, "Magnitude and Filter", "Magnitude"))
    if magnitude is None and _safe_len(details.get("photometry")):
        magnitude = f"NED photometry: {_safe_len(details['photometry'])} row(s)"

    size_text = "Not available"
    if _safe_len(details.get("diameters")):
        size_text = f"NED diameter table: {_safe_len(details['diameters'])} row(s)"

    info_extra = (
        f"Photometry: {_safe_len(details.get('photometry'))} row(s); "
        f"Diameters: {_safe_len(details.get('diameters'))} row(s); "
        f"Redshifts: {_safe_len(details.get('redshifts'))} row(s); "
        f"FITS images: {_safe_len(image_urls)}; FITS spectra: {_safe_len(spectrum_urls)}"
    )

    result = {
        "main_id": name,
        "ra": _number_value(_row_value(row, "RA", "ra")),
        "dec": _number_value(_row_value(row, "DEC", "Dec", "dec")),
        "otype": _clean_value(_row_value(row, "Type", "Object Type")),
        "rvz_radvel": _number_value(_row_value(row, "Velocity")),
        "rvz_redshift": _number_value(_row_value(row, "Redshift")),
        "galdim_majaxis": None,
        "galdim_minaxis": None,
        "size_text": size_text,
        "magnitude_filter": magnitude,
        "separation_arcsec": _number_value(_row_value(row, "_gv_separation_arcsec", "Separation")),
        "info_extra": info_extra,
        "_selectionRule": "NED row 1",
        "_candidateCount": len(table),
    }
    return _encode_rows([result])


if colab_output is not None:
    colab_output.register_callback("gv0058.simbad_query", _simbad_query_official)
    colab_output.register_callback("gv0058.ned_query", _ned_query_official)

with urllib.request.urlopen(BASE_URL, timeout=90) as response:
    source = response.read().decode("utf-8")

replacements = [
    ("Galaxy Viewer — GV-0057", "Galaxy Viewer — GV-0058"),
    ("GV-0057 is standalone.", "GV-0058 uses the approved DEV-0003 official SIMBAD and NED catalog routines."),
    ("SIMBAD and NED use a 6-arcsecond search.", "SIMBAD and NED use a 30-arcsecond search."),
    ("gv0057.ned_query", "gv0058.ned_query"),
    ("Search complete. GV-0057 used SIMBAD row 1 and NED row 1 from the 6-arcsecond search window.",
     "Search complete. GV-0058 used SIMBAD row 1 and NED row 1 from the 30-arcsecond search window."),
]
for old, new in replacements:
    if old not in source:
        raise RuntimeError(f"GV-0058 patch target not found: {old}")
    source = source.replace(old, new, 1)

old_setup = 'document.getElementById("searchBody").innerHTML=CATALOGS.map(n=>`<tr><td>${n}</td><td>6 arcsec cone search</td><td id="status-${n}">Ready</td></tr>`).join("")+SURVEYS.map'
new_setup = 'document.getElementById("searchBody").innerHTML=CATALOGS.map(n=>`<tr><td>${n}</td><td>${(n==="SIMBAD"||n==="NED")?"30":"6"} arcsec cone search</td><td id="status-${n}">Ready</td></tr>`).join("")+SURVEYS.map'
if old_setup not in source:
    raise RuntimeError("GV-0058 setup patch target not found")
source = source.replace(old_setup, new_setup, 1)

old_size = 'function size(o,d){const a=+o?.galdim_majaxis,b=+o?.galdim_minaxis;if(!Number.isFinite(a)||!Number.isFinite(d))return"Not available";if(Number.isFinite(b))return`${fmt(d*a/206264.806,0)} × ${fmt(d*b/206264.806,0)} ly (${fmt(a*1000,3)} mas × ${fmt(b*1000,3)} mas)`;return`${fmt(d*a/206264.806,0)} ly (${fmt(a*1000,3)} mas)`}'
new_size = 'function size(o,d){if(o?.size_text)return o.size_text;const a=+o?.galdim_majaxis,b=+o?.galdim_minaxis;if(!Number.isFinite(a))return"Not available";if(Number.isFinite(b))return`${fmt(a,4)} × ${fmt(b,4)} arcmin`;return`${fmt(a,4)} arcmin`}'
if old_size not in source:
    raise RuntimeError("GV-0058 size patch target not found")
source = source.replace(old_size, new_size, 1)

old_simbad = 'async function simbad(ra,dec){const rad=6/3600,q=`SELECT TOP 20 main_id,ra,dec,rvz_redshift,rvz_radvel,plx_value,plx_err,galdim_majaxis,galdim_minaxis,otype,sp_type,DISTANCE(POINT(\'ICRS\',ra,dec),POINT(\'ICRS\',${ra},${dec})) AS separation FROM basic WHERE 1=CONTAINS(POINT(\'ICRS\',ra,dec),CIRCLE(\'ICRS\',${ra},${dec},${rad})) ORDER BY separation ASC`,p=await getJSON("https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query="+encodeURIComponent(q));return(p.data||[]).map(r=>Object.fromEntries(p.metadata.map((m,i)=>[m.name,r[i]])))}'
new_simbad = 'async function simbad(ra,dec){const r=await google.colab.kernel.invokeFunction("gv0058.simbad_query",[ra,dec],{});let encoded=r?.data?.["text/plain"]??r?.data?.["application/json"]??r;encoded=String(encoded).trim();if((encoded.startsWith("\\\"")&&encoded.endsWith("\\\""))||(encoded.startsWith("\'")&&encoded.endsWith("\'")))encoded=encoded.slice(1,-1);const jsonText=decodeURIComponent(Array.from(atob(encoded)).map(ch=>"%"+ch.charCodeAt(0).toString(16).padStart(2,"0")).join(""));const p=JSON.parse(jsonText);if(p&&Array.isArray(p.rows))return p.rows;throw Error("SIMBAD callback returned no decodable rows")}'
if old_simbad not in source:
    raise RuntimeError("GV-0058 SIMBAD patch target not found")
source = source.replace(old_simbad, new_simbad, 1)

old_sep = 'sep=Number.isFinite(+o.angular_separation_arcmin)?`${fmt(+o.angular_separation_arcmin*60,3)} arcsec`:(Number.isFinite(+o.separation)?`${fmt(+o.separation*3600,3)} arcsec`:"Not available"),info=`Catalog: ${c}; Selection: ${c} row 1; Candidates: ${o._candidateCount||1}`'
new_sep = 'sep=Number.isFinite(+o.separation_arcsec)?`${fmt(+o.separation_arcsec,3)} arcsec`:(Number.isFinite(+o.angular_separation_arcmin)?`${fmt(+o.angular_separation_arcmin*60,3)} arcsec`:(Number.isFinite(+o.separation)?`${fmt(+o.separation*3600,3)} arcsec`:"Not available")),info=`Catalog: ${c}; Selection: ${c} row 1; Candidates: ${o._candidateCount||1}${o.info_extra?"; "+o.info_extra:""}`'
if old_sep not in source:
    raise RuntimeError("GV-0058 result patch target not found")
source = source.replace(old_sep, new_sep, 1)

exec(compile(source, "GV-0058.py", "exec"))
