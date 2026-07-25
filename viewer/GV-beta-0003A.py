from IPython.display import HTML, display

# GV-beta-0003A
# Wrapper that executes GV-beta-0002A so we keep a clean version trail.
# This file is generated automatically – if you need to tweak Viewer code,
# edit GV-beta-0002A.py instead and bump the wrapper accordingly.

import urllib.request, runpy, sys, types, tempfile

REMOTE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0002A.py"
_code = urllib.request.urlopen(REMOTE_URL).read().decode("utf-8")
exec(compile(_code, REMOTE_URL, "exec"), globals())
