from pathlib import Path

files = [
    (Path.home() / "GV_AR05_PUSH/lab/build-doe-continuous-0004.py", 2),
    (Path.home() / "GV_AR05_PUSH/viewer/modules/diagnostics/gv-stutter-lab-0004.js", 2),
]

old = "const end=Number(run.measurementEndedPerfMs);"
new = """const end=
          run.measurementEndedPerfMs===null ||
          run.measurementEndedPerfMs===undefined
            ? null
            : Number(run.measurementEndedPerfMs);"""

for path, expected in files:
    s = path.read_text()
    n = s.count(old)
    print(f"{path.name}: NULL-END ANCHOR COUNT={n} EXPECTED={expected}")
    if n != expected:
        raise SystemExit(f"UNEXPECTED NULL-END ANCHOR COUNT IN {path}: {n}")
    path.write_text(s.replace(old, new))
    print(f"{path.name}: NULL-END REPAIR WRITE — PASS")

print("015E OBSERVER NULL-END REPAIR — PASS")
