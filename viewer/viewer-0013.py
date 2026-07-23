from urllib.request import urlopen

# viewer-0013
# Fixes the missing visible finder box in viewer-0012.
# 1. Keep finder height matched to the coordinate box.
# 2. Keep finder width enlarged by 8 percent.
# 3. Scale the native blue finder symbol exactly once to 90 percent.
# 4. Force a visible coordinate-matched light border around the finder.
# 5. Preserve the approved yellow helper text.

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

old_border_block = '''        nativePointer.style.setProperty("border-top-style", coordinateStyle.borderTopStyle, "important");
        nativePointer.style.setProperty("border-right-style", coordinateStyle.borderRightStyle, "important");
        nativePointer.style.setProperty("border-bottom-style", coordinateStyle.borderBottomStyle, "important");
        nativePointer.style.setProperty("border-left-style", coordinateStyle.borderRightStyle, "important");

        nativePointer.style.setProperty("border-top-width", coordinateStyle.borderTopWidth, "important");
        nativePointer.style.setProperty("border-right-width", coordinateStyle.borderRightWidth, "important");
        nativePointer.style.setProperty("border-bottom-width", coordinateStyle.borderBottomWidth, "important");
        nativePointer.style.setProperty("border-left-width", "1px", "important");

        nativePointer.style.setProperty("border-top-color", coordinateStyle.borderTopColor, "important");
        nativePointer.style.setProperty("border-right-color", coordinateStyle.borderRightColor, "important");
        nativePointer.style.setProperty("border-bottom-color", coordinateStyle.borderBottomColor, "important");
        nativePointer.style.setProperty("border-left-color", coordinateStyle.borderRightColor, "important");'''

new_border_block = '''        /*
        The outer Aladin coordinate wrapper reports no usable border in this build.
        Force the same visible light-gray/white stroke seen around the coordinate box.
        */
        const finderBorderColor = "#D8E2EA";

        nativePointer.style.setProperty("border-top-style", "solid", "important");
        nativePointer.style.setProperty("border-right-style", "solid", "important");
        nativePointer.style.setProperty("border-bottom-style", "solid", "important");
        nativePointer.style.setProperty("border-left-style", "solid", "important");

        nativePointer.style.setProperty("border-top-width", "2px", "important");
        nativePointer.style.setProperty("border-right-width", "2px", "important");
        nativePointer.style.setProperty("border-bottom-width", "2px", "important");
        nativePointer.style.setProperty("border-left-width", "1px", "important");

        nativePointer.style.setProperty("border-top-color", finderBorderColor, "important");
        nativePointer.style.setProperty("border-right-color", finderBorderColor, "important");
        nativePointer.style.setProperty("border-bottom-color", finderBorderColor, "important");
        nativePointer.style.setProperty("border-left-color", finderBorderColor, "important");'''

old_helper_color = '''    color: var(--text-blue) !important;
    font-family: Arial, Helvetica, sans-serif !important;'''
new_helper_color = '''    color: #FFD166 !important;
    font-family: Arial, Helvetica, sans-serif !important;'''

old_helper_shadow = '''    text-shadow: 0 0 4px rgba(98, 216, 255, 0.38) !important;'''
new_helper_shadow = '''    text-shadow: 0 0 4px rgba(255, 209, 102, 0.45) !important;'''

for label, anchor in (
    ("target CSS", old_target_css),
    ("target geometry", old_geometry),
    ("target border", old_border_block),
    ("helper color", old_helper_color),
    ("helper shadow", old_helper_shadow),
):
    if anchor not in source:
        raise RuntimeError(f"viewer-0013: {label} anchor was not found")

source = source.replace(old_target_css, new_target_css, 1)
source = source.replace(old_geometry, new_geometry, 1)
source = source.replace(old_border_block, new_border_block, 1)
source = source.replace(old_helper_color, new_helper_color, 1)
source = source.replace(old_helper_shadow, new_helper_shadow, 1)
source = source.replace("# viewer-0007", "# viewer-0013", 1)

exec(compile(source, "viewer-0013.py", "exec"))
