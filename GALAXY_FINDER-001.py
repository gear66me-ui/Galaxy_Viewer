# GALAXY_FINDER-001.py
# Standalone Galaxy Finder module for Google Colab.
# Random Galaxy + SIMBAD information bridge.

from __future__ import annotations

import json
import random
import subprocess
import sys
from typing import Any

try:
    from astroquery.simbad import Simbad
    from astropy.coordinates import SkyCoord
    import astropy.units as u
except ImportError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "astroquery",
        "astropy",
    ])
    from astroquery.simbad import Simbad
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
    "otype",
    "ra",
    "dec",
    "dimensions",
    "mesdistance",
    "velocity",
    "rvz_redshift",
    "V",
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
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        try:
            return float(str(value).strip())
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


def safe_value(row: Any, possible_names: list[str]) -> Any:
    columns = available_column_names(row)
    lookup = {str(column).lower(): column for column in columns}

    for possible_name in possible_names:
        real_name = lookup.get(possible_name.lower())
        if real_name is None:
            continue
        try:
            value = row[real_name]
        except Exception:
            continue
        try:
            if getattr(value, "mask", False):
                continue
        except Exception:
            pass
        if value is None:
            continue
        text = decode_text(value)
        if text.lower() in {"", "nan", "none", "--", "masked"}:
            continue
        return value

    return None


def find_column_by_fragments(row: Any, fragments: list[str]) -> Any:
    for column in available_column_names(row):
        lowered = str(column).lower()
        if not all(fragment.lower() in lowered for fragment in fragments):
            continue
        try:
            value = row[column]
        except Exception:
            continue
        try:
            if getattr(value, "mask", False):
                continue
        except Exception:
            pass
        text = decode_text(value)
        if text.lower() not in {"", "nan", "none", "--", "masked"}:
            return value

    return None


def get_coordinate_from_row(row: Any) -> tuple[float, float]:
    ra_value = safe_value(row, ["ra", "ra_d", "ra_deg", "ra_icrs"])
    dec_value = safe_value(row, ["dec", "dec_d", "dec_deg", "dec_icrs"])

    ra_float = parse_float(ra_value)
    dec_float = parse_float(dec_value)

    if ra_float is not None and dec_float is not None:
        return float(ra_float), float(dec_float)

    ra_text = decode_text(ra_value)
    dec_text = decode_text(dec_value)

    if ra_text and dec_text:
        coordinate = SkyCoord(
            f"{ra_text} {dec_text}",
            unit=(u.hourangle, u.deg),
            frame="icrs",
        )
        return float(coordinate.ra.deg), float(coordinate.dec.deg)

    raise RuntimeError("SIMBAD returned no usable coordinates.")


def extract_object_type(row: Any) -> str:
    value = safe_value(row, ["otype", "otype_3", "otype_s"])
    if value is None:
        value = find_column_by_fragments(row, ["otype"])
    return decode_text(value) or "Not available"


def extract_dimension(row: Any) -> str:
    value = safe_value(row, [
        "galdim_majaxis",
        "dim_majaxis",
        "dimensions_majaxis",
        "majaxis",
    ])
    if value is None:
        value = find_column_by_fragments(row, ["majaxis"])
    return decode_text(value) or "Not available"


def extract_distance(row: Any) -> str:
    value = safe_value(row, [
        "mesdistance_distance",
        "distance_distance",
        "distance",
    ])
    if value is None:
        value = find_column_by_fragments(row, ["distance"])
    return decode_text(value) or "Not available"


def extract_redshift(row: Any) -> str:
    value = safe_value(row, ["rvz_redshift", "z_value", "redshift"])
    if value is None:
        value = find_column_by_fragments(row, ["redshift"])
    return decode_text(value) or "Not available"


def extract_velocity(row: Any) -> str:
    value = safe_value(row, ["rvz_radvel", "rv_value", "velocity"])
    if value is None:
        value = find_column_by_fragments(row, ["radvel"])
    if value is None:
        value = find_column_by_fragments(row, ["velocity"])
    return decode_text(value) or "Not available"


def extract_v_magnitude(row: Any) -> str:
    value = safe_value(row, ["flux_v", "v"])
    if value is None:
        value = find_column_by_fragments(row, ["flux", "v"])
    return decode_text(value) or "Not available"


def calculate_fov(dimension_text: str) -> float:
    try:
        major_arcmin = float(dimension_text)
        if major_arcmin > 0:
            return round(
                max(0.03, min(5.0, major_arcmin / 60.0 * 3.0)),
                6,
            )
    except Exception:
        pass
    return 0.15


def row_to_galaxy(row: Any) -> dict[str, Any]:
    name = decode_text(safe_value(row, ["main_id", "mainid"]))
    if not name:
        name = decode_text(find_column_by_fragments(row, ["main", "id"]))
    if not name:
        raise RuntimeError("SIMBAD returned no object name.")

    ra_deg, dec_deg = get_coordinate_from_row(row)
    dimension_text = extract_dimension(row)

    return {
        "name": name,
        "ra": round(float(ra_deg), 8),
        "dec": round(float(dec_deg), 8),
        "fov": calculate_fov(dimension_text),
        "survey_id": "P/DSS2/color",
        "object_type": extract_object_type(row),
        "object_size": dimension_text,
    }


def find_random_galaxy() -> dict[str, Any]:
    candidates = list(RANDOM_GALAXY_NAMES)
    random.shuffle(candidates)
    errors: list[str] = []

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


def random_galaxy_callback() -> str:
    global LAST_GALAXY

    try:
        galaxy = find_random_galaxy()
        LAST_GALAXY = galaxy
        result = {
            "ok": True,
            "source": "SIMBAD",
            "galaxy": galaxy,
        }
    except Exception as exc:
        result = {
            "ok": False,
            "source": "SIMBAD",
            "error": str(exc),
        }

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

        table = None
        lookup_method = "SIMBAD object-name lookup"

        try:
            table = simbad_client.query_object(name)
        except Exception:
            table = None

        if table is None or len(table) == 0:
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
            table = simbad_client.query_region(
                coordinate,
                radius=30.0 * u.arcsec,
            )

        if table is None or len(table) == 0:
            raise RuntimeError("SIMBAD returned no matching object.")

        row = table[0]
        primary = row_to_galaxy(row)

        rows = [
            {
                "parameter": "Object name",
                "value": primary["name"],
                "notes": "First returned SIMBAD row.",
                "source": "SIMBAD",
            },
            {
                "parameter": "ICRS coordinates",
                "value": f'{primary["ra"]:.8f} {primary["dec"]:.8f}',
                "notes": "Decimal degrees, ICRS.",
                "source": "SIMBAD",
            },
            {
                "parameter": "Object type",
                "value": primary.get("object_type", "Not available"),
                "notes": "",
                "source": "SIMBAD",
            },
            {
                "parameter": "Distance",
                "value": extract_distance(row),
                "notes": "",
                "source": "SIMBAD",
            },
            {
                "parameter": "Object size",
                "value": extract_dimension(row),
                "notes": "Major-axis field when available from SIMBAD.",
                "source": "SIMBAD",
            },
            {
                "parameter": "Redshift",
                "value": extract_redshift(row),
                "notes": "",
                "source": "SIMBAD",
            },
            {
                "parameter": "Radial velocity",
                "value": extract_velocity(row),
                "notes": "",
                "source": "SIMBAD",
            },
            {
                "parameter": "V magnitude",
                "value": extract_v_magnitude(row),
                "notes": "",
                "source": "SIMBAD",
            },
        ]

        result = {
            "ok": True,
            "title": primary["name"],
            "summary": (
                "Direct SIMBAD catalog result. "
                "No Gemini Search grounding used."
            ),
            "lookup_method": lookup_method,
            "primary": primary,
            "rows": rows,
        }
    except Exception as exc:
        result = {
            "ok": False,
            "source": "SIMBAD",
            "error": str(exc),
        }

    return json.dumps(result, ensure_ascii=False)


colab_output.register_callback(
    "catalogBridge.randomGalaxy",
    random_galaxy_callback,
)
colab_output.register_callback(
    "catalogBridge.getInfo",
    get_info_callback,
)

bridge_html = r'''
<div id="catalog-bridge-root" style="
    max-width:1100px;
    margin:0 auto;
    padding:16px;
    background:#000000;
    color:#7FDBFF;
    border:1px solid #137aa3;
    border-radius:10px;
    font-family:Arial,Helvetica,sans-serif;
">
    <h3 style="margin:0 0 14px 0;color:#35c6ff;">
        Independent Direct-Catalog Bridge Test
    </h3>

    <button id="catalog-random-test" style="
        padding:12px 18px;
        margin-right:10px;
        background:#7b3fc6;
        color:#ffffff;
        border:0;
        border-radius:8px;
        font-weight:bold;
        cursor:pointer;
    ">Random Galaxy Test</button>

    <button id="catalog-info-test" style="
        padding:12px 18px;
        background:#bd7015;
        color:#ffffff;
        border:0;
        border-radius:8px;
        font-weight:bold;
        cursor:pointer;
    ">Get Info Test</button>

    <div id="catalog-bridge-status" style="
        margin-top:14px;
        padding:12px;
        background:#020b11;
        border:1px solid #0d668a;
        border-radius:7px;
        white-space:pre-wrap;
        font-family:monospace;
    ">Bridge loaded. Press Random Galaxy Test.</div>

    <pre id="catalog-bridge-output" style="
        margin-top:14px;
        padding:14px;
        max-height:650px;
        overflow:auto;
        background:#01070b;
        color:#b9edff;
        border:1px solid #0d668a;
        border-radius:7px;
        white-space:pre-wrap;
    "></pre>
</div>

<script>
(() => {
    const status = document.getElementById("catalog-bridge-status");
    const output = document.getElementById("catalog-bridge-output");
    const randomButton = document.getElementById("catalog-random-test");
    const infoButton = document.getElementById("catalog-info-test");

    let currentGalaxy = null;

    function parseColabValue(value) {
        if (value === null || value === undefined) {
            return value;
        }

        if (typeof value !== "string") {
            return value;
        }

        value = value.trim();

        if (
            value.length >= 2 &&
            value.startsWith("'") &&
            value.endsWith("'")
        ) {
            value = value.slice(1, -1);
            value = value
                .replace(/\\'/g, "'")
                .replace(/\\\\/g, "\\");
        }

        if (
            value.length >= 2 &&
            value.startsWith('"') &&
            value.endsWith('"')
        ) {
            try {
                value = JSON.parse(value);
            } catch (_) {
            }
        }

        if (typeof value === "string") {
            try {
                return JSON.parse(value);
            } catch (_) {
                return value;
            }
        }

        return value;
    }

    function normalizeCallbackResponse(response) {
        if (!response) {
            throw new Error("No callback response returned.");
        }

        const data = response.data ?? response;

        if (
            data &&
            typeof data === "object" &&
            data.ok !== undefined
        ) {
            return data;
        }

        if (data && typeof data === "object") {
            const value =
                data["application/json"] ??
                data["text/plain"] ??
                Object.values(data)[0];

            return parseColabValue(value);
        }

        return parseColabValue(data);
    }

    randomButton.onclick = async () => {
        randomButton.disabled = true;
        status.textContent = "Calling catalogBridge.randomGalaxy...";

        try {
            const response = await google.colab.kernel.invokeFunction(
                "catalogBridge.randomGalaxy",
                [],
                {}
            );

            const result = normalizeCallbackResponse(response);

            output.textContent =
                typeof result === "string"
                ? result
                : JSON.stringify(result, null, 2);

            if (!result || result.ok !== true) {
                throw new Error(
                    result?.error ||
                    "Random catalog callback failed."
                );
            }

            currentGalaxy = result.galaxy;

            status.textContent =
                "RANDOM CATALOG BRIDGE SUCCESS\n" +
                currentGalaxy.name +
                "\nRA " + currentGalaxy.ra +
                "  DEC " + currentGalaxy.dec +
                "  FOV " + currentGalaxy.fov +
                "\nSource: " + result.source;
        } catch (error) {
            status.textContent =
                "RANDOM CATALOG BRIDGE FAILED\n" +
                String(error?.message || error);
        } finally {
            randomButton.disabled = false;
        }
    };

    infoButton.onclick = async () => {
        infoButton.disabled = true;

        if (!currentGalaxy) {
            status.textContent = "Run Random Galaxy Test first.";
            infoButton.disabled = false;
            return;
        }

        status.textContent = "Calling catalogBridge.getInfo...";

        try {
            const response = await google.colab.kernel.invokeFunction(
                "catalogBridge.getInfo",
                [
                    currentGalaxy.name,
                    currentGalaxy.ra,
                    currentGalaxy.dec
                ],
                {}
            );

            const result = normalizeCallbackResponse(response);

            output.textContent =
                typeof result === "string"
                ? result
                : JSON.stringify(result, null, 2);

            if (!result || result.ok !== true) {
                throw new Error(
                    result?.error ||
                    "Get Info catalog callback failed."
                );
            }

            status.textContent =
                "GET INFO CATALOG BRIDGE SUCCESS\n" +
                result.title +
                "\nLookup: " + result.lookup_method +
                "\nRows returned: " +
                (
                    Array.isArray(result.rows)
                    ? result.rows.length
                    : 0
                );
        } catch (error) {
            status.textContent =
                "GET INFO CATALOG BRIDGE FAILED\n" +
                String(error?.message || error);
        } finally {
            infoButton.disabled = false;
        }
    };
})();
</script>
'''

display(HTML(bridge_html))
