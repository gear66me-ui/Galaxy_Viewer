from __future__ import annotations

import urllib.request

# viewer-0002
# Controlled revision of viewer-0001.
# Only the SIMBAD Pointer placement/sizing logic is changed:
# - the original lower-row pointer is hidden and its gap collapses
# - a compact target cell is inserted directly after the coordinate block
# - no absolute screen-position calculation is used

BASE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "main/early-development/viewer/viewer-0001.py"
)

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace("# viewer-0001", "# viewer-0002", 1)

OLD_TARGET_CSS = r'''/* Compact engineering target joined to the coordinate box. */
#aladin-cosmic-command-test #gv-simbad-coordinate-target {
    position: absolute !important;
    z-index: 5000 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    background: rgba(0, 0, 0, 0.92) !important;
    border-top: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
    border-left: 1px solid #ffffff !important;
    border-radius: 0 7px 7px 0 !important;
    color: var(--target-blue) !important;
    cursor: pointer !important;
    touch-action: manipulation !important;
    transform: none !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target svg {
    width: 72% !important;
    height: 72% !important;
    max-width: 72% !important;
    max-height: 72% !important;
    overflow: visible !important;
}'''

NEW_TARGET_CSS = r'''/* Coordinate row used only to join the compact SIMBAD target cell. */
#aladin-cosmic-command-test .gv-coordinate-target-row {
    display: flex !important;
    flex-flow: row nowrap !important;
    align-items: stretch !important;
    gap: 0 !important;
    column-gap: 0 !important;
    width: max-content !important;
    max-width: 100% !important;
}

/* Compact engineering target joined to the coordinate box. */
#aladin-cosmic-command-test #gv-simbad-coordinate-target {
    position: static !important;
    z-index: auto !important;
    display: flex !important;
    flex: 0 0 56px !important;
    align-items: center !important;
    justify-content: center !important;
    width: 56px !important;
    min-width: 56px !important;
    max-width: 56px !important;
    height: 56px !important;
    min-height: 56px !important;
    max-height: 56px !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    background: rgba(0, 0, 0, 0.92) !important;
    border-top: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
    border-left: 1px solid #ffffff !important;
    border-radius: 0 7px 7px 0 !important;
    color: var(--target-blue) !important;
    cursor: pointer !important;
    touch-action: manipulation !important;
    transform: none !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target svg {
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    min-height: 36px !important;
    max-width: 36px !important;
    max-height: 36px !important;
    overflow: visible !important;
}'''

OLD_POSITION_FUNCTION = r'''    function positionCoordinateTarget() {
        const coordinateBox = findCoordinateBox();
        const targetButton = createCoordinateTarget();
        if (!coordinateBox || !targetButton) return;

        coordinateBox.classList.add("gv-coordinate-joined", "gv-standard-text");

        const rootRect = root.getBoundingClientRect();
        const coordinateRect = coordinateBox.getBoundingClientRect();
        const size = Math.max(44, Math.min(64, Math.round(coordinateRect.height)));
        const left = Math.round(coordinateRect.right - rootRect.left - 1);
        const top = Math.round(coordinateRect.top - rootRect.top);

        targetButton.style.setProperty("left", left + "px", "important");
        targetButton.style.setProperty("top", top + "px", "important");
        targetButton.style.setProperty("width", size + "px", "important");
        targetButton.style.setProperty("min-width", size + "px", "important");
        targetButton.style.setProperty("max-width", size + "px", "important");
        targetButton.style.setProperty("height", size + "px", "important");
        targetButton.style.setProperty("min-height", size + "px", "important");
        targetButton.style.setProperty("max-height", size + "px", "important");
        targetButton.style.setProperty("transform", "none", "important");
    }'''

NEW_POSITION_FUNCTION = r'''    function positionCoordinateTarget() {
        const coordinateBox = findCoordinateBox();
        const targetButton = createCoordinateTarget();
        if (!coordinateBox || !targetButton) return;

        coordinateBox.classList.add("gv-coordinate-joined", "gv-standard-text");

        const coordinateParent = coordinateBox.parentElement;
        if (!coordinateParent) return;

        coordinateParent.classList.add("gv-coordinate-target-row");
        coordinateParent.style.setProperty("display", "flex", "important");
        coordinateParent.style.setProperty("flex-flow", "row nowrap", "important");
        coordinateParent.style.setProperty("align-items", "stretch", "important");
        coordinateParent.style.setProperty("gap", "0px", "important");
        coordinateParent.style.setProperty("column-gap", "0px", "important");

        if (
            targetButton.parentElement !== coordinateParent ||
            coordinateBox.nextElementSibling !== targetButton
        ) {
            coordinateBox.insertAdjacentElement("afterend", targetButton);
        }

        const coordinateRect = coordinateBox.getBoundingClientRect();
        const size = Math.max(44, Math.min(64, Math.round(coordinateRect.height)));
        const iconSize = Math.max(28, Math.min(38, Math.round(size * 0.64)));

        targetButton.style.setProperty("position", "static", "important");
        targetButton.style.setProperty("left", "auto", "important");
        targetButton.style.setProperty("top", "auto", "important");
        targetButton.style.setProperty("right", "auto", "important");
        targetButton.style.setProperty("bottom", "auto", "important");
        targetButton.style.setProperty("flex", `0 0 ${size}px`, "important");
        targetButton.style.setProperty("width", size + "px", "important");
        targetButton.style.setProperty("min-width", size + "px", "important");
        targetButton.style.setProperty("max-width", size + "px", "important");
        targetButton.style.setProperty("height", size + "px", "important");
        targetButton.style.setProperty("min-height", size + "px", "important");
        targetButton.style.setProperty("max-height", size + "px", "important");
        targetButton.style.setProperty("transform", "none", "important");

        const svg = targetButton.querySelector("svg");
        if (svg) {
            svg.style.setProperty("width", iconSize + "px", "important");
            svg.style.setProperty("height", iconSize + "px", "important");
            svg.style.setProperty("min-width", iconSize + "px", "important");
            svg.style.setProperty("min-height", iconSize + "px", "important");
            svg.style.setProperty("max-width", iconSize + "px", "important");
            svg.style.setProperty("max-height", iconSize + "px", "important");
        }
    }'''

if OLD_TARGET_CSS not in source:
    raise RuntimeError("viewer-0002: expected target CSS block was not found")
if OLD_POSITION_FUNCTION not in source:
    raise RuntimeError("viewer-0002: expected positioning function was not found")

source = source.replace(OLD_TARGET_CSS, NEW_TARGET_CSS, 1)
source = source.replace(OLD_POSITION_FUNCTION, NEW_POSITION_FUNCTION, 1)

# Verification guards: refuse to execute if the dangerous old positioning survived.
if "position: absolute !important;\n    z-index: 5000" in source:
    raise RuntimeError("viewer-0002: absolute target positioning was not removed")
if 'const left = Math.round(coordinateRect.right - rootRect.left - 1);' in source:
    raise RuntimeError("viewer-0002: old screen-coordinate positioning survived")
if 'coordinateBox.insertAdjacentElement("afterend", targetButton);' not in source:
    raise RuntimeError("viewer-0002: target is not joined after the coordinate block")

exec(compile(source, "viewer-0002-generated.py", "exec"))
