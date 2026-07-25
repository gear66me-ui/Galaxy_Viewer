from IPython.display import HTML, display

# viewer-0003
# Standalone Aladin Lite v3.8.2 viewer.
# No dependency on or reference to any earlier viewer file.

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
    text-shadow: 0 0 5px rgba(98,216,255,.55) !important;
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

#aladin-cosmic-command-test .gv-coordinate-joined {
    border-top-right-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
    box-sizing: border-box !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target {
    position: absolute !important;
    z-index: 5000 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 52px !important;
    min-width: 52px !important;
    max-width: 52px !important;
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    background: rgba(0,0,0,.92) !important;
    border-top: 2px solid #fff !important;
    border-right: 2px solid #fff !important;
    border-bottom: 2px solid #fff !important;
    border-left: 1px solid #fff !important;
    border-radius: 0 7px 7px 0 !important;
    color: var(--target-blue) !important;
    cursor: pointer !important;
    touch-action: manipulation !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target.gv-ready {
    visibility: visible !important;
    opacity: 1 !important;
}

#aladin-cosmic-command-test #gv-simbad-coordinate-target svg {
    display: block !important;
    width: 32px !important;
    min-width: 32px !important;
    max-width: 32px !important;
    height: 32px !important;
    min-height: 32px !important;
    max-height: 32px !important;
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
    background: rgba(10,25,65,.98) !important;
    box-shadow: 0 0 10px rgba(47,123,255,.95), inset 0 0 8px rgba(47,123,255,.45) !important;
}

#aladin-cosmic-command-test .gv-native-simbad-hidden {
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
}

#aladin-cosmic-command-test .gv-compact-icon-row {
    gap: 0 !important;
    column-gap: 0 !important;
    row-gap: 0 !important;
}

#aladin-cosmic-command-test .gv-compact-icon-row > * {
    margin-left: 0 !important;
    margin-right: 0 !important;
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

    function findNativeSimbadPointer() {
        return root.querySelector(".aladin-simbadPointerControl") ||
               root.querySelector("[class*='simbadPointer']");
    }

    function findVisibleCoordinateBox() {
        const rootRect = root.getBoundingClientRect();
        const matches = [];
        const selectors = [
            ".aladin-location",
            ".aladin-coordinates",
            "[class*='location']",
            "[class*='coordinates']"
        ];

        selectors.forEach(selector => {
            root.querySelectorAll(selector).forEach(element => {
                if (element.id === "gv-simbad-coordinate-target" || element.closest("#gv-simbad-coordinate-target")) return;

                const rect = element.getBoundingClientRect();
                const text = (element.textContent || "").trim();
                const relativeTop = rect.top - rootRect.top;
                const relativeLeft = rect.left - rootRect.left;
                const looksLikeCoordinates = /[-+]?\d+(\.\d+)?\s+[-+]?\d+(\.\d+)?/.test(text);
                const visible = rect.width > 0 && rect.height > 0;

                if (
                    visible &&
                    looksLikeCoordinates &&
                    rect.width >= 220 && rect.width <= 620 &&
                    rect.height >= 38 && rect.height <= 72 &&
                    relativeTop >= 0 && relativeTop <= 130 &&
                    relativeLeft >= 0 && relativeLeft <= rootRect.width * 0.65
                ) {
                    matches.push({ element, area: rect.width * rect.height });
                }
            });
        });

        matches.sort((a, b) => a.area - b.area);
        return matches.length ? matches[0].element : null;
    }

    function createTargetButton() {
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
            </svg>`;

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

    function placeTargetSafely() {
        const coordinateBox = findVisibleCoordinateBox();
        const nativePointer = findNativeSimbadPointer();
        const button = createTargetButton();

        if (!coordinateBox || !nativePointer || !button) return false;

        const rootRect = root.getBoundingClientRect();
        const coordinateRect = coordinateBox.getBoundingClientRect();
        const size = Math.max(44, Math.min(52, Math.round(coordinateRect.height)));
        const left = Math.round(coordinateRect.right - rootRect.left - 1);
        const top = Math.round(coordinateRect.top - rootRect.top + (coordinateRect.height - size) / 2);

        const insideViewer =
            left >= 0 &&
            top >= 0 &&
            left + size <= rootRect.width &&
            top + size <= rootRect.height;

        if (!insideViewer) {
            button.classList.remove("gv-ready");
            return false;
        }

        button.style.setProperty("left", left + "px", "important");
        button.style.setProperty("top", top + "px", "important");
        button.style.setProperty("width", size + "px", "important");
        button.style.setProperty("min-width", size + "px", "important");
        button.style.setProperty("max-width", size + "px", "important");
        button.style.setProperty("height", size + "px", "important");
        button.style.setProperty("min-height", size + "px", "important");
        button.style.setProperty("max-height", size + "px", "important");
        button.classList.add("gv-ready");
        coordinateBox.classList.add("gv-coordinate-joined", "gv-standard-text");

        const originalParent = nativePointer.parentElement;
        nativePointer.classList.add("gv-native-simbad-hidden");
        if (originalParent) originalParent.classList.add("gv-compact-icon-row");

        return true;
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
                text === "ICRS" || text === "ICRSd" ||
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

        placeTargetSafely();
    }

    setTimeout(applyPalette, 250);
    setTimeout(applyPalette, 700);
    setTimeout(applyPalette, 1400);
    setTimeout(applyPalette, 2400);

    window.addEventListener("resize", placeTargetSafely);
    new ResizeObserver(() => placeTargetSafely()).observe(root);
});
</script>
'''))
