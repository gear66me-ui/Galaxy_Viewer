from __future__ import annotations

import urllib.request

# GALAXY VIEWER ALADIN LOCK
# Immutable Aladin/viewer configuration. Do not edit.
LOCKED_VIEWER_COMMIT = "7faf2b22a47244e3fa1b74fdb7b6602d4758fd53"
LOCKED_VIEWER_FILE = "VIEWER-46-4.py"
BASE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    f"{LOCKED_VIEWER_COMMIT}/{LOCKED_VIEWER_FILE}"
)

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

exec(compile(source, "GALAXY-VIEWER-ALADIN-LOCK.py", "exec"))
