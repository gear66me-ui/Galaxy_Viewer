from pathlib import Path

p = Path.home() / "GV_AR05_PUSH/lab/build-doe-continuous-0004.py"
s = p.read_text()

fixes = [
    (
        'for(const e of list.getEntries(){',
        'for(const e of list.getEntries()){',
        3
    ),
    (
        'push(\\"longtask\\,{',
        'push(\\"longtask\\",{',
        1
    ),
]

for old, new, expected in fixes:
    n = s.count(old)
    print(f"FIX {old!r} COUNT={n} EXPECTED={expected}")
    if n != expected:
        raise SystemExit(f"UNEXPECTED COUNT FOR {old!r}: {n}")
    s = s.replace(old, new)

p.write_text(s)
print("015C-2 OBSERVER ANCHOR REPAIR WRITE: PASS")
