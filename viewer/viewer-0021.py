from urllib.request import urlopen

# viewer-0021
# Corrects only the viewer-0020 launcher structure.
# Approved interface changes remain exactly:
# 1. Mirror SIMBAD feedback beneath the yellow helper.
# 2. Color zoom plus green and zoom minus red.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0019.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_exec = 'exec(compile(source, "viewer-0019-expanded.py", "exec"))'

extra_css = r'''
/* viewer-0021: compact SIMBAD feedback beneath the approved helper. */
#aladin-cosmic-command-test .gv-simbad-live-status {
    display: none;
    margin: 3px 0 0 0 !important;
    padding: 2px 7px !important;
    max-width: 245px !important;
    box-sizing: border-box !important;
    color: #FFD166 !important;
    background: rgba(0, 0, 0, 0.72) !important;
    border: 1px solid rgba(255, 209, 102, 0.62) !important;
    border-radius: 4px !important;
    font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace !important;
    font-size: 10px !important;
    line-height: 1.25 !important;
    letter-spacing: 0.10px !important;
    text-align: left !important;
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

#aladin-cosmic-command-test .gv-plus img,
#aladin-cosmic-command-test .gv-plus canvas {
    filter: brightness(0) saturate(100%) invert(84%) sepia(66%) saturate(654%) hue-rotate(77deg) brightness(105%) contrast(104%) !important;
}

#aladin-cosmic-command-test .gv-minus img,
#aladin-cosmic-command-test .gv-minus canvas {
    filter: brightness(0) saturate(100%) invert(53%) sepia(84%) saturate(3287%) hue-rotate(319deg) brightness(105%) contrast(101%) !important;
}
'''

extra_js = r'''
(function installViewer0021Enhancements() {
    const root = document.getElementById("aladin-cosmic-command-test");
    if (!root) return;

    const normalize = value => String(value || "").trim().split(/\s+/).join(" ");

    function ensureLiveStatus() {
        const helper = root.querySelector(".gv-simbad-helper");
        if (!helper) return null;

        let status = root.querySelector(".gv-simbad-live-status");
        if (!status) {
            status = document.createElement("div");
            status.className = "gv-simbad-live-status";
            status.setAttribute("aria-live", "polite");
            helper.insertAdjacentElement("afterend", status);
        } else if (status.previousElementSibling !== helper) {
            helper.insertAdjacentElement("afterend", status);
        }
        return status;
    }

    function isSimbadFeedback(element) {
        if (!element || element.closest(".gv-simbad-helper, .gv-simbad-live-status")) return false;

        const text = normalize(element.textContent).toLowerCase();
        if (!text || text.length > 240) return false;

        const matches = (
            text.includes("simbad") ||
            text.includes("pointer") ||
            text.includes("click again") ||
            text.includes("click on an object") ||
            text.includes("click an object") ||
            text.includes("select an object")
        );
        if (!matches) return false;

        const rect = element.getBoundingClientRect();
        const rootRect = root.getBoundingClientRect();
        return (
            rect.width > 0 &&
            rect.height > 0 &&
            rect.top >= rootRect.top + rootRect.height * 0.55
        );
    }

    function mirrorSimbadFeedback() {
        const status = ensureLiveStatus();
        if (!status) return;

        const candidates = [...root.querySelectorAll("div, span, p")]
            .filter(isSimbadFeedback)
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

    function bindTargetImmediateStatus() {
        const target = root.querySelector(".gv-native-simbad-moved");
        const status = ensureLiveStatus();
        if (!target || !status || target.dataset.gvLiveStatusBound) return;

        target.dataset.gvLiveStatusBound = "true";
        target.addEventListener("click", () => {
            status.textContent = "SIMBAD active — click a galaxy or star.";
            status.classList.add("gv-visible");
            setTimeout(mirrorSimbadFeedback, 30);
            setTimeout(mirrorSimbadFeedback, 180);
            setTimeout(mirrorSimbadFeedback, 600);
        });
    }

    function enforceZoomPalette() {
        root.querySelectorAll("*").forEach(element => {
            const text = normalize(element.textContent);
            const description = [
                element.className || "",
                element.id || "",
                element.getAttribute?.("title") || "",
                element.getAttribute?.("aria-label") || ""
            ].join(" ").toLowerCase();

            const control = element.closest(
                "button, [role='button'], [class*='Control'], [class*='control']"
            ) || element;

            if (text === "+" || description.includes("zoom in") || description.includes("zoomin")) {
                control.classList.add("gv-command", "gv-plus");
            }
            if (text === "−" || text === "-" || description.includes("zoom out") || description.includes("zoomout")) {
                control.classList.add("gv-command", "gv-minus");
            }
        });
    }

    function refreshViewer0021() {
        ensureLiveStatus();
        bindTargetImmediateStatus();
        enforceZoomPalette();
        mirrorSimbadFeedback();
    }

    setTimeout(refreshViewer0021, 300);
    setTimeout(refreshViewer0021, 900);
    setTimeout(refreshViewer0021, 1800);

    const observer = new MutationObserver(refreshViewer0021);
    observer.observe(root, {
        childList: true,
        subtree: true,
        characterData: true
    });
})();
'''

replacement_lines = [
    "# viewer-0021: inject the two approved additions into the fully expanded viewer.",
    f"extra_css = {extra_css!r}",
    f"extra_js = {extra_js!r}",
    "if '</style>' not in source:",
    "    raise RuntimeError('viewer-0021: closing style tag was not found')",
    "if '</script>' not in source:",
    "    raise RuntimeError('viewer-0021: closing script tag was not found')",
    "source = source.replace('</style>', extra_css + '\\n</style>', 1)",
    "script_head, script_tail = source.rsplit('</script>', 1)",
    "source = script_head + extra_js + '\\n</script>' + script_tail",
    "required_final = (",
    "    '.gv-simbad-live-status',",
    "    'SIMBAD active — click a galaxy or star.',",
    "    '#55FF88',",
    "    '#FF5E78',",
    "    'nativePointer.style.setProperty(\"border-color\", borderColor',",
    "    'nativePointer.style.setProperty(\"border-width\", borderWidth',",
    "    'nativePointer.style.setProperty(\"border-radius\", radius',",
    "    'transform: scale(0.81) !important;',",
    ")",
    "for token in required_final:",
    "    if token not in source:",
    "        raise RuntimeError(f'viewer-0021 final integrity check failed: {token}')",
    "compile(source, 'viewer-0021-expanded.py', 'exec')",
    "exec(compile(source, 'viewer-0021-expanded.py', 'exec'))",
]

replacement_code = "\n".join(replacement_lines)

if old_exec not in source:
    raise RuntimeError("viewer-0021: viewer-0019 final execution anchor was not found")

source = source.replace(old_exec, replacement_code, 1)
source = source.replace("# viewer-0019", "# viewer-0021", 1)

compile(source, "viewer-0021-intermediate.py", "exec")
exec(compile(source, "viewer-0021-intermediate.py", "exec"))
