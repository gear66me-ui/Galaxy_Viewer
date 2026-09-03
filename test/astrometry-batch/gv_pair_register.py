#!/usr/bin/env python3
import argparse, json, math, re, sys, time
from pathlib import Path
from urllib.parse import urlencode

import cv2
import numpy as np
import requests

UA = "Galaxy-Viewer-Astrometry-Batch/0001"
IMG_SIZE = 384


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
    # FOV strings such as "0.040333 x 0.043167 degrees": use the larger dimension.
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
            for k, v in obj.items(): walk(v, str(k))
        elif isinstance(obj, list):
            for v in obj: walk(v, key)
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
        return None, {"index": idx+1, "id": rid, "reason": "missing ra/dec/fov/image", "ra": ra, "dec": dec, "fov": fov, "image": url}
    return {"index": idx+1, "id": str(rid), "name": str(name), "ra": ra, "dec": dec, "fov": fov, "image": url}, None


def get_bytes(url, timeout=60):
    r = requests.get(url, timeout=timeout, headers={"User-Agent": UA})
    r.raise_for_status()
    return r.content


def decode_image(blob):
    a = np.frombuffer(blob, dtype=np.uint8)
    im = cv2.imdecode(a, cv2.IMREAD_COLOR)
    if im is None:
        raise ValueError("image decode failed")
    return im


def dss2_url(ra, dec, fov, size=1200):
    q = urlencode({
        "hips": "P/DSS2/color", "width": size, "height": size,
        "fov": f"{fov:.9f}", "projection": "TAN", "coordsys": "icrs",
        "ra": f"{ra:.12f}", "dec": f"{dec:.12f}", "format": "jpg"
    })
    return "https://alasky.cds.unistra.fr/hips-image-services/hips2fits?" + q


def square_crop(im):
    h, w = im.shape[:2]
    n = min(h, w)
    y = (h-n)//2; x = (w-n)//2
    return im[y:y+n, x:x+n]


def preprocess(im):
    im = square_crop(im)
    im = cv2.resize(im, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    gray = cv2.GaussianBlur(gray, (0,0), 1.2)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    g = cv2.magnitude(gx, gy)
    lo, hi = np.percentile(g, (25, 99.5))
    g = np.clip((g-lo)/(hi-lo+1e-6), 0, 1).astype(np.float32)
    # Downweight borders where crops/rotation generate artificial edges.
    yy, xx = np.mgrid[:IMG_SIZE,:IMG_SIZE]
    cx = cy = (IMG_SIZE-1)/2
    r = np.sqrt((xx-cx)**2 + (yy-cy)**2) / (IMG_SIZE/2)
    mask = np.clip((1.0-r)/0.18, 0, 1).astype(np.float32)
    return g*mask, im


def warp_rotation_scale(im, angle, scale):
    c = ((IMG_SIZE-1)/2, (IMG_SIZE-1)/2)
    M = cv2.getRotationMatrix2D(c, angle, scale)
    return cv2.warpAffine(im, M, (IMG_SIZE, IMG_SIZE), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def shifted(im, dx, dy):
    M = np.float32([[1,0,dx],[0,1,dy]])
    return cv2.warpAffine(im, M, (IMG_SIZE, IMG_SIZE), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def score_candidate(src, ref, angle, scale, hann):
    w = warp_rotation_scale(ref, angle, scale)
    (dx, dy), response = cv2.phaseCorrelate(w, src, hann)
    a = shifted(w, dx, dy)
    m = (a > 0.02) & (src > 0.02)
    if m.sum() < 5000:
        return -1e9, dx, dy, response, 0.0
    x = src[m].astype(np.float64); y = a[m].astype(np.float64)
    x -= x.mean(); y -= y.mean()
    ncc = float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12))
    score = 0.65*float(response) + 0.35*ncc
    return score, dx, dy, float(response), ncc


def solve(src, ref):
    hann = cv2.createHanningWindow((IMG_SIZE, IMG_SIZE), cv2.CV_32F)
    best = None
    # Coarse global search. Broad scale range intentionally tolerates imperfect catalog FOV.
    for scale in np.arange(0.70, 1.301, 0.05):
        for angle in np.arange(0.0, 360.0, 3.0):
            s = score_candidate(src, ref, float(angle), float(scale), hann)
            row = (s[0], float(angle), float(scale), s[1], s[2], s[3], s[4])
            if best is None or row[0] > best[0]: best = row
    # Fine search around the coarse maximum.
    _, a0, s0, *_ = best
    fine = None
    for scale in np.arange(max(0.60,s0-0.04), min(1.45,s0+0.0401), 0.005):
        for da in np.arange(-4.0, 4.001, 0.25):
            angle = (a0 + da) % 360.0
            s = score_candidate(src, ref, float(angle), float(scale), hann)
            row = (s[0], float(angle), float(scale), s[1], s[2], s[3], s[4])
            if fine is None or row[0] > fine[0]: fine = row
    return fine


def diagnostic(provider_bgr, ref_bgr, result, out_file):
    _, angle, scale, dx, dy, _, _ = result
    p = cv2.resize(square_crop(provider_bgr), (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)
    r = cv2.resize(square_crop(ref_bgr), (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)
    wr = warp_rotation_scale(r.astype(np.float32)/255.0, angle, scale)
    wr = shifted(wr, dx, dy)
    wr = np.clip(wr*255,0,255).astype(np.uint8)
    overlay = cv2.addWeighted(p, 0.5, wr, 0.5, 0)
    canvas = np.hstack([p, r, overlay])
    cv2.putText(canvas, f"provider | DSS2 north-up | aligned  angle={angle:.2f} scale={scale:.4f}", (10,24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1, cv2.LINE_AA)
    cv2.imwrite(str(out_file), canvas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    diag = out/"diagnostics"; diag.mkdir(exist_ok=True)
    data = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    records = records_of(data)
    results=[]; skipped=[]
    usable=[]
    for i, raw in enumerate(records):
        rec, err = parse_record(raw, i)
        if rec: usable.append(rec)
        else: skipped.append(err)
        if len(usable) >= args.limit: break
    print(f"CATALOG records={len(records)} usable_selected={len(usable)} skipped_before_limit={len(skipped)}")
    for n, rec in enumerate(usable, 1):
        t0=time.time(); print(f"[{n}/{len(usable)}] {rec['id']} {rec['name']}", flush=True)
        row={**rec, "reference":"P/DSS2/color", "status":"FAIL"}
        try:
            pblob=get_bytes(rec["image"]); provider=decode_image(pblob)
            rurl=dss2_url(rec["ra"],rec["dec"],rec["fov"]); reference=decode_image(get_bytes(rurl))
            src,_=preprocess(provider); ref,_=preprocess(reference)
            res=solve(src,ref)
            score,angle,scale,dx,dy,response,ncc=res
            corrected_fov=rec["fov"]/scale
            row.update({
                "status":"SOLVED",
                "orientation_deg_dss2_to_provider":round(angle,4),
                "aladin_rotation_candidate_deg":round(angle if angle<=180 else angle-360,4),
                "scale_reference_to_provider":round(scale,6),
                "corrected_fov_deg_candidate":round(corrected_fov,9),
                "translation_px_at_384":{"x":round(dx,3),"y":round(dy,3)},
                "score":round(score,6),"phase_response":round(response,6),"gradient_ncc":round(ncc,6),
                "reference_url":rurl,
                "elapsed_s":round(time.time()-t0,2)
            })
            diagnostic(provider,reference,res,diag/f"{n:02d}_{re.sub(r'[^A-Za-z0-9._-]+','_',rec['id'])}.jpg")
            print(f"  SOLVED angle={angle:.3f} scale={scale:.4f} fov={corrected_fov:.7f} score={score:.4f}")
        except Exception as e:
            row["error"]=f"{type(e).__name__}: {e}"
            row["elapsed_s"]=round(time.time()-t0,2)
            print("  FAIL",row["error"],file=sys.stderr)
        results.append(row)
    payload={
        "schema":"gv-dss2-image-registration-proof-0001",
        "catalog":args.catalog,"limit":args.limit,"image_size":IMG_SIZE,
        "method":"gradient-map rotation/scale sweep + phase-correlation translation + NCC",
        "important":"READ-ONLY proof. Candidate parameters require visual validation before any catalog write.",
        "results":results,"skipped":skipped
    }
    (out/"results.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    solved=sum(r["status"]=="SOLVED" for r in results)
    print(f"DONE solved={solved}/{len(results)} artifact={out/'results.json'}")
    return 0 if solved else 2

if __name__ == "__main__":
    raise SystemExit(main())
