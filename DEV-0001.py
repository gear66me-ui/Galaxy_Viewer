from __future__ import annotations

from io import BytesIO, StringIO
from urllib.parse import quote, urljoin
import base64
import html
import math
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageStat
from IPython.display import HTML, display

SEARCH_RA_DEG = 53.172576
SEARCH_DEC_DEG = -27.796392
SEARCH_RADIUS_ARCSEC = 6.0

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 GalaxyViewer DEV-0001",
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
    text = re.sub(r"\s+", " ", str(value)).strip()
    return None if not text or text.lower() in {"nan", "none", "null", "...", "n/a"} else text


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


def sexagesimal_ra(value):
    text = clean(value)
    if text is None:
        return None
    direct = number(text)
    if direct is not None and not re.search(r"[hms:]", text, re.I):
        return direct
    match = re.search(r"(\d+)\s*[h:]\s*(\d+)\s*[m:]\s*([\d.]+)", text, re.I)
    if not match:
        return None
    return 15.0 * (float(match[1]) + float(match[2]) / 60.0 + float(match[3]) / 3600.0)


def sexagesimal_dec(value):
    text = clean(value)
    if text is None:
        return None
    direct = number(text)
    if direct is not None and not re.search(r"[dms:]", text, re.I):
        return direct
    match = re.search(r"([+-]?)\s*(\d+)\s*[d:]\s*(\d+)\s*[m:]\s*([\d.]+)", text, re.I)
    if not match:
        return None
    sign = -1.0 if match[1] == "-" else 1.0
    return sign * (float(match[2]) + float(match[3]) / 60.0 + float(match[4]) / 3600.0)


def simbad_object_url(name):
    return "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=" + quote(name)


def ned_object_url(name):
    return "https://ned.ipac.caltech.edu/byname?objname=" + quote(name)


def ned_image_service_url(name):
    return (
        "https://ned.ipac.caltech.edu/imageservice"
        "?search_type=Near%20Name%20Search&objname=" + quote(name)
    )


def fetch_simbad():
    radius_deg = SEARCH_RADIUS_ARCSEC / 3600.0
    query = f"""
    SELECT TOP 20 main_id,ra,dec,otype,sp_type,rvz_redshift,rvz_radvel,
           galdim_majaxis,galdim_minaxis,nbref,
           DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',{SEARCH_RA_DEG},{SEARCH_DEC_DEG})) AS separation
    FROM basic
    WHERE 1=CONTAINS(
      POINT('ICRS',ra,dec),
      CIRCLE('ICRS',{SEARCH_RA_DEG},{SEARCH_DEC_DEG},{radius_deg})
    )
    ORDER BY separation ASC
    """
    response = SESSION.get(
        "https://simbad.cds.unistra.fr/simbad/sim-tap/sync",
        params={"request": "doQuery", "lang": "adql", "format": "json", "query": query},
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    metadata = [item["name"] for item in payload.get("metadata", [])]
    rows = [dict(zip(metadata, row)) for row in payload.get("data", [])]
    return rows


def fetch_ned():
    url = (
        "https://ned.ipac.caltech.edu/cgi-bin/objsearch"
        "?search_type=Near+Position+Search"
        "&in_csys=Equatorial&in_equinox=J2000.0"
        f"&lon={SEARCH_RA_DEG}d&lat={SEARCH_DEC_DEG}d"
        "&radius=0.1&hconst=73&omegam=0.27&omegav=0.73&corr_z=1"
        "&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z"
        "&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes2=Galaxies"
        "&out_csys=Equatorial&out_equinox=J2000.0"
        "&obj_sort=Distance+to+search+center&of=table"
    )
    response = SESSION.get(url, timeout=90)
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text), header=None)
    selected = None
    for frame in tables:
        if frame.empty or frame.shape[1] < 10:
            continue
        first = frame.iloc[:, 0].astype(str).str.strip()
        mask = first.str.fullmatch(r"\d+")
        if mask.sum() >= 1:
            selected = frame.loc[mask].copy()
            break
    if selected is None or selected.empty:
        return []
    results = []
    for _, row in selected.iterrows():
        cells = [clean(value) for value in row.tolist()]
        results.append({
            "main_id": cells[1] if len(cells) > 1 else None,
            "ra": sexagesimal_ra(cells[2] if len(cells) > 2 else None),
            "dec": sexagesimal_dec(cells[3] if len(cells) > 3 else None),
            "otype": cells[4] if len(cells) > 4 else None,
            "rvz_radvel": None if (len(cells) > 5 and cells[5] and re.search(r"[<>]", cells[5])) else number(cells[5] if len(cells) > 5 else None),
            "rvz_redshift": number(cells[6] if len(cells) > 6 else None),
            "magnitude_filter": cells[8] if len(cells) > 8 else None,
            "angular_separation_arcmin": number(cells[9] if len(cells) > 9 else None),
            "_raw": cells,
        })
    return results


def candidate_text(candidate):
    return " ".join([
        candidate.get("url", ""), candidate.get("source_url", ""),
        candidate.get("alt", ""), candidate.get("title", ""),
        candidate.get("class_text", ""), candidate.get("parent_text", ""),
    ]).lower()


def add_candidate(candidates, seen, url, page_url, source_url=None, alt="", title="", class_text="", parent_text=""):
    if not url:
        return
    absolute = urljoin(page_url, url.strip())
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


print(f"Searching SIMBAD and NED at {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}...")
simbad_rows = fetch_simbad()
ned_rows = fetch_ned()

selected_rows = []
if simbad_rows:
    obj = simbad_rows[0]
    name = clean(obj.get("main_id")) or "Not available"
    object_url = simbad_object_url(name)
    thumb = best_thumbnail([object_url])
    selected_rows.append({"catalog": "SIMBAD", "object": obj, "name": name, "object_url": object_url,
                          "thumbnail": thumb, "candidates": len(simbad_rows)})
if ned_rows:
    obj = ned_rows[0]
    name = clean(obj.get("main_id")) or "Not available"
    object_url = ned_object_url(name)
    thumb = best_thumbnail([object_url, ned_image_service_url(name)])
    selected_rows.append({"catalog": "NED", "object": obj, "name": name, "object_url": object_url,
                          "thumbnail": thumb, "candidates": len(ned_rows)})

rows_html = ""
for item in selected_rows:
    obj = item["object"]
    catalog = item["catalog"]
    ra = number(obj.get("ra"))
    dec = number(obj.get("dec"))
    z = number(obj.get("rvz_redshift"))
    velocity = number(obj.get("rvz_radvel"))
    if catalog == "SIMBAD":
        separation = number(obj.get("separation"))
        separation_arcsec = separation * 3600.0 if separation is not None else None
    else:
        separation_arcmin = number(obj.get("angular_separation_arcmin"))
        separation_arcsec = separation_arcmin * 60.0 if separation_arcmin is not None else None
    magnitude = clean(obj.get("magnitude_filter")) or "Not available"
    size_text = "Not available"
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
    info = f"Catalog: {catalog}<br>Selection: {catalog} row 1<br>Candidates: {item['candidates']}"
    rows_html += f'''<tr><td>{object_link}<div class="thumbnail-container">{thumb_html}</div></td><td class="coordinates">{coordinates}</td><td>{esc(clean(obj.get("otype")) or "Not available")}<br>{size_text}</td><td>{velocity_text}</td><td>{redshift_text}</td><td>{esc(magnitude)}</td><td>{separation_text}</td><td>{info}</td></tr>'''

if not rows_html:
    rows_html = '<tr><td colspan="8" style="text-align:center">No SIMBAD or NED match found.</td></tr>'

preview = f'''
<div id="dev0001-preview">
<style>
#dev0001-preview{{box-sizing:border-box;width:100%;max-width:1180px;margin:0 auto;padding:14px;background:#000;color:#7FDBFF;font-family:Arial,Helvetica,sans-serif;border:1px solid #0b4f6c;border-radius:10px;box-shadow:0 0 18px rgba(0,174,239,.18)}}
#dev0001-preview h4{{color:#35c6ff;margin:4px 0 10px}}
#dev0001-preview .table-wrap{{overflow-x:auto;border:1px solid #0b526f;border-radius:8px;background:#000}}
#dev0001-preview table{{width:100%;min-width:1040px;border-collapse:collapse;background:#000;color:#7FDBFF;font-size:14px}}
#dev0001-preview thead tr{{background:#031723}}
#dev0001-preview th{{padding:9px;color:#43d2ff;font-weight:700;text-align:left;vertical-align:top;border:1px solid #116482}}
#dev0001-preview td{{padding:8px;color:#7FDBFF;background:#000;border:1px solid #0b506b;vertical-align:top;line-height:1.45}}
#dev0001-preview tbody tr:nth-child(even) td{{background:#020b10}}
#dev0001-preview th:nth-child(1),#dev0001-preview td:nth-child(1){{width:170px;min-width:170px;max-width:170px}}
#dev0001-preview th:nth-child(2),#dev0001-preview td:nth-child(2){{width:135px;min-width:135px;max-width:135px}}
#dev0001-preview .object-link{{display:inline-block;color:#58d7ff;font-weight:700;text-decoration:none;border-bottom:1px dotted rgba(88,215,255,.65)}}
#dev0001-preview .object-link:hover{{color:#a6eeff;text-shadow:0 0 8px rgba(67,210,255,.75)}}
#dev0001-preview .thumbnail-container{{margin-top:10px}}
#dev0001-preview .thumbnail-link{{display:block;width:150px;text-decoration:none}}
#dev0001-preview .catalog-thumbnail{{display:block;width:150px;height:105px;object-fit:cover;background:#02080d;border:1px solid #137aa3;border-radius:7px;box-shadow:0 0 10px rgba(0,174,239,.20);cursor:pointer}}
#dev0001-preview .thumbnail-link:hover .catalog-thumbnail{{border-color:#58d7ff;box-shadow:0 0 14px rgba(67,210,255,.48);transform:scale(1.018)}}
#dev0001-preview .thumbnail-caption{{width:150px;margin-top:5px;color:#61b9d5;font-size:10px;line-height:1.3;text-align:center}}
#dev0001-preview .thumbnail-placeholder{{display:flex;flex-direction:column;align-items:center;justify-content:center;width:150px;height:105px;box-sizing:border-box;color:#79cce8;background:linear-gradient(135deg,#02080d,#031723);border:1px dashed #137aa3;border-radius:7px;text-align:center}}
#dev0001-preview .coordinates{{font-family:Consolas,Menlo,Monaco,monospace;white-space:nowrap}}
#dev0001-preview .coord-label{{display:inline-block;width:28px;color:#43d2ff;font-weight:700}}
#dev0001-preview .note{{margin-top:10px;color:#61b9d5;font-size:12px;line-height:1.45}}
</style>
<h4>DEV-0001 — Object figures of merit</h4>
<div class="table-wrap"><table><thead><tr><th>Object name</th><th>RA / Dec</th><th>Object type / Size</th><th>Velocity</th><th>Redshift / Distance</th><th>Magnitude / Filter</th><th>Angular separation</th><th>Information</th></tr></thead><tbody>{rows_html}</tbody></table></div>
<div class="note">Search coordinate: {SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}. Clicking either an object name or thumbnail opens the corresponding catalog record in a new tab. No magnitude-derived size calculation is used.</div>
</div>
'''

display(HTML(preview))

print("\nDEV-0001 DEBUG")
print("=" * 72)
print("Search coordinate:", f"{SEARCH_RA_DEG:.6f} {SEARCH_DEC_DEG:.6f}")
print("SIMBAD rows:", len(simbad_rows))
print("NED rows:", len(ned_rows))
for item in selected_rows:
    print(f"\n{item['catalog']} row 1")
    print("Object:", item["name"])
    print("Object page:", item["object_url"])
    if item["thumbnail"]:
        print("Thumbnail:", item["thumbnail"]["final_url"])
        print("Dimensions:", f"{item['thumbnail']['width']} × {item['thumbnail']['height']}")
    else:
        print("Thumbnail: unavailable")
    print("Raw row:", item["object"])
