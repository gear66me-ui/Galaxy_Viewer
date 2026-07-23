from urllib.request import urlopen

# viewer-0017
# Applies exactly one approved positioning correction to viewer-0014:
# remove the 8-pixel left margin so the standalone SIMBAD target sits
# flush against the coordinate box. No other viewer styling is changed.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0014.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

old_margin_declaration = "    margin: 0 0 0 8px !important;"
new_margin_declaration = "    margin: 0 !important;"

old_integrity_entry = (
    '    ("standalone gap", "margin: 0 0 0 8px !important;"),'
)
new_integrity_entry = (
    '    ("standalone flush", "margin: 0 !important;"),'
)

if old_margin_declaration not in source:
    raise RuntimeError("viewer-0017: target margin declaration was not found")

source = source.replace(
    old_margin_declaration,
    new_margin_declaration,
    1,
)

if old_integrity_entry in source:
    source = source.replace(
        old_integrity_entry,
        new_integrity_entry,
        1,
    )

source = source.replace("# viewer-0014", "# viewer-0017", 1)

# Validate only the generated target CSS block, not comments or check strings.
target_selector = "#aladin-cosmic-command-test .gv-native-simbad-moved {"
target_start = source.find(target_selector)
target_end = source.find("}", target_start)

if target_start < 0 or target_end < 0:
    raise RuntimeError("viewer-0017: target CSS block was not found")

target_block = source[target_start:target_end + 1]

if new_margin_declaration not in target_block:
    raise RuntimeError("viewer-0017: flush target margin was not installed")
if old_margin_declaration in target_block:
    raise RuntimeError("viewer-0017: 8-pixel target margin remains")

# Confirm approved styling remains present and untouched.
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
        raise RuntimeError(f"viewer-0017 integrity check failed: {token}")

compile(source, "viewer-0017-expanded.py", "exec")
exec(compile(source, "viewer-0017-expanded.py", "exec"))
