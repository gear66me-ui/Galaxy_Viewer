from __future__ import annotations

import urllib.request

BASE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "2ff37125d994a920b5e15ca4aac97a094ed0bc46/GV-0058.py"
)

with urllib.request.urlopen(BASE_URL, timeout=90) as response:
    source = response.read().decode("utf-8")

source = source.replace("GV-0058", "GV-0059").replace("gv0058", "gv0059")

old_import = "import urllib.request\n\nimport pandas as pd"
new_import = '''import urllib.request
from io import BytesIO
from urllib.parse import quote, urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageStat'''
if old_import not in source:
    raise RuntimeError("GV-0059 import patch target not found")
source = source.replace(old_import, new_import, 1)

helper_anchor = "def _encode_rows(rows):\n"
helper_code = r'''PREVIEW_SESSION = requests.Session()
PREVIEW_SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 GalaxyViewer GV-0059",
    "Accept": "text/html,application/xhtml+xml,image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
})

_PREVIEW_REJECT = {
    "envelope", "email", "mail", "contact", "logo", "icon", "favicon",
    "facebook", "twitter", "youtube", "github", "spinner", "loading",
    "blank", "transparent", "pixel", "button", "arrow", "help", "home",
    "survey_logo", "masthead", "banner",
}
_PREVIEW_ASTRONOMY = {
    "postage", "stamp", "preview", "thumbnail", "thumb", "dss", "sky",
    "finder", "cutout", "image", "jpeg", "jpg", "gif", "fits", "firefly",
}


def _catalog_url(catalog, name):
    if catalog == "SIMBAD":
        return "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=" + quote(str(name))
    return "https://ned.ipac.caltech.edu/byname?objname=" + quote(str(name))


def _ned_image_service_url(name):
    return (
        "https://ned.ipac.caltech.edu/imageservice"
        "?search_type=Near%20Name%20Search&objname=" + quote(str(name))
    )


def _preview_text(candidate):
    return " ".join([
        candidate.get("url", ""), candidate.get("source_url", ""),
        candidate.get("alt", ""), candidate.get("title", ""),
        candidate.get("class_text", ""), candidate.get("parent_text", ""),
    ]).lower()


def _add_preview_candidate(candidates, seen, url, page_url, source_url=None,
                           alt="", title="", class_text="", parent_text=""):
    if not url:
        return
    absolute = urljoin(page_url, str(url).strip())
    if absolute.startswith("data:") or absolute in seen:
        return
    seen.add(absolute)
    candidates.append({
        "url": absolute,
        "source_url": source_url or absolute,
        "page_url": page_url,
        "alt": alt or "",
        "title": title or "",
        "class_text": class_text or "",
        "parent_text": parent_text or "",
    })


def _discover_preview_candidates(page_url):
    response = PREVIEW_SESSION.get(page_url, timeout=60, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    candidates, seen = [], set()
    for image_tag in soup.find_all("img"):
        sources = [
            image_tag.get(key)
            for key in ("src", "data-src", "data-lazy-src", "data-original")
            if image_tag.get(key)
        ]
        if image_tag.get("srcset"):
            sources.extend(
                part.strip().split(" ")[0]
                for part in image_tag["srcset"].split(",")
                if part.strip()
            )
        parent = image_tag.find_parent("a", href=True)
        parent_href = parent.get("href") if parent else None
        parent_text = parent.get_text(" ", strip=True) if parent else ""
        for item in sources:
            _add_preview_candidate(
                candidates, seen, item, response.url, parent_href,
                image_tag.get("alt", ""), image_tag.get("title", ""),
                " ".join(image_tag.get("class", [])), parent_text,
            )
        if parent_href:
            _add_preview_candidate(
                candidates, seen, parent_href, response.url, parent_href,
                image_tag.get("alt", ""), parent.get("title", ""),
                " ".join(parent.get("class", [])), parent_text,
            )
    for link in soup.find_all("a", href=True):
        text = " ".join([
            link.get("href", ""), link.get_text(" ", strip=True),
            link.get("title", ""), " ".join(link.get("class", [])),
        ]).lower()
        if any(word in text for word in _PREVIEW_ASTRONOMY):
            _add_preview_candidate(
                candidates, seen, link["href"], response.url, link["href"],
                link.get_text(" ", strip=True), link.get("title", ""),
                " ".join(link.get("class", [])), "",
            )
    return candidates


def _inspect_preview(candidate):
    text = _preview_text(candidate)
    if any(word in text for word in _PREVIEW_REJECT):
        return None
    try:
        response = PREVIEW_SESSION.get(
            candidate["url"], timeout=50, allow_redirects=True,
            headers={"Referer": candidate["page_url"]},
        )
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if not content_type.startswith("image/") or content_type == "image/svg+xml":
            return None
        if len(response.content) < 1000:
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
        if any(word in text for word in _PREVIEW_ASTRONOMY):
            score += 160.0
        if "postage" in text or "stamp" in text:
            score += 240.0
        if "dss" in text or "finder" in text:
            score += 180.0
        if "preview" in text or "thumbnail" in text:
            score += 100.0
        if dynamic_range > 30:
            score += 80.0
        if variance > 100:
            score += 80.0
        score += min(width, 1200) / 20.0 + min(height, 1200) / 20.0
        encoded = base64.b64encode(response.content).decode("ascii")
        return {
            "thumbnail_data_uri": f"data:{content_type};base64,{encoded}",
            "thumbnail_width": width,
            "thumbnail_height": height,
            "thumbnail_source": response.url,
            "score": score,
        }
    except Exception:
        return None


def _best_preview(page_urls):
    candidates = []
    for page_url in page_urls:
        try:
            candidates.extend(_discover_preview_candidates(page_url))
        except Exception:
            pass
    unique, seen = [], set()
    for candidate in candidates:
        if candidate["url"] not in seen:
            seen.add(candidate["url"])
            unique.append(candidate)
    verified = []
    for candidate in unique[:50]:
        result = _inspect_preview(candidate)
        if result is not None:
            verified.append(result)
    verified.sort(key=lambda item: item["score"], reverse=True)
    return verified[0] if verified else None


def _enrich_first_row(rows, catalog):
    if not rows:
        return rows
    first = rows[0]
    name = first.get("main_id") or "Not available"
    object_url = _catalog_url(catalog, name)
    first["object_url"] = object_url
    pages = [object_url]
    if catalog == "NED":
        pages.append(_ned_image_service_url(name))
    preview = _best_preview(pages)
    if preview:
        first.update(preview)
    return rows


def _encode_rows(rows, catalog=None):
'''
if helper_anchor not in source:
    raise RuntimeError("GV-0059 helper anchor not found")
source = source.replace(helper_anchor, helper_code, 1)

source = source.replace("return _encode_rows([])", "return _encode_rows([], \"SIMBAD\")", 1)
source = source.replace("return _encode_rows(rows)", "return _encode_rows(_enrich_first_row(rows, \"SIMBAD\"), \"SIMBAD\")", 1)
source = source.replace("return _encode_rows([])", "return _encode_rows([], \"NED\")", 1)
source = source.replace("return _encode_rows([result])", "return _encode_rows(_enrich_first_row([result], \"NED\"), \"NED\")", 1)

old_css = "#gv0011-root .small-note{margin-top:10px;font-size:12px;color:#61b9d5;line-height:1.45}"
new_css = old_css + '''
#gv0011-root .object-link{display:inline-block;color:#58d7ff;font-weight:700;text-decoration:none;border-bottom:1px dotted rgba(88,215,255,.65)}
#gv0011-root .object-link:hover{color:#a6eeff;text-shadow:0 0 8px rgba(67,210,255,.75)}
#gv0011-root .thumbnail-container{margin-top:10px}
#gv0011-root .thumbnail-link{display:block;width:150px;text-decoration:none}
#gv0011-root .catalog-thumbnail{display:block;width:150px;height:105px;object-fit:cover;background:#02080d;border:1px solid #137aa3;border-radius:7px;box-shadow:0 0 10px rgba(0,174,239,.20);cursor:pointer}
#gv0011-root .thumbnail-link:hover .catalog-thumbnail{border-color:#58d7ff;box-shadow:0 0 14px rgba(67,210,255,.48);transform:scale(1.018)}
#gv0011-root .thumbnail-caption{width:150px;margin-top:5px;color:#61b9d5;font-size:10px;line-height:1.3;text-align:center}
#gv0011-root .thumbnail-placeholder{display:flex;align-items:center;justify-content:center;width:150px;height:105px;box-sizing:border-box;color:#79cce8;background:linear-gradient(135deg,#02080d,#031723);border:1px dashed #137aa3;border-radius:7px;text-align:center}'''
if old_css not in source:
    raise RuntimeError("GV-0059 CSS patch target not found")
source = source.replace(old_css, new_css, 1)

old_result = 'return`<tr><td>${safe(name)}</td><td style="font-family:monospace">${ra} ${de}</td>'
new_result = '''const objectUrl=o.object_url||"#",objectLink=`<a class="object-link" href="${safe(objectUrl)}" target="_blank" rel="noopener noreferrer">${safe(name)} <span>↗</span></a>`,thumb=o.thumbnail_data_uri?`<a class="thumbnail-link" href="${safe(objectUrl)}" target="_blank" rel="noopener noreferrer"><img class="catalog-thumbnail" src="${o.thumbnail_data_uri}" alt="${safe(c)} preview"></a><div class="thumbnail-caption">${safe(c)} native preview<br>${safe(o.thumbnail_width)} × ${safe(o.thumbnail_height)} px</div>`:`<a class="thumbnail-link" href="${safe(objectUrl)}" target="_blank" rel="noopener noreferrer"><div class="thumbnail-placeholder">Preview unavailable<br><small>Open ${safe(c)} record</small></div></a>`;return`<tr><td>${objectLink}<div class="thumbnail-container">${thumb}</div></td><td style="font-family:monospace">${ra} ${de}</td>'''
if old_result not in source:
    raise RuntimeError("GV-0059 result-row patch target not found")
source = source.replace(old_result, new_result, 1)

old_note = "GV-0059 uses the approved DEV-0003 official SIMBAD and NED catalog routines."
new_note = "GV-0059 preserves the approved DEV-0003 official SIMBAD and NED catalog routines and restores clickable catalog hotlinks and thumbnails."
if old_note not in source:
    raise RuntimeError("GV-0059 note patch target not found")
source = source.replace(old_note, new_note, 1)

exec(compile(source, "GV-0059.py", "exec"))
