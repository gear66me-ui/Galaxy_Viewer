from urllib.request import urlopen

# viewer-0016
# Applies one approved positioning correction to viewer-0014:
# Remove the 8-pixel gap so the standalone SIMBAD target sits flush
# against the coordinate box. Also updates viewer-0014's inherited
# integrity-check token so validation checks the new flush margin.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0014.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_margin_css = '''    margin: 0 0 0 8px !important;'''
new_margin_css = '''    margin: 0 !important;'''

old_integrity_token = '''    ("standalone gap", "margin: 0 0 0 8px !important;"),'''
new_integrity_token = '''    ("standalone flush", "margin: 0 !important;"),'''

if source.count(old_margin_css) < 2:
    raise RuntimeError(
        "viewer-0016: expected the old 8-pixel margin in both CSS and integrity checks"
    )
if old_integrity_token not in source:
    raise RuntimeError("viewer-0016: inherited standalone-gap check was not found")

# Replace only the actual CSS declaration first.
source = source.replace(old_margin_css, new_margin_css, 1)

# Then replace the inherited validation tuple explicitly.
source = source.replace(old_integrity_token, new_integrity_token, 1)
source = source.replace("# viewer-0014", "# viewer-0016", 1)

# Post-edit validation of the generated viewer source.
target_css_anchor = '''#aladin-cosmic-command-test .gv-native-simbad-moved {'''
target_css_start = source.find(target_css_anchor)
target_css_end = source.find("}", target_css_start)

if target_css_start < 0 or target_css_end < 0:
    raise RuntimeError("viewer-0016: target CSS block was not found after editing")

target_css_block = source[target_css_start:target_css_end + 1]

if "margin: 0 !important;" not in target_css_block:
    raise RuntimeError("viewer-0016: target is not configured flush")
if "margin: 0 0 0 8px !important;" in target_css_block:
    raise RuntimeError("viewer-0016: target CSS still contains the 8-pixel gap")
if '("standalone flush", "margin: 0 !important;")' not in source:
    raise RuntimeError("viewer-0016: flush integrity check was not installed")

# Confirm approved styling remains present.
required_tokens = (
    'nativePointer.style.setProperty("border-color", borderColor',
    'nativePointer.style.setProperty("border-width", borderWidth',
    'nativePointer.style.setProperty("border-radius", radius',
    "transform: scale(0.90) !important;",
    'font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace',
    "color: #FFD166 !important;",
)

for token in required_tokens:
    if token not in source:
        raise RuntimeError(f"viewer-0016 integrity check failed: {token}")

exec(compile(source, "viewer-0016.py", "exec"))
