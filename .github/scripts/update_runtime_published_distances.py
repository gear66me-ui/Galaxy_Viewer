#!/usr/bin/env python3
"""Populate Galaxy Viewer runtime distances from published NED/SIMBAD values and redshifts."""
import json, math, os, statistics, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

RUNTIME = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0003.json")
REPORT = Path("ned-simbad-distance-verification.json")
NED = "https://ned.ipac.caltech.edu/NED::API/DistancesOfObject?"
SIMBAD = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
MPC_TO_MLY = 3.261563777
ABSURD_MLY = 100000.0
USER_AGENT = "GalaxyViewerPublishedDistanceUpdate/1.0 (catalog correction)"

def fetch(url, data=None, timeout=20):
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/x-votable+xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()

def parse_votable(payload):
    root = ET.fromstring(payload)
    fields = root.findall(".//{*}FIELD")
    names = [f.attrib.get("name") or f.attrib.get("ID") or f"col{i}" for i, f in enumerate(fields)]
    rows = []
    for tr in root.findall(".//{*}TABLEDATA/{*}TR"):
        vals = [(td.text or "").strip() for td in tr.findall("{*}TD")]
        rows.append({names[i]: vals[i] if i < len(vals) else "" for i in range(len(names))})
    return rows

def keymap(row):
    return {str(k).strip().lower().replace("_", " "): v for k, v in row.items()}

def pick(row, *keys):
    m = keymap(row)
    for k in keys:
        v = m.get(k.lower().replace("_", " "))
        if v is not None and str(v).strip() not in ("", "--", "null", "None", "NaN"):
            return str(v).strip()
    return ""

def number(value):
    try:
        x = float(str(value).strip())
        return x if math.isfinite(x) else None
    except Exception:
        return None

def positive(value):
    x = number(value)
    return x if x is not None and x > 0 else None

def get_records(doc):
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for k in ("entries", "records", "galaxies", "catalog", "items", "data"):
            if isinstance(doc.get(k), list):
                return doc[k]
    raise RuntimeError("Unknown runtime JSON shape; refusing to edit")

def identifiers(entry):
    values = []
    for k in ("designation", "name", "objectName", "targetName", "simbadName", "nedName", "title", "archiveId", "id"):
        v = entry.get(k)
        if isinstance(v, str) and v.strip() and v.strip() not in values:
            values.append(v.strip())
    science = entry.get("science")
    if isinstance(science, dict):
        for k in ("designation", "name", "objectName", "targetName", "simbadName", "nedName"):
            v = science.get(k)
            if isinstance(v, str) and v.strip() and v.strip() not in values:
                values.append(v.strip())
    # Avoid sending long descriptive captions to either archive.
    return [v for v in values if len(v) <= 100][:4]

def ned_lookup(name):
    url = NED + urllib.parse.urlencode({"TARGET": name, "MAXREC": 1000})
    rows = parse_votable(fetch(url))
    distances, redshifts, methods, refs = [], [], [], []
    for row in rows:
        d = positive(pick(row, "Distance"))
        if d is not None:
            distances.append(d * MPC_TO_MLY)
            methods.append(pick(row, "Method"))
            refs.append(pick(row, "Reference"))
        z = number(pick(row, "Redshift"))
        if z is not None and z >= 0:
            redshifts.append(z)
    return {"distances": distances, "redshifts": redshifts, "methods": methods, "references": refs, "url": url}

def simbad_lookup(name):
    q = name.replace("'", "''")
    adql = ("SELECT b.main_id, b.rvz_redshift FROM ident AS i "
            "JOIN basic AS b ON i.oidref=b.oid "
            f"WHERE i.id='{q}'")
    body = urllib.parse.urlencode({"request": "doQuery", "lang": "adql", "format": "votable", "query": adql}).encode()
    rows = parse_votable(fetch(SIMBAD, body))
    redshifts, ids = [], []
    for row in rows:
        z = number(pick(row, "rvz_redshift"))
        if z is not None and z >= 0:
            redshifts.append(z)
        mid = pick(row, "main_id")
        if mid:
            ids.append(mid)
    # SIMBAD distance measurements are fetched directly from its published measurement table.
    adql_dist = ("SELECT b.main_id, d.distance, d.unit, d.method, d.bibcode "
                 "FROM ident AS i JOIN basic AS b ON i.oidref=b.oid "
                 "JOIN mesDistance AS d ON d.oidref=b.oid "
                 f"WHERE i.id='{q}'")
    body_dist = urllib.parse.urlencode({"request": "doQuery", "lang": "adql", "format": "votable", "query": adql_dist}).encode()
    rows_dist = parse_votable(fetch(SIMBAD, body_dist))
    distances, methods, refs = [], [], []
    for row in rows_dist:
        d = positive(pick(row, "distance"))
        unit = pick(row, "unit").lower().replace(" ", "")
        if d is None:
            continue
        if unit in ("mpc", "megaparsec", "megaparsecs"):
            mly = d * MPC_TO_MLY
        elif unit in ("kpc", "kiloparsec", "kiloparsecs"):
            mly = d * 0.003261563777
        elif unit in ("pc", "parsec", "parsecs"):
            mly = d * 0.000003261563777
        else:
            continue
        if mly > 0:
            distances.append(mly)
            methods.append(pick(row, "method"))
            refs.append(pick(row, "bibcode"))
    return {"distances": distances, "redshifts": redshifts, "methods": methods, "references": refs, "ids": ids}

def redshift_luminosity_distance_mly(z):
    # Fallback only for an absurd existing distance when no published distance is returned.
    # Flat LCDM H0=70 km/s/Mpc, Om0=0.3; Simpson integration.
    n, dz, h0, om, c = 4000, z / 4000.0, 70.0, 0.3, 299792.458
    total = 0.0
    for i in range(n + 1):
        zz = i * dz
        weight = 1 if i in (0, n) else (4 if i % 2 else 2)
        total += weight / math.sqrt(om * (1 + zz) ** 3 + 1 - om)
    dc_mpc = (c / h0) * total * dz / 3
    return dc_mpc * (1 + z) * MPC_TO_MLY

def process(item):
    index, entry = item
    science = entry.get("science") if isinstance(entry.get("science"), dict) else {}
    names = identifiers(entry)
    result = {"index": index, "name": names[0] if names else "", "distanceValuesMly": [], "redshiftValues": [], "sources": [], "errors": []}
    if not names:
        result["status"] = "NO_IDENTIFIER"
        return index, result
    # Try identifiers in order; stop after the first source that returns a match.
    for name in names:
        try:
            n = ned_lookup(name)
            if n["distances"] or n["redshifts"]:
                result["distanceValuesMly"].extend(n["distances"])
                result["redshiftValues"].extend(n["redshifts"])
                result["sources"].extend([{"source":"NED","method":m,"reference":r,"query":n["url"]} for m,r in zip(n["methods"],n["references"])])
                result["nedMatch"] = name
                break
        except Exception as e:
            result["errors"].append("NED "+name+": "+str(e)[:160])
        time.sleep(0.12)
    for name in names[:2]:
        try:
            s = simbad_lookup(name)
            if s["distances"] or s["redshifts"]:
                result["distanceValuesMly"].extend(s["distances"])
                result["redshiftValues"].extend(s["redshifts"])
                result["sources"].extend([{"source":"SIMBAD","method":m,"reference":r,"match":(s.get("ids") or [name])[0]} for m,r in zip(s["methods"],s["references"])])
                result["simbadMatch"] = (s.get("ids") or [name])[0]
                break
        except Exception as e:
            result["errors"].append("SIMBAD "+name+": "+str(e)[:160])
        time.sleep(0.12)
    result["distanceValuesMly"] = [x for x in result["distanceValuesMly"] if positive(x)]
    result["redshiftValues"] = [x for x in result["redshiftValues"] if x is not None and math.isfinite(x) and x >= 0]
    # If both archives provide values, use the median of every positive published measurement.
    # One published measurement is used as-is.
    if result["distanceValuesMly"]:
        result["selectedDistanceMly"] = statistics.median(result["distanceValuesMly"])
    else:
        result["selectedDistanceMly"] = None
    if result["redshiftValues"]:
        result["selectedRedshift"] = statistics.median(result["redshiftValues"])
    else:
        result["selectedRedshift"] = None
    old = positive(science.get("distanceMly", entry.get("distanceMly")))
    result["oldDistanceMly"] = old
    result["oldRedshift"] = science.get("redshift", entry.get("redshift"))
    result["status"] = "PUBLISHED_DISTANCE_FOUND" if result["selectedDistanceMly"] else ("REDSHIFT_ONLY" if result["selectedRedshift"] is not None else "NO_EXTERNAL_VALUE")
    return index, result

def main():
    doc = json.loads(RUNTIME.read_text(encoding="utf-8"))
    rows = get_records(doc)
    if len(rows) != 1847:
        raise SystemExit(f"Expected 1847 runtime records; found {len(rows)}. Refusing changes.")
    results = [None] * len(rows)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(process, (i, entry)) for i, entry in enumerate(rows)]
        done = 0
        for future in as_completed(futures):
            i, result = future.result()
            results[i] = result
            done += 1
            if done % 25 == 0 or done == len(rows):
                print(f"Processed {done}/{len(rows)} records", flush=True)
    counters = {"records":len(rows),"publishedDistanceUpdated":0,"redshiftPopulated":0,"absurdDistanceReplaced":0,"absurdDistanceCleared":0,"noExternalValue":0}
    for entry, result in zip(rows, results):
        if not isinstance(entry.get("science"), dict):
            entry["science"] = {}
        science = entry["science"]
        dist = result.get("selectedDistanceMly")
        z = result.get("selectedRedshift")
        old = result.get("oldDistanceMly")
        if dist is not None:
            science["distanceMly"] = round(dist, 4)
            science["distanceMethod"] = "median_of_published_NED_SIMBAD_measurements" if len(result["distanceValuesMly"]) > 1 else "single_published_NED_SIMBAD_measurement"
            science["distanceEvidence"] = json.dumps(result["sources"], ensure_ascii=False, separators=(",", ":"))[:4000]
            science["distanceEstimated"] = False
            science["distanceDisplay"] = f"{dist:,.4g} million light-years"
            entry["distance"] = science["distanceDisplay"]
            counters["publishedDistanceUpdated"] += 1
        if z is not None:
            science["redshift"] = round(z, 8)
            science["redshiftDisplay"] = f"z {z:.6f}"
            science["redshiftEstimated"] = False
            science["redshiftMethod"] = "published_NED_SIMBAD_redshift"
            science["redshiftSource"] = "NED/SIMBAD"
            counters["redshiftPopulated"] += 1
        elif positive(science.get("redshift", entry.get("redshift"))) is None:
            # No redshift found; do not fabricate one.
            pass
        # Never leave trillion-light-year-scale values in the runtime catalog.
        current = positive(science.get("distanceMly", entry.get("distanceMly")))
        if current is not None and current > ABSURD_MLY:
            if z is not None:
                fallback = redshift_luminosity_distance_mly(z)
                science["distanceMly"] = round(fallback, 4)
                science["distanceMethod"] = "redshift_LCDM_fallback_no_published_distance"
                science["distanceEvidence"] = "Fallback estimate from published redshift because no published distance measurement was returned."
                science["distanceEstimated"] = True
                science["distanceDisplay"] = f"EST. {fallback:,.4g} million light-years"
                entry["distance"] = science["distanceDisplay"]
                counters["absurdDistanceReplaced"] += 1
            elif dist is None:
                science["distanceMly"] = None
                science["distanceMethod"] = "unavailable_absurd_prior_value_cleared"
                science["distanceDisplay"] = "Distance unavailable"
                science["distanceEstimated"] = False
                entry["distance"] = "Distance unavailable"
                counters["absurdDistanceCleared"] += 1
        if result["status"] == "NO_EXTERNAL_VALUE":
            counters["noExternalValue"] += 1
    output = {
        "schema":"gv-ned-simbad-published-distance-redshift-0002",
        "generatedUtc":datetime.now(timezone.utc).isoformat(),
        "runtimePath":str(RUNTIME),
        "runtimeRecordCount":len(rows),
        "policy":"Use median of all positive published NED/SIMBAD distance measurements; use the sole value when only one is returned. Redshift is populated from available published NED/SIMBAD values. Redshift-derived distance is fallback only when an existing value exceeds 100,000 Mly and no published distance was returned.",
        "counters":counters,
        "records":results
    }
    REPORT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    RUNTIME.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    checked=json.loads(RUNTIME.read_text(encoding="utf-8"))
    checkrows=get_records(checked)
    if len(checkrows)!=1847:
        raise SystemExit("Post-write record count validation failed")
    for i,e in enumerate(checkrows):
        s=e.get("science",{})
        d=s.get("distanceMly")
        if d is not None and (not isinstance(d,(int,float)) or not math.isfinite(d) or d<=0 or d>ABSURD_MLY):
            raise SystemExit(f"Invalid or absurd distance remains at record {i}: {d!r}")
        z=s.get("redshift")
        if z is not None and (not isinstance(z,(int,float)) or not math.isfinite(z) or z<0 or z>20):
            raise SystemExit(f"Invalid redshift at record {i}: {z!r}")
    print(json.dumps(counters,indent=2))
if __name__ == "__main__":
    main()
