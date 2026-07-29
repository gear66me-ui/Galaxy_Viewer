"""Build up to 1,000 visually promising Galaxy Viewer targets.

The builder gives first priority to objects appearing in the repository's ESO and
HST outreach examples, verifies every candidate against SIMBAD, keeps confirmed
galaxy classes only, rejects stellar/nebular/cluster/quasar classes, prefers
objects with measured angular extent, and supplements the outreach results with
well-documented extended SIMBAD galaxies until the requested catalog size is met.

This module writes only ``beautiful-galaxy-catalog-beta.json``. It does not modify
viewer, launcher, artwork, manifest, service-worker, or workflow files.
"""

from __future__ import annotations

import ast
import csv
import io
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ESO_SOURCE = ROOT / "aladin-source-clone/examples/al-ESO-outreach.html"
HST_SOURCE = ROOT / "aladin-source-clone/examples/al-HST-outreach.html"
OUTPUT_PATH = Path(__file__).with_name("beautiful-galaxy-catalog-beta.json")
SIMBAD_TAP_SYNC_URL = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"

TARGET_COUNT = 1000
MIN_MAJOR_AXIS_ARCMIN = 0.75
OUTREACH_MIN_MAJOR_AXIS_ARCMIN = 0.35
MIN_BIBLIOGRAPHY_REFERENCES = 8
SUPPLEMENT_POOL_SIZE = 12000
QUERY_BATCH_SIZE = 150
HTTP_TIMEOUT_SECONDS = 120

# Confirmed extragalactic object classes. Generic AGN/quasar/radio-source classes
# are intentionally absent because many render as stellar points in DSS2.
ALLOWED_GALAXY_TYPES = {
    "G",
    "LSB",
    "bCG",
    "SBG",
    "H2G",
    "EmG",
    "SyG",
    "GiC",
    "BiC",
    "GiG",
    "GiP",
    "IG",
    "PaG",
}

FIELDS_PATTERN = re.compile(
    r"const\s+fields\s*=\s*(\[[\s\S]*?\]);",
    re.MULTILINE,
)


@dataclass(frozen=True)
class GalaxyTarget:
    """One SIMBAD-verified curated target."""

    name: str
    ra_deg: float
    dec_deg: float
    object_type: str
    major_axis_arcmin: float | None
    minor_axis_arcmin: float | None
    bibliography_references: int
    source_catalogs: tuple[str, ...]
    outreach_priority: bool

    @property
    def preferred_fov_deg(self) -> float:
        """Frame the measured galaxy with useful surrounding context."""
        major = self.major_axis_arcmin
        if major is None or not math.isfinite(major) or major <= 0:
            return 0.18 if self.outreach_priority else 0.12
        # Roughly 2.8 major-axis diameters, constrained for mobile viewing.
        return round(min(1.5, max(0.06, major * 2.8 / 60.0)), 4)

    @property
    def quality_score(self) -> float:
        """Rank large, documented outreach galaxies ahead of marginal targets."""
        major = max(0.0, self.major_axis_arcmin or 0.0)
        size_score = min(60.0, math.log1p(major) * 22.0)
        reference_score = min(25.0, math.log1p(self.bibliography_references) * 5.0)
        outreach_score = 15.0 if self.outreach_priority else 0.0
        return round(size_score + reference_score + outreach_score, 3)


def normalize_name(value: str) -> str:
    """Normalize whitespace without changing the astronomical identifier."""
    return " ".join(value.split()).strip()


def escape_adql(value: str) -> str:
    """Escape one ADQL string literal."""
    return value.replace("'", "''")


def optional_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        result = float(text)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def optional_int(value: str | None) -> int:
    number = optional_float(value)
    return max(0, int(number)) if number is not None else 0


def extract_fields(path: Path) -> list[str]:
    """Extract and normalize the JavaScript outreach target list."""
    text = path.read_text(encoding="utf-8")
    match = FIELDS_PATTERN.search(text)
    if not match:
        raise RuntimeError(f"Could not locate fields array in {path}")
    values = ast.literal_eval(match.group(1))
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise RuntimeError(f"Unexpected fields array structure in {path}")
    return [normalize_name(value) for value in values if normalize_name(value)]


def outreach_candidates() -> tuple[list[str], dict[str, tuple[str, ...]]]:
    """Merge the ESO/HST lists while retaining source membership."""
    membership: dict[str, set[str]] = {}
    canonical: dict[str, str] = {}
    for source_name, path in (
        ("ESO outreach", ESO_SOURCE),
        ("HST outreach", HST_SOURCE),
    ):
        for name in extract_fields(path):
            key = name.casefold()
            canonical.setdefault(key, name)
            membership.setdefault(key, set()).add(source_name)

    names = [canonical[key] for key in sorted(canonical)]
    sources = {key: tuple(sorted(value)) for key, value in membership.items()}
    return names, sources


def chunks(values: Sequence[str], size: int) -> Iterator[Sequence[str]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def request_csv(adql: str) -> str:
    """Execute one SIMBAD TAP synchronous query and return CSV text."""
    body = urlencode(
        {
            "request": "doQuery",
            "lang": "adql",
            "format": "csv",
            "query": adql,
        }
    ).encode("utf-8")
    request = Request(
        SIMBAD_TAP_SYNC_URL,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "Galaxy-Viewer-Beautiful-Catalog/0002",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:800]
        raise RuntimeError(f"SIMBAD returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach SIMBAD: {exc.reason}") from exc


def galaxy_type_clause() -> str:
    return ",".join(f"'{escape_adql(value)}'" for value in sorted(ALLOWED_GALAXY_TYPES))


def query_outreach_batch(names: Sequence[str]) -> str:
    """Resolve outreach aliases through SIMBAD's identifier table."""
    identifiers = ",".join(f"'{escape_adql(name)}'" for name in names)
    return f"""
SELECT
    ident.id AS requested_id,
    basic.main_id,
    basic.ra,
    basic.dec,
    basic.otype,
    basic.nbref,
    basic.galdim_majaxis,
    basic.galdim_minaxis
FROM ident
JOIN basic ON ident.oidref = basic.oid
WHERE ident.id IN ({identifiers})
  AND basic.ra IS NOT NULL
  AND basic.dec IS NOT NULL
  AND basic.otype IN ({galaxy_type_clause()})
""".strip()


def query_supplemental_pool() -> str:
    """Request a large pool of extended, well-documented galaxies."""
    return f"""
SELECT TOP {SUPPLEMENT_POOL_SIZE}
    main_id,
    ra,
    dec,
    otype,
    nbref,
    galdim_majaxis,
    galdim_minaxis
FROM basic
WHERE ra IS NOT NULL
  AND dec IS NOT NULL
  AND otype IN ({galaxy_type_clause()})
  AND nbref >= {MIN_BIBLIOGRAPHY_REFERENCES}
  AND galdim_majaxis >= {MIN_MAJOR_AXIS_ARCMIN}
ORDER BY galdim_majaxis DESC, nbref DESC
""".strip()


def rows_from_csv(csv_text: str) -> Iterable[dict[str, str]]:
    return csv.DictReader(io.StringIO(csv_text))


def row_to_target(
    row: dict[str, str],
    *,
    source_catalogs: tuple[str, ...],
    outreach_priority: bool,
) -> GalaxyTarget | None:
    """Validate and normalize one SIMBAD result."""
    name = normalize_name(row.get("main_id") or row.get("requested_id") or "")
    object_type = normalize_name(row.get("otype") or "")
    ra = optional_float(row.get("ra"))
    dec = optional_float(row.get("dec"))
    major = optional_float(row.get("galdim_majaxis"))
    minor = optional_float(row.get("galdim_minaxis"))
    references = optional_int(row.get("nbref"))

    if not name or ra is None or dec is None:
        return None
    if object_type not in ALLOWED_GALAXY_TYPES:
        return None
    if not (0.0 <= ra < 360.0 and -90.0 <= dec <= 90.0):
        return None

    minimum_size = OUTREACH_MIN_MAJOR_AXIS_ARCMIN if outreach_priority else MIN_MAJOR_AXIS_ARCMIN
    if major is not None and major < minimum_size:
        return None
    if not outreach_priority and major is None:
        return None
    if not outreach_priority and references < MIN_BIBLIOGRAPHY_REFERENCES:
        return None

    return GalaxyTarget(
        name=name,
        ra_deg=ra,
        dec_deg=dec,
        object_type=object_type,
        major_axis_arcmin=major,
        minor_axis_arcmin=minor,
        bibliography_references=references,
        source_catalogs=source_catalogs,
        outreach_priority=outreach_priority,
    )


def target_identity(target: GalaxyTarget) -> tuple[int, int]:
    """Deduplicate aliases resolving to effectively the same sky position."""
    return (round(target.ra_deg * 3600), round(target.dec_deg * 3600))


def resolve_outreach_targets() -> list[GalaxyTarget]:
    names, memberships = outreach_candidates()
    targets: list[GalaxyTarget] = []
    seen_positions: set[tuple[int, int]] = set()

    for batch in chunks(names, QUERY_BATCH_SIZE):
        for row in rows_from_csv(request_csv(query_outreach_batch(batch))):
            requested = normalize_name(row.get("requested_id") or "")
            sources = memberships.get(requested.casefold(), ("ESO/HST outreach",))
            target = row_to_target(
                row,
                source_catalogs=sources,
                outreach_priority=True,
            )
            if target is None:
                continue
            identity = target_identity(target)
            if identity in seen_positions:
                continue
            seen_positions.add(identity)
            targets.append(target)

    return targets


def resolve_supplemental_targets(existing: Sequence[GalaxyTarget]) -> list[GalaxyTarget]:
    """Fill the catalog with large SIMBAD galaxies not already represented."""
    targets: list[GalaxyTarget] = []
    seen_positions = {target_identity(target) for target in existing}

    for row in rows_from_csv(request_csv(query_supplemental_pool())):
        target = row_to_target(
            row,
            source_catalogs=("SIMBAD extended-galaxy supplement",),
            outreach_priority=False,
        )
        if target is None:
            continue
        identity = target_identity(target)
        if identity in seen_positions:
            continue
        seen_positions.add(identity)
        targets.append(target)
        if len(existing) + len(targets) >= TARGET_COUNT:
            break

    return targets


def serialize_target(target: GalaxyTarget) -> dict:
    return {
        "name": target.name,
        "fov": target.preferred_fov_deg,
        "ra_deg": round(target.ra_deg, 8),
        "dec_deg": round(target.dec_deg, 8),
        "object_type": target.object_type,
        "major_axis_arcmin": target.major_axis_arcmin,
        "minor_axis_arcmin": target.minor_axis_arcmin,
        "bibliography_references": target.bibliography_references,
        "quality_score": target.quality_score,
        "source_catalogs": list(target.source_catalogs),
        "outreach_priority": target.outreach_priority,
    }


def build_catalog() -> dict:
    """Build a ranked catalog with outreach galaxies first, capped at 1,000."""
    outreach = resolve_outreach_targets()
    supplemental = resolve_supplemental_targets(outreach)

    outreach.sort(key=lambda target: (-target.quality_score, target.name.casefold()))
    supplemental.sort(key=lambda target: (-target.quality_score, target.name.casefold()))
    targets = (outreach + supplemental)[:TARGET_COUNT]

    if len(targets) < TARGET_COUNT:
        raise RuntimeError(
            f"Only {len(targets)} qualified galaxies were found; {TARGET_COUNT} requested. "
            "Lower the size threshold only after reviewing visual quality."
        )

    return {
        "module": "Galaxy Viewer Beautiful Galaxy Catalog",
        "version": "beta-0002",
        "record_count": len(targets),
        "selection_weight": 0.9,
        "target_count_requested": TARGET_COUNT,
        "quality_policy": {
            "confirmed_galaxy_types": sorted(ALLOWED_GALAXY_TYPES),
            "outreach_min_major_axis_arcmin": OUTREACH_MIN_MAJOR_AXIS_ARCMIN,
            "supplement_min_major_axis_arcmin": MIN_MAJOR_AXIS_ARCMIN,
            "supplement_min_bibliography_references": MIN_BIBLIOGRAPHY_REFERENCES,
            "stellar_nebular_cluster_quasar_classes_excluded": True,
        },
        "source_files": [
            str(ESO_SOURCE.relative_to(ROOT)),
            str(HST_SOURCE.relative_to(ROOT)),
        ],
        "outreach_record_count": len(outreach),
        "supplemental_record_count": len(targets) - len(outreach),
        "targets": [serialize_target(target) for target in targets],
    }


def main() -> None:
    payload = build_catalog()
    OUTPUT_PATH.write_text(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Saved {payload['record_count']} galaxies "
        f"({payload['outreach_record_count']} outreach, "
        f"{payload['supplemental_record_count']} supplemental) to {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
