#!/usr/bin/env python3
"""Repair the 2MASX J22014163+1151237 distance across all six runtime catalogs.

The object is reported at roughly 374 million light-years (not 28 billion).
This is an identity-guarded, one-object correction; it does not blanket-edit
other catalog entries.
"""
import json, math
from pathlib import Path

TARGETS = [
    "viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0007.json",
    "viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json",
    "viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json",
    "viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json",
    "viewer/image-databases/NoirLab/databases/gv-noirlab-galaxies-full-0001.json",
    "viewer/image-databases/Spitzer/databases/gv-spitzer-galaxies-full-0011.json",
]
ALIASES = {"2MASX J22014163+1151237", "MASX J22014163+1151237"}
DISTANCE_MLY = 374.0
DISPLAY = "about 374 million light-years"

def norm(value):
    return "".join(c for c in str(value or "").upper() if c.isalnum())

needles = {norm(x) for x in ALIASES}
found = 0
changed_files = []
for filename in TARGETS:
    path = Path(filename)
    if not path.exists():
        raise SystemExit(f"Required catalog missing: {filename}")
    doc = json.loads(path.read_text(encoding="utf-8"))
    entries = doc.get("entries")
    if not isinstance(entries, list):
        raise SystemExit(f"Invalid catalog structure: {filename}")
    changed = False
    for i, entry in enumerate(entries):
        identifiers = [entry.get("name"), entry.get("title"), entry.get("displayName"),
                       entry.get("designation"), entry.get("archiveId")]
        identifiers += entry.get("curationAliases", []) if isinstance(entry.get("curationAliases"), list) else []
        if not any(any(n in norm(v) for n in needles) for v in identifiers if v):
            continue
        found += 1
        science = entry.setdefault("science", {})
        old = science.get("distanceMly")
        # Only replace this exact object, irrespective of the bad current value.
        science["distanceMly"] = DISTANCE_MLY
        science["distanceDisplay"] = DISPLAY
        science["distanceMethod"] = "curated_object_distance_2MASX_J22014163+1151237_20261012"
        science["distanceEvidence"] = "Catalog identity matched to 2MASX J22014163+1151237; published summaries report approximately 374 million light-years. This supersedes the erroneous 28-billion-light-year value."
        science["distanceEstimated"] = True
        entry["distance"] = DISPLAY
        # Recompute physical dimensions when a supported FOV pair is present.
        pairs = [
            ("avmHorizontalFovDegrees", "avmVerticalFovDegrees"),
            ("imageFovXDeg", "imageFovYDeg"),
            ("fieldOfViewDegrees", "fieldOfViewDegrees"),
        ]
        fov = None
        for xkey, ykey in pairs:
            x, y = entry.get(xkey), entry.get(ykey)
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and x > 0 and y > 0:
                fov = (x, y); break
        if fov:
            w = DISTANCE_MLY * 1000 * math.tan(math.radians(fov[0]) / 2) * 2
            h = DISTANCE_MLY * 1000 * math.tan(math.radians(fov[1]) / 2) * 2
            science["sizeKly"] = [w, h]
            science["sizeMethod"] = "derived_from_catalog_fov_and_corrected_distance"
            science["sizeEstimated"] = True
            science["sizeDisplay"] = f"EST. {w:.2f} × {h:.2f} KLY"
        changed = True
        print(f"{filename}[{i}] {entry.get('name')}: distanceMly {old!r} -> {DISTANCE_MLY}")
    if changed:
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        changed_files.append(filename)
if not found:
    raise SystemExit("Target object not found in any of the six catalogs; no files changed.")
print(f"MATCHES={found}; CHANGED_FILES={len(changed_files)}")
for name in changed_files:
    print("UPDATED", name)
