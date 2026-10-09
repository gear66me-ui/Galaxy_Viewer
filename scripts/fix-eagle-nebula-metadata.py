import json
from pathlib import Path

targets = [
    (Path("viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json"), "entries", "heic0506b", "esa"),
    (Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0003.json"), "records", "heic0506b", "runtime"),
]

distance_evidence = "NASA Eagle Nebula / Pillars of Creation object distance: 6,500 light-years"
age_evidence = "Approximate 1–2 million-year age of the young stellar population; representative estimate 1.5 Myr."

for path, collection, archive_id, kind in targets:
    doc = json.loads(path.read_text(encoding="utf-8"))
    matches = [r for r in doc[collection] if r.get("archiveId") == archive_id and (kind != "runtime" or r.get("providerKey") == "hubble")]
    if len(matches) != 1:
        raise RuntimeError(f"{path}: expected one {archive_id} record, found {len(matches)}")
    rec = matches[0]
    rec["distance"] = "6,500 light-years"
    rec["imageBand"] = "Visible light"
    science = rec.setdefault("science", {})
    science.update({
        "distanceMly": 0.0065,
        "distanceMethod": "NASA_Hubble_authoritative_object_distance",
        "distanceEvidence": distance_evidence,
        "distanceDisplay": "6.5 KLY",
        "distanceEstimated": False,
        "ageGyr": 0.0000015,
        "ageMethod": "young_eagle_nebula_cluster_age_reference",
        "ageEstimated": True,
        "ageDisplay": "EST. 1.5 MYR",
        "ageEvidence": age_evidence,
    })
    if kind == "esa":
        rec["age"] = "EST. 1.5 MYR"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Re-open and verify the targeted record after serialization.
    check = json.loads(path.read_text(encoding="utf-8"))
    again = [r for r in check[collection] if r.get("archiveId") == archive_id and (kind != "runtime" or r.get("providerKey") == "hubble")]
    assert len(again) == 1 and again[0]["distance"] == "6,500 light-years"
    assert again[0]["imageBand"] == "Visible light"
    assert again[0]["science"]["ageDisplay"] == "EST. 1.5 MYR"
    print(f"Verified {path}: {archive_id}, distance/age/imageBand")
