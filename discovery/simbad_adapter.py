"""SIMBAD adapter for Galaxy Discovery Engine — Beta 0001.

Uses the public SIMBAD TAP sync endpoint and Python's standard library only.
It retrieves a candidate pool of galaxies with coordinates, randomizes the
results locally, and normalizes them into GalaxyCandidate records from
GV-galaxy-discovery-beta-0001.py.

The beta workflow runs this adapter with a 10-galaxy default.
"""

from __future__ import annotations

import csv
import importlib.util
import io
import random
import sys
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SIMBAD_TAP_SYNC_URL = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
FOUNDATION_PATH = Path(__file__).with_name("GV-galaxy-discovery-beta-0001.py")
DEFAULT_POOL_SIZE = 500
DEFAULT_TIMEOUT_SECONDS = 45


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


def _build_adql(pool_size: int) -> str:
    if pool_size < 1:
        raise ValueError("pool_size must be at least 1")

    return f"""
SELECT TOP {pool_size}
    main_id,
    ra,
    dec,
    otype
FROM basic
WHERE ra IS NOT NULL
  AND dec IS NOT NULL
  AND otype IN ('G','LSB','bCG','SBG','H2G','EmG','AGN','SyG','Sy1','Sy2','rG','LIN')
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
            "User-Agent": "Galaxy-Viewer-Discovery-Beta/0001",
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
    estimate_initial_fov_deg = foundation.estimate_initial_fov_deg

    records = []
    seen = set()

    for row in rows:
        name = (row.get("main_id") or "").strip()
        ra = _optional_float(row.get("ra"))
        dec = _optional_float(row.get("dec"))
        if not name or ra is None or dec is None:
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
                morphology=None,
                preferred_fov_deg=estimate_initial_fov_deg(None),
                preferred_survey=None,
            )
        )

    return records


def fetch_random_galaxies(
    limit: int = 10,
    *,
    pool_size: int = DEFAULT_POOL_SIZE,
    seed: int | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
):
    """Fetch and return a randomized list of normalized SIMBAD galaxies."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if pool_size < limit:
        raise ValueError("pool_size must be greater than or equal to limit")

    csv_text = _request_csv(_build_adql(pool_size), timeout=timeout)
    reader = csv.DictReader(io.StringIO(csv_text))
    records = _normalize_rows(reader)

    if len(records) < limit:
        raise SimbadAdapterError(
            f"SIMBAD returned only {len(records)} usable galaxies; {limit} requested."
        )

    rng = random.Random(seed)
    return rng.sample(records, limit)


def main() -> None:
    galaxies = fetch_random_galaxies(limit=10)
    foundation = _load_foundation_module()
    foundation.save_catalog(galaxies)

    print(f"Saved {len(galaxies)} SIMBAD candidates to {foundation.CATALOG_PATH}")
    for galaxy in galaxies:
        print(
            f"{galaxy.primary_name}: RA={galaxy.ra_deg:.6f}, "
            f"Dec={galaxy.dec_deg:.6f}, FOV={galaxy.preferred_fov_deg:.4f} deg"
        )


if __name__ == "__main__":
    main()
