from __future__ import annotations

import urllib.request

# GALAXY-VIEWER-CORE-03
# Scope locked: CORE-02 unchanged except the Aladin reticle is disabled.

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/25bfd531692e4b936aa208993c62a313101a0542/GALAXY-VIEWER-CORE-02.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

old = "showReticle: true,"
new = "showReticle: false,"

if source.count(old) != 1:
    raise RuntimeError("CORE-03 integrity check failed: expected exactly one reticle setting")

source = source.replace("# GALAXY-VIEWER-CORE-02", "# GALAXY-VIEWER-CORE-03", 1)
source = source.replace(old, new, 1)

exec(compile(source, "GALAXY-VIEWER-CORE-03-runtime.py", "exec"))
