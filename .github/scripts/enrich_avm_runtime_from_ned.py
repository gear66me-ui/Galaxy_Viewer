#!/usr/bin/env python3
"""Enrich Galaxy Viewer runtime records from the NED OverviewOfObject API.

Safe defaults: audit only. Apply only when MODE=apply. Ambiguous/unresolved
objects are reported and left unchanged. Canonical distance is distanceMly.
"""
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import median

RUNTIME = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0003.json")
REPORT = Path("ned-runtime-distance-audit.json")
MODE = os.getenv("MODE", "audit").strip().lower()
MPC_TO_MLY = 3.261563777
USER_AGENT = "GalaxyViewer-distance-audit/1.0 (NED API; respectful low-rate requests)"
BASE = "https://ned.ipac.caltech.edu/NED::API/OverviewOfObject"

def finite_positive(value):
    try:
        x = float(value)
        return x if math.isfinite(x) and x > 0 else None
    except (TypeError, ValueError):
        return None

def records_from(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("records", "entries", "galaxies", "items", "data"):
            if isinstance(data.get(key), list):
                return data[key]
    raise ValueError("Unrecognized runtime JSON structure; refusing to guess.")

def clean_target(value):
    if not isinstance(value, str):
        return ""
    s = value.strip()
    if not s:
        return ""
    # Prefer the actual object before image captions / supernova suffixes.
    s = re.split(r"\\s+[|/]\\s+|\\s+—\\s+|\\s+–\\s+", s, maxsplit=1)[0].strip()
    s = re.sub(r"\\s*,\\s*(SN|supernova|HST|Hubble).*?$", "", s, flags=re.I).strip()
    s = re.sub(r"^(the\\s+)?(galaxy|spiral galaxy|barred spiral galaxy)\\s+", "", s, flags=re.I).strip()
    # Avoid querying prose titles such as "A curious supernova in ...".
    if len(s) > 100 or re.search(r"\\b(the|and|with|from|image of|observations of)\\b", s, re.I):
        return ""
    return s

def target_for(record):
    # Structured object identifiers are safest; generic title is deliberately last.
    for key in ("objectName", "targetName", "galaxyName", "target", "name", "title"):
        candidate = clean_target(record.get(key))
        if candidate:
            return candidate
    return ""

def local_name(tag):
    return tag.rsplit("}", 1)[-1]

def parse_votable(xml_bytes):
    root = ET.fromstring(xml_bytes)
    tables = []
    for table in root.iter():
        if local_name(table.tag) != "TABLE":
            continue
        fields = []
        for child in list(table):
            if local_name(child.tag) == "FIELD":
                fields.append((child.attrib.get("name") or child.attrib.get("ID") or "").strip())
        for child in list(table):
            if local_name(child.tag) == "DATA":
                for data_child in list(child):
                    if local_name(data_child.tag) == "TABLEDATA":
                        for tr in list(data_child):
                            if local_name(tr.tag) == "TR":
                                vals = [((td.text or "").strip()) for td in list(tr) if local_name(td.tag) == "TD"]
                                if fields and vals:
                                    tables.append(dict(zip(fields, vals)))
    return tables

def lookup(target):
    query = urllib.parse.urlencode({"TARGET": target})
    url = BASE + "?" + query
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/x-votable+xml, application/xml, text/xml"})
    last_error = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                body = response.read()
            rows = parse_votable(body)
            if not rows:
                return {"status": "no_data", "target": target, "url": url}
            # OverviewOfObject is expected to return one row. Choose its first row;
            # the query is name-based, and the returned canonical identity is recorded.
            row = rows[0]
            lower = {re.sub(r"[^a-z0-9]+", "", k.lower()): v for k, v in row.items()}
            def get(*names):
                for name in names:
                    k = re.sub(r"[^a-z0-9]+", "", name.lower())
                    if k in lower and lower[k] not in ("", "--", "null", "None"):
                        return lower[k]
                return None
            z = None
            raw_z = get("Redshift", "Redshift (z)")
            try:
                z0 = float(raw_z) if raw_z is not None else None
                z = z0 if z0 is not None and math.isfinite(z0) and z0 >= 0 else None
            except (ValueError, TypeError):
                pass
            independent_mpc = finite_positive(get("Mean Distance"))
            flow_mpc = finite_positive(get("D (3K CMB)", "D 3K CMB"))
            if independent_mpc is not None:
                distance_mly = independent_mpc * MPC_TO_MLY
                method = "NED mean redshift-independent distance"
                estimated = False
            elif flow_mpc is not None:
                distance_mly = flow_mpc * MPC_TO_MLY
                method = "NED 3K-CMB Hubble-flow distance (NED cosmology)"
                estimated = True
            else:
                distance_mly = None
                method = None
                estimated = None
            canonical = get("Cross-identifications", "Object Name")
            ref = get("Position Refcode", "Redshift Refcode")
            return {
                "status": "ok" if (distance_mly is not None or z is not None) else "no_usable_measurements",
                "target": target,
                "canonicalName": canonical,
                "redshift": z,
                "distanceMly": distance_mly,
                "distanceMethod": method,
                "distanceEstimated": estimated,
                "reference": ref,
                "url": url,
                "rawFields": row,
            }
        except Exception as exc:
            last_error = str(exc)
            time.sleep(2 ** attempt)
    return {"status": "error", "target": target, "url": url, "error": last_error}

def main():
    if MODE not in ("audit", "apply"):
        raise SystemExit("MODE must be audit or apply")
    if not RUNTIME.is_file():
        raise SystemExit(f"Runtime catalog not found: {RUNTIME}")
    original_text = RUNTIME.read_text(encoding="utf-8")
    data = json.loads(original_text)
    rows = records_from(data)
    if len(rows) < 100:
        raise SystemExit(f"Unexpectedly small runtime catalog ({len(rows)}); refusing to proceed.")

    cache = {}
    changes = []
    unresolved = []
    # One API query per unique target string, with a conservative request cadence.
    for index, record in enumerate(rows):
        if not isinstance(record, dict):
            continue
        target = target_for(record)
        if not target:
            unresolved.append({"index": index, "name": record.get("name"), "reason": "no safe object-name candidate"})
            continue
        key = target.casefold()
        if key not in cache:
            cache[key] = lookup(target)
            time.sleep(0.35)
        result = cache[key]
        if result.get("status") != "ok":
            unresolved.append({"index": index, "name": record.get("name"), "target": target, "reason": result.get("status"), "error": result.get("error")})
            continue
        old_d = finite_positive(record.get("distanceMly"))
        new_d = finite_positive(result.get("distanceMly"))
        old_z = record.get("redshift")
        new_z = result.get("redshift")
        # Do not silently replace a published source distance with a modelled one.
        # Independent NED distance may replace existing value; a Hubble-flow value
        # fills only a missing/invalid canonical distance. All choices are reported.
        chosen_d = new_d
        if result.get("distanceEstimated") is True and old_d is not None:
            chosen_d = old_d
        item = {
            "index": index,
            "name": record.get("name"),
            "target": target,
            "canonicalName": result.get("canonicalName"),
            "oldDistanceMly": old_d,
            "nedDistanceMly": new_d,
            "chosenDistanceMly": chosen_d,
            "oldRedshift": old_z,
            "nedRedshift": new_z,
            "distanceMethod": result.get("distanceMethod"),
            "distanceEstimated": result.get("distanceEstimated"),
            "sourceUrl": result.get("url"),
            "reference": result.get("reference"),
        }
        if chosen_d is not None and (old_d is None or abs(chosen_d - old_d) > max(0.01, abs(old_d) * 0.001)):
            changes.append(item)
        elif new_z is not None and old_z is None:
            changes.append(item)
        if MODE == "apply":
            if chosen_d is not None:
                record["distanceMly"] = round(chosen_d, 6)
                record["distanceSource"] = "NASA/IPAC Extragalactic Database (NED)"
                record["distanceMethod"] = result.get("distanceMethod") if chosen_d == new_d else record.get("distanceMethod", "preserved existing measured distance")
                record["distanceEstimated"] = bool(result.get("distanceEstimated")) if chosen_d == new_d else bool(record.get("distanceEstimated", False))
                record["distanceEvidence"] = result.get("url")
            if new_z is not None:
                record["redshift"] = new_z
                record["redshiftSource"] = "NASA/IPAC Extragalactic Database (NED)"
                record["redshiftEvidence"] = result.get("url")

    report = {
        "mode": MODE,
        "runtimePath": str(RUNTIME),
        "runtimeRecordCount": len(rows),
        "uniqueTargetsQueried": len(cache),
        "apiStatusCounts": {},
        "changeCount": len(changes),
        "unresolvedCount": len(unresolved),
        "changes": changes,
        "unresolved": unresolved,
        "lookupResults": list(cache.values()),
        "policy": {
            "canonicalDistanceField": "distanceMly",
            "units": "million light-years (Mly)",
            "redshiftField": "redshift",
            "distanceRule": "Use NED mean redshift-independent distance when available; otherwise use NED 3K-CMB Hubble-flow distance only to fill a missing/invalid distance. Preserve existing distance against model-derived replacement.",
            "ambiguities": "Unresolved names are left unchanged and listed in this report."
        }
    }
    from collections import Counter
    report["apiStatusCounts"] = dict(Counter(x.get("status", "unknown") for x in cache.values()))
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if MODE == "apply" and changes:
        RUNTIME.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("mode", "runtimeRecordCount", "uniqueTargetsQueried", "apiStatusCounts", "changeCount", "unresolvedCount")}, indent=2))
    print(f"Full report: {REPORT}")
    if MODE == "audit":
        print("AUDIT ONLY: runtime catalog was not modified.")
    else:
        print("APPLY MODE: updated runtime catalog and added source evidence fields.")

if __name__ == "__main__":
    main()
