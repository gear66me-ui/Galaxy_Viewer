from pathlib import Path

p = Path.home() / "GV_AR05_PUSH/lab/build-doe-continuous-0004.py"
s = p.read_text()

fixes = [
    ('rg.count("const VERSION=0094;")',
     'rg.count("const VERSION=\'0094\';")'),
    ('"const VERSION=0094;"',
     '"const VERSION=\'0094\';"'),
    ('"const VERSION=0095;"',
     '"const VERSION=\'0095\';"'),
    ('"VERSION!==0094"',
     '"VERSION!==\'0094\'"'),
    ('"VERSION!==0095"',
     '"VERSION!==\'0095\'"'),
]

changed = 0
for old, new in fixes:
    n = s.count(old)
    print(f"FIX {old!r}: {n}")
    if n:
        s = s.replace(old, new)
        changed += n

p.write_text(s)
print(f"TOTAL REPLACEMENTS: {changed}")
print("QUOTE REPAIR WRITE: PASS")
