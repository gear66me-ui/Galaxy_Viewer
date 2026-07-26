#!/usr/bin/env python3
"""Measure the exact DSS2 Color HiPS footprint needed for M31 development.

This script does not commit survey data. It downloads a bounded M31 tile set on a
GitHub Actions runner, records exact file sizes, failures, and mirror usage, and
writes JSON/CSV/Markdown reports suitable for review before cloning anything.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import astropy.units as u
import requests
from astropy.coordinates import SkyCoord
from astropy_healpix import HEALPix

M31_RA_DEG = 10.6847083
M31_DEC_DEG = 41.26875
MAX_ORDER = 9
RADII_DEG = (1.0, 1.5, 2.0)
MIRRORS = (
    "https://alasky.cds.unistra.fr/DSS/DSSColor",
    "https://alaskybis.cds.unistra.fr/DSS/DSSColor",
    "https://irsa.ipac.caltech.edu/data/hips/CDS/DSS2/color",
    "https://stpubdata.s3.us-east-1.amazonaws.com/mast/skybackgrounds/DSSColor",
)


@dataclass(frozen=True)
class Tile:
    order: int
    npix: int

    @property
    def relative_path(self) -> str:
        directory = (self.npix // 10000) * 10000
        return f"Norder{self.order}/Dir{directory}/Npix{self.npix}.jpg"


@dataclass
class DownloadResult:
    order: int
    npix: int
    relative_path: str
    ok: bool
    size_bytes: int
    mirror: str
    status_code: int | None
    elapsed_seconds: float
    error: str


def tile_set(radius_deg: float) -> set[Tile]:
    """Return a conservative, fully padded cone footprint for all HiPS orders."""
    center = SkyCoord(M31_RA_DEG * u.deg, M31_DEC_DEG * u.deg, frame="icrs")
    tiles: set[Tile] = set()
    for order in range(MAX_ORDER + 1):
        hp = HEALPix(nside=2**order, order="nested", frame="icrs")
        # Padding by twice the nominal HEALPix pixel resolution avoids edge holes.
        padded = radius_deg * u.deg + 2.0 * hp.pixel_resolution
        indices = hp.cone_search_skycoord(center, padded)
        tiles.update(Tile(order, int(index)) for index in indices)
    return tiles


def download_one(tile: Tile, output_root: Path, session: requests.Session) -> DownloadResult:
    target = output_root / tile.relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    for mirror in MIRRORS:
        url = f"{mirror}/{tile.relative_path}"
        started = time.monotonic()
        try:
            with session.get(url, timeout=(15, 90), stream=True) as response:
                elapsed = time.monotonic() - started
                if response.status_code != 200:
                    errors.append(f"{mirror}: HTTP {response.status_code}")
                    continue
                size = 0
                with target.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=256 * 1024):
                        if chunk:
                            handle.write(chunk)
                            size += len(chunk)
                if size == 0:
                    target.unlink(missing_ok=True)
                    errors.append(f"{mirror}: zero-byte response")
                    continue
                return DownloadResult(
                    order=tile.order,
                    npix=tile.npix,
                    relative_path=tile.relative_path,
                    ok=True,
                    size_bytes=size,
                    mirror=mirror,
                    status_code=response.status_code,
                    elapsed_seconds=elapsed,
                    error="",
                )
        except requests.RequestException as exc:
            errors.append(f"{mirror}: {type(exc).__name__}: {exc}")

    target.unlink(missing_ok=True)
    return DownloadResult(
        order=tile.order,
        npix=tile.npix,
        relative_path=tile.relative_path,
        ok=False,
        size_bytes=0,
        mirror="",
        status_code=None,
        elapsed_seconds=0.0,
        error=" | ".join(errors),
    )


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.2f} {unit}"
        amount /= 1024
    raise AssertionError


def summarize(results: list[DownloadResult], sets_by_radius: dict[float, set[Tile]]) -> dict:
    by_key = {(r.order, r.npix): r for r in results}
    successful = [r for r in results if r.ok]
    failed = [r for r in results if not r.ok]

    radius_summaries = []
    for radius, tiles in sets_by_radius.items():
        subset = [by_key[(t.order, t.npix)] for t in tiles]
        ok_subset = [r for r in subset if r.ok]
        radius_summaries.append(
            {
                "radius_deg": radius,
                "diameter_deg": radius * 2,
                "file_count": len(tiles),
                "successful_files": len(ok_subset),
                "failed_files": len(subset) - len(ok_subset),
                "total_bytes": sum(r.size_bytes for r in ok_subset),
                "largest_file_bytes": max((r.size_bytes for r in ok_subset), default=0),
            }
        )

    order_summaries = []
    for order in range(MAX_ORDER + 1):
        group = [r for r in successful if r.order == order]
        order_summaries.append(
            {
                "order": order,
                "file_count": len(group),
                "total_bytes": sum(r.size_bytes for r in group),
                "largest_file_bytes": max((r.size_bytes for r in group), default=0),
                "median_file_bytes": int(statistics.median([r.size_bytes for r in group])) if group else 0,
            }
        )

    mirrors: dict[str, dict[str, int]] = {}
    for result in successful:
        entry = mirrors.setdefault(result.mirror, {"files": 0, "bytes": 0})
        entry["files"] += 1
        entry["bytes"] += result.size_bytes

    return {
        "center": {"name": "M31", "ra_deg": M31_RA_DEG, "dec_deg": M31_DEC_DEG},
        "max_hips_order": MAX_ORDER,
        "survey": "CDS/P/DSS2/color",
        "mirrors_tested": list(MIRRORS),
        "union_file_count": len(results),
        "successful_files": len(successful),
        "failed_files": len(failed),
        "union_total_bytes": sum(r.size_bytes for r in successful),
        "largest_file_bytes": max((r.size_bytes for r in successful), default=0),
        "any_file_over_50_mib": any(r.size_bytes > 50 * 1024 * 1024 for r in successful),
        "any_file_over_100_mib": any(r.size_bytes > 100 * 1024 * 1024 for r in successful),
        "radius_summaries": radius_summaries,
        "order_summaries": order_summaries,
        "mirror_usage": mirrors,
        "failures": [asdict(r) for r in failed],
    }


def write_reports(report_dir: Path, summary: dict, results: list[DownloadResult]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (report_dir / "files.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(result) for result in results)

    lines = [
        "# M31 DSS2 Color HiPS measurement",
        "",
        f"- Survey: `{summary['survey']}`",
        f"- Center: M31 ({M31_RA_DEG:.7f}°, {M31_DEC_DEG:.7f}°)",
        f"- Orders measured: 0–{MAX_ORDER}",
        f"- Downloaded union: **{summary['successful_files']} / {summary['union_file_count']} files**",
        f"- Union size: **{human_bytes(summary['union_total_bytes'])}**",
        f"- Largest individual tile: **{human_bytes(summary['largest_file_bytes'])}**",
        f"- Any tile over 50 MiB: **{summary['any_file_over_50_mib']}**",
        f"- Any tile over 100 MiB: **{summary['any_file_over_100_mib']}**",
        f"- Failed files: **{summary['failed_files']}**",
        "",
        "## Development footprint options",
        "",
        "| Radius | Diameter | Files | Size | Largest file | Failures |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for item in summary["radius_summaries"]:
        lines.append(
            f"| {item['radius_deg']:.1f}° | {item['diameter_deg']:.1f}° | "
            f"{item['file_count']} | {human_bytes(item['total_bytes'])} | "
            f"{human_bytes(item['largest_file_bytes'])} | {item['failed_files']} |"
        )

    lines.extend(
        [
            "",
            "## Per-order totals for the 2°-radius union",
            "",
            "| Order | Files | Size | Median tile | Largest tile |",
            "|---:|---:|---:|---:|---:|",
        ]
    )
    for item in summary["order_summaries"]:
        lines.append(
            f"| {item['order']} | {item['file_count']} | {human_bytes(item['total_bytes'])} | "
            f"{human_bytes(item['median_file_bytes'])} | {human_bytes(item['largest_file_bytes'])} |"
        )

    lines.extend(["", "## Mirror usage", ""])
    for mirror, stats in summary["mirror_usage"].items():
        lines.append(f"- `{mirror}`: {stats['files']} files, {human_bytes(stats['bytes'])}")

    if summary["failures"]:
        lines.extend(["", "## Failures", ""])
        for failure in summary["failures"][:50]:
            lines.append(f"- `{failure['relative_path']}` — {failure['error']}")

    (report_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="hips-measurement")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()

    output = Path(args.output)
    tiles_dir = output / "tiles"
    reports_dir = output / "reports"

    sets_by_radius = {radius: tile_set(radius) for radius in RADII_DEG}
    union = sorted(set().union(*sets_by_radius.values()), key=lambda t: (t.order, t.npix))
    print(f"Planned union: {len(union)} tiles", flush=True)
    for radius, tiles in sets_by_radius.items():
        print(f"  radius {radius:.1f}°: {len(tiles)} tiles", flush=True)

    session = requests.Session()
    session.headers.update({"User-Agent": "Galaxy-Viewer-M31-HiPS-Measurement/1.0"})

    results: list[DownloadResult] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download_one, tile, tiles_dir, session): tile for tile in union}
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            state = "OK" if result.ok else "FAIL"
            print(
                f"[{index}/{len(union)}] {state} {result.relative_path} "
                f"{human_bytes(result.size_bytes)}",
                flush=True,
            )

    results.sort(key=lambda r: (r.order, r.npix))
    summary = summarize(results, sets_by_radius)
    write_reports(reports_dir, summary, results)
    print((reports_dir / "summary.md").read_text(encoding="utf-8"), flush=True)

    # Measurement is considered unsuccessful only if any required tile failed.
    return 1 if summary["failed_files"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
