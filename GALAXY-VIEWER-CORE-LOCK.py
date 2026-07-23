from __future__ import annotations

import urllib.request

# GALAXY-VIEWER-CORE-LOCK
# Immutable dependency. Future modules must invoke this file and must not edit the core.
CORE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "541c518a8025889fd2900d07276523ab8df6cc9b/"
    "GALAXY-VIEWER-CORE-002.py"
)

with urllib.request.urlopen(CORE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

exec(compile(source, "GALAXY-VIEWER-CORE-002-LOCKED.py", "exec"))
