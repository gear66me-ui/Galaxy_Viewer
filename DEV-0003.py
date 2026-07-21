from __future__ import annotations

import sys
import subprocess
import math
import html
import re
import base64
from io import BytesIO
from urllib.parse import quote, urljoin

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

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageStat
from IPython.display import HTML, display

SEARCH_RA_DEG = 53.172576
SEARCH_DEC_DEG = -27.796392
SEARCH_RADIUS_ARCSEC = 30.0

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 GalaxyViewer DEV-0003",
    "Accept": "text/html,application/xhtml+xml,image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
})

REJECT_WORDS = {
    "envelope", "email", "mail", "contact", "logo", "icon", "favicon",
    "facebook", "twitter", "youtube", "github", "spinner", "loading",
    "blank", "transparent", "pixel", "button", "arrow", "help", "home",
    "survey_logo", "masthead", "banner",
}
ASTRONOMY_WORDS = {
    "postage", "stamp", "preview", "thumbnail", "thumb", "dss", "sky",
    "finder", "cutout", "image", "jpeg", "jpg", "gif", "fits", "firefly",
}


def esc(value):
    return html.escape(str(value), quote=True)


def clean(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if hasattr(value, "mask") and bool(getattr(value, "mask", False)):
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return None if not text or text.lower() in {"nan", "none", "null", "...", "n/a", "--"} else text


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


def table_value(row, *names):
    columns = {str(name).casefold(): name for name in row.colnames}
    for requested in names:
        actual = columns.get(str(requested).casefold())
        if actual is not None:
            value = row[actual]
            if clean(value) is not None:
                return value
    return None


def simbad_object_url(name):
    return "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=" + quote(name)


def ned_object_url(name):
    return "https://ned.ipac.caltech.edu/byname?objname=" + quote(name)


def ned_image_service_url(name):
    return (
        "https://ned.ipac.caltech.edu/imageservice"
        "?search_type=Near%20Name%20Search&objname=" + quote(name)
    )


def fetch_simbad_official():
    simbad = Simbad()
    simbad.ROW_LIMIT = 20
    requested = ["otype", "sp_type", "velocity", "dimensions", "U", "B", "V", "R", "I"]
    accepted = []
    for field in requested:
        try:
            simbad.add_votable_fields(field)
            accepted.append(field)
        except Exception:
            pass

    center = SkyCoord(SEARCH_RA_DEG * u.deg, SEARCH_DEC_DEG * u.deg, frame="icrs")
    table = simbad.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return [], accepted

    object_coords = SkyCoord(table["ra"], table["dec"], unit=(u.deg, u.deg), frame="icrs")
    separations = center.separation(object_coords).arcsec
    table["_gv_separation_arcsec"] = separations
    table.sort("_gv_separation_arcsec")
    return table, accepted


def fetch_ned_official():
    center = SkyCoord(SEARCH_RA_DEG * u.deg, SEARCH_DEC_DEG * u.deg, frame="icrs")
    table = Ned.query_region(center, radius=SEARCH_RADIUS_ARCSEC * u.arcsec)
    if table is None or len(table) == 0:
        return []

    ra_column = None
    dec_column = None
    for candidate in ("RA", "ra"):
        if candidate in table.colnames:
            ra_column = candidate
            break
    for candidate in ("DEC", "Dec", "dec"):
        if candidate in table.colnames:
            dec_column = candidate
            break
    if ra_column and dec_column:
        object_coords = SkyCoord(table[ra_column], table[dec_column], unit=(u.deg, u.deg), frame="icrs")
        table["_gv_separation_arcsec"] = center.separation(object_coords).arcsec
        table.sort("_gv_separation_arcsec")
    return table


def ned_detail_tables(name):
    details = {}
    for table_name in ("photometry", "diameters", "redshifts", "positions", "references", "object_notes"):
        try:
            table = Ned.get_table(name, table=table_name)
            details[table_name] = table
        except Exception as error:
            details[table_name] = error
    try:
        details["image_urls"] = Ned.get_image_list(name)
    except Exception as error:
        details["image_urls"] = error
    try:
        details["spectrum_urls"] = Ned.get_image_list(name, item="spectra", file_format="fits")
    except Exception as error:
        details["spectrum_urls"] = error
    return details


def candidate_text(candidate):
    return " ".join([
        candidate.get("url", ""), candidate.get("source_url", ""),
        candidate.get("alt", ""), candidate.get("title", ""),
        candidate.get("class_text", ""), candidate.get("parent_text", ""),
    ]).lower()


def add_candidate(candidates, seen, url, page_url, source_url=None, alt="", title="", class_text="", parent_text=""):
    if not url:
        return
    absolute = urljoin(page_url, str(url).strip())
    if absolute.startswith("data:") or absolute in seen:
        return
    seen.add(absolute)
    candidates.append({
        "url": absolute, "source_url": source_url or absolute, "page_url": page_url,
        "alt": alt or "", "title": title or "", "class_text": class_text or "",
        "parent_text": parent_text or "",
    })


def discover_images(page_url):
    response = SESSION.get(page_url, timeout=60, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    candidates, seen = [], set()
    for image_tag in soup.find_all("img"):
        sources = [image_tag.get(key) for key in ("src", "data-src", "data-lazy-src", "data-original") if image_tag.get(key)]
        if image_tag.get("srcset"):
            sources += [part.strip().split(" ")[0] for part in image_tag["srcset"].split(",") if part.strip()]
        parent = image_tag.find_parent("a", href=True)
        parent_href = parent.get("href") if parent else None
        parent_text = parent.get_text(" ", strip=True) if parent else ""
        for source in sources:
            add_candidate(candidates, seen, source, response.url, parent_href,
                          image_tag.get("alt", ""), image_tag.get("title", ""),
                          " ".join(image_tag.get("class", [])), parent_text)
        if parent_href:
            add_candidate(candidates, seen, parent_href, response.url, parent_href,
                          image_tag.get("alt", ""), parent.get("title", ""),
                          " ".join(parent.get("class", [])), parent_text)
    for link in soup.find_all("a", href=True):
        text = " ".join([link.get("href", ""), link.get_text(" ", strip=True), link.get("title", ""), " ".join(link.get("class", []))]).lower()
        if any(word in text for word in ASTRONOMY_WORDS):
            add_candidate(candidates, seen, link["href"], response.url, link["href"],
                          link.get_text(" ", strip=True), link.get("title", ""),
                          " ".join(link.get("class", [])), "")
    return candidates


def inspect_image(candidate):
    text = candidate_text(candidate)
    if any(word in text for word in REJECT_WORDS):
        return None
    try:
        response = SESSION.get(candidate["url"], timeout=50, allow_redirects=True,
                               headers={"Referer": candidate["page_url"]})
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if not content_type.startswith("image/") or content_type == "image/svg+xml" or len(response.content) < 1000:
            return None
        image = Image.open(BytesIO(response.content))
        image.load()
        width, height = image.size
        if width < 70 or height < 70 or width * height < 10000:
            return None
        aspect = width / height
        if aspect < 0.35 or aspect > 3.5:
            return None
        sample = image.convert("RGB")
        sample.thumbnail((160, 160))
        stats = ImageStat.Stat(sample)
        dynamic_range = sum(high - low for low, high in stats.extrema) / 3.0
        variance = sum(stats.var) / 3.0
        score = math.log10(width * height) * 100.0
        if any(word in text for word in ASTRONOMY_WORDS): score += 160.0
        if "postage" in text or "stamp" in text: score += 240.0
        if "dss" in text or "finder" in text: score += 180.0
        if "preview" in text or "thumbnail" in text: score += 100.0
        if dynamic_range > 30: score += 80.0
        if variance > 100: score += 80.0
        score += min(width, 1200) / 20.0 + min(height, 1200) / 20.0
        return {**candidate, "final_url": response.url, "content_type": content_type,
                "bytes": response.content, "width": width, "height": height, "score": score}
    except Exception:
        return None


def best_thumbnail(page_urls):
    candidates = []
    for page_url in page_urls:
        try:
            candidates.extend(discover_images(page_url))
        except Exception:
            pass
    unique, seen = [], set()
    for candidate in candidates:
        if candidate["url"] not in seen:
            seen.add(candidate["url"])
            unique.append(candidate)
    verified = [result for candidate in unique[:50] if (result := inspect_image(candidate)) is not None]
    verified.sort(key=lambda item: item["score"], reverse=True)
    return verified[0] if verified else None


def data_uri(image_result):
    encoded = base64.b64encode(image_result["bytes"]).decode("ascii")
    return f"data:{image_result['content_type']};base64,{encoded}"


def magnitude_lines_from_simbad(row):
    values = []
    for band in ("U", "B", "V", "R", "I"):
        value = table_value(row, band)
        numeric = number(value)
        if numeric is not None:
            values.append(f"{band} {numeric:.4f}")
    return "<br>".join(values) if values else "Not available"


def simbad_size_text(row):
    major = number(table_value(row, "galdim_majaxis"))
    minor = number(table_value(row, "galdim_minaxis"))
    if major is None:
        return "Not available"
    if minor is None:
        return f"{major:.4f} arcmin"
    return f"{major:.4f} × {minor:.4f} arcmin"


def ned_summary_from_details(details):
    lines = []
    for key in ("photometry", "diameters", "redshifts"):
        value = details.get(key)
        if hasattr(value, "__len__") and not isinstance(value, Exception):
            lines.append(f"{key.title()}: {len(value)} row(s)")
        else:
            lines.append(f"{key.title()}: unavailable")
    images = details.get("image_urls")
    spectra = details.get("spectrum_urls")
    lines.append(f"FITS images: {len(images) if isinstance(images, list) else 0}")
    lines.append(f"FITS spectra: {len(spectra) if isinstance(spectra, list) else 0}")
    return "<br>".join(lines)


print(f"Searching official SIMBAD and NED interfaces at {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}...")
simbad_table, accepted_fields = fetch_simbad_official()
ned_table = fetch_ned_official()

selected_rows = []
if len(simbad_table):
    row = simbad_table[0]
    name = clean(table_value(row, "main_id")) or "Not available"
    object_url = simbad_object_url(name)
    selected_rows.append({
        "catalog": "SIMBAD", "row": row, "name": name, "object_url": object_url,
        "thumbnail": best_thumbnail([object_url]), "candidates": len(simbad_table), "details": None,
    })

if len(ned_table):
    row = ned_table[0]
    name = clean(table_value(row, "Object Name", "Object_Name", "object_name")) or "Not available"
    object_url = ned_object_url(name)
    details = ned_detail_tables(name)
    selected_rows.append({
        "catalog": "NED", "row": row, "name": name, "object_url": object_url,
        "thumbnail": best_thumbnail([object_url, ned_image_service_url(name)]),
        "candidates": len(ned_table), "details": details,
    })

rows_html = ""
for item in selected_rows:
    row = item["row"]
    catalog = item["catalog"]
    ra = number(table_value(row, "ra", "RA"))
    dec = number(table_value(row, "dec", "DEC", "Dec"))
    z = number(table_value(row, "rvz_redshift", "Redshift"))
    velocity = number(table_value(row, "rvz_radvel", "Velocity"))
    separation_arcsec = number(table_value(row, "_gv_separation_arcsec", "Separation"))

    if catalog == "SIMBAD":
        magnitude = magnitude_lines_from_simbad(row)
        size_text = simbad_size_text(row)
        otype = clean(table_value(row, "otype")) or "Not available"
        info_extra = "Official fields: " + ", ".join(accepted_fields)
    else:
        magnitude = clean(table_value(row, "Magnitude and Filter", "Magnitude", "Photometry Points")) or "See NED photometry table"
        size_text = "See NED diameter table" if hasattr(item["details"].get("diameters"), "__len__") else "Not available"
        otype = clean(table_value(row, "Type")) or "Not available"
        info_extra = ned_summary_from_details(item["details"])

    object_link = f'<a class="object-link" href="{esc(item["object_url"])}" target="_blank" rel="noopener noreferrer">{esc(item["name"])} <span>↗</span></a>'
    if item["thumbnail"]:
        thumb = item["thumbnail"]
        thumb_html = f'''<a class="thumbnail-link" href="{esc(item["object_url"])}" target="_blank" rel="noopener noreferrer"><img class="catalog-thumbnail" src="{data_uri(thumb)}" alt="{esc(catalog)} preview"></a><div class="thumbnail-caption">{esc(catalog)} native preview<br>{thumb["width"]} × {thumb["height"]} px</div>'''
    else:
        thumb_html = f'''<a class="thumbnail-link" href="{esc(item["object_url"])}" target="_blank" rel="noopener noreferrer"><div class="thumbnail-placeholder">Preview unavailable<br><small>Open {esc(catalog)} record</small></div></a>'''

    coordinates = f'<span class="coord-label">RA</span> {ra:.6f}<br><span class="coord-label">Dec</span> {dec:.6f}' if ra is not None and dec is not None else "Not available"
    velocity_text = f"{velocity:,.3f} km/s" if velocity is not None else "Not available"
    redshift_text = f"{z:.6f}" if z is not None else "Not available"
    separation_text = f"{separation_arcsec:.3f} arcsec" if separation_arcsec is not None else "Not available"
    info = f"Catalog: {catalog}<br>Selection: nearest official row<br>Candidates: {item['candidates']}<br>{info_extra}"

    rows_html += f'''<tr><td>{object_link}<div class="thumbnail-container">{thumb_html}</div></td><td class="coordinates">{coordinates}</td><td>{esc(otype)}<br>{esc(size_text)}</td><td>{velocity_text}</td><td>{redshift_text}</td><td>{magnitude}</td><td>{separation_text}</td><td>{info}</td></tr>'''

if not rows_html:
    rows_html = '<tr><td colspan="8" style="text-align:center">No SIMBAD or NED match found.</td></tr>'

preview = f'''
<div id="dev0003-preview">
<style>
#dev0003-preview{{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}}
#dev0003-preview h4{{color:#35c6ff;margin:4px 0 10px}}
#dev0003-preview .table-wrap{{overflow-x:auto;border:1px solid #0b526f;border-radius:8px;background:#000}}
#dev0003-preview table{{width:100%;min-width:1040px;border-collapse:collapse;background:#000;color:#7FDBFF;font-size:14px}}
#dev0003-preview thead tr{{background:#031723}}
#dev0003-preview th{{padding:9px;color:#43d2ff;font-weight:700;text-align:left;vertical-align:top;border:1px solid #116482}}
#dev0003-preview td{{padding:8px;color:#7FDBFF;background:#000;border:1px solid #0b506b;vertical-align:top;line-height:1.45}}
#dev0003-preview tbody tr:nth-child(even) td{{background:#020b10}}
#dev0003-preview th:nth-child(1),#dev0003-preview td:nth-child(1){{width:170px;min-width:170px;max-width:170px}}
#dev0003-preview th:nth-child(2),#dev0003-preview td:nth-child(2){{width:135px;min-width:135px;max-width:135px}}
#dev0003-preview .object-link{{display:inline-block;color:#58d7ff;font-weight:700;text-decoration:none;border-bottom:1px dotted rgba(88,215,255,.65)}}
#dev0003-preview .object-link:hover{{color:#a6eeff;text-shadow:0 0 8px rgba(67,210,255,.75)}}
#dev0003-preview .thumbnail-container{{margin-top:10px}}
#dev0003-preview .thumbnail-link{{display:block;width:150px;text-decoration:none}}
#dev0003-preview .catalog-thumbnail{{display:block;width:150px;height:105px;object-fit:cover;background:#02080d;border:1px solid #137aa3;border-radius:7px;box-shadow:0 0 10px rgba(0,174,239,.20);cursor:pointer}}
#dev0003-preview .thumbnail-link:hover .catalog-thumbnail{{border-color:#58d7ff;box-shadow:0 0 14px rgba(67,210,255,.48);transform:scale(1.018)}}
#dev0003-preview .thumbnail-caption{{width:150px;margin-top:5px;color:#61b9d5;font-size:10px;line-height:1.3;text-align:center}}
#dev0003-preview .thumbnail-placeholder{{display:flex;flex-direction:column;align-items:center;justify-content:center;width:150px;height:105px;box-sizing:border-box;color:#79cce8;background:linear-gradient(135deg,#02080d,#031723);border:1px dashed #137aa3;border-radius:7px;text-align:center}}
#dev0003-preview .coordinates{{font-family:Consolas,Menlo,Monaco,monospace;white-space:nowrap}}
#dev0003-preview .coord-label{{display:inline-block;width:28px;color:#43d2ff;font-weight:700}}
#dev0003-preview .note{{margin-top:10px;color:#61b9d5;font-size:12px;line-height:1.45}}
</style>
<h4>DEV-0003 — Official catalog routines comparison</h4>
<div class="table-wrap"><table><thead><tr><th>Object name</th><th>RA / Dec</th><th>Object type / Size</th><th>Velocity</th><th>Redshift / Distance</th><th>Magnitude / Filter</th><th>Angular separation</th><th>Information</th></tr></thead><tbody>{rows_html}</tbody></table></div>
<div class="note">Search coordinate: {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}. Same DEV-0001 interface and native-thumbnail behavior. Catalog data now comes from official Astroquery SIMBAD and NED routines. No magnitude-derived size calculation is used.</div>
</div>
'''

display(HTML(preview))

print("\nDEV-0003 DEBUG")
print("=" * 76)
print("Search coordinate:", f"{SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}")
print("Radius:", f"{SEARCH_RADIUS_ARCSEC:.1f} arcsec")
print("SIMBAD accepted fields:", accepted_fields)
print("SIMBAD rows:", len(simbad_table))
print("NED rows:", len(ned_table))
for item in selected_rows:
    print(f"\n{item['catalog']} selected row")
    print("Object:", item["name"])
    print("Object page:", item["object_url"])
    if item["thumbnail"]:
        print("Thumbnail:", item["thumbnail"]["final_url"])
        print("Thumbnail dimensions:", f"{item['thumbnail']['width']} × {item['thumbnail']['height']}")
    else:
        print("Thumbnail: unavailable")
    print("Columns:", list(item["row"].colnames))
    print("Raw row:", item["row"])
    if item["catalog"] == "NED":
        print("NED detail tables:")
        for key, value in item["details"].items():
            if isinstance(value, Exception):
                print(f"  {key}: ERROR — {value}")
            elif isinstance(value, list):
                print(f"  {key}: {len(value)} URL(s)")
            else:
                print(f"  {key}: {len(value)} row(s)")
