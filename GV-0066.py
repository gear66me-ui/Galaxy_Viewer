from __future__ import annotations

import ast
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/6174d6b976c20c2f9ff4a01a8fd34f4e80bdd459/GV-0066.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

bad_ned = '                ned_coord = SkyCoord(ned_ra * u.deg, ned_dec * u.deg, frame="icrs")\n                separations.append(center.separation(ned_coord).arcsec)\n                )'
good_ned = '                ned_coord = SkyCoord(ned_ra * u.deg, ned_dec * u.deg, frame="icrs")\n                separations.append(center.separation(ned_coord).arcsec)'
if source.count(bad_ned) != 1:
    raise RuntimeError("GV-0066-6 malformed NED block was not found exactly once.")
source = source.replace(bad_ned, good_ned, 1)

if source.count("Galaxy Viewer — GV-0066") != 1:
    raise RuntimeError("GV-0066-6 viewer title was not found exactly once.")
source = source.replace("Galaxy Viewer — GV-0066", "Galaxy Viewer — GV-0066-6", 1)

bridge_open = '<select id="surveySelect-gv0066" onchange="gv0066ChangeSurvey()">'
bridge_new = '<select id="surveySelect-gv0066" onchange="window.gv0066SurveyBridge(this.value)" style="display:block;width:100%;max-width:420px;margin-top:10px;padding:14px;font-size:18px;background:#000;color:#7FDBFF;border:2px solid #169ac7;border-radius:8px;pointer-events:auto;touch-action:manipulation;position:relative;z-index:99999">'
if source.count(bridge_open) != 1:
    raise RuntimeError("GV-0066-6 survey selector was not found exactly once.")
source = source.replace(bridge_open, bridge_new, 1)

bridge_js = "window.gv0066SurveyBridge=function(id){const select=document.getElementById('surveySelect-gv0066');if(select)select.value=id;gv0066Survey(id);save({survey:id});status('Loaded survey: '+id);};"
if source.count("</script>") != 1:
    raise RuntimeError("GV-0066-6 closing script tag was not found exactly once.")
source = source.replace("</script>", bridge_js + "</script>", 1)

ast.parse(source, filename="GV-0066-6-generated.py")
exec(compile(source, "GV-0066.py", "exec"))
