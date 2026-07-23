from IPython.display import HTML, display

# viewer-0007
# Standalone Aladin Lite v3.8.2 viewer.
# Preserves the viewer-0006 palette and controls.
# Refines only the joined SIMBAD target geometry and helper instruction.

display(HTML(r'''
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />

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

/* Coordinate + native SIMBAD pointer occupy one exact flex row. */
#aladin-cosmic-command-test .gv-native-coordinate-target-row {
    position: absolute !important;
    z-index: 5000 !important;
    display: flex !important;
    flex-flow: row nowrap !important;
    align-items: stretch !important;
    gap: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    width: max-content !important;
    box-sizing: border-box !important;
}

#aladin-cosmic-command-test .gv-native-coordinate-target-row > .aladin-location,
#aladin-cosmic-command-test .gv-native-coordinate-target-row > .aladin-coordinates {
    position: static !important;
    inset: auto !important;
    margin: 0 !important;
    transform: none !important;
    border-top-right-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
}

/* Native pointer: dimensions and border are copied from the coordinate box in JS. */
#aladin-cosmic-command-test .gv-native-simbad-moved {
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
}

/* Smaller two-line instruction that stays clear of right-side controls. */
#aladin-cosmic-command-test .gv-simbad-helper {
    display: flex !important;
    align-items: center !important;
    align-self: center !important;
    gap: 6px !important;
    margin: 0 0 0 9px !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    color: var(--text-blue) !important;
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    line-height: 1.12 !important;
    width: 238px !important;
    max-width: 238px !important;
    white-space: normal !important;
    text-shadow: 0 0 4px rgba(98, 216, 255, 0.38) !important;
    pointer-events: none !important;
}

#aladin-cosmic-command-test .gv-simbad-helper-text {
    display: block !important;
    width: 205px !important;
    max-width: 205px !important;
}

#aladin-cosmic-command-test .gv-simbad-helper-arrow {
    width: 19px !important;
    min-width: 19px !important;
    height: 12px !important;
    display: block !important;
    overflow: visible !important;
    color: var(--target-blue) !important;
    filter: drop-shadow(0 0 3px rgba(47, 123, 255, 0.72)) !important;
}

#aladin-cosmic-command-test .gv-simbad-helper-arrow path {
    fill: none !important;
    stroke: currentColor !important;
    stroke-width: 2 !important;
    stroke-linecap: round !important;
    stroke-linejoin: round !important;
}

#aladin-cosmic-command-test .gv-simbad-helper.gv-active .gv-simbad-helper-arrow {
    animation: gv-left-arrow-pulse 1.15s ease-in-out infinite;
}

@keyframes gv-left-arrow-pulse {
    0%, 100% { transform: translateX(0); opacity: 0.82; }
    50%      { transform: translateX(-2px); opacity: 1; }
}
</style>

<div id="aladin-cosmic-command-test"></div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js" charset="utf-8"></script>

<script>
A.init.then(() => {
    const root = document.getElementById("aladin-cosmic-command-test");

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

    const filters = {
        copy: "brightness(0) saturate(100%) invert(94%) sepia(44%) saturate(1415%) hue-rotate(160deg) brightness(103%) contrast(103%)",
        layers: "brightness(0) saturate(100%) invert(58%) sepia(99%) saturate(1819%) hue-rotate(190deg) brightness(102%) contrast(101%)",
        target: "brightness(0) saturate(100%) invert(42%) sepia(96%) saturate(4214%) hue-rotate(218deg) brightness(103%) contrast(105%)",
        world: "brightness(0) saturate(100%) invert(55%) sepia(94%) saturate(1690%) hue-rotate(219deg) brightness(101%) contrast(101%)",
        projection: "brightness(0) saturate(100%) invert(79%) sepia(38%) saturate(1260%) hue-rotate(172deg) brightness(101%) contrast(102%)",
        fullscreen: "brightness(0) saturate(100%) invert(94%) sepia(21%) saturate(996%) hue-rotate(171deg) brightness(104%) contrast(102%)",
        plus: "brightness(0) saturate(100%) invert(84%) sepia(66%) saturate(654%) hue-rotate(77deg) brightness(105%) contrast(104%)",
        minus: "brightness(0) saturate(100%) invert(53%) sepia(84%) saturate(3287%) hue-rotate(319deg) brightness(105%) contrast(101%)"
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
            "button, [role='button'], [class*='Control'], [class*='control'], " +
            "[class*='projection'], [class*='fullscreen'], [class*='location']"
        ) || element;
    }

    function mark(element, className, filterName) {
        const control = controlContainer(element);
        control.classList.add("gv-command", className);
        control.style.setProperty("--command-filter", filters[filterName], "important");
    }

    function findNativeCoordinateBox() {
        return root.querySelector(".aladin-location") ||
               root.querySelector(".aladin-coordinates");
    }

    function findNativeSimbadPointer() {
        return root.querySelector(".aladin-simbadPointerControl") ||
               root.querySelector("[class*='simbadPointer']");
    }

    function ensureHelper(row, nativePointer) {
        let helper = row.querySelector(".gv-simbad-helper");

        if (!helper) {
            helper = document.createElement("div");
            helper.className = "gv-simbad-helper";
            helper.setAttribute("aria-live", "polite");
            helper.innerHTML = `
                <svg class="gv-simbad-helper-arrow" viewBox="0 0 24 14" aria-hidden="true">
                    <path d="M22 7H6"></path>
                    <path d="M11 2L5 7L11 12"></path>
                </svg>
                <span class="gv-simbad-helper-text">Click target, then click<br>a galaxy or star to find info</span>
            `;
        }

        if (helper.parentElement !== row || nativePointer.nextElementSibling !== helper) {
            nativePointer.insertAdjacentElement("afterend", helper);
        }

        if (!nativePointer.dataset.gvHelperBound) {
            nativePointer.dataset.gvHelperBound = "true";
            nativePointer.addEventListener("click", () => {
                const active = helper.classList.toggle("gv-active");
                const text = helper.querySelector(".gv-simbad-helper-text");
                if (text) {
                    text.innerHTML = active
                        ? "Now click a galaxy or star<br>to find information"
                        : "Click target, then click<br>a galaxy or star to find info";
                }
            });
        }

        return helper;
    }

    function synchronizeTargetGeometry(coordinateBox, nativePointer) {
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
    }

    function moveNativeSimbadPointer() {
        const coordinateBox = findNativeCoordinateBox();
        const nativePointer = findNativeSimbadPointer();

        if (!coordinateBox || !nativePointer) return false;

        let row = root.querySelector(".gv-native-coordinate-target-row");

        if (!row) {
            const rootRect = root.getBoundingClientRect();
            const coordinateRect = coordinateBox.getBoundingClientRect();

            if (
                coordinateRect.width <= 0 ||
                coordinateRect.height <= 0 ||
                coordinateRect.left < rootRect.left ||
                coordinateRect.top < rootRect.top ||
                coordinateRect.right > rootRect.right
            ) {
                return false;
            }

            row = document.createElement("div");
            row.className = "gv-native-coordinate-target-row";
            row.style.setProperty("left", Math.round(coordinateRect.left - rootRect.left) + "px", "important");
            row.style.setProperty("top", Math.round(coordinateRect.top - rootRect.top) + "px", "important");

            coordinateBox.parentElement.insertBefore(row, coordinateBox);
            row.appendChild(coordinateBox);
        }

        if (nativePointer.parentElement !== row) {
            row.appendChild(nativePointer);
        }

        nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-target");
        nativePointer.style.setProperty("--command-filter", filters.target, "important");

        synchronizeTargetGeometry(coordinateBox, nativePointer);
        ensureHelper(row, nativePointer);

        return coordinateBox.nextElementSibling === nativePointer;
    }

    function applyPalette() {
        root.querySelectorAll("*").forEach(element => {
            const description = describe(element);
            const text = (element.textContent || "").trim();

            if (description.includes("copy") || description.includes("clipboard")) mark(element, "gv-copy", "copy");
            if (description.includes("layer") || description.includes("stack")) mark(element, "gv-layers", "layers");
            if (description.includes("world") || description.includes("globe") || description.includes("grid")) mark(element, "gv-world", "world");
            if (description.includes("projection") || text === "TAN" || text === "SIN") mark(element, "gv-projection", "projection");
            if (description.includes("fullscreen") || description.includes("full screen") || description.includes("maximize")) mark(element, "gv-fullscreen", "fullscreen");
            if (description.includes("zoom in") || description.includes("zoomin") || text === "+") mark(element, "gv-plus", "plus");
            if (description.includes("zoom out") || description.includes("zoomout") || text === "-" || text === "−") mark(element, "gv-minus", "minus");

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
        root.querySelectorAll(".aladin-fullscreen, .aladin-fullscreenControl, [class*='fullscreen']")
            .forEach(element => mark(element, "gv-fullscreen", "fullscreen"));
        root.querySelectorAll(".aladin-location, .aladin-coordinates, .aladin-frameChoice, .aladin-fov")
            .forEach(element => element.classList.add("gv-standard-text"));

        moveNativeSimbadPointer();
    }

    setTimeout(applyPalette, 250);
    setTimeout(applyPalette, 700);
    setTimeout(applyPalette, 1400);
    setTimeout(applyPalette, 2400);

    window.addEventListener("resize", moveNativeSimbadPointer);
});
</script>
'''))
