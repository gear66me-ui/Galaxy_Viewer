#!/usr/bin/env python3
"""Galaxy Viewer orientation/FOV/center registration engine 0001.

Uses only real source images and a real Aladin Lite render. No generated imagery.

Pipeline per record:
  1. download the published source image
  2. render the same sky in Aladin Lite (north-up) with headless Chromium
  3. estimate an affine registration with SIFT + RANSAC
  4. convert the transform to predicted rotation, FOV and center RA/Dec
  5. write JSON predictions for the assisted HTML reviewer

The reviewer remains authoritative: predictions are suggestions until a human presses USE THIS.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import math
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

import cv2
import numpy as np
import requests

ALADIN_JS = "https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js"
DEFAULT_SURVEY = "P/DSS2/color"


def entries(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("entries", "galaxies", "records", "items", "data", "catalog"):
            v = obj.get(key)
            if isinstance(v, list):
                return v
    return []


def num(record: dict[str, Any], *keys: str) -> float | None:
    for k in keys:
        try:
            v = float(record[k])
            if math.isfinite(v):
                return v
        except Exception:
            pass
    return None


def image_url(record: dict[str, Any]) -> str:
    for k in ("selectedImageUrl", "githubImageUrl", "esaPublicationJpeg", "publicationJpeg", "imageUrl", "jpegUrl", "image"):
        v = record.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    jc = record.get("jpegCandidates")
    if isinstance(jc, list):
        for v in jc:
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""


def fov_deg(record: dict[str, Any]) -> float:
    v = record.get("fieldOfView", record.get("fov", record.get("FOV")))
    if isinstance(v, (int, float)) and math.isfinite(float(v)):
        return max(float(v), 1e-6)
    if isinstance(v, list):
        vals = [float(x) for x in v if isinstance(x, (int, float)) and math.isfinite(float(x))]
        return max(vals) if vals else 1.0
    s = str(v or "").lower()
    import re
    vals = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
    if not vals:
        return 1.0
    m = max(vals)
    if "arcsec" in s or "arcsecond" in s or "″" in s:
        m /= 3600.0
    elif "arcmin" in s or "arcminute" in s or "′" in s:
        m /= 60.0
    elif not any(t in s for t in ("degree", " deg", "°")) and m > 20:
        m /= 60.0
    return max(m, 1e-6)


def record_key(catalog: str, record: dict[str, Any], index: int) -> str:
    rid = record.get("archiveId") or record.get("id") or record.get("designation") or record.get("name") or index
    return f"{catalog}:{rid}"


def load_json_source(src: str) -> Any:
    if src.startswith("http://") or src.startswith("https://"):
        r = requests.get(src, timeout=60)
        r.raise_for_status()
        return r.json()
    return json.loads(Path(src).read_text(encoding="utf-8"))


def download_image(url: str, out: Path) -> None:
    r = requests.get(url, timeout=90, headers={"User-Agent": "GalaxyViewerRegistration/0001"})
    r.raise_for_status()
    out.write_bytes(r.content)


def read_cv(path: Path) -> np.ndarray:
    data = np.frombuffer(path.read_bytes(), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"OpenCV could not decode {path}")
    return img


def normalize_image(img: np.ndarray, max_side: int = 900) -> np.ndarray:
    h, w = img.shape[:2]
    scale = min(1.0, max_side / max(h, w))
    if scale < 1:
        img = cv2.resize(img, (max(1, round(w * scale)), max(1, round(h * scale))), interpolation=cv2.INTER_AREA)
    return img


def feature_plane(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    return cv2.GaussianBlur(gray, (0, 0), 0.8)


@dataclass
class MatchResult:
    ok: bool
    method: str
    matrix: list[list[float]] | None = None
    rotation_deg: float | None = None
    scale: float | None = None
    tx_px: float | None = None
    ty_px: float | None = None
    confidence: float = 0.0
    matches: int = 0
    inliers: int = 0
    inlier_ratio: float = 0.0
    median_error_px: float | None = None
    warning: str | None = None


def estimate_registration(aladin_bgr: np.ndarray, source_bgr: np.ndarray) -> MatchResult:
    """Estimate affine mapping Aladin pixels -> source pixels."""
    a = normalize_image(aladin_bgr)
    s = normalize_image(source_bgr)
    ag = feature_plane(a)
    sg = feature_plane(s)

    sift = cv2.SIFT_create(nfeatures=6000, contrastThreshold=0.015, edgeThreshold=15)
    ka, da = sift.detectAndCompute(ag, None)
    ks, ds = sift.detectAndCompute(sg, None)
    if da is None or ds is None or len(ka) < 8 or len(ks) < 8:
        return MatchResult(False, "sift-ransac", warning="insufficient_features")

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    pairs = matcher.knnMatch(da, ds, k=2)
    good = [m for m, n in pairs if m.distance < 0.73 * n.distance]
    if len(good) < 6:
        return MatchResult(False, "sift-ransac", matches=len(good), warning="insufficient_good_matches")

    pa = np.float32([ka[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    ps = np.float32([ks[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv2.estimateAffinePartial2D(pa, ps, method=cv2.RANSAC, ransacReprojThreshold=5.0, maxIters=10000, confidence=0.999, refineIters=50)
    if M is None or mask is None:
        return MatchResult(False, "sift-ransac", matches=len(good), warning="ransac_failed")

    inlier_mask = mask.ravel().astype(bool)
    inliers = int(inlier_mask.sum())
    ratio = inliers / max(len(good), 1)
    a00, _, tx = map(float, M[0])
    a10, _, ty = map(float, M[1])
    scale = math.sqrt(a00 * a00 + a10 * a10)
    rotation = math.degrees(math.atan2(a10, a00))

    pred = cv2.transform(pa[inlier_mask], M)
    err = np.linalg.norm(pred.reshape(-1, 2) - ps[inlier_mask].reshape(-1, 2), axis=1) if inliers else np.array([])
    med_err = float(np.median(err)) if err.size else None

    c_matches = min(1.0, inliers / 30.0)
    c_ratio = min(1.0, ratio / 0.65)
    c_err = math.exp(-((med_err or 20.0) / 8.0))
    confidence = max(0.0, min(1.0, 0.42 * c_matches + 0.38 * c_ratio + 0.20 * c_err))

    warning = None
    if scale < 0.15 or scale > 6.0:
        confidence *= 0.45
        warning = "extreme_scale"
    if inliers < 8:
        confidence *= 0.55
        warning = warning or "few_inliers"

    return MatchResult(True, "sift-ransac", matrix=[[float(x) for x in row] for row in M], rotation_deg=rotation, scale=scale, tx_px=tx, ty_px=ty, confidence=confidence, matches=len(good), inliers=inliers, inlier_ratio=ratio, median_error_px=med_err, warning=warning)


def transform_to_prediction(match: MatchResult, catalog_ra: float, catalog_dec: float, catalog_fov: float, aladin_shape: tuple[int, int], source_shape: tuple[int, int]) -> tuple[float, float, float, float]:
    if not match.ok or match.matrix is None or not match.scale:
        return catalog_ra, catalog_dec, catalog_fov, 0.0
    M = np.array(match.matrix, dtype=np.float64)
    inv = np.linalg.inv(np.vstack([M, [0.0, 0.0, 1.0]]))
    sh, sw = source_shape
    ah, aw = aladin_shape
    al_at_src_center = inv @ np.array([sw / 2.0, sh / 2.0, 1.0])
    dx = float(al_at_src_center[0] - aw / 2.0)
    dy = float(al_at_src_center[1] - ah / 2.0)

    dec = catalog_dec - (dy / ah) * catalog_fov
    cosd = max(0.05, math.cos(math.radians(catalog_dec)))
    ra = (catalog_ra - (dx / aw) * catalog_fov / cosd) % 360.0
    fov = max(1e-6, catalog_fov / match.scale)
    rotation = -float(match.rotation_deg or 0.0)
    while rotation > 180:
        rotation -= 360
    while rotation <= -180:
        rotation += 360
    return ra, dec, fov, rotation


async def render_aladin(page, ra: float, dec: float, fov: float, out: Path, size: int = 640) -> None:
    html = f"""<!doctype html><html><head><meta charset='utf-8'>
<style>html,body,#aladin{{margin:0;width:{size}px;height:{size}px;overflow:hidden;background:#000}}</style>
<script src='{ALADIN_JS}'></script></head><body><div id='aladin'></div><script>
window.__ready=false;window.__err='';(async()=>{{try{{await A.init;window.v=A.aladin('#aladin',{{survey:'{DEFAULT_SURVEY}',target:'0 +0',fov:1,projection:'TAN',cooFrame:'ICRSd',lockNorthUp:false,northPoleOrientation:0,showReticle:false,showCooGrid:false,showZoomControl:false,showLayersControl:false,showFullscreenControl:false,inertia:false}});v.gotoRaDec({ra},{dec});v.setFoV({fov});v.setRotation(0);setTimeout(()=>window.__ready=true,2200);}}catch(e){{window.__err=String(e);}}}})();
</script></body></html>"""
    await page.set_content(html, wait_until="domcontentloaded")
    for _ in range(80):
        if await page.evaluate("window.__ready===true"):
            break
        err = await page.evaluate("window.__err||''")
        if err:
            raise RuntimeError(err)
        await asyncio.sleep(0.1)
    else:
        raise TimeoutError("Aladin render timeout")
    await page.locator("#aladin").screenshot(path=str(out))


async def run(args: argparse.Namespace) -> int:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: pip install playwright && python -m playwright install chromium", file=sys.stderr)
        return 2

    catalogs = []
    for spec in args.catalog:
        if "=" not in spec:
            raise SystemExit("--catalog must be NAME=PATH_OR_URL")
        name, src = spec.split("=", 1)
        catalogs.append((name, src, entries(load_json_source(src))))

    gold: dict[str, dict[str, Any]] = {}
    if args.gold:
        g = load_json_source(args.gold)
        for rec in g.get("corrections", []):
            gold[f"{rec.get('catalog')}:{rec.get('archiveId')}"] = rec

    out_records: list[dict[str, Any]] = []
    work = Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage", "--no-sandbox"])
        page = await browser.new_page(viewport={"width": args.render_size, "height": args.render_size})
        processed = 0
        for catalog_name, catalog_src, recs in catalogs:
            for i, rec in enumerate(recs):
                if args.only_missing_orientation and rec.get("orientation") not in (None, ""):
                    continue
                if args.limit and processed >= args.limit:
                    break
                key = record_key(catalog_name, rec, i)
                ra = num(rec, "ra", "RA", "raDeg", "raDegrees")
                dec = num(rec, "dec", "Dec", "DEC", "decDeg", "decDegrees")
                url = image_url(rec)
                cfov = fov_deg(rec)
                base = {"key": key, "catalog": catalog_name, "archiveId": rec.get("archiveId") or rec.get("id"), "name": rec.get("displayName") or rec.get("name") or rec.get("title") or key, "catalogRaDeg": ra, "catalogDecDeg": dec, "catalogFovDeg": cfov, "sourceImageUrl": url, "catalogSource": catalog_src}
                processed += 1
                print(f"[{processed}] {key}", flush=True)
                if ra is None or dec is None or not url:
                    base.update({"status": "failed", "confidence": 0.0, "warning": "missing_ra_dec_or_image"})
                    out_records.append(base)
                    continue
                safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)[:140]
                src_path = work / f"{safe}.source"
                ali_path = work / f"{safe}.aladin.png"
                try:
                    download_image(url, src_path)
                    await render_aladin(page, ra, dec, cfov, ali_path, args.render_size)
                    source = read_cv(src_path)
                    aladin = read_cv(ali_path)
                    match = estimate_registration(aladin, source)
                    pra, pdec, pfov, prot = transform_to_prediction(match, ra, dec, cfov, aladin.shape[:2], source.shape[:2])
                    base.update({"status": "ok" if match.ok else "low-confidence", "predictedRaDeg": pra, "predictedDecDeg": pdec, "predictedFovDeg": pfov, "predictedRotationDeg": prot, "confidence": match.confidence, "registration": asdict(match)})
                    if key in gold:
                        g = gold[key]
                        grot = float(g.get("aladinRotationDeg", 0.0))
                        gfov = float(g.get("confirmedFovDeg", cfov))
                        d_rot = abs(((prot - grot + 180) % 360) - 180)
                        base["benchmark"] = {"humanRotationDeg": grot, "humanFovDeg": gfov, "rotationAbsErrorDeg": d_rot, "fovRelativeError": abs(pfov - gfov) / max(gfov, 1e-9)}
                except Exception as e:
                    base.update({"status": "failed", "confidence": 0.0, "warning": f"{type(e).__name__}: {e}"})
                out_records.append(base)
                if args.checkpoint_every and processed % args.checkpoint_every == 0:
                    write_output(args.output, out_records, args)
            if args.limit and processed >= args.limit:
                break
        await browser.close()

    write_output(args.output, out_records, args)
    if gold:
        report_benchmark(out_records)
    return 0


def write_output(path: str, records: list[dict[str, Any]], args: argparse.Namespace) -> None:
    obj = {"schema": "gv-registration-predictions-0001", "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "survey": DEFAULT_SURVEY, "renderSize": args.render_size, "predictionCount": len(records), "predictions": records}
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def report_benchmark(records: Iterable[dict[str, Any]]) -> None:
    b = [r["benchmark"] for r in records if "benchmark" in r and r.get("status") != "failed"]
    if not b:
        print("No benchmark overlaps.")
        return
    rot = np.array([x["rotationAbsErrorDeg"] for x in b], dtype=float)
    fov = np.array([x["fovRelativeError"] for x in b], dtype=float)
    print(f"BENCHMARK n={len(b)} rotation median={np.median(rot):.2f}° p90={np.percentile(rot,90):.2f}°; FOV rel median={np.median(fov)*100:.1f}% p90={np.percentile(fov,90)*100:.1f}%")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", action="append", required=True, help="NAME=PATH_OR_URL; repeatable")
    ap.add_argument("--gold", help="optional human corrections JSON for benchmarking")
    ap.add_argument("--output", default="gv-registration-predictions-0001.json")
    ap.add_argument("--workdir", default=".gv-registration-cache")
    ap.add_argument("--render-size", type=int, default=640)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--checkpoint-every", type=int, default=25)
    ap.add_argument("--only-missing-orientation", action="store_true")
    return ap.parse_args()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run(parse_args())))
