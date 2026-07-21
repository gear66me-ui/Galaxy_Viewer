from IPython.display import HTML, display
import urllib.request

RAW_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0048.py"

source = urllib.request.urlopen(RAW_URL).read().decode("utf-8")

replacements = [
    (
        "<h3>Galaxy Viewer — GV-0048</h3>",
        "<h3>Galaxy Viewer — GV-0049</h3>"
    ),
    (
        "GV-0048 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Distance now displays in BLY and tiny angular sizes are shown in MAS so they do not round down to zero.",
        "GV-0049 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Distance displays in BLY, tiny angular sizes are shown in MAS, the survey selector is hardened, and the default survey is Hubble Outreach Color."
    ),
    (
        'const SURVEYS = [\n  {name:"DSS2 Color", id:"P/DSS2/color"},\n  {name:"DSS2 Red", id:"P/DSS2/red"},\n  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},\n  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},\n  {name:"2MASS Color", id:"P/2MASS/color"},\n  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"}\n];',
        'const SURVEYS = [\n  {name:"Hubble Outreach Color", id:"CDS/P/HST/EPO"},\n  {name:"DSS2 Color", id:"P/DSS2/color"},\n  {name:"DSS2 Red", id:"P/DSS2/red"},\n  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},\n  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},\n  {name:"2MASS Color", id:"P/2MASS/color"},\n  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"}\n];'
    ),
    (
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0048-state";',
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0049-state";'
    ),
    (
        'function defaultViewerState() {\n  return { ra: 10.684708, dec: 41.268750, survey: "P/DSS2/color", fov: 1.0 };\n}',
        'function defaultViewerState() {\n  return { ra: 10.684708, dec: 41.268750, survey: "CDS/P/HST/EPO", fov: 1.0 };\n}\nfunction surveyExists(id) {\n  return SURVEYS.some(s => s.id === id);\n}\nfunction normalizeSurveyId(id) {\n  return surveyExists(id) ? id : defaultViewerState().survey;\n}'
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
        'function applySurvey(id, options={}) {\n  const persist = options.persist !== false;\n  const silent = options.silent === true;\n  const surveyId = normalizeSurveyId(id);\n  if (!window.aladin) return false;\n  try {\n    document.getElementById("surveySelect").value = surveyId;\n    window.aladin.setImageSurvey(surveyId);\n    if (persist) saveViewerState({survey: surveyId});\n    return true;\n  } catch(err) {\n    const fallbackId = defaultViewerState().survey;\n    try {\n      document.getElementById("surveySelect").value = fallbackId;\n      window.aladin.setImageSurvey(fallbackId);\n      if (persist) saveViewerState({survey: fallbackId});\n    } catch(innerErr) {}\n    if (!silent) setStatus("Survey failed: " + err.message);\n    return false;\n  }\n}\nfunction restoreViewerState(reason="") {\n  if (!window.aladin) return;\n  const state = loadViewerState();\n  try {\n    document.getElementById("coordBox").value = formatCoords(state.ra, state.dec);\n    window.aladin.gotoRaDec(state.ra, state.dec);\n    if (typeof window.aladin.setFoV === "function" && Number.isFinite(state.fov) && state.fov > 0) window.aladin.setFoV(state.fov);\n    applySurvey(state.survey, {persist:false, silent:true});\n    if (reason) setStatus(reason);\n  } catch(err) {\n    if (reason) setStatus(reason + " (restore warning: " + err.message + ")");\n  }\n}'
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
        '    setStatus("Search complete. GV-0048 used the first SIMBAD row from the 30-arcsecond cone search, kept your current view, and now displays tiny angular sizes in MAS.");',
        '    setStatus("Search complete. GV-0049 used the first SIMBAD row from the 30-arcsecond cone search, kept your current view, displays tiny angular sizes in MAS, and defaults to Hubble Outreach Color.");'
    )
]

for old, new in replacements:
    if old not in source:
        raise RuntimeError(f"Patch target not found:\n{old[:120]}")
    source = source.replace(old, new, 1)

exec(source, globals())
