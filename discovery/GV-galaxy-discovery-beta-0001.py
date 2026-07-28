"""Galaxy Discovery Engine — Beta 0001.

Step 1 foundation module for Galaxy Viewer.

This module intentionally does not modify or import the Galaxy Viewer, launchers,
mobile app, or service workers. It defines the discovery record format, source
registry, field-of-view defaults, and pipeline states that later modules will use.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Optional


MODULE_NAME = "Galaxy Discovery Engine"
MODULE_VERSION = "beta-0001"
CATALOG_PATH = Path(__file__).with_name("galaxy-catalog-beta.json")


class DiscoveryStatus(str, Enum):
    DISCOVERED = "discovered"
    COORDINATES_VERIFIED = "coordinates_verified"
    PREVIEW_REQUESTED = "preview_requested"
    FOV_ADJUSTED = "fov_adjusted"
    IMAGE_APPROVED = "image_approved"
    PUBLISHED = "published"
    REJECTED = "rejected"
    RETRY_LATER = "retry_later"


@dataclass(slots=True)
class GalaxyCandidate:
    primary_name: str
    ra_deg: float
    dec_deg: float
    source: str
    source_id: str
    major_axis_arcmin: Optional[float] = None
    minor_axis_arcmin: Optional[float] = None
    morphology: Optional[str] = None
    preferred_fov_deg: Optional[float] = None
    preferred_survey: Optional[str] = None
    image_quality_score: Optional[float] = None
    clipping_score: Optional[float] = None
    status: DiscoveryStatus = DiscoveryStatus.DISCOVERED


CATALOG_SOURCES = (
    "NED",
    "SIMBAD",
    "VizieR",
    "HyperLEDA",
    "OpenNGC",
)

SURVEY_FALLBACK_ORDER = (
    "DESI Legacy Surveys",
    "Pan-STARRS",
    "SDSS",
    "DSS2 color",
    "2MASS",
)


def estimate_initial_fov_deg(
    major_axis_arcmin: Optional[float],
    *,
    padding_factor: float = 2.2,
    minimum_fov_deg: float = 0.04,
    unknown_size_fov_deg: float = 0.25,
) -> float:
    """Return a safe first-pass field of view for preview analysis."""
    if major_axis_arcmin is None or major_axis_arcmin <= 0:
        return unknown_size_fov_deg
    return max((major_axis_arcmin / 60.0) * padding_factor, minimum_fov_deg)


def save_catalog(records: list[GalaxyCandidate], path: Path = CATALOG_PATH) -> None:
    """Write discovery records as UTF-8 JSON for the beta pipeline."""
    payload = {
        "module": MODULE_NAME,
        "version": MODULE_VERSION,
        "record_count": len(records),
        "records": [asdict(record) for record in records],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    """Create an empty beta catalog and report the next implementation step."""
    if not CATALOG_PATH.exists():
        save_catalog([])

    print(f"{MODULE_NAME} {MODULE_VERSION}")
    print(f"Catalog: {CATALOG_PATH}")
    print("Step 1 complete: discovery schema and pipeline foundation are ready.")
    print("Next step: implement the first catalog adapter and fetch test candidates.")


if __name__ == "__main__":
    main()
