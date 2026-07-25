from IPython.display import HTML, display

# viewer-0004
# Standalone Aladin Lite v3.8.2 viewer.
# Approved bridge-coordinate-row-0001 layout embedded in the real viewer.
# No dependency on any earlier viewer or bridge file.

display(HTML(r'''
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />

<style>
#gv-viewer-0004 {
    width: 100%;
    height: 650px;
    position: relative !important;
    --text-blue: #62D8FF;
    --copy-blue: #7DF4FF;
    --target-blue: #2F7BFF;
}

/* Approved bridge row: fixed structural placement, no DOM coordinate math. */
#gv-viewer-0004 .gv-approved-top-row {
    position: absolute;
    top: 8px;
    left: 8px;
    z-index: 6000;
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
    gap: 8px;
    pointer-events: auto;
    font-family: Arial, Helvetica, sans-serif;
}

#gv-viewer-0004 .gv-frame-cell,
#gv-viewer-0004 .gv-coordinate-group {
    height: 54px;
    box-sizing: border-box;
}

#gv-viewer-0004 .gv-frame-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 108px;
    padding: 0 18px;
    color: var(--text-blue);
    background: rgba(0, 0, 0, 0.92);
    border: 2px solid #ffffff;
    border-radius: 8px;
    font-size: 21px;
    font-weight: 600;
    text-shadow: 0 0 5px rgba(98, 216, 255, 0.55);
}

#gv-viewer-0004 .gv-coordinate-group {
    display: flex;
    align-items: stretch;
    flex-wrap: nowrap;
    gap: 0;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.92);
    border: 2px solid #ffffff;
    border-radius: 8px;
}

#gv-viewer-0004 .gv-copy-cell,
#gv-viewer-0004 .gv-coordinate-cell,
#gv-viewer-0004 .gv-target-cell {
    height: 50px;
    box-sizing: border-box;
    border: 0;
    margin: 0;
    padding: 0;
    background: transparent;
}

#gv-viewer-0004 .gv-copy-cell {
    width: 54px;
    min-width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--copy-blue);
    border-right: 1px solid rgba(255, 255, 255, 0.75);
    cursor: pointer;
}

#gv-viewer-0004 .gv-copy-cell svg {
    width: 26px;
    height: 26px;
    stroke: currentColor;
    fill: none;
}

#gv-viewer-0004 .gv-coordinate-cell {
    min-width: 318px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    color: var(--text-blue);
    border-right: 1px solid rgba(255, 255, 255, 0.75);
    font-family: "Courier New", Courier, monospace;
    font-size: 20px;
    font-weight: 700;
    white-space: nowrap;
    text-shadow: 0 0 5px rgba(98, 216, 255, 0.55);
}

#gv-viewer-0004 .gv-target-cell {
    width: 54px;
    min-width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--target-blue);
    cursor: pointer;
    touch-action: manipulation;
}

#gv-viewer-0004 .gv-target-cell svg {
    width: 32px;
    height: 32px;
    stroke: currentColor;
    fill: none;
}

#gv-viewer-0004 .gv-target-cell .gv-center-dot {
    fill: currentColor;
    stroke: none;
}

#gv-viewer-0004 .gv-target-cell.gv-active {
    background: rgba(10, 25, 65, 0.98);
    box-shadow: 0 0 10px rgba(47, 123, 255, 0.95), inset 0 0 8px rgba(47, 123, 255, 0.45);
}

/* Hide only the duplicate native coordinate and SIMBAD controls. */
#gv-viewer-0004 .gv-hide-native-duplicate {
    display: none !important;
}
</style>

<div id="gv-viewer-0004">
    <div class="gv-approved-top-row" aria-label="Coordinate controls">
        <div class="gv-frame-cell">ICRSd</div>

        <div class="gv-coordinate-group">
            <button class="gv-copy-cell" type="button" title="Copy coordinates" aria-label="Copy coordinates">
                <svg viewBox="0 0 32 32" aria-hidden="true">
                    <rect x="10" y="8" width="14" height="17" rx="2" stroke-width="2.4"></rect>
                    <path d="M8 21H6.8A2.8 2.8 0 0 1 4 18.2V6.8A2.8 2.8 0 0 1 6.8 4h9.4A2.8 2.8 0 0 1 19 6.8V8" stroke-width="2.4"></path>
                </svg>
            </button>

            <div class="gv-coordinate-cell">10.6847083&nbsp;&nbsp;+41.2687500</div>

            <button class="gv-target-cell" type="button" title="SIMBAD Pointer" aria-label="Activate SIMBAD Pointer">
                <svg viewBox="0 0 100 100" aria-hidden="true">
                    <circle cx="50" cy="50" r="28" stroke-width="5"></circle>
                    <circle cx="50" cy="50" r="11" stroke-width="4"></circle>
                    <line x1="50" y1="3" x2="50" y2="35" stroke-width="5"></line>
                    <line x1="50" y1="65" x2="50" y2="97" stroke-width="5"></line>
                    <line x1="3" y1="50" x2="35" y2="50" stroke-width="5"></line>
                    <line x1="65" y1="50" x2="97" y2="50" stroke-width="5"></line>
                    <circle class="gv-center-dot" cx="50" cy="50" r="4"></circle>
                </svg>
            </button>
        </div>
    </div>
</div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js" charset="utf-8"></script>
<script>
A.init.then(() => {
    const root = document.getElementById("gv-viewer-0004");
    const coordinateText = root.querySelector(".gv-coordinate-cell");
    const copyButton = root.querySelector(".gv-copy-cell");
    const targetButton = root.querySelector(".gv-target-cell");

    const aladin = A.aladin("#gv-viewer-0004", {
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
    });

    window.aladin_viewer_0004 = aladin;

    function nativeSimbadPointer() {
        return root.querySelector(".aladin-simbadPointerControl") ||
               root.querySelector("[class*='simbadPointer']");
    }

    function hideNativeDuplicates() {
        root.querySelectorAll(".aladin-location, .aladin-coordinates")
            .forEach(element => element.classList.add("gv-hide-native-duplicate"));

        const nativePointer = nativeSimbadPointer();
        if (nativePointer) nativePointer.classList.add("gv-hide-native-duplicate");
    }

    function formatCoordinate(value) {
        return Number(value).toFixed(7);
    }

    function refreshCoordinates() {
        try {
            const position = aladin.getRaDec();
            if (!position || position.length < 2) return;
            const ra = formatCoordinate(position[0]);
            const decValue = Number(position[1]);
            const dec = (decValue >= 0 ? "+" : "") + formatCoordinate(decValue);
            coordinateText.textContent = `${ra}  ${dec}`;
        } catch (_) {
            /* Keep the last valid coordinate display. */
        }
    }

    copyButton.addEventListener("click", async () => {
        const text = coordinateText.textContent.trim().replace(/\s+/g, " ");
        try {
            await navigator.clipboard.writeText(text);
            copyButton.title = "Coordinates copied";
        } catch (_) {
            copyButton.title = "Copy unavailable in this frame";
        }
    });

    targetButton.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        const nativePointer = nativeSimbadPointer();
        if (!nativePointer) return;
        nativePointer.click();
        targetButton.classList.toggle("gv-active");
    });

    setTimeout(hideNativeDuplicates, 250);
    setTimeout(hideNativeDuplicates, 800);
    setTimeout(hideNativeDuplicates, 1600);
    setTimeout(refreshCoordinates, 300);
    setInterval(refreshCoordinates, 350);
});
</script>
'''))
