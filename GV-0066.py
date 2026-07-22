from __future__ import annotations

import ast
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/6174d6b976c20c2f9ff4a01a8fd34f4e80bdd459/GV-0066.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    wrapper = response.read().decode("utf-8")

bad_ned = '''                ned_coord = SkyCoord(ned_ra * u.deg, ned_dec * u.deg, frame="icrs")
                separations.append(center.separation(ned_coord).arcsec)
                )'''
good_ned = '''                ned_coord = SkyCoord(ned_ra * u.deg, ned_dec * u.deg, frame="icrs")
                separations.append(center.separation(ned_coord).arcsec)'''
if wrapper.count(bad_ned) != 1:
    raise RuntimeError("GV-0066-5 malformed NED block was not found exactly once.")
wrapper = wrapper.replace(bad_ned, good_ned, 1)

old_exec = 'exec(compile(source, "GV-0066.py", "exec"))'
bridge_js_literal = repr(
    "window.gv0066SurveyBridge=function(id){"
    "const select=document.getElementById('surveySelect-gv0066');"
    "if(select)select.value=id;"
    "gv0066Survey(id);"
    "save({survey:id});"
    "status('Loaded survey: '+id);"
    "};"
)
bridge_patch = (
    "# GV-0066-5: verified native Colab/Android select bridge.\n"
    "source = source.replace('Galaxy Viewer — GV-0066', 'Galaxy Viewer — GV-0066-5', 1)\n"
    "bridge_open = '<select id=\"surveySelect-gv0066\" onchange=\"gv0066ChangeSurvey()\">'\n"
    "bridge_new = '<select id=\"surveySelect-gv0066\" onchange=\"window.gv0066SurveyBridge(this.value)\" style=\"display:block;width:100%;max-width:420px;margin-top:10px;padding:14px;font-size:18px;background:#000;color:#7FDBFF;border:2px solid #169ac7;border-radius:8px;pointer-events:auto;touch-action:manipulation;position:relative;z-index:99999\">'\n"
    "if source.count(bridge_open) != 1:\n"
    "    raise RuntimeError('GV-0066-5 survey bridge selector was not found exactly once.')\n"
    "source = source.replace(bridge_open, bridge_new, 1)\n"
    f"bridge_js = {bridge_js_literal}\n"
    "if source.count('</script>') != 1:\n"
    "    raise RuntimeError('GV-0066-5 closing script tag was not found exactly once.')\n"
    "source = source.replace('</script>', bridge_js + '</script>', 1)\n"
    "exec(compile(source, 'GV-0066.py', 'exec'))"
)

if wrapper.count(old_exec) != 1:
    raise RuntimeError("GV-0066-5 base execution line was not found exactly once.")
wrapper = wrapper.replace(old_exec, bridge_patch, 1)

ast.parse(wrapper, filename="GV-0066-5-generated-wrapper.py")
exec(compile(wrapper, "GV-0066-5-generated-wrapper.py", "exec"))
