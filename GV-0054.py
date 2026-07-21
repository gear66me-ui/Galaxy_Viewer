from IPython.display import HTML, display
import urllib.request
import json
import math
import re

import pandas as pd
import requests

try:
    from google.colab import output as colab_output
except Exception:
    colab_output = None

BASE_WRAPPER_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0051.py"


def _gv0054_clean(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    text = re.sub(r"\s+", " ", str(value)).strip()
    if not text or text.lower() in {"nan", "none", "..."}:
        return None
    return text


def _gv0054_number(value):
    text = _gv0054_clean(value)
    if text is None:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        number = float(match.group(0))
        return number if math.isfinite(number) else None
    except Exception:
        return None


def _gv0054_ra_degrees(value):
    text = _gv0054_clean(value)
    if text is None:
        return None
    direct = _gv0054_number(text)
    if direct is not None and not re.search(r"[hms:]", text, re.I):
        return direct
    match = re.search(r"(\d+)\s*[h:]\s*(\d+)\s*[m:]\s*([\d.]+)", text, re.I)
    if not match:
        return None
    return 15.0 * (float(match.group(1)) + float(match.group(2)) / 60.0 + float(match.group(3)) / 3600.0)


def _gv0054_dec_degrees(value):
    text = _gv0054_clean(value)
    if text is None:
        return None
    direct = _gv0054_number(text)
    if direct is not None and not re.search(r"[dms:]", text, re.I):
        return direct
    match = re.search(r"([+-]?)\s*(\d+)\s*[d:]\s*(\d+)\s*[m:]\s*([\d.]+)", text, re.I)
    if not match:
        return None
    sign = -1.0 if match.group(1) == "-" else 1.0
    return sign * (float(match.group(2)) + float(match.group(3)) / 60.0 + float(match.group(4)) / 3600.0)


def _gv0054_ned_query(ra, dec):
    ra = float(ra)
    dec = float(dec)
    url = (
        "https://ned.ipac.caltech.edu/cgi-bin/objsearch"
        "?search_type=Near+Position+Search"
        "&in_csys=Equatorial"
        "&in_equinox=J2000.0"
        f"&lon={ra}d"
        f"&lat={dec}d"
        "&radius=0.1"
        "&hconst=73"
        "&omegam=0.27"
        "&omegav=0.73"
        "&corr_z=1"
        "&z_constraint=Unconstrained"
        "&z_value1="
        "&z_value2="
        "&z_unit=z"
        "&ot_include=ANY"
        "&in_objtypes1=Galaxies"
        "&in_objtypes2=Galaxies"
        "&out_csys=Equatorial"
        "&out_equinox=J2000.0"
        "&obj_sort=Distance+to+search+center"
        "&of=table"
    )

    response = requests.get(url, timeout=60)
    response.raise_for_status()
    tables = pd.read_html(response.text)
    if not tables:
        return {"rows": [], "url": url, "http_status": response.status_code, "tables_found": 0}

    frame = max(tables, key=lambda table: table.shape[0]).copy()
    if frame.empty:
        return {"rows": [], "url": url, "http_status": response.status_code, "tables_found": len(tables)}

    row = frame.iloc[0]
    cells = [_gv0054_clean(value) for value in row.tolist()]

    def cell(index):
        return cells[index] if 0 <= index < len(cells) else None

    normalized = {
        "main_id": cell(1) or "Not available",
        "ra_text": cell(2),
        "dec_text": cell(3),
        "ra": _gv0054_ra_degrees(cell(2)),
        "dec": _gv0054_dec_degrees(cell(3)),
        "otype": cell(4),
        "rvz_radvel": _gv0054_number(cell(5)),
        "rvz_redshift": _gv0054_number(cell(6)),
        "sp_type": None,
        "galdim_majaxis": None,
        "galdim_minaxis": None,
        "ned_distance_arcmin": _gv0054_number(cell(9)),
        "_sizeSource": "Unavailable",
        "_selectionRule": "NED row 1",
        "_candidateCount": int(frame.shape[0]),
        "_ned_columns": [str(column) for column in frame.columns],
        "_ned_raw_first_row": cells,
    }

    return {
        "rows": [normalized],
        "url": url,
        "http_status": response.status_code,
        "tables_found": len(tables),
        "selected_table_shape": [int(frame.shape[0]), int(frame.shape[1])],
    }


if colab_output is not None:
    colab_output.register_callback("gv0054.ned_query", _gv0054_ned_query)

base_wrapper = urllib.request.urlopen(BASE_WRAPPER_URL, timeout=60).read().decode("utf-8")
exec_marker = "exec(source, globals())"
if base_wrapper.count(exec_marker) != 1:
    raise RuntimeError("GV-0051 execution marker not found exactly once")

scope = {}
exec(compile(base_wrapper.replace(exec_marker, "", 1), "gv-0051.py", "exec"), scope)
source = scope["source"]

replacements = [
    (
        "<h3>Galaxy Viewer — GV-0051</h3>",
        "<h3>Galaxy Viewer — GV-0054</h3>"
    ),
    (
        "GV-0051 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Distance now displays in BLY and tiny angular sizes are shown in MAS so they do not round down to zero. The default survey is Hubble Outreach Color, the default view opens on the Hubble Ultra Deep Field, and the table now shows Z / Distance plus Type / Spectrum without duplicating distance.",
        "GV-0054 preserves the current viewer position, selected survey, and zoom level when switching tabs. SIMBAD and NED use a 6-arcsecond search window. The Object figures of merit table lists SIMBAD row 1 first and NED row 1 second. NED is queried through the Colab Python kernel with the requested NED table parameters. All other GV-0051 behavior remains unchanged."
    ),
    (
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0051-state";',
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0054-state";'
    ),
    (
        '''function restoreViewerState(reason="") {
  if (!window.aladin) return;
  const state = loadViewerState();
  try {
    document.getElementById("coordBox").value = formatCoords(state.ra, state.dec);
    window.aladin.gotoRaDec(state.ra, state.dec);
    if (typeof window.aladin.setFoV === "function" && Number.isFinite(state.fov) && state.fov > 0) window.aladin.setFoV(state.fov);
    applySurvey(state.survey, {persist:false, silent:true});
    if (reason) setStatus(reason);
  } catch(err) {
    if (reason) setStatus(reason + " (restore warning: " + err.message + ")");
  }
}''',
        '''function restoreViewerState(reason="") {
  if (!window.aladin) return;
  const state = loadViewerState();
  try {
    document.getElementById("coordBox").value = formatCoords(state.ra, state.dec);
    applySurvey(state.survey, {persist:false, silent:true});
    window.aladin.gotoRaDec(state.ra, state.dec);
    const applySavedFov = () => {
      try {
        if (typeof window.aladin.setFoV === "function" && Number.isFinite(state.fov) && state.fov > 0) window.aladin.setFoV(state.fov);
      } catch(e) {}
    };
    applySavedFov();
    setTimeout(applySavedFov, 150);
    setTimeout(applySavedFov, 500);
    if (reason) setStatus(reason);
  } catch(err) {
    if (reason) setStatus(reason + " (restore warning: " + err.message + ")");
  }
}'''
    ),
    (
        '  const catalogRows = CATALOGS.map(name => `<tr><td>${safe(name)}</td><td>30 arcsec cone search</td><td id="status-${name.replace(/[^A-Za-z0-9]/g,"")}">Ready</td></tr>`);',
        '  const catalogRows = CATALOGS.map(name => `<tr><td>${safe(name)}</td><td>6 arcsec cone search</td><td id="status-${name.replace(/[^A-Za-z0-9]/g,"")}">Ready</td></tr>`);'
    ),
    (
        '  const radius = 30/3600;',
        '  const radius = 6/3600;'
    ),
    (
        '''async function probeNed(ra,dec) {
  const url = `https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&of=json_basic&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.5`;
  return await fetchJSON(url);
}''',
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
}'''
    ),
    (
        '''function summarizeTopSimbadCandidate(rows, requested, ned=null, vizier=null) {
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const primary = {...rows[0]};
  primary._candidateCount = rows.length;
  primary._selectionRule = "SIMBAD row 1";
  const distanceLy = resolveDistanceLy(primary, ned);
  const size = resolveWholeGalaxySize(primary, ned, vizier, distanceLy);
  if (size) {
    primary.galdim_majaxis = size.majorArcsec;
    primary.galdim_minaxis = size.minorArcsec;
    primary._sizeSource = size.source;
  } else {
    primary._sizeSource = "Unavailable";
  }
  return primary;
}''',
        '''function summarizeTopSimbadCandidate(rows, requested, ned=null, vizier=null) {
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const primary = {...rows[0]};
  primary._candidateCount = rows.length;
  primary._selectionRule = "SIMBAD row 1";
  const distanceLy = resolveDistanceLy(primary, ned);
  const size = resolveWholeGalaxySize(primary, ned, vizier, distanceLy);
  if (size) {
    primary.galdim_majaxis = size.majorArcsec;
    primary.galdim_minaxis = size.minorArcsec;
    primary._sizeSource = size.source;
  } else {
    primary._sizeSource = "Unavailable";
  }
  return primary;
}
function summarizeTopNedCandidate(rows) {
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const primary = {...rows[0]};
  primary._candidateCount = Number(primary._candidateCount) || rows.length;
  primary._selectionRule = "NED row 1";
  primary._sizeSource = primary._sizeSource || "Unavailable";
  return primary;
}'''
    ),
    (
        '''function renderResult(obj, requested, ned=null) {
  const body = document.getElementById("resultBody");
  if(!obj){
    body.innerHTML = `<tr><td colspan="7" style="text-align:center">No SIMBAD object found within 30 arcseconds of ${safe(requested.ra.toFixed(6)+" "+requested.dec.toFixed(6))}</td></tr>`;
    return;
  }
  const z = Number(obj.rvz_redshift);
  const distanceLy = resolveDistanceLy(obj, ned);
  const coords = Number(obj.ra).toFixed(6)+" "+Number(obj.dec).toFixed(6);
  const name = cleanId(obj.main_id || "Not available");
  const sizeSource = obj._sizeSource ? `Size source: ${obj._sizeSource}` : null;
  const selectionRule = obj._selectionRule ? `Selection: ${obj._selectionRule}` : null;
  const parallaxInfo = Number.isFinite(Number(obj.plx_value)) && Number(obj.plx_value) > 0 ? `Parallax: ${fmt(obj.plx_value,3)} mas` : null;
  const info = [
    obj.otype ? "Type: " + obj.otype : null,
    obj.sp_type ? "Spectrum: " + obj.sp_type : null,
    parallaxInfo,
    sizeSource,
    selectionRule,
    obj._candidateCount ? `Candidates: ${obj._candidateCount}` : null
  ].filter(Boolean).join("; ") || "No additional SIMBAD classification";

  let zDistanceText = "Not available";
  if (Number.isFinite(z) || Number.isFinite(distanceLy)) {
    const zPart = Number.isFinite(z) ? z.toFixed(6) : "z unavailable";
    const dPart = Number.isFinite(distanceLy) ? formatBlyFromLy(distanceLy, 6) : "distance unavailable";
    zDistanceText = `${zPart} / ${dPart}`;
  }

  const ageText = "Not available in SIMBAD";
  const typeSpectrumText = [obj.otype || null, obj.sp_type || null].filter(Boolean).join(" / ") || "Not available";

  body.innerHTML = `<tr><td>${safe(name)}</td><td style="font-family:monospace">${safe(coords)}</td><td>${safe(zDistanceText)}</td><td>${safe(sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td><td>${safe(ageText)}</td><td>${safe(typeSpectrumText)}</td><td>${safe(info)}</td></tr>`;
}''',
        '''function buildResultRow(obj, catalogName, requested, nedForDistance=null) {
  if (!obj) return "";
  const z = Number(obj.rvz_redshift);
  const distanceLy = resolveDistanceLy(obj, nedForDistance);
  const raValue = Number.isFinite(Number(obj.ra)) ? Number(obj.ra).toFixed(6) : requested.ra.toFixed(6);
  const decValue = Number.isFinite(Number(obj.dec)) ? Number(obj.dec).toFixed(6) : requested.dec.toFixed(6);
  const coords = raValue + " " + decValue;
  const name = cleanId(obj.main_id || "Not available");
  const sizeSource = obj._sizeSource ? `Size source: ${obj._sizeSource}` : null;
  const selectionRule = obj._selectionRule ? `Selection: ${obj._selectionRule}` : null;
  const parallaxInfo = Number.isFinite(Number(obj.plx_value)) && Number(obj.plx_value) > 0 ? `Parallax: ${fmt(obj.plx_value,3)} mas` : null;
  const info = [
    `Catalog: ${catalogName}`,
    obj.otype ? "Type: " + obj.otype : null,
    obj.sp_type ? "Spectrum: " + obj.sp_type : null,
    parallaxInfo,
    sizeSource,
    selectionRule,
    obj._candidateCount ? `Candidates: ${obj._candidateCount}` : null
  ].filter(Boolean).join("; ");

  let zDistanceText = "Not available";
  if (Number.isFinite(z) || Number.isFinite(distanceLy)) {
    const zPart = Number.isFinite(z) ? z.toFixed(6) : "z unavailable";
    const dPart = Number.isFinite(distanceLy) ? formatBlyFromLy(distanceLy, 6) : "distance unavailable";
    zDistanceText = `${zPart} / ${dPart}`;
  }

  const ageText = catalogName === "SIMBAD" ? "Not available in SIMBAD" : "Not available in NED";
  const typeSpectrumText = [obj.otype || null, obj.sp_type || null].filter(Boolean).join(" / ") || "Not available";
  return `<tr><td>${safe(name)}</td><td style="font-family:monospace">${safe(coords)}</td><td>${safe(zDistanceText)}</td><td>${safe(sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td><td>${safe(ageText)}</td><td>${safe(typeSpectrumText)}</td><td>${safe(info)}</td></tr>`;
}
function renderResult(simbadObj, nedObj, requested, nedPayload=null) {
  const body = document.getElementById("resultBody");
  const rows = [];
  if (simbadObj) rows.push(buildResultRow(simbadObj, "SIMBAD", requested, nedPayload));
  if (nedObj) rows.push(buildResultRow(nedObj, "NED", requested, null));
  if (!rows.length) {
    body.innerHTML = `<tr><td colspan="7" style="text-align:center">No SIMBAD or NED object found within 6 arcseconds of ${safe(requested.ra.toFixed(6)+" "+requested.dec.toFixed(6))}</td></tr>`;
    return;
  }
  body.innerHTML = rows.join("");
}'''
    ),
    (
        '''    setStatus("All catalog responses returned. Using SIMBAD row 1 as the displayed primary object…");
    const finalSummary = summarizeTopSimbadCandidate(simbadRows,coords,ned,vizier);
    renderResult(finalSummary,coords,ned);
    setDebugText(buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, finalSummary));
    saveViewerState();
    setStatus("Search complete. GV-0051 used the first SIMBAD row from the 30-arcsecond cone search, kept your current view, defaults to Hubble Outreach Color, opens on the Hubble Ultra Deep Field, and now shows Z / Distance plus Type / Spectrum.");''',
        '''    setStatus("All catalog responses returned. Using SIMBAD row 1 first and NED row 1 second…");
    const simbadSummary = summarizeTopSimbadCandidate(simbadRows,coords,ned,vizier);
    const nedSummary = summarizeTopNedCandidate(ned);
    renderResult(simbadSummary,nedSummary,coords,ned);
    setDebugText(buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, simbadSummary || nedSummary));
    saveViewerState();
    setStatus("Search complete. GV-0054 used the first SIMBAD row and first NED row from the 6-arcsecond search window and restored the saved zoom level.");'''
    )
]

for old, new in replacements:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"Patch target count was {count}, expected 1:\n{old[:160]}")
    source = source.replace(old, new, 1)

exec(source, globals())
