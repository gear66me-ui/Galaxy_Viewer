#!/usr/bin/env python3
"""Build a plain Chrome page from the 0158B IPython payloads; injects no UI."""
import ast
import pathlib
import re
import sys

source = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "RC-V1.0.0.9-BLD-0158B.py")
output = pathlib.Path("GV-BLD-0158B-LOCAL.html")
tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
html_parts, js_parts = [], []

calls = sorted(
    (node for node in ast.walk(tree)
     if isinstance(node, ast.Call)
     and isinstance(node.func, ast.Name)
     and node.func.id == "display"
     and node.args),
    key=lambda node: (node.lineno, node.col_offset),
)

for node in calls:
    payload = node.args[0]
    if not isinstance(payload, ast.Call) or not isinstance(payload.func, ast.Name) or not payload.args:
        continue
    try:
        value = ast.literal_eval(payload.args[0])
    except Exception:
        continue
    if not isinstance(value, str):
        continue
    if payload.func.id == "HTML":
        html_parts.append(value)
    elif payload.func.id == "Javascript":
        js_parts.append(value)

if len(html_parts) != 1 or len(js_parts) != 1:
    raise SystemExit(f"Expected exactly one HTML and one Javascript payload; found HTML={len(html_parts)} JS={len(js_parts)}")

document = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Galaxy Viewer Build 0158B</title></head><body>
"""
document += html_parts[0]
safe_js = re.sub(r"</script", r"<\/script", js_parts[0], flags=re.IGNORECASE)
document += "\n<script>\n" + safe_js + "\n</script>\n</body></html>\n"
output.write_text(document, encoding="utf-8")
print(f"Created {output.resolve()} ({output.stat().st_size} bytes)")
