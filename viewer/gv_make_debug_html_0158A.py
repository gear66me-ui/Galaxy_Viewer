#!/usr/bin/env python3
"""Extract the Build 0158A IPython HTML/Javascript payloads into a plain browser page."""
import ast
import pathlib
import sys

source = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "RC-V1.0.0.9-BLD-0158A.py")
output = pathlib.Path("GV-BLD-0158A-LOCAL.html")
tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
html_parts, js_parts = [], []

for node in ast.walk(tree):
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "display" or not node.args:
        continue
    payload = node.args[0]
    if not isinstance(payload, ast.Call) or not isinstance(payload.func, ast.Name) or not payload.args:
        continue
    kind = payload.func.id
    try:
        value = ast.literal_eval(payload.args[0])
    except Exception:
        continue
    if not isinstance(value, str):
        continue
    if kind == "HTML":
        html_parts.append(value)
    elif kind == "Javascript":
        js_parts.append(value)

if not html_parts or not js_parts:
    raise SystemExit("Could not extract both display(HTML(...)) and display(Javascript(...)) payloads.")

document = "<!doctype html>\n<html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no\"><title>Galaxy Viewer Build 0158A</title></head><body>\n"
document += "\n".join(html_parts)
for js in js_parts:
    document += "\n<script>\n" + js.replace("</script>", "<\\/script>") + "\n</script>\n"
document += "\n</body></html>\n"
output.write_text(document, encoding="utf-8")
print(f"Created {output.resolve()}")
