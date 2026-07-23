# BRIDGE-SEARCH-0012
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

BRIDGE_VERSION = "BRIDGE-SEARCH-0012"
BATCH_SIZE = 20
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/07902c7732514e46417e8362cb682fd5ea06d8e4/BRIDGE-SEARCH-0011.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0011"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0012"')
source = source.replace('root = "bridge_search_0011_viewer"', 'root = "bridge_search_0012_viewer"')

namespace = {"__name__": "bridge_search_0012_runtime"}
exec(compile(source, "BRIDGE-SEARCH-0012-base.py", "exec"), namespace)
namespace["BRIDGE_VERSION"] = BRIDGE_VERSION
namespace["BATCH_SIZE"] = BATCH_SIZE
namespace["OUTPUT_PATH"] = Path(f"/content/{BRIDGE_VERSION}_{BATCH_SIZE}_GALAXIES.xlsx")

_original_concise_age = namespace["concise_age"]
_original_physical_angular_size = namespace["physical_angular_size"]


def concise_age(value: str, morphology: str) -> str:
    age = _original_concise_age(value, morphology)
    return f"{age} — stars span a range of ages"


def physical_angular_size(angular_text: str, distance_text: str, morphology: str) -> str:
    text = _original_physical_angular_size(angular_text, distance_text, morphology)
    text = text.replace(" thousand ly", " thousand light-years")
    text = text.replace(" million ly", " million light-years")
    text = re.sub(
        r"\s*\((\d+(?:\.\d+)?)′\s*×\s*(\d+(?:\.\d+)?)′\)\s*$",
        r" / \1 × \2 arcminutes",
        text,
    )
    return text


namespace["concise_age"] = concise_age
namespace["physical_angular_size"] = physical_angular_size
namespace["main"]()
