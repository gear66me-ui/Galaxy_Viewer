from __future__ import annotations

import base64
import json
import urllib.request

from google.colab import output
from IPython.display import Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

GV0055_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/bc0df8ddebb8a230a6709c51c893bbd67a228f2d"

with urllib.request.urlopen(GV0055_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))

source = base64.b64decode(payload["content"]).decode("utf-8")
source = source.replace("gv0055", "gv0067_1")
source = source.replace("GV-0055", "GV-0067-1")

required = [
    '<select id="surveySelect" onchange="changeSurvey()"></select>',
    'function changeSurvey()',
    'window.aladin.setImageSurvey(id)',
    'document.addEventListener("visibilitychange",()=>document.hidden?save():restore("Viewer restored from saved tab state."))',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"GV-0067-1 required GV-0055 dropdown behavior missing: {token}")

exec(compile(source, "GV-0067-1.py", "exec"))
