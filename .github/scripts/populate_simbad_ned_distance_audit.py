#!/usr/bin/env python3
"""Audit-only SIMBAD + NED distance comparison. Never edits catalog JSON."""
import csv, io, os, re, sys, time, math, statistics, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(".")
INPUT = ROOT / "audit/distance-age-review/galaxy-distance-age-source-audit.csv"
OUTPUT = Path(os.environ.get("AUDIT_OUTPUT", str(ROOT / "audit/distance-age-review/galaxy-distance-age-source-audit.enriched.csv")))
USER_AGENT = "GalaxyViewerDistanceAudit/1.0 (research audit; respectful low-rate queries)"
NED_BASE = "https://ned.ipac.caltech.edu/NED::API/"
SIMBAD_TAP = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
MPC_TO_MLY = 3.261563777
COLUMNS = [
    "simbad_match_id", "simbad_distance_count", "simbad_distances_mly",
    "simbad_distance_median_mly", "simbad_distance_methods", "simbad_distance_references",
    "simbad_redshift", "simbad_query_url", "simbad_status",
    "ned_match_id", "ned_distance_count", "ned_distances_mly",
    "ned_distance_median_mly", "ned_distance_methods", "ned_distance_references",
    "ned_redshift", "ned_query_url", "ned_status",
    "source_median_distance_mly", "source_measurement_count",
    "distance_discrepancy_pct", "review_status"
]

def fetch(url, data=None, timeout=15):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT, "Accept": "application/x-votable+xml, text/plain, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def parse_votable(payload):
    root = ET.fromstring(payload)
    ns = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}
    fields = root.findall(".//v:FIELD", ns)
    if not fields:
        fields = root.findall(".//{*}FIELD")
    names = [f.attrib.get("name") or f.attrib.get("ID") or f"col{i}" for i,f in enumerate(fields)]
    rows = []
    for tr in root.findall(".//{*}TABLEDATA/{*}TR"):
        vals = [(td.text or "").strip() for td in tr.findall("{*}TD")]
        rows.append(dict(zip(names, vals)))
    return rows

def pick(d, *keys):
    lower = {str(k).strip().lower(): v for k,v in d.items()}
    for key in keys:
        if key.lower() in lower and lower[key.lower()] not in ("", "--", "null", "None"):
            return lower[key.lower()]
    return ""

def number(v):
    try:
        x = float(str(v).replace(",", "").strip())
        return x if math.isfinite(x) else None
    except Exception:
        return None

def compact(values):
    seen = []
    for v in values:
        v = str(v).strip()
        if v and v not in seen:
            seen.append(v)
    return " | ".join(seen)

def get_identifiers(row):
    # Prioritize actual object identifiers. The original CSV's NED_query cells
    # contain concatenated descriptive text and must not be sent as object names.
    vals = []
    for key in ("name", "designation", "displayName", "archiveId"):
        raw = (row.get(key) or "").strip()
        if not raw:
            continue
        for v in [p.strip() for p in re.split(r"\\s*/\\s*", raw) if p.strip()]:
            if v and v not in vals:
                vals.append(v)
    # Keep fallback names short and identifier-like only.
    for key in ("SIMBAD_query", "NED_query", "title"):
        v = (row.get(key) or "").strip()
        if v and len(v.split()) <= 4 and not any(token in v.lower() for token in ("distance", "redshift", "observation of")) and v not in vals:
            vals.append(v)
    return vals[:3]

def simbad_lookup(row):
    names = get_identifiers(row)
    ra, dec = number(row.get("ra_deg") or row.get("ra")), number(row.get("dec_deg") or row.get("dec"))
    last_error = ""
    # Query SIMBAD's measurements table by object identifier; each query is bounded and logged.
    for name in names:
        qname = name.replace("'", "''")
        adql = (
            "SELECT b.main_id, b.ra, b.dec, d.* "
            "FROM ident AS i JOIN basic AS b ON i.oidref=b.oid "
            "JOIN mesDistance AS d ON d.oidref=b.oid "
            f"WHERE i.id='{qname}'"
        )
        try:
            body = urllib.parse.urlencode({"request":"doQuery","lang":"adql","format":"votable","query":adql}).encode()
            rows = parse_votable(fetch(SIMBAD_TAP, body))
            if rows:
                ds = []
                methods, refs, ids, zs = [], [], [], []
                for r in rows:
                    # SIMBAD distance table values are generally in parsecs; inspect unit fields when present.
                    raw = number(pick(r, "distance", "dist", "value", "d"))
                    unit = pick(r, "unit", "distance_unit", "dist_unit").lower()
                    if raw is not None:
                        if "mpc" in unit: mly = raw * MPC_TO_MLY
                        elif "kpc" in unit: mly = raw * 0.003261563777
                        elif "pc" in unit: mly = raw / 1e6 * 3.261563777
                        else: mly = raw * MPC_TO_MLY if raw < 1e4 else raw / 1e6 * 3.261563777
                        if mly > 0: ds.append(mly)
                    methods.append(pick(r, "method", "bibcode", "r"))
                    refs.append(pick(r, "bibcode", "reference", "ref"))
                    ids.append(pick(r, "main_id"))
                    zs.append(pick(r, "rvz_redshift", "redshift", "z"))
                med = statistics.median(ds) if ds else None
                return {
                    "simbad_match_id": compact(ids), "simbad_distance_count": str(len(ds)),
                    "simbad_distances_mly": ";".join(f"{x:.6g}" for x in ds),
                    "simbad_distance_median_mly": f"{med:.6g}" if med else "",
                    "simbad_distance_methods": compact(methods), "simbad_distance_references": compact(refs),
                    "simbad_redshift": compact(zs), "simbad_query_url": "https://simbad.cds.unistra.fr/simbad/sim-id?Ident="+urllib.parse.quote(name),
                    "simbad_status": "MATCH_WITH_DISTANCE" if ds else "MATCH_NO_DISTANCE"
                }
        except Exception as e:
            last_error = str(e)[:180]
        time.sleep(0.15)
    # Coordinate-based fallback, if coordinates exist.
    if ra is not None and dec is not None:
        try:
            adql = ("SELECT b.main_id,b.ra,b.dec,d.* FROM basic AS b JOIN mesDistance AS d ON d.oidref=b.oid "
                    f"WHERE DISTANCE(POINT('ICRS',b.ra,b.dec),POINT('ICRS',{ra},{dec})) < 0.001")
            body = urllib.parse.urlencode({"request":"doQuery","lang":"adql","format":"votable","query":adql}).encode()
            rows = parse_votable(fetch(SIMBAD_TAP, body))
            if rows:
                return {"simbad_match_id":compact([pick(r,"main_id") for r in rows]),
                        "simbad_distance_count":"0","simbad_status":"COORDINATE_MATCH_REVIEW_REQUIRED"}
        except Exception as e:
            last_error = str(e)[:180]
    return {"simbad_status": "ERROR:"+last_error if last_error else "NO_MATCH"}

def ned_lookup(row):
    names = get_identifiers(row)
    last_error = ""
    for name in names:
        url = NED_BASE + "DistancesOfObject?" + urllib.parse.urlencode({"TARGET": name, "MAXREC": 1000})
        try:
            rows = parse_votable(fetch(url))
            if rows:
                distances, methods, refs, ids, zs = [], [], [], [], []
                for r in rows:
                    mpc = number(pick(r, "Distance"))
                    if mpc is not None and mpc > 0:
                        distances.append(mpc * MPC_TO_MLY)
                    methods.append(pick(r, "Method"))
                    refs.append(pick(r, "Reference"))
                    ids.append(pick(r, "Object Name", "ObjectName", "Name"))
                    zs.append(pick(r, "Redshift"))
                med = statistics.median(distances) if distances else None
                return {
                    "ned_match_id": compact(ids) or name, "ned_distance_count": str(len(distances)),
                    "ned_distances_mly": ";".join(f"{x:.6g}" for x in distances),
                    "ned_distance_median_mly": f"{med:.6g}" if med else "",
                    "ned_distance_methods": compact(methods), "ned_distance_references": compact(refs),
                    "ned_redshift": compact(zs), "ned_query_url": url,
                    "ned_status": "MATCH_WITH_DISTANCE" if distances else "MATCH_NO_DISTANCE"
                }
        except Exception as e:
            last_error = str(e)[:180]
        time.sleep(0.35)  # NED asks automated clients to keep query rates low.
    return {"ned_status": "ERROR:"+last_error if last_error else "NO_MATCH"}

def main():
    if not INPUT.exists():
        raise SystemExit(f"Input CSV not found: {INPUT}")
    with INPUT.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        original_fields = reader.fieldnames or []
    limit = int(os.environ.get("AUDIT_LIMIT", "0") or "0")
    if limit > 0:
        rows = rows[:limit]
        print(f"Pilot limit enabled: first {len(rows)} records", flush=True)
    if not rows:
        raise SystemExit("Input CSV is empty")
    fields = list(original_fields)
    for c in COLUMNS:
        if c not in fields: fields.append(c)
    for i,row in enumerate(rows,1):
        # Resume safely: previously completed rows are not re-queried.
        if row.get("simbad_status") and row.get("ned_status"):
            continue
        row.update(simbad_lookup(row))
        row.update(ned_lookup(row))
        candidates = [number(row.get("simbad_distance_median_mly")), number(row.get("ned_distance_median_mly"))]
        candidates = [x for x in candidates if x and x > 0]
        median = statistics.median(candidates) if candidates else None
        current = number(row.get("science.distanceMly") or row.get("science_distanceMly") or row.get("distanceMly"))
        row["source_median_distance_mly"] = f"{median:.6g}" if median else ""
        row["source_measurement_count"] = str(sum(int(number(row.get(k)) or 0) for k in ("simbad_distance_count","ned_distance_count")))
        row["distance_discrepancy_pct"] = f"{abs(current-median)/median*100:.2f}" if current and median else ""
        row["review_status"] = ("REVIEW_GT50_PERCENT" if current and median and abs(current-median)/median > .5 else
                                "REVIEW_GT20_PERCENT" if current and median and abs(current-median)/median > .2 else
                                "SOURCES_FOUND_REVIEW" if median else "NO_SOURCE_DISTANCE")
        if i % 10 == 0:
            print(f"Processed {i}/{len(rows)} rows", flush=True)
        # checkpoint after every 10 records so a rerun resumes without repeating finished queries
        if i % 10 == 0 or i == len(rows):
            with OUTPUT.open("w", newline="", encoding="utf-8") as f:
                w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                w.writeheader(); w.writerows(rows)
        time.sleep(0.15)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    counts={}
    for r in rows:
        for k in ("simbad_status","ned_status","review_status"):
            counts[k+":"+str(r.get(k,""))]=counts.get(k+":"+str(r.get(k,"")),0)+1
    print("AUDIT SUMMARY")
    print(f"Rows: {len(rows)}")
    for k,v in sorted(counts.items()): print(f"{k}={v}")
    print(f"Output: {OUTPUT}")
if __name__ == "__main__":
    main()
