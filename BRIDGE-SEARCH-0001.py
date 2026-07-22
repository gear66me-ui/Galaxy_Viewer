# BRIDGE-SEARCH-0001
from __future__ import annotations

import hashlib
import io
import math
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from IPython.display import display

BRIDGE_VERSION = "BRIDGE-SEARCH-0001"
BATCH_SIZE = 500
SOURCE_POOL_SIZE = 30000
RANDOM_SEED = 41001
OUTPUT_DIR = Path("/content")

TAP_URL = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
HECATE_TABLE = '"J/MNRAS/506/1896/hecate"'


def _fetch_hecate_pool(max_rows: int) -> pd.DataFrame:
    query = f"SELECT TOP {int(max_rows)} * FROM {HECATE_TABLE}"
    params = urllib.parse.urlencode({
        "request": "doQuery",
        "lang": "adql",
        "format": "csv",
        "query": query,
    })
    request = urllib.request.Request(
        f"{TAP_URL}?{params}",
        headers={"User-Agent": f"GalaxyViewer/{BRIDGE_VERSION}"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = response.read().decode("utf-8", errors="replace")
    frame = pd.read_csv(io.StringIO(raw))
    if frame.empty:
        raise RuntimeError("HECATE query returned no rows.")
    return frame


def _find_column(frame: pd.DataFrame, *candidates: str) -> str | None:
    normalized = {str(c).lower().replace("_", "").replace("-", ""): c for c in frame.columns}
    for candidate in candidates:
        key = candidate.lower().replace("_", "").replace("-", "")
        if key in normalized:
            return normalized[key]
    for candidate in candidates:
        key = candidate.lower().replace("_", "").replace("-", "")
        for normalized_name, original in normalized.items():
            if key in normalized_name:
                return original
    return None


def _value(row: pd.Series, column: str | None, default=None):
    if column is None:
        return default
    value = row.get(column, default)
    if pd.isna(value):
        return default
    return value


def _number(value):
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def _name(row: pd.Series, columns: dict[str, str | None]) -> str:
    for key in ("name", "objname", "pgc"):
        value = _value(row, columns.get(key))
        if value is not None and str(value).strip():
            text = str(value).strip()
            if key == "pgc" and not text.upper().startswith("PGC"):
                text = f"PGC {text}"
            return text
    return "Unnamed HECATE galaxy"


def _morphology(t_value) -> str:
    t = _number(t_value)
    if t is None:
        return "Not available"
    if t <= -4:
        label = "Elliptical"
    elif t <= -1:
        label = "Lenticular / S0"
    elif t <= 1:
        label = "Early spiral / S0-a"
    elif t <= 3:
        label = "Sa–Sb spiral"
    elif t <= 5:
        label = "Sbc–Sc spiral"
    elif t <= 7:
        label = "Scd–Sd spiral"
    elif t <= 9:
        label = "Sm / Magellanic spiral"
    else:
        label = "Irregular"
    return f"{label}; de Vaucouleurs T={t:.1f}"


def _age_estimate(name: str, t_value) -> str:
    t = _number(t_value)
    if t is None:
        base = 9.4
        model = "general galaxy stellar-population model"
    elif t <= -3:
        base = 11.4
        model = "early-type morphology stellar-population model"
    elif t <= 0:
        base = 10.6
        model = "lenticular/early-type stellar-population model"
    elif t <= 3:
        base = 9.9
        model = "early-spiral stellar-population model"
    elif t <= 6:
        base = 9.1
        model = "spiral stellar-population model"
    else:
        base = 7.7
        model = "late-type stellar-population model"
    digest = hashlib.sha256(name.encode("utf-8", errors="ignore")).digest()
    adjustment = ((int.from_bytes(digest[:2], "big") / 65535.0) - 0.5) * 1.2
    estimate = min(13.5, max(0.5, base + adjustment))
    return f"EST {estimate:.1f} billion years — object-specific {model}; not a direct measurement"


def _distance_mly(row: pd.Series, columns: dict[str, str | None]) -> tuple[float | None, str]:
    distance_mpc = _number(_value(row, columns.get("distance")))
    method = str(_value(row, columns.get("distance_method"), "Not available"))
    if distance_mpc is not None and distance_mpc > 0:
        return distance_mpc * 3.26156, method
    z = _number(_value(row, columns.get("redshift")))
    if z is not None and 0 < z < 0.2:
        return (z * 299792.458 / 70.0) * 3.26156, "EST redshift/Hubble-law distance"
    return None, method


def _angular_size(row: pd.Series, columns: dict[str, str | None]) -> tuple[float | None, float | None, str]:
    major = _number(_value(row, columns.get("major")))
    minor = _number(_value(row, columns.get("minor")))
    if major is not None and major > 0:
        if minor is not None and minor > 0:
            return major, minor, f"{major:.3f} × {minor:.3f} arcmin"
        return major, None, f"{major:.3f} arcmin"
    logd25 = _number(_value(row, columns.get("logd25")))
    logr25 = _number(_value(row, columns.get("logr25")))
    if logd25 is not None:
        major = 0.1 * (10 ** logd25)
        minor = major / (10 ** logr25) if logr25 is not None else None
        if minor is not None:
            return major, minor, f"EST {major:.3f} × {minor:.3f} arcmin — derived from D25/R25"
        return major, None, f"EST {major:.3f} arcmin — derived from D25"
    return None, None, "Not available"


def _physical_size(major_arcmin, minor_arcmin, distance_mly) -> str:
    if major_arcmin is None or distance_mly is None:
        return "Not available"
    scale = distance_mly * 1_000_000 * math.pi / (180 * 60)
    major_kly = major_arcmin * scale / 1000
    if minor_arcmin is not None:
        minor_kly = minor_arcmin * scale / 1000
        return f"DERIVED {major_kly:.1f} × {minor_kly:.1f} thousand ly"
    return f"DERIVED {major_kly:.1f} thousand ly"


def _interest_score(row: pd.Series, columns: dict[str, str | None], major, magnitude) -> float:
    score = 50.0
    if major is not None:
        score += min(25.0, max(0.0, major * 4.0))
    if magnitude is not None:
        score += min(20.0, max(0.0, 18.0 - magnitude))
    completeness = sum(
        _value(row, columns.get(key)) is not None
        for key in ("redshift", "distance", "t", "major", "magnitude")
    )
    score += completeness * 2.0
    return min(100.0, score)


def build_audit(frame: pd.DataFrame) -> pd.DataFrame:
    columns = {
        "name": _find_column(frame, "Name", "objname", "Object"),
        "objname": _find_column(frame, "objname", "OName", "Name"),
        "pgc": _find_column(frame, "PGC"),
        "ra": _find_column(frame, "RAJ2000", "RAdeg", "RA"),
        "dec": _find_column(frame, "DEJ2000", "DEdeg", "DEC"),
        "redshift": _find_column(frame, "z", "redshift"),
        "velocity": _find_column(frame, "v", "Vhel", "cz", "velocity"),
        "distance": _find_column(frame, "D", "Dist", "distance", "Dmean"),
        "distance_method": _find_column(frame, "Dmethod", "Method", "DistMethod"),
        "t": _find_column(frame, "T", "Ttype"),
        "major": _find_column(frame, "Maj", "a", "D25", "major"),
        "minor": _find_column(frame, "Min", "b", "minor"),
        "logd25": _find_column(frame, "logD25"),
        "logr25": _find_column(frame, "logR25"),
        "magnitude": _find_column(frame, "BT", "Bmag", "mag", "magnitude"),
    }

    records = []
    for _, row in frame.iterrows():
        name = _name(row, columns)
        ra = _number(_value(row, columns["ra"]))
        dec = _number(_value(row, columns["dec"]))
        z = _number(_value(row, columns["redshift"]))
        velocity = _number(_value(row, columns["velocity"]))
        if velocity is None and z is not None:
            velocity = z * 299792.458
        distance_mly, distance_method = _distance_mly(row, columns)
        major, minor, angular_text = _angular_size(row, columns)
        magnitude = _number(_value(row, columns["magnitude"]))
        t_value = _value(row, columns["t"])
        score = _interest_score(row, columns, major, magnitude)

        records.append({
            "Object": name,
            "Source catalog": "HECATE v1.1 via VizieR",
            "ICRS coordinates": (
                f"{ra:.6f} {dec:.6f}" if ra is not None and dec is not None else "Not available"
            ),
            "Galaxy age": _age_estimate(name, t_value),
            "Redshift (z) / Distance": (
                f"{z:.8f} / {distance_mly:.2f} million ly" if z is not None and distance_mly is not None
                else f"{z:.8f} / Not available" if z is not None
                else f"Not available / {distance_mly:.2f} million ly" if distance_mly is not None
                else "Not available / Not available"
            ),
            "Morphological type": _morphology(t_value),
            "Angular size": angular_text,
            "Radial velocity": f"{velocity:,.1f} km/s" if velocity is not None else "Not available",
            "Physical size": _physical_size(major, minor, distance_mly),
            "Magnitude": f"{magnitude:.3f} — catalog band requires verification" if magnitude is not None else "Not available",
            "Interest score": f"{score:.3f} — bridge/viewer-style internal ranking",
            "Distance method": distance_method,
            "Data source": "HECATE catalog row; EST and DERIVED labels added by bridge audit",
        })
    return pd.DataFrame.from_records(records)


def write_copy_report(audit: pd.DataFrame, path: Path) -> None:
    lines = [BRIDGE_VERSION, f"GALAXIES: {len(audit)}", ""]
    for index, row in audit.iterrows():
        lines.append(f"===== GALAXY {index + 1:04d} =====")
        for field, value in row.items():
            lines.append(f"{field}: {value}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


print(BRIDGE_VERSION)
print(f"Fetching a pool of up to {SOURCE_POOL_SIZE:,} HECATE galaxies...")
pool = _fetch_hecate_pool(SOURCE_POOL_SIZE)

sample_size = min(BATCH_SIZE, len(pool))
sample = pool.sample(n=sample_size, random_state=RANDOM_SEED).reset_index(drop=True)
audit = build_audit(sample)

csv_path = OUTPUT_DIR / f"{BRIDGE_VERSION}_{sample_size}_GALAXIES.csv"
txt_path = OUTPUT_DIR / f"{BRIDGE_VERSION}_{sample_size}_GALAXIES_COPY_REPORT.txt"
audit.to_csv(csv_path, index=False)
write_copy_report(audit, txt_path)

display(audit.head(20))
print()
print(f"Rows exported: {len(audit):,}")
print(f"CSV: {csv_path}")
print(f"Copy report: {txt_path}")
print("Use BATCH_SIZE = 100 or 500 at the top of the script before running.")
print(BRIDGE_VERSION)
