#!/usr/bin/env python3
"""Build runtime catalog 0006 from the saved 1,847-row audit CSV.
Uses the exact 400 POTENTIAL_DISCREPANCY_REVIEW rows and extracts the distance quote
from its context. Fetches only an individual flagged provider page when the audit
snippet is insufficient; never repeats the 1,847-page audit.
"""
import csv, json, math, re, time
from pathlib import Path
from html import unescape
from urllib.request import Request, urlopen

SRC = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0004.json")
OUT = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0006.json")
REPORT = Path("distance-source-wording-0006-report.json")
CSV_PATH = Path("distance-source-wording-audit/runtime-distance-source-wording-audit.csv")
QUOTAS = {"chandra": 3, "eso": 55, "hubble": 295, "jwst": 20, "noirlab": 27}
H0, OM, C = 67.6, 0.315, 299792.458
DISTANCE_RE = re.compile(r"(?i)(\d[\d,.]*)\s*(million|billion|thousand)?\s*(light[- ]years?|Mly|Mpc|megaparsecs?|kpc|Gpc)\b")

def e_z(z):
    return math.sqrt(OM * (1 + z) ** 3 + (1 - OM))

def luminosity_distance_mly(z):
    n = 1200
    dz = z / n
    total = 0.0
    for i in range(n + 1):
        zz = i * dz
        total += (1 if i in (0, n) else (4 if i % 2 else 2)) / e_z(zz)
    dc_mpc = (C / H0) * (dz / 3) * total
    return (1 + z) * dc_mpc * 3.261563777

def redshift_for_distance(distance_mly):
    lo, hi = 0.0, 20.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if luminosity_distance_mly(mid) < distance_mly: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def convert_match(m):
    n = float(m.group(1).replace(",", ""))
    scale = (m.group(2) or "").lower()
    unit = m.group(3).lower().replace(" ", "")
    if unit in ("mpc", "megaparsecs"): return n * 3.261563777
    if unit == "kpc": return n * 0.003261563777
    if unit == "gpc": return n * 3261.563777
    if unit == "mly": return n
    if scale == "billion": return n * 1000
    if scale == "million": return n
    if scale == "thousand": return n / 1000
    return n / 1_000_000

def parse_context(snippets):
    # Strongest evidence first: provider's structured Distance field, then a clear
    # distance-to-Earth statement. Exclude physical-size and local-separation claims.
    for sn in snippets:
        if re.search(r"(?i)\bDistance\s*:", sn):
            m = DISTANCE_RE.search(sn.split("Distance:", 1)[1])
            if m: return convert_match(m), sn
    patterns = [
        re.compile(r"(?i)(?:located|lies|lying|resides|situated)\s+(?:about\s+|approximately\s+|roughly\s+)?\d[\d,.]*\s*(?:million|billion|thousand)?\s*light[- ]years?\s+(?:away|from (?:the )?Earth|from us)"),
        re.compile(r"(?i)\d[\d,.]*\s*(?:million|billion|thousand)?\s*light[- ]years?\s+(?:away from Earth|from Earth|from the Earth|away|distant)"),
        re.compile(r"(?i)distance estimate\s*[: ]*\s*\d[\d,.]*\s*(?:million|billion|thousand)?\s*light[- ]years?"),
    ]
    for sn in snippets:
        # A snippet can contain a size AND a distance; search specifically for the
        # distance clause rather than rejecting the whole snippet because it says "across".
        for p in patterns:
            m = p.search(sn)
            if m:
                dm = DISTANCE_RE.search(m.group(0))
                if dm: return convert_match(dm), m.group(0)
    return None

def fetch_page(url):
    if not url: return ""
    try:
        req = Request(url, headers={"User-Agent":"GalaxyViewerDistanceAudit/1.1","Accept":"text/html,*/*"})
        with urlopen(req, timeout=18) as response:
            raw = response.read(2_000_000).decode("utf-8","replace")
        raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
        raw = re.sub(r"(?i)</(p|div|li|h[1-6]|section|article|br|tr)>", "\n", raw)
        raw = re.sub(r"(?s)<[^>]+>", " ", raw)
        return re.sub(r"\s+", " ", unescape(raw)).strip()
    except Exception:
        return ""

def page_distance(text):
    # Try structured Distance metadata first.
    m = re.search(r"(?i)Distance\s*:\s*"+DISTANCE_RE.pattern[4:], text)
    if m:
        dm = DISTANCE_RE.search(m.group(0))
        if dm: return convert_match(dm), m.group(0)[:350]
    snippets = [text[max(0,m.start()-100):min(len(text),m.end()+120)] for m in DISTANCE_RE.finditer(text)]
    return parse_context(snippets)

def candidates_from_csv():
    if not CSV_PATH.exists(): raise SystemExit(f"Saved audit CSV not found: {CSV_PATH}")
    flagged = []
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            provider = (row.get("provider") or "").strip().lower()
            if provider not in QUOTAS or row.get("classification") != "POTENTIAL_DISCREPANCY_REVIEW":
                continue
            try: current = float(row.get("runtimeDistanceMly") or "")
            except (TypeError, ValueError): continue
            evidence = (row.get("evidenceQuotes") or "").strip()
            snippets = evidence.split(" || ") if evidence else []
            source_url = ""
            quote = ""
            parsed = parse_context(snippets)
            if parsed:
                published, quote = parsed
                source_url = next((s.split(": ",1)[0] for s in snippets if quote in s), "")
            else:
                urls = (row.get("fetchedUrls") or row.get("candidateSourceUrls") or "").split(" | ")
                for url in urls:
                    text = fetch_page(url.strip())
                    parsed = page_distance(text) if text else None
                    if parsed:
                        published, quote = parsed
                        source_url = url.strip()
                        break
            if not parsed:
                flagged.append({"provider":provider,"archiveId":row.get("archiveId"),"reason":"No contextual distance quote resolved from audit evidence or provider page"})
                continue
            if not (math.isfinite(published) and published > 0):
                flagged.append({"provider":provider,"archiveId":row.get("archiveId"),"reason":f"Invalid distance {published}"})
                continue
            flagged.append({
                "provider":provider,"archiveId":row.get("archiveId",""),"name":row.get("name",""),
                "distance":published,"current":current,"delta":abs(published-current)/max(abs(current),1e-9),
                "sourceUrl":source_url,"quote":quote,"classification":row.get("classification",""),
            })
    unresolved = [x for x in flagged if "reason" in x]
    if unresolved:
        raise SystemExit("ABORT: could not resolve provider-page distance for flagged rows: "+json.dumps(unresolved))
    counts = {p:sum(1 for x in flagged if x["provider"]==p) for p in QUOTAS}
    if len(flagged)!=400 or counts!=QUOTAS:
        raise SystemExit(f"ABORT: expected the 400 flagged audit rows and provider quotas; got total={len(flagged)} counts={counts}")
    return flagged

def set_distance(r, distance, source_url, quote):
    z = redshift_for_distance(distance)
    display = f"{distance:,.2f} million light-years"
    r["distanceMly"] = round(distance, 6)
    r["redshift"] = round(z, 8)
    s = r.get("science") if isinstance(r.get("science"), dict) else {}
    r["science"] = s
    s["distanceMly"] = round(distance, 6)
    s["distanceDisplay"] = display
    s["distanceMethod"] = "published_provider_page_distance_from_saved_audit_csv"
    s["distanceSource"] = source_url
    s["distanceEvidence"] = quote
    s["distanceVerified"] = True
    s["redshift"] = round(z, 8)
    s["redshiftMethod"] = "flat_LCDM_from_published_distance_H0_67.6_Om_0.315"
    s["redshiftSource"] = source_url
    s["redshiftEvidence"] = f"Calculated from provider-published distance {distance:.6f} Mly assuming luminosity distance in flat Lambda-CDM (H0=67.6, Omega_m=0.315)."
    if isinstance(r.get("distance"), dict):
        r["distance"]["mly"] = round(distance, 6)
        r["distance"]["display"] = display
    if "distanceDisplay" in r: r["distanceDisplay"] = display

def main():
    obj = json.loads(SRC.read_text(encoding="utf-8"))
    records = obj.get("records") if isinstance(obj, dict) else obj
    if not isinstance(records, list) or len(records) != 1847: raise SystemExit("Source catalog must contain exactly 1,847 records.")
    by_key = {(str(r.get("providerKey") or "").lower(), str(r.get("archiveId") or "")):(i,r) for i,r in enumerate(records) if isinstance(r,dict)}
    selected = candidates_from_csv()
    changed=[]
    for row in selected:
        key=(row["provider"],str(row["archiveId"]))
        if key not in by_key: raise SystemExit(f"Flagged record missing in v0004: {key}")
        _,rec=by_key[key]
        set_distance(rec,row["distance"],row["sourceUrl"],row["quote"])
        changed.append({"provider":row["provider"],"archiveId":row["archiveId"],"name":row["name"],
            "previousDistanceMly":row["current"],"distanceMly":round(row["distance"],6),
            "redshift":round(redshift_for_distance(row["distance"]),8),"sourceUrl":row["sourceUrl"],
            "sourceQuote":row["quote"],"auditClassification":row["classification"]})
    obj["schema"]="gv-avm-runtime-catalog-0006"
    obj["version"]="0006"
    obj["derivedFrom"]="gv-avm-runtime-catalog-0004"
    obj["distanceRedshiftUpdate"]={"method":"saved provider-page audit CSV contextual distance quotes; flat Lambda-CDM H0=67.6 Omega_m=0.315",
        "sourceAuditRunId":40020620652,"changedRecords":400,"providerCounts":QUOTAS}
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    REPORT.write_text(json.dumps({"sourceCatalog":str(SRC),"sourceAuditCsv":str(CSV_PATH),"sourceAuditRunId":40020620652,
        "outputCatalog":str(OUT),"sourceRecordCount":len(records),"updatedRecordCount":len(changed),
        "providerCounts":QUOTAS,"updates":changed},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(OUT),"records":len(records),"updated":len(changed),"providerCounts":QUOTAS},indent=2))

if __name__=="__main__": main()
