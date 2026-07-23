from urllib.request import urlopen

# viewer-0012
# Corrects the viewer-0011 double-scaling issue:
# 1. Keep the finder height matched to the coordinate box.
# 2. Keep the finder width enlarged by 8 percent.
# 3. Scale the native blue finder symbol exactly once to 90 percent.
# 4. Preserve the live coordinate-box border hue and yellow helper text.

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

/* Scale the native blue finder symbol exactly once to 90 percent. */
#aladin-cosmic-command-test .gv-native-simbad-moved > * {
    transform: scale(0.90) !important;
    transform-origin: center center !important;
}'''

old_geometry = '''        const height = Math.max(1, Math.round(coordinateRect.height));
        const rightRadius = coordinateStyle.borderTopRightRadius || "3px";

        nativePointer.style.setProperty("width", height + "px", "important");
        nativePointer.style.setProperty("min-width", height + "px", "important");
        nativePointer.style.setProperty("max-width", height + "px", "important");'''

new_geometry = '''        const height = Math.max(1, Math.round(coordinateRect.height));
        const boxWidth = Math.max(height, Math.round(height * 1.08));
        const rightRadius = coordinateStyle.borderTopRightRadius || "3px";

        nativePointer.style.setProperty("width", boxWidth + "px", "important");
        nativePointer.style.setProperty("min-width", boxWidth + "px", "important");
        nativePointer.style.setProperty("max-width", boxWidth + "px", "important");'''

old_helper_color = '''    color: var(--text-blue) !important;
    font-family: Arial, Helvetica, sans-serif !important;'''

new_helper_color = '''    color: #FFD166 !important;
    font-family: Arial, Helvetica, sans-serif !important;'''

old_helper_shadow = '''    text-shadow: 0 0 4px rgba(98, 216, 255, 0.38) !important;'''
new_helper_shadow = '''    text-shadow: 0 0 4px rgba(255, 209, 102, 0.45) !important;'''

if old_target_css not in source:
    raise RuntimeError("viewer-0012: target CSS anchor was not found")
if old_geometry not in source:
    raise RuntimeError("viewer-0012: target geometry anchor was not found")
if old_helper_color not in source:
    raise RuntimeError("viewer-0012: helper color anchor was not found")
if old_helper_shadow not in source:
    raise RuntimeError("viewer-0012: helper shadow anchor was not found")

source = source.replace(old_target_css, new_target_css, 1)
source = source.replace(old_geometry, new_geometry, 1)
source = source.replace(old_helper_color, new_helper_color, 1)
source = source.replace(old_helper_shadow, new_helper_shadow, 1)
source = source.replace("# viewer-0007", "# viewer-0012", 1)

exec(compile(source, "viewer-0012.py", "exec"))
