# GALAXY_FINDER-002.py
# Standalone Galaxy Finder module for Google Colab.
# Status bar + ten figures of merit + source links + debug output.
# Random Galaxy and SIMBAD-first behavior preserved from GALAXY_FINDER-001.py.

from __future__ import annotations

import json
import math
import random
import subprocess
import sys
from statistics import median
from typing import Any

try:
    from astroquery.simbad import Simbad
    from astroquery.ipac.ned import Ned
    from astropy.coordinates import SkyCoord
    import astropy.units as u
except ImportError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q", "astroquery", "astropy"
    ])
    from astroquery.simbad import Simbad
    from astroquery.ipac.ned import Ned
    from astropy.coordinates import SkyCoord
    import astropy.units as u

from google.colab import output as colab_output
from IPython.display import HTML, display

LAST_GALAXY: dict[str, Any] | None = None

RANDOM_GALAXY_NAMES = [
    "M 31", "M 33", "M 51", "M 63", "M 64", "M 65", "M 66",
    "M 74", "M 77", "M 81", "M 82", "M 83", "M 87", "M 94",
    "M 95", "M 96", "M 100", "M 101", "M 104", "M 106",
    "NGC 253", "NGC 300", "NGC 891", "NGC 1097", "NGC 1300",
    "NGC 1365", "NGC 2403", "NGC 2903", "NGC 3115", "NGC 3370",
    "NGC 3628", "NGC 4565", "NGC 4631", "NGC 4945", "NGC 5128",
    "NGC 5194", "NGC 6744", "NGC 6946", "NGC 7331", "IC 342",
]

simbad_client = Simbad()
simbad_client.TIMEOUT = 45

for field_name in [
    "otype", "ra", "dec", "dimensions", "mesdistance",
    "velocity", "rvz_redshift", "V", "morphtype",
]:
    try:
        simbad_client.add_votable_fields(field_name)
    except Exception:
        pass


def decode_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    return str(value).strip()


def parse_float(value: Any) -> float | None:
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def available_column_names(row: Any) -> list[str]:
    try:
        return list(row.colnames)
    except Exception:
        try:
            return list(row.keys())
        except Exception:
            return []


def safe_value(row: Any, names: list[str]) -> Any:
    columns = available_column_names(row)
    lookup = {str(column).lower(): column for column in columns}
    for name in names:
        real_name = lookup.get(name.lower())
        if real_name is None:
            continue
        try:
            value = row[real_name]
            if getattr(value, "mask", False):
                continue
        except Exception:
            continue
        text = decode_text(value)
        if text.lower() not in {"", "nan", "none", "--", "masked"}:
            return value
    return None


def find_column(row: Any, fragments: list[str]) -> Any:
    for column in available_column_names(row):
        lowered = str(column).lower()
        if not all(fragment.lower() in lowered for fragment in fragments):
            continue
        try:
            value = row[column]
            if getattr(value, "mask", False):
                continue
        except Exception:
            continue
        text = decode_text(value)
        if text.lower() not in {"", "nan", "none", "--", "masked"}:
            return value
    return None


def table_debug(table: Any, limit: int = 6) -> dict[str, Any]:
    if table is None:
        return {"rows": 0, "columns": [], "sample": []}
    columns = list(getattr(table, "colnames", []))
    sample = []
    try:
        for row in table[:limit]:
            sample.append({str(c): decode_text(row[c]) for c in columns})
    except Exception:
        pass
    return {"rows": len(table), "columns": columns, "sample": sample}


def get_coordinate_from_row(row: Any) -> tuple[float, float]:
    ra_value = safe_value(row, ["ra", "ra_d", "ra_deg", "ra_icrs"])
    dec_value = safe_value(row, ["dec", "dec_d", "dec_deg", "dec_icrs"])
    ra_float = parse_float(ra_value)
    dec_float = parse_float(dec_value)
    if ra_float is not None and dec_float is not None:
        return ra_float, dec_float
    coordinate = SkyCoord(
        f"{decode_text(ra_value)} {decode_text(dec_value)}",
        unit=(u.hourangle, u.deg),
        frame="icrs",
    )
    return float(coordinate.ra.deg), float(coordinate.dec.deg)


def extract_text(row: Any, names: list[str], fragments: list[str]) -> str:
    value = safe_value(row, names)
    if value is None:
        value = find_column(row, fragments)
    return decode_text(value) or "Not available"


def extract_object_type(row: Any) -> str:
    return extract_text(row, ["otype", "otype_3", "otype_s"], ["otype"])


def extract_morphology(row: Any) -> str:
    return extract_text(
        row,
        ["morphtype", "morph_type", "morphology", "morph"],
        ["morph"],
    )


def extract_dimension(row: Any) -> str:
    return extract_text(
        row,
        ["galdim_majaxis", "dim_majaxis", "dimensions_majaxis", "majaxis"],
        ["majaxis"],
    )


def extract_redshift(row: Any) -> str:
    return extract_text(row, ["rvz_redshift", "z_value", "redshift"], ["redshift"])


def extract_velocity(row: Any) -> str:
    value = safe_value(row, ["rvz_radvel", "rv_value", "velocity"])
    if value is None:
        value = find_column(row, ["radvel"])
    if value is None:
        value = find_column(row, ["velocity"])
    return decode_text(value) or "Not available"


def extract_v_magnitude(row: Any) -> str:
    return extract_text(row, ["flux_v", "v"], ["flux", "v"])


def calculate_fov(dimension_text: str) -> float:
    major_arcmin = parse_float(dimension_text)
    if major_arcmin is not None and major_arcmin > 0:
        return round(max(0.03, min(5.0, major_arcmin / 60.0 * 3.0)), 6)
    return 0.15


def row_to_galaxy(row: Any) -> dict[str, Any]:
    name = decode_text(safe_value(row, ["main_id", "mainid"]))
    if not name:
        name = decode_text(find_column(row, ["main", "id"]))
    if not name:
        raise RuntimeError("SIMBAD returned no object name.")
    ra_deg, dec_deg = get_coordinate_from_row(row)
    dimension_text = extract_dimension(row)
    return {
        "name": name,
        "ra": round(ra_deg, 8),
        "dec": round(dec_deg, 8),
        "fov": calculate_fov(dimension_text),
        "survey_id": "P/DSS2/color",
        "object_type": extract_object_type(row),
        "object_size": dimension_text,
    }


def find_random_galaxy() -> dict[str, Any]:
    candidates = list(RANDOM_GALAXY_NAMES)
    random.shuffle(candidates)
    errors = []
    for candidate_name in candidates:
        try:
            table = simbad_client.query_object(candidate_name)
            if table is None or len(table) == 0:
                errors.append(f"{candidate_name}: no rows")
                continue
            galaxy = row_to_galaxy(table[0])
            galaxy["requested_name"] = candidate_name
            return galaxy
        except Exception as exc:
            errors.append(f"{candidate_name}: {exc}")
    raise RuntimeError(
        "SIMBAD did not return any galaxy from the candidate list. "
        + " | ".join(errors[:5])
    )


def query_aliases(name: str) -> list[str]:
    aliases = []
    try:
        table = Simbad.query_objectids(name)
        if table is not None:
            for row in table:
                text = decode_text(safe_value(row, ["id", "identifier"]))
                if text and text not in aliases:
                    aliases.append(text)
    except Exception:
        pass
    return aliases[:20]


def constellation_name(ra: float, dec: float) -> str:
    try:
        return SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            frame="icrs",
        ).get_constellation(short_name=False)
    except Exception:
        return "Not available"


def query_ned(name: str) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    debug: dict[str, Any] = {}
    try:
        main = Ned.query_object(name)
        debug["main"] = table_debug(main)
    except Exception as exc:
        main = None
        debug["main_error"] = str(exc)

    extras: dict[str, Any] = {}
    for table_name in ["diameters", "redshifts", "photometry"]:
        try:
            table = Ned.get_table(name, table=table_name)
            extras[table_name] = table
            debug[table_name] = table_debug(table)
        except Exception as exc:
            extras[table_name] = None
            debug[f"{table_name}_error"] = str(exc)
    return main, extras, debug


def ned_main_value(main: Any, names: list[str]) -> str:
    if main is None or len(main) == 0:
        return ""
    return decode_text(safe_value(main[0], names))


def first_numeric(table: Any, hints: list[list[str]]) -> tuple[float | None, str]:
    if table is None:
        return None, ""
    columns = list(getattr(table, "colnames", []))
    for hint_set in hints:
        for column in columns:
            lowered = str(column).lower()
            if not all(h.lower() in lowered for h in hint_set):
                continue
            for row in table:
                number = parse_float(row[column])
                if number is not None and number > 0:
                    return number, str(column)
    return None, ""


def distance_candidates(row: Any) -> list[tuple[float, str, str]]:
    columns = available_column_names(row)
    result = []
    unit = ""
    for column in columns:
        lowered = str(column).lower()
        if "distance" in lowered and "unit" in lowered:
            unit = decode_text(row[column])
            break
    for column in columns:
        lowered = str(column).lower()
        if "distance" not in lowered:
            continue
        if any(token in lowered for token in ["bibcode", "error", "method", "unit"]):
            continue
        number = parse_float(row[column])
        if number is not None and number > 0:
            result.append((number, unit, f"SIMBAD:{column}"))
    return result


def to_mpc(value: float, unit: str) -> float | None:
    normalized = unit.strip().lower().replace(" ", "")
    if normalized in {"mpc", "megaparsec", "megaparsecs"}:
        return value
    if normalized in {"kpc", "kiloparsec", "kiloparsecs"}:
        return value / 1000.0
    if normalized in {"pc", "parsec", "parsecs"}:
        return value / 1_000_000.0
    if normalized in {"mly", "millionly"}:
        return value / 3.26156
    return None


def build_distance(row: Any, redshift_text: str) -> tuple[str, str]:
    mpc_values = []
    for value, unit, source in distance_candidates(row):
        converted = to_mpc(value, unit)
        if converted is not None:
            mpc_values.append((converted, source))
    if mpc_values:
        med_mpc = median([item[0] for item in mpc_values])
        return (
            f"{med_mpc * 3.26156:.3f} million ly ({med_mpc:.3f} Mpc)",
            f"Median of {len(mpc_values)} compatible SIMBAD direct-distance value(s).",
        )

    z = parse_float(redshift_text)
    if z is not None and z > 0.003:
        mpc = 299792.458 * z / 70.0
        return (
            f"~{mpc * 3.26156:.3f} million ly (~{mpc:.3f} Mpc)",
            "Approximate redshift distance using H0=70 km/s/Mpc; not applied to very local galaxies.",
        )
    return (
        "Not available",
        "No compatible direct distance returned; local redshift was not converted.",
    )


def build_diameter(
    angular_arcmin: float | None,
    distance_text: str,
    field_name: str,
) -> tuple[str, str]:
    if angular_arcmin is None:
        return "Not available", "No usable angular diameter was returned."

    mpc = None
    if "Mpc" in distance_text:
        try:
            mpc = float(
                distance_text.split("(")[1]
                .split("Mpc")[0]
                .replace("~", "")
                .strip()
            )
        except Exception:
            mpc = None

    if mpc is None:
        return (
            f"{angular_arcmin:.3f} arcmin",
            f"Angular major axis from {field_name}; physical size needs a compatible distance.",
        )

    radians = math.radians(angular_arcmin / 60.0)
    diameter_ly = mpc * 3_261_560.0 * radians
    return (
        f"~{diameter_ly:,.0f} light-years ({angular_arcmin:.3f} arcmin)",
        f"Calculated from angular major axis and displayed distance; field: {field_name}.",
    )


def source_links(name: str, ra: float, dec: float) -> list[dict[str, str]]:
    encoded = name.replace(" ", "+")
    return [
        {"label": "SIMBAD", "url": f"https://simbad.cds.unistra.fr/simbad/sim-basic?Ident={encoded}"},
        {"label": "NASA/IPAC NED", "url": f"https://ned.ipac.caltech.edu/byname?objname={encoded}"},
        {"label": "HyperLEDA", "url": f"http://leda.univ-lyon1.fr/ledacat.cgi?o={encoded}"},
        {"label": "VizieR", "url": f"https://vizier.cds.unistra.fr/viz-bin/VizieR?-c={ra}+{dec}&-c.rs=2"},
        {"label": "Aladin Lite", "url": f"https://aladin.cds.unistra.fr/AladinLite/?target={ra}%20{dec}&fov=0.2&survey=P%2FDSS2%2Fcolor"},
    ]


def random_galaxy_callback() -> str:
    global LAST_GALAXY
    try:
        galaxy = find_random_galaxy()
        LAST_GALAXY = galaxy
        result = {"ok": True, "source": "SIMBAD", "galaxy": galaxy}
    except Exception as exc:
        result = {"ok": False, "source": "SIMBAD", "error": str(exc)}
    return json.dumps(result, ensure_ascii=False)


def get_info_callback(
    name: str = "",
    ra: float | None = None,
    dec: float | None = None,
) -> str:
    global LAST_GALAXY
    try:
        if not name and LAST_GALAXY:
            name = str(LAST_GALAXY.get("name", ""))
        if ra is None and LAST_GALAXY:
            ra = float(LAST_GALAXY.get("ra"))
        if dec is None and LAST_GALAXY:
            dec = float(LAST_GALAXY.get("dec"))
        if not name:
            raise RuntimeError("Run Random Galaxy Test first.")

        simbad_table = None
        lookup_method = "SIMBAD object-name lookup"
        try:
            simbad_table = simbad_client.query_object(name)
        except Exception:
            simbad_table = None

        if simbad_table is None or len(simbad_table) == 0:
            if ra is None or dec is None:
                raise RuntimeError(
                    "SIMBAD name lookup failed and coordinates were unavailable."
                )
            lookup_method = "SIMBAD 30-arcsecond cone"
            coordinate = SkyCoord(
                ra=float(ra) * u.deg,
                dec=float(dec) * u.deg,
                frame="icrs",
            )
            simbad_table = simbad_client.query_region(
                coordinate,
                radius=30.0 * u.arcsec,
            )

        if simbad_table is None or len(simbad_table) == 0:
            raise RuntimeError("SIMBAD returned no matching object.")

        row = simbad_table[0]
        primary = row_to_galaxy(row)
        aliases = query_aliases(primary["name"])
        constellation = constellation_name(primary["ra"], primary["dec"])
        morphology = extract_morphology(row)
        redshift = extract_redshift(row)
        v_magnitude = extract_v_magnitude(row)

        ned_main, ned_extra, ned_debug = query_ned(primary["name"])

        if morphology == "Not available":
            morphology = ned_main_value(
                ned_main,
                ["Morphology", "Morphological Type", "Type"],
            ) or "Not available"

        if redshift == "Not available":
            redshift = ned_main_value(ned_main, ["Redshift", "z"]) or "Not available"

        if v_magnitude == "Not available":
            v_magnitude = ned_main_value(
                ned_main,
                ["Magnitude and Filter", "Magnitude"],
            ) or "Not available"

        distance_value, distance_note = build_distance(row, redshift)

        angular_major, diameter_field = first_numeric(
            ned_extra.get("diameters"),
            [["major", "axis"], ["diameter"]],
        )
        if angular_major is None:
            angular_major = parse_float(extract_dimension(row))
            if angular_major is not None:
                diameter_field = "SIMBAD major-axis field"

        diameter_value, diameter_note = build_diameter(
            angular_major,
            distance_value,
            diameter_field or "unknown field",
        )

        designations = ", ".join(aliases[:12]) or primary["name"]
        velocity = extract_velocity(row)

        rows = [
            {"parameter": "Common Designations", "value": designations, "notes": "SIMBAD cross-identifications.", "source": "SIMBAD"},
            {"parameter": "Constellation", "value": constellation, "notes": "Calculated from the SIMBAD ICRS position.", "source": "Astropy / IAU boundaries"},
            {"parameter": "Morphological Type", "value": morphology, "notes": "SIMBAD first; NED fallback.", "source": "SIMBAD / NED"},
            {"parameter": "Distance", "value": distance_value, "notes": distance_note, "source": "SIMBAD / derived fallback"},
            {"parameter": "Diameter / Size", "value": diameter_value, "notes": diameter_note, "source": "NED / SIMBAD"},
            {"parameter": "Total Stellar Mass", "value": "Not available", "notes": "No defensible stellar-mass value returned by this first-tier query.", "source": "SIMBAD / NED checked"},
            {"parameter": "Estimated Star Count", "value": "Not available", "notes": "Not inferred without a referenced stellar-mass estimate.", "source": "Not calculated"},
            {"parameter": "Redshift (z)", "value": redshift, "notes": f"SIMBAD radial velocity: {velocity} km/s" if velocity != "Not available" else "No radial velocity returned.", "source": "SIMBAD / NED"},
            {"parameter": "Apparent Magnitude", "value": f"V = {v_magnitude}" if v_magnitude != "Not available" else "Not available", "notes": "SIMBAD V-band first; NED fallback.", "source": "SIMBAD / NED"},
            {"parameter": "Estimated Stellar Age", "value": "Not available", "notes": "No referenced stellar-population age returned by this first-tier query.", "source": "SIMBAD / NED checked"},
        ]

        result = {
            "ok": True,
            "title": primary["name"],
            "summary": "SIMBAD-first figures of merit with NED supplementation.",
            "lookup_method": lookup_method,
            "primary": primary,
            "rows": rows,
            "links": source_links(primary["name"], primary["ra"], primary["dec"]),
            "debug": {
                "module": "GALAXY_FINDER-002.py",
                "lookup_method": lookup_method,
                "requested_name": name,
                "primary": primary,
                "simbad": table_debug(simbad_table),
                "simbad_alias_count": len(aliases),
                "ned": ned_debug,
                "figures_of_merit": rows,
            },
        }
    except Exception as exc:
        result = {
            "ok": False,
            "source": "SIMBAD / NED",
            "error": str(exc),
            "debug": {"module": "GALAXY_FINDER-002.py", "exception": repr(exc)},
        }
    return json.dumps(result, ensure_ascii=False)


colab_output.register_callback("catalogBridge.randomGalaxy", random_galaxy_callback)
colab_output.register_callback("catalogBridge.getInfo", get_info_callback)

bridge_html = r'''
<div id="catalog-bridge-root" style="max-width:1180px;margin:0 auto;padding:16px;background:#000;color:#7FDBFF;border:1px solid #137aa3;border-radius:10px;font-family:Arial,Helvetica,sans-serif;">
  <h3 style="margin:0 0 14px 0;color:#35c6ff;">GALAXY FINDER — 002</h3>

  <div style="display:flex;align-items:stretch;gap:10px;flex-wrap:wrap;">
    <button id="catalog-random-test" style="padding:12px 18px;background:#7b3fc6;color:#fff;border:0;border-radius:8px;font-weight:bold;cursor:pointer;">Random Galaxy Test</button>
    <button id="catalog-info-test" style="padding:12px 18px;background:#bd7015;color:#fff;border:0;border-radius:8px;font-weight:bold;cursor:pointer;">Get Info Test</button>
    <div id="catalog-bridge-status" style="flex:1 1 360px;min-height:22px;padding:11px 14px;background:#020b11;border:1px solid #0d668a;border-radius:7px;white-space:pre-wrap;font-family:monospace;color:#9be8ff;">READY — Press Random Galaxy Test.</div>
  </div>

  <div id="catalog-primary" style="margin-top:14px;padding:12px;background:#020b11;border:1px solid #0d668a;border-radius:7px;display:none;"></div>

  <div id="catalog-table-wrap" style="margin-top:14px;overflow-x:auto;display:none;">
    <table id="catalog-table" style="width:100%;border-collapse:collapse;background:#000;color:#b9edff;font-size:14px;">
      <thead>
        <tr style="background:#062033;color:#62d8ff;">
          <th style="padding:10px;border:1px solid #0d668a;text-align:left;">Parameter</th>
          <th style="padding:10px;border:1px solid #0d668a;text-align:left;">Value / Astronomical Data</th>
          <th style="padding:10px;border:1px solid #0d668a;text-align:left;">Notes / Reference</th>
          <th style="padding:10px;border:1px solid #0d668a;text-align:left;">Source</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>

  <div id="catalog-links" style="margin-top:14px;padding:12px;background:#020b11;border:1px solid #0d668a;border-radius:7px;display:none;"></div>
</div>

<div id="catalog-debug-cell" style="max-width:1180px;margin:12px auto 0 auto;padding:16px;background:#000;color:#b9edff;border:1px solid #0d668a;border-radius:10px;font-family:Arial,Helvetica,sans-serif;">
  <div style="color:#35c6ff;font-weight:bold;margin-bottom:10px;">CODE OUTPUT / DEBUG DUMP</div>
  <pre id="catalog-bridge-output" style="margin:0;padding:14px;max-height:650px;overflow:auto;background:#01070b;color:#b9edff;border:1px solid #0d668a;border-radius:7px;white-space:pre-wrap;">No query has run yet.</pre>
</div>

<script>
(() => {
  const status = document.getElementById("catalog-bridge-status");
  const output = document.getElementById("catalog-bridge-output");
  const randomButton = document.getElementById("catalog-random-test");
  const infoButton = document.getElementById("catalog-info-test");
  const primaryBox = document.getElementById("catalog-primary");
  const tableWrap = document.getElementById("catalog-table-wrap");
  const tableBody = document.querySelector("#catalog-table tbody");
  const linksBox = document.getElementById("catalog-links");
  let currentGalaxy = null;

  function parseColabValue(value) {
    if (value === null || value === undefined) return value;
    if (typeof value !== "string") return value;
    value = value.trim();
    if (value.length >= 2 && value.startsWith("'") && value.endsWith("'")) {
      value = value.slice(1, -1).replace(/\\'/g, "'").replace(/\\\\/g, "\\");
    }
    if (value.length >= 2 && value.startsWith('"') && value.endsWith('"')) {
      try { value = JSON.parse(value); } catch (_) {}
    }
    if (typeof value === "string") {
      try { return JSON.parse(value); } catch (_) { return value; }
    }
    return value;
  }

  function normalizeCallbackResponse(response) {
    if (!response) throw new Error("No callback response returned.");
    const data = response.data ?? response;
    if (data && typeof data === "object" && data.ok !== undefined) return data;
    if (data && typeof data === "object") {
      const value = data["application/json"] ?? data["text/plain"] ?? Object.values(data)[0];
      return parseColabValue(value);
    }
    return parseColabValue(data);
  }

  function setBusy(message) {
    status.textContent = "WORKING — " + message;
    status.style.color = "#ffe58a";
  }
  function setSuccess(message) {
    status.textContent = "SUCCESS — " + message;
    status.style.color = "#7dff9b";
  }
  function setFailure(message) {
    status.textContent = "FAILED — " + message;
    status.style.color = "#ff8f8f";
  }

  function renderRows(rows) {
    tableBody.innerHTML = "";
    (rows || []).forEach((row, index) => {
      const tr = document.createElement("tr");
      tr.style.background = index % 2 === 0 ? "#000" : "#03131d";
      [row.parameter, row.value, row.notes, row.source].forEach(value => {
        const td = document.createElement("td");
        td.textContent = value ?? "";
        td.style.padding = "10px";
        td.style.border = "1px solid #0d668a";
        td.style.verticalAlign = "top";
        tr.appendChild(td);
      });
      tableBody.appendChild(tr);
    });
    tableWrap.style.display = "block";
  }

  function renderLinks(links) {
    linksBox.innerHTML = '<div style="font-weight:bold;color:#35c6ff;margin-bottom:8px;">Research links</div>';
    (links || []).forEach(link => {
      const a = document.createElement("a");
      a.href = link.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = link.label;
      a.style.color = "#7FDBFF";
      a.style.marginRight = "16px";
      a.style.display = "inline-block";
      a.style.marginBottom = "6px";
      linksBox.appendChild(a);
    });
    linksBox.style.display = "block";
  }

  randomButton.onclick = async () => {
    randomButton.disabled = true;
    infoButton.disabled = true;
    setBusy("Selecting and confirming a galaxy through SIMBAD...");
    try {
      const response = await google.colab.kernel.invokeFunction(
        "catalogBridge.randomGalaxy", [], {}
      );
      const result = normalizeCallbackResponse(response);
      output.textContent = typeof result === "string" ? result : JSON.stringify(result, null, 2);
      if (!result || result.ok !== true) {
        throw new Error(result?.error || "Random catalog callback failed.");
      }
      currentGalaxy = result.galaxy;
      primaryBox.style.display = "block";
      primaryBox.textContent = currentGalaxy.name + " — ICRS " + currentGalaxy.ra + " " + currentGalaxy.dec + " — FOV " + currentGalaxy.fov;
      setSuccess("Random galaxy selected: " + currentGalaxy.name + ". Press Get Info Test.");
    } catch (error) {
      setFailure(String(error?.message || error));
    } finally {
      randomButton.disabled = false;
      infoButton.disabled = false;
    }
  };

  infoButton.onclick = async () => {
    if (!currentGalaxy) {
      setFailure("Run Random Galaxy Test first.");
      return;
    }
    randomButton.disabled = true;
    infoButton.disabled = true;
    setBusy("Querying SIMBAD first, then NED, and building 10 figures of merit...");
    try {
      const response = await google.colab.kernel.invokeFunction(
        "catalogBridge.getInfo",
        [currentGalaxy.name, currentGalaxy.ra, currentGalaxy.dec],
        {}
      );
      const result = normalizeCallbackResponse(response);
      output.textContent = JSON.stringify(result, null, 2);
      if (!result || result.ok !== true) {
        throw new Error(result?.error || "Get Info catalog callback failed.");
      }
      currentGalaxy = result.primary;
      primaryBox.style.display = "block";
      primaryBox.textContent = result.title + " — ICRS " + result.primary.ra + " " + result.primary.dec + " — " + result.summary;
      renderRows(result.rows);
      renderLinks(result.links);
      setSuccess(result.title + " — 10 figures of merit populated. Lookup: " + result.lookup_method);
    } catch (error) {
      setFailure(String(error?.message || error));
    } finally {
      randomButton.disabled = false;
      infoButton.disabled = false;
    }
  };
})();
</script>
'''

display(HTML(bridge_html))
