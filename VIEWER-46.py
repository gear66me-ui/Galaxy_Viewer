from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-46 — FINAL
# Locked corrected source: VIEWER-46-4 commit 7faf2b22a47244e3fa1b74fdb7b6602d4758fd53.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/7faf2b22a47244e3fa1b74fdb7b6602d4758fd53/VIEWER-46-4.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-46-corrected-final.py", "exec"))
