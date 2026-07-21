from __future__ import annotations

from io import StringIO
from urllib.parse import quote
import html
import math
import re

import pandas as pd
import requests
from IPython.display import HTML, display

SEARCH_RA = 53.172576
SEARCH_DEC = -27.796392
SEARCH_RADIUS_ARCSEC = 6.0

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 GalaxyViewer-VVV-0001"})


def clean(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    text = re.sub(r"\s+", " ", str(value)).strip()
    return None if not text or text.lower() in {"nan", "none", "null", "..."} else text


def number(value):
    text = clean(value)
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


def ra_degrees(value):
    text = clean(value)
    if text is None:
        return None
    if not re.search(r"[hms:]", text, re.I):
        return number(text)
    match = re.search(r"(\d+)\s*[h:]\s*(\d+)\s*[m:]\s*([\d.]+)", text, re.I)
    if not match:
        return None
    return 15.0 * (float(match.group(1)) + float(match.group(2)) / 60.0 + float(match.group(3)) / 3600.0)


def dec_degrees(value):
    text = clean(value)
    if text is None:
        return None
    if not re.search(r"[dms:]", text, re.I):
        return number(text)
    match = re.search(r"([+-]?)\s*(\d+)\s*[d:]\s*(\d+)\s*[m:]\s*([\d.]+)", text, re.I)
    if not match:
        return None
    sign = -1.0 if match.group(1) == "-" else 1.0
    return sign * (float(match.group(2)) + float(match.group(3)) / 60.0 + float(match.group(4)) / 3600.0)


def simbad_query():
    radius = SEARCH_RADIUS_ARCSEC / 3600.0
    adql = f"""
    SELECT TOP 20
        main_id, ra, dec, otype, sp_type,
        rvz_redshift, rvz_radvel,
        flux_U, flux_B, flux_V, flux_R, flux_I,
        nbref,
        DISTANCE(
            POINT('ICRS', ra, dec),
            POINT('ICRS', {SEARCH_RA}, {SEARCH_DEC})
        ) AS separation
    FROM basic
    WHERE 1 = CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE('ICRS', {SEARCH_RA}, {SEARCH_DEC}, {radius})
    )
    ORDER BY separation ASC
    """
    response = SESSION.get(
        "https://simbad.cds.unistra.fr/simbad/sim-tap/sync",
        params={"request": "doQuery", "lang": "adql", "format": "json", "query": adql},
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    columns = [item["name"] for item in payload.get("metadata", [])]
    frame = pd.DataFrame(payload.get("data", []), columns=columns)
    if frame.empty:
        return None, frame
    row = frame.iloc[0].to_dict()
    separation = number(row.get("separation"))
    if separation is not None:
        separation *= 3600.0
    magnitudes = []
    for band in ["U", "B", "V", "R", "I"]:
        value = number(row.get(f"flux_{band}"))
        if value is not None:
            magnitudes.append(f"{band} {value:.4f}")
    return {
        "catalog": "SIMBAD",
        "name": clean(row.get("main_id")) or "Not available",
        "ra": number(row.get("ra")),
        "dec": number(row.get("dec")),
        "otype": clean(row.get("otype")) or "Not available",
        "velocity": number(row.get("rvz_radvel")),
        "redshift": number(row.get("rvz_redshift")),
        "magnitude": "<br>".join(magnitudes) if magnitudes else "Not available",
        "separation": separation,
        "references": number(row.get("nbref")),
        "candidates": len(frame),
    }, frame


def ned_query():
    url = (
        "https://ned.ipac.caltech.edu/cgi-bin/objsearch"
        "?search_type=Near+Position+Search"
        "&in_csys=Equatorial&in_equinox=J2000.0"
        f"&lon={SEARCH_RA}d&lat={SEARCH_DEC}d"
        "&radius=0.1&hconst=73&omegam=0.27&omegav=0.73&corr_z=1"
        "&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z"
        "&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes2=Galaxies"
        "&out_csys=Equatorial&out_equinox=J2000.0"
        "&obj_sort=Distance+to+search+center&of=table"
    )
    response = SESSION.get(url, timeout=90)
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text), header=None)
    result = None
    for frame in tables:
        if frame.empty or frame.shape[1] < 10:
            continue
        numbered = frame.iloc[:, 0].astype(str).str.strip().str.fullmatch(r"\d+")
        if numbered.sum() >= 1:
            result = frame.loc[numbered].copy()
            break
    if result is None or result.empty:
        return None, None
    cells = [clean(value) for value in result.iloc[0].tolist()]
    raw_velocity = cells[5] if len(cells) > 5 else None
    velocity = None if raw_velocity and re.search(r"[<>]", raw_velocity) else number(raw_velocity)
    separation_arcmin = number(cells[9] if len(cells) > 9 else None)
    return {
        "catalog": "NED",
        "name": cells[1] if len(cells) > 1 else "Not available",
        "ra": ra_degrees(cells[2] if len(cells) > 2 else None),
        "dec": dec_degrees(cells[3] if len(cells) > 3 else None),
        "otype": cells[4] if len(cells) > 4 else "Not available",
        "velocity": velocity,
        "redshift": number(cells[6] if len(cells) > 6 else None),
        "magnitude": cells[8] if len(cells) > 8 and clean(cells[8]) else "Not available",
        "separation": separation_arcmin * 60.0 if separation_arcmin is not None else None,
        "references": None,
        "candidates": len(result),
    }, result


def object_url(row):
    if row["catalog"] == "SIMBAD":
        return "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=" + quote(row["name"])
    return "https://ned.ipac.caltech.edu/byname?objname=" + quote(row["name"])


def thumbnail_url(row):
    if row["catalog"] == "SIMBAD":
        return (
            "https://alasky.cds.unistra.fr/cgi/simbad-thumbnails/get-thumbnail.py"
            f"?name={quote(row['name'])}&size=0.0666667&legend=P%2FDSS2%2Fcolor"
            "&reticle=true&reticleWidth=1&reticleColor=yellow&scale=true"
        )
    return (
        "https://irsa.ipac.caltech.edu/applications/finderchart/servlet/api"
        f"?mode=getImage&locstr={quote(row['name'])}&subsetsize=3.25"
        "&thumbnail_size=small&survey=DSS&grid=false"
        "&dss_bands=poss2ukstu_red&type=jpgurl"
    )


def fmt(value, decimals=3):
    return "Not available" if value is None else f"{value:,.{decimals}f}"


print(f"Searching SIMBAD and NED at {SEARCH_RA:.6f} {SEARCH_DEC:.6f}...")

simbad_row, simbad_raw = simbad_query()
ned_row, ned_raw = ned_query()
rows = [row for row in [simbad_row, ned_row] if row is not None]

if not rows:
    raise RuntimeError("No SIMBAD or NED rows were returned.")

body = ""
for row in rows:
    link = object_url(row)
    thumb = thumbnail_url(row)
    references = "Not available" if row["references"] is None else str(int(row["references"]))
    velocity = "Not available" if row["velocity"] is None else f"{row['velocity']:,.3f} km/s"
    redshift = "Not available" if row["redshift"] is None else f"{row['redshift']:.6f}"
    separation = "Not available" if row["separation"] is None else f"{row['separation']:.3f} arcsec"
    body += f"""
    <tr>
      <td class='object-cell'>
        <a class='object-link' href='{html.escape(link, quote=True)}' target='_blank' rel='noopener noreferrer'>
          {html.escape(row['name'])} <span>↗</span>
        </a>
        <a class='thumb-link' href='{html.escape(link, quote=True)}' target='_blank' rel='noopener noreferrer'>
          <img class='thumb' src='{html.escape(thumb, quote=True)}' alt='{html.escape(row['catalog'])} preview'>
        </a>
        <div class='caption'>{html.escape(row['catalog'])} native preview</div>
      </td>
      <td class='coords'><b>RA</b> {fmt(row['ra'], 6)}<br><b>Dec</b> {fmt(row['dec'], 6)}</td>
      <td>{html.escape(row['otype'])}<br>Not available</td>
      <td>{velocity}</td>
      <td>{redshift}</td>
      <td>{row['magnitude']}</td>
      <td>{separation}</td>
      <td>Catalog: {row['catalog']}<br>Selection: row 1<br>Candidates: {row['candidates']}<br>References: {references}</td>
    </tr>
    """

widget = f"""
<div id='vvv0001'>
<style>
#vvv0001{{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}}
#vvv0001 h4{{color:#35c6ff;margin:4px 0 10px}}
#vvv0001 .wrap{{overflow-x:auto;border:1px solid #0b526f;border-radius:8px;background:#000}}
#vvv0001 table{{width:100%;min-width:1040px;border-collapse:collapse;background:#000;color:#7FDBFF;font-size:14px}}
#vvv0001 thead tr{{background:#031723}}
#vvv0001 th{{padding:9px;color:#43d2ff;font-weight:700;text-align:left;vertical-align:top;border:1px solid #116482}}
#vvv0001 td{{padding:8px;color:#7FDBFF;background:#000;border:1px solid #0b506b;vertical-align:top;line-height:1.45}}
#vvv0001 tbody tr:nth-child(even) td{{background:#020b10}}
#vvv0001 th:nth-child(1),#vvv0001 td:nth-child(1){{width:170px;min-width:170px;max-width:170px}}
#vvv0001 th:nth-child(2),#vvv0001 td:nth-child(2){{width:135px;min-width:135px;max-width:135px}}
#vvv0001 .object-link{{display:inline-block;color:#58d7ff;font-weight:700;text-decoration:none;border-bottom:1px dotted rgba(88,215,255,.65)}}
#vvv0001 .object-link:hover{{color:#a6eeff;text-shadow:0 0 8px rgba(67,210,255,.75)}}
#vvv0001 .thumb-link{{display:block;width:150px;margin-top:10px;text-decoration:none}}
#vvv0001 .thumb{{display:block;width:150px;height:105px;object-fit:cover;background:#02080d;border:1px solid #137aa3;border-radius:7px;box-shadow:0 0 10px rgba(0,174,239,.20)}}
#vvv0001 .thumb-link:hover .thumb{{border-color:#58d7ff;box-shadow:0 0 14px rgba(67,210,255,.48);transform:scale(1.018)}}
#vvv0001 .caption{{width:150px;margin-top:5px;color:#61b9d5;font-size:10px;text-align:center}}
#vvv0001 .coords{{font-family:Consolas,Menlo,Monaco,monospace;white-space:nowrap}}
#vvv0001 .coords b{{display:inline-block;width:28px;color:#43d2ff}}
#vvv0001 .note{{margin-top:10px;color:#61b9d5;font-size:12px;line-height:1.45}}
</style>
<h4>VVV-0001 — Object figures of merit</h4>
<div class='wrap'>
<table>
<thead><tr><th>Object name</th><th>RA / Dec</th><th>Object type / Size</th><th>Velocity</th><th>Redshift</th><th>Magnitude / Filter</th><th>Angular separation</th><th>Information</th></tr></thead>
<tbody>{body}</tbody>
</table>
</div>
<div class='note'>Search coordinate: {SEARCH_RA:.6f} {SEARCH_DEC:.6f}. Clicking either an object name or thumbnail opens the corresponding catalog record in a new tab. No galaxy-size calculation is performed.</div>
</div>
"""

display(HTML(widget))

print("\nSIMBAD RAW FIRST ROW")
display(simbad_raw.head(1) if simbad_raw is not None else pd.DataFrame())
print("\nNED RAW FIRST ROW")
display(ned_raw.head(1) if ned_raw is not None else pd.DataFrame())
