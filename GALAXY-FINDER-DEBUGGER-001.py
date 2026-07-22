from __future__ import annotations

import csv
import io
import json
import math
import random
import urllib.request
from pathlib import Path
from typing import Any

VERSION = "GALAXY-FINDER-DEBUGGER-001"
HECATE_URL = "https://hecate.ia.forth.gr/assets/files/HECATE_v1.1.csv"
CACHE_PATH = Path("/content/GALAXY-BEAUTY-CATALOG-0001.json")
SAMPLE_SIZE = 100
TOP_CATALOG_SIZE = 30000
C_KMS = 299792.458


def _clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"", "nan", "none", "--", "-99", "-999"} else text


def _number(value: Any) -> float | None:
    try:
        text = _clean(value)
        if not text:
            return None
        number = float(text)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def _pick(row: dict[str, Any], *names: str) -> str:
    lookup = {str(key).upper(): value for key, value in row.items()}
    for name in names:
        text = _clean(lookup.get(name.upper()))
        if text:
            return text
    return ""


def _interest_score(row: dict[str, Any]) -> float:
    r1 = _number(_pick(row, "R1"))
    bt = _number(_pick(row, "BT"))
    t_type = _number(_pick(row, "T"))
    inclination = _number(_pick(row, "INCL"))
    distance_mpc = _number(_pick(row, "D"))
    velocity = _number(_pick(row, "V"))
    name = _pick(row, "OBJNAME", "ID_NED")

    score = 0.0
    if r1 is not None:
        score += min(34.0, 13.0 * math.log10(max(1.0, 2.0 * r1 * 60.0)))
    if bt is not None:
        score += max(0.0, min(22.0, (18.0 - bt) * 3.0))
    if t_type is not None:
        if 1 <= t_type <= 9:
            score += 18.0
        elif t_type >= 9:
            score += 12.0
        elif -3 <= t_type < 1:
            score += 7.0
    if inclination is not None:
        score += max(0.0, 10.0 - abs(inclination - 42.0) / 5.0)
    if name.upper().startswith(("M ", "MESSIER", "NGC", "IC", "ARP", "UGC")):
        score += 10.0
    if distance_mpc is not None:
        score += 4.0
    if velocity is not None:
        score += 2.0

    completeness = sum(
        _number(_pick(row, key)) is not None
        for key in ("D", "V", "BT", "R1", "R2", "T", "INCL")
    )
    score += completeness * 1.5
    return round(score, 3)


def _download_hecate() -> list[dict[str, str]]:
    request = urllib.request.Request(
        HECATE_URL,
        headers={"User-Agent": f"{VERSION}/1.0"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        text = response.read().decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


def _build_catalog() -> list[dict[str, Any]]:
    rows = _download_hecate()
    scored: list[dict[str, Any]] = []

    for row in rows:
        ra = _number(_pick(row, "RA"))
        dec = _number(_pick(row, "DEC"))
        name = _pick(row, "OBJNAME", "ID_NED")
        if ra is None or dec is None or not name:
            continue

        record = {
            "name": name,
            "ra_deg": ra,
            "dec_deg": dec,
            "distance_mpc": _number(_pick(row, "D")),
            "distance_method": _pick(row, "DMETHOD") or "Not available",
            "velocity_kms": _number(_pick(row, "V")),
            "major_radius_arcmin": _number(_pick(row, "R1")),
            "minor_radius_arcmin": _number(_pick(row, "R2")),
            "magnitude_b": _number(_pick(row, "BT")),
            "morphology_t": _number(_pick(row, "T")),
            "inclination_deg": _number(_pick(row, "INCL")),
            "interest_score": _interest_score(row),
        }
        scored.append(record)

    scored.sort(key=lambda item: item["interest_score"], reverse=True)
    catalog = scored[:TOP_CATALOG_SIZE]
    CACHE_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return catalog


def _load_catalog() -> list[dict[str, Any]]:
    if CACHE_PATH.exists():
        try:
            data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list) and len(data) >= SAMPLE_SIZE:
                return data
        except Exception:
            pass
    return _build_catalog()


def _distance_text(distance_mpc: float | None) -> str:
    if distance_mpc is None or distance_mpc <= 0:
        return "Not available"
    million_ly = distance_mpc * 3.26156
    if million_ly < 1000.0:
        return f"{million_ly:.3f} million ly"
    return f"{million_ly / 1000.0:.6f} billion ly"


def _z_value(velocity_kms: float | None) -> float | None:
    if velocity_kms is None:
        return None
    return velocity_kms / C_KMS


def _angular_size(record: dict[str, Any]) -> str:
    r1 = _number(record.get("major_radius_arcmin"))
    r2 = _number(record.get("minor_radius_arcmin"))
    if r1 is None:
        return "Not available"
    major = 2.0 * r1
    if r2 is None:
        return f"{major:.3f} arcmin"
    return f"{major:.3f} x {2.0 * r2:.3f} arcmin"


def _physical_size(record: dict[str, Any]) -> str:
    distance_mpc = _number(record.get("distance_mpc"))
    r1 = _number(record.get("major_radius_arcmin"))
    r2 = _number(record.get("minor_radius_arcmin"))
    if distance_mpc is None or r1 is None:
        return "Not available"
    major_kly = math.radians((2.0 * r1) / 60.0) * distance_mpc * 3.26156e3
    if r2 is None:
        return f"{major_kly:.1f} thousand ly"
    minor_kly = math.radians((2.0 * r2) / 60.0) * distance_mpc * 3.26156e3
    return f"{major_kly:.1f} x {minor_kly:.1f} thousand ly"


def _format_number(value: float | None, digits: int = 3) -> str:
    return "Not available" if value is None else f"{value:.{digits}f}"


def main() -> None:
    catalog = _load_catalog()
    sample = random.sample(catalog, k=min(SAMPLE_SIZE, len(catalog)))

    print(f"{VERSION}")
    print(f"SOURCE: HECATE v1.1 Beauty Catalog Top {len(catalog):,}")
    print(f"SAMPLE SIZE: {len(sample)}")
    print("=" * 72)

    for index, galaxy in enumerate(sample, start=1):
        velocity = _number(galaxy.get("velocity_kms"))
        z = _z_value(velocity)
        morphology = _number(galaxy.get("morphology_t"))
        magnitude = _number(galaxy.get("magnitude_b"))
        score = _number(galaxy.get("interest_score"))

        print(f"GALAXY {index:03d}")
        print(f"1. Object: {galaxy.get('name') or 'Not available'}")
        print(f"2. ICRS coordinates: {float(galaxy['ra_deg']):.6f} {float(galaxy['dec_deg']):.6f}")
        print(f"3. Z: {'Not available' if z is None else f'{z:.8f}'}")
        print(f"4. Distance: {_distance_text(_number(galaxy.get('distance_mpc')))}")
        print(f"5. Distance method: {galaxy.get('distance_method') or 'Not available'}")
        print(f"6. Radial velocity: {'Not available' if velocity is None else f'{velocity:,.1f} km/s'}")
        print(f"7. Morphological type: {'Not available' if morphology is None else f'de Vaucouleurs T={morphology:.1f}'}")
        print(f"8. Angular size: {_angular_size(galaxy)}")
        print(f"9. Physical size: {_physical_size(galaxy)}")
        print(f"10. Magnitude / Interest score: {_format_number(magnitude, 3)} / {_format_number(score, 3)}")
        print("-" * 72)


if __name__ == "__main__":
    main()
