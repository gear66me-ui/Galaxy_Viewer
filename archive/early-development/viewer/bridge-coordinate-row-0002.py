from IPython.display import HTML, display

# bridge-coordinate-row-0002
# Standalone visual bridge for approving the first viewer row.
# No Aladin dependency. No dependency on any viewer version.


display(HTML(r'''
<style>
#gv-coordinate-bridge-0002 {
    --text-blue:       #62D8FF;
    --copy-blue:       #7DF4FF;
    --target-blue:     #2F7BFF;
    --projection-blue: #6FC7FF;
    --fullscreen-blue: #BCEEFF;

    width: 100%;
    min-height: 170px;
    box-sizing: border-box;
    padding: 24px;
    background:
        radial-gradient(circle at 35% 45%, rgba(58, 93, 170, 0.14), transparent 34%),
        #03060d;
    font-family: Arial, Helvetica, sans-serif;
}

#gv-coordinate-bridge-0002 .gv-first-row {
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
    gap: 8px;
    width: 100%;
    max-width: 100%;
}

#gv-coordinate-bridge-0002 .gv-frame-cell,
#gv-coordinate-bridge-0002 .gv-coordinate-group,
#gv-coordinate-bridge-0002 .gv-fov-cell,
#gv-coordinate-bridge-0002 .gv-projection-cell,
#gv-coordinate-bridge-0002 .gv-fullscreen-cell {
    height: 54px;
    box-sizing: border-box;
}

#gv-coordinate-bridge-0002 .gv-frame-cell,
#gv-coordinate-bridge-0002 .gv-fov-cell,
#gv-coordinate-bridge-0002 .gv-projection-cell,
#gv-coordinate-bridge-0002 .gv-fullscreen-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-blue);
    background: rgba(0, 0, 0, 0.92);
    border: 2px solid #ffffff;
    border-radius: 8px;
    text-shadow: 0 0 5px rgba(98, 216, 255, 0.55);
}

#gv-coordinate-bridge-0002 .gv-frame-cell {
    min-width: 108px;
    padding: 0 18px;
    font-size: 21px;
    font-weight: 600;
}

#gv-coordinate-bridge-0002 .gv-coordinate-group {
    display: flex;
    align-items: stretch;
    flex-wrap: nowrap;
    gap: 0;
    overflow: hidden;
    flex: 0 1 auto;
    min-width: 0;
    background: rgba(0, 0, 0, 0.92);
    border: 2px solid #ffffff;
    border-radius: 8px;
}

#gv-coordinate-bridge-0002 .gv-copy-cell,
#gv-coordinate-bridge-0002 .gv-coordinate-cell,
#gv-coordinate-bridge-0002 .gv-target-cell,
#gv-coordinate-bridge-0002 .gv-instruction-cell {
    height: 50px;
    box-sizing: border-box;
    border: 0;
    margin: 0;
    padding: 0;
    background: transparent;
}

#gv-coordinate-bridge-0002 .gv-copy-cell {
    width: 54px;
    min-width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--copy-blue);
    border-right: 1px solid rgba(255, 255, 255, 0.75);
}

#gv-coordinate-bridge-0002 .gv-copy-cell svg {
    width: 26px;
    height: 26px;
    stroke: currentColor;
    fill: none;
}

#gv-coordinate-bridge-0002 .gv-coordinate-cell {
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

#gv-coordinate-bridge-0002 .gv-target-cell {
    width: 54px;
    min-width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--target-blue);
    cursor: pointer;
    touch-action: manipulation;
    border-right: 1px solid rgba(255, 255, 255, 0.42);
}

#gv-coordinate-bridge-0002 .gv-target-cell svg {
    width: 32px;
    height: 32px;
    stroke: currentColor;
    fill: none;
}

#gv-coordinate-bridge-0002 .gv-target-cell .gv-center-dot {
    fill: currentColor;
    stroke: none;
}

#gv-coordinate-bridge-0002 .gv-target-cell.gv-active {
    background: rgba(10, 25, 65, 0.98);
    box-shadow:
        0 0 10px rgba(47, 123, 255, 0.95),
        inset 0 0 8px rgba(47, 123, 255, 0.45);
}

#gv-coordinate-bridge-0002 .gv-instruction-cell {
    min-width: 246px;
    padding: 0 15px 0 12px;
    display: flex;
    align-items: center;
    gap: 9px;
    color: var(--text-blue);
    white-space: nowrap;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.1px;
    text-shadow: 0 0 4px rgba(98, 216, 255, 0.35);
}

#gv-coordinate-bridge-0002 .gv-modern-arrow {
    width: 30px;
    min-width: 30px;
    height: 18px;
    display: block;
    overflow: visible;
    color: var(--target-blue);
    filter: drop-shadow(0 0 4px rgba(47, 123, 255, 0.78));
}

#gv-coordinate-bridge-0002 .gv-modern-arrow path {
    fill: none;
    stroke: currentColor;
    stroke-width: 2.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

#gv-coordinate-bridge-0002 .gv-instruction-cell.gv-active .gv-modern-arrow {
    animation: gv-arrow-pulse-0002 1.15s ease-in-out infinite;
}

@keyframes gv-arrow-pulse-0002 {
    0%, 100% { transform: translateX(0); opacity: 0.82; }
    50%      { transform: translateX(4px); opacity: 1; }
}

#gv-coordinate-bridge-0002 .gv-right-spacer {
    flex: 1 1 auto;
    min-width: 8px;
}

#gv-coordinate-bridge-0002 .gv-fov-cell {
    min-width: 154px;
    padding: 0 14px;
    font-family: "Courier New", Courier, monospace;
    font-size: 16px;
    font-weight: 700;
}

#gv-coordinate-bridge-0002 .gv-projection-cell {
    min-width: 72px;
    padding: 0 14px;
    color: var(--projection-blue);
    font-size: 17px;
    font-weight: 700;
}

#gv-coordinate-bridge-0002 .gv-fullscreen-cell {
    width: 54px;
    min-width: 54px;
    color: var(--fullscreen-blue);
}

#gv-coordinate-bridge-0002 .gv-fullscreen-cell svg {
    width: 26px;
    height: 26px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2.4;
    stroke-linecap: round;
    stroke-linejoin: round;
}

#gv-coordinate-bridge-0002 .gv-caption {
    margin-top: 16px;
    color: #9bb4c8;
    font: 13px/1.4 "Courier New", Courier, monospace;
}

@media (max-width: 1040px) {
    #gv-coordinate-bridge-0002 .gv-first-row {
        overflow-x: auto;
        padding-bottom: 4px;
    }

    #gv-coordinate-bridge-0002 .gv-right-spacer {
        flex: 0 0 8px;
    }
}
</style>

<div id="gv-coordinate-bridge-0002">
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

            <div class="gv-instruction-cell" aria-live="polite">
                <svg class="gv-modern-arrow" viewBox="0 0 34 20" aria-hidden="true">
                    <path d="M2 10H27"></path>
                    <path d="M21 4L28 10L21 16"></path>
                </svg>
                <span class="gv-instruction-text">Tap target, then tap object</span>
            </div>
        </div>

        <div class="gv-right-spacer"></div>
        <div class="gv-fov-cell">1.50° × 1.50°</div>
        <div class="gv-projection-cell">TAN</div>
        <button class="gv-fullscreen-cell" type="button" title="Fullscreen" aria-label="Fullscreen">
            <svg viewBox="0 0 32 32" aria-hidden="true">
                <path d="M5 12V5H12"></path>
                <path d="M20 5H27V12"></path>
                <path d="M27 20V27H20"></path>
                <path d="M12 27H5V20"></path>
            </svg>
        </button>
    </div>

    <div class="gv-caption">
        BRIDGE TEST: APPROVED COORDINATE GROUP + MODERN TARGET INSTRUCTION
    </div>
</div>

<script>
(() => {
    const root = document.getElementById("gv-coordinate-bridge-0002");
    if (!root) return;

    const target = root.querySelector(".gv-target-cell");
    const instruction = root.querySelector(".gv-instruction-cell");
    const instructionText = root.querySelector(".gv-instruction-text");

    if (target && instruction && instructionText) {
        target.addEventListener("click", () => {
            const active = target.classList.toggle("gv-active");
            instruction.classList.toggle("gv-active", active);
            instructionText.textContent = active
                ? "Now tap a galaxy or object"
                : "Tap target, then tap object";
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
