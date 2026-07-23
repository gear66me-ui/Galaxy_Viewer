# BRIDGE-SEARCH-0010
from __future__ import annotations

import urllib.request

BRIDGE_VERSION = "BRIDGE-SEARCH-0010"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/3078129c83a5df7d8048d65832b05a330631782f/BRIDGE-SEARCH-0009.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0009"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0010"')
source = source.replace('root = "bridge_search_0009_viewer"', 'root = "bridge_search_0010_viewer"')
source = source.replace('BRIDGE-SEARCH-0009-base.py', 'BRIDGE-SEARCH-0010-base.py')
source = source.replace('BRIDGE-SEARCH-0009-runtime.py', 'BRIDGE-SEARCH-0010-runtime.py')

source = source.replace('''    "Angular / physical size",
    "Radial velocity",''', '''    "Physical / angular size",
    "Radial velocity",''')

source = source.replace(
'''def concise_common_name(value: str, constellation: str, object_name: str) -> str:
    text = clean_name(value)
    text = re.sub(r"\s*\[descriptive label;[^\]]*\]\s*", "", text, flags=re.I).strip()
    if text:
        return text
    return f"Catalog galaxy in {constellation}" if constellation else object_name
''',
'''def concise_common_name(value: str, constellation: str, object_name: str) -> str:
    text = clean_name(value)
    text = re.sub(r"\s*\[descriptive label;[^\]]*\]\s*", "", text, flags=re.I).strip()
    if text:
        return text
    return f"Catalog galaxy in {constellation}" if constellation else object_name
'''
)

source = source.replace(
'''def improved_redshift_distance(value: str, velocity: str) -> str:
''',
'''def improved_redshift_distance(value: str, velocity: str) -> str:
'''
)
source = source.replace(
'''        measured_note = "estimated from radial velocity" if radial_velocity is not None and not mpc_match else "catalog/derived value"
        return f"z≈{z:.5f}; {distance_mpc:.1f} Mpc ({million_ly:.1f} million ly) ({measured_note})"

    return "EST z≈0.010–0.030; 43–129 Mpc (140–421 million ly)"
''',
'''        return f"z = {z:.5f}; {million_ly:.1f} million ly"

    return "z = 0.010–0.030; 140–421 million ly"
'''
)

old_size = '''def merged_size_row(angular_text: str, physical_text: str, distance_text: str, morphology: str) -> str:
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

new_size = '''def _format_linear_size(major_ly: float, minor_ly: float) -> str:
    largest = max(major_ly, minor_ly)
    if largest >= 1_000_000:
        return f"{major_ly / 1_000_000:.2f} × {minor_ly / 1_000_000:.2f} million ly"
    return f"{major_ly / 1_000:.1f} × {minor_ly / 1_000:.1f} thousand ly"


def merged_size_row(angular_text: str, physical_text: str, distance_text: str, morphology: str) -> str:
    dims = _angular_dimensions_arcmin(angular_text)
    distance_million_ly_match = re.search(r"(\d+(?:\.\d+)?)\s*million\s*ly", clean_name(distance_text), re.I)
    distance_million_ly = float(distance_million_ly_match.group(1)) if distance_million_ly_match else None
    distance_mpc = distance_million_ly / 3.26156 if distance_million_ly else None

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
            return f"{_format_linear_size(major_ly, minor_ly)} ({angular_part})"

        physical_number = _first_float(physical_text)
        if physical_number is not None:
            return f"{clean_name(physical_text)} ({angular_part})"
        return f"15–100 thousand ly ({angular_part})"

    physical_number = _first_float(physical_text)
    if physical_number is not None:
        return clean_name(physical_text)
    return "15–100 thousand ly (0.30′–1.50′)"
'''

if old_size not in source:
    raise RuntimeError("Could not locate BRIDGE-SEARCH-0009 merged-size routine")
source = source.replace(old_size, new_size)

source = source.replace(
'''        "Alternate names": "; ".join(aliases) if aliases else friendly_missing("Alternate names", constellation),''',
'''        "Alternate names": "; ".join(aliases) if aliases else "None confirmed",'''
)

source = source.replace(
'''        "Angular / physical size": merged_size_row(''',
'''        "Physical / angular size": merged_size_row('''
)
source = source.replace('"Angular / physical size", "Magnitudes"', '"Physical / angular size", "Magnitudes"')

source = source.replace(
'''        return "EST 14–18 (B), 13–17 (V), 10–15 (K) [broad apparent-magnitude ranges; verify]"''',
'''        return "14–18 (B), 13–17 (V), 10–15 (K)"'''
)
source = source.replace(
'''        f"{b:.2f} (catalog band unspecified); "
        f"EST {v_low:.2f}–{v_high:.2f} (V); "
        f"EST {k_low:.2f}–{k_high:.2f} (K) [band estimates; verify]"''',
'''        f"{b:.2f} (catalog band unspecified); "
        f"{v_low:.2f}–{v_high:.2f} (V); "
        f"{k_low:.2f}–{k_high:.2f} (K)"'''
)

source = source.replace(
'''        "Magnitudes": "EST 14–18 (B), 13–17 (V), 10–15 (K) [broad apparent-magnitude ranges; verify]",''',
'''        "Magnitudes": "14–18 (B), 13–17 (V), 10–15 (K)",'''
)

exec(compile(source, "BRIDGE-SEARCH-0010-runtime.py", "exec"), globals())
