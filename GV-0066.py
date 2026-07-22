from __future__ import annotations

import ast
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a2c7ae2751da302c03e4442376f09ab5a6de84bf/GV-0066.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace("output.no_vertical_scroll()\n", "", 1)
source = source.replace('display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))\n', "", 1)

if source.count("Galaxy Viewer — GV-0066") != 1:
    raise RuntimeError("GV-0066-7 viewer title was not found exactly once.")
source = source.replace("Galaxy Viewer — GV-0066", "Galaxy Viewer — GV-0066-7", 1)

old_selector = '<select id="surveySelect" onchange="changeSurvey()"></select>'
new_selector = '''<select id="surveySelect" onchange="window.gv0066SurveyBridge(this.value)" style="display:block;width:100%;max-width:420px;margin-top:10px;padding:14px;font-size:18px;background:#000;color:#7FDBFF;border:2px solid #169ac7;border-radius:8px;pointer-events:auto;touch-action:manipulation;position:relative;z-index:99999">
<option value="CDS/P/HST/EPO">Hubble Outreach Color</option>
<option value="P/DSS2/color">DSS2 Color</option>
<option value="P/DSS2/red">DSS2 Red</option>
<option value="P/PanSTARRS/DR1/color-z-zg-g">Pan-STARRS DR1 Color</option>
<option value="P/DECaLS/DR5/color">DECaLS DR5 Color</option>
<option value="P/2MASS/color">2MASS Color</option>
<option value="P/GALEXGR6/AIS/color">GALEX GR6/7 Color</option>
</select>'''
if source.count(old_selector) != 1:
    raise RuntimeError("GV-0066-7 survey selector was not found exactly once.")
source = source.replace(old_selector, new_selector, 1)

bridge_js = "window.gv0066SurveyBridge=function(id){const s=document.getElementById('surveySelect');if(s)s.value=id;survey(id);save({survey:id});status('Loaded survey: '+id);};"
if source.count("</script>") != 1:
    raise RuntimeError("GV-0066-7 closing script tag was not found exactly once.")
source = source.replace("</script>", bridge_js + "</script>", 1)

ast.parse(source, filename="GV-0066-7-generated.py")
exec(compile(source, "GV-0066.py", "exec"))