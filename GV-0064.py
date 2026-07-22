from __future__ import annotations

import urllib.request

SOURCE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/f085610ad94f22bacb30f23ea5a3bc605a9d619f/GV-0062_DECODED_TMP.py"

with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace("gv0062", "gv0064")
source = source.replace("GV-0062", "GV-0064")
source = source.replace('fov:3.0', 'fov:0.05')
source = source.replace('The default field of view is 3 degrees.', 'The default field of view is 3 arcminutes.')

exec(compile(source, "GV-0064.py", "exec"))
