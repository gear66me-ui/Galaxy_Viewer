from IPython.display import HTML, display
import urllib.request

# GV-beta-0002Q14
# Active-state visual refinement layered over Q13.
# Adds a fast-evolving but smoothly blended iris/cloud color flow to:
#   1. the active Target icon, and
#   2. the "Tap Target Again / to Exit" instruction.
# The first instruction line remains steady yellow.
# No geometry, helper sizing, or SIMBAD behavior is changed.

_Q13_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0002Q13.py"
with urllib.request.urlopen(_Q13_URL) as response:
    _q13_source = response.read().decode("utf-8")
exec(compile(_q13_source, _Q13_URL, "exec"), globals(), globals())

display(HTML(r'''
<style>
#aladin-cosmic-command-test{
    --gv-iris-color:hsl(190 100% 70%);
    --gv-iris-glow:hsl(190 100% 70% / .82);
}

/* Keep the first active instruction line steady yellow. */
#aladin-cosmic-command-test .gv-helper-row.gv-active
.gv-helper-active-line:nth-child(1){
    color:#FFD166!important;
    text-shadow:0 0 10px rgba(255,209,102,.75)!important;
}

/* Synchronize only the exit instruction with the active Target icon. */
#aladin-cosmic-command-test .gv-helper-row.gv-active
.gv-helper-active-line:nth-child(2),
#aladin-cosmic-command-test .gv-helper-row.gv-active
.gv-helper-active-line:nth-child(3){
    color:var(--gv-iris-color)!important;
    text-shadow:
        0 0 4px var(--gv-iris-glow),
        0 0 9px var(--gv-iris-glow),
        0 0 15px var(--gv-iris-glow)!important;
    transition:
        color 420ms ease-in-out,
        text-shadow 420ms ease-in-out!important;
}

/* Flowing active-state color through the Target icon without changing its shape. */
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active,
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active svg,
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active svg *{
    color:var(--gv-iris-color)!important;
    transition:
        color 420ms ease-in-out,
        filter 420ms ease-in-out!important;
}

#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active svg{
    filter:
        drop-shadow(0 0 2px var(--gv-iris-glow))
        drop-shadow(0 0 5px var(--gv-iris-glow))
        drop-shadow(0 0 9px var(--gv-iris-glow))!important;
    animation:gv-q14-cloud-bloom 1.6s ease-in-out infinite!important;
}

@keyframes gv-q14-cloud-bloom{
    0%,100%{opacity:.88;transform:scale(.985)}
    35%{opacity:1;transform:scale(1.035)}
    68%{opacity:.94;transform:scale(1.005)}
}

@media (prefers-reduced-motion:reduce){
    #aladin-cosmic-command-test button.gv-simbad-proxy.gv-active svg{
        animation:none!important;
    }
}
</style>
<script>
(() => {
    const root = document.getElementById("aladin-cosmic-command-test");
    if(!root) return;

    const STEP_MS = 200;
    const STEPS_PER_SEQUENCE = 20;
    const hueAnchors = [
        188, 202, 222, 246, 272, 300,
        326, 350, 24, 48, 78, 112, 146, 170
    ];

    let timer = null;
    let sequence = [];
    let sequenceIndex = 0;

    function randomBetween(min, max){
        return min + Math.random() * (max - min);
    }

    function circularHueDistance(a, b){
        const d = Math.abs(a - b) % 360;
        return Math.min(d, 360 - d);
    }

    function buildSequence(){
        const colors = [];
        let previousHue = Math.random() * 360;

        for(let i = 0; i < STEPS_PER_SEQUENCE; i++){
            const nearby = hueAnchors.filter(h => circularHueDistance(h, previousHue) <= 105);
            const pool = nearby.length ? nearby : hueAnchors;
            const anchor = pool[Math.floor(Math.random() * pool.length)];
            const hue = (anchor + randomBetween(-18, 18) + 360) % 360;
            const saturation = Math.round(randomBetween(82, 100));
            const lightness = Math.round(randomBetween(61, 76));
            const alpha = randomBetween(.68, .92).toFixed(2);

            colors.push({hue, saturation, lightness, alpha});
            previousHue = hue;
        }
        return colors;
    }

    function setIrisColor(color){
        root.style.setProperty(
            "--gv-iris-color",
            `hsl(${color.hue.toFixed(1)} ${color.saturation}% ${color.lightness}%)`
        );
        root.style.setProperty(
            "--gv-iris-glow",
            `hsl(${color.hue.toFixed(1)} ${color.saturation}% ${color.lightness}% / ${color.alpha})`
        );
    }

    function nextColor(){
        if(sequenceIndex >= sequence.length){
            sequence = buildSequence();
            sequenceIndex = 0;
        }
        setIrisColor(sequence[sequenceIndex++]);
    }

    function startIris(){
        if(timer) return;
        sequence = buildSequence();
        sequenceIndex = 0;
        nextColor();
        timer = setInterval(nextColor, STEP_MS);
    }

    function stopIris(){
        if(timer){
            clearInterval(timer);
            timer = null;
        }
        root.style.setProperty("--gv-iris-color", "hsl(190 100% 70%)");
        root.style.setProperty("--gv-iris-glow", "hsl(190 100% 70% / .82)");
    }

    function syncState(){
        const target = root.querySelector("button.gv-simbad-proxy");
        const active = !!target && target.classList.contains("gv-active");
        if(active) startIris();
        else stopIris();
    }

    syncState();
    const observer = new MutationObserver(syncState);
    observer.observe(root, {
        subtree:true,
        childList:true,
        attributes:true,
        attributeFilter:["class"]
    });

    [100, 300, 700, 1400, 2400].forEach(delay => setTimeout(syncState, delay));
})();
</script>
'''))
