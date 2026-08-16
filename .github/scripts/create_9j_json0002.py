from pathlib import Path
import re
import subprocess

src = Path('viewer/GV-beta-0009I.py')
dst = Path('viewer/GV-beta-0009J.py')
if dst.exists():
    raise SystemExit('REFUSE: viewer/GV-beta-0009J.py already exists')
text = src.read_text()

text = text.replace('# GV-beta-0009I', '# GV-beta-0009J', 1)
text = text.replace("const VERSION='9I';", "const VERSION='9J';", 1)
old_catalog = "const HUBBLE_CATALOG_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0001.json?v=060f0abadd103e320c70f035ac93f42d200eda0f';"
new_catalog = "const HUBBLE_CATALOG_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0002.json?v=c1e850ee3f9476882e7efde5fa24d0a36290a1b3';"
if old_catalog not in text:
    raise SystemExit('REFUSE: exact 9I catalog URL not found')
text = text.replace(old_catalog, new_catalog, 1)

pattern = re.compile(r"    function extractDesignation\(candidate\)\{.*?\n    \}", re.S)
match = pattern.search(text)
if not match:
    raise SystemExit('REFUSE: extractDesignation function not found')
replacement = r'''    function extractDesignation(candidate){
        const texts=[candidate?.designation,candidate?.name,candidate?.title].map(value=>String(value||'').trim()).filter(Boolean);
        const joined=texts.join(' | ');
        if(/\bstephan(?:'|’)?s\s+quintet\b/i.test(joined))return 'HCG 92';
        for(const text of texts){
            let match=text.match(/\bHCG\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bHICKSON(?:\s+COMPACT\s+GROUP)?\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bABELL\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `ABELL ${match[1].toUpperCase()}`;
        }
        const explicit=String(candidate?.designation||'').trim();
        if(explicit)return explicit.replace(/\s+/g,' ').toUpperCase();
        for(const text of texts){
            const match=text.match(/\b(?:M|NGC|IC|UGC|PGC|ARP)\s*[- ]?\s*\d+[A-Z]?\b/i);
            if(match)return match[0].replace(/\s+/g,' ').toUpperCase();
        }
        return '';
    }'''
text = text[:match.start()] + replacement + text[match.end():]

old_block = """        const distance=parseDistanceMly(candidate.distance);\n        const constellation=String(candidate.constellation||'').trim();\n        const designation=extractDesignation(candidate);\n        const commonName=String(candidate.title||candidate.name||'').trim();\n        const age=String(candidate.age??candidate.ageEstimate??candidate.age_estimate??'').trim();\n        const ageYears=Number(candidate.ageYears??candidate.age_years);\n        const sizeRaw=candidate.physicalSizeLy??candidate.physical_size_ly??null;\n        const physicalSizeLy=Array.isArray(sizeRaw)?sizeRaw.map(Number):Number(sizeRaw);"""
new_block = """        const science=(candidate.science&&typeof candidate.science==='object')?candidate.science:{};\n        const scienceDistance=Number(science.distanceMly);\n        const distance=Number.isFinite(scienceDistance)&&scienceDistance>0?scienceDistance:parseDistanceMly(candidate.distance);\n        const constellation=String(candidate.constellation||'').trim();\n        const designation=extractDesignation(candidate);\n        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();\n        const age=String(science.ageDisplay??candidate.age??candidate.ageEstimate??candidate.age_estimate??'').trim();\n        const scienceAgeGyr=Number(science.ageGyr);\n        const ageYears=Number(candidate.ageYears??candidate.age_years??(Number.isFinite(scienceAgeGyr)&&scienceAgeGyr>0?scienceAgeGyr*1e9:NaN));\n        const scienceSizeKly=Array.isArray(science.sizeKly)?science.sizeKly:null;\n        const sizeRaw=candidate.physicalSizeLy??candidate.physical_size_ly??(scienceSizeKly?scienceSizeKly.map(value=>Number(value)*1000):null);\n        const physicalSizeLy=Array.isArray(sizeRaw)?sizeRaw.map(Number):Number(sizeRaw);"""
if old_block not in text:
    raise SystemExit('REFUSE: exact 9I catalog mapping block not found')
text = text.replace(old_block, new_block, 1)
text = text.replace("source:'ESA/HUBBLE GALAXIES CATALOG FULL-0001'", "source:'ESA/HUBBLE GALAXIES CATALOG FULL-0002'", 1)
text = text.replace(
    '# Authorized 9I change: prewarm final Aladin P/DSS2/color survey imagery for the ten Hubble-ready destinations and immediately prioritize the selected destination without changing visible travel choreography.',
    '# 9J: preserves 9I choreography; switches to Hubble sandbox JSON 0002, consumes enriched science fields, and prefers recognized group designations when the image represents a group.',
    1
)
dst.write_text(text)

viewer_blob = subprocess.check_output(['git','hash-object',str(dst)], text=True).strip()
launch_src=Path('mobile/beta/9I.html')
launch_dst=Path('mobile/beta/9J.html')
if launch_dst.exists():
    raise SystemExit('REFUSE: mobile/beta/9J.html already exists')
launcher=launch_src.read_text()
launcher=launcher.replace('GV-9I APP LAUNCHER','GV-9J APP LAUNCHER')
launcher=launcher.replace('Galaxy Viewer 9I','Galaxy Viewer 9J')
launcher=launcher.replace('GALAXY VIEWER BETA 9I','GALAXY VIEWER BETA 9J')
launcher=launcher.replace('GALAXY VIEWER 9I — APP LAUNCHER','GALAXY VIEWER 9J — APP LAUNCHER')
launcher=launcher.replace('GV-beta-0009I.py','GV-beta-0009J.py')
launcher=launcher.replace('GV-BETA-0009I.PY','GV-BETA-0009J.PY')
launcher=launcher.replace('GALAXY VIEWER 9I STARTUP TIMEOUT','GALAXY VIEWER 9J STARTUP TIMEOUT')
launcher=launcher.replace('GALAXY VIEWER 9I APP LAUNCHER FAILURE','GALAXY VIEWER 9J APP LAUNCHER FAILURE')
launcher=launcher.replace('COULD NOT EXTRACT THE VERIFIED 9I FULL VIEWER','COULD NOT EXTRACT THE VERIFIED 9J FULL VIEWER')
launcher=launcher.replace('AUTHORIZED RELEASE: viewer/GV-beta-0009J.py blob 04dffd9eca05022019ab3933595285011ef4cac7',f'AUTHORIZED RELEASE: viewer/GV-beta-0009J.py blob {viewer_blob}')
launcher=launcher.replace("../../viewer/GV-beta-0009J.py?v=04dffd9eca05022019ab3933595285011ef4cac7",f"../../viewer/GV-beta-0009J.py?v={viewer_blob}")
launch_dst.write_text(launcher)

beta_index=Path('mobile/beta/index.html')
index_text=beta_index.read_text()
if "window.location.replace('./9I.html'" not in index_text:
    raise SystemExit('REFUSE: beta index does not currently point to 9I')
beta_index.write_text(index_text.replace("window.location.replace('./9I.html'", "window.location.replace('./9J.html'", 1))

assert 'gv-hubble-galaxies-full-0002.json' in dst.read_text()
assert 'gv-hubble-galaxies-full-0001.json' not in dst.read_text()
assert 'HCG 92' in dst.read_text()
assert 'HICKSON' in dst.read_text()
assert 'ABELL' in dst.read_text()
assert 'science.sizeKly' in dst.read_text()
assert 'science.distanceMly' in dst.read_text()
assert './9J.html' in beta_index.read_text()
print('VIEWER_BLOB='+viewer_blob)
