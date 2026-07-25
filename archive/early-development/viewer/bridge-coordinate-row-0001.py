from IPython.display import HTML, display

# bridge-coordinate-row-0001
# Standalone visual bridge for approving the first viewer row.
# No Aladin dependency. No dependency on any viewer version.

display(HTML(r'''
<style>
#gv-coordinate-bridge {
    --text-blue:   #62D8FF;
    --copy-blue:   #7DF4FF;
    --target-blue: #2F7BFF;

    width: 100%;
    min-height: 170px;
    box-sizing: border-box;
    padding: 24px;
    background:
        radial-gradient(circle at 35% 45%, rgba(58, 93, 170, 0.14), transparent 34%),
        #03060d;
    font-family: Arial, Helvetica, sans-serif;
}

#gv-coordinate-bridge .gv-first-row {
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
    gap: 8px;
    width: max-content;
    max-width: 100%;
}

#gv-coordinate-bridge .gv-frame-cell,
#gv-coordinate-bridge .gv-coordinate-group {
    height: 54px;
    box-sizing: border-box;
}

#gv-coordinate-bridge .gv-frame-cell {
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

#gv-coordinate-bridge .gv-coordinate-group {
    display: flex;
    align-items: stretch;
    flex-wrap: nowrap;
    gap: 0;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.92);
    border: 2px solid #ffffff;
    border-radius: 8px;
}

#gv-coordinate-bridge .gv-copy-cell,
#gv-coordinate-bridge .gv-coordinate-cell,
#gv-coordinate-bridge .gv-target-cell {
    height: 50px;
    box-sizing: border-box;
    border: 0;
    margin: 0;
    padding: 0;
    background: transparent;
}

#gv-coordinate-bridge .gv-copy-cell {
    width: 54px;
    min-width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--copy-blue);
    border-right: 1px solid rgba(255, 255, 255, 0.75);
}

#gv-coordinate-bridge .gv-copy-cell svg {
    width: 26px;
    height: 26px;
    stroke: currentColor;
    fill: none;
}

#gv-coordinate-bridge .gv-coordinate-cell {
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

#gv-coordinate-bridge .gv-target-cell {
    width: 54px;
    min-width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--target-blue);
    cursor: pointer;
    touch-action: manipulation;
}

#gv-coordinate-bridge .gv-target-cell svg {
    width: 32px;
    height: 32px;
    stroke: currentColor;
    fill: none;
}

#gv-coordinate-bridge .gv-target-cell .gv-center-dot {
    fill: currentColor;
    stroke: none;
}

#gv-coordinate-bridge .gv-target-cell.gv-active {
    background: rgba(10, 25, 65, 0.98);
    box-shadow:
        0 0 10px rgba(47, 123, 255, 0.95),
        inset 0 0 8px rgba(47, 123, 255, 0.45);
}

#gv-coordinate-bridge .gv-caption {
    margin-top: 16px;
    color: #9bb4c8;
    font: 13px/1.4 "Courier New", Courier, monospace;
}
</style>

<div id="gv-coordinate-bridge">
    <div class="gv-first-row">
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

    <div class="gv-caption">
        BRIDGE TEST: ICRSd + COPY + COORDINATES + SIMBAD TARGET
    </div>
</div>

<script>
(() => {
    const root = document.getElementById("gv-coordinate-bridge");
    if (!root) return;

    const target = root.querySelector(".gv-target-cell");
    if (target) {
        target.addEventListener("click", () => {
            target.classList.toggle("gv-active");
        });
    }

    const copy = root.querySelector(".gv-copy-cell");
    if (copy) {
        copy.addEventListener("click", async () => {
            const text = "10.6847083 +41.2687500";
            try {
                await navigator.clipboard.writeText(text);
                copy.title = "Coordinates copied";
            } catch (_) {
                copy.title = "Copy unavailable in this frame";
            }
        });
    }
})();
</script>
'''))
