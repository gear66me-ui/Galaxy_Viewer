from __future__ import annotations

import json
import urllib.request
from google.colab import output
from IPython.display import Javascript, display

# VIEWER-47-1
# VIEWER-46 is the immutable UI baseline.
# BRIDGE-SEARCH-0012 is the immutable data engine.
VIEWER_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/8b3f3464c9401be0f6e7470487364939e1569545/VIEWER-46.py"
BRIDGE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/7e2653ffd5b4e4e3dc0f8bdc1eb0953ef5e0eff0/BRIDGE-SEARCH-0012.py"

with urllib.request.urlopen(VIEWER_URL, timeout=60) as response:
    viewer_source = response.read().decode("utf-8")
exec(compile(viewer_source, "VIEWER-46-immutable.py", "exec"), globals())

with urllib.request.urlopen(BRIDGE_URL, timeout=60) as response:
    bridge_source = response.read().decode("utf-8")
# Load the exact locked bridge functions without launching its standalone 20-object batch UI.
bridge_runtime_source = bridge_source.replace('\nnamespace["main"]()\n', '\n')
_bridge_module = {"__name__": "viewer47_locked_bridge12"}
exec(compile(bridge_runtime_source, "BRIDGE-SEARCH-0012-locked.py", "exec"), _bridge_module)
_bridge = _bridge_module["namespace"]


def _old_row_from_viewer(g: dict) -> dict:
    row = {field: "" for field in _bridge["OLD_FIELDS"]}
    row["Object"] = str(g.get("name") or "Catalog galaxy")
    row["ICRS coordinates"] = f'{float(g.get("ra")):.6f} {float(g.get("dec")):.6f}'
    row["Morphological type"] = str(g.get("morphology") or "")
    row["Angular size"] = str(g.get("angular_size") or "")
    row["Redshift (z) / Distance"] = str(g.get("redshift_distance") or "")
    row["Radial velocity"] = "" if g.get("velocity_kms") is None else f'{float(g.get("velocity_kms"))} km/s'
    row["Physical size"] = str(g.get("physical_size") or "")
    row["Magnitude"] = str(g.get("magnitude") or "")
    row["Galaxy age"] = str(g.get("galaxy_age") or "")
    return row


def viewer47_bridge_enrich(g):
    try:
        item = dict(g or {})
        primary = _old_row_from_viewer(item)
        first = _bridge["simbad_backup"](primary) if _bridge["needs_backup"](primary) else _bridge["blank_old_row"](primary)
        merged = _bridge["merge_old"](primary, first)
        second = _bridge["vizier_backup"](merged) if _bridge["needs_backup"](merged) else _bridge["blank_old_row"](primary)
        backup = _bridge["merge_old"](first, second)
        combined = _bridge["viewer_row"](primary, backup)
        item.update({
            "ok": True,
            "name": combined.get("Object", item.get("name")),
            "common_name": combined.get("Common name / nickname", ""),
            "alternate_names": combined.get("Alternate names", ""),
            "constellation": combined.get("Constellation", ""),
            "morphology": combined.get("Morphological type", ""),
            "redshift_distance": combined.get("Redshift (z) / Distance", ""),
            "angular_size": combined.get("Physical / angular size", ""),
            "physical_size": "",
            "magnitude": combined.get("Magnitudes", ""),
            "galaxy_age": combined.get("Galaxy age", ""),
            "velocity_kms": _bridge["first_number"](combined.get("Radial velocity", "")),
            "bridge_record": combined,
            "source": "BRIDGE-SEARCH-0012 locked primary + SIMBAD backup + VizieR backup + combined record",
        })
        return item
    except Exception as exc:
        return {"ok": False, "error": f"BRIDGE-SEARCH-0012 failed: {exc}"}

output.register_callback("viewer47.bridgeEnrich", viewer47_bridge_enrich)

display(Javascript(r'''
(() => {
  const KEY='galaxy-viewer-viewer47-record';
  const originalShow=window.viewer14ShowGalaxy;
  if(typeof originalShow!=='function') return;
  window.viewer47OriginalShowGalaxy=window.viewer47OriginalShowGalaxy||originalShow;

  function saveRecord(g){
    try{localStorage.setItem(KEY,JSON.stringify(g));window.viewer47CurrentRecord=g;}catch(_){ }
  }
  function loadRecord(){try{return JSON.parse(localStorage.getItem(KEY)||'null');}catch(_){return null;}}
  function renderBridgeRows(g){
    const r=g?.bridge_record;if(!r)return;
    const status=document.getElementById('viewer14Status');if(!status)return;
    const labels=['Object','Common name / nickname','Alternate names','Constellation','ICRS coordinates','Galaxy age','Redshift (z) / Distance','Morphological type','Physical / angular size','Radial velocity','Magnitudes'];
    status.innerHTML='<div class="fom-title">Galaxy Info</div><table><tbody>'+labels.map(label=>`<tr><th>${label}</th><td>${String(r[label]??'Not available')}</td></tr>`).join('')+'</tbody></table>';
  }
  window.viewer14ShowGalaxy=async function(g){
    let finalRecord=g;
    try{
      const response=await google.colab.kernel.invokeFunction('viewer47.bridgeEnrich',[g],{});
      const enriched=viewer14Result(response);
      if(enriched?.ok===true) finalRecord=enriched;
    }catch(error){viewer14Status('Bridge enrichment failed: '+String(error?.message||error));}
    window.viewer47OriginalShowGalaxy(finalRecord);
    renderBridgeRows(finalRecord);
    saveRecord(finalRecord);
  };
  const restore=()=>{const g=loadRecord();if(!g)return;window.viewer47OriginalShowGalaxy(g);renderBridgeRows(g);};
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)setTimeout(restore,120);});
  window.addEventListener('pageshow',()=>setTimeout(restore,120));
  setTimeout(restore,600);
  const title=()=>{const h=document.querySelector('#viewer14-root h3');if(h)h.textContent='Galaxy Viewer — VIEWER-47-1';};
  title();setInterval(title,500);
})();
'''))
