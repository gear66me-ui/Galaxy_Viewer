#!/usr/bin/env python3
"""Apply and algorithmically verify the reviewed Abell 3158 runtime correction."""
import json
from pathlib import Path

PATH = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0003.json")
TARGET_NAME = "Abell 3158"
TARGET_ARCHIVE_ID = "noirlab2306a"
EXPECTED_Z = 0.0586
EXPECTED_DISTANCE_MLY = 830.0

def records_of(doc):
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for key in ("entries", "records", "galaxies", "catalog", "items", "data"):
            if isinstance(doc.get(key), list):
                return doc[key]
    raise AssertionError("Unknown runtime catalog JSON shape; refusing to edit")

def strings(entry):
    vals = []
    for key in ("designation", "name", "objectName", "targetName", "title", "archiveId", "archive_id", "id", "imageId", "image_id", "providerImageId"):
        v = entry.get(key)
        if isinstance(v, str):
            vals.append(v.strip())
    for key in ("metadata", "science", "image", "source", "avm"):
        v = entry.get(key)
        if isinstance(v, dict):
            vals.extend(str(v[k]).strip() for k in v if isinstance(v[k], str))
    return vals

def main():
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    records = records_of(doc)
    matches = []
    for i, entry in enumerate(records):
        if not isinstance(entry, dict):
            continue
        vals = strings(entry)
        name_match = any(v.casefold() == TARGET_NAME.casefold() for v in vals)
        archive_match = any(v.casefold() == TARGET_ARCHIVE_ID.casefold() for v in vals)
        if name_match and archive_match:
            matches.append((i, entry))
    if len(matches) != 1:
        # Diagnostic only: do not mutate unless the exact record is uniquely identified.
        nearby = [{"index": i, "values": strings(e)[:30]} for i, e in enumerate(records)
                  if isinstance(e, dict) and any("3158" in v.casefold() for v in strings(e))]
        raise AssertionError(f"Expected exactly one record matching both {TARGET_NAME!r} and {TARGET_ARCHIVE_ID!r}; found {len(matches)}. Candidates: {nearby[:10]}")
    index, entry = matches[0]
    science = entry.get("science")
    if not isinstance(science, dict):
        raise AssertionError(f"Target record index {index} has no science object; refusing schema guess")
    # Preserve the catalog's established canonical field names.
    if "distanceMly" not in science:
        raise AssertionError(f"Target record index {index} lacks science.distanceMly")
    science["distanceMly"] = EXPECTED_DISTANCE_MLY
    # Update an existing redshift field, without introducing competing field names.
    zkeys = [k for k in science if k.casefold() in ("redshift", "redshiftz", "redshift_z", "z")]
    if len(zkeys) != 1:
        raise AssertionError(f"Expected exactly one existing redshift field in science; found {zkeys}")
    science[zkeys[0]] = EXPECTED_Z
    # Keep any top-level canonical distance/redshift fields synchronized if present.
    for key in ("distanceMly",):
        if key in entry:
            entry[key] = EXPECTED_DISTANCE_MLY
    for key in list(entry):
        if key.casefold() in ("redshift", "redshiftz", "redshift_z", "z"):
            entry[key] = EXPECTED_Z
    PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Reload and assert the exact target record and values, plus unchanged record count.
    check = json.loads(PATH.read_text(encoding="utf-8"))
    checked = records_of(check)
    assert len(checked) == len(records), "Record count changed"
    found = [(i, e) for i, e in enumerate(checked) if isinstance(e, dict)
             and TARGET_NAME.casefold() in [v.casefold() for v in strings(e)]
             and TARGET_ARCHIVE_ID.casefold() in [v.casefold() for v in strings(e)]]
    assert len(found) == 1, f"Post-write target uniqueness check failed: {len(found)}"
    i, e = found[0]
    s = e["science"]
    assert float(s["distanceMly"]) == EXPECTED_DISTANCE_MLY, s.get("distanceMly")
    assert float(s[zkeys[0]]) == EXPECTED_Z, s.get(zkeys[0])
    print(f"PASS: {PATH} valid JSON; records={len(checked)}; unique target index={i}; archive={TARGET_ARCHIVE_ID}; redshift={EXPECTED_Z}; distanceMly={EXPECTED_DISTANCE_MLY}")
if __name__ == "__main__":
    main()
