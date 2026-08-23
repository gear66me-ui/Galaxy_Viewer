#!/usr/bin/env python3
"""Galaxy Viewer Hubble V automated alignment auditor.

Reads the immutable Hubble catalog, measures the dominant subject in each HD
image, renders the same target in Aladin Lite through Playwright, compares
centering/scale/orientation, attempts bounded corrections, and emits machine-
readable JSON plus an HTML exception review. The source catalog is never
modified by this program.

Runtime dependencies:
    python -m pip install numpy pillow playwright
    playwright install chromium
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import math
import os
import statistics
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image


DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "databases" / "gv-hubble-galaxies-full-0022.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "output"
ALADIN_JS = "https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"
ALADIN_CSS = "https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.css"
SURVEY = "P/DSS2/color"
TARGET_OCCUPANCY = 0.80
MAX_ATTEMPTS = 5

PASS_ERROR = 0.05
ACCEPTABLE_ERROR = 0.10
PASS_ROTATION_DEG = 5.0
ACCEPTABLE_ROTATION_DEG = 10.0


@dataclass
class ShapeMeasurement:
    centroid_x: float
    centroid_y: float
    width_fraction: float
    height_fraction: float
    occupancy: float
    angle_deg: float
    confidence: float
    component_count: int
    dominant_fraction: float
    complex_field: bool


@dataclass
class AuditResult:
    index: int
    object_id: str
    name: str
    source_image_url: str
    source_url: str
    current_ra: float
    current_dec: float
    current_fov: float
    current_orientation: float
    classification: str
    position_error: float | None
    scale_error: float | None
    rotation_error_deg: float | None
    object_confidence: float
    proposed_ra: float | None
    proposed_dec: float | None
    proposed_fov: float | None
    proposed_orientation: float | None
    attempts: int
    reason: str
    hubble_preview: str | None
    aladin_preview: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Hubble image alignment against Aladin Lite")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--start", type=int, default=0, help="zero-based first catalog index")
    parser.add_argument("--limit", type=int, default=None, help="maximum number of records")
    parser.add_argument("--max-attempts", type=int, default=MAX_ATTEMPTS)
    parser.add_argument("--headful", action="store_true", help="show Chromium while rendering")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    return parser.parse_args()


def first_value(record: dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        value = record.get(key)
        if value is not None and value != "":
            return value
    return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def record_identity(record: dict[str, Any], index: int) -> tuple[str, str]:
    object_id = str(first_value(record, ("archiveId", "assetName", "designation", "name"), f"record-{index}"))
    name = str(first_value(record, ("displayName", "name", "title", "designation"), object_id))
    return object_id, name


def load_catalog(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = first_value(payload, ("galaxies", "records", "items", "data"), [])
    else:
        raise ValueError("Catalog JSON must be a list or object containing a record list")
    if not isinstance(records, list):
        raise ValueError("Catalog record container is not a list")
    return [item for item in records if isinstance(item, dict)]


def download_image(url: str, timeout: int = 45) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "GalaxyViewer-Hubble-Audit/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def decode_rgb(data: bytes, max_side: int = 900) -> np.ndarray:
    image = Image.open(io.BytesIO(data)).convert("RGB")
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return np.asarray(image, dtype=np.uint8)


def _connected_components(mask: np.ndarray, min_pixels: int) -> list[np.ndarray]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    components: list[np.ndarray] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            stack = [(y, x)]
            visited[y, x] = True
            coords: list[tuple[int, int]] = []
            while stack:
                cy, cx = stack.pop()
                coords.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
            if len(coords) >= min_pixels:
                components.append(np.asarray(coords, dtype=np.int32))
    return components


def measure_subject(rgb: np.ndarray) -> ShapeMeasurement:
    """Estimate the dominant luminous object's footprint and principal axis.

    The threshold is derived from image luminance rather than fixed black-level
    assumptions. Tiny disconnected components are discarded so stars/noise do
    not dominate the subject estimate.
    """
    height, width, _ = rgb.shape
    lum = rgb.astype(np.float32).mean(axis=2)
    p50 = float(np.percentile(lum, 50))
    p90 = float(np.percentile(lum, 90))
    p99 = float(np.percentile(lum, 99))
    threshold = max(p50 + (p90 - p50) * 0.45, p50 + 4.0)
    if p99 - p50 < 8.0:
        threshold = p50 + max(2.0, (p99 - p50) * 0.35)
    mask = lum >= threshold

    min_pixels = max(12, int(height * width * 0.00008))
    components = _connected_components(mask, min_pixels)
    if not components:
        raise ValueError("No significant luminous component detected")

    sizes = np.asarray([len(c) for c in components], dtype=np.float64)
    order = np.argsort(sizes)[::-1]
    components = [components[int(i)] for i in order]
    sizes = sizes[order]
    dominant = components[0]
    total_kept = float(sizes.sum())
    dominant_fraction = float(sizes[0] / total_kept) if total_kept else 0.0

    ys = dominant[:, 0].astype(np.float64)
    xs = dominant[:, 1].astype(np.float64)
    cx = float(xs.mean())
    cy = float(ys.mean())

    x0, x1 = float(xs.min()), float(xs.max())
    y0, y1 = float(ys.min()), float(ys.max())
    width_fraction = (x1 - x0 + 1.0) / width
    height_fraction = (y1 - y0 + 1.0) / height
    occupancy = max(width_fraction, height_fraction)

    centered = np.column_stack((xs - cx, ys - cy))
    covariance = np.cov(centered, rowvar=False) if len(dominant) > 2 else np.eye(2)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    major = eigenvectors[:, int(np.argmax(eigenvalues))]
    angle = math.degrees(math.atan2(float(major[1]), float(major[0]))) % 180.0

    significant_count = int(np.sum(sizes >= max(min_pixels, sizes[0] * 0.08)))
    edge_penalty = min(cx / width, 1 - cx / width, cy / height, 1 - cy / height) * 2.0
    contrast = min(1.0, max(0.0, (p99 - p50) / 80.0))
    confidence = max(0.0, min(1.0, 0.55 * dominant_fraction + 0.25 * contrast + 0.20 * edge_penalty))
    complex_field = significant_count >= 8 or (significant_count >= 4 and dominant_fraction < 0.45)

    return ShapeMeasurement(
        centroid_x=cx / width,
        centroid_y=cy / height,
        width_fraction=width_fraction,
        height_fraction=height_fraction,
        occupancy=occupancy,
        angle_deg=angle,
        confidence=confidence,
        component_count=significant_count,
        dominant_fraction=dominant_fraction,
        complex_field=complex_field,
    )


def angular_difference(a: float, b: float) -> float:
    delta = abs((a - b) % 180.0)
    return min(delta, 180.0 - delta)


def position_error(a: ShapeMeasurement, b: ShapeMeasurement) -> float:
    return math.hypot(a.centroid_x - b.centroid_x, a.centroid_y - b.centroid_y)


def scale_error(a: ShapeMeasurement, b: ShapeMeasurement) -> float:
    denominator = max(a.occupancy, 1e-6)
    return abs(b.occupancy - a.occupancy) / denominator


def fit_fov(current_fov: float, reference: ShapeMeasurement, rendered: ShapeMeasurement) -> float:
    if rendered.occupancy <= 1e-6:
        return current_fov
    desired = min(TARGET_OCCUPANCY, max(0.20, reference.occupancy))
    return max(0.00001, current_fov * rendered.occupancy / desired)


def offset_radec(ra: float, dec: float, fov: float, rendered: ShapeMeasurement) -> tuple[float, float]:
    dx = rendered.centroid_x - 0.5
    dy = rendered.centroid_y - 0.5
    cos_dec = max(0.05, math.cos(math.radians(dec)))
    new_ra = (ra + dx * fov / cos_dec) % 360.0
    new_dec = max(-90.0, min(90.0, dec - dy * fov))
    return new_ra, new_dec


def make_preview(data: bytes, max_width: int = 560) -> str:
    image = Image.open(io.BytesIO(data)).convert("RGB")
    image.thumbnail((max_width, max_width), Image.Resampling.LANCZOS)
    out = io.BytesIO()
    image.save(out, format="JPEG", quality=82, optimize=True)
    encoded = base64.b64encode(out.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


class AladinRenderer:
    def __init__(self, headless: bool, timeout_ms: int):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError("Playwright is required: python -m pip install playwright && playwright install chromium") from exc
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=headless)
        self._page = self._browser.new_page(viewport={"width": 900, "height": 900}, device_scale_factor=1)
        self._page.set_default_timeout(timeout_ms)
        html = f"""<!doctype html><html><head>
<link rel='stylesheet' href='{ALADIN_CSS}'>
<script src='{ALADIN_JS}' charset='utf-8'></script>
<style>html,body,#aladin-lite-div{{margin:0;width:900px;height:900px;overflow:hidden;background:#000}}</style>
</head><body><div id='aladin-lite-div'></div></body></html>"""
        self._page.set_content(html, wait_until="domcontentloaded")
        self._page.wait_for_function("typeof A !== 'undefined' && typeof A.aladin === 'function'")
        self._page.evaluate(
            """() => {
                window.__gvAladin = A.aladin('#aladin-lite-div', {
                    survey: 'P/DSS2/color',
                    fov: 1.5,
                    target: '0 0',
                    showReticle: false,
                    showZoomControl: false,
                    showFullscreenControl: false,
                    showLayersControl: false,
                    showGotoControl: false,
                    showSimbadPointerControl: false
                });
            }"""
        )

    def close(self) -> None:
        self._browser.close()
        self._playwright.stop()

    def render(self, ra: float, dec: float, fov: float, orientation: float) -> bytes:
        self._page.evaluate(
            """({ra, dec, fov, orientation}) => {
                const aladin = window.__gvAladin;
                aladin.gotoRaDec(ra, dec);
                aladin.setFoV(fov);
                if (typeof aladin.setViewCenter2NorthPoleAngle === 'function') {
                    aladin.setViewCenter2NorthPoleAngle(orientation);
                } else if (typeof aladin.setRotation === 'function') {
                    aladin.setRotation(orientation);
                }
            }""",
            {"ra": ra, "dec": dec, "fov": fov, "orientation": orientation},
        )
        self._page.wait_for_timeout(1800)
        return self._page.locator("#aladin-lite-div").screenshot(type="png")


def classify(reference: ShapeMeasurement, rendered: ShapeMeasurement) -> tuple[str, float, float, float, str]:
    if reference.complex_field or rendered.complex_field:
        return "IGNORE COMPLEX FIELD", position_error(reference, rendered), scale_error(reference, rendered), angular_difference(reference.angle_deg, rendered.angle_deg), "Multiple significant objects make a forced single-galaxy alignment unreliable"

    pos = position_error(reference, rendered)
    scale = scale_error(reference, rendered)
    rot = angular_difference(reference.angle_deg, rendered.angle_deg)
    confidence = min(reference.confidence, rendered.confidence)

    if confidence < 0.35:
        return "MANUAL REVIEW", pos, scale, rot, "Dominant-object confidence is too low for automatic correction"
    if pos <= PASS_ERROR and scale <= PASS_ERROR and rot <= PASS_ROTATION_DEG:
        return "PASS", pos, scale, rot, "All measurements are within strict pass tolerances"
    if pos <= ACCEPTABLE_ERROR and scale <= ACCEPTABLE_ERROR and rot <= ACCEPTABLE_ROTATION_DEG:
        return "PASS", pos, scale, rot, "Measurements are within acceptable tolerances"
    if pos > ACCEPTABLE_ERROR:
        return "AUTO-FIX COORDINATES", pos, scale, rot, "Centroid displacement exceeds 10%"
    if scale > ACCEPTABLE_ERROR:
        return "AUTO-FIX FOV", pos, scale, rot, "Scale/FOV error exceeds 10%"
    if rot > ACCEPTABLE_ROTATION_DEG:
        return "AUTO-FIX ORIENTATION", pos, scale, rot, "Rotation error exceeds 10 degrees"
    return "MANUAL REVIEW", pos, scale, rot, "Measurements are inconclusive"


def audit_record(index: int, record: dict[str, Any], renderer: AladinRenderer, max_attempts: int) -> AuditResult:
    object_id, name = record_identity(record, index)
    image_url = str(first_value(record, ("selectedImageUrl", "githubImageUrl", "imageUrl"), ""))
    source_url = str(first_value(record, ("sourceUrl",), ""))
    ra = as_float(first_value(record, ("ra", "RA")))
    dec = as_float(first_value(record, ("dec", "DEC")))
    fov = as_float(first_value(record, ("fieldOfView", "fov")), 1.5)
    orientation = as_float(first_value(record, ("orientation", "rotation")), 0.0)

    if not image_url:
        return AuditResult(index, object_id, name, image_url, source_url, ra, dec, fov, orientation, "MANUAL REVIEW", None, None, None, 0.0, None, None, None, None, 0, "No selected HD image URL", None, None)

    hubble_bytes = download_image(image_url)
    hubble_measure = measure_subject(decode_rgb(hubble_bytes))
    hubble_preview = make_preview(hubble_bytes)

    if hubble_measure.complex_field:
        return AuditResult(index, object_id, name, image_url, source_url, ra, dec, fov, orientation, "IGNORE COMPLEX FIELD", None, None, None, hubble_measure.confidence, None, None, None, None, 0, "Hubble image contains a complex multi-object field", hubble_preview, None)

    current_ra, current_dec, current_fov, current_orientation = ra, dec, fov, orientation
    best: tuple[float, str, ShapeMeasurement, bytes, float, float, float, str, float, float, float, float] | None = None

    for attempt in range(1, max_attempts + 1):
        aladin_bytes = renderer.render(current_ra, current_dec, current_fov, current_orientation)
        rendered_measure = measure_subject(decode_rgb(aladin_bytes))
        classification, pos, scale, rot, reason = classify(hubble_measure, rendered_measure)
        score = pos + scale + rot / 90.0 + (1.0 - min(hubble_measure.confidence, rendered_measure.confidence)) * 0.25
        candidate = (score, classification, rendered_measure, aladin_bytes, pos, scale, rot, reason, current_ra, current_dec, current_fov, current_orientation)
        if best is None or score < best[0]:
            best = candidate
        if classification in ("PASS", "IGNORE COMPLEX FIELD", "MANUAL REVIEW"):
            break

        if classification == "AUTO-FIX COORDINATES":
            current_ra, current_dec = offset_radec(current_ra, current_dec, current_fov, rendered_measure)
        elif classification == "AUTO-FIX FOV":
            current_fov = fit_fov(current_fov, hubble_measure, rendered_measure)
        elif classification == "AUTO-FIX ORIENTATION":
            signed = (hubble_measure.angle_deg - rendered_measure.angle_deg + 90.0) % 180.0 - 90.0
            current_orientation = (current_orientation + signed) % 360.0

    assert best is not None
    _, classification, rendered_measure, aladin_bytes, pos, scale, rot, reason, proposed_ra, proposed_dec, proposed_fov, proposed_orientation = best
    confidence = min(hubble_measure.confidence, rendered_measure.confidence)

    if classification.startswith("AUTO-FIX"):
        reason += "; bounded correction attempts did not reach tolerance"
        classification = "MANUAL REVIEW"

    changed = any((
        abs(proposed_ra - ra) > 1e-10,
        abs(proposed_dec - dec) > 1e-10,
        abs(proposed_fov - fov) > 1e-10,
        abs(((proposed_orientation - orientation + 180.0) % 360.0) - 180.0) > 1e-10,
    ))

    if not changed and classification == "PASS":
        proposed_ra = proposed_dec = proposed_fov = proposed_orientation = None

    return AuditResult(
        index=index,
        object_id=object_id,
        name=name,
        source_image_url=image_url,
        source_url=source_url,
        current_ra=ra,
        current_dec=dec,
        current_fov=fov,
        current_orientation=orientation,
        classification=classification,
        position_error=pos,
        scale_error=scale,
        rotation_error_deg=rot,
        object_confidence=confidence,
        proposed_ra=proposed_ra,
        proposed_dec=proposed_dec,
        proposed_fov=proposed_fov,
        proposed_orientation=proposed_orientation,
        attempts=attempt,
        reason=reason,
        hubble_preview=hubble_preview,
        aladin_preview=make_preview(aladin_bytes),
    )


def write_json(results: list[AuditResult], output: Path, catalog: Path) -> Path:
    path = output / "hubble-audit-results.json"
    payload = {
        "catalog": str(catalog),
        "catalogModified": False,
        "targetOccupancy": TARGET_OCCUPANCY,
        "tolerances": {
            "strictPercent": 5,
            "acceptablePercent": 10,
            "strictRotationDegrees": PASS_ROTATION_DEG,
            "acceptableRotationDegrees": ACCEPTABLE_ROTATION_DEG,
        },
        "counts": {label: sum(r.classification == label for r in results) for label in (
            "PASS", "AUTO-FIX FOV", "AUTO-FIX ORIENTATION", "AUTO-FIX COORDINATES", "MANUAL REVIEW", "IGNORE COMPLEX FIELD"
        )},
        "results": [asdict(result) for result in results],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def esc(value: Any) -> str:
    import html
    return html.escape(str(value), quote=True)


def metric(value: float | None, percent: bool = False) -> str:
    if value is None:
        return "—"
    return f"{value * 100:.1f}%" if percent else f"{value:.2f}°"


def write_html(results: list[AuditResult], output: Path) -> Path:
    path = output / "hubble-audit-review.html"
    exceptions = [r for r in results if r.classification != "PASS"]
    cards: list[str] = []
    for r in exceptions:
        hubble_img = f"<img src='{r.hubble_preview}' alt='Hubble'>" if r.hubble_preview else "<div class='missing'>No Hubble preview</div>"
        aladin_img = f"<img src='{r.aladin_preview}' alt='Aladin'>" if r.aladin_preview else "<div class='missing'>No Aladin preview</div>"
        proposed = (
            f"RA {r.proposed_ra:.8f} · Dec {r.proposed_dec:.8f} · FOV {r.proposed_fov:.6f} · Orientation {r.proposed_orientation:.2f}°"
            if None not in (r.proposed_ra, r.proposed_dec, r.proposed_fov, r.proposed_orientation)
            else "No automatic proposal"
        )
        cards.append(f"""
<section class='card' data-index='{r.index}'>
  <h2>{esc(r.name)} <small>#{r.index}</small></h2>
  <div class='status'>{esc(r.classification)}</div>
  <div class='pair'><figure>{hubble_img}<figcaption>HUBBLE IMAGE</figcaption></figure><figure>{aladin_img}<figcaption>ALADIN RESULT</figcaption></figure></div>
  <div class='metrics'>Position {metric(r.position_error, True)} · Scale/FOV {metric(r.scale_error, True)} · Rotation {metric(r.rotation_error_deg)} · Confidence {r.object_confidence * 100:.1f}% · Attempts {r.attempts}</div>
  <p>{esc(r.reason)}</p><p><strong>PROPOSED:</strong> {esc(proposed)}</p>
  <div class='actions'><button onclick='mark(this,"ACCEPT FIX")'>ACCEPT FIX</button><button onclick='mark(this,"KEEP CURRENT")'>KEEP CURRENT</button><button onclick='mark(this,"MANUAL REVIEW")'>MANUAL REVIEW</button></div>
</section>""")

    html = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Hubble V Audit Review</title><style>
body{{font-family:system-ui,sans-serif;background:#101218;color:#f3f5f7;margin:0;padding:20px}}h1{{margin-top:0}}.summary{{padding:12px 16px;background:#1a1f2b;border-radius:10px;margin-bottom:18px}}.card{{background:#171b24;border:1px solid #333b4d;border-radius:12px;padding:16px;margin:18px 0}}h2{{margin:0 0 8px}}small{{opacity:.6}}.status{{font-weight:800;margin-bottom:12px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}figure{{margin:0}}img{{width:100%;max-height:560px;object-fit:contain;background:#000}}figcaption{{text-align:center;font-weight:700;padding:6px}}.metrics{{font-weight:700;padding:8px 0}}button{{padding:10px 14px;margin:4px;border-radius:8px;border:1px solid #667;background:#252b38;color:white}}button.selected{{outline:3px solid white}}@media(max-width:700px){{.pair{{grid-template-columns:1fr}}}}
</style></head><body><h1>Hubble V — Alignment Exceptions</h1><div class='summary'>{len(results)} processed · {len(exceptions)} shown · PASS records hidden</div>{''.join(cards) if cards else '<p>No exceptions.</p>'}
<script>function mark(btn,label){{const card=btn.closest('.card');card.querySelectorAll('button').forEach(b=>b.classList.remove('selected'));btn.classList.add('selected');card.dataset.decision=label;}}</script></body></html>"""
    path.write_text(html, encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    records = load_catalog(args.catalog)
    selected = records[args.start:]
    if args.limit is not None:
        selected = selected[: max(0, args.limit)]
    args.output.mkdir(parents=True, exist_ok=True)

    results: list[AuditResult] = []
    renderer = AladinRenderer(headless=not args.headful, timeout_ms=args.timeout_ms)
    try:
        for offset, record in enumerate(selected):
            index = args.start + offset
            object_id, name = record_identity(record, index)
            print(f"[{index + 1}/{len(records)}] {name}", flush=True)
            try:
                result = audit_record(index, record, renderer, args.max_attempts)
            except Exception as exc:
                ra = as_float(first_value(record, ("ra", "RA")))
                dec = as_float(first_value(record, ("dec", "DEC")))
                fov = as_float(first_value(record, ("fieldOfView", "fov")), 1.5)
                orientation = as_float(first_value(record, ("orientation", "rotation")), 0.0)
                image_url = str(first_value(record, ("selectedImageUrl", "githubImageUrl", "imageUrl"), ""))
                result = AuditResult(index, object_id, name, image_url, str(record.get("sourceUrl", "")), ra, dec, fov, orientation, "MANUAL REVIEW", None, None, None, 0.0, None, None, None, None, 0, f"Audit error: {type(exc).__name__}: {exc}", None, None)
            results.append(result)
    finally:
        renderer.close()

    json_path = write_json(results, args.output, args.catalog)
    html_path = write_html(results, args.output)
    print(f"JSON: {json_path}")
    print(f"HTML: {html_path}")
    print("Source catalog modified: NO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
