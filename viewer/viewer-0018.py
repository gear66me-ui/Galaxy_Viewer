from urllib.request import urlopen

# viewer-0018
# Applies exactly two approved target-icon corrections to viewer-0014:
# 1. Preserve the viewer-0017 flush target position.
# 2. Match the target icon to the copy-control palette.
# 3. Reduce the current 90-percent target size by 10 percent, to 81 percent.
# No other viewer styling or behavior is changed.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0014.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

# Preserve the approved flush position from viewer-0017.
old_margin = "    margin: 0 0 0 8px !important;"
new_margin = "    margin: 0 !important;"

# Match the target icon to the copy icon's existing palette class and filter.
old_target_class = (
    'nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-target");'
)
new_target_class = (
    'nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-copy");'
)

old_target_filter = (
    'nativePointer.style.setProperty("--command-filter", filters.target, "important");'
)
new_target_filter = (
    'nativePointer.style.setProperty("--command-filter", filters.copy, "important");'
)

# A 10-percent reduction from the approved 90-percent size is 81 percent.
old_scale = "    transform: scale(0.90) !important;"
new_scale = "    transform: scale(0.81) !important;"

required_anchors = (
    ("flush margin", old_margin),
    ("target palette class", old_target_class),
    ("target palette filter", old_target_filter),
    ("target scale", old_scale),
)

for label, anchor in required_anchors:
    if anchor not in source:
        raise RuntimeError(f"viewer-0018: {label} anchor was not found")

source = source.replace(old_margin, new_margin, 1)
source = source.replace(old_target_class, new_target_class, 1)
source = source.replace(old_target_filter, new_target_filter, 1)
source = source.replace(old_scale, new_scale, 1)

# Update viewer-0014's inherited integrity-check expectations.
source = source.replace(
    '("standalone gap", "margin: 0 0 0 8px !important;"),',
    '("standalone flush", "margin: 0 !important;"),',
    1,
)
source = source.replace(
    '("single 90-percent scale", "transform: scale(0.90) !important;"),',
    '("single 81-percent scale", "transform: scale(0.81) !important;"),',
    1,
)
source = source.replace("# viewer-0014", "# viewer-0018", 1)

# Verify the generated viewer contains exactly the requested changes.
checks = (
    ("flush target", "margin: 0 !important;"),
    ("copy palette class", '"gv-native-simbad-moved", "gv-command", "gv-copy"'),
    ("copy palette filter", '"--command-filter", filters.copy'),
    ("81-percent scale", "transform: scale(0.81) !important;"),
    ("matched border color logic", 'nativePointer.style.setProperty("border-color", borderColor'),
    ("matched border width logic", 'nativePointer.style.setProperty("border-width", borderWidth'),
    ("matched radius logic", 'nativePointer.style.setProperty("border-radius", radius'),
    ("technical helper font", 'font-family: "Roboto Mono", "DejaVu Sans Mono", Consolas, monospace'),
    ("yellow helper text", "color: #FFD166 !important;"),
)

for label, token in checks:
    if token not in source:
        raise RuntimeError(f"viewer-0018 integrity check failed: {label}")

for forbidden in (
    '"gv-native-simbad-moved", "gv-command", "gv-target"',
    '"--command-filter", filters.target',
    "transform: scale(0.90) !important;",
):
    if forbidden in source:
        raise RuntimeError(f"viewer-0018 still contains superseded target setting: {forbidden}")

compile(source, "viewer-0018-expanded.py", "exec")
exec(compile(source, "viewer-0018-expanded.py", "exec"))
