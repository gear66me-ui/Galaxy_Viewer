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
source = source.replace("Galaxy Viewer — VIEWER-6", "Galaxy Viewer — VIEWER-7-2", 1)

old_buttons = '<div class="controls">\n<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">\n<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>\n</div>'
new_buttons = '<div class="controls">\n<button class="fetch-btn" onclick="viewer1FetchCoords()">Fetch Coordinates</button>\n<input id="viewer1CoordBox" type="text" value="53.162500 -27.791667" style="min-width:280px">\n<button class="find-btn" onclick="viewer1FindGalaxy()">Find Galaxy / Star</button>\n</div>'
if source.count(old_buttons) != 1:
    raise RuntimeError("VIEWER-7-2 primary controls token not found exactly once")
source = source.replace(old_buttons, new_buttons, 1)

old_status = '<div id="viewer1Status" class="status">Viewer loading…</div>'
new_status = '<div id="viewer1Status" class="status">Viewer loading…</div>\n<div class="controls">\n<button class="random-btn" onclick="viewer1RandomGalaxy()">Random Galaxy</button>\n<input id="viewer1GalaxyName" type="text" value="" readonly style="min-width:360px" aria-label="Selected galaxy name">\n</div>'
if source.count(old_status) != 1:
    raise RuntimeError("VIEWER-7-2 status block token not found exactly once")
source = source.replace(old_status, new_status, 1)

old_show = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;window.viewer1Aladin.setImageSurvey("P/DSS2/color");window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:"P/DSS2/color",fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}'
new_show = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;document.getElementById("viewer1GalaxyName").value=g.name;window.viewer1Aladin.setImageSurvey("P/DSS2/color");window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:"P/DSS2/color",fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}'
if source.count(old_show) != 1:
    raise RuntimeError("VIEWER-7-2 random galaxy display token not found exactly once")
source = source.replace(old_show, new_show, 1)

required = [
    'viewer1SurveyMenu',
    'viewer1ChooseSurvey',
    'window.viewer1Aladin.setImageSurvey(id)',
    'id="viewer1GalaxyName"',
    'document.getElementById("viewer1GalaxyName").value=g.name',
    'viewer1FetchCoords()',
    'viewer1FindGalaxy()',
    'viewer1RandomGalaxy()',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"VIEWER-7-2 required behavior missing: {token}")

exec(compile(source, "VIEWER-7-2.py", "exec"))
"""

if wrapper.count(old_exec) != 1:
    raise RuntimeError("VIEWER-7-2 VIEWER-6 execution token not found exactly once")
wrapper = wrapper.replace(old_exec, insert, 1)

compile(wrapper, "VIEWER-7-2-wrapper.py", "exec")
exec(compile(wrapper, "VIEWER-7-2-wrapper.py", "exec"))
