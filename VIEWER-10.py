from __future__ import annotations

import base64
import json
import urllib.request

VIEWER6_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/62096681b8b997d6f4b53fcd95bb1f6b94f7e3a4"

with urllib.request.urlopen(VIEWER6_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
wrapper = base64.b64decode(payload["content"]).decode("utf-8")

old_exec = 'exec(compile(source, "VIEWER-6.py", "exec"))'

insert = r'''
source = source.replace("Galaxy Viewer — VIEWER-6", "Galaxy Viewer — VIEWER-10", 1)

old_catalog_start = 'const VIEWER1_GALAXIES=['
old_catalog_end = '];\nconst VIEWER1_KEY="galaxy-viewer-viewer1-state";'
start_index = source.find(old_catalog_start)
end_index = source.find(old_catalog_end)
if start_index == -1 or end_index == -1 or end_index <= start_index:
    raise RuntimeError("VIEWER-10 fixed galaxy catalog block not found")
source = (
    source[:start_index]
    + 'const VIEWER1_KEY="galaxy-viewer-viewer1-state";'
    + source[end_index + len(old_catalog_end):]
)

old_pick = 'function viewer1PickRandom(){return VIEWER1_GALAXIES[Math.floor(Math.random()*VIEWER1_GALAXIES.length)]}'
new_pick = 'function viewer1PickRandom(){const ra=Math.random()*360;const dec=Math.asin((Math.random()*2)-1)*180/Math.PI;const fov=0.08+Math.random()*0.92;return{ra,dec,fov}}'
if source.count(old_pick) != 1:
    raise RuntimeError("VIEWER-10 random picker token not found exactly once")
source = source.replace(old_pick, new_pick, 1)

old_show = 'function viewer1ShowGalaxy(g,message="Random galaxy loaded"){document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;window.viewer1Aladin.setImageSurvey("P/DSS2/color");window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:"P/DSS2/color",fov:g.fov});viewer1Status(`${message}: ${g.name} | ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | FOV ${g.fov}°`)}'
new_show = 'function viewer1ShowGalaxy(g,message="Random survey image loaded"){const survey=viewer1Norm(document.getElementById("viewer1SurveySelect")?.value||viewer1Load().survey);document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;window.viewer1Aladin.setImageSurvey(survey);window.viewer1Aladin.gotoRaDec(g.ra,g.dec);const f=()=>{try{window.viewer1Aladin.setFoV(g.fov)}catch(e){}};f();setTimeout(f,150);setTimeout(f,500);viewer1Save({ra:g.ra,dec:g.dec,survey:survey,fov:g.fov});viewer1Status(`${message} | Random ICRS ${g.ra.toFixed(6)} ${g.dec.toFixed(6)} | Survey ${survey} | FOV ${g.fov.toFixed(3)}°`)}'
if source.count(old_show) != 1:
    raise RuntimeError("VIEWER-10 random image loader token not found exactly once")
source = source.replace(old_show, new_show, 1)

old_launch = '(async()=>{viewer1Setup();const g=viewer1PickRandom();document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;document.getElementById("viewer1SurveySelect").value="P/DSS2/color";await A.init;window.viewer1Aladin=A.aladin("#viewer1-aladin",{target:`${g.ra} ${g.dec}`,survey:"P/DSS2/color",fov:g.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});viewer1ShowGalaxy(g,"Launch galaxy")})().catch(e=>viewer1Status("Viewer initialization failed: "+e.message));'
new_launch = '(async()=>{viewer1Setup();const g=viewer1PickRandom();const survey=viewer1State0().survey;document.getElementById("viewer1CoordBox").value=`${g.ra.toFixed(6)} ${g.dec.toFixed(6)}`;document.getElementById("viewer1SurveySelect").value=survey;await A.init;window.viewer1Aladin=A.aladin("#viewer1-aladin",{target:`${g.ra} ${g.dec}`,survey:survey,fov:g.fov,cooFrame:"ICRS",showReticle:true,showZoomControl:true,showFullscreenControl:true,showLayersControl:true,showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true});viewer1ShowGalaxy(g,"Launch random survey image")})().catch(e=>viewer1Status("Viewer initialization failed: "+e.message));'
if source.count(old_launch) != 1:
    raise RuntimeError("VIEWER-10 launch token not found exactly once")
source = source.replace(old_launch, new_launch, 1)

old_random = 'function viewer1RandomGalaxy(){viewer1ShowGalaxy(viewer1PickRandom())}'
new_random = 'function viewer1RandomGalaxy(){viewer1Status("Loading a completely random live survey image from the web…");viewer1ShowGalaxy(viewer1PickRandom())}'
if source.count(old_random) != 1:
    raise RuntimeError("VIEWER-10 random button token not found exactly once")
source = source.replace(old_random, new_random, 1)

required = [
    'Random Galaxy',
    'viewer1RandomGalaxy()',
    'viewer1PickRandom()',
    'viewer1FetchCoords()',
    'viewer1FindGalaxy()',
    'viewer1SurveyMenu',
    'viewer1ChooseSurvey',
    'window.viewer1Aladin.setImageSurvey(id)',
    'Math.asin((Math.random()*2)-1)',
    'Random survey image loaded',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"VIEWER-10 required behavior missing: {token}")

if 'const VIEWER1_GALAXIES=[' in source:
    raise RuntimeError("VIEWER-10 fixed galaxy catalog was not removed")

exec(compile(source, "VIEWER-10.py", "exec"))
'''

if wrapper.count(old_exec) != 1:
    raise RuntimeError("VIEWER-10 VIEWER-6 execution token not found exactly once")
wrapper = wrapper.replace(old_exec, insert, 1)

compile(wrapper, "VIEWER-10-wrapper.py", "exec")
exec(compile(wrapper, "VIEWER-10-wrapper.py", "exec"))
