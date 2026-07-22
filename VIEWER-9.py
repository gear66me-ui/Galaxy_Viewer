from __future__ import annotations

import base64
import json
import urllib.request

VIEWER6_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/62096681b8b997d6f4b53fcd95bb1f6b94f7e3a4"

with urllib.request.urlopen(VIEWER6_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
wrapper = base64.b64decode(payload["content"]).decode("utf-8")

old_exec = 'exec(compile(source, "VIEWER-6.py", "exec"))'

insert = r"""
source = source.replace("Galaxy Viewer — VIEWER-6", "Galaxy Viewer — VIEWER-9", 1)

old_buttons = '<div class="controls">\n<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">\n<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>\n</div>'
new_buttons = '<div class="controls">\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">\n<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>\n</div>'
if source.count(old_buttons) != 1:
    raise RuntimeError("VIEWER-9 controls token not found exactly once")
source = source.replace(old_buttons, new_buttons, 1)

required = [
    'viewer1SurveyMenu',
    'viewer1ChooseSurvey',
    'window.viewer1Aladin.setImageSurvey(id)',
    'viewer1FetchCoords()',
    'viewer1FindGalaxy()',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"VIEWER-9 required behavior missing: {token}")

if '<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>' in source:
    raise RuntimeError("VIEWER-9 random galaxy row was not removed")

exec(compile(source, "VIEWER-9.py", "exec"))
"""

if wrapper.count(old_exec) != 1:
    raise RuntimeError("VIEWER-9 VIEWER-6 execution token not found exactly once")
wrapper = wrapper.replace(old_exec, insert, 1)

compile(wrapper, "VIEWER-9-wrapper.py", "exec")
exec(compile(wrapper, "VIEWER-9-wrapper.py", "exec"))
