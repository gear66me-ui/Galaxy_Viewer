# BRIDGE-SEARCH-0002
from __future__ import annotations

import contextlib
import io
import json
import math
import os
import random
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from google.colab import userdata

BRIDGE_VERSION = "BRIDGE-SEARCH-0002"
BATCH_SIZE = 500
OUTPUT_DIR = Path("/content")
OUTPUT_NAME = f"{BRIDGE_VERSION}_{BATCH_SIZE}_GALAXIES.csv"
REPO = "gear66me-ui/Galaxy_Viewer"
BRANCH = "sandbox"
REMOTE_PATH = f"bridge-search/{OUTPUT_NAME}"
SECRET_NAME = "GITHUB_TOKEN"
TAP = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
SIMBAD_TAP = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
NED_API = "https://ned.ipac.caltech.edu/NED::API/OverviewOfObject"
USER_AGENT = "GalaxyViewer/BRIDGE-SEARCH-0002"
C_KMS = 299792.458


def http_text(url: str, timeout: int = 60) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def tap_csv(table: str, top: int) -> pd.DataFrame:
    query = f'SELECT TOP {int(top)} * FROM "{table}"'
    params = urllib.parse.urlencode({"request": "doQuery", "lang": "adql", "format": "csv", "query": query})
    return pd.read_csv(io.StringIO(http_text(f"{TAP}?{params}", 180)))


def norm(name: str) -> str:
    return "".join(ch.lower() for ch in str(name) if ch.isalnum())


def exact_col(frame: pd.DataFrame, *names: str) -> str | None:
    mapping = {norm(c): c for c in frame.columns}
    for name in names:
        if norm(name) in mapping:
            return mapping[norm(name)]
    return None


def num(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except Exception:
        return None


def val(row: pd.Series, col: str | None):
    if col is None:
        return None
    value = row.get(col)
    return None if pd.isna(value) else value


def format_name(value, prefix: str | None = None) -> str:
    text = str(value or "").strip()
    if not text:
        return "Unknown galaxy"
    if prefix and text.isdigit():
        return f"{prefix} {text}"
    return text


def parse_ra_dec(frame: pd.DataFrame, row: pd.Series) -> tuple[float | None, float | None]:
    ra_col = exact_col(frame, "RAJ2000", "RAdeg", "RA2000", "RA")
    dec_col = exact_col(frame, "DEJ2000", "DEdeg", "DE2000", "DEC")
    ra, dec = num(val(row, ra_col)), num(val(row, dec_col))
    return ra, dec


def source_rows() -> list[dict]:
    # Independent pools; no fixed random seed.
    pools = []
    specs = [
        ("HECATE v1.1", "J/MNRAS/506/1896/hecate", 5000),
        ("RC3", "VII/155/rc3", 5000),
        ("HyperLEDA PGC", "VII/237/pgc", 8000),
    ]
    for label, table, top in specs:
        try:
            frame = tap_csv(table, top)
            if not frame.empty:
                pools.append((label, frame))
        except Exception:
            pass
    if not pools:
        raise RuntimeError("No source catalogs were available.")

    quotas = [BATCH_SIZE // len(pools)] * len(pools)
    for i in range(BATCH_SIZE % len(pools)):
        quotas[i] += 1

    result = []
    for (label, frame), quota in zip(pools, quotas):
        indices = random.sample(range(len(frame)), min(quota, len(frame)))
        for index in indices:
            result.append({"source_label": label, "frame": frame, "row": frame.iloc[index]})
    random.SystemRandom().shuffle(result)
    return result[:BATCH_SIZE]


def base_record(item: dict) -> dict:
    frame, row, source = item["frame"], item["row"], item["source_label"]
    pgc_col = exact_col(frame, "PGC")
    name_col = exact_col(frame, "Name", "OName", "objname", "ANames")
    name = format_name(val(row, name_col))
    if name == "Unknown galaxy":
        name = format_name(val(row, pgc_col), "PGC")

    ra, dec = parse_ra_dec(frame, row)
    velocity_col = exact_col(frame, "V", "Vhel", "cz", "HRV", "vhelio")
    velocity = num(val(row, velocity_col))
    redshift_col = exact_col(frame, "z", "Redshift")
    redshift = num(val(row, redshift_col))
    if redshift is not None and not (0 <= redshift < 1):
        redshift = None
    if redshift is None and velocity is not None:
        redshift = velocity / C_KMS
    if velocity is None and redshift is not None:
        velocity = redshift * C_KMS

    distance_col = exact_col(frame, "D", "Dist", "Dmean", "distance")
    distance_mpc = num(val(row, distance_col))
    method_col = exact_col(frame, "Dmethod", "DistMethod", "Method")
    distance_method = str(val(row, method_col) or "Not available")

    t_col = exact_col(frame, "T", "Ttype", "TType")
    t_value = num(val(row, t_col))
    maj_col = exact_col(frame, "Maj", "D25", "logD25", "major")
    min_col = exact_col(frame, "Min", "minor")
    major, minor = num(val(row, maj_col)), num(val(row, min_col))
    mag_col = exact_col(frame, "BT", "Bmag", "mag", "magnitude")
    magnitude = num(val(row, mag_col))

    return {
        "name": name,
        "source_catalog": source,
        "ra": ra,
        "dec": dec,
        "redshift": redshift,
        "velocity": velocity,
        "distance_mpc": distance_mpc,
        "distance_method": distance_method,
        "t": t_value,
        "major_arcmin": major,
        "minor_arcmin": minor,
        "magnitude": magnitude,
        "provenance": [source],
        "agreement": [],
    }


def simbad_lookup(name: str) -> dict:
    safe = name.replace("'", "''")
    query = (
        "SELECT TOP 1 b.main_id,b.ra,b.dec,b.otype,b.rvz_redshift,b.rvz_radvel,"
        "b.galdim_majaxis,b.galdim_minaxis FROM basic AS b JOIN ident AS i ON b.oid=i.oidref "
        f"WHERE i.id='{safe}'"
    )
    params = urllib.parse.urlencode({"request": "doQuery", "lang": "adql", "format": "json", "query": query})
    try:
        payload = json.loads(http_text(f"{SIMBAD_TAP}?{params}", 35))
        if not payload.get("data"):
            return {}
        return {meta["name"]: payload["data"][0][i] for i, meta in enumerate(payload["metadata"])}
    except Exception:
        return {}


def recursive_find(data, keys: set[str]):
    if isinstance(data, dict):
        for key, value in data.items():
            if norm(key) in keys and value not in (None, ""):
                return value
        for value in data.values():
            found = recursive_find(value, keys)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for value in data:
            found = recursive_find(value, keys)
            if found not in (None, ""):
                return found
    return None


def ned_lookup(name: str) -> dict:
    try:
        url = f"{NED_API}?{urllib.parse.urlencode({'TARGET': name})}"
        return json.loads(http_text(url, 35))
    except Exception:
        return {}


def agree(a, b, relative=0.08) -> bool:
    a, b = num(a), num(b)
    if a is None or b is None:
        return False
    return abs(a - b) <= max(1e-12, relative * max(abs(a), abs(b)))


def merge_external(record: dict, simbad: dict, ned: dict) -> dict:
    if simbad:
        record["provenance"].append("SIMBAD")
        sz = num(simbad.get("rvz_redshift"))
        sv = num(simbad.get("rvz_radvel"))
        if record["redshift"] is None and sz is not None:
            record["redshift"] = sz
        elif agree(record["redshift"], sz, 0.10):
            record["agreement"].append("redshift")
        if record["velocity"] is None and sv is not None:
            record["velocity"] = sv
        elif agree(record["velocity"], sv, 0.10):
            record["agreement"].append("velocity")
        if record["ra"] is None:
            record["ra"] = num(simbad.get("ra"))
        if record["dec"] is None:
            record["dec"] = num(simbad.get("dec"))
        if record["major_arcmin"] is None:
            record["major_arcmin"] = num(simbad.get("galdim_majaxis"))
            record["minor_arcmin"] = num(simbad.get("galdim_minaxis"))
        record["simbad_type"] = simbad.get("otype")

    if ned:
        record["provenance"].append("NASA/IPAC NED")
        nz = num(recursive_find(ned, {norm("Redshift"), norm("z")}))
        nv = num(recursive_find(ned, {norm("v (Heliocentric)"), norm("Velocity"), norm("Radial velocity")}))
        if record["redshift"] is None and nz is not None:
            record["redshift"] = nz
        elif agree(record["redshift"], nz, 0.10):
            record["agreement"].append("redshift")
        if record["velocity"] is None and nv is not None:
            record["velocity"] = nv
        elif agree(record["velocity"], nv, 0.10):
            record["agreement"].append("velocity")
    return record


def morphology_text(record: dict) -> str:
    if record.get("simbad_type"):
        return f"{record['simbad_type']} [SIMBAD classification]"
    t = record.get("t")
    if t is None:
        return "Not available"
    if t <= -4: label = "Elliptical"
    elif t <= -1: label = "Lenticular / S0"
    elif t <= 1: label = "Early spiral / S0-a"
    elif t <= 3: label = "Sa–Sb spiral"
    elif t <= 5: label = "Sbc–Sc spiral"
    elif t <= 7: label = "Scd–Sd spiral"
    elif t <= 9: label = "Sm / Magellanic spiral"
    else: label = "Irregular"
    return f"{label}; de Vaucouleurs T={t:.1f} [catalog classification]"


def age_text(record: dict) -> str:
    t = record.get("t")
    if t is None:
        return "EST [broad 8–12 billion year population range; not object-specific; verify independently]"
    if t <= -1:
        return "EST [typically old-dominated stellar population, roughly 9–13 billion years; morphology-based, not a direct measurement]"
    if t <= 6:
        return "EST [mixed stellar populations, broadly 5–12 billion years; morphology-based, not a direct measurement]"
    return "EST [mixed/younger stellar populations possible, broadly 1–10 billion years; morphology-based, not a direct measurement]"


def distance_text(record: dict) -> tuple[str, float | None]:
    z, d = record.get("redshift"), record.get("distance_mpc")
    if d is None and z is not None and 0 < z < 0.2:
        d = z * C_KMS / 70.0
        record["distance_method"] = "EST [simple Hubble-law distance; verify independently]"
    mly = d * 3.26156 if d is not None else None
    z_text = f"{z:.8f}" if z is not None else "Not available"
    d_text = f"{mly:.2f} million ly" if mly is not None else "Not available"
    return f"{z_text} / {d_text}", mly


def angular_text(record: dict) -> str:
    a, b = record.get("major_arcmin"), record.get("minor_arcmin")
    if a is None:
        return "Not available"
    return f"{a:.3f} × {b:.3f} arcmin [catalog value; band/isophote may vary]" if b is not None else f"{a:.3f} arcmin [catalog value]"


def physical_text(record: dict, mly: float | None) -> str:
    a, b = record.get("major_arcmin"), record.get("minor_arcmin")
    if a is None or mly is None:
        return "Not available"
    scale = mly * 1_000_000 * math.pi / (180 * 60) / 1000
    return (f"EST [{a*scale:.1f} × {b*scale:.1f} thousand ly; derived from adopted distance and angular size]"
            if b is not None else f"EST [{a*scale:.1f} thousand ly; derived from adopted distance and angular size]")


def data_score(record: dict) -> int:
    weights = {
        "name": 8, "ra": 8, "dec": 8, "redshift": 12, "velocity": 10,
        "distance_mpc": 10, "t": 8, "major_arcmin": 10, "magnitude": 8,
    }
    score = sum(weight for key, weight in weights.items() if record.get(key) not in (None, "", "Unknown galaxy"))
    score += min(12, len(set(record.get("provenance", []))) * 4)
    score += min(6, len(set(record.get("agreement", []))) * 3)
    return min(100, score)


def render(record: dict) -> dict:
    redshift_distance, mly = distance_text(record)
    ra, dec = record.get("ra"), record.get("dec")
    score = data_score(record)
    return {
        "Object": record["name"],
        "Source catalog": record["source_catalog"],
        "ICRS coordinates": f"{ra:.6f} {dec:.6f}" if ra is not None and dec is not None else "Not available",
        "Galaxy age": age_text(record),
        "Redshift (z) / Distance": redshift_distance,
        "Morphological type": morphology_text(record),
        "Angular size": angular_text(record),
        "Radial velocity": f"{record['velocity']:,.1f} km/s" if record.get("velocity") is not None else "Not available",
        "Physical size": physical_text(record, mly),
        "Magnitude": f"{record['magnitude']:.3f} [catalog photometry; band must be shown in viewer]" if record.get("magnitude") is not None else "Not available",
        "Interest score": "Not evaluated by bridge",
        "Distance method": record.get("distance_method") or "Not available",
        "Data source": "; ".join(dict.fromkeys(record.get("provenance", []))) + "; values marked EST require verification",
        "Data score": f"{score}% [completeness + multi-source agreement; not a scientific certainty score]",
    }


def enrich_one(item: dict) -> dict:
    record = base_record(item)
    name = record["name"]
    return render(merge_external(record, simbad_lookup(name), ned_lookup(name)))


def upload_csv(path: Path, token: str) -> str:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            from github import Auth, Github
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "PyGithub"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            from github import Auth, Github
    client = Github(auth=Auth.Token(token))
    repo = client.get_repo(REPO)
    content = path.read_bytes()
    try:
        existing = repo.get_contents(REMOTE_PATH, ref=BRANCH)
        repo.update_file(REMOTE_PATH, f"Update {OUTPUT_NAME}", content, existing.sha, branch=BRANCH)
    except Exception as exc:
        if "404" not in str(exc):
            raise
        repo.create_file(REMOTE_PATH, f"Upload {OUTPUT_NAME}", content, branch=BRANCH)
    client.close()
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{REMOTE_PATH}"


def main() -> None:
    token = userdata.get(SECRET_NAME)
    if not token:
        raise RuntimeError(f"Colab Secret {SECRET_NAME} is unavailable.")
    items = source_rows()
    rows = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(enrich_one, item) for item in items]
        for future in as_completed(futures):
            try:
                rows.append(future.result())
            except Exception:
                pass
    if not rows:
        raise RuntimeError("No audit rows were produced.")
    output_path = OUTPUT_DIR / OUTPUT_NAME
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(upload_csv(output_path, token))


with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    try:
        _buffer = io.StringIO()
        with contextlib.redirect_stdout(_buffer), contextlib.redirect_stderr(_buffer):
            main()
        _lines = [line.strip() for line in _buffer.getvalue().splitlines() if line.strip().startswith("https://")]
    except Exception:
        raise
print(_lines[-1] if _lines else f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{REMOTE_PATH}")
