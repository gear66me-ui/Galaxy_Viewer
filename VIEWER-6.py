from __future__ import annotations

import base64
import json
import urllib.request

VIEWER5_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/e0dd33220a6809556003435415990ecd193a9716"

with urllib.request.urlopen(VIEWER5_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
source = base64.b64decode(payload["content"]).decode("utf-8")

source = source.replace("Galaxy Viewer — VIEWER-5", "Galaxy Viewer — VIEWER-6", 1)

old_css = '#viewer1-root .status{margin-top:12px;padding:11px;background:#02080d;color:#8be0ff;border:1px solid #0d668a;border-radius:7px;font-family:monospace;white-space:pre-wrap}'
new_css = old_css + '#viewer1-root .survey-menu-wrap{position:relative;display:inline-block;min-width:290px}#viewer1-root .survey-menu-button{width:100%;text-align:left;background:#000;color:#7FDBFF;border:1px solid #169ac7;border-radius:8px;padding:12px;font-size:16px;font-weight:400}#viewer1-root .survey-menu{display:none;position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:999999;background:#000;border:1px solid #169ac7;border-radius:8px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.75)}#viewer1-root .survey-menu.open{display:block}#viewer1-root .survey-option{display:block;width:100%;text-align:left;background:#000;color:#7FDBFF;border:0;border-bottom:1px solid #0b526f;border-radius:0;padding:12px;font-size:16px;font-weight:400}#viewer1-root .survey-option:last-child{border-bottom:0}#viewer1-root .survey-option:active{background:#063047}'
if source.count(old_css) != 1:
    raise RuntimeError("VIEWER-6 status CSS token not found exactly once")
source = source.replace(old_css, new_css, 1)

old_select = '<label for="viewer1SurveySelect">Displayed survey:</label>\n<select id="viewer1SurveySelect" onchange="viewer1ChangeSurvey()"></select>'
new_select = '<label>Displayed survey:</label>\n<div class="survey-menu-wrap"><input type="hidden" id="viewer1SurveySelect"><button type="button" id="viewer1SurveyButton" class="survey-menu-button" onclick="viewer1ToggleSurveyMenu(event)">DSS2 Color ▾</button><div id="viewer1SurveyMenu" class="survey-menu"></div></div>'
if source.count(old_select) != 1:
    raise RuntimeError("VIEWER-6 native survey selector token not found exactly once")
source = source.replace(old_select, new_select, 1)

old_survey = 'function viewer1Survey(id){id=viewer1Norm(id);document.getElementById("viewer1SurveySelect").value=id;window.viewer1Aladin.setImageSurvey(id)}'
new_survey = 'function viewer1Survey(id){id=viewer1Norm(id);document.getElementById("viewer1SurveySelect").value=id;const item=VIEWER1_SURVEYS.find(s=>s.id===id);document.getElementById("viewer1SurveyButton").textContent=(item?item.name:id)+" ▾";window.viewer1Aladin.setImageSurvey(id)}'
if source.count(old_survey) != 1:
    raise RuntimeError("VIEWER-6 survey setter token not found exactly once")
source = source.replace(old_survey, new_survey, 1)

old_setup = 'function viewer1Setup(){document.getElementById("viewer1SurveySelect").innerHTML=VIEWER1_SURVEYS.map(s=>`<option value="${s.id}">${s.name}</option>`).join("")}'
new_setup = 'function viewer1Setup(){document.getElementById("viewer1SurveyMenu").innerHTML=VIEWER1_SURVEYS.map(s=>`<button type="button" class="survey-option" onclick="viewer1ChooseSurvey(\\\'${s.id}\\\',event)">${s.name}</button>`).join("")}function viewer1ToggleSurveyMenu(e){e.stopPropagation();document.getElementById("viewer1SurveyMenu").classList.toggle("open")}function viewer1ChooseSurvey(id,e){e.stopPropagation();viewer1Survey(id);viewer1Save({survey:id});document.getElementById("viewer1SurveyMenu").classList.remove("open");viewer1Status("Loaded survey: "+id)}document.addEventListener("click",()=>{const m=document.getElementById("viewer1SurveyMenu");if(m)m.classList.remove("open")})'
if source.count(old_setup) != 1:
    raise RuntimeError("VIEWER-6 setup token not found exactly once")
source = source.replace(old_setup, new_setup, 1)

old_change = 'function viewer1ChangeSurvey(){const id=viewer1Norm(document.getElementById("viewer1SurveySelect").value);viewer1Survey(id);viewer1Save({survey:id});viewer1Status("Loaded survey: "+id)}'
new_change = 'function viewer1ChangeSurvey(){const id=viewer1Norm(document.getElementById("viewer1SurveySelect").value);viewer1ChooseSurvey(id,{stopPropagation(){}})}'
if source.count(old_change) != 1:
    raise RuntimeError("VIEWER-6 changeSurvey token not found exactly once")
source = source.replace(old_change, new_change, 1)

required = [
    'Random Galaxy',
    'viewer1PickRandom()',
    'viewer1FetchCoords()',
    'viewer1FindGalaxy()',
    'viewer1SurveyMenu',
    'viewer1ChooseSurvey',
    'window.viewer1Aladin.setImageSurvey(id)',
]
for token in required:
    if token not in source:
        raise RuntimeError(f"VIEWER-6 required behavior missing: {token}")

exec(compile(source, "VIEWER-6.py", "exec"))
