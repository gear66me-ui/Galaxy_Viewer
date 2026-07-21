from IPython.display import HTML, display
import urllib.request
import json

try:
    from google.colab import output as colab_output
except Exception:
    colab_output = None

BASE_WRAPPER_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/GV-0054.py"

base_wrapper = urllib.request.urlopen(BASE_WRAPPER_URL, timeout=60).read().decode("utf-8")
exec_marker = "exec(source, globals())"
if base_wrapper.count(exec_marker) != 1:
    raise RuntimeError("GV-0054 execution marker not found exactly once")

scope = {}
exec(compile(base_wrapper.replace(exec_marker, "", 1), "GV-0054.py", "exec"), scope)
source = scope["source"]


def _gv0055_ned_query(ra, dec):
    payload = scope["_gv0054_ned_query"](ra, dec)
    return json.dumps(payload, ensure_ascii=False, allow_nan=False)


if colab_output is not None:
    colab_output.register_callback("gv0055.ned_query", _gv0055_ned_query)

replacements = [
    (
        "<h3>Galaxy Viewer — GV-0054</h3>",
        "<h3>Galaxy Viewer — GV-0055</h3>"
    ),
    (
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0054-state";',
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0055-state";'
    ),
    (
        '''async function probeNed(ra,dec) {
  if (!(window.google && google.colab && google.colab.kernel && typeof google.colab.kernel.invokeFunction === "function")) {
    throw new Error("Colab Python callback unavailable");
  }
  const result = await google.colab.kernel.invokeFunction("gv0054.ned_query", [ra, dec], {});
  let payload = result?.data?.["application/json"] ?? result?.data?.["text/plain"] ?? result;
  if (typeof payload === "string") {
    try { payload = JSON.parse(payload); } catch(err) {}
  }
  if (payload && Array.isArray(payload.rows)) return payload.rows;
  if (Array.isArray(payload)) return payload;
  return [];
}''',
        '''async function probeNed(ra,dec) {
  if (!(window.google && google.colab && google.colab.kernel && typeof google.colab.kernel.invokeFunction === "function")) {
    throw new Error("Colab Python callback unavailable");
  }
  const result = await google.colab.kernel.invokeFunction("gv0055.ned_query", [ra, dec], {});
  let payload = result?.data?.["application/json"] ?? result?.data?.["text/plain"] ?? result;
  for (let i=0; i<3 && typeof payload === "string"; i++) {
    const text = payload.trim();
    try {
      payload = JSON.parse(text);
      continue;
    } catch(err) {}
    if ((text.startsWith("'") && text.endsWith("'")) || (text.startsWith('"') && text.endsWith('"'))) {
      try {
        payload = JSON.parse(text.slice(1,-1).replace(/\\\\"/g,'"').replace(/\\\\n/g,'\\n'));
        continue;
      } catch(err) {}
    }
    break;
  }
  if (payload && Array.isArray(payload.rows)) return payload.rows;
  if (Array.isArray(payload)) return payload;
  throw new Error("NED callback returned no decodable rows");
}'''
    ),
    (
        '  const name = cleanId(obj.main_id || "Not available");',
        '  const name = `${cleanId(obj.main_id || "Not available")} — ${catalogName}`;'
    ),
    (
        '    setStatus("Search complete. GV-0054 used the first SIMBAD row and first NED row from the 6-arcsecond search window and restored the saved zoom level.");',
        '    setStatus("Search complete. GV-0055 used the first SIMBAD row and first NED row from the 6-arcsecond search window and restored the saved zoom level.");'
    ),
    (
        "GV-0054 preserves the current viewer position, selected survey, and zoom level when switching tabs. SIMBAD and NED use a 6-arcsecond search window. The Object figures of merit table lists SIMBAD row 1 first and NED row 1 second. NED is queried through the Colab Python kernel with the requested NED table parameters. All other GV-0051 behavior remains unchanged.",
        "GV-0055 preserves the current viewer position, selected survey, and zoom level when switching tabs. SIMBAD and NED use a 6-arcsecond search window. The Object figures of merit table lists the first SIMBAD match first and the first NED match second, with each catalog name shown beside its object name. NED callback decoding is corrected. All other GV-0054 behavior remains unchanged."
    )
]

for old, new in replacements:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"Patch target count was {count}, expected 1:\n{old[:160]}")
    source = source.replace(old, new, 1)

exec(source, globals())
