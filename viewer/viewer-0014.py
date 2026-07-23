from urllib.request import urlopen

# viewer-0014
# Applies only the approved standalone-target corrections to viewer-0007:
# 1. Restore the coordinate box's original rounded right corners.
# 2. Make the SIMBAD target a separate standalone control.
# 3. Copy the visible coordinate-cell border color, width, style, and radius.
# 4. Keep the target box height matched to the coordinate box.
# 5. Keep the target symbol at one true 90-percent scale.
# 6. Use a technical monospace helper font while preserving yellow text.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0007.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_coordinate_css = '''#aladin-cosmic-command-test .gv-native-coordinate-target-row > .aladin-location,
#aladin-cosmic-command-test .gv-native-coordinate-target-row > .aladin-coordinates {
    position: static !important;
    inset: auto !important;
    margin: 0 !important;
    transform: none !important;
    border-top-right-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
}'''

new_coordinate_css = '''#aladin-cosmic-command-test .gv-native-coordinate-target-row > .aladin-location,
#aladin-cosmic-command-test .gv-native-coordinate-target-row > .aladin-coordinates {
    position: static !important;
    inset: auto !important;
    margin: 0 !important;
    transform: none !important;
}'''

old_target_css = '''#aladin-cosmic-command-test .gv-native-simbad-moved {
    position: static !important;
    inset: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    transform: none !important;
    flex: 0 0 auto !important;
    align-self: stretch !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    border-left-width: 1px !important;
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
}'''

new_target_css = '''#aladin-cosmic-command-test .gv-native-simbad-moved {
    position: static !important;
    inset: auto !important;
    margin: 0 0 0 8px !important;
    padding: 0 !important;
    transform: none !important;
    flex: 0 0 auto !important;
    align-self: stretch !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

/* Scale the native blue finder symbol exactly once to 90 percent. */
#aladin-cosmic-command-test .gv-native-simbad-moved > * {
    transform: scale(0.90) !important;
    transform-origin: center center !important;
}'''

old_helper_font = '''    font-family: Arial, Helvetica, sans-serif !important;
    font-size: 11px !important;'''
new_helper_font = '''    font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.15px !important;'''

old_helper_color = '''    color: var(--text-blue) !important;
    font-family:''' 
new_helper_color = '''    color: #FFD166 !important;
    font-family:'''

old_helper_shadow = '''    text-shadow: 0 0 4px rgba(98, 216, 255, 0.38) !important;'''
new_helper_shadow = '''    text-shadow: 0 0 4px rgba(255, 209, 102, 0.45) !important;'''

old_geometry_function = '''    function synchronizeTargetGeometry(coordinateBox, nativePointer) {
        const coordinateRect = coordinateBox.getBoundingClientRect();
        const coordinateStyle = window.getComputedStyle(coordinateBox);

        const height = Math.max(1, Math.round(coordinateRect.height));
        const rightRadius = coordinateStyle.borderTopRightRadius || "3px";

        nativePointer.style.setProperty("width", height + "px", "important");
        nativePointer.style.setProperty("min-width", height + "px", "important");
        nativePointer.style.setProperty("max-width", height + "px", "important");
        nativePointer.style.setProperty("height", height + "px", "important");
        nativePointer.style.setProperty("min-height", height + "px", "important");
        nativePointer.style.setProperty("max-height", height + "px", "important");

        nativePointer.style.setProperty("border-top-style", coordinateStyle.borderTopStyle, "important");
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
        nativePointer.style.setProperty("border-left-color", coordinateStyle.borderRightColor, "important");

        nativePointer.style.setProperty("border-top-right-radius", rightRadius, "important");
        nativePointer.style.setProperty("border-bottom-right-radius", coordinateStyle.borderBottomRightRadius || rightRadius, "important");
    }'''

new_geometry_function = '''    function synchronizeTargetGeometry(coordinateBox, nativePointer) {
        const coordinateRect = coordinateBox.getBoundingClientRect();
        const height = Math.max(1, Math.round(coordinateRect.height));
        const boxWidth = Math.max(height, Math.round(height * 1.08));

        /*
        Find the actual visible bordered coordinate cell. The outer Aladin
        wrapper itself can report border-style:none, which caused the finder
        outline to disappear in earlier revisions.
        */
        const candidates = [coordinateBox, ...coordinateBox.querySelectorAll("*")]
            .map(element => {
                const rect = element.getBoundingClientRect();
                const style = window.getComputedStyle(element);
                const width = parseFloat(style.borderRightWidth) || 0;
                const visible =
                    style.borderRightStyle !== "none" &&
                    width > 0 &&
                    style.borderRightColor !== "transparent" &&
                    style.borderRightColor !== "rgba(0, 0, 0, 0)";

                return {
                    element,
                    rect,
                    style,
                    visible,
                    rightDistance: Math.abs(rect.right - coordinateRect.right),
                    area: rect.width * rect.height
                };
            })
            .filter(item => item.visible && item.rect.width > 0 && item.rect.height > 0)
            .sort((a, b) =>
                a.rightDistance - b.rightDistance ||
                b.area - a.area
            );

        const borderStyle = candidates.length
            ? candidates[0].style
            : window.getComputedStyle(coordinateBox);

        const borderColor =
            borderStyle.borderRightColor &&
            borderStyle.borderRightColor !== "transparent" &&
            borderStyle.borderRightColor !== "rgba(0, 0, 0, 0)"
                ? borderStyle.borderRightColor
                : "rgb(236, 236, 236)";

        const borderWidth =
            parseFloat(borderStyle.borderRightWidth) > 0
                ? borderStyle.borderRightWidth
                : "1px";

        const borderLineStyle =
            borderStyle.borderRightStyle !== "none"
                ? borderStyle.borderRightStyle
                : "solid";

        const radius =
            borderStyle.borderTopRightRadius &&
            borderStyle.borderTopRightRadius !== "0px"
                ? borderStyle.borderTopRightRadius
                : (
                    borderStyle.borderTopLeftRadius &&
                    borderStyle.borderTopLeftRadius !== "0px"
                        ? borderStyle.borderTopLeftRadius
                        : "6px"
                );

        nativePointer.style.setProperty("width", boxWidth + "px", "important");
        nativePointer.style.setProperty("min-width", boxWidth + "px", "important");
        nativePointer.style.setProperty("max-width", boxWidth + "px", "important");
        nativePointer.style.setProperty("height", height + "px", "important");
        nativePointer.style.setProperty("min-height", height + "px", "important");
        nativePointer.style.setProperty("max-height", height + "px", "important");

        nativePointer.style.setProperty("border-style", borderLineStyle, "important");
        nativePointer.style.setProperty("border-width", borderWidth, "important");
        nativePointer.style.setProperty("border-color", borderColor, "important");
        nativePointer.style.setProperty("border-radius", radius, "important");
    }'''

required_anchors = (
    ("coordinate CSS", old_coordinate_css),
    ("target CSS", old_target_css),
    ("helper font", old_helper_font),
    ("helper color", old_helper_color),
    ("helper shadow", old_helper_shadow),
    ("geometry function", old_geometry_function),
)

for label, anchor in required_anchors:
    if anchor not in source:
        raise RuntimeError(f"viewer-0014: {label} anchor was not found")

source = source.replace(old_coordinate_css, new_coordinate_css, 1)
source = source.replace(old_target_css, new_target_css, 1)
source = source.replace(old_helper_font, new_helper_font, 1)
source = source.replace(old_helper_color, new_helper_color, 1)
source = source.replace(old_helper_shadow, new_helper_shadow, 1)
source = source.replace(old_geometry_function, new_geometry_function, 1)
source = source.replace("# viewer-0007", "# viewer-0014", 1)

# Ten explicit pre-execution integrity checks.
checks = (
    ("standalone gap", "margin: 0 0 0 8px !important;"),
    ("coordinate corners restored", "border-top-right-radius: 0 !important;"),
    ("single 90-percent scale", "transform: scale(0.90) !important;"),
    ("no duplicate max-width scaling", "max-width: 90% !important;"),
    ("visible-border descendant scan", "coordinateBox.querySelectorAll(\"*\")"),
    ("border color copied", 'nativePointer.style.setProperty("border-color", borderColor'),
    ("border width copied", 'nativePointer.style.setProperty("border-width", borderWidth'),
    ("all corners rounded", 'nativePointer.style.setProperty("border-radius", radius'),
    ("technical font", 'font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace'),
    ("yellow helper preserved", "color: #FFD166 !important;"),
)

for label, token in checks:
    present = token in source
    if label in ("coordinate corners restored", "no duplicate max-width scaling"):
        present = not present
    if not present:
        raise RuntimeError(f"viewer-0014 integrity check failed: {label}")

exec(compile(source, "viewer-0014.py", "exec"))
