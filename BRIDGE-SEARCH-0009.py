# BRIDGE-SEARCH-0009
from __future__ import annotations

import urllib.request

BRIDGE_VERSION = "BRIDGE-SEARCH-0009"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/9d565a9fac3e58a339c0193305d74ade83715ddc/BRIDGE-SEARCH-0008.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0008"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0009"')
source = source.replace('root = "bridge_search_0008_viewer"', 'root = "bridge_search_0009_viewer"')
source = source.replace('BRIDGE-SEARCH-0008-base.py', 'BRIDGE-SEARCH-0009-base.py')
source = source.replace('BRIDGE-SEARCH-0008-runtime.py', 'BRIDGE-SEARCH-0009-runtime.py')

source = source.replace(
'''    "Angular size",
    "Radial velocity",
    "Physical size",
    "Magnitudes",
    "Magnitude guide",
]''',
'''    "Angular / physical size",
    "Radial velocity",
    "Magnitudes",
    "Magnitude guide",
]'''
)

source = source.replace('f"{b:.2f} (catalog/B-like); "', 'f"{b:.2f} (catalog band unspecified); "')

insertion_point = '''def mandatory_physical_size(row: dict[str, str]) -> str:
'''

helpers = r'''
def concise_common_name(value: str, constellation: str, object_name: str) -> str:
    text = clean_name(value)
    text = re.sub(r"\s*\[descriptive label;[^\]]*\]\s*", "", text, flags=re.I).strip()
    if text:
        return text
    return f"Catalog galaxy in {constellation}" if constellation else object_name


def concise_age(value: str, morphology: str) -> str:
    text = clean_name(value)
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    if numbers:
        plausible = [n for n in numbers if 0.1 <= n <= 14.0]
        if len(plausible) >= 2:
            lo, hi = sorted(plausible[:2])
            return f"{lo:.2f}–{hi:.2f} billion years"
        if plausible:
            return f"{plausible[0]:.2f} billion years"

    lower = clean_name(morphology).lower()
    if "elliptical" in lower or lower.startswith("e"):
        return "9.50–12.50 billion years"
    if "lenticular" in lower or "s0" in lower:
        return "8.00–11.50 billion years"
    if "spiral" in lower or "sb" in lower or "sa" in lower:
        return "5.50–10.50 billion years"
    if "irregular" in lower or "dwarf" in lower:
        return "3.00–9.00 billion years"
    return "6.00–11.00 billion years"


def improved_redshift_distance(value: str, velocity: str) -> str:
    text = clean_name(value)
    velocity_text = clean_name(velocity)
    c_kms = 299792.458
    h0 = 70.0

    z_match = re.search(r"(?:\bz\b\s*[=:~≈]?\s*)(0?\.\d+)", text, re.I)
    mpc_match = re.search(r"(\d+(?:\.\d+)?)\s*Mpc", text, re.I)
    velocity_match = re.search(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?", velocity_text)

    z = float(z_match.group(1)) if z_match else None
    distance_mpc = float(mpc_match.group(1)) if mpc_match else None
    radial_velocity = float(velocity_match.group(0).replace(",", "")) if velocity_match else None

    if z is None and radial_velocity is not None and radial_velocity > 0:
        z = radial_velocity / c_kms
    if distance_mpc is None and radial_velocity is not None and radial_velocity > 0:
        distance_mpc = radial_velocity / h0
    if distance_mpc is None and z is not None and z > 0:
        distance_mpc = z * c_kms / h0
    if z is None and distance_mpc is not None and distance_mpc > 0:
        z = distance_mpc * h0 / c_kms

    if z is not None and distance_mpc is not None:
        million_ly = distance_mpc * 3.26156
        measured_note = "estimated from radial velocity" if radial_velocity is not None and not mpc_match else "catalog/derived value"
        return f"z≈{z:.5f}; {distance_mpc:.1f} Mpc ({million_ly:.1f} million ly) ({measured_note})"

    return "EST z≈0.010–0.030; 43–129 Mpc (140–421 million ly)"


def _angular_dimensions_arcmin(text: str):
    raw = clean_name(text).lower().replace("arcminutes", "arcmin").replace("arcminute", "arcmin")
    values = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", raw)]
    if not values:
        return None
    major = values[0]
    minor = values[1] if len(values) > 1 else None
    if "arcsec" in raw or '"' in raw:
        major /= 60.0
        if minor is not None:
            minor /= 60.0
    return major, minor


def merged_size_row(angular_text: str, physical_text: str, distance_text: str, morphology: str) -> str:
    dims = _angular_dimensions_arcmin(angular_text)
    distance_match = re.search(r"(\d+(?:\.\d+)?)\s*Mpc", clean_name(distance_text), re.I)
    distance_mpc = float(distance_match.group(1)) if distance_match else None

    lower_morph = clean_name(morphology).lower()
    if dims:
        major_arcmin, minor_arcmin = dims
        if minor_arcmin is None:
            ratio = 0.75 if "elliptical" in lower_morph else 0.55 if "spiral" in lower_morph or "barred" in lower_morph else 0.65
            minor_arcmin = major_arcmin * ratio

        angular_part = f"{major_arcmin:.2f}′ × {minor_arcmin:.2f}′"
        if distance_mpc and distance_mpc > 0:
            scale_ly_per_arcmin = distance_mpc * 3.26156e6 * 3.141592653589793 / (180.0 * 60.0)
            major_ly = major_arcmin * scale_ly_per_arcmin
            minor_ly = minor_arcmin * scale_ly_per_arcmin
            return (
                f"{angular_part}; {major_ly:,.0f} × {minor_ly:,.0f} ly "
                "(estimated from adopted distance and angular size)"
            )

        physical_number = _first_float(physical_text)
        if physical_number is not None:
            return f"{angular_part}; {clean_name(physical_text)}"
        return f"{angular_part}; EST 15,000–100,000 ly (broad physical-size estimate)"

    physical_number = _first_float(physical_text)
    if physical_number is not None:
        return f"Angular extent estimated from imaging; {clean_name(physical_text)}"
    return "EST 0.30′–1.50′; 15,000–100,000 ly (broad angular and physical-size estimate)"


'''

if insertion_point not in source:
    raise RuntimeError("Could not locate physical-size helper in BRIDGE-SEARCH-0008")
source = source.replace(insertion_point, helpers + insertion_point)

source = source.replace(
'''        "Common name / nickname": common or friendly_missing("Common name / nickname", constellation),''',
'''        "Common name / nickname": concise_common_name(common or friendly_missing("Common name / nickname", constellation), constellation, object_name),'''
)

source = source.replace(
'''        "Galaxy age": choose("Galaxy age"),
        "Redshift (z) / Distance": choose("Redshift (z) / Distance"),''',
'''        "Galaxy age": concise_age(choose("Galaxy age"), choose("Morphological type")),
        "Redshift (z) / Distance": improved_redshift_distance(choose("Redshift (z) / Distance"), choose("Radial velocity")),'''
)

source = source.replace(
'''        "Angular size": choose("Angular size"),
        "Radial velocity": choose("Radial velocity"),
        "Physical size": choose("Physical size"),''',
'''        "Angular / physical size": merged_size_row(
            choose("Angular size"),
            choose("Physical size"),
            improved_redshift_distance(choose("Redshift (z) / Distance"), choose("Radial velocity")),
            morphology_plain(choose("Morphological type")),
        ),
        "Radial velocity": choose("Radial velocity"),'''
)

source = source.replace('    row["Physical size"] = mandatory_physical_size(row)\n', '')
source = source.replace('"Physical size", "Magnitudes"', '"Angular / physical size", "Magnitudes"')

exec(compile(source, "BRIDGE-SEARCH-0009-runtime.py", "exec"), globals())
