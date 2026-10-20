#!/usr/bin/env python3
"""Correct Abell 3158 in the active AVM runtime catalog 0004 and verify in place."""
import json
from pathlib import Path

PATH = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0004.json")
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
    raise AssertionError("Unknown runtime JSON shape; refusing to edit")

def walk_strings(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(v, str):
                yield k, v.strip()
            else:
                yield from walk_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_strings(v)

def is_target(entry):
    vals = [v.casefold() for _, v in walk_strings(entry)]
    return TARGET_NAME.casefold() in vals and TARGET_ARCHIVE_ID.casefold() in vals

def set_existing_redshift_fields(value):
    """Update existing redshift keys recursively; create top-level redshift only if absent."""
    found = []
    def visit(node, path="$"):
        if isinstance(node, dict):
            for key, child in node.items():
                if key.casefold().replace("_", "") in ("redshift", "redshiftz", "z"):
                    node[key] = EXPECTED_Z
                    found.append(path + "." + key)
                elif isinstance(child, (dict, list)):
                    visit(child, path + "." + key)
        elif isinstance(node, list):
            for i, child in enumerate(node):
                visit(child, f"{path}[{i}]")
    visit(value)
    if not found:
        value["redshift"] = EXPECTED_Z
        found.append("$.redshift (added canonical field)")
    return found

def main():
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    records = records_of(doc)
    matches = [(i, e) for i, e in enumerate(records) if isinstance(e, dict) and is_target(e)]
    if len(matches) != 1:
        nearby = [{"index": i, "strings": list(walk_strings(e))[:30]}
                  for i, e in enumerate(records) if isinstance(e, dict)
                  and any("3158" in v.casefold() for _, v in walk_strings(e))]
        raise AssertionError(f"Expected exactly one {TARGET_NAME}/{TARGET_ARCHIVE_ID} record; found {len(matches)}. Candidates: {nearby[:5]}")
    index, entry = matches[0]
    # Runtime 0004 uses top-level distanceMly as the canonical distance.
    entry["distanceMly"] = EXPECTED_DISTANCE_MLY
    if isinstance(entry.get("science"), dict) and "distanceMly" in entry["science"]:
        entry["science"]["distanceMly"] = EXPECTED_DISTANCE_MLY
    if isinstance(entry.get("metadata"), dict) and "distanceMly" in entry["metadata"]:
        entry["metadata"]["distanceMly"] = EXPECTED_DISTANCE_MLY
    zpaths = set_existing_redshift_fields(entry)
    PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    check = json.loads(PATH.read_text(encoding="utf-8"))
    checked = records_of(check)
    assert len(checked) == len(records), "Record count changed"
    found = [(i, e) for i, e in enumerate(checked) if isinstance(e, dict) and is_target(e)]
    assert len(found) == 1, f"Post-write target uniqueness failed: {len(found)}"
    i, e = found[0]
    assert float(e["distanceMly"]) == EXPECTED_DISTANCE_MLY, e.get("distanceMly")
    zs = []
    def collect_z(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.casefold().replace("_", "") in ("redshift", "redshiftz", "z"):
                    try: zs.append(float(v))
                    except (TypeError, ValueError): pass
                elif isinstance(v, (dict, list)):
                    collect_z(v)
        elif isinstance(node, list):
            for v in node: collect_z(v)
    collect_z(e)
    assert zs and all(z == EXPECTED_Z for z in zs), f"Redshift verification failed: {zs}"
    print(f"PASS: {PATH}; valid JSON; records={len(checked)}; unique target index={i}; archive={TARGET_ARCHIVE_ID}; redshift={EXPECTED_Z}; distanceMly={EXPECTED_DISTANCE_MLY}; redshift_fields={zpaths}")

if __name__ == "__main__":
    main()
