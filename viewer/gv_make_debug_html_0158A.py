#!/usr/bin/env python3
"""Generate a uniquely named, cache-busted standalone HTML test page for Build 0158A."""
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

document = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">
<title>Galaxy Viewer — Build 0158A Local Test</title>
<style>
html,body{margin:0;width:100%;height:100%;background:#000;color:#fff}
#gv-0158a-status{position:fixed;z-index:2147483646;top:8px;left:8px;right:8px;padding:8px 10px;background:#171717;color:#ddd;font:12px monospace;border:1px solid #555}
#gv-0158a-error{position:fixed;z-index:2147483647;inset:8px;overflow:auto;white-space:pre-wrap;word-break:break-word;background:#160909;color:#ffb4b4;border:2px solid #ff5555;border-radius:8px;padding:14px;font:14px/1.45 monospace}
</style></head><body>
<div id="gv-0158a-status">BUILD 0158A — PAGE LOADED; INITIALIZING VIEWER…</div>
<script>
(function(){
 function report(label,detail){
  var p=document.getElementById("gv-0158a-error");
  if(!p){p=document.createElement("pre");p.id="gv-0158a-error";document.body.appendChild(p);}
  p.textContent="GALAXY VIEWER "+label+"\n\n"+String(detail&&(detail.stack||detail.message)||detail||"Unknown error");
 }
 window.addEventListener("error",function(e){report("SCRIPT ERROR",e.error||e.message||e);});
 window.addEventListener("unhandledrejection",function(e){report("UNHANDLED PROMISE REJECTION",e.reason);});
})();
</script>
"""
document += "\n".join(html_parts)
for js in js_parts:
    document += "\n<script>\n" + js.replace("</script>", "<\\/script>") + "\n</script>\n"
document += "\n</body></html>\n"
output.write_text(document, encoding="utf-8")
print(f"Created {output.resolve()} from {source} ({len(html_parts)} HTML block(s), {len(js_parts)} JavaScript block(s)).")
