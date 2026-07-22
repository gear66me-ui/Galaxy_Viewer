from __future__ import annotations

import urllib.request

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/6174d6b976c20c2f9ff4a01a8fd34f4e80bdd459/GV-0066.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    wrapper = response.read().decode("utf-8")

# GV-0066-3: repair the malformed GV-0066-1 Python wrapper before compiling it.
malformed_ned = '''                separations.append(center.separation(ned_coord).arcsec)
                )
        table["_gv_sep"] = separations'''
repaired_ned = '''                separations.append(center.separation(ned_coord).arcsec)
        table["_gv_sep"] = separations'''
if wrapper.count(malformed_ned) != 1:
    raise RuntimeError("GV-0066-3 malformed NED wrapper line was not found exactly once.")
wrapper = wrapper.replace(malformed_ned, repaired_ned, 1)

old_exec = 'exec(compile(source, "GV-0066.py", "exec"))'
bridge_patch = r'''
# GV-0066-3: use the verified native Colab/Android select bridge.
bridge_open = '<select id="surveySelect-gv0066" onchange="gv0066ChangeSurvey()">'
bridge_new = '<select id="surveySelect-gv0066" onchange="window.gv0066SurveyBridge(this.value)" style="display:block;width:100%;max-width:420px;margin-top:10px;padding:14px;font-size:18px;background:#000;color:#7FDBFF;border:2px solid #169ac7;border-radius:8px;pointer-events:auto;touch-action:manipulation;position:relative;z-index:99999">'
if source.count(bridge_open) != 1:
    raise RuntimeError("GV-0066-3 survey bridge selector was not found exactly once.")
source = source.replace(bridge_open, bridge_new, 1)

bridge_js = '''
window.gv0066SurveyBridge = function(id) {
    const select = document.getElementById("surveySelect-gv0066");
    if (select) select.value = id;
    gv0066Survey(id);
    save({survey:id});
    status("Loaded survey: " + id);
};
'''
if source.count('</script>') != 1:
    raise RuntimeError("GV-0066-3 closing script tag was not found exactly once.")
source = source.replace('</script>', bridge_js + '</script>', 1)

exec(compile(source, "GV-0066.py", "exec"))
'''

if wrapper.count(old_exec) != 1:
    raise RuntimeError("GV-0066-3 base execution line was not found exactly once.")
wrapper = wrapper.replace(old_exec, bridge_patch, 1)

exec(compile(wrapper, "GV-0066-3-wrapper.py", "exec"))
