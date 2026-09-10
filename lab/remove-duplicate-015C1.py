from pathlib import Path
p = Path.home() / "GV_AR05_PUSH/lab/build-doe-continuous-0004.py"
s = p.read_text()

marker = "# 015C-1"
hits = []
start = 0
while True:
    i = s.find(marker, start)
    if i < 0:
        break
    hits.append(i)
    start = i + 1

print("015C-1 MARKER COUNT:", len(hits))

if len(hits) != 2:
    raise SystemExit("EXPECTED EXACTLY 2 015C-1 BLOCKS")

cut = s.rfind("\n# ============================================================", 0, hits[1])
if cut < 0:
    raise SystemExit("SECOND BLOCK START NOT FOUND")

p.write_text(s[:cut].rstrip() + "\n")
print("DUPLICATE 015C-1 BLOCK REMOVED: PASS")
print("RESTORED SIZE:", p.stat().st_size)
