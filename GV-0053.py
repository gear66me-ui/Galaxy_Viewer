from IPython.display import HTML, display
import urllib.request

BASE_WRAPPER_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0051.py"

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
        "<h3>Galaxy Viewer — GV-0053</h3>"
    ),
    (
        "GV-0051 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Distance now displays in BLY and tiny angular sizes are shown in MAS so they do not round down to zero. The default survey is Hubble Outreach Color, the default view opens on the Hubble Ultra Deep Field, and the table now shows Z / Distance plus Type / Spectrum without duplicating distance.",
        "GV-0053 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD and NED use a 6-arcsecond search window. The Object figures of merit table lists SIMBAD row 1 first and NED row 1 second. The saved zoom level is restored when returning to the tab. All other GV-0051 behavior remains unchanged."
    ),
    (
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0051-state";',
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0053-state";'
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
        '''async function fetchText(url, options={}) {
  const response = await fetch(url, options);
  if(!response.ok) throw new Error("HTTP " + response.status);
  return await response.text();
}
function parseNedRaToDegrees(text) {
  const match = String(text ?? "").trim().match(/^(\\d+)h(\\d+)m([\\d.]+)s$/i);
  if (!match) return null;
  const hours = Number(match[1]), minutes = Number(match[2]), seconds = Number(match[3]);
  if (![hours, minutes, seconds].every(Number.isFinite)) return null;
  return 15 * (hours + minutes / 60 + seconds / 3600);
}
function parseNedDecToDegrees(text) {
  const match = String(text ?? "").trim().match(/^([+-]?)(\\d+)d(\\d+)m([\\d.]+)s$/i);
  if (!match) return null;
  const sign = match[1] === "-" ? -1 : 1;
  const degrees = Number(match[2]), minutes = Number(match[3]), seconds = Number(match[4]);
  if (![degrees, minutes, seconds].every(Number.isFinite)) return null;
  return sign * (degrees + minutes / 60 + seconds / 3600);
}
function cleanNedCell(value) {
  const text = String(value ?? "").replace(/\\s+/g, " ").trim();
  return text && text !== "..." ? text : null;
}
async function probeNed(ra,dec) {
  const url = `https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.1&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes2=Galaxies&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=table`;
  const html = await fetchText(url);
  const doc = new DOMParser().parseFromString(html, "text/html");
  let bestRows = [];
  doc.querySelectorAll("table").forEach(table => {
    const rows = [...table.querySelectorAll("tr")]
      .map(tr => [...tr.querySelectorAll("td")].map(td => td.textContent.replace(/\\s+/g, " ").trim()))
      .filter(cells => cells.length >= 10);
    if (rows.length > bestRows.length) bestRows = rows;
  });
  return bestRows.map(cells => {
    const zText = cleanNedCell(cells[6]);
    const velText = cleanNedCell(cells[5]);
    const zValue = Number(zText);
    const velValue = Number(String(velText ?? "").replace(/[^\\d.+-]/g, ""));
    return {
      main_id: cleanNedCell(cells[1]) || "Not available",
      ra_text: cleanNedCell(cells[2]),
      dec_text: cleanNedCell(cells[3]),
      ra: parseNedRaToDegrees(cells[2]),
      dec: parseNedDecToDegrees(cells[3]),
      otype: cleanNedCell(cells[4]),
      rvz_radvel: Number.isFinite(velValue) ? velValue : null,
      rvz_redshift: Number.isFinite(zValue) ? zValue : null,
      sp_type: null,
      galdim_majaxis: null,
      galdim_minaxis: null,
      _sizeSource: "Unavailable"
    };
  });
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
  primary._candidateCount = rows.length;
  primary._selectionRule = "NED row 1";
  primary._sizeSource = "Unavailable";
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
        '''function buildResultRow(obj, catalogName, requested) {
  if (!obj) return "";
  const z = Number(obj.rvz_redshift);
  const distanceLy = resolveDistanceLy(obj);
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

  const ageText = "Not available in " + catalogName;
  const typeSpectrumText = [obj.otype || null, obj.sp_type || null].filter(Boolean).join(" / ") || "Not available";
  return `<tr><td>${safe(name)}</td><td style="font-family:monospace">${safe(coords)}</td><td>${safe(zDistanceText)}</td><td>${safe(sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td><td>${safe(ageText)}</td><td>${safe(typeSpectrumText)}</td><td>${safe(info)}</td></tr>`;
}
function renderResult(simbadObj, nedObj, requested) {
  const body = document.getElementById("resultBody");
  const rows = [];
  if (simbadObj) rows.push(buildResultRow(simbadObj, "SIMBAD", requested));
  if (nedObj) rows.push(buildResultRow(nedObj, "NED", requested));
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
    renderResult(simbadSummary,nedSummary,coords);
    setDebugText(buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, simbadSummary || nedSummary));
    saveViewerState();
    setStatus("Search complete. GV-0053 used the first SIMBAD row and first NED row from the 6-arcsecond search window, kept your current view, and restores the saved zoom when you return to the tab.");'''
    )
]

for old, new in replacements:
    if source.count(old) != 1:
        raise RuntimeError(f"Patch target count was {source.count(old)}, expected 1:\n{old[:140]}")
    source = source.replace(old, new, 1)

exec(source, globals())
