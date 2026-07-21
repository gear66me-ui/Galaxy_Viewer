# DEV-0002.py
# Development-only ipyaladin + SIMBAD search widget.
# Does not modify any released Galaxy Viewer file.

from __future__ import annotations

import sys
import subprocess
import importlib.util


def _ensure_package(import_name: str, pip_name: str) -> None:
    if importlib.util.find_spec(import_name) is None:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            pip_name,
        ])


_ensure_package("ipyaladin", "ipyaladin")
_ensure_package("astroquery", "astroquery")

import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
from ipyaladin import Aladin
from IPython.display import clear_output, display
import ipywidgets as widgets


DEFAULT_COORDINATES = "53.172576 -27.796392"
SEARCH_RADIUS = 30 * u.arcsec


# ------------------------------------------------------------
# SIMBAD CONFIGURATION
# ------------------------------------------------------------

simbad = Simbad()
simbad.ROW_LIMIT = 20

# Ask SIMBAD for the same categories useful to Galaxy Viewer.
# Unsupported fields are skipped individually so the widget remains usable
# if a SIMBAD mirror exposes a slightly different schema.
for field_name in (
    "otype",
    "sp_type",
    "velocity",
    "dimensions",
    "U",
    "B",
    "V",
    "R",
    "I",
):
    try:
        simbad.add_votable_fields(field_name)
    except Exception:
        pass


# ------------------------------------------------------------
# VIEWER
# ------------------------------------------------------------

aladin = Aladin(
    target=DEFAULT_COORDINATES,
    fov=0.08,
    survey="P/DSS2/color",
    height=520,
)


# ------------------------------------------------------------
# CONTROLS
# ------------------------------------------------------------

coordinate_input = widgets.Text(
    value=DEFAULT_COORDINATES,
    description="ICRS:",
    layout=widgets.Layout(width="430px"),
    style={"description_width": "55px"},
)

find_button = widgets.Button(
    description="Find Galaxy / Star",
    button_style="info",
    icon="search",
    layout=widgets.Layout(width="190px"),
)

clear_button = widgets.Button(
    description="Clear Results",
    icon="trash",
    layout=widgets.Layout(width="145px"),
)

status = widgets.HTML(
    value=(
        '<span style="color:#7FDBFF">'
        'Ready. Enter decimal ICRS coordinates and press Find Galaxy / Star.'
        '</span>'
    )
)

result_output = widgets.Output(
    layout=widgets.Layout(
        border="1px solid #0b526f",
        padding="8px",
        width="100%",
    )
)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------


def _parse_coordinates(text: str) -> SkyCoord:
    parts = text.replace(",", " ").split()
    if len(parts) != 2:
        raise ValueError("Use decimal ICRS format: RA Dec")

    return SkyCoord(
        ra=float(parts[0]) * u.deg,
        dec=float(parts[1]) * u.deg,
        frame="icrs",
    )


def _column_name(table, candidates):
    lookup = {name.casefold(): name for name in table.colnames}
    for candidate in candidates:
        found = lookup.get(candidate.casefold())
        if found:
            return found
    return None


def _format_value(value, digits=6):
    try:
        if value is None or getattr(value, "mask", False):
            return "Not available"
        numeric = float(value)
        return f"{numeric:.{digits}f}"
    except Exception:
        text = str(value).strip()
        return text if text and text != "--" else "Not available"


def _display_summary(table, center: SkyCoord) -> None:
    if table is None or len(table) == 0:
        print("No SIMBAD objects were returned within 30 arcseconds.")
        return

    first = table[0]

    name_col = _column_name(table, ["main_id", "MAIN_ID"])
    ra_col = _column_name(table, ["ra", "RA"])
    dec_col = _column_name(table, ["dec", "DEC"])
    type_col = _column_name(table, ["otype", "OTYPE"])
    z_col = _column_name(table, ["rvz_redshift", "RVZ_REDSHIFT"])
    vel_col = _column_name(table, ["rvz_radvel", "RVZ_RADVEL"])

    name = _format_value(first[name_col], 0) if name_col else "Not available"
    ra = _format_value(first[ra_col]) if ra_col else "Not available"
    dec = _format_value(first[dec_col]) if dec_col else "Not available"
    object_type = _format_value(first[type_col], 0) if type_col else "Not available"
    redshift = _format_value(first[z_col]) if z_col else "Not available"
    velocity = _format_value(first[vel_col], 3) if vel_col else "Not available"

    print("SIMBAD FIRST ROW")
    print("=" * 64)
    print("Object name :", name)
    print("RA          :", ra)
    print("Dec         :", dec)
    print("Object type :", object_type)
    print("Redshift    :", redshift)
    print("Velocity    :", velocity)
    print("Candidates  :", len(table))
    print("Radius      : 30 arcsec")
    print()
    print("Returned columns:")
    print(", ".join(table.colnames))
    print()

    # Compact table preview with the first ten rows.
    display(table[:10])


# ------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------


def _find_object(_button=None):
    find_button.disabled = True
    status.value = '<span style="color:#ffd166">Querying SIMBAD…</span>'

    try:
        center = _parse_coordinates(coordinate_input.value)

        # Recenter the viewer without replacing it.
        aladin.target = f"{center.ra.deg:.8f} {center.dec.deg:.8f}"

        table = simbad.query_region(center, radius=SEARCH_RADIUS)

        with result_output:
            clear_output(wait=True)

            if table is None or len(table) == 0:
                print("No SIMBAD objects were returned within 30 arcseconds.")
            else:
                # Overlay the returned catalog directly on Aladin.
                try:
                    aladin.add_table(table)
                except Exception as overlay_error:
                    print("Viewer overlay warning:", overlay_error)
                    print()

                _display_summary(table, center)

        count = 0 if table is None else len(table)
        status.value = (
            '<span style="color:#7FDBFF">'
            f'Complete — {count} SIMBAD candidate(s) returned.'
            '</span>'
        )

    except Exception as error:
        with result_output:
            clear_output(wait=True)
            print("SEARCH ERROR")
            print("=" * 64)
            print(type(error).__name__ + ":", error)

        status.value = (
            '<span style="color:#ff8a8a">'
            f'Search failed: {type(error).__name__}'
            '</span>'
        )

    finally:
        find_button.disabled = False


def _clear_results(_button=None):
    with result_output:
        clear_output(wait=True)

    status.value = (
        '<span style="color:#7FDBFF">'
        'Results cleared. Viewer position is preserved.'
        '</span>'
    )


find_button.on_click(_find_object)
clear_button.on_click(_clear_results)


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

header = widgets.HTML(
    value="""
    <div style="
        background:#000000;
        color:#7FDBFF;
        border:1px solid #0b4f6c;
        border-radius:8px;
        padding:10px 12px;
        font-family:Arial,Helvetica,sans-serif;
    ">
      <div style="color:#43d2ff;font-size:18px;font-weight:700;">
        DEV-0002 — ipyaladin + SIMBAD Search Test
      </div>
      <div style="color:#61b9d5;font-size:12px;margin-top:4px;">
        30-arcsecond SIMBAD cone search, first-row summary, returned-table preview,
        and direct catalog overlay on the viewer.
      </div>
    </div>
    """
)

controls = widgets.HBox(
    [coordinate_input, find_button, clear_button],
    layout=widgets.Layout(
        align_items="center",
        flex_flow="row wrap",
        gap="8px",
        width="100%",
    ),
)

app = widgets.VBox(
    [
        header,
        controls,
        status,
        aladin,
        result_output,
    ],
    layout=widgets.Layout(width="100%", gap="8px"),
)


display(app)
