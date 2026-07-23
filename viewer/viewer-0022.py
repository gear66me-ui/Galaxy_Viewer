from IPython.display import HTML, display

# viewer-0022
# Standalone Galaxy Viewer release.
# Based on the approved Viewer 19 interface, copied into this file.
# Adds only:
# 1. SIMBAD feedback directly beneath the yellow target helper.
# 2. Green zoom-plus and red zoom-minus controls.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML(r"""
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
}

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
    overflow: hidden !important;
}

#aladin-cosmic-command-test .gv-native-simbad-moved > * {
    transform: scale(0.81) !important;
    transform-origin: center center !important;
}

#aladin-cosmic-command-test .gv-simbad-helper-stack {
    display: flex !important;
    flex-direction: column !important;
    align-self: center !important;
    margin: 0 0 0 9px !important;
    padding: 0 !important;
}

#aladin-cosmic-command-test .gv-simbad-helper {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    color: #FFD166 !important;
    font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    line-height: 1.12 !important;
    letter-spacing: 0.15px !important;
    width: 238px !important;
    max-width: 238px !important;
    white-space: normal !important;
    text-shadow: 0 0 4px rgba(255, 209, 102, 0.45) !important;
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
    color: var(--copy-blue) !important;
    filter: drop-shadow(0 0 3px rgba(125, 244, 255, 0.72)) !important;
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

#aladin-cosmic-command-test .gv-simbad-live-status {
    display: none !important;
    margin: 4px 0 0 25px !important;
    padding: 2px 6px !important;
    width: max-content !important;
    max-width: 210px !important;
    box-sizing: border-box !important;
    color: #FFD166 !important;
    background: rgba(0, 0, 0, 0.74) !important;
    border: 1px solid rgba(255, 209, 102, 0.60) !important;
    border-radius: 4px !important;
    font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace !important;
    font-size: 10px !important;
    line-height: 1.25 !important;
    white-space: normal !important;
    pointer-events: none !important;
}

#aladin-cosmic-command-test .gv-simbad-live-status.gv-visible {
    display: block !important;
}

#aladin-cosmic-command-test .gv-plus,
#aladin-cosmic-command-test .gv-plus * {
    color: #55FF88 !important;
}

#aladin-cosmic-command-test .gv-minus,
#aladin-cosmic-command-test .gv-minus * {
    color: #FF5E78 !important;
}

#aladin-cosmic-command-test .gv-plus svg,
#aladin-cosmic-command-test .gv-plus svg * {
    stroke: #55FF88 !important;
    fill: #55FF88 !important;
}

#aladin-cosmic-command-test .gv-minus svg,
#aladin-cosmic-command-test .gv-minus svg * {
    stroke: #FF5E78 !important;
    fill: #FF5E78 !important;
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
        world: "brightness(0) saturate(100%) invert(55%) sepia(94%) saturate(1690%) hue-rotate(219deg) brightness(101%) contrast(101%)",
        projection: "brightness(0) saturate(100%) invert(79%) sepia(38%) saturate(1260%) hue-rotate(172deg) brightness(101%) contrast(102%)",
        fullscreen: "brightness(0) saturate(100%) invert(94%) sepia(21%) saturate(996%) hue-rotate(171deg) brightness(104%) contrast(102%)",
        plus: "brightness(0) saturate(100%) invert(84%) sepia(66%) saturate(654%) hue-rotate(77deg) brightness(105%) contrast(104%)",
        minus: "brightness(0) saturate(100%) invert(53%) sepia(84%) saturate(3287%) hue-rotate(319deg) brightness(105%) contrast(101%)"
    };

    const normalize = value => String(value || "").trim().split(/\s+/).join(" ");

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
        let stack = row.querySelector(".gv-simbad-helper-stack");
        if (!stack) {
            stack = document.createElement("div");
            stack.className = "gv-simbad-helper-stack";
            stack.innerHTML = `
                <div class="gv-simbad-helper" aria-live="polite">
                    <svg class="gv-simbad-helper-arrow" viewBox="0 0 24 14" aria-hidden="true">
                        <path d="M22 7H6"></path>
                        <path d="M11 2L5 7L11 12"></path>
                    </svg>
                    <span class="gv-simbad-helper-text">Click target, then click<br>a galaxy or star to find info</span>
                </div>
                <div class="gv-simbad-live-status" aria-live="polite"></div>
            `;
        }

        if (stack.parentElement !== row || nativePointer.nextElementSibling !== stack) {
            nativePointer.insertAdjacentElement("afterend", stack);
        }

        if (!nativePointer.dataset.gvHelperBound) {
            nativePointer.dataset.gvHelperBound = "true";
            nativePointer.addEventListener("click", () => {
                const helper = stack.querySelector(".gv-simbad-helper");
                const text = stack.querySelector(".gv-simbad-helper-text");
                const status = stack.querySelector(".gv-simbad-live-status");

                helper?.classList.add("gv-active");
                if (text) {
                    text.innerHTML = "Now click a galaxy or star<br>to find information";
                }
                if (status) {
                    status.textContent = "SIMBAD active — target click registered.";
                    status.classList.add("gv-visible");
                }

                setTimeout(mirrorNativeFeedback, 40);
                setTimeout(mirrorNativeFeedback, 180);
                setTimeout(mirrorNativeFeedback, 600);
            });
        }

        return stack;
    }

    function synchronizeTargetGeometry(coordinateBox, nativePointer) {
        const coordinateRect = coordinateBox.getBoundingClientRect();
        const height = Math.max(1, Math.round(coordinateRect.height));
        const boxWidth = Math.max(height, Math.round(height * 1.08));

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
                    rect,
                    style,
                    visible,
                    rightDistance: Math.abs(rect.right - coordinateRect.right),
                    area: rect.width * rect.height
                };
            })
            .filter(item => item.visible && item.rect.width > 0 && item.rect.height > 0)
            .sort((a, b) => a.rightDistance - b.rightDistance || b.area - a.area);

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

        nativePointer.classList.remove("gv-target");
        nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-copy");
        nativePointer.style.setProperty("--command-filter", filters.copy, "important");

        synchronizeTargetGeometry(coordinateBox, nativePointer);
        ensureHelper(row, nativePointer);
        return coordinateBox.nextElementSibling === nativePointer;
    }

    function isNativeSimbadFeedback(element) {
        if (!element || element.closest(".gv-simbad-helper-stack")) return false;
        const text = normalize(element.textContent).toLowerCase();
        if (!text || text.length > 240) return false;

        const matches =
            text.includes("simbad") ||
            text.includes("pointer") ||
            text.includes("click again") ||
            text.includes("click on an object") ||
            text.includes("click an object") ||
            text.includes("select an object");

        if (!matches) return false;

        const rect = element.getBoundingClientRect();
        const rootRect = root.getBoundingClientRect();
        return (
            rect.width > 0 &&
            rect.height > 0 &&
            rect.top >= rootRect.top + rootRect.height * 0.55
        );
    }

    function mirrorNativeFeedback() {
        const status = root.querySelector(".gv-simbad-live-status");
        if (!status) return;

        const candidates = [...root.querySelectorAll("div, span, p")]
            .filter(isNativeSimbadFeedback)
            .sort((a, b) => b.getBoundingClientRect().top - a.getBoundingClientRect().top);

        const nativeMessage = candidates[0] || null;
        if (!nativeMessage) return;

        const text = normalize(nativeMessage.textContent);
        if (!text) return;

        status.textContent = text;
        status.classList.add("gv-visible");
        nativeMessage.style.setProperty("display", "none", "important");
        nativeMessage.dataset.gvSimbadFeedbackMoved = "true";
    }

    function applyPalette() {
        root.querySelectorAll("*").forEach(element => {
            const description = describe(element);
            const text = normalize(element.textContent);

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
        mirrorNativeFeedback();
    }

    setTimeout(applyPalette, 250);
    setTimeout(applyPalette, 700);
    setTimeout(applyPalette, 1400);
    setTimeout(applyPalette, 2400);

    const observer = new MutationObserver(() => {
        applyPalette();
    });
    observer.observe(root, {
        childList: true,
        subtree: true,
        characterData: true
    });

    window.addEventListener("resize", moveNativeSimbadPointer);
});
</script>
"""))
