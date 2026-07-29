"""Build the Galaxy Viewer curated outreach-galaxy catalog.

The script reads the ESO and HST outreach examples already stored in this
repository, checks a reviewed 40-galaxy allowlist against those source lists,
deduplicates the targets, and writes the compact ``targets`` schema consumed by
GV-beta-0005E.py.

It performs no network requests and modifies only the curated JSON catalog.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ESO_SOURCE = ROOT / "aladin-source-clone/examples/al-ESO-outreach.html"
HST_SOURCE = ROOT / "aladin-source-clone/examples/al-HST-outreach.html"
OUTPUT_PATH = Path(__file__).with_name("beautiful-galaxy-catalog-beta.json")

CURATED_TARGETS = [
    ("M 33", 0.50),
    ("M 77", 0.50),
    ("M 83", 0.50),
    ("M 87", 0.50),
    ("M 100", 0.50),
    ("M 104", 0.50),
    ("NGC 1300", 0.18),
    ("NGC 1365", 0.18),
    ("NGC 253", 0.18),
    ("NGC 300", 0.18),
    ("NGC 1097", 0.18),
    ("NGC 1232", 0.18),
    ("NGC 1566", 0.18),
    ("NGC 3621", 0.18),
    ("NGC 3627", 0.18),
    ("NGC 3628", 0.18),
    ("NGC 4565", 0.18),
    ("NGC 4650A", 0.18),
    ("NGC 6744", 0.18),
    ("NGC 7424", 0.18),
    ("NGC 7479", 0.18),
    ("NGC 7793", 0.18),
    ("Cartwheel Galaxy", 0.30),
    ("Hoag's Object", 0.22),
    ("Stephan's Quintet", 0.30),
    ("Centaurus A", 0.30),
    ("Circinus Galaxy", 0.22),
    ("Leo Triplet", 0.30),
    ("Spiderweb Galaxy", 0.30),
    ("Arp 147", 0.22),
    ("Arp 220", 0.22),
    ("Arp 299", 0.22),
    ("NGC 2442", 0.18),
    ("NGC 2997", 0.18),
    ("NGC 3521", 0.18),
    ("NGC 4030", 0.18),
    ("NGC 4254", 0.18),
    ("NGC 4535", 0.18),
    ("NGC 5247", 0.18),
    ("NGC 6384", 0.18),
]

FIELDS_PATTERN = re.compile(
    r"const\s+fields\s*=\s*(\[[\s\S]*?\]);",
    re.MULTILINE,
)


def extract_fields(path: Path) -> set[str]:
    """Return normalized target names from one outreach example."""
    text = path.read_text(encoding="utf-8")
    match = FIELDS_PATTERN.search(text)
    if not match:
        raise RuntimeError(f"Could not locate fields array in {path}")
    values = ast.literal_eval(match.group(1))
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise RuntimeError(f"Unexpected fields array structure in {path}")
    return {" ".join(value.split()).casefold() for value in values}


def build_catalog() -> dict:
    """Create the compact curated catalog consumed by Galaxy Viewer 5E."""
    eso_names = extract_fields(ESO_SOURCE)
    hst_names = extract_fields(HST_SOURCE)

    targets = []
    seen = set()
    for name, fov in CURATED_TARGETS:
        normalized = " ".join(name.split())
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)

        source_catalogs = []
        if key in eso_names:
            source_catalogs.append("ESO outreach")
        if key in hst_names:
            source_catalogs.append("HST outreach")
        if not source_catalogs:
            source_catalogs.append("reviewed outreach allowlist")

        targets.append(
            {
                "name": normalized,
                "fov": float(fov),
                "source_catalogs": source_catalogs,
            }
        )

    return {
        "module": "Galaxy Viewer Beautiful Galaxy Catalog",
        "version": "beta-0001",
        "record_count": len(targets),
        "selection_weight": 0.9,
        "source_files": [
            str(ESO_SOURCE.relative_to(ROOT)),
            str(HST_SOURCE.relative_to(ROOT)),
        ],
        "targets": targets,
    }


def main() -> None:
    payload = build_catalog()
    OUTPUT_PATH.write_text(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {payload['record_count']} curated galaxies to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
