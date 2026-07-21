from __future__ import annotations

import urllib.request

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "620354ce013ac86e51d56693d2596a757b17369a/DEV-0004.py"
)

with urllib.request.urlopen(SOURCE_URL, timeout=90) as response:
    source = response.read().decode("utf-8")

old = '''from IPython.display import Javascript, HTML, display
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

from __future__ import annotations
'''
new = '''from __future__ import annotations

from IPython.display import HTML, display
'''

if old not in source:
    raise RuntimeError("DEV-0004 import-order patch target not found")

source = source.replace(old, new, 1)
compile(source, "DEV-0004.py", "exec")
exec(compile(source, "DEV-0004.py", "exec"))
