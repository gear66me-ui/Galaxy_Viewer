from IPython.display import Javascript, HTML, display
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

from __future__ import annotations

import html
import math
import re
import subprocess
import sys
from urllib.parse import quote

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

import pandas as pd

SEARCH_RA_DEG = 53.124507
SEARCH_DEC_DEG = -27.740285
SEARCH_RADIUS_ARCSEC = 30.0


def clean(value):
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
    if not text or text.lower() in {"nan", "none", "null", "...", "--", "n/a"}:
        return None
    return text


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


def row_value(row, *names):
    columns = {str(name).casefold(): name for name in row.colnames}
    for requested in names:
        actual = columns.get(str(requested).casefold())
        if actual is not None:
            value = row[actual]
            if clean(value) is not None:
                return value
    return None


def first_matching_column(row, predicates):
    for name in row.colnames:
        lowered = str(name).casefold()
        if any(predicate(lowered) for predicate in predicates):
            value = row[name]
            if clean(value) is not None:
                return value, str(name)
    return None, None


def distance_from_z(z):
    z = number(z)
    if z is None or z <= 0:
        return None
    h0 = 67.4
    omega_m = 0.315
    omega_l = 0.685
    c_km_s = 299792.458
    steps = 4000
    total = 0.0
    for index in range(steps):
        x = (index + 0.5) * z / steps
        total += 1.0 / math.sqrt(omega_m * (1.0 + x) ** 3 + omega_l)
    megaparsec = (c_km_s / h0) * (total * z / steps)
    return megaparsec * 3261563.777


def cutout_url(ra, dec):
    return (
        "https://alasky.cds.unistra.fr/hips-image-services/hips2fits"
        "?hips=CDS/P/DSS2/color&width=220&height=160&fov=0.03"
        "&projection=TAN&coordsys=icrs&format=jpg"
        f"&ra={float(ra):.8f}&dec={float(dec):.8f}"
    )


def simbad_url(name):
    return "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=" + quote(str(name))


def ned_url(name):
    return "https://ned.ipac.caltech.edu/byname?objname=" + quote(str(name))


def vizier_url(catalog, ra, dec):
    return (
        "https://vizier.cds.unistra.fr/viz-bin/VizieR"
        f"?-source={quote(str(catalog))}&-c={float(ra):.8f}%20{float(dec):.8f}"
        "&-c.rs=30&-out.max=100&-out.add=_r&-sort=_r"
    )


def fetch_simbad(center):
    service = Simbad()
    service.ROW_LIMIT = 20
    for field in ("otype", "sp_type", "velocity", "dimensions", "U", "B", "V", "R", "I"):
        try:
            service.add_votable_fields(field)
        except Exception:
            pass
    table = service.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return None, 0
    coords = SkyCoord(table["ra"], table["dec"], frame="icrs")
    table["_gv_separation_arcsec"] = center.separation(coords).arcsec
    table.sort("_gv_separation_arcsec")
    row = table[0]
    name = clean(row_value(row, "main_id")) or "Not available"
    ra = number(row_value(row, "ra")) or SEARCH_RA_DEG
    dec = number(row_value(row, "dec")) or SEARCH_DEC_DEG
    z = number(row_value(row, "rvz_redshift"))
    velocity = number(row_value(row, "rvz_radvel"))
    major = number(row_value(row, "galdim_majaxis"))
    minor = number(row_value(row, "galdim_minaxis"))
    size_text = "Not available"
    if major is not None and minor is not None:
        size_text = f"{major:.4f} x {minor:.4f} arcmin"
    elif major is not None:
        size_text = f"{major:.4f} arcmin"
    mags = []
    for band in ("U", "B", "V", "R", "I"):
        value = number(row_value(row, band))
        if value is not None:
            mags.append(f"{band} {value:.4f}")
    return {
        "catalog": "SIMBAD",
        "name": name,
        "ra": ra,
        "dec": dec,
        "otype": clean(row_value(row, "otype")) or "Not available",
        "size": size_text,
        "velocity": velocity,
        "z": z,
        "magnitude": "; ".join(mags) if mags else "Not available",
        "separation": number(row_value(row, "_gv_separation_arcsec")),
        "url": simbad_url(name),
        "thumbnail": cutout_url(ra, dec),
        "info": f"SIMBAD row 1; candidates: {len(table)}",
    }, len(table)


def fetch_ned(center):
    table = Ned.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return None, 0
    ra_col = next((name for name in ("RA", "ra") if name in table.colnames), None)
    dec_col = next((name for name in ("DEC", "Dec", "dec") if name in table.colnames), None)
    if ra_col and dec_col:
        try:
            coords = SkyCoord(table[ra_col], table[dec_col], frame="icrs")
        except Exception:
            coords = SkyCoord(
                [number(value) for value in table[ra_col]],
                [number(value) for value in table[dec_col]],
                unit=(u.deg, u.deg),
                frame="icrs",
            )
        table["_gv_separation_arcsec"] = center.separation(coords).arcsec
        table.sort("_gv_separation_arcsec")
    row = table[0]
    name = clean(row_value(row, "Object Name", "Object_Name", "object_name")) or "Not available"
    ra = number(row_value(row, "RA", "ra")) or SEARCH_RA_DEG
    dec = number(row_value(row, "DEC", "Dec", "dec")) or SEARCH_DEC_DEG
    try:
        redshift_rows = len(Ned.get_table(name, table="redshifts"))
    except Exception:
        redshift_rows = 0
    try:
        diameter_rows = len(Ned.get_table(name, table="diameters"))
    except Exception:
        diameter_rows = 0
    return {
        "catalog": "NED",
        "name": name,
        "ra": ra,
        "dec": dec,
        "otype": clean(row_value(row, "Type", "Object Type")) or "Not available",
        "size": f"NED diameter table: {diameter_rows} row(s)" if diameter_rows else "Not available",
        "velocity": number(row_value(row, "Velocity")),
        "z": number(row_value(row, "Redshift")),
        "magnitude": clean(row_value(row, "Magnitude and Filter", "Magnitude")) or "Not available",
        "separation": number(row_value(row, "_gv_separation_arcsec", "Separation")),
        "url": ned_url(name),
        "thumbnail": cutout_url(ra, dec),
        "info": f"NED row 1; candidates: {len(table)}; redshift rows: {redshift_rows}",
    }, len(table)


def fetch_vizier(center):
    service = Vizier(columns=["**", "+_r"], row_limit=50)
    tables = service.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    best = None
    catalog_count = len(tables)
    total_rows = 0
    for table in tables:
        total_rows += len(table)
        catalog = clean(table.meta.get("name")) or clean(table.meta.get("ID")) or "VizieR catalog"
        for row in table:
            separation = number(row_value(row, "_r"))
            ra = number(row_value(row, "RA_ICRS", "RAJ2000", "RAdeg", "RA"))
            dec = number(row_value(row, "DE_ICRS", "DEJ2000", "DEdeg", "DEC", "Dec"))
            if ra is None or dec is None:
                continue
            if separation is None:
                separation = center.separation(SkyCoord(ra * u.deg, dec * u.deg, frame="icrs")).arcsec
            id_value, id_column = first_matching_column(
                row,
                [
                    lambda name: name in {"name", "id", "source", "objid", "recno"},
                    lambda name: name.endswith("id"),
                    lambda name: "name" in name,
                ],
            )
            mag_value, mag_column = first_matching_column(
                row,
                [lambda name: "mag" in name],
            )
            name = clean(id_value) or f"{catalog} row 1"
            candidate = {
                "catalog": "VizieR",
                "catalog_id": catalog,
                "name": name,
                "ra": ra,
                "dec": dec,
                "otype": "VizieR catalog source",
                "size": "Not available",
                "velocity": None,
                "z": None,
                "magnitude": (
                    f"{clean(mag_value)} ({mag_column})" if clean(mag_value) is not None else "Not available"
                ),
                "separation": separation,
                "url": vizier_url(catalog, ra, dec),
                "thumbnail": cutout_url(ra, dec),
                "info": f"Closest VizieR row; catalog: {catalog}; catalogs matched: {catalog_count}; rows matched: {total_rows}",
            }
            if best is None or candidate["separation"] < best["separation"]:
                best = candidate
    return best, total_rows


def fmt(value, digits=3):
    return "Not available" if value is None else f"{float(value):,.{digits}f}"


def row_html(item):
    if item is None:
        return ""
    distance = distance_from_z(item.get("z"))
    z_distance = "Not available"
    if item.get("z") is not None:
        z_distance = f"{item['z']:.6f}"
        if distance is not None:
            z_distance += f" / {distance / 1e9:.6f} billion ly"
    velocity = "Not available" if item.get("velocity") is None else f"{item['velocity']:,.3f} km/s"
    name = html.escape(str(item["name"]), quote=True)
    url = html.escape(str(item["url"]), quote=True)
    thumbnail = html.escape(str(item["thumbnail"]), quote=True)
    return f"""
    <tr>
      <td>
        <a class="object-link" href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>
        <div class="thumb-wrap"><a href="{url}" target="_blank" rel="noopener noreferrer"><img class="thumb" src="{thumbnail}" alt="{item['catalog']} preview"></a></div>
      </td>
      <td class="mono">{item['ra']:.6f} {item['dec']:.6f}</td>
      <td>{html.escape(str(item['otype']))}<br>{html.escape(str(item['size']))}</td>
      <td>{html.escape(velocity)}</td>
      <td>{html.escape(z_distance)}</td>
      <td>{html.escape(str(item['magnitude']))}</td>
      <td>{fmt(item.get('separation'), 3)} arcsec</td>
      <td>{html.escape(str(item['info']))}</td>
    </tr>
    """


center = SkyCoord(SEARCH_RA_DEG * u.deg, SEARCH_DEC_DEG * u.deg, frame="icrs")
print(f"DEV-0004 bridge search at {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f} with a 30 arcsecond cone...")

simbad_result, simbad_count = fetch_simbad(center)
ned_result, ned_count = fetch_ned(center)
vizier_result, vizier_count = fetch_vizier(center)

results = [
    simbad_result or {
        "catalog": "SIMBAD", "name": "No SIMBAD match", "ra": SEARCH_RA_DEG, "dec": SEARCH_DEC_DEG,
        "otype": "Not available", "size": "Not available", "velocity": None, "z": None,
        "magnitude": "Not available", "separation": None, "url": simbad_url(f"{SEARCH_RA_DEG} {SEARCH_DEC_DEG}"),
        "thumbnail": cutout_url(SEARCH_RA_DEG, SEARCH_DEC_DEG), "info": "No SIMBAD match within 30 arcseconds",
    },
    ned_result or {
        "catalog": "NED", "name": "No NED match", "ra": SEARCH_RA_DEG, "dec": SEARCH_DEC_DEG,
        "otype": "Not available", "size": "Not available", "velocity": None, "z": None,
        "magnitude": "Not available", "separation": None, "url": ned_url(f"{SEARCH_RA_DEG} {SEARCH_DEC_DEG}"),
        "thumbnail": cutout_url(SEARCH_RA_DEG, SEARCH_DEC_DEG), "info": "No NED match within 30 arcseconds",
    },
    vizier_result or {
        "catalog": "VizieR", "name": "No VizieR match", "ra": SEARCH_RA_DEG, "dec": SEARCH_DEC_DEG,
        "otype": "Not available", "size": "Not available", "velocity": None, "z": None,
        "magnitude": "Not available", "separation": None,
        "url": vizier_url("", SEARCH_RA_DEG, SEARCH_DEC_DEG),
        "thumbnail": cutout_url(SEARCH_RA_DEG, SEARCH_DEC_DEG), "info": "No VizieR match within 30 arcseconds",
    },
]

rows = "".join(row_html(item) for item in results)
debug_lines = [
    "DEV-0004 DEBUG SUMMARY",
    "======================",
    f"Search center: {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}",
    f"Radius: {SEARCH_RADIUS_ARCSEC:.1f} arcsec",
    f"SIMBAD candidates: {simbad_count}",
    f"NED candidates: {ned_count}",
    f"VizieR rows across matched catalogs: {vizier_count}",
    "",
]
for item in results:
    debug_lines.extend([
        item["catalog"],
        "-" * len(item["catalog"]),
        f"name: {item['name']}",
        f"coordinates: {item['ra']:.6f} {item['dec']:.6f}",
        f"separation_arcsec: {item.get('separation')}",
        f"object_url: {item['url']}",
        "thumbnail: external image URL omitted from debug output",
        f"information: {item['info']}",
        "",
    ])

debug_text = html.escape("\n".join(debug_lines))

page = f"""
<div id="dev0004-root">
<style>
#dev0004-root{{background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;padding:14px;border:1px solid #0b4f6c;border-radius:10px;max-width:1500px;margin:auto}}
#dev0004-root h3,#dev0004-root h4{{color:#35c6ff}}
#dev0004-root .table-wrap{{overflow-x:auto;border:1px solid #0b526f;border-radius:8px}}
#dev0004-root table{{width:100%;border-collapse:collapse;background:#000;color:#7FDBFF;font-size:14px}}
#dev0004-root th{{background:#031723;color:#43d2ff;border:1px solid #116482;padding:9px;text-align:left}}
#dev0004-root td{{background:#000;color:#7FDBFF;border:1px solid #0b506b;padding:8px;vertical-align:top}}
#dev0004-root .object-link{{color:#58d7ff;font-weight:700;text-decoration:none}}
#dev0004-root .thumb-wrap{{margin-top:8px}}
#dev0004-root .thumb{{width:150px;height:105px;object-fit:cover;border:1px solid #137aa3;border-radius:7px;background:#02080d}}
#dev0004-root .mono{{font-family:Consolas,Menlo,monospace}}
#dev0004-root pre{{white-space:pre-wrap;word-break:break-word;background:#02080d;color:#9fe8ff;border:1px solid #0b526f;border-radius:8px;padding:12px;max-height:900px;overflow:auto}}
</style>
<h3>DEV-0004 - SIMBAD / NED / VizieR bridge</h3>
<p>General 30-arcsecond cone search at {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}. Exactly three rows are displayed in catalog order.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Object name</th><th>RA / Dec</th><th>Object type / Size</th><th>Velocity</th><th>Redshift / Distance</th><th>Magnitude / Filter</th><th>Angular separation</th><th>Information</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<h4>Plain-text debug summary</h4>
<pre>{debug_text}</pre>
</div>
"""

display(HTML(page))
