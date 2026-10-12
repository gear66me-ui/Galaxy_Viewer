#!/usr/bin/env python3
"""Guarded application of the supplied 157-row distance log.

Each row is accepted only if both the catalog entry identity and the recorded
pre-change distance match. Already-applied target values are idempotently skipped.
Known independently reviewed corrections are protected from provisional overrides.
"""
import csv, json, math
from pathlib import Path

CSV_PATH = Path(".github/data/distance-fix-157-log-20261012_204406.csv")
CATALOGS = {
    "gv-hubble-galaxies-full-0035-ESA-FOV.json": Path("viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json"),
    "gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json": Path("viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json"),
    "gv-eso-galaxies-full-0001.json": Path("viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json"),
    "gv-chandra-galaxies-full-0007.json": Path("viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0007.json"),
    "gv-spitzer-galaxies-full-0011.json": Path("viewer/image-databases/Spitzer/databases/gv-spitzer-galaxies-full-0011.json"),
    "gv-noirlab-galaxies-full-0001.json": Path("viewer/image-databases/NoirLab/databases/gv-noirlab-galaxies-full-0001.json"),
}
# Preserve previously independently reviewed values rather than replacing them
# with the provisional CSV's different values.
PROTECTED = {
    ("gv-eso-galaxies-full-0001.json", 154): 13.0,   # NGC 4945
    ("gv-eso-galaxies-full-0001.json", 193): 50.0,   # NGC 1097
    ("gv-eso-galaxies-full-0001.json", 197): 33.0,   # Messier 95
}

with CSV_PATH.open(newline="", encoding="utf-8-sig") as fh:
    rows = list(csv.DictReader(fh))
if len(rows) != 157:
    raise SystemExit(f"Expected 157 CSV rows, found {len(rows)}")

docs = {}
changed_paths = set()
applied = skipped_already = skipped_protected = conflicts = 0
for row in rows:
    fname = row["catalog_file"].strip()
    if fname not in CATALOGS:
        print(f"CONFLICT unknown catalog: {fname}")
        conflicts += 1
        continue
    idx = int(row["entry_index"])
    expected = float(row["before_Mly"])
    target = float(row["after_Mly"])
    path = CATALOGS[fname]
    if fname not in docs:
        docs[fname] = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(docs[fname].get("entries"), list):
            raise SystemExit(f"Missing entries array in {path}")
    entries = docs[fname]["entries"]
    if idx < 0 or idx >= len(entries):
        print(f"CONFLICT {fname}[{idx}]: index out of range")
        conflicts += 1
        continue
    entry = entries[idx]
    name = str(entry.get("name", "")).strip()
    if name != row["name"].strip():
        print(f"CONFLICT {fname}[{idx}]: name mismatch CSV={row['name']!r} catalog={name!r}")
        conflicts += 1
        continue
    science = entry.setdefault("science", {})
    current = science.get("distanceMly")
    protected = PROTECTED.get((fname, idx))
    if protected is not None and isinstance(current, (int, float)) and math.isclose(current, protected, rel_tol=1e-8, abs_tol=1e-10):
        print(f"PROTECTED {fname}[{idx}] {name}: independently reviewed {current} Mly")
        skipped_protected += 1
        continue
    if isinstance(current, (int, float)) and math.isclose(current, target, rel_tol=1e-8, abs_tol=1e-10):
        skipped_already += 1
        continue
    if not isinstance(current, (int, float)) or not math.isclose(current, expected, rel_tol=1e-7, abs_tol=1e-10):
        print(f"CONFLICT {fname}[{idx}] {name}: current={current!r}, expected={expected}, target={target}")
        conflicts += 1
        continue
    science["distanceMly"] = target
    science["distanceMethod"] = "provisional_NED_match_batch_20261012"
    science["distanceEvidence"] = "Supplied distance-fix-157 log; NED object match marked provisional and not independently verified."
    science["distanceEstimated"] = True
    if target < 1:
        science["distanceDisplay"] = f"{target * 1_000_000:,.0f} light-years"
    else:
        science["distanceDisplay"] = f"{target:,.6g} million light-years"
    wfov = entry.get("avmHorizontalFovDegrees", entry.get("imageFovXDeg"))
    hfov = entry.get("avmVerticalFovDegrees", entry.get("imageFovYDeg"))
    if isinstance(wfov, (int, float)) and isinstance(hfov, (int, float)) and wfov > 0 and hfov > 0:
        w_kly = target * 1000 * wfov * math.pi / 180
        h_kly = target * 1000 * hfov * math.pi / 180
        science["sizeKly"] = [w_kly, h_kly]
        science["sizeMethod"] = "derived_from_avm_wcs_fov_and_provisional_corrected_distance"
        science["sizeEstimated"] = True
        science["sizeDisplay"] = f"EST. {w_kly:.4f} × {h_kly:.4f} KLY"
    changed_paths.add(path)
    applied += 1

for fname, doc in docs.items():
    path = CATALOGS[fname]
    # Only write a catalog if at least one row was applied to it.
    if path in changed_paths:
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        parsed = json.loads(path.read_text(encoding="utf-8"))
        assert len(parsed["entries"]) == len(doc["entries"])
        for i, entry in enumerate(parsed["entries"]):
            v = entry.get("science", {}).get("distanceMly")
            if not isinstance(v, (int, float)) or v <= 0:
                raise SystemExit(f"Invalid distance in {path}[{i}]")
        print(f"VALIDATED {path}: {len(parsed['entries'])} entries")

print(f"SUMMARY rows={len(rows)} applied={applied} already_target={skipped_already} protected={skipped_protected} conflicts={conflicts}")
# Conflicts are reported and left untouched; they do not discard safe guarded changes.
