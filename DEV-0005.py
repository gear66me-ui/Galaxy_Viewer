from __future__ import annotations

import urllib.request

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "620354ce013ac86e51d56693d2596a757b17369a/DEV-0004.py"
)

with urllib.request.urlopen(SOURCE_URL, timeout=90) as response:
    source = response.read().decode("utf-8")

old_header = '''from IPython.display import Javascript, HTML, display
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

from __future__ import annotations
'''
new_header = '''from __future__ import annotations

from IPython.display import HTML, display
'''
if old_header not in source:
    raise RuntimeError("DEV-0005 header patch target not found")
source = source.replace(old_header, new_header, 1)

helper_anchor = '''def fetch_vizier(center):
'''
helper_code = '''def vizier_object_type(row):
    value = row_value(
        row,
        "otype", "ObjectType", "Object Type", "objType", "ObjType",
        "source_type", "SourceType", "class", "Class", "classification",
    )
    return clean(value) or "Not available"


def vizier_magnitude(row):
    preferred = (
        "Gmag", "phot_g_mean_mag", "gmag", "G", "Vmag", "Bmag",
        "Rmag", "Imag", "Jmag", "Hmag", "Kmag",
    )
    columns = {str(name).casefold(): name for name in row.colnames}
    for requested in preferred:
        actual = columns.get(requested.casefold())
        if actual is not None:
            value = clean(row[actual])
            if value is not None:
                return value, str(actual)

    for name in row.colnames:
        lowered = str(name).casefold()
        if "mag" not in lowered:
            continue
        if lowered.startswith(("e_", "o_", "n_", "q_")):
            continue
        if any(token in lowered for token in ("error", "err", "count", "number", "nobs", "obs")):
            continue
        value = clean(row[name])
        if value is not None:
            return value, str(name)
    return None, None


def fetch_vizier(center):
'''
if helper_anchor not in source:
    raise RuntimeError("DEV-0005 helper insertion target not found")
source = source.replace(helper_anchor, helper_code, 1)

old_mag = '''            mag_value, mag_column = first_matching_column(
                row,
                [lambda name: "mag" in name],
            )
'''
new_mag = '''            mag_value, mag_column = vizier_magnitude(row)
'''
if old_mag not in source:
    raise RuntimeError("DEV-0005 magnitude patch target not found")
source = source.replace(old_mag, new_mag, 1)

old_otype = '''                "otype": "VizieR catalog source",
'''
new_otype = '''                "otype": vizier_object_type(row),
'''
if old_otype not in source:
    raise RuntimeError("DEV-0005 object-type patch target not found")
source = source.replace(old_otype, new_otype, 1)

source = source.replace("DEV-0004", "DEV-0005")
compile(source, "DEV-0005.py", "exec")
exec(compile(source, "DEV-0005.py", "exec"))
