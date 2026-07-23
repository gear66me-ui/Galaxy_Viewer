from urllib.request import urlopen

# viewer-0010
# Applies only the approved finder corrections to viewer-0007:
# 1. The finder border is copied from the live coordinate box hue and geometry.
# 2. The blue finder symbol is reduced so it remains inside that matched box.
# 3. The approved yellow helper text from viewer-0008 is preserved.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0007.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_target_css = '''    box-sizing: border-box !important;
    border-left-width: 1px !important;
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
}'''

new_target_css = '''    box-sizing: border-box !important;
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
    overflow: hidden !important;
}

/* Keep the native blue finder symbol comfortably inside the matched box. */
#aladin-cosmic-command-test .gv-native-simbad-moved > * {
    transform: scale(0.70) !important;
    transform-origin: center center !important;
}

#aladin-cosmic-command-test .gv-native-simbad-moved svg,
#aladin-cosmic-command-test .gv-native-simbad-moved img,
#aladin-cosmic-command-test .gv-native-simbad-moved canvas {
    max-width: 70% !important;
    max-height: 70% !important;
}'''

old_helper_color = '''    color: var(--text-blue) !important;
    font-family: Arial, Helvetica, sans-serif !important;'''

new_helper_color = '''    color: #FFD166 !important;
    font-family: Arial, Helvetica, sans-serif !important;'''

old_helper_shadow = '''    text-shadow: 0 0 4px rgba(98, 216, 255, 0.38) !important;'''
new_helper_shadow = '''    text-shadow: 0 0 4px rgba(255, 209, 102, 0.45) !important;'''

if old_target_css not in source:
    raise RuntimeError("viewer-0010: target CSS anchor was not found")
if old_helper_color not in source:
    raise RuntimeError("viewer-0010: helper color anchor was not found")
if old_helper_shadow not in source:
    raise RuntimeError("viewer-0010: helper shadow anchor was not found")

source = source.replace(old_target_css, new_target_css, 1)
source = source.replace(old_helper_color, new_helper_color, 1)
source = source.replace(old_helper_shadow, new_helper_shadow, 1)
source = source.replace("# viewer-0007", "# viewer-0010", 1)

exec(compile(source, "viewer-0010.py", "exec"))
