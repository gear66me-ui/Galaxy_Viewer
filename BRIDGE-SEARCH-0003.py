# BRIDGE-SEARCH-0003
from __future__ import annotations

import csv
import io
import json
import math
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from google.colab import userdata

BRIDGE_VERSION = "BRIDGE-SEARCH-0003"
BATCH_SIZE = 500
OWNER = "gear66me-ui"
REPOSITORY = "Galaxy_Viewer"
BRANCH = "sandbox"
REMOTE_FOLDER = "bridge-search"
TOKEN_SECRET = "GITHUB_TOKEN"
OUTPUT_PATH = Path(f"/content/{BRIDGE_VERSION}_{BATCH_SIZE}_GALAXIES.xlsx")
MAIN_CSV_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/sandbox/bridge-search/BRIDGE-SEARCH-0002_500_GALAXIES.csv"
FIELDS = [
    "Object", "Source catalog", "ICRS coordinates", "Galaxy age",
    "Redshift (z) / Distance", "Morphological type", "Angular size",
    "Radial velocity", "Physical size", "Magnitude", "Interest score",
    "Distance method", "Data source", "Data score"
]


def fetch_text(url: str, timeout: int = 120) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": f"GalaxyViewer/{BRIDGE_VERSION}"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def load_main() -> list[dict[str, str]]:
    rows = list(csv.DictReader(io.StringIO(fetch_text(MAIN_CSV_URL))))
    if len(rows) < BATCH_SIZE:
        raise RuntimeError(f"Expected {BATCH_SIZE} rows, received {len(rows)}")
    return [{field: str(row.get(field, "") or "") for field in FIELDS} for row in rows[:BATCH_SIZE]]


def parse_coords(text: str):
    try:
        p = re.split(r"[\s,]+", text.strip())
        ra, dec = float(p[0]), float(p[1])
        return (ra, dec) if math.isfinite(ra) and math.isfinite(dec) else None
    except Exception:
        return None


def missing(value: str) -> bool:
    t = str(value or "").strip().lower()
    return not t or "not available" in t or "not evaluated" in t or t == "unknown"


def tap_json(query: str, base: str) -> dict:
    params = urllib.parse.urlencode({"request": "doQuery", "lang": "adql", "format": "json", "query": query})
    return json.loads(fetch_text(f"{base}?{params}", timeout=90))


def first_record(payload: dict):
    data = payload.get("data") or []
    metadata = payload.get("metadata") or []
    if not data:
        return None
    names = [m.get("name") for m in metadata]
    return {names[i]: data[0][i] for i in range(min(len(names), len(data[0])))}


def simbad_backup(row: dict[str, str]) -> dict[str, str]:
    out = {field: "" for field in FIELDS}
    out["Object"] = row["Object"]
    out["ICRS coordinates"] = row["ICRS coordinates"]
    coords = parse_coords(row["ICRS coordinates"])
    if not coords:
        return out
    ra, dec = coords
    q = f"""SELECT TOP 1 main_id,ra,dec,otype,rvz_redshift,rvz_radvel,galdim_majaxis,galdim_minaxis
    FROM basic WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{dec},0.0083333333))
    ORDER BY DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',{ra},{dec}))"""
    try:
        rec = first_record(tap_json(q, "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"))
    except Exception:
        rec = None
    if not rec:
        return out
    out["Source catalog"] = "SIMBAD targeted backup"
    if rec.get("main_id"):
        out["Object"] = str(rec["main_id"]).strip()
    if rec.get("otype"):
        out["Morphological type"] = morphology_description(str(rec["otype"]))
    z = number(rec.get("rvz_redshift"))
    v = number(rec.get("rvz_radvel"))
    if z is not None:
        out["Redshift (z) / Distance"] = f"{z:.8f} / EST [{hubble_distance_mly(z):.2f} million ly; simple redshift distance]"
    if v is not None:
        out["Radial velocity"] = f"{v:,.1f} km/s"
    maj, min_ = number(rec.get("galdim_majaxis")), number(rec.get("galdim_minaxis"))
    if maj is not None:
        out["Angular size"] = f"{maj:.3f} × {min_:.3f} arcmin [SIMBAD]" if min_ is not None else f"{maj:.3f} arcmin [SIMBAD]"
    out["Galaxy age"] = age_from_morphology(out["Morphological type"])
    out["Data source"] = "SIMBAD targeted backup"
    return out


def vizier_backup(row: dict[str, str]) -> dict[str, str]:
    out = {field: "" for field in FIELDS}
    out["Object"] = row["Object"]
    out["ICRS coordinates"] = row["ICRS coordinates"]
    coords = parse_coords(row["ICRS coordinates"])
    if not coords:
        return out
    ra, dec = coords
    tables = [
        ("HECATE", '"J/MNRAS/506/1896/hecate"', "RAJ2000", "DEJ2000"),
        ("RC3", '"VII/155/rc3"', "RAJ2000", "DEJ2000"),
        ("HyperLEDA", '"VII/237/pgc"', "RAJ2000", "DEJ2000"),
    ]
    record = None
    source = ""
    for label, table, rac, decc in tables:
        q = f"SELECT TOP 1 * FROM {table} WHERE 1=CONTAINS(POINT('ICRS',{rac},{decc}),CIRCLE('ICRS',{ra},{dec},0.0083333333))"
        try:
            record = first_record(tap_json(q, "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"))
        except Exception:
            record = None
        if record:
            source = label
            break
    if not record:
        return out
    out["Source catalog"] = f"{source} targeted backup"
    out["Data source"] = f"{source} targeted backup"
    name = pick(record, "Name", "OName", "PGC", "NGC", "IC")
    if name:
        out["Object"] = str(name).strip()
    z = first_number(record, "z", "redshift")
    vel = first_number(record, "Vhel", "v", "cz", "HRV")
    if z is None and vel is not None:
        z = vel / 299792.458
    dist = first_number(record, "D", "Dist", "Dmean")
    if z is not None or dist is not None:
        dist_mly = dist * 3.26156 if dist is not None else hubble_distance_mly(z)
        ztxt = f"{z:.8f}" if z is not None else "Not available"
        out["Redshift (z) / Distance"] = f"{ztxt} / {dist_mly:.2f} million ly"
    if vel is not None:
        out["Radial velocity"] = f"{vel:,.1f} km/s"
    t = first_number(record, "T", "Ttype")
    if t is not None:
        out["Morphological type"] = t_description(t)
    maj = first_number(record, "Maj", "a", "D25")
    min_ = first_number(record, "Min", "b")
    if maj is not None:
        out["Angular size"] = f"{maj:.3f} × {min_:.3f} arcmin [{source}]" if min_ is not None else f"{maj:.3f} arcmin [{source}]"
    mag = first_number(record, "BT", "Bmag", "mag")
    if mag is not None:
        out["Magnitude"] = f"{mag:.3f} [catalog photometry; band verify]"
    out["Galaxy age"] = age_from_morphology(out["Morphological type"])
    return out


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except Exception:
        return None


def pick(record: dict, *names):
    norm = {str(k).lower().replace("_", ""): v for k, v in record.items()}
    for name in names:
        key = name.lower().replace("_", "")
        if key in norm and norm[key] not in (None, ""):
            return norm[key]
    return None


def first_number(record: dict, *names):
    return number(pick(record, *names))


def hubble_distance_mly(z: float) -> float:
    return (z * 299792.458 / 70.0) * 3.26156


def morphology_description(code: str) -> str:
    c = code.strip().upper()
    mapping = {
        "G": "Galaxy [SIMBAD G]", "GIG": "Galaxy in a group [SIMBAD GiG]",
        "GIP": "Galaxy in a pair [SIMBAD GiP]", "GIC": "Galaxy in a cluster [SIMBAD GiC]",
        "H2G": "Galaxy with prominent H II emission [SIMBAD H2G]", "AGN": "Active galaxy [SIMBAD AGN]",
        "AG?": "Possible active galaxy [SIMBAD AG?]", "LSB": "Low-surface-brightness galaxy [SIMBAD LSB]"
    }
    return mapping.get(c, f"Galaxy classification [{code.strip()}]")


def t_description(t: float) -> str:
    if t <= -4: label = "Elliptical galaxy"
    elif t <= -1: label = "Lenticular galaxy"
    elif t <= 1: label = "Early spiral / S0-a galaxy"
    elif t <= 3: label = "Sa–Sb spiral galaxy"
    elif t <= 5: label = "Sbc–Sc spiral galaxy"
    elif t <= 7: label = "Scd–Sd spiral galaxy"
    elif t <= 9: label = "Magellanic spiral galaxy"
    else: label = "Irregular galaxy"
    return f"{label} [de Vaucouleurs T={t:.1f}]"


def age_from_morphology(text: str) -> str:
    s = (text or "").lower()
    if "elliptical" in s or "lenticular" in s:
        return "EST [typically old-dominated stellar population, broadly 9–13 billion years; morphology-based]"
    if "irregular" in s or "h ii" in s or "active" in s:
        return "EST [mixed or younger stellar populations possible, broadly 1–10 billion years; morphology-based]"
    return "EST [broad 5–12 billion year stellar-population range; not an object-specific measurement]"


def numeric_tokens(text: str):
    return [float(x.replace(",", "")) for x in re.findall(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?", str(text or ""))]


def reconcile(field: str, values: list[str]) -> str:
    usable = [v.strip() for v in values if v and not missing(v)]
    if not usable:
        return "Not available"
    normalized = [re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", v)).strip().lower() for v in usable]
    for i, n in enumerate(normalized):
        if normalized.count(n) >= 2:
            return usable[i]
    if field in {"Redshift (z) / Distance", "Radial velocity", "Angular size", "Magnitude"} and len(usable) >= 2:
        nums = [numeric_tokens(v) for v in usable]
        firsts = [n[0] for n in nums if n]
        if len(firsts) >= 2:
            med = sorted(firsts)[len(firsts)//2]
            agreeing = [v for v, n in zip(usable, nums) if n and abs(n[0]-med) <= max(abs(med)*0.08, 0.0005)]
            if len(agreeing) >= 2:
                return agreeing[0]
            return f"{usable[0]} — UNVERIFIED [alternate: {usable[1]}]"
    return usable[0] if len(usable) == 1 else f"{usable[0]} — UNVERIFIED [alternate: {usable[1]}]"


def derive_size(row: dict[str, str]) -> str:
    if not missing(row.get("Physical size", "")):
        return row["Physical size"]
    angular = numeric_tokens(row.get("Angular size", ""))
    red_dist = numeric_tokens(row.get("Redshift (z) / Distance", ""))
    if not angular or len(red_dist) < 2:
        return "Not available"
    distance_mly = red_dist[-1]
    scale = distance_mly * 1_000_000 * math.pi / (180 * 60) / 1000
    major = angular[0] * scale
    if len(angular) > 1:
        return f"EST [{major:.1f} × {angular[1]*scale:.1f} thousand ly; derived from adopted distance and angular size]"
    return f"EST [{major:.1f} thousand ly; derived from adopted distance and angular size]"


def score_row(row: dict[str, str], three_pass_values: dict[str, list[str]]) -> str:
    core = ["ICRS coordinates", "Redshift (z) / Distance", "Morphological type", "Angular size", "Radial velocity", "Physical size", "Magnitude"]
    complete = sum(not missing(row.get(f, "")) for f in core) / len(core)
    agreement_hits = 0
    agreement_total = 0
    for f in core:
        vals = [v for v in three_pass_values[f] if v and not missing(v)]
        if len(vals) >= 2:
            agreement_total += 1
            norms = [re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", v)).strip().lower() for v in vals]
            if len(set(norms)) < len(norms):
                agreement_hits += 1
            elif f in {"Redshift (z) / Distance", "Radial velocity"}:
                nums = [numeric_tokens(v) for v in vals]
                x = [n[0] for n in nums if n]
                if len(x) >= 2 and (max(x)-min(x)) <= max(abs(sum(x)/len(x))*0.08, 0.0005):
                    agreement_hits += 1
    agreement = agreement_hits / agreement_total if agreement_total else 0
    provenance = min(1.0, sum(bool(v and not missing(v)) for v in three_pass_values["Data source"]) / 3)
    score = round(100 * (0.40*complete + 0.35*agreement + 0.25*provenance))
    return f"{score}% [completeness + independent agreement + provenance; verify critical values]"


def build_combined(main, backup1, backup2):
    combined = []
    for a, b, c in zip(main, backup1, backup2):
        vals = {field: [a.get(field, ""), b.get(field, ""), c.get(field, "")] for field in FIELDS}
        row = {field: reconcile(field, vals[field]) for field in FIELDS}
        row["Object"] = a.get("Object") or b.get("Object") or c.get("Object")
        row["Source catalog"] = "Multiple astronomy catalogs"
        row["Data source"] = "Multiple astronomy catalogs; verify critical values"
        row["Physical size"] = derive_size(row)
        row["Galaxy age"] = reconcile("Galaxy age", vals["Galaxy age"])
        row["Data score"] = score_row(row, vals)
        combined.append(row)
    return combined


def make_workbook(sheets: dict[str, list[dict[str, str]]]):
    try:
        from artifact_tool import Workbook, SpreadsheetFile
    except Exception as exc:
        raise RuntimeError("artifact_tool is required to generate the four-tab workbook") from exc
    wb = Workbook.create()
    header = {"fill": "#0B4F6C", "font": {"bold": True, "color": "#FFFFFF"}, "wrap_text": True}
    for name, rows in sheets.items():
        ws = wb.worksheets.add(name)
        matrix = [FIELDS] + [[row.get(field, "") for field in FIELDS] for row in rows]
        ws.get_range_by_indexes(0, 0, len(matrix), len(FIELDS)).values = matrix
        ws.get_range_by_indexes(0, 0, 1, len(FIELDS)).format = header
        ws.freeze_panes.freeze_rows(1)
        ws.get_range_by_indexes(0, 0, len(matrix), len(FIELDS)).format.wrap_text = True
        for col in range(len(FIELDS)):
            ws.get_range_by_indexes(0, col, len(matrix), 1).format.column_width = 22 if col not in (3, 4, 5, 8, 12, 13) else 34
        if name == "Combined":
            ws.get_range(f"N2:N{len(matrix)}").conditional_formats.add_color_scale({"minColor": "#FECACA", "midColor": "#FEF3C7", "maxColor": "#DCFCE7"})
    SpreadsheetFile.export_xlsx(wb).save(str(OUTPUT_PATH))


def upload(path: Path, token: str) -> str:
    try:
        from github import Auth, Github
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "PyGithub"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        from github import Auth, Github
    client = Github(auth=Auth.Token(token))
    repo = client.get_repo(f"{OWNER}/{REPOSITORY}")
    remote = f"{REMOTE_FOLDER}/{path.name}"
    content = path.read_bytes()
    try:
        existing = repo.get_contents(remote, ref=BRANCH)
        repo.update_file(remote, f"Update {path.name}", content, existing.sha, branch=BRANCH)
    except Exception as exc:
        if "404" not in str(exc):
            raise
        repo.create_file(remote, f"Upload {path.name}", content, branch=BRANCH)
    client.close()
    return f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{BRANCH}/{remote}"


def main():
    source_rows = load_main()
    backup1 = [simbad_backup(row) if any(missing(row.get(f, "")) for f in FIELDS[3:12]) else simbad_backup(row) for row in source_rows]
    backup2 = [vizier_backup({**row, **{k: (b.get(k) or row.get(k, "")) for k in FIELDS}}) for row, b in zip(source_rows, backup1)]
    combined = build_combined(source_rows, backup1, backup2)
    make_workbook({"Main": source_rows, "Backup 1": backup1, "Backup 2": backup2, "Combined": combined})
    token = userdata.get(TOKEN_SECRET)
    if not token:
        raise RuntimeError(f"Colab Secret {TOKEN_SECRET!r} is required")
    print(upload(OUTPUT_PATH, token))


if __name__ == "__main__":
    main()
