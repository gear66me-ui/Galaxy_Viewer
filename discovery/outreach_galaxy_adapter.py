"""Build Galaxy Viewer's curated outreach-galaxy catalog.

This script reads the existing ESO and HST outreach example files already stored
in this repository, extracts their JavaScript ``fields`` arrays, keeps only the
explicitly reviewed galaxy allowlist below, deduplicates names, and writes
``beautiful-galaxy-catalog-beta.json``.

It performs no network requests and does not modify viewer or launcher files.
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

CURATED_GALAXY_NAMES = [
    "M 33",
    "M 77",
    "M 83",
    "M 84",
    "M 87",
    "M 95",
    "M 96",
    "M 100",
    "M 104",
    "Messier 49",
    "Messier 61",
    "Messier 66",
    "Messier 74",
    "Messier 77",
    "Messier 82",
    "Messier 83",
    "Messier 84",
    "Messier 85",
    "Messier 86",
    "Messier 87",
    "Messier 90",
    "Messier 95",
    "Messier 96",
    "Messier 98",
    "Messier 100",
    "Messier 104",
    "Messier 106",
    "NGC 55",
    "NGC 87",
    "NGC 92",
    "NGC 105",
    "NGC 134",
    "NGC 157",
    "NGC 247",
    "NGC 253",
    "NGC 300",
    "NGC 406",
    "NGC 428",
    "NGC 470",
    "NGC 613",
    "NGC 660",
    "NGC 691",
    "NGC 695",
    "NGC 7727",
    "NGC 7793",
    "NGC 799",
    "NGC 908",
    "NGC 936",
    "NGC 972",
    "NGC 986",
    "NGC 1022",
    "NGC 1084",
    "NGC 1087",
    "NGC 1097",
    "NGC 1187",
    "NGC 1222",
    "NGC 1232",
    "NGC 1288",
    "NGC 1300",
    "NGC 1309",
    "NGC 1313",
    "NGC 1316",
    "NGC 1350",
    "NGC 1365",
    "NGC 1398",
    "NGC 1433",
    "NGC 1448",
    "NGC 1559",
    "NGC 1566",
    "NGC 1637",
    "NGC 1705",
    "NGC 1792",
    "NGC 1964",
    "NGC 2217",
    "NGC 2273",
    "NGC 2336",
    "NGC 2403",
    "NGC 2442",
    "NGC 2613",
    "NGC 2768",
    "NGC 2770",
    "NGC 2865",
    "NGC 2976",
    "NGC 2985",
    "NGC 2997",
    "NGC 3147",
    "NGC 3166",
    "NGC 3190",
    "NGC 3244",
    "NGC 3259",
    "NGC 3314",
    "NGC 3344",
    "NGC 3370",
    "NGC 3384",
    "NGC 3447",
    "NGC 3521",
    "NGC 3568",
    "NGC 3597",
    "NGC 3621",
    "NGC 3627",
    "NGC 3628",
    "NGC 3738",
    "NGC 3921",
    "NGC 3981",
    "NGC 3982",
    "NGC 4030",
    "NGC 4068",
    "NGC 4100",
    "NGC 4102",
    "NGC 4183",
    "NGC 4194",
    "NGC 4237",
    "NGC 4254",
    "NGC 4261",
    "NGC 4303",
    "NGC 4365",
    "NGC 4402",
    "NGC 4424",
    "NGC 4435",
    "NGC 4485",
    "NGC 4522",
    "NGC 4526",
    "NGC 4535",
    "NGC 4548",
    "NGC 4565",
    "NGC 4567",
    "NGC 4571",
    "NGC 4603",
    "NGC 4605",
    "NGC 4650A",
    "NGC 4651",
    "NGC 4656",
    "NGC 4660",
    "NGC 4666",
    "NGC 4689",
    "NGC 4707",
    "NGC 4762",
    "NGC 4789A",
    "NGC 4845",
    "NGC 4861",
    "NGC 4889",
    "NGC 4981",
    "NGC 5011B",
    "NGC 5018",
    "NGC 5090",
    "NGC 5128",
    "NGC 5236",
    "NGC 5247",
    "NGC 5248",
    "NGC 5252",
    "NGC 5253",
    "NGC 5291",
    "NGC 5331",
    "NGC 5364",
    "NGC 5426",
    "NGC 5477",
    "NGC 5548",
    "NGC 5584",
    "NGC 5643",
    "NGC 5806",
    "NGC 5917",
    "NGC 5921",
    "NGC 5972",
    "NGC 6052",
    "NGC 6118",
    "NGC 6139",
    "NGC 6300",
    "NGC 6384",
    "NGC 6744",
    "NGC 6753",
    "NGC 6769",
    "NGC 6782",
    "NGC 6861",
    "NGC 6902",
    "NGC 7098",
    "NGC 7173",
    "NGC 7252",
    "NGC 7329",
    "NGC 7424",
    "NGC 7479",
    "NGC 7582",
    "NGC 7640",
    "IC 10",
    "IC 335",
    "IC 391",
    "IC 559",
    "IC 755",
    "IC 1727",
    "IC 1954",
    "IC 2006",
    "IC 2163",
    "IC 2184",
    "IC 2233",
    "IC 3506",
    "IC 4653",
    "IC 4710",
    "IC 5063",
    "IC 5298",
    "UGC 477",
    "UGC 2885",
    "UGC 3855",
    "UGC 4459",
    "UGC 5101",
    "UGC 5497",
    "UGC 6093",
    "UGC 8201",
    "UGC 8335",
    "UGC 9128",
    "UGC 11411",
    "UGC 12812",
    "Cartwheel Galaxy",
    "Hoag's Object",
    "Stephan's Quintet",
    "Centaurus A",
    "Circinus Galaxy",
    "Leo Triplet",
    "Spiderweb Galaxy",
    "WLM Galaxy",
    "Barnard's Galaxy",
    "Sculptor Dwarf Galaxy",
    "Fornax Dwarf Galaxy",
    "Carina Dwarf Galaxy",
    "Sagittarius Dwarf Galaxy",
    "Leo A",
    "Holmberg IX",
    "I Zw 18",
    "Arp 147",
    "Arp 220",
    "Arp 299"
]

FIELDS_PATTERN = re.compile(
    r"const\s+fields\s*=\s*(\[[\s\S]*?\]);",
    re.MULTILINE,
)


def extract_fields(path: Path) -> list[str]:
    """Extract the JavaScript fields array from one outreach example."""
    text = path.read_text(encoding="utf-8")
    match = FIELDS_PATTERN.search(text)
    if not match:
        raise RuntimeError(f"Could not locate fields array in {path}")
    values = ast.literal_eval(match.group(1))
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise RuntimeError(f"Unexpected fields array structure in {path}")
    return values


def preferred_fov_deg(name: str) -> float:
    """Return a conservative initial field of view for a curated target."""
    normalized = " ".join(name.split()).upper()
    if normalized.startswith(("M ", "MESSIER ")):
        return 0.50
    if normalized.startswith("NGC "):
        return 0.18
    if normalized.startswith("IC "):
        return 0.16
    if normalized.startswith("UGC "):
        return 0.14
    if any(label in normalized for label in ("TRIPLET", "QUINTET", "CARTWHEEL", "CENTAURUS", "SPIDERWEB")):
        return 0.30
    return 0.22


def build_catalog() -> dict:
    """Create the reviewed, deduplicated outreach galaxy catalog."""
    source_membership: dict[str, set[str]] = {}
    for source_name, source_path in (
        ("ESO outreach", ESO_SOURCE),
        ("HST outreach", HST_SOURCE),
    ):
        for target in extract_fields(source_path):
            normalized = " ".join(target.split())
            source_membership.setdefault(normalized.casefold(), set()).add(source_name)

    records = []
    seen = set()
    for index, target in enumerate(CURATED_GALAXY_NAMES, start=1):
        normalized = " ".join(target.split())
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)

        catalogs = sorted(source_membership.get(key, set()))
        if not catalogs:
            catalogs = ["reviewed outreach allowlist"]

        records.append(
            {
                "primary_name": normalized,
                "target_name": normalized,
                "source": "OUTREACH",
                "source_id": f"OUTREACH:{index:04d}",
                "source_catalogs": catalogs,
                "preferred_fov_deg": preferred_fov_deg(normalized),
                "curated_priority": 1,
                "status": "curated",
            }
        )

    return {
        "module": "Galaxy Viewer Beautiful Galaxy Catalog",
        "version": "beta-0001",
        "record_count": len(records),
        "selection_weight": 0.9,
        "source_files": [
            str(ESO_SOURCE.relative_to(ROOT)),
            str(HST_SOURCE.relative_to(ROOT)),
        ],
        "records": records,
    }


def main() -> None:
    payload = build_catalog()
    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {payload['record_count']} curated galaxies to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
