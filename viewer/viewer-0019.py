from urllib.request import urlopen

# viewer-0019
# Applies exactly two approved icon-only changes to the working viewer-0017 result:
# 1. Match the SIMBAD target icon to the copy icon palette.
# 2. Reduce the target icon by 10 percent from 90 percent to 81 percent.
# No box, position, border, radius, helper text, or other viewer setting changes.

SOURCE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "beta/viewer/viewer-0014.py"
)

source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

# Preserve the approved flush position.
source = source.replace(
    "    margin: 0 0 0 8px !important;",
    "    margin: 0 !important;",
    1,
)
source = source.replace(
    '("standalone gap", "margin: 0 0 0 8px !important;"),',
    '("standalone flush", "margin: 0 !important;"),',
    1,
)

# Change viewer-0014's generated scale rule from 90 percent to 81 percent.
source = source.replace(
    "    transform: scale(0.90) !important;",
    "    transform: scale(0.81) !important;",
    1,
)
source = source.replace(
    '("single 90-percent scale", "transform: scale(0.90) !important;"),',
    '("single 81-percent scale", "transform: scale(0.81) !important;"),',
    1,
)

# Insert palette replacements into viewer-0014 immediately before it executes
# the fully expanded viewer-0007 source. At that stage the exact JS anchors exist.
old_exec = 'exec(compile(source, "viewer-0014.py", "exec"))'
new_exec = '''# Apply the icon palette change to the fully expanded viewer source.
old_target_class = 'nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-target");'
new_target_class = 'nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-copy");'
old_target_filter = 'nativePointer.style.setProperty("--command-filter", filters.target, "important");'
new_target_filter = 'nativePointer.style.setProperty("--command-filter", filters.copy, "important");'

if old_target_class not in source:
    raise RuntimeError("viewer-0019: expanded target palette class anchor was not found")
if old_target_filter not in source:
    raise RuntimeError("viewer-0019: expanded target palette filter anchor was not found")

source = source.replace(old_target_class, new_target_class, 1)
source = source.replace(old_target_filter, new_target_filter, 1)

# Final requested-state checks on the expanded viewer.
required_final = (
    'margin: 0 !important;',
    'transform: scale(0.81) !important;',
    'nativePointer.classList.add("gv-native-simbad-moved", "gv-command", "gv-copy");',
    'nativePointer.style.setProperty("--command-filter", filters.copy, "important");',
    'nativePointer.style.setProperty("border-color", borderColor',
    'nativePointer.style.setProperty("border-width", borderWidth',
    'nativePointer.style.setProperty("border-radius", radius',
)
for token in required_final:
    if token not in source:
        raise RuntimeError(f"viewer-0019 final integrity check failed: {token}")

compile(source, "viewer-0019-expanded.py", "exec")
exec(compile(source, "viewer-0019-expanded.py", "exec"))'''

if old_exec not in source:
    raise RuntimeError("viewer-0019: viewer-0014 execution anchor was not found")
source = source.replace(old_exec, new_exec, 1)
source = source.replace("# viewer-0014", "# viewer-0019", 1)

# Syntax-check the patched intermediate script before running it.
compile(source, "viewer-0019-intermediate.py", "exec")
exec(compile(source, "viewer-0019-intermediate.py", "exec"))
