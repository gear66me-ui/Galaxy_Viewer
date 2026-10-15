#!/usr/bin/env python3
"""Apply only the two independently reviewed Galaxy Viewer distance corrections.

This script scans in-situ JSON catalogs and runtime metadata, matches exact object
identifiers/aliases, and changes only records whose existing distance is exactly
the reviewed old value (1000 Mly). Unexpected values stop the run; unrelated
records are never rewritten semantically.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path("viewer/image-databases")
REPORT = Path("distance-correction-report.json")

TARGETS = {
    "LEDA 1313424": {
        "aliases": {"LEDA 1313424", "Bullseye Galaxy"},
        "old_mly": 1000.0,
        "new_mly": 567.0,
        "method": "NASA_Hubble_LEDA_1313424_distance_567_Mly",
        "evidence": "NASA Science, LEDA 1313424: 567 million light-years; https://science.nasa.gov/asset/hubble/galaxy-leda-1313424-compass-image/ (checked 2026-10-15).",
    },
    "IC 2431": {
        "aliases": {
            "IC 2431", "PGC 25476", "CGCG 090-063", "UGC 4756",
            "Mrk 1224", "IRAS 09018+1447", "MCG +03-23-030",
            "VV 645", "LSBC D634-04", "SFRS 040",
        },
        "old_mly": 1000.0,
        "new_mly": 684.0,
        "method": "published_distance_reference_IC_2431_684_Mly",
        "evidence": "Published IC 2431 reference lists 684 Mly (209.71 Mpc); https://en.wikipedia.org/wiki/IC_2431 (checked 2026-10-15). SIMBAD batch median was 681.667 Mly.",
    },
}

IDENTITY_KEYS = (
    "name", "designation", "displayName", "objectName", "target",
    "aliases", "objectNames", "names", "identifiers", "alternateNames",
)

def norm(value):
    return " ".join(str(value).casefold().replace("_", " ").split())

def values(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(x) for x in value if isinstance(x, (str, int, float))]
    return []

def identity_values(record):
    out = []
    for key in IDENTITY_KEYS:
        out.extend(values(record.get(key)))
    # Title is only accepted when the entire title starts with the object identifier,
    # avoiding accidental matches to unrelated objects mentioned in descriptions.
    title = record.get("title")
    if isinstance(title, str):
        ntitle = norm(title)
        if any(ntitle == norm(a) or ntitle.startswith(norm(a) + " ") or ntitle.startswith(norm(a) + ":") for t in TARGETS.values() for a in t["aliases"]):
            out.append(title)
    return {norm(v) for v in out}

def recs(node, path="$"):
    if isinstance(node, dict):
        yield node, path
        for k, v in node.items():
            yield from recs(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from recs(v, f"{path}[{i}]")

def find_fov(record):
    candidates_x = ("avmHorizontalFovDegrees", "imageFovXDeg", "fieldOfViewXDegrees")
    candidates_y = ("avmVerticalFovDegrees", "imageFovYDeg", "fieldOfViewYDegrees")
    x = next((record.get(k) for k in candidates_x if isinstance(record.get(k), (int, float)) and record.get(k) > 0), None)
    y = next((record.get(k) for k in candidates_y if isinstance(record.get(k), (int, float)) and record.get(k) > 0), None)
    return x, y

def update_record(record, target):
    science = record.get("science")
    if not isinstance(science, dict):
        return False
    current = science.get("distanceMly")
    desired = target["new_mly"]
    if isinstance(current, (int, float)) and math.isclose(float(current), desired, rel_tol=0, abs_tol=1e-8):
        return False
    if not isinstance(current, (int, float)) or not math.isclose(float(current), target["old_mly"], rel_tol=0, abs_tol=1e-6):
        raise ValueError(f"unexpected current distance for matched record: {current!r}; expected {target['old_mly']} or already {desired}")
    science["distanceMly"] = desired
    science["distanceMethod"] = target["method"]
    science["distanceEvidence"] = target["evidence"]
    science["distanceEstimated"] = False
    science["distanceDisplay"] = f"{desired:g} million light-years"
    # Keep any legacy/display field consistent where it is clearly a distance string.
    if isinstance(record.get("distance"), str) and "light-year" in record["distance"].casefold():
        record["distance"] = f"{desired:g} million light-years"
    # Recompute physical image footprint only if the existing size is marked estimated.
    if science.get("sizeEstimated") is True:
        fx, fy = find_fov(record)
        if fx is not None and fy is not None:
            x_kly = desired * 1000 * math.radians(float(fx))
            y_kly = desired * 1000 * math.radians(float(fy))
            science["sizeKly"] = [round(x_kly, 3), round(y_kly, 3)]
            science["sizeMethod"] = "image_footprint_fov_distance_estimate_after_validated_distance_correction"
            science["sizeEstimated"] = True
            science["sizeDisplay"] = f"EST. {x_kly:.1f} × {y_kly:.1f} KLY"
    return True

def main():
    if not ROOT.exists():
        raise SystemExit(f"Catalog root missing: {ROOT}")
    report = {
        "branch_scope": "release",
        "policy": "only exact reviewed identities; only old value 1000 Mly -> reviewed new value",
        "targets": {},
        "files_changed": [],
        "unrelated_record_policy": "No non-target identities are modified.",
    }
    json_files = sorted(ROOT.rglob("*.json"))
    docs = {}
    for p in json_files:
        try:
            docs[p] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            # Every JSON under the image-database root is expected to be parseable.
            raise SystemExit(f"Cannot parse JSON {p}: {exc}")
    changes = []
    for target_name, target in TARGETS.items():
        aliases = {norm(a) for a in target["aliases"]}
        matches = []
        already = []
        for p, doc in docs.items():
            for record, record_path in recs(doc):
                science = record.get("science")
                if not isinstance(science, dict) or "distanceMly" not in science:
                    continue
                ids = identity_values(record)
                hit_aliases = sorted(ids & aliases)
                if not hit_aliases:
                    continue
                current = science.get("distanceMly")
                item = {
                    "file": str(p), "record_path": record_path,
                    "matched_aliases": hit_aliases, "current_distance_Mly": current,
                    "recommended_distance_Mly": target["new_mly"],
                }
                if isinstance(current, (int, float)) and math.isclose(float(current), target["new_mly"], rel_tol=0, abs_tol=1e-8):
                    already.append(item)
                    continue
                if not isinstance(current, (int, float)) or not math.isclose(float(current), target["old_mly"], rel_tol=0, abs_tol=1e-6):
                    raise SystemExit(
                        f"GUARD FAILED for {target_name}: {p} {record_path}, aliases={hit_aliases}, "
                        f"current={current!r}; expected {target['old_mly']} Mly or already {target['new_mly']} Mly. No files written."
                    )
                matches.append((p, record, record_path, item))
        if not matches and not already:
            raise SystemExit(f"GUARD FAILED: no matching in-situ catalog record found for {target_name}; no files written.")
        report["targets"][target_name] = {
            "old_distance_Mly": target["old_mly"], "new_distance_Mly": target["new_mly"],
            "records_to_change": [item for _, _, _, item in matches],
            "already_correct": already,
        }
        changes.extend(matches)
    # All guards passed before any file is written.
    changed_paths = set()
    for p, record, record_path, item in changes:
        target = next(TARGETS[name] for name, data in report["targets"].items() if item in data["records_to_change"])
        update_record(record, target)
        changed_paths.add(p)
    for p in changed_paths:
        p.write_text(json.dumps(docs[p], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["files_changed"] = sorted(str(p) for p in changed_paths)
    report["changed_record_count"] = len(changes)
    report["already_correct_record_count"] = sum(len(v["already_correct"]) for v in report["targets"].values())
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not changes:
        print("No catalog changes required; all matching records were already at target values.")

if __name__ == "__main__":
    main()
