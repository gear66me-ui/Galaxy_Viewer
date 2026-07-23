from urllib.request import urlopen

# viewer-0009
# Applies one approved visual correction to viewer-0008:
# Ensure the moved SIMBAD finder has a clearly visible white box while
# preserving the coordinate-matched height and right-side corner radius.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0008.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_target_css = '''    border: 2px solid #ffffff !important;
    border-left-width: 1px !important;
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;'''

new_target_css = '''    border: 2px solid #ffffff !important;
    border-left-width: 1px !important;
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
    box-shadow: inset 0 0 0 2px #ffffff !important;
    overflow: hidden !important;'''

if old_target_css not in source:
    raise RuntimeError("viewer-0009: target box CSS anchor was not found")

source = source.replace(old_target_css, new_target_css, 1)
source = source.replace("# viewer-0008", "# viewer-0009", 1)

exec(compile(source, "viewer-0009.py", "exec"))
