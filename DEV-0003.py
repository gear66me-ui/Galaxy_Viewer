from __future__ import annotations

import urllib.request

BASE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "bf94c61266134f78cf84d33ddbea78fd36814692/DEV-0003.py"
)

with urllib.request.urlopen(BASE_URL, timeout=90) as response:
    source = response.read().decode("utf-8")

old = '''        object_coords = SkyCoord(table[ra_column], table[dec_column], unit=(u.deg, u.deg), frame="icrs")'''
new = '''        try:
            object_coords = SkyCoord(table[ra_column], table[dec_column], frame="icrs")
        except Exception:
            object_coords = SkyCoord(
                [number(value) for value in table[ra_column]],
                [number(value) for value in table[dec_column]],
                unit=(u.deg, u.deg),
                frame="icrs",
            )'''

if old not in source:
    raise RuntimeError("DEV-0003 patch target not found; original source was not modified.")

source = source.replace(old, new, 1)
exec(compile(source, "DEV-0003.py", "exec"))
