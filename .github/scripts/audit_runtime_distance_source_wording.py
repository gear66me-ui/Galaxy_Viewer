#!/usr/bin/env python3
"""Read-only audit of runtime distances against source-page distance wording.
Does not edit the runtime catalog. Produces CSV/JSON evidence for manual review.
"""
import csv, json, re, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from html import unescape
from datetime import datetime, timezone

RUNTIME = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0004.json")
OUT = Path("distance-source-wording-audit")
OUT.mkdir(exist_ok=True)
UA = "GalaxyViewerDistanceAudit/1.0 (read-only research)"
DIST_RE = re.compile(r"(?i)(?:(?:distance|located|lies|lying|resides|situated|away|light[- ]years?|Mly|Mpc|megaparsecs?|parsecs?)\b[^.!?]{0,140}|\b\d[\d,.]*\s*(?:million|billion|thousand)?\s*(?:light[- ]years?|Mly|Mpc|megaparsecs?|kpc|Gpc)\b[^.!?]{0,100})")
NUM_RE = re.compile(r"(?i)(\d[\d,.]*)\s*(million|billion|thousand)?\s*(light[- ]years?|Mly|Mpc|megaparsecs?|kpc|Gpc)")

def text_from_html(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)</(p|div|li|h[1-6]|section|article|br|tr)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", unescape(raw)).strip()

def candidates(r):
    provider = str(r.get("providerKey") or "").lower()
    aid = str(r.get("archiveId") or "").strip()
    image = str(r.get("imageUrl") or "")
    urls = []
    if provider == "hubble" and aid:
        urls += [f"https://esahubble.org/images/{aid}/"]
    elif provider == "jwst" and aid:
        urls += [f"https://esawebb.org/images/{aid}/", f"https://webbtelescope.org/contents/media/images/{aid}"]
    elif provider == "eso" and aid:
        urls += [f"https://www.eso.org/public/images/{aid}/"]
    elif provider == "noirlab" and aid:
        urls += [f"https://astropix.org/image/{aid}", f"https://noirlab.edu/public/images/{aid}/"]
    elif provider == "spitzer" and aid:
        urls += [f"https://astropix.org/archive/spitzer/{aid}/"]
    elif provider == "chandra" and image:
        p = urlparse(image).path.split("/")
        if "photo" in p:
            k = p.index("photo")
            if len(p) > k+2:
                urls += [f"https://chandra.harvard.edu/photo/{p[k+1]}/{p[k+2]}/"]
    # A direct source/image URL is a last-resort page to inspect, never assumed to be a description.
    if image and image not in urls:
        urls.append(image)
    # retain order, remove duplicates
    return list(dict.fromkeys(urls))

def fetch(url):
    try:
        req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*"})
        with urlopen(req, timeout=18) as resp:
            ct = resp.headers.get("Content-Type", "")
            data = resp.read(2_000_000)
            if "html" not in ct.lower() and not data.lstrip().startswith((b"<!", b"<html", b"<HTML")):
                return {"url": resp.geturl(), "status": "non_html", "text": ""}
            return {"url": resp.geturl(), "status": f"http_{resp.status}", "text": text_from_html(data.decode("utf-8", "replace"))}
    except Exception as e:
        return {"url": url, "status": "fetch_error:" + type(e).__name__ + ":" + str(e)[:160], "text": ""}

def to_mly(number, scale, unit):
    n = float(number.replace(",", ""))
    u = unit.lower().replace(" ", "")
    s = (scale or "").lower()
    if u in ("ml y", "mly"): return n
    if u == "mpc" or u == "megaparsecs":
        return n * 3.26156
    if u == "kpc": return n * 0.00326156
    if u == "gpc": return n * 3261.56
    if "light-year" in u:
        if s == "billion": return n * 1000
        if s == "million": return n
        if s == "thousand": return n / 1000
        return n / 1_000_000
    return None

def find_quotes(text):
    found = []
    for m in DIST_RE.finditer(text):
        snippet = m.group(0).strip()
        if not re.search(r"(?i)\d[\d,.]*\s*(?:million|billion|thousand)?\s*(?:light[- ]years?|Mly|Mpc|megaparsecs?|kpc|Gpc)", snippet):
            continue
        values = []
        for n in NUM_RE.finditer(snippet):
            try:
                v = to_mly(n.group(1), n.group(2), n.group(3))
                if v is not None: values.append(round(v, 6))
            except Exception: pass
        found.append((snippet[:500], values))
    # remove duplicate snippets
    seen=set(); out=[]
    for q, vals in found:
        k=(q,tuple(vals))
        if k not in seen: seen.add(k); out.append((q,vals))
    return out[:12]

def audit(r):
    dist = r.get("distanceMly")
    try: dist = float(dist) if dist is not None else None
    except Exception: dist = None
    urls = candidates(r)
    fetched = []
    for url in urls[:3]:
        page = fetch(url)
        fetched.append(page)
        if page["text"] and find_quotes(page["text"]):
            break
    quotes = []
    for p in fetched:
        for q, vals in find_quotes(p["text"]):
            quotes.append({"url":p["url"],"quote":q,"quotedDistanceMly":vals})
    # classify only as triage: source text must be reviewed before changing any value.
    values = [v for q in quotes for v in q["quotedDistanceMly"]]
    status = "NO_SOURCE_PAGE_FETCHED"
    if quotes:
        if dist is None: status = "RUNTIME_DISTANCE_MISSING"
        elif any(abs(v-dist) <= max(2.0, dist*0.03) for v in values): status = "MATCH_WITHIN_3PCT_OR_2MLY"
        elif values: status = "POTENTIAL_DISCREPANCY_REVIEW"
        else: status = "SOURCE_TEXT_FOUND_NO_NUMERIC_DISTANCE"
    elif any(p["text"] for p in fetched):
        status = "PAGE_FETCHED_NO_EXPLICIT_DISTANCE_FOUND"
    return {
        "provider":r.get("providerKey",""),"archiveId":r.get("archiveId",""),"name":r.get("name",""),
        "runtimeDistanceMly":dist,"sourceCatalog":r.get("sourceCatalog",""),"imageUrl":r.get("imageUrl",""),
        "candidateSourceUrls":" | ".join(urls),"fetchedUrls":" | ".join(p["url"] for p in fetched),
        "fetchStatuses":" | ".join(p["status"] for p in fetched),"quotedDistanceMly":" | ".join(str(v) for v in values),
        "evidenceQuotes":" || ".join(f'{q["url"]}: {q["quote"]}' for q in quotes),
        "classification":status,"auditNote":"Automated extraction is triage only; confirm context and rounding before declaring a true discrepancy."
    }

def main():
    obj=json.loads(RUNTIME.read_text(encoding="utf-8"))
    records=obj.get("records") if isinstance(obj,dict) else obj
    if not isinstance(records,list): raise SystemExit("Unexpected runtime schema")
    rows=[]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures=[pool.submit(audit,r) for r in records if isinstance(r,dict)]
        for i,f in enumerate(as_completed(futures),1):
            rows.append(f.result())
            if i % 100 == 0: print(f"processed {i}/{len(futures)}",flush=True)
    order={(str(r.get("providerKey","")),str(r.get("archiveId",""))):i for i,r in enumerate(records) if isinstance(r,dict)}
    rows.sort(key=lambda x:order.get((str(x["provider"]),str(x["archiveId"])),10**9))
    csvpath=OUT/"runtime-distance-source-wording-audit.csv"
    fields=list(rows[0].keys()) if rows else []
    with csvpath.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    from collections import Counter
    summary={"generatedUtc":datetime.now(timezone.utc).isoformat(),"branch":"release","runtimeCatalog":str(RUNTIME),
             "runtimeRecordCount":len(records),"auditedRecordCount":len(rows),
             "classificationCounts":dict(Counter(x["classification"] for x in rows)),
             "important":"Read-only audit. No catalog values are changed. Automated text extraction is not a final scientific judgment."}
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
