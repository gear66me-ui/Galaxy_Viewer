from IPython.display import HTML, display
import urllib.request

# GV-beta-0002Q13
# Visual-only refinement layered over Q12.
# Reduces the active helper width from 235px to 200px (14.9%).
# Preserves Q12 text, colors, emoji, height, and all SIMBAD behavior.

_Q12_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0002Q12.py"
with urllib.request.urlopen(_Q12_URL) as response:
    _q12_source = response.read().decode("utf-8")
exec(compile(_q12_source, _Q12_URL, "exec"), globals(), globals())

display(HTML(r'''
<style>
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-box{
    width:200px!important;
    max-width:200px!important;
}
</style>
'''))
