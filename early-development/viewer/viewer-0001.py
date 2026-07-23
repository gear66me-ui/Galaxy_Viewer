from IPython.display import HTML, display

# viewer-0001
# Aladin Lite v3.8.2 with the approved cosmic palette.
# The native SIMBAD Pointer is represented by a compact engineering target
# joined directly to the right side of the coordinate block.

display(HTML(r"""
<link
  rel="stylesheet"
  href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css"
/>

<style>
#aladin-cosmic-command-test {
    width: 100%;
    height: 650px;
    position: relative !important;

    --text-blue:       #62D8FF;
    --copy-blue:       #7DF4FF;
    --layers-blue:     #4F9DFF;
    --target-blue:     #2F7BFF;
    --world-blue:      #8B7CFF;
    --projection-blue: #6FC7FF;
    --fullscreen-blue: #BCEEFF;
    --border-blue:     #247EAE;
    --zoom-plus:       #55FF88;
    --zoom-minus:      #FF5E78;
}

#aladin-cosmic-command-test .gv-standard-text,
#aladin-cosmic-command-test .gv-standard-text * {
    color: var(--text-blue) !important;
    fill: var(--text-blue) !important;
    text-shadow: 0 0 5px rgba(98, 216, 255, 0.55) !important;
}

#aladin-cosmic-command-test .gv-copy       { --command-color: var(--copy-blue); }
#aladin-cosmic-command-test .gv-layers     { --command-color: var(--layers-blue); }
#aladin-cosmic-command-test .gv-target     { --command-color: var(--target-blue); }
#aladin-cosmic-command-test .gv-world      { --command-color: var(--world-blue); }
#aladin-cosmic-command-test .gv-projection { --command-color: var(--projection-blue); }
#aladin-cosmic-command-test .gv-fullscreen { --command-color: var(--fullscreen-blue); }
#aladin-cosmic-command-test .gv-plus       { --command-color: var(--zoom-plus); }
#aladin-cosmic-command-test .gv-minus      { --command-color: var(--zoom-minus); }

#aladin-cosmic-command-test .gv-command,
#aladin-cosmic-command-test .gv-command * {
    color: var(--command-color) !important;
}

#aladin-cosmic-command-test .gv-command svg,
#aladin-cosmic-command-test .gv-command svg * {
    color: var(--command-color) !important;
}

#aladin-cosmic-command-test .gv-command svg path,
#aladin-cosmic-command-test .gv-command svg line,
#aladin-cosmic-command-test .gv-command svg polyline,
#aladin-cosmic-command-test .gv-command svg polygon,
#aladin-cosmic-command-test .gv-command svg circle,
#aladin-cosmic-command-test .gv-command svg ellipse,
#aladin-cosmic-command-test .gv-command svg rect {
    stroke: var(--command-color) !important;
}

#aladin-cosmic-command-test .gv-command svg path[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg polygon[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg circle[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg rect[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg text,
#aladin-cosmic-command-test .gv-command svg tspan {
    fill: var(--command-color) !important;
}

#aladin-cosmic-command-test .gv-command img,
#aladin-cosmic-command-test .gv-command canvas {
    filter: var(--command-filter) !important;
}

/* Remove the original SIMBAD Pointer completely from the lower icon row. */
#aladin-cosmic-command-test .gv-native-simbad-hidden {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    min-width: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
}

/* Close the remaining lower-row space so Layers and World touch. */
#aladin-cosmic-command-test .gv-compact-icon-row {
    gap: 0 !important;
    column-gap: 0 !important;
    row-gap: 0 !important;
}

#aladin-cosmic-command-test .gv-compact-icon-row > * {
    margin-left: 0 !important;
    margin-right: 0 !important;
}

/* Coordinate box is the left side of a single joined assembly. */
#aladin-cosmic-command-test .gv-coordinate-joined {
    border-top-right-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
    box-sizing: border-box !important;
}

/* Compact engineering target joined to the coordinate box. */
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
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target svg circle,
#aladin-cosmic-command-test #gv-simbad-coordinate-target svg line {
    stroke: var(--target-blue) !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target .gv-target-dot {
    fill: var(--target-blue) !important;
    stroke: none !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target.gv-active {
    background: rgba(10, 25, 65, 0.98) !important;
    box-shadow:
        0 0 10px rgba(47, 123, 255, 0.95),
        inset 0 0 8px rgba(47, 123, 255, 0.45) !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target:hover {
    filter: drop-shadow(0 0 6px var(--target-blue)) brightness(1.15);
}
</style>

<div id="aladin-cosmic-command-test"></div>

<script
  src="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js"
  charset="utf-8">
</script>

<script>
A.init.then(() => {
    window.aladin_cosmic_command_test = A.aladin(
        "#aladin-cosmic-command-test",
        {
            target: "M 31",
            survey: "P/DSS2/color",
            fov: 1.5,
            cooFrame: "ICRSd",
            projection: "TAN",
            reticleColor: "#62D8FF",
            reticleSize: 22,
            showReticle: true,
            showZoomControl: true,
            showFullscreenControl: true,
            showLayersControl: true,
            showGotoControl: true,
            showCooGridControl: true,
            showSimbadPointerControl: true,
            showProjectionControl: true
        }
    );

    const root = document.getElementById("aladin-cosmic-command-test");

    const filters = {
        copy:
            "brightness(0) saturate(100%) invert(94%) sepia(44%) " +
            "saturate(1415%) hue-rotate(160deg) brightness(103%) contrast(103%)",
        layers:
            "brightness(0) saturate(100%) invert(58%) sepia(99%) " +
            "saturate(1819%) hue-rotate(190deg) brightness(102%) contrast(101%)",
        target:
            "brightness(0) saturate(100%) invert(42%) sepia(96%) " +
            "saturate(4214%) hue-rotate(218deg) brightness(103%) contrast(105%)",
        world:
            "brightness(0) saturate(100%) invert(55%) sepia(94%) " +
            "saturate(1690%) hue-rotate(219deg) brightness(101%) contrast(101%)",
        projection:
            "brightness(0) saturate(100%) invert(79%) sepia(38%) " +
            "saturate(1260%) hue-rotate(172deg) brightness(101%) contrast(102%)",
        fullscreen:
            "brightness(0) saturate(100%) invert(94%) sepia(21%) " +
            "saturate(996%) hue-rotate(171deg) brightness(104%) contrast(102%)",
        plus:
            "brightness(0) saturate(100%) invert(84%) sepia(66%) " +
            "saturate(654%) hue-rotate(77deg) brightness(105%) contrast(104%)",
        minus:
            "brightness(0) saturate(100%) invert(53%) sepia(84%) " +
            "saturate(3287%) hue-rotate(319deg) brightness(105%) contrast(101%)"
    };

    function describe(element) {
        return [
            element.className || "",
            element.id || "",
            element.getAttribute?.("title") || "",
            element.getAttribute?.("aria-label") || "",
            element.getAttribute?.("data-tooltip") || "",
            element.textContent || ""
        ].join(" ").toLowerCase();
    }

    function controlContainer(element) {
        return element.closest(
            "button, [role='button'], " +
            "[class*='Control'], [class*='control'], " +
            "[class*='projection'], [class*='fullscreen'], " +
            "[class*='location']"
        ) || element;
    }

    function mark(element, className, filterName) {
        const control = controlContainer(element);
        control.classList.add("gv-command", className);
        control.style.setProperty(
            "--command-filter",
            filters[filterName],
            "important"
        );
    }

    function findNativeSimbadPointer() {
        return (
            root.querySelector(".aladin-simbadPointerControl") ||
            root.querySelector("[class*='simbadPointer']")
        );
    }

    function findCoordinateBox() {
        const rootRect = root.getBoundingClientRect();
        const candidates = [];
        const selectors = [
            ".aladin-location",
            ".aladin-coordinates",
            "[class*='location']",
            "[class*='coordinates']"
        ];

        selectors.forEach(selector => {
            root.querySelectorAll(selector).forEach(element => {
                if (
                    element.id === "gv-simbad-coordinate-target" ||
                    element.closest("#gv-simbad-coordinate-target")
                ) {
                    return;
                }

                const rect = element.getBoundingClientRect();
                const text = (element.textContent || "").trim();
                const relativeTop = rect.top - rootRect.top;
                const relativeLeft = rect.left - rootRect.left;
                const digitCount = (text.match(/\d/g) || []).length;
                const looksLikeCoordinates =
                    /[-+]?\d+(\.\d+)?\s+[-+]?\d+(\.\d+)?/.test(text);

                if (
                    looksLikeCoordinates &&
                    rect.width >= 250 &&
                    rect.width <= 900 &&
                    rect.height >= 40 &&
                    rect.height <= 100 &&
                    relativeTop >= 0 &&
                    relativeTop < 150 &&
                    relativeLeft >= 0 &&
                    relativeLeft < rootRect.width * 0.75
                ) {
                    candidates.push({
                        element,
                        score: rect.width + digitCount * 25 - relativeTop
                    });
                }
            });
        });

        candidates.sort((a, b) => b.score - a.score);
        return candidates.length ? candidates[0].element : null;
    }

    function createCoordinateTarget() {
        let button = root.querySelector("#gv-simbad-coordinate-target");
        if (button) return button;

        button = document.createElement("button");
        button.id = "gv-simbad-coordinate-target";
        button.type = "button";
        button.title = "SIMBAD Pointer";
        button.setAttribute("aria-label", "Activate SIMBAD Pointer");
        button.innerHTML = `
            <svg viewBox="0 0 100 100" aria-hidden="true">
                <circle cx="50" cy="50" r="29" fill="none" stroke-width="5"/>
                <circle cx="50" cy="50" r="12" fill="none" stroke-width="4"/>
                <line x1="50" y1="4" x2="50" y2="35" stroke-width="5"/>
                <line x1="50" y1="65" x2="50" y2="96" stroke-width="5"/>
                <line x1="4" y1="50" x2="35" y2="50" stroke-width="5"/>
                <line x1="65" y1="50" x2="96" y2="50" stroke-width="5"/>
                <circle class="gv-target-dot" cx="50" cy="50" r="4"/>
            </svg>
        `;

        button.addEventListener("click", event => {
            event.preventDefault();
            event.stopPropagation();
            const nativePointer = findNativeSimbadPointer();
            if (!nativePointer) return;
            nativePointer.click();
            button.classList.toggle("gv-active");
        });

        root.appendChild(button);
        return button;
    }

    function compactNativePointerRow() {
        const nativePointer = findNativeSimbadPointer();
        if (!nativePointer) return;

        const parent = nativePointer.parentElement;
        nativePointer.classList.add("gv-native-simbad-hidden");

        if (parent) {
            parent.classList.add("gv-compact-icon-row");
            parent.style.setProperty("gap", "0px", "important");
            parent.style.setProperty("column-gap", "0px", "important");
            parent.style.setProperty("row-gap", "0px", "important");
        }
    }

    function positionCoordinateTarget() {
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
    }

    function applyPalette() {
        root.querySelectorAll("*").forEach(element => {
            const description = describe(element);
            const text = (element.textContent || "").trim();

            if (description.includes("copy") || description.includes("clipboard")) {
                mark(element, "gv-copy", "copy");
            }
            if (description.includes("layer") || description.includes("stack")) {
                mark(element, "gv-layers", "layers");
            }
            if (
                description.includes("world") ||
                description.includes("globe") ||
                description.includes("grid")
            ) {
                mark(element, "gv-world", "world");
            }
            if (
                description.includes("projection") ||
                text === "TAN" ||
                text === "SIN"
            ) {
                mark(element, "gv-projection", "projection");
            }
            if (
                description.includes("fullscreen") ||
                description.includes("full screen") ||
                description.includes("maximize")
            ) {
                mark(element, "gv-fullscreen", "fullscreen");
            }
            if (
                description.includes("zoom in") ||
                description.includes("zoomin") ||
                text === "+"
            ) {
                mark(element, "gv-plus", "plus");
            }
            if (
                description.includes("zoom out") ||
                description.includes("zoomout") ||
                text === "-" ||
                text === "−"
            ) {
                mark(element, "gv-minus", "minus");
            }
            if (
                text === "ICRS" ||
                text === "ICRSd" ||
                /^[-+]?\d+(\.\d+)?\s+[-+]?\d+(\.\d+)?$/.test(text) ||
                /^\d+(\.\d+)?\s*°?\s*[x×]\s*\d+(\.\d+)?\s*°?$/.test(text)
            ) {
                element.classList.add("gv-standard-text");
            }
        });

        root.querySelectorAll(".aladin-layersControl")
            .forEach(element => mark(element, "gv-layers", "layers"));

        root.querySelectorAll(".aladin-gridControl, [class*='gridControl']")
            .forEach(element => mark(element, "gv-world", "world"));

        root.querySelectorAll(".aladin-projectionControl, [class*='projection']")
            .forEach(element => mark(element, "gv-projection", "projection"));

        root.querySelectorAll(
            ".aladin-fullscreen, .aladin-fullscreenControl, [class*='fullscreen']"
        ).forEach(element => mark(element, "gv-fullscreen", "fullscreen"));

        root.querySelectorAll(
            ".aladin-location, .aladin-coordinates, .aladin-frameChoice, .aladin-fov"
        ).forEach(element => element.classList.add("gv-standard-text"));

        compactNativePointerRow();
        positionCoordinateTarget();
    }

    setTimeout(applyPalette, 250);
    setTimeout(applyPalette, 700);
    setTimeout(applyPalette, 1400);
    setTimeout(applyPalette, 2400);

    window.addEventListener("resize", positionCoordinateTarget);

    const viewerResizeObserver = new ResizeObserver(() => {
        positionCoordinateTarget();
    });
    viewerResizeObserver.observe(root);
});
</script>
"""))
