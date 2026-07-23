from urllib.request import urlopen

# viewer-0015
# Applies one approved positioning correction to viewer-0014:
# Remove the 8-pixel gap so the standalone SIMBAD target sits flush
# against the coordinate box without changing its shape or styling.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0014.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_margin = '''    margin: 0 0 0 8px !important;'''
new_margin = '''    margin: 0 !important;'''

if old_margin not in source:
    raise RuntimeError("viewer-0015: standalone target margin anchor was not found")

source = source.replace(old_margin, new_margin, 1)
source = source.replace("# viewer-0014", "# viewer-0015", 1)

# Integrity checks: only the horizontal gap is removed.
required_tokens = (
    "margin: 0 !important;",
    'nativePointer.style.setProperty("border-color", borderColor',
    'nativePointer.style.setProperty("border-width", borderWidth',
    'nativePointer.style.setProperty("border-radius", radius',
    "transform: scale(0.90) !important;",
    'font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace',
    "color: #FFD166 !important;",
)

for token in required_tokens:
    if token not in source:
        raise RuntimeError(f"viewer-0015 integrity check failed: {token}")

if "margin: 0 0 0 8px !important;" in source:
    raise RuntimeError("viewer-0015 integrity check failed: 8-pixel gap remains")

exec(compile(source, "viewer-0015.py", "exec"))
