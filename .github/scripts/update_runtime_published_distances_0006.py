#!/usr/bin/env python3
"""Build AVM runtime catalog 0006 from the saved provider-distance audit CSV.

Uses the already completed audit artifact; does not refetch 1,847 provider pages.
Only rows with one unambiguous quoted distance and a value different from v0004 are eligible.
"""
import csv, json, math
from pathlib import Path

SRC = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0004.json")
OUT = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0006.json")
REPORT = Path("distance-source-wording-0006-report.json")
CSV_PATH = Path("distance-source-wording-audit/runtime-distance-source-wording-audit.csv")
QUOTAS = {"chandra": 3, "eso": 55, "hubble": 295, "jwst": 20, "noirlab": 27}
H0, OM, C = 67.6, 0.315, 299792.458
MPC_TO_MLY = 3.261563777

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
    return (1 + z) * dc_mpc * MPC_TO_MLY

def redshift_for_distance(distance_mly):
    lo, hi = 0.0, 20.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if luminosity_distance_mly(mid) < distance_mly:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def candidates_from_csv():
    if not CSV_PATH.exists():
        raise SystemExit(f"Saved audit CSV not found: {CSV_PATH}")
    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            provider = (row.get("provider") or "").strip().lower()
            if provider not in QUOTAS:
                continue
            try:
                current = float(row.get("runtimeDistanceMly") or "")
                vals = [float(v.strip()) for v in (row.get("quotedDistanceMly") or "").split("|") if v.strip()]
            except (TypeError, ValueError):
                continue
            # Duplicate quote values can appear on a page; distinct values are ambiguous.
            distinct = []
            for v in vals:
                if math.isfinite(v) and v > 0 and not any(abs(v-x) <= max(0.01, abs(x)*0.0001) for x in distinct):
                    distinct.append(v)
            if len(distinct) != 1:
                continue
            published = distinct[0]
            if abs(published-current) < 1e-9:
                continue
            source = (row.get("evidenceQuotes") or "").strip()
            # Preserve the exact evidence line from the saved audit and its source URL.
            first_evidence = source.split(" || ", 1)[0] if source else ""
            if ": " in first_evidence:
                source_url, quote = first_evidence.split(": ", 1)
            else:
                source_url, quote = (row.get("fetchedUrls") or row.get("candidateSourceUrls") or "").split(" | ", 1)[0], first_evidence
            delta = abs(published-current) / max(abs(current), 1e-9)
            rows.append({
                "provider": provider, "archiveId": row.get("archiveId", ""), "name": row.get("name", ""),
                "distance": published, "current": current, "delta": delta,
                "sourceUrl": source_url, "quote": quote,
                "classification": row.get("classification", ""),
            })
    return rows

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
    if "distanceDisplay" in r:
        r["distanceDisplay"] = display

def main():
    obj = json.loads(SRC.read_text(encoding="utf-8"))
    records = obj.get("records") if isinstance(obj, dict) else obj
    if not isinstance(records, list) or len(records) != 1847:
        raise SystemExit("Source catalog must contain exactly 1,847 records.")
    by_key = {}
    for i, r in enumerate(records):
        if isinstance(r, dict):
            by_key[(str(r.get("providerKey") or "").lower(), str(r.get("archiveId") or ""))] = (i, r)
    candidates = candidates_from_csv()
    selected = {}
    shortages = {}
    for provider, quota in QUOTAS.items():
        pool = [x for x in candidates if x["provider"] == provider and (provider, str(x["archiveId"])) in by_key]
        pool.sort(key=lambda x: (-x["delta"], x["archiveId"]))
        if len(pool) < quota:
            shortages[provider] = {"available": len(pool), "required": quota}
        selected[provider] = pool[:quota]
    if shortages:
        raise SystemExit("ABORT: saved CSV has insufficient unambiguous, differing source distances by provider: " + json.dumps(shortages) + ". No catalog published.")
    changed = []
    for provider, rows in selected.items():
        for row in rows:
            idx, rec = by_key[(provider, str(row["archiveId"]))]
            set_distance(rec, row["distance"], row["sourceUrl"], row["quote"])
            changed.append({
                "provider": provider, "archiveId": row["archiveId"], "name": row["name"],
                "previousDistanceMly": row["current"], "distanceMly": round(row["distance"], 6),
                "redshift": round(redshift_for_distance(row["distance"]), 8),
                "sourceUrl": row["sourceUrl"], "sourceQuote": row["quote"],
                "auditClassification": row["classification"],
            })
    if len(changed) != 400:
        raise SystemExit(f"ABORT: expected 400 updated records, got {len(changed)}.")
    obj["schema"] = "gv-avm-runtime-catalog-0006"
    obj["version"] = "0006"
    obj["derivedFrom"] = "gv-avm-runtime-catalog-0004"
    obj["distanceRedshiftUpdate"] = {
        "method": "saved provider-page audit CSV; explicit quoted distance; flat Lambda-CDM H0=67.6 Omega_m=0.315",
        "sourceAuditRunId": 40020620652,
        "changedRecords": 400,
        "providerCounts": {p: len(selected[p]) for p in QUOTAS},
    }
    OUT.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(json.dumps({
        "sourceCatalog": str(SRC), "sourceAuditCsv": str(CSV_PATH),
        "sourceAuditRunId": 40020620652, "outputCatalog": str(OUT),
        "sourceRecordCount": len(records), "updatedRecordCount": len(changed),
        "providerCounts": {p: len(selected[p]) for p in QUOTAS}, "updates": changed,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT), "records": len(records), "updated": len(changed),
        "providerCounts": {p: len(selected[p]) for p in QUOTAS},
        "sourceAuditRunId": 40020620652,
    }, indent=2))

if __name__ == "__main__":
    main()
