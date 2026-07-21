from IPython.display import HTML, display
import urllib.request

RAW_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0049.py"

source = urllib.request.urlopen(RAW_URL).read().decode("utf-8")

replacements = [
    (
        'RAW_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0048.py"',
        'RAW_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/gv-0049.py"'
    ),
    (
        "<h3>Galaxy Viewer — GV-0049</h3>",
        "<h3>Galaxy Viewer — GV-0050</h3>"
    ),
    (
        "GV-0049 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Distance displays in BLY, tiny angular sizes are shown in MAS, the survey selector is hardened, and the default survey is Hubble Outreach Color.",
        "GV-0050 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object. Hubble Outreach Color remains the default survey, the survey selector remains hardened, and the default starting view is the Hubble Ultra Deep Field."
    ),
    (
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0049-state";',
        'const VIEWER_STATE_KEY = "galaxy-viewer-gv0050-state";'
    ),
    (
        'function defaultViewerState() {\n  return { ra: 10.684708, dec: 41.268750, survey: "CDS/P/HST/EPO", fov: 1.0 };\n}\nfunction surveyExists(id) {\n  return SURVEYS.some(s => s.id === id);\n}\nfunction normalizeSurveyId(id) {\n  return surveyExists(id) ? id : defaultViewerState().survey;\n}',
        'function defaultViewerState() {\n  return { ra: 53.162500, dec: -27.791417, survey: "CDS/P/HST/EPO", fov: 1.0 };\n}\nfunction surveyExists(id) {\n  return SURVEYS.some(s => s.id === id);\n}\nfunction normalizeSurveyId(id) {\n  return surveyExists(id) ? id : defaultViewerState().survey;\n}'
    ),
    (
        '    setStatus("Search complete. GV-0049 used the first SIMBAD row from the 30-arcsecond cone search, kept your current view, displays tiny angular sizes in MAS, and defaults to Hubble Outreach Color.");',
        '    setStatus("Search complete. GV-0050 used the first SIMBAD row from the 30-arcsecond cone search, kept your current view, defaults to Hubble Outreach Color, and starts from the Hubble Ultra Deep Field when no saved state exists.");'
    )
]

for old, new in replacements:
    if old not in source:
        raise RuntimeError(f"Patch target not found:\n{old[:120]}")
    source = source.replace(old, new, 1)

exec(source, globals())
