"""SIMBAD adapter for Galaxy Discovery Engine — filtered galaxy revision.

Uses the public SIMBAD TAP sync endpoint and Python's standard library only.
The selection is intentionally conservative: confirmed galaxy classes, recognized
optical-galaxy catalogue names, and bibliography-backed objects only. Radio-source,
quasar, generic AGN, stellar, and unknown point-source classes are excluded.
"""

from __future__ import annotations

import csv
import importlib.util
import io
import random
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SIMBAD_TAP_SYNC_URL = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
FOUNDATION_PATH = Path(__file__).with_name("GV-galaxy-discovery-beta-0001.py")
DEFAULT_POOL_SIZE = 1000
DEFAULT_TIMEOUT_SECONDS = 60

# These classes describe galaxies themselves rather than unresolved nuclei,
# radio detections, quasars, or generic point sources.
ALLOWED_GALAXY_TYPES = ("G", "LSB", "bCG", "SBG", "H2G", "EmG", "SyG")

# Established optical-galaxy catalogues are used as a second independent gate.
# The SIMBAD object type remains authoritative; the name gate removes ambiguous
# radio-source identifiers such as 3C/4C and generic NAME objects.
GALAXY_NAME_PATTERN = re.compile(
    r"^(?:M\s+\d+|NGC\s*\d+|IC\s*\d+|UGC\s*\d+|PGC\s*\d+|LEDA\s*\d+|"
    r"ESO\s+\S+|MCG\s*[+-]\S+|CGCG\s+\S+|Mrk\s*\d+)$",
    re.IGNORECASE,
)


class SimbadAdapterError(RuntimeError):
    """Raised when SIMBAD cannot return a usable candidate pool."""


def _load_foundation_module():
    module_name = "gv_discovery_foundation"
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, FOUNDATION_PATH)
    if spec is None or spec.loader is None:
        raise SimbadAdapterError(f"Could not load discovery foundation: {FOUNDATION_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _optional_float(value: str | None) -> float | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _preferred_fov_for_name(name: str) -> float:
    """Choose a tighter initial FOV from catalogue family.

    This is a conservative visual heuristic until angular-dimension joins are
    introduced. It prevents the previous 0.25-degree one-size-fits-all framing
    from turning compact galaxies into tiny star-like points.
    """
    normalized = " ".join(name.split()).upper()
    if normalized.startswith("M "):
        return 0.50
    if normalized.startswith(("NGC ", "IC ")):
        return 0.14
    if normalized.startswith(("UGC ", "ESO ")):
        return 0.10
    return 0.08


def _build_adql(pool_size: int) -> str:
    if pool_size < 1:
        raise ValueError("pool_size must be at least 1")

    galaxy_types = ",".join(f"'{value}'" for value in ALLOWED_GALAXY_TYPES)
    return f"""
SELECT TOP {pool_size}
    main_id,
    ra,
    dec,
    otype,
    nbref
FROM basic
WHERE ra IS NOT NULL
  AND dec IS NOT NULL
  AND otype IN ({galaxy_types})
  AND nbref >= 20
  AND (
       main_id LIKE 'M %'
    OR main_id LIKE 'NGC%'
    OR main_id LIKE 'IC %'
    OR main_id LIKE 'UGC%'
    OR main_id LIKE 'PGC%'
    OR main_id LIKE 'LEDA%'
    OR main_id LIKE 'ESO %'
    OR main_id LIKE 'MCG%'
    OR main_id LIKE 'CGCG%'
    OR main_id LIKE 'Mrk %'
  )
ORDER BY nbref DESC
""".strip()


def _request_csv(adql: str, *, timeout: int) -> str:
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
            "User-Agent": "Galaxy-Viewer-Discovery-Filtered/0002",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise SimbadAdapterError(f"SIMBAD returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise SimbadAdapterError(f"Could not reach SIMBAD: {exc.reason}") from exc


def _normalize_rows(rows: Iterable[dict[str, str]]):
    foundation = _load_foundation_module()
    GalaxyCandidate = foundation.GalaxyCandidate

    records = []
    seen = set()

    for row in rows:
        name = (row.get("main_id") or "").strip()
        object_type = (row.get("otype") or "").strip()
        ra = _optional_float(row.get("ra"))
        dec = _optional_float(row.get("dec"))
        nbref = _optional_float(row.get("nbref")) or 0.0

        if not name or ra is None or dec is None:
            continue
        if object_type not in ALLOWED_GALAXY_TYPES:
            continue
        if not GALAXY_NAME_PATTERN.match(" ".join(name.split())):
            continue
        if nbref < 20:
            continue

        key = (name.casefold(), round(ra, 7), round(dec, 7))
        if key in seen:
            continue
        seen.add(key)

        records.append(
            GalaxyCandidate(
                primary_name=name,
                ra_deg=ra,
                dec_deg=dec,
                source="SIMBAD",
                source_id=f"SIMBAD:{name}",
                major_axis_arcmin=None,
                minor_axis_arcmin=None,
                morphology=object_type,
                preferred_fov_deg=_preferred_fov_for_name(name),
                preferred_survey=None,
            )
        )

    return records


def fetch_random_galaxies(
    limit: int = 100,
    *,
    pool_size: int = DEFAULT_POOL_SIZE,
    seed: int | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
):
    """Fetch a randomized set of conservatively filtered galaxy candidates."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if pool_size < limit:
        raise ValueError("pool_size must be greater than or equal to limit")

    csv_text = _request_csv(_build_adql(pool_size), timeout=timeout)
    reader = csv.DictReader(io.StringIO(csv_text))
    records = _normalize_rows(reader)

    if len(records) < limit:
        raise SimbadAdapterError(
            f"SIMBAD returned only {len(records)} filtered galaxies; {limit} requested."
        )

    rng = random.Random(seed)
    return rng.sample(records, limit)


def main() -> None:
    galaxies = fetch_random_galaxies(limit=100)
    foundation = _load_foundation_module()
    foundation.save_catalog(galaxies)

    print(f"Saved {len(galaxies)} filtered SIMBAD galaxies to {foundation.CATALOG_PATH}")
    for galaxy in galaxies:
        print(
            f"{galaxy.primary_name}: RA={galaxy.ra_deg:.6f}, "
            f"Dec={galaxy.dec_deg:.6f}, FOV={galaxy.preferred_fov_deg:.4f} deg"
        )


if __name__ == "__main__":
    main()
