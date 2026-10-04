#!/usr/bin/env python3
"""
Galaxy Viewer survey thumbnail builder.

Reads the release master catalog, generates small cache-friendly WebP thumbnails
for every survey record, and writes a compact lookup index used by Survey Mode.

Safe to rerun:
- existing generated thumbnails are reused unless --force is passed;
- stale generated thumbnails can be pruned with --prune;
- failures are recorded in the index instead of aborting the whole run.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import io
import json
import re
import shutil
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urlunparse

import requests
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "viewer/image-databases/master-database/gv-master-catalog.json"
OUT_ROOT = ROOT / "viewer/artwork/runtime/survey-thumbnails"
INDEX_PATH = OUT_ROOT / "gv-survey-thumbnail-index.json"

DEFAULT_SIZE = 192
DEFAULT_QUALITY = 76
DEFAULT_WORKERS = 12
MAX_DOWNLOAD_BYTES = 32 * 1024 * 1024
TIMEOUT = (8, 30)
USER_AGENT = "GalaxyViewer-SurveyThumbnailBuilder/1.0 (+https://github.com/gear66me-ui/Galaxy_Viewer)"

URL_KEYS = (
    "thumbnailUrl",
    "thumbUrl",
    "selectedImageUrl",
    "screenUrl",
    "imageUrl",
    "githubImageUrl",
    "hdUrl",
    "largeUrl",
    "avmSourceUrl",
    "esaPublicationJpeg",
)

_thread_local = threading.local()


@dataclass(frozen=True)
class WorkItem:
    provider: str
    catalog_name: str
    catalog_path: str
    catalog_key: str
    catalog_index: int
    archive_id: str
    designation: str
    display_name: str
    source_candidates: tuple[str, ...]
    lookup_key: str
    relative_output: str
    output_path: Path


def session() -> requests.Session:
    s = getattr(_thread_local, "session", None)
    if s is None:
        s = requests.Session()
        s.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            }
        )
        adapter = requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=0)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        _thread_local.session = s
    return s


def slugify(value: str, fallback: str = "image") -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", str(value or "").strip()).strip("-").lower()
    return s[:64] or fallback


def norm_provider(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", str(value or "").upper()) or "UNKNOWN"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def locate_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        for key in ("entries", "records", "galaxies", "items", "images"):
            v = data.get(key)
            if isinstance(v, list) and (not v or isinstance(v[0], dict)):
                return [x for x in v if isinstance(x, dict)]

    candidates: list[list[dict[str, Any]]] = []

    def walk(node: Any) -> None:
        if isinstance(node, list):
            dicts = [x for x in node if isinstance(x, dict)]
            if dicts and len(dicts) >= max(1, len(node) // 2):
                scored = sum(
                    1
                    for d in dicts[: min(40, len(dicts))]
                    if any(k in d for k in URL_KEYS)
                    or any(k in d for k in ("ra", "dec", "designation", "archiveId"))
                )
                if scored:
                    candidates.append(dicts)
            for x in node[:20]:
                walk(x)
        elif isinstance(node, dict):
            for v in node.values():
                walk(v)

    walk(data)
    return max(candidates, key=len) if candidates else []


def normalize_url(url: str) -> str:
    u = str(url or "").strip()
    if not u.startswith(("http://", "https://")):
        return ""
    if u.startswith("http://"):
        u = "https://" + u[7:]
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)", u)
    if m:
        return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{m.group(3)}/{m.group(4)}"
    return u


def provider_thumb_variant(url: str) -> str:
    """Prefer provider-hosted thumbnail derivatives when the URL pattern is known."""
    u = normalize_url(url)
    if not u:
        return ""
    try:
        p = urlparse(u)
        host = p.hostname.lower() if p.hostname else ""
        path = p.path
        if host in {"cdn.esawebb.org", "cdn.esahubble.org"} and "/archives/images/screen/" in path:
            path = path.replace("/archives/images/screen/", "/archives/images/thumb300y/")
        elif host in {"www.eso.org", "cdn.eso.org"} and "/public/archives/images/screen/" in path:
            path = path.replace("/public/archives/images/screen/", "/public/archives/images/thumb300y/")
        elif host == "storage.noirlab.edu" and "/media/archives/images/screen/" in path:
            path = path.replace("/media/archives/images/screen/", "/media/archives/images/thumb300y/")
        else:
            return ""
        return urlunparse((p.scheme, p.netloc, path, p.params, p.query, p.fragment))
    except Exception:
        return ""


def collect_urls(record: dict[str, Any]) -> tuple[str, ...]:
    raw: list[str] = []

    def add(value: Any) -> None:
        if isinstance(value, str):
            u = normalize_url(value)
            if u and u not in raw:
                raw.append(u)
        elif isinstance(value, list):
            for x in value:
                add(x)

    for key in URL_KEYS:
        add(record.get(key))
    add(record.get("jpegCandidates"))

    derived: list[str] = []
    for u in raw:
        v = provider_thumb_variant(u)
        if v and v not in derived:
            derived.append(v)

    out: list[str] = []
    for u in derived + raw:
        if u and u not in out:
            out.append(u)
    return tuple(out)


def record_identity(provider: str, catalog_key: str, catalog_index: int, record: dict[str, Any]) -> str:
    archive = str(record.get("archiveId") or record.get("id") or "").strip()
    designation = str(record.get("designation") or record.get("name") or record.get("title") or "").strip()
    selected = normalize_url(
        record.get("selectedImageUrl")
        or record.get("imageUrl")
        or record.get("githubImageUrl")
        or record.get("hdUrl")
        or ""
    )
    return f"{provider}|{catalog_key}|{catalog_index}|{archive}|{designation}|{selected}"


def build_items() -> tuple[list[WorkItem], dict[str, dict[str, Any]]]:
    master = load_json(MASTER)
    catalogs = master.get("catalogs") if isinstance(master, dict) else None
    if not isinstance(catalogs, dict):
        raise RuntimeError(f"Master catalog does not contain a catalogs mapping: {MASTER}")

    items: list[WorkItem] = []
    catalog_stats: dict[str, dict[str, Any]] = {}

    for catalog_name, rel_path in catalogs.items():
        path = ROOT / str(rel_path)
        if not path.exists():
            raise FileNotFoundError(path)
        data = load_json(path)
        records = locate_records(data)
        provider_default = norm_provider(
            (data.get("provider") if isinstance(data, dict) else "")
            or (data.get("providerLabel") if isinstance(data, dict) else "")
            or catalog_name
        )
        catalog_stats[provider_default] = {
            "catalogName": catalog_name,
            "catalogPath": str(rel_path),
            "records": len(records),
            "generated": 0,
            "reused": 0,
            "failed": 0,
        }

        for i, record in enumerate(records):
            provider = norm_provider(record.get("provider") or provider_default)
            catalog_key = str(record.get("catalogKey") or catalog_name).strip()
            try:
                catalog_index = int(record.get("catalogIndex"))
            except Exception:
                catalog_index = i

            archive_id = str(record.get("archiveId") or "").strip()
            designation = str(record.get("designation") or record.get("name") or "").strip()
            display_name = str(
                record.get("commonName")
                or record.get("displayName")
                or record.get("name")
                or record.get("title")
                or designation
                or archive_id
                or f"IMAGE {catalog_index + 1}"
            ).strip()

            candidates = collect_urls(record)
            identity = record_identity(provider, catalog_key, catalog_index, record)
            digest = hashlib.sha1(identity.encode("utf-8")).hexdigest()[:10]
            readable = slugify(archive_id or designation or display_name, f"{catalog_index:04d}")
            provider_dir = provider.lower()
            filename = f"{catalog_index:04d}-{readable}-{digest}.webp"
            rel_out = f"viewer/artwork/runtime/survey-thumbnails/{provider_dir}/{filename}"
            lookup_key = f"{provider}|{catalog_key}|{catalog_index}"
            items.append(
                WorkItem(
                    provider=provider,
                    catalog_name=str(catalog_name),
                    catalog_path=str(rel_path),
                    catalog_key=catalog_key,
                    catalog_index=catalog_index,
                    archive_id=archive_id,
                    designation=designation,
                    display_name=display_name,
                    source_candidates=candidates,
                    lookup_key=lookup_key,
                    relative_output=rel_out,
                    output_path=ROOT / rel_out,
                )
            )

    return items, catalog_stats


def download_bytes(url: str) -> tuple[bytes, str]:
    last_error = "unknown"
    for attempt in range(3):
        try:
            with session().get(url, stream=True, timeout=TIMEOUT, allow_redirects=True) as r:
                r.raise_for_status()
                ctype = (r.headers.get("content-type") or "").lower()
                if "text/html" in ctype:
                    raise ValueError(f"HTML response ({ctype})")
                total_header = r.headers.get("content-length")
                if total_header and int(total_header) > MAX_DOWNLOAD_BYTES:
                    raise ValueError(f"source too large: {total_header} bytes")
                chunks: list[bytes] = []
                total = 0
                for chunk in r.iter_content(128 * 1024):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > MAX_DOWNLOAD_BYTES:
                        raise ValueError(f"source exceeded {MAX_DOWNLOAD_BYTES} bytes")
                    chunks.append(chunk)
                return b"".join(chunks), r.url
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"
            if attempt < 2:
                time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(last_error)


def render_webp(data: bytes, out_path: Path, size: int, quality: int) -> None:
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        if im.mode == "RGBA":
            bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
            bg.alpha_composite(im)
            im = bg.convert("RGB")
        else:
            im = im.convert("RGB")

        im.thumbnail((size, size), Image.Resampling.LANCZOS, reducing_gap=3.0)
        canvas = Image.new("RGB", (size, size), (0, 0, 0))
        canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        temp = out_path.with_suffix(out_path.suffix + ".tmp")
        canvas.save(temp, "WEBP", quality=quality, method=6)
        temp.replace(out_path)


def process_item(item: WorkItem, size: int, quality: int, force: bool) -> dict[str, Any]:
    if item.output_path.exists() and item.output_path.stat().st_size > 128 and not force:
        return {
            "status": "reused",
            "item": item,
            "source": "",
            "bytes": item.output_path.stat().st_size,
            "error": "",
        }

    if not item.source_candidates:
        return {"status": "failed", "item": item, "source": "", "bytes": 0, "error": "no image URL candidates"}

    errors: list[str] = []
    for url in item.source_candidates:
        try:
            data, final_url = download_bytes(url)
            render_webp(data, item.output_path, size, quality)
            return {
                "status": "generated",
                "item": item,
                "source": final_url,
                "bytes": item.output_path.stat().st_size,
                "error": "",
            }
        except (UnidentifiedImageError, OSError, RuntimeError, ValueError, requests.RequestException) as e:
            errors.append(f"{url} -> {type(e).__name__}: {e}")
        except Exception as e:
            errors.append(f"{url} -> {type(e).__name__}: {e}")

    return {
        "status": "failed",
        "item": item,
        "source": "",
        "bytes": 0,
        "error": " | ".join(errors)[-6000:],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=DEFAULT_SIZE)
    ap.add_argument("--quality", type=int, default=DEFAULT_QUALITY)
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--prune", action="store_true")
    args = ap.parse_args()

    if not (64 <= args.size <= 512):
        raise SystemExit("--size must be between 64 and 512")
    if not (30 <= args.quality <= 95):
        raise SystemExit("--quality must be between 30 and 95")
    if not (1 <= args.workers <= 24):
        raise SystemExit("--workers must be between 1 and 24")

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    items, catalog_stats = build_items()
    print(f"Survey records discovered: {len(items)}")
    for provider, stat in sorted(catalog_stats.items()):
        print(f"  {provider:8s} {stat['records']:5d}  {stat['catalogPath']}")

    if not items:
        raise SystemExit("No survey records discovered")

    generated: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    total_bytes = 0
    done = 0
    lock = threading.Lock()
    started = time.time()

    def consume(result: dict[str, Any]) -> None:
        nonlocal total_bytes, done
        item: WorkItem = result["item"]
        status = result["status"]
        stat = catalog_stats.setdefault(
            item.provider,
            {"catalogName": item.catalog_name, "catalogPath": item.catalog_path, "records": 0, "generated": 0, "reused": 0, "failed": 0},
        )
        stat[status] = stat.get(status, 0) + 1
        done += 1

        if status in ("generated", "reused"):
            total_bytes += int(result["bytes"] or 0)
            generated[item.lookup_key] = {
                "provider": item.provider,
                "catalogKey": item.catalog_key,
                "catalogIndex": item.catalog_index,
                "archiveId": item.archive_id,
                "designation": item.designation,
                "name": item.display_name,
                "path": item.relative_output,
                "bytes": int(result["bytes"] or 0),
                "source": result["source"],
            }
        else:
            failures.append(
                {
                    "provider": item.provider,
                    "catalogKey": item.catalog_key,
                    "catalogIndex": item.catalog_index,
                    "archiveId": item.archive_id,
                    "designation": item.designation,
                    "name": item.display_name,
                    "candidates": list(item.source_candidates),
                    "error": result["error"],
                }
            )

        if done % 25 == 0 or done == len(items):
            elapsed = max(0.1, time.time() - started)
            print(
                f"[{done:4d}/{len(items)}] "
                f"ok={len(generated):4d} fail={len(failures):3d} "
                f"{done/elapsed:5.1f} rec/s"
            )

    with cf.ThreadPoolExecutor(max_workers=args.workers, thread_name_prefix="gvthumb") as pool:
        futures = [pool.submit(process_item, item, args.size, args.quality, args.force) for item in items]
        for fut in cf.as_completed(futures):
            with lock:
                consume(fut.result())

    desired = {item.relative_output for item in items}
    pruned: list[str] = []
    if args.prune:
        for path in OUT_ROOT.rglob("*.webp"):
            rel = path.relative_to(ROOT).as_posix()
            if rel not in desired:
                pruned.append(rel)
                path.unlink()
        for p in sorted(OUT_ROOT.iterdir()):
            if p.is_dir() and not any(p.rglob("*")):
                shutil.rmtree(p)

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    index = {
        "version": "0001",
        "generatedAt": generated_at,
        "generator": "tools/survey_thumbnails/build_survey_thumbnails.py",
        "format": "webp",
        "canvasPixels": args.size,
        "quality": args.quality,
        "workerCount": args.workers,
        "recordCount": len(items),
        "thumbnailCount": len(generated),
        "failedCount": len(failures),
        "totalThumbnailBytes": total_bytes,
        "catalogs": catalog_stats,
        "lookupKey": "PROVIDER|catalogKey|catalogIndex",
        "records": dict(sorted(generated.items())),
        "failures": failures,
        "pruned": pruned,
    }
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Index: {INDEX_PATH.relative_to(ROOT)}")
    print(f"Thumbnails: {len(generated)}/{len(items)}")
    print(f"Failures: {len(failures)}")
    print(f"Total thumbnail bytes: {total_bytes:,}")
    if pruned:
        print(f"Pruned stale thumbnails: {len(pruned)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
