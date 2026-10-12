import json
from pathlib import Path

path = Path("viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json")
data = json.loads(path.read_text(encoding="utf-8"))
rows = [
    (21, 68.655838, 54.794271),
    (145, 68.655838, 54.794271),
    (260, 55.0, 17.840754),
    (652, 68.655838, 54.794271),
    (762, 45.0, 32.941794),
    (946, 0.0002, 1.562289),
    (984, 2400.0, 1810.167896),
    (987, 4000.0, 5772.967885),
]
applied = already = 0
for idx, before, after in rows:
    e = data["entries"][idx]
    current = float(e["science"]["distanceMly"])
    if abs(current-after) <= max(1e-8, abs(after)*1e-7):
        already += 1
        continue
    if abs(current-before) > max(1e-8, abs(before)*1e-7):
        raise RuntimeError(f"Guard failed at Hubble entry {idx}: current={current}, expected={before}")
    e["science"]["distanceMly"] = after
    display = (f"{round(after*1_000_000):,} light-years" if after < 1
               else f"{round(after, 3):,} million light-years")
    e["science"]["distanceDisplay"] = display
    e["science"]["distanceMethod"] = "NED_crossmatch_provisional_2026-10-12"
    e["science"]["distanceEvidence"] = (
        "Provisional NED-based replacement from distance-fix-157-log-20261012_204406.csv; "
        "independently unverified"
    )
    if isinstance(e.get("distance"), str):
        e["distance"] = display
    hf, vf = float(e.get("avmHorizontalFovDegrees") or 0), float(e.get("avmVerticalFovDegrees") or 0)
    if hf > 0 and vf > 0 and e["science"].get("sizeMethod") == "derived_from_avm_wcs_fov_and_distance":
        import math
        h = 2 * after * math.tan(math.radians(hf / 2)) * 1000
        v = 2 * after * math.tan(math.radians(vf / 2)) * 1000
        e["science"]["sizeKly"] = [h, v]
        e["science"]["sizeDisplay"] = f"EST. {round(h):,} × {round(v):,} LY"
        e["science"]["sizeEstimated"] = True
    applied += 1
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Hubble guarded rows: applied={applied}, already_correct={already}, total={len(rows)}")
