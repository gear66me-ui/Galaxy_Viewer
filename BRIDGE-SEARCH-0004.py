# BRIDGE-SEARCH-0004
from __future__ import annotations

import urllib.request

BRIDGE_VERSION = "BRIDGE-SEARCH-0004"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/c821f86a66b6d796a93a5cb04939e2f98b6e0a17/BRIDGE-SEARCH-0003.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0003"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0004"')
source = source.replace('BATCH_SIZE = 500', 'BATCH_SIZE = 40')
source = source.replace('def fetch_text(url: str, timeout: int = 120)', 'def fetch_text(url: str, timeout: int = 45)')
source = source.replace('timeout=90))', 'timeout=30))')

old_main = '''def main():
    source_rows = load_main()
    backup1 = [simbad_backup(row) if any(missing(row.get(f, "")) for f in FIELDS[3:12]) else simbad_backup(row) for row in source_rows]
    backup2 = [vizier_backup({**row, **{k: (b.get(k) or row.get(k, "")) for k in FIELDS}}) for row, b in zip(source_rows, backup1)]
    combined = build_combined(source_rows, backup1, backup2)
    make_workbook({"Main": source_rows, "Backup 1": backup1, "Backup 2": backup2, "Combined": combined})
    token = userdata.get(TOKEN_SECRET)
    if not token:
        raise RuntimeError(f"Colab Secret {TOKEN_SECRET!r} is required")
    print(upload(OUTPUT_PATH, token))
'''

new_main = '''def _blank_backup(row):
    out = {field: "" for field in FIELDS}
    out["Object"] = row.get("Object", "")
    out["ICRS coordinates"] = row.get("ICRS coordinates", "")
    return out


def _needs_backup(row):
    critical = [
        "Redshift (z) / Distance", "Morphological type", "Angular size",
        "Radial velocity", "Magnitude", "Distance method"
    ]
    return any(missing(row.get(field, "")) for field in critical)


def _merge_nonempty(primary, backup):
    merged = dict(primary)
    for field in FIELDS:
        value = backup.get(field, "")
        if value and not missing(value):
            merged[field] = value
    return merged


def main():
    source_rows = load_main()

    backup1 = []
    for row in source_rows:
        backup1.append(simbad_backup(row) if _needs_backup(row) else _blank_backup(row))

    backup2 = []
    for row, first_backup in zip(source_rows, backup1):
        merged = _merge_nonempty(row, first_backup)
        backup2.append(vizier_backup(merged) if _needs_backup(merged) else _blank_backup(row))

    combined = build_combined(source_rows, backup1, backup2)
    make_workbook({"Main": source_rows, "Backup 1": backup1, "Backup 2": backup2, "Combined": combined})

    token = userdata.get(TOKEN_SECRET)
    if not token:
        raise RuntimeError(f"Colab Secret {TOKEN_SECRET!r} is required")
    print(upload(OUTPUT_PATH, token))
'''

if old_main not in source:
    raise RuntimeError("BRIDGE-SEARCH-0003 main block did not match the expected release source")

source = source.replace(old_main, new_main)
exec(compile(source, "BRIDGE-SEARCH-0004-runtime.py", "exec"), globals())
