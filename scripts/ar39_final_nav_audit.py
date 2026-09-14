from pathlib import Path
import json,re,math,hashlib,difflib,collections,subprocess

root=Path('.')
nav12=root/'viewer/modules/navigation/gv-navigation-0001.js'
nav16=root/'viewer/modules/navigation/gv-navigation-0016.js'
nav17=root/'viewer/modules/navigation/gv-navigation-0017.js'
worker5=root/'viewer/modules/navigation/gv-navigation-worker-0005.js'
worker6=root/'viewer/modules/navigation/gv-navigation-worker-0006.js'
random112=root/'viewer/modules/random-galaxy/gv-random-galaxy-0112.js'
ar38=root/'viewer/GV-beta-0012AR-38.py'
ar39=root/'viewer/GV-beta-0012AR-39.py'
pointer=root/'viewer/gv-current-viewer.json'
hubble=root/'viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0031.json'
audit=root/'docs/audits/GV-12AR39-NAV-AUDIT.md'
for p in [nav12,nav16,worker5,random112,ar38,pointer,hubble]:
    if not p.exists(): raise SystemExit(f'MISSING {p}')

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def toks(s): return re.findall(r'[A-Za-z_$][A-Za-z0-9_$]*|\d+(?:\.\d+)?|[^\s]',s)
def funcs(s):
    z=set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(',s))
    z.update(re.findall(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>',s))
    return z
def stats(a,b):
    sm=difflib.SequenceMatcher(a=a,b=b,autojunk=False); ca=cd=0
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag in ('delete','replace'): cd+=i2-i1
        if tag in ('insert','replace'): ca+=j2-j1
    la=ld=0
    for x in difflib.ndiff(a.splitlines(),b.splitlines()):
        la+=x.startswith('+ '); ld+=x.startswith('- ')
    A=collections.Counter(toks(a)); B=collections.Counter(toks(b)); fa=funcs(a); fb=funcs(b)
    return dict(old_bytes=len(a.encode()),new_bytes=len(b.encode()),byte_delta=len(b.encode())-len(a.encode()),old_chars=len(a),new_chars=len(b),char_delta=len(b)-len(a),chars_added=ca,chars_deleted=cd,old_words=sum(A.values()),new_words=sum(B.values()),words_added=sum((B-A).values()),words_deleted=sum((A-B).values()),old_lines=len(a.splitlines()),new_lines=len(b.splitlines()),lines_added=la,lines_deleted=ld,old_functions=len(fa),new_functions=len(fb),functions_added=sorted(fb-fa),functions_deleted=sorted(fa-fb),old_sha256=sha(a),new_sha256=sha(b))

# Audit Hubble 0031 fields using same mandatory navigation-facing fields.
H=json.loads(hubble.read_text()); entries=H.get('entries',[]); reasons={}; eligible=[]
def pos(v):
    try:return math.isfinite(float(v)) and float(v)>0
    except:return False
def dist(e):
    v=(e.get('science') or {}).get('distanceMly',e.get('distance'))
    if isinstance(v,(int,float)):return float(v) if pos(v) else None
    s=str(v or '').lower().replace(',','')
    m=re.search(r'([0-9]+(?:\.[0-9]+)?)\s*(billion|million|thousand)\s+light\s*-?\s*years?',s)
    if m:
        n=float(m.group(1)); return n*1000 if m.group(2)=='billion' else n if m.group(2)=='million' else n/1000
    m=re.search(r'([0-9]+(?:\.[0-9]+)?)\s+light\s*-?\s*years?',s)
    return float(m.group(1))/1e6 if m else None
for e in entries:
    why=[]
    try: ra=float(e.get('ra')); dec=float(e.get('dec'))
    except: ra=dec=float('nan')
    if not str(e.get('name') or e.get('title') or '').strip(): why.append('name')
    if not math.isfinite(ra) or not 0<=ra<360: why.append('ra')
    if not math.isfinite(dec) or not -90<=dec<=90: why.append('dec')
    if not pos(dist(e)): why.append('distance')
    if not str(e.get('constellation') or '').strip(): why.append('constellation')
    if not pos(e.get('fovDegrees')): why.append('fovDegrees')
    try: okrot=math.isfinite(float(e.get('aladinRotation')))
    except: okrot=False
    if not okrot: why.append('aladinRotation')
    if why:
        for x in why: reasons[x]=reasons.get(x,0)+1
    else: eligible.append(e)
if len(entries)<800 or len(eligible)<700: raise SystemExit(f'HUBBLE AUDIT FAIL raw={len(entries)} eligible={len(eligible)} reasons={reasons}')

# Authoritative 12AR choreography must itself contain the defining constants/ease.
baseline=nav12.read_text()
for token in ['TRANSLATE_START:.30','FOV_APEX:.50','TRANSLATE_END:.70','35*t**4-84*t**5+70*t**6-20*t**7']:
    if token not in baseline: raise SystemExit('12AR BASELINE TOKEN MISSING '+token)

oldnav=nav16.read_text(); s=oldnav
s=s.replace("const VERSION='0016';","const VERSION='0017';",1)
s=s.replace('BOOTSTRAP_TRAVEL_SECONDS: 10','BOOTSTRAP_TRAVEL_SECONDS: 7.5',1).replace('BOOTSTRAP_TRAVEL_SECONDS:10','BOOTSTRAP_TRAVEL_SECONDS:7.5',1)
pos0=s.find('function flightSmootherstep(value)')
if pos0<0: raise SystemExit('flightSmootherstep anchor missing')
s=s[:pos0]+"function flightNavigationSmootherstep(value){const t=flightClamp01(value);return 35*t**4-84*t**5+70*t**6-20*t**7;}\n\n  "+s[pos0:]
replacement=r'''function flightStateAt(sec,{firstHomeTrip,startFov,finalFov,maxFov,startRotation,targetRotation}){
    const duration=firstHomeTrip?7.5:17;
    const t=flightClamp01((Math.max(0,Number(sec)||0))/duration);
    if(firstHomeTrip){
      const translationEnd=flightClamp01(4/duration);
      if(t<translationEnd){
        const p=flightSmootherstep(t/translationEnd);
        return {phase:'12AR_FIRST_TRANSLATE_ROTATE',translation:p,fov:startFov,rotation:startRotation+flightNormalizeRotationDelta(targetRotation-startRotation)*p};
      }
      const p=flightSmootherstep((t-translationEnd)/Math.max(1-translationEnd,0.000001));
      return {phase:'12AR_FIRST_FINAL_ZOOM',translation:1,fov:flightLogLerp(startFov,finalFov,p),rotation:targetRotation};
    }
    const translateStart=0.30;
    const translationComplete=0.70;
    let translation;
    if(t<=translateStart)translation=0;
    else if(t>=translationComplete)translation=1;
    else translation=flightNavigationSmootherstep((t-translateStart)/(translationComplete-translateStart));
    let fov;
    if(t<=0.50){const p=flightNavigationSmootherstep(t/0.50);fov=flightLogLerp(startFov,maxFov,p);}
    else{const p=flightNavigationSmootherstep((t-0.50)/0.50);fov=flightLogLerp(maxFov,finalFov,p);}
    const rotation=startRotation+flightNormalizeRotationDelta(targetRotation-startRotation)*translation;
    return {phase:'12AR_CONTINUOUS_TRIP',translation,fov,rotation};
  }'''
pat=re.compile(r"function flightStateAt\(sec,\{firstHomeTrip,startFov,finalFov,maxFov,startRotation,targetRotation\}\)\{.*?\n  \}\n\n  async function flyViewport",re.S)
if len(pat.findall(s))!=1: raise SystemExit('flightStateAt match count !=1')
s=pat.sub(replacement+'\n\n  async function flyViewport',s,count=1)
old="const durationSeconds=Number(firstHomeTrip?10:17),duration=durationSeconds*1000;\n    const targetRotation=Number.isFinite(Number(destination?.aladinRotation))?Number(destination.aladinRotation):0;"
new="const durationSeconds=Number(firstHomeTrip?7.5:17),duration=durationSeconds*1000;\n    const targetRotation=Number(destination?.aladinRotation);\n    if(!Number.isFinite(targetRotation))throw new Error('DESTINATION aladinRotation IS REQUIRED FOR RANDOM GALAXY TRAVEL');"
if old not in s: raise SystemExit('duration/target anchor missing')
s=s.replace(old,new,1)
old='let destinationCenterApplied=false,finalRotationApplied=false,lastAladinSample=-1,lastBlackBoxSample=-1;'
new='let destinationCenterApplied=false,finalRotationApplied=false,zoomInRotationGuardChecked=false,lastAladinSample=-1,lastBlackBoxSample=-1;'
if old not in s: raise SystemExit('flight flags anchor missing')
s=s.replace(old,new,1)
anchor='const state=flightStateAt(sec,{firstHomeTrip,startFov:startFovNumber,finalFov,maxFov:Number(maxFov),startRotation:actualStartRotation,targetRotation});\n  commandSetFov(aladin,state.fov);'
guard="""const state=flightStateAt(sec,{firstHomeTrip,startFov:startFovNumber,finalFov,maxFov:Number(maxFov),startRotation:actualStartRotation,targetRotation});
  const zoomInStartFraction=firstHomeTrip?(4/durationSeconds):0.50;
  if(!zoomInRotationGuardChecked && t>=zoomInStartFraction){
    const currentSpecRotation=Number(destination?.aladinRotation);
    if(!Number.isFinite(currentSpecRotation) || Math.abs(flightNormalizeRotationDelta(currentSpecRotation-targetRotation))>1e-9)
      throw new Error('DESTINATION aladinRotation CHANGED OR INVALID BEFORE ZOOM IN');
    zoomInRotationGuardChecked=true;
    emitTrace(4780,'ROTATION_SPEC_PRE_ZOOM_IN_OK',{targetRotation,currentSpecRotation});
  }
  commandSetFov(aladin,state.fov);"""
if anchor not in s: raise SystemExit('frame state anchor missing')
s=s.replace(anchor,guard,1)
old="""commandSetFov(aladin,finalFov);
if(!finalRotationApplied && Number.isFinite(targetRotation) && typeof aladin.setRotation==='function'){
  commandSetRotation(aladin,targetRotation); finalRotationApplied=true;
}"""
new="""commandSetFov(aladin,finalFov);
const finalSpecRotation=Number(destination?.aladinRotation);
if(!Number.isFinite(finalSpecRotation) || Math.abs(flightNormalizeRotationDelta(finalSpecRotation-targetRotation))>1e-9)
  throw new Error('DESTINATION aladinRotation CHANGED OR INVALID AT FINAL ROTATION COMMIT');
commandSetRotation(aladin,targetRotation);
finalRotationApplied=true;"""
if old not in s: raise SystemExit('final rotation anchor missing')
s=s.replace(old,new,1)
owner='  // Navigation 0006 is the sole owner of active-viewer motion commands.\n'
if owner not in s: raise SystemExit('motion owner anchor missing')
s=s.replace(owner,owner+'  let lastNavigationCommandedRotation=NaN;\n',1)
old="""  function commandSetRotation(aladin,rotation){
    if(!aladin || typeof aladin.setRotation !== 'function')
      throw new Error('NAVIGATION 0016 setRotation UNAVAILABLE');
    aladin.setRotation(rotation);
  }"""
new="""  function commandSetRotation(aladin,rotation){
    if(!aladin || typeof aladin.setRotation !== 'function')
      throw new Error('NAVIGATION 0017 setRotation UNAVAILABLE');
    const commanded=Number(rotation);
    if(!Number.isFinite(commanded))throw new Error('NAVIGATION 0017 ROTATION COMMAND INVALID');
    lastNavigationCommandedRotation=commanded;
    aladin.setRotation(commanded);
    try{global.dispatchEvent(new CustomEvent('gv-navigation-rotation-command',{detail:{moduleVersion:VERSION,rotation:commanded}}));}catch(_){}
  }

  function getLastCommandedRotation(){
    return Number.isFinite(lastNavigationCommandedRotation)?lastNavigationCommandedRotation:null;
  }"""
if old not in s: raise SystemExit('commandSetRotation anchor missing')
s=s.replace(old,new,1)
if '    commandSetRotation,\n    abortActiveFlight,' not in s: raise SystemExit('export anchor missing')
s=s.replace('    commandSetRotation,\n    abortActiveFlight,','    commandSetRotation,\n    getLastCommandedRotation,\n    abortActiveFlight,',1)
s=s.replace('gv-navigation-worker-0005.js','gv-navigation-worker-0006.js').replace("NAVIGATION_WORKER_VERSION='0005'","NAVIGATION_WORKER_VERSION='0006'").replace('NAVIGATION 0016','NAVIGATION 0017')
for token in ['ZOOM_OUT_ONLY','TRANSLATE_ZOOM_OUT_BLEND','STRAIGHT_TRANSLATE_ROTATE','TRANSLATE_ZOOM_IN_BLEND','ZOOM_IN_ONLY']:
    if token in s: raise SystemExit('STOP/GO TOKEN REMAINS '+token)
for token in ['translateStart=0.30','translationComplete=0.70','t<=0.50','35*t**4-84*t**5+70*t**6-20*t**7','12AR_CONTINUOUS_TRIP']:
    if token not in s: raise SystemExit('12AR GATE MISSING '+token)
fb=s[s.index('async function flyViewport'):s.index('// Navigation 0006 is the sole owner')]
for bad in ['destination?.orientation','destination?.orientationDegrees','destination?.archiveOrientation']:
    if bad in fb: raise SystemExit('FORBIDDEN ROTATION SOURCE '+bad)
if '?Number(destination.aladinRotation):0' in fb: raise SystemExit('ZERO ROTATION FALLBACK REMAINS')
if 'ROTATION_SPEC_PRE_ZOOM_IN_OK' not in fb or 'FINAL ROTATION COMMIT' not in fb: raise SystemExit('ROTATION GUARD MISSING')
nav17.write_text(s)

oldw=worker5.read_text(); w=oldw.replace("WORKER_VERSION='0005'","WORKER_VERSION='0006'").replace('gv-navigation-0016.js','gv-navigation-0017.js').replace("api.VERSION!=='0016'","api.VERSION!=='0017'").replace('NAVIGATION WORKER 0005','NAVIGATION WORKER 0006').replace('NAVIGATION 0016','NAVIGATION 0017'); worker6.write_text(w)

olda=ar38.read_text(); p=olda
for a,b in [('12AR-38','12AR-39'),('GV-beta-0012AR-38.py','GV-beta-0012AR-39.py'),('gv-navigation-0016.js','gv-navigation-0017.js'),("NAVIGATION_VERSION='0016'","NAVIGATION_VERSION='0017'")]: p=p.replace(a,b)
old="""        const updateLiveAladinRotation=()=>{
  try{
      const value=Number(aladin?.getRotation?.());
      rotationReadout.textContent=Number.isFinite(value)
          ? `ALADIN ROTATION ${value.toFixed(1)}°`
          : 'ALADIN ROTATION —';
  }catch(_){rotationReadout.textContent='ALADIN ROTATION —';}
        };"""
new="""        const updateLiveAladinRotation=()=>{
  try{
      const navValue=Number(window.GalaxyViewerNavigation?.getLastCommandedRotation?.());
      const liveValue=Number(aladin?.getRotation?.());
      const navText=Number.isFinite(navValue)?navValue.toFixed(2):'—';
      const liveText=Number.isFinite(liveValue)?liveValue.toFixed(2):'—';
      rotationReadout.textContent=`NAV ROT ${navText} / ALADIN LIVE ROT ${liveText}`;
  }catch(_){rotationReadout.textContent='NAV ROT — / ALADIN LIVE ROT —';}
        };"""
if old not in p: raise SystemExit('rotation readout anchor missing')
p=p.replace(old,new,1).replace("maxWidth:'170px'","maxWidth:'340px'",1)
ar39.write_text(p); pointer.write_text(json.dumps({'version':'12AR-39.py','viewer':'GV-beta-0012AR-39.py'},indent=2)+'\n')

# Full rotation ownership audit.
r=random112.read_text()
random_calls=[(i+1,x.strip()) for i,x in enumerate(r.splitlines()) if 'setRotation(' in x]
nav_calls=[(i+1,x.strip()) for i,x in enumerate(s.splitlines()) if 'setRotation(' in x]
viewer_calls=[(i+1,x.strip()) for i,x in enumerate(p.splitlines()) if 'setRotation(' in x]
if random_calls: raise SystemExit('RANDOM DIRECT setRotation '+repr(random_calls))
bad_view=[x for x in viewer_calls if 'aladin.setRotation(0)' not in x[1]]
if bad_view: raise SystemExit('VIEWER NON-HOME setRotation '+repr(bad_view))
subprocess.run(['node','--check',str(nav17)],check=True)
subprocess.run(['node','--check',str(worker6)],check=True)
subprocess.run(['python3','-m','py_compile',str(ar39)],check=True)
N=stats(oldnav,s); W=stats(oldw,w); A=stats(olda,p)

def row(n,d):return f"| {n} | {d['old_bytes']} | {d['new_bytes']} | {d['byte_delta']:+d} | {d['chars_added']} | {d['chars_deleted']} | {d['words_added']} | {d['words_deleted']} | {d['lines_added']} | {d['lines_deleted']} | {len(d['functions_added'])} | {len(d['functions_deleted'])} |"
lines=['# GV 12AR-39 Navigation Forensic Audit','', '## Executive result',
'- PASS: normal Random Galaxy travel uses the 12AR continuous 17-second choreography: FOV out 0–50%, FOV in 50–100%, translation and rotation 30–70%, seventh-order smootherstep.',
'- PASS: first Earth departure is 7.5 seconds: first 4 seconds translate + rotate with FOV frozen, then coordinates lock and logarithmic zoom-in completes.',
'- PASS: destination `aladinRotation` is mandatory, with no zero fallback and no alternate destination orientation source in active travel.',
'- PASS: `aladinRotation` is checked again at zoom-in boundary and immediately before final rotation commit.',
'- PASS: final arrival reissues the exact captured `aladinRotation` through `commandSetRotation`.',
'- PASS: NAV ROT diagnostics is the exact numeric value stored immediately before the same value is passed to `aladin.setRotation(commanded)`.',
'', '## Hubble 0031',f'- Raw entries: {len(entries)}',f'- Fully eligible: {len(eligible)}',f'- Rejections: `{json.dumps(reasons,sort_keys=True)}`','',
'## Byte / character / token-word / line / function tally','| Transition | Old bytes | New bytes | Δ bytes | chars + | chars - | words + | words - | lines + | lines - | funcs + | funcs - |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|',row('navigation 0016 → 0017',N),row('worker 0005 → 0006',W),row('viewer 12AR-38 → 12AR-39',A),'']
for n,d in [('Navigation',N),('Worker',W),('Viewer',A)]:
    lines += [f'### {n}',f"- Old SHA-256: `{d['old_sha256']}`",f"- New SHA-256: `{d['new_sha256']}`",f"- Old/new characters: {d['old_chars']} / {d['new_chars']} ({d['char_delta']:+d})",f"- Old/new tokenized words/symbols: {d['old_words']} / {d['new_words']}",f"- Old/new lines: {d['old_lines']} / {d['new_lines']}",f"- Old/new functions: {d['old_functions']} / {d['new_functions']}",f"- Functions added: `{d['functions_added']}`",f"- Functions deleted: `{d['functions_deleted']}`",'']
lines += ['## Rotation command sites',f'- Navigation 0017: `{nav_calls}`',f'- Random Galaxy 0112: `{random_calls}`',f'- Viewer 12AR-39: `{viewer_calls}`','',
'## Algorithm review','- PASS: old five independent stop/start flight-phase labels are absent.','- PASS: great-circle center translation and FOV interpolation do not alter the rotation target.','- PASS: Random Galaxy does not directly call `setRotation`; Navigation owns active travel rotation.','- PASS: no `orientation`, `orientationDegrees`, or `archiveOrientation` destination field is accepted by `flyViewport` as a travel rotation target.','- PASS: invalid/missing `aladinRotation` aborts travel rather than silently substituting 0.','- PASS: source mutation is checked at zoom-in start and final commit.','- PASS: final rotation command is unconditional after validation and uses the original exact target.','', '## Static validation','- `node --check gv-navigation-0017.js`: PASS','- `node --check gv-navigation-worker-0006.js`: PASS','- `python -m py_compile GV-beta-0012AR-39.py`: PASS']
audit.parent.mkdir(parents=True,exist_ok=True); audit.write_text('\n'.join(lines)+'\n')
print('AR39 FINAL NAV AUDIT PASS')
print('HUBBLE',len(entries),len(eligible),reasons)
print('NAV',json.dumps(N,sort_keys=True)); print('WORKER',json.dumps(W,sort_keys=True)); print('VIEWER',json.dumps(A,sort_keys=True))
print('NAV CALLS',nav_calls); print('RANDOM CALLS',random_calls); print('VIEWER CALLS',viewer_calls)
