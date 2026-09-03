#!/usr/bin/env python3
import argparse, json, math, re
from pathlib import Path
from urllib.parse import urlencode

import requests

UA = "Galaxy-Viewer-Astrometry-Pair-Acquisition/0001"


def records_of(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("records", "galaxies", "items", "data", "results"):
            if isinstance(data.get(k), list):
                return data[k]
        for v in data.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
    raise ValueError("No record array found in catalog")


def nested(rec, path):
    cur = rec
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def first(rec, paths):
    for p in paths:
        v = nested(rec, p)
        if v is not None and v != "":
            return v
    return None


def as_float(v):
    try:
        x = float(v)
        return x if math.isfinite(x) else None
    except Exception:
        return None


def parse_fov(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        x = float(v)
        return x if x > 0 else None
    nums = [float(x) for x in re.findall(r"[-+]?\d+(?:\.\d+)?", str(v))]
    nums = [x for x in nums if x > 0]
    if not nums:
        return None
    return max(nums[:2]) if len(nums) >= 2 else nums[0]


def image_url(rec):
    preferred = first(rec, [
        "selectedImageUrl", "selected_image_url", "selectedImage.url",
        "imageUrl", "image_url", "hdUrl", "hd_url", "url"
    ])
    if isinstance(preferred, str) and preferred.startswith(("http://", "https://")):
        return preferred
    found = []
    def walk(obj, key=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, str(k))
        elif isinstance(obj, list):
            for v in obj:
                walk(v, key)
        elif isinstance(obj, str) and obj.startswith(("http://", "https://")):
            low = obj.lower().split("?")[0]
            if low.endswith((".jpg", ".jpeg", ".png", ".webp")):
                score = 0
                lk = key.lower()
                if "selected" in lk: score += 20
                if "large" in low or "publication" in low: score += 10
                if "image" in lk or "url" in lk: score += 5
                found.append((score, obj))
    walk(rec)
    return max(found, default=(None, None))[1]


def parse_record(rec, idx):
    ra = as_float(first(rec, ["ra", "RA", "raDeg", "ra_deg", "coordinates.ra", "position.ra"]))
    dec = as_float(first(rec, ["dec", "DEC", "decDeg", "dec_deg", "coordinates.dec", "position.dec"]))
    fov = parse_fov(first(rec, ["fieldOfViewDeg", "fieldOfView", "field_of_view", "fov", "FOV", "selectedImage.fieldOfView"]))
    url = image_url(rec)
    rid = first(rec, ["archiveId", "archive_id", "id", "name", "title"]) or f"record-{idx+1}"
    name = first(rec, ["commonName", "name", "title", "designation"]) or str(rid)
    if None in (ra, dec, fov) or not url:
        return None
    return {"catalog_index": idx+1, "id": str(rid), "name": str(name), "ra": ra, "dec": dec, "fov": fov, "provider_url": url}


def dss2_url(ra, dec, fov, size=1600):
    q = urlencode({
        "hips": "P/DSS2/color",
        "width": size,
        "height": size,
        "fov": f"{fov:.9f}",
        "projection": "TAN",
        "coordsys": "icrs",
        "ra": f"{ra:.12f}",
        "dec": f"{dec:.12f}",
        "format": "jpg",
    })
    return "https://alasky.cds.unistra.fr/hips-image-services/hips2fits?" + q


def download(url, path):
    r = requests.get(url, timeout=90, headers={"User-Agent": UA})
    r.raise_for_status()
    path.write_bytes(r.content)
    return len(r.content), r.headers.get("content-type", "")


def safe_name(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(s)).strip("_")[:60] or "UNKNOWN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    records = records_of(data)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    selected = []
    for i, raw in enumerate(records):
        rec = parse_record(raw, i)
        if rec:
            selected.append(rec)
        if len(selected) >= args.limit:
            break

    manifest = {
        "schema": "gv-astrometry-pair-acquisition-0001",
        "purpose": "IMAGE ACQUISITION ONLY — no astrometry solution is computed here.",
        "catalog": args.catalog,
        "reference": "P/DSS2/color",
        "reference_orientation": "north-up 0 deg",
        "pairs": [],
    }

    for n, rec in enumerate(selected, 1):
        folder = out / f"PAIR-{n:04d}-{safe_name(rec['id'])}"
        folder.mkdir(parents=True, exist_ok=True)
        provider_path = folder / "01_PROVIDER.jpg"
        dss2_path = folder / "02_DSS2_NORTH_UP.jpg"
        metadata_path = folder / "03_METADATA.json"
        ref_url = dss2_url(rec["ra"], rec["dec"], rec["fov"])

        p_size, p_type = download(rec["provider_url"], provider_path)
        d_size, d_type = download(ref_url, dss2_path)

        meta = {
            **rec,
            "pair_number": n,
            "reference": "P/DSS2/color",
            "reference_orientation_deg": 0,
            "reference_url": ref_url,
            "provider_file": str(provider_path.relative_to(out)),
            "reference_file": str(dss2_path.relative_to(out)),
            "provider_bytes": p_size,
            "reference_bytes": d_size,
            "provider_content_type": p_type,
            "reference_content_type": d_type,
            "analysis_status": "UNANALYZED",
        }
        metadata_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        manifest["pairs"].append(meta)
        print(f"PAIR {n}: {rec['id']} | {rec['name']} | provider={p_size} bytes | DSS2={d_size} bytes")

    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"ACQUISITION COMPLETE: {len(manifest['pairs'])} pairs -> {out}")


if __name__ == "__main__":
    main()
