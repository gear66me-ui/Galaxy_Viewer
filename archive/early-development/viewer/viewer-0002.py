from __future__ import annotations

import urllib.request

# viewer-0002
# Controlled revision of viewer-0001.
# Only the SIMBAD Pointer placement/sizing logic is changed:
# - the original lower-row pointer is hidden and its gap collapses
# - a compact 56 px target cell is anchored directly to the coordinate box
# - the approved palette and all other viewer settings remain unchanged

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

NEW_TARGET_CSS = r'''/* Compact engineering target visibly joined to the coordinate box. */
#aladin-cosmic-command-test #gv-simbad-coordinate-target {
    position: absolute !important;
    z-index: 5000 !important;
    display: flex !important;
    flex: none !important;
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
    display: block !important;
    flex: none !important;
    width: 34px !important;
    min-width: 34px !important;
    max-width: 34px !important;
    height: 34px !important;
    min-height: 34px !important;
    max-height: 34px !important;
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

        /*
        Keep the custom button in the viewer root. Aladin internal toolbar
        containers may clip or suppress added children.
        */
        if (targetButton.parentElement !== root) {
            root.appendChild(targetButton);
        }

        const rootRect = root.getBoundingClientRect();
        const coordinateRect = coordinateBox.getBoundingClientRect();
        const size = Math.max(44, Math.min(56, Math.round(coordinateRect.height)));
        const iconSize = Math.max(28, Math.min(34, Math.round(size * 0.61)));
        const left = Math.round(coordinateRect.right - rootRect.left - 1);
        const top = Math.round(
            coordinateRect.top - rootRect.top +
            (coordinateRect.height - size) / 2
        );

        targetButton.style.setProperty("position", "absolute", "important");
        targetButton.style.setProperty("left", left + "px", "important");
        targetButton.style.setProperty("top", top + "px", "important");
        targetButton.style.setProperty("right", "auto", "important");
        targetButton.style.setProperty("bottom", "auto", "important");
        targetButton.style.setProperty("width", size + "px", "important");
        targetButton.style.setProperty("min-width", size + "px", "important");
        targetButton.style.setProperty("max-width", size + "px", "important");
        targetButton.style.setProperty("height", size + "px", "important");
        targetButton.style.setProperty("min-height", size + "px", "important");
        targetButton.style.setProperty("max-height", size + "px", "important");
        targetButton.style.setProperty("transform", "none", "important");
        targetButton.style.setProperty("visibility", "visible", "important");
        targetButton.style.setProperty("opacity", "1", "important");

        const svg = targetButton.querySelector("svg");
        if (svg) {
            svg.style.setProperty("width", iconSize + "px", "important");
            svg.style.setProperty("min-width", iconSize + "px", "important");
            svg.style.setProperty("max-width", iconSize + "px", "important");
            svg.style.setProperty("height", iconSize + "px", "important");
            svg.style.setProperty("min-height", iconSize + "px", "important");
            svg.style.setProperty("max-height", iconSize + "px", "important");
        }
    }'''

if OLD_TARGET_CSS not in source:
    raise RuntimeError("viewer-0002: expected target CSS block was not found")
if OLD_POSITION_FUNCTION not in source:
    raise RuntimeError("viewer-0002: expected positioning function was not found")

source = source.replace(OLD_TARGET_CSS, NEW_TARGET_CSS, 1)
source = source.replace(OLD_POSITION_FUNCTION, NEW_POSITION_FUNCTION, 1)

# Verification guards. Refuse to execute if the requested implementation is absent.
required_fragments = (
    'root.appendChild(targetButton);',
    'coordinateRect.right - rootRect.left - 1',
    'width: 56px !important;',
    'height: 56px !important;',
    'width: 34px !important;',
    'visibility", "visible"',
)
for fragment in required_fragments:
    if fragment not in source:
        raise RuntimeError(
            f"viewer-0002: required target implementation is missing: {fragment}"
        )

if 'coordinateBox.insertAdjacentElement("afterend", targetButton);' in source:
    raise RuntimeError("viewer-0002: clipped sibling-placement method survived")

exec(compile(source, "viewer-0002-generated.py", "exec"))
