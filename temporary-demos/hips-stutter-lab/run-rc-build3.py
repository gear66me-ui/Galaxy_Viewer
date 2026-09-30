#!/usr/bin/env python3
import os, sys, types, runpy, subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
COMMIT="8559bf279f4a285c51397fbceeff4e5ad89d9cd3"
TARGET="viewer/GV-beta-200-027.py"

class _DisplayObj:
    def __init__(self,data): self.data=data
class HTML(_DisplayObj): pass
class Javascript(_DisplayObj): pass
captured=[]
def display(obj):
    if isinstance(obj,(HTML,Javascript)): captured.append(obj)

ip=types.ModuleType("IPython")
ipd=types.ModuleType("IPython.display")
ipd.HTML=HTML; ipd.Javascript=Javascript; ipd.display=display
ip.display=ipd
sys.modules["IPython"]=ip
sys.modules["IPython.display"]=ipd

def execute_exact_build3():
    global captured
    captured=[]
    src=subprocess.check_output(["git","-C",REPO,"show",f"{COMMIT}:{TARGET}"],text=True)
    code=compile(src,f"{COMMIT}:{TARGET}","exec")
    ns={"__name__":"__main__","__file__":TARGET}
    exec(code,ns,ns)
    html="".join(x.data for x in captured if isinstance(x,HTML))
    js="\n".join(x.data for x in captured if isinstance(x,Javascript))
    if not html or not js:
        raise RuntimeError(f"capture failed: HTML={len(html)} JS={len(js)}")
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>GV RC Build 0003 HiPS Lab</title></head><body>{html}<script>{js}</script><script src="/temporary-demos/hips-stutter-lab/hips-lab.js?v=rc10007b0003"></script></body></html>"""

class H(BaseHTTPRequestHandler):
    def send_bytes(self,b,ctype="text/html; charset=utf-8",status=200):
        self.send_response(status); self.send_header("Content-Type",ctype); self.send_header("Content-Length",str(len(b))); self.send_header("Cache-Control","no-store, no-cache, must-revalidate"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        path=self.path.split("?",1)[0]
        if path in ("/","/lab","/rc-build3"):
            try: self.send_bytes(execute_exact_build3().encode())
            except Exception as e: self.send_bytes(("BUILD 0003 PYTHON EXECUTION FAILED\n"+repr(e)).encode(),"text/plain; charset=utf-8",500)
            return
        fs=os.path.abspath(os.path.join(REPO,path.lstrip("/")))
        if not fs.startswith(REPO+os.sep) or not os.path.isfile(fs):
            self.send_bytes(b"404","text/plain",404); return
        ext=os.path.splitext(fs)[1].lower()
        c={".js":"application/javascript",".css":"text/css",".json":"application/json",".png":"image/png",".svg":"image/svg+xml",".jpg":"image/jpeg",".jpeg":"image/jpeg"}.get(ext,"application/octet-stream")
        with open(fs,"rb") as f: self.send_bytes(f.read(),c)
    def log_message(self,fmt,*args): print(fmt%args)

if __name__=="__main__":
    print("EXECUTING EXACT RC V1.0.0.7 BUILD 0003:",COMMIT)
    print("PYTHON PAYLOAD:",TARGET)
    print("CHROME: http://127.0.0.1:8080/rc-build3")
    ThreadingHTTPServer(("127.0.0.1",8080),H).serve_forever()
