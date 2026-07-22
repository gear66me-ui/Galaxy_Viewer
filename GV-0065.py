from __future__ import annotations

import urllib.request

from google.colab import output
from IPython.display import Javascript, display

output.no_vertical_scroll()
display(Javascript("google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})"))

SOURCE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/f085610ad94f22bacb30f23ea5a3bc605a9d619f/GV-0062_DECODED_TMP.py"

with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace("gv0062", "gv0065")
source = source.replace("GV-0062", "GV-0065")
source = source.replace('fov:3.0', 'fov:0.05')
source = source.replace('The default field of view is 3 degrees.', 'The default field of view is 3 arcminutes.')
source = source.replace(
    'function restore(m=""){if(!window.aladin)return;const s=load();document.getElementById("coordBox").value=`${s.ra.toFixed(6)} ${s.dec.toFixed(6)}`;',
    'function restore(m=""){if(!window.aladin||window.gv0065CoordDirty)return;const s=load();'
)
source = source.replace(
    '(async()=>{setup();const s=load();',
    'document.addEventListener("input",e=>{if(e.target&&e.target.id==="coordBox")window.gv0065CoordDirty=true});(async()=>{setup();const s=load();'
)
source = source.replace(
    'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);',
    'async function findGalaxy(){try{const c=coords(document.getElementById("coordBox").value);window.gv0065CoordDirty=false;'
)
source = source.replace(
    'coords = SkyCoord(table[ra_col], table[dec_col], unit=(u.deg, u.deg), frame="icrs")',
    'coords = SkyCoord(ra=table[ra_col], dec=table[dec_col], frame="icrs")'
)

exec(compile(source, "GV-0065.py", "exec"))
