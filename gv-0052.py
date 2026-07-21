from IPython.display import HTML, display
import urllib.request

RAW_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0048.py"

source = urllib.request.urlopen(RAW_URL).read().decode("utf-8")

replacements = [
    (
        '<input id="coordBox" type="text" value="10.684708 41.268750" style="min-width:280px" />',
        '<input id="coordBox" type="text" value="53.162500 -27.791667" style="min-width:280px" />'
    ),
    (
        "<h3>Galaxy Viewer — GV-0048</h3>",
        "<h3>Galaxy Viewer — GV-0052</h3>"
    ),
    (
        "GV-0048 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Distance now displays in BLY and tiny angular sizes are shown in MAS so they do not round down to zero.",
        "GV-0052 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD and NED now use a 6-arcsecond search window, the Object figures table lists SIMBAD row 1 first and NED row 1 second, distance still displays in BLY, tiny angular sizes still display in MAS, and the saved zoom level is restored when you return to the tab. The default survey is Hubble Outreach Color, the default view opens on the Hubble Ultra Deep Field, and the table still shows Z / Distance plus Type / Spectrum without duplicating distance."
    ),
    (
        'const SURVEYS = [\n  {name:"DSS2 Color", id:"P/DSS2/color"},\n  {name:"DSS2 Red", id:"P/DSS2/red"},\n  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},\n  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},\n  {name:"2MASS Color", id:"P/2MASS/color"},\n  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"}\n];',
        'const SURVEYS = [\n  {name:"Hubble Outreach Color", id:"CDS/P/HST/EPO"},\n  {name:"DSS2 Color", id:"P/DSS2/color"},\n  {name:"DSS2 Red", id:"P/DSS2/red"},\n  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},\n  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},\n  {name:"2MASS Color", id:"P/2MASS/color"},\n  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"}\n];'
    ),
    (
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0048-state";',
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0051-state";'
    ),
    (
        'function defaultViewerState() {\n  return { ra: 10.684708, dec: 41.268750, survey: "P/DSS2/color", fov: 1.0 };\n}',
        'function defaultViewerState() {\n  return { ra: 53.162500, dec: -27.791667, survey: "CDS/P/HST/EPO", fov: 1.0 };\n}\nfunction surveyExists(id) {\n  return SURVEYS.some(s => s.id === id);\n}\nfunction normalizeSurveyId(id) {\n  return surveyExists(id) ? id : defaultViewerState().survey;\n}'
    ),
    (
        '      survey: typeof parsed?.survey === "string" && parsed.survey ? parsed.survey : defaultViewerState().survey,',
        '      survey: normalizeSurveyId(parsed?.survey),'
    ),
    (
        '    const nextState = { ...defaultViewerState(), ...current, ...override };\n    localStorage.setItem(VIEWER_STATE_KEY, JSON.stringify(nextState));\n    return nextState;',
        '    const nextState = { ...defaultViewerState(), ...current, ...override };\n    nextState.survey = normalizeSurveyId(nextState.survey);\n    localStorage.setItem(VIEWER_STATE_KEY, JSON.stringify(nextState));\n    return nextState;'
    ),
    (
        '  const survey = document.getElementById("surveySelect")?.value || fallback.survey;\n  return { ra, dec, survey, fov };',
        '  const survey = normalizeSurveyId(document.getElementById("surveySelect")?.value || fallback.survey);\n  return { ra, dec, survey, fov };'
    ),
    (
        'function restoreViewerState(reason="") {\n  if (!window.aladin) return;\n  const state = loadViewerState();\n  try {\n    document.getElementById("coordBox").value = formatCoords(state.ra, state.dec);\n    document.getElementById("surveySelect").value = state.survey;\n    window.aladin.gotoRaDec(state.ra, state.dec);\n    if (typeof window.aladin.setFoV === "function" && Number.isFinite(state.fov) && state.fov > 0) window.aladin.setFoV(state.fov);\n    window.aladin.setImageSurvey(state.survey);\n    if (reason) setStatus(reason);\n  } catch(err) {\n    if (reason) setStatus(reason + " (restore warning: " + err.message + ")");\n  }\n}',
        'function applySurvey(id, options={}) {\n  const persist = options.persist !== false;\n  const silent = options.silent === true;\n  const surveyId = normalizeSurveyId(id);\n  if (!window.aladin) return false;\n  try {\n    document.getElementById("surveySelect").value = surveyId;\n    window.aladin.setImageSurvey(surveyId);\n    if (persist) saveViewerState({survey: surveyId});\n    return true;\n  } catch(err) {\n    const fallbackId = defaultViewerState().survey;\n    try {\n      document.getElementById("surveySelect").value = fallbackId;\n      window.aladin.setImageSurvey(fallbackId);\n      if (persist) saveViewerState({survey: fallbackId});\n    } catch(innerErr) {}\n    if (!silent) setStatus("Survey failed: " + err.message);\n    return false;\n  }\n}\nfunction restoreViewerState(reason="") {\n  if (!window.aladin) return;\n  const state = loadViewerState();\n  try {\n    document.getElementById("coordBox").value = formatCoords(state.ra, state.dec);\n    applySurvey(state.survey, {persist:false, silent:true});\n    window.aladin.gotoRaDec(state.ra, state.dec);\n    const applySavedFov = () => {\n      try {\n        if (typeof window.aladin.setFoV === "function" && Number.isFinite(state.fov) && state.fov > 0) window.aladin.setFoV(state.fov);\n      } catch(e) {}\n    };\n    applySavedFov();\n    setTimeout(applySavedFov, 150);\n    if (reason) setStatus(reason);\n  } catch(err) {\n    if (reason) setStatus(reason + " (restore warning: " + err.message + ")");\n  }\n}'
    ),
    (
        '  document.getElementById("surveySelect").value = initialState.survey;',
        '  document.getElementById("surveySelect").value = normalizeSurveyId(initialState.survey);'
    ),
    (
        '      survey: initialState.survey,',
        '      survey: normalizeSurveyId(initialState.survey),'
    ),
    (
        'function changeSurvey() {\n  if (!window.aladin) return;\n  const id = document.getElementById("surveySelect").value;\n  setStatus("Loading survey: " + id);\n  try {\n    window.aladin.setImageSurvey(id);\n    saveViewerState({survey:id});\n    setStatus("Loaded survey: " + id);\n  } catch (err) {\n    setStatus("Survey failed: " + err.message);\n  }\n}',
        'function changeSurvey() {\n  if (!window.aladin) return;\n  const id = normalizeSurveyId(document.getElementById("surveySelect").value);\n  setStatus("Loading survey: " + id);\n  if (applySurvey(id, {persist:true, silent:false})) {\n    setStatus("Loaded survey: " + id);\n  }\n}'
    ),
    (
        '      window.aladin.setImageSurvey(SURVEYS[i].id);',
        '      applySurvey(SURVEYS[i].id, {persist:false, silent:true});'
    ),
    (
        '  window.aladin.setImageSurvey(document.getElementById("surveySelect").value);\n  saveViewerState();',
        '  applySurvey(document.getElementById("surveySelect").value, {persist:false, silent:true});\n  saveViewerState();'
    ),
    (
        '<th>Distance (BLY)</th>\n          <th>Object size</th>\n          <th>Galaxy age</th>\n          <th>Z / Distance</th>\n          <th>SIMBAD information</th>',
        '<th>Z / Distance</th>\n          <th>Object size</th>\n          <th>Galaxy age</th>\n          <th>Type / Spectrum</th>\n          <th>SIMBAD information</th>'
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
        'async function probeNed(ra,dec) {\n  const url = `https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&of=json_basic&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.5`;\n  return await fetchJSON(url);\n}',
        'async function fetchText(url, options={}) {\n  const response = await fetch(url, options);\n  if(!response.ok) throw new Error("HTTP " + response.status);\n  return await response.text();\n}\nfunction parseNedRaToDegrees(text) {\n  const match = String(text ?? "").trim().match(/^(\\d+)h(\\d+)m([\\d.]+)s$/i);\n  if (!match) return null;\n  const hours = Number(match[1]), minutes = Number(match[2]), seconds = Number(match[3]);\n  if (![hours, minutes, seconds].every(Number.isFinite)) return null;\n  return 15 * (hours + minutes / 60 + seconds / 3600);\n}\nfunction parseNedDecToDegrees(text) {\n  const match = String(text ?? "").trim().match(/^([+-]?)(\\d+)d(\\d+)m([\\d.]+)s$/i);\n  if (!match) return null;\n  const sign = match[1] === "-" ? -1 : 1;\n  const degrees = Number(match[2]), minutes = Number(match[3]), seconds = Number(match[4]);\n  if (![degrees, minutes, seconds].every(Number.isFinite)) return null;\n  return sign * (degrees + minutes / 60 + seconds / 3600);\n}\nfunction cleanNedCell(value) {\n  const text = String(value ?? "").replace(/\\s+/g, " ").trim();\n  return text && text !== "..." ? text : null;\n}\nasync function probeNed(ra,dec) {\n  const url = `https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.1&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes2=Galaxies&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=table`;\n  const html = await fetchText(url);\n  const doc = new DOMParser().parseFromString(html, "text/html");\n  let bestRows = [];\n  doc.querySelectorAll("table").forEach(table => {\n    const rows = [...table.querySelectorAll("tr")]\n      .map(tr => [...tr.querySelectorAll("td")].map(td => td.textContent.replace(/\\s+/g, " ").trim()))\n      .filter(cells => cells.length >= 10);\n    if (rows.length > bestRows.length) bestRows = rows;\n  });\n  return bestRows.map(cells => {\n    const zText = cleanNedCell(cells[6]);\n    const velText = cleanNedCell(cells[5]);\n    const distanceText = cleanNedCell(cells[9]);\n    const zValue = Number(zText);\n    const velValue = Number(String(velText ?? "").replace(/[^\\d.+-]/g, ""));\n    const distanceArcmin = Number(distanceText);\n    return {\n      main_id: cleanNedCell(cells[1]) || "Not available",\n      ra_text: cleanNedCell(cells[2]),\n      dec_text: cleanNedCell(cells[3]),\n      ra: parseNedRaToDegrees(cells[2]),\n      dec: parseNedDecToDegrees(cells[3]),\n      otype: cleanNedCell(cells[4]),\n      rvz_radvel: Number.isFinite(velValue) ? velValue : null,\n      rvz_redshift: Number.isFinite(zValue) ? zValue : null,\n      sp_type: null,\n      galdim_majaxis: null,\n      galdim_minaxis: null,\n      ned_distance_arcmin: Number.isFinite(distanceArcmin) ? distanceArcmin : null,\n      _sizeSource: "Unavailable"\n    };\n  });\n}'
    ),
    (
        'function summarizeTopSimbadCandidate(rows, requested, ned=null, vizier=null) {\n  if (!Array.isArray(rows) || rows.length === 0) return null;\n  const primary = {...rows[0]};\n  primary._candidateCount = rows.length;\n  primary._selectionRule = "SIMBAD row 1";\n  const distanceLy = resolveDistanceLy(primary, ned);\n  const size = resolveWholeGalaxySize(primary, ned, vizier, distanceLy);\n  if (size) {\n    primary.galdim_majaxis = size.majorArcsec;\n    primary.galdim_minaxis = size.minorArcsec;\n    primary._sizeSource = size.source;\n  } else {\n    primary._sizeSource = "Unavailable";\n  }\n  return primary;\n}',
        'function summarizeTopSimbadCandidate(rows, requested, ned=null, vizier=null) {\n  if (!Array.isArray(rows) || rows.length === 0) return null;\n  const primary = {...rows[0]};\n  primary._candidateCount = rows.length;\n  primary._selectionRule = "SIMBAD row 1";\n  const distanceLy = resolveDistanceLy(primary, ned);\n  const size = resolveWholeGalaxySize(primary, ned, vizier, distanceLy);\n  if (size) {\n    primary.galdim_majaxis = size.majorArcsec;\n    primary.galdim_minaxis = size.minorArcsec;\n    primary._sizeSource = size.source;\n  } else {\n    primary._sizeSource = "Unavailable";\n  }\n  return primary;\n}\nfunction summarizeTopNedCandidate(rows, requested) {\n  if (!Array.isArray(rows) || rows.length === 0) return null;\n  const primary = {...rows[0]};\n  primary.ra = Number.isFinite(Number(primary.ra)) ? Number(primary.ra) : requested.ra;\n  primary.dec = Number.isFinite(Number(primary.dec)) ? Number(primary.dec) : requested.dec;\n  primary._candidateCount = rows.length;\n  primary._selectionRule = "NED row 1";\n  if (!primary._sizeSource) primary._sizeSource = "Unavailable";\n  return primary;\n}\nfunction buildResultInfo(obj, sourceLabel) {\n  const sizeSource = obj._sizeSource ? `Size source: ${obj._sizeSource}` : null;\n  const selectionRule = obj._selectionRule ? `Selection: ${obj._selectionRule}` : null;\n  const parallaxInfo = Number.isFinite(Number(obj.plx_value)) && Number(obj.plx_value) > 0 ? `Parallax: ${fmt(obj.plx_value,3)} mas` : null;\n  return [\n    `Source: ${sourceLabel}`,\n    obj.otype ? "Type: " + obj.otype : null,\n    obj.sp_type ? "Spectrum: " + obj.sp_type : null,\n    parallaxInfo,\n    sizeSource,\n    selectionRule,\n    obj._candidateCount ? `Candidates: ${obj._candidateCount}` : null\n  ].filter(Boolean).join("; ") || "No additional classification";\n}\nfunction buildResultRow(obj, sourceLabel, requested, nedPayload=null) {\n  if (!obj) return "";\n  const z = Number(obj.rvz_redshift);\n  const distanceLy = resolveDistanceLy(obj, sourceLabel === "SIMBAD" ? nedPayload : null);\n  const coords = Number(obj.ra).toFixed(6)+" "+Number(obj.dec).toFixed(6);\n  const name = cleanId(obj.main_id || "Not available");\n  let zDistanceText = "Not available";\n  if (Number.isFinite(z) || Number.isFinite(distanceLy)) {\n    const zPart = Number.isFinite(z) ? z.toFixed(6) : "z unavailable";\n    const dPart = Number.isFinite(distanceLy) ? formatBlyFromLy(distanceLy, 6) : "distance unavailable";\n    zDistanceText = `${zPart} / ${dPart}`;\n  }\n  const ageText = sourceLabel === "SIMBAD" ? "Not available in SIMBAD" : "Not available in NED";\n  const typeSpectrumText = [obj.otype || null, obj.sp_type || null].filter(Boolean).join(" / ") || "Not available";\n  const info = buildResultInfo(obj, sourceLabel);\n  return `<tr><td>${safe(name)}</td><td style="font-family:monospace">${safe(coords)}</td><td>${safe(zDistanceText)}</td><td>${safe(sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td><td>${safe(ageText)}</td><td>${safe(typeSpectrumText)}</td><td>${safe(info)}</td></tr>`;\n}'
    ),
    (
        'function renderResult(obj, requested, ned=null) {\n  const body = document.getElementById("resultBody");\n  if(!obj){\n    body.innerHTML = `<tr><td colspan="7" style="text-align:center">No SIMBAD object found within 30 arcseconds of ${safe(requested.ra.toFixed(6)+" "+requested.dec.toFixed(6))}</td></tr>`;\n    return;\n  }\n  const z = Number(obj.rvz_redshift);\n  const distanceLy = resolveDistanceLy(obj, ned);\n  const coords = Number(obj.ra).toFixed(6)+" "+Number(obj.dec).toFixed(6);\n  const name = cleanId(obj.main_id || "Not available");\n  const sizeSource = obj._sizeSource ? `Size source: ${obj._sizeSource}` : null;\n  const selectionRule = obj._selectionRule ? `Selection: ${obj._selectionRule}` : null;\n  const parallaxInfo = Number.isFinite(Number(obj.plx_value)) && Number(obj.plx_value) > 0 ? `Parallax: ${fmt(obj.plx_value,3)} mas` : null;\n  const info = [\n    obj.otype ? "Type: " + obj.otype : null,\n    obj.sp_type ? "Spectrum: " + obj.sp_type : null,\n    parallaxInfo,\n    sizeSource,\n    selectionRule,\n    obj._candidateCount ? `Candidates: ${obj._candidateCount}` : null\n  ].filter(Boolean).join("; ") || "No additional SIMBAD classification";\n\n  let zDistanceText = "Not available";\n  if (Number.isFinite(z) || Number.isFinite(distanceLy)) {\n    const zPart = Number.isFinite(z) ? z.toFixed(6) : "z unavailable";\n    const dPart = Number.isFinite(distanceLy) ? formatBlyFromLy(distanceLy, 6) : "distance unavailable";\n    zDistanceText = `${zPart} / ${dPart}`;\n  }\n\n  const ageText = "Not available in SIMBAD";\n  const typeSpectrumText = [obj.otype || null, obj.sp_type || null].filter(Boolean).join(" / ") || "Not available";\n\n  body.innerHTML = `<tr><td>${safe(name)}</td><td style="font-family:monospace">${safe(coords)}</td><td>${safe(zDistanceText)}</td><td>${safe(sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td><td>${safe(ageText)}</td><td>${safe(typeSpectrumText)}</td><td>${safe(info)}</td></tr>`;\n}',
        'function renderResult(simbadObj, nedObj, requested, nedPayload=null) {\n  const body = document.getElementById("resultBody");\n  const rows = [];\n  if (simbadObj) rows.push(buildResultRow(simbadObj, "SIMBAD", requested, nedPayload));\n  if (nedObj) rows.push(buildResultRow(nedObj, "NED", requested, null));\n  if (!rows.length) {\n    body.innerHTML = `<tr><td colspan="7" style="text-align:center">No SIMBAD or NED object found within 6 arcseconds of ${safe(requested.ra.toFixed(6)+" "+requested.dec.toFixed(6))}</td></tr>`;\n    return;\n  }\n  body.innerHTML = rows.join("");\n}'
    ),
    (
        '    setStatus("All catalog responses returned. Using SIMBAD row 1 as the displayed primary object…");\n    const finalSummary = summarizeTopSimbadCandidate(simbadRows,coords,ned,vizier);\n    renderResult(finalSummary,coords,ned);\n    setDebugText(buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, finalSummary));\n    saveViewerState();\n    setStatus("Search complete. GV-0048 used the first SIMBAD row from the 30-arcsecond cone search, kept your current view, and now displays tiny angular sizes in MAS.");',
        '    setStatus("All catalog responses returned. Using SIMBAD row 1 and NED row 1 as the displayed matches…");\n    const finalSummary = summarizeTopSimbadCandidate(simbadRows,coords,ned,vizier);\n    const nedSummary = summarizeTopNedCandidate(ned,coords);\n    renderResult(finalSummary,nedSummary,coords,ned);\n    setDebugText(buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, finalSummary));\n    saveViewerState();\n    setStatus("Search complete. GV-0052 used the first SIMBAD row and first NED row from the 6-arcsecond search window, kept your current view, and restores the saved zoom when you return to the tab.");'
    )
]

for old, new in replacements:
    if old not in source:
        raise RuntimeError(f"Patch target not found:\n{old[:120]}")
    source = source.replace(old, new, 1)

exec(source, globals())
