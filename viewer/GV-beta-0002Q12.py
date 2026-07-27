from IPython.display import HTML, display
import urllib.request

# GV-beta-0002Q12
# Visual-only correction layered over Q11.
# Restores the yellow active helper text and star emoji.
# Uses a narrower, shorter three-line active helper box.

_Q11_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0002Q11.py"
with urllib.request.urlopen(_Q11_URL) as response:
    _q11_source = response.read().decode("utf-8")
exec(compile(_q11_source, _Q11_URL, "exec"), globals(), globals())

display(HTML(r'''
<style>
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-box{
    width:235px!important;
    max-width:235px!important;
    height:56px!important;
    min-height:56px!important;
    padding:3px 10px!important;
    flex-direction:column!important;
    align-items:center!important;
    justify-content:center!important;
    text-align:center!important;
    color:#FFD166!important;
    line-height:1.12!important;
    text-shadow:0 0 10px rgba(255,209,102,.75)!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line{
    display:block!important;
    width:100%!important;
    text-align:center!important;
    color:#FFD166!important;
}
</style>
<script>
(() => {
    const root = document.getElementById("aladin-cosmic-command-test");
    if(!root) return;

    const activeMarkup =
        '<span class="gv-helper-active-line">✨ Tap Galaxy / Star</span>' +
        '<span class="gv-helper-active-line">or Tap Target Again</span>' +
        '<span class="gv-helper-active-line">to Exit</span>';

    function applyQ12Helper(){
        const row = root.querySelector(".gv-helper-row");
        const box = root.querySelector(".gv-helper-box");
        if(!row || !box || !row.classList.contains("gv-active")) return;
        if(box.innerHTML !== activeMarkup) box.innerHTML = activeMarkup;
        box.style.setProperty("color", "#FFD166", "important");
        box.style.setProperty("text-shadow", "0 0 10px rgba(255,209,102,.75)", "important");
    }

    applyQ12Helper();
    [100, 300, 700, 1400, 2400].forEach(delay => setTimeout(applyQ12Helper, delay));

    const observer = new MutationObserver(() => applyQ12Helper());
    observer.observe(root, {
        childList:true,
        subtree:true,
        characterData:true,
        attributes:true,
        attributeFilter:["class"]
    });
})();
</script>
'''))
