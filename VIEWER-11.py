from __future__ import annotations

import urllib.request

BROKEN_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/b09311d3c9baac98ea98771c4ca2ee0141371551/VIEWER-11.py"

with urllib.request.urlopen(BROKEN_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace("insert = r'''", 'insert = r"""', 1)
source = source.replace("\n'''\n\nif wrapper.count(old_exec)", '\n"""\n\nif wrapper.count(old_exec)', 1)

compile(source, "VIEWER-11-repaired.py", "exec")
exec(compile(source, "VIEWER-11-repaired.py", "exec"))
