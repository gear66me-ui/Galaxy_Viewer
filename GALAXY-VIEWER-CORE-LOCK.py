from __future__ import annotations

import urllib.request

# GALAXY-VIEWER-CORE-LOCK
# Immutable dependency. Future modules must invoke this file and must not edit the core.
CORE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "d752629bc90b851dfbfefe147f06a6c815e2c767/"
    "GALAXY-VIEWER-CORE-001.py"
)

with urllib.request.urlopen(CORE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

exec(compile(source, "GALAXY-VIEWER-CORE-001-LOCKED.py", "exec"))
