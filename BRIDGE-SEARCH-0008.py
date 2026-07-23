# BRIDGE-SEARCH-0008
from __future__ import annotations

import re
import urllib.request

BRIDGE_VERSION = "BRIDGE-SEARCH-0008"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a11cd0e8c36de202cdd046dd2493169d5344fd68/BRIDGE-SEARCH-0007.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0007"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0008"')

source = source.replace(
'''    "Physical size",
    "Magnitude",
    "Data source",
]''',
'''    "Physical size",
    "Magnitudes",
    "Magnitude guide",
]'''
)

source = source.replace(
'''        "Magnitude": "Observed galaxy; brightness estimates vary with filter, aperture, and catalog",
        "Data source": "Multiple astronomy catalogs and web-audit query; verify critical values",''',
'''        "Magnitudes": "EST 14–18 (B), 13–17 (V), 10–15 (K) [broad apparent-magnitude ranges; verify]",
        "Magnitude guide": "Lower magnitude numbers mean a brighter-looking galaxy; values depend on the observing filter.",'''
)

marker = '''def morphology_plain(value: str) -> str:
    text = clean_name(value)
    if not text or missing(text):
        return ""
    replacements = {
        "Galaxy [SIMBAD G]": "Galaxy; detailed morphology not specified [SIMBAD G]",
        "Galaxy classification [G]": "Galaxy; detailed morphology not specified [SIMBAD G]",
    }
    return replacements.get(text, text)
'''

helpers = r'''


def _first_float(text: str):
    match = re.search(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?", str(text or ""))
    if not match:
        return None
    try:
        return float(match.group(0).replace(",", ""))
    except Exception:
        return None


def labeled_magnitudes(*values: str) -> str:
    usable = [clean_name(v) for v in values if v and not missing(v)]
    measured = next((_first_float(v) for v in usable if _first_float(v) is not None), None)

    if measured is None:
        return "EST 14–18 (B), 13–17 (V), 10–15 (K) [broad apparent-magnitude ranges; verify]"

    b = measured
    v_low, v_high = b - 1.0, b - 0.3
    k_low, k_high = b - 4.2, b - 2.0
    return (
        f"{b:.2f} (catalog band); "
        f"EST {v_low:.2f}–{v_high:.2f} (V); "
        f"EST {k_low:.2f}–{k_high:.2f} (K) [band estimates; verify]"
    )


def mandatory_physical_size(row: dict[str, str]) -> str:
    current = clean_name(row.get("Physical size", ""))
    if current and not missing(current) and _first_float(current) is not None:
        return current

    derived = derive_size({
        "Angular size": row.get("Angular size", ""),
        "Redshift (z) / Distance": row.get("Redshift (z) / Distance", ""),
        "Physical size": "",
    })
    if derived and not missing(derived) and _first_float(derived) is not None:
        return derived

    morphology = clean_name(row.get("Morphological type", "")).lower()
    if "dwarf" in morphology:
        return "EST 3–15 thousand ly [broad dwarf-galaxy size range; verify]"
    if "elliptical" in morphology:
        return "EST 30–180 thousand ly [broad elliptical-galaxy size range; verify]"
    if "spiral" in morphology or "barred" in morphology:
        return "EST 25–120 thousand ly [broad spiral-galaxy size range; verify]"
    if "irregular" in morphology:
        return "EST 5–50 thousand ly [broad irregular-galaxy size range; verify]"
    return "EST 15–100 thousand ly [broad galaxy-size range; verify]"
'''

if marker not in source:
    raise RuntimeError("Could not locate morphology helper in BRIDGE-SEARCH-0007")
source = source.replace(marker, marker + helpers)

source = source.replace(
'''        "Physical size": choose("Physical size"),
        "Magnitude": choose("Magnitude"),
        "Data source": "Multiple astronomy catalogs; web-audit query supplied for manual verification",
    }
    if "awaits" in row["Physical size"].lower():
        old_shape = {
            "Angular size": row["Angular size"],
            "Redshift (z) / Distance": row["Redshift (z) / Distance"],
            "Physical size": "",
        }
        derived = derive_size(old_shape)
        if derived and not missing(derived):
            row["Physical size"] = derived
    return row''',
'''        "Physical size": choose("Physical size"),
        "Magnitudes": labeled_magnitudes(
            primary.get("Magnitude", ""),
            backup_a.get("Magnitude", ""),
            backup_b.get("Magnitude", ""),
        ),
        "Magnitude guide": "Lower magnitude numbers mean a brighter-looking galaxy; values depend on the observing filter.",
    }
    row["Physical size"] = mandatory_physical_size(row)
    return row'''
)

source = source.replace(
'''        for index, column in enumerate(columns, 1):
            width = 38 if column in {"Galaxy age", "Redshift (z) / Distance", "Morphological type", "Physical size", "Google search string", "Manual source notes"} else 24''',
'''        for index, column in enumerate(columns, 1):
            width = 38 if column in {"Galaxy age", "Redshift (z) / Distance", "Morphological type", "Physical size", "Magnitudes", "Magnitude guide", "Google search string", "Manual source notes"} else 24'''
)

source = source.replace('root = "bridge_search_0007_viewer"', 'root = "bridge_search_0008_viewer"')
source = source.replace('"Magnitude"', '"Magnitudes"')
source = source.replace('BRIDGE-SEARCH-0007-base.py', 'BRIDGE-SEARCH-0008-base.py')

exec(compile(source, "BRIDGE-SEARCH-0008-runtime.py", "exec"), globals())
