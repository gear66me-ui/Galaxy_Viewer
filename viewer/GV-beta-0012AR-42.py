from urllib.request import urlopen

# GV 12AR-42 — ICRSd restoration / rotation-frame fix.
# Baseline: GV-beta-0012AR-41.py
# Purpose: keep Aladin and the visible coordinate overlay in ICRSd so the
# hand-curated aladinRotation values are applied in the same tangent-plane
# basis in which they were curated.

BASE_URL = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0012AR-41.py'

with urlopen(BASE_URL, timeout=30) as response:
    source = response.read().decode('utf-8')


def replace_once(old, new, label):
    global source
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f'12AR-42 PATCH DRIFT [{label}] expected 1 match, found {count}')
    source = source.replace(old, new, 1)

# Roll visible/internal viewer revision only; preserve all AR-41 functionality.
source = source.replace('12AR-41', '12AR-42')

# 1) Aladin render frame: Galactic -> ICRS decimal degrees.
replace_once("cooFrame:'galactic',", "cooFrame:'ICRSd',", 'ALADIN COOFRAME')

# 2) Coordinate overlay state: Galactic -> ICRSD.
replace_once("let frame='GAL',latestRa=HOME.ra,latestDec=HOME.dec;",
             "let frame='ICRSD',latestRa=HOME.ra,latestDec=HOME.dec;",
             'COORDINATE FRAME DEFAULT')

# 3) Lock the coordinate readout in ICRSD for this verification release.
#    This prevents an accidental tap from switching Aladin back to Galactic
#    and rotating the tangent plane away from the curated orientation basis.
replace_once(
    "#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}",
    "#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:none}",
    'COORDINATE FRAME LOCK'
)

# 4) Defensive callback. Even a programmatic frame-change request is forced
#    back to ICRSd, so the rendered sky and the displayed coordinates cannot
#    drift into different reference frames.
old_callback = """coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
        renderCoordinates();
    }});"""
new_callback = """coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(){
        frame='ICRSD';
        try{if(typeof aladin.setFrame==='function')aladin.setFrame('ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
        coordinate?.setFrame('ICRSD');
        renderCoordinates();
    }});"""
replace_once(old_callback, new_callback, 'FRAME CHANGE CALLBACK')

# Release guards: fail loudly instead of silently shipping Galactic rendering.
if "cooFrame:'galactic'" in source:
    raise RuntimeError('12AR-42 ICRSD GUARD FAILED: Galactic Aladin cooFrame remains')
if "let frame='GAL'" in source:
    raise RuntimeError('12AR-42 ICRSD GUARD FAILED: Galactic coordinate default remains')

exec(compile(source, 'GV-beta-0012AR-42.py::<12AR-41-rollup>', 'exec'), globals(), globals())
