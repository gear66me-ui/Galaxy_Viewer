from pathlib import Path
import base64
import sys

nav=Path(sys.argv[1])

helper=base64.b64decode(sys.argv[2]).decode("utf-8")
old_init=base64.b64decode(sys.argv[3]).decode("utf-8")
new_init=base64.b64decode(sys.argv[4]).decode("utf-8")

s=nav.read_text()

marker="  class RoutePlanner{\n"

if s.count(marker)!=1:
    raise SystemExit(f"FAIL — ROUTEPLANNER MARKER COUNT {s.count(marker)}")

if "NAVIGATION_WORKER_VERSION='0001'" in s:
    raise SystemExit("FAIL — WORKER HELPER ALREADY PRESENT")

if s.count(old_init)!=1:
    raise SystemExit(f"FAIL — INITIALIZE BASELINE COUNT {s.count(old_init)}")

s=s.replace(marker,helper+marker,1)
s=s.replace(old_init,new_init,1)

nav.write_text(s)
