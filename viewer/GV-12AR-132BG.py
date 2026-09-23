from IPython.display import display
import urllib.request

# 12AR-132BG — authorized BG roll.
# Loads BD source, changes only the visible revision and AVM module filename.
# Random Galaxy and Navigation module filenames remain unchanged.

BD_RAW_URL = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-12AR-132BD.py?bg=132BG-avm0055-20260923'

src = urllib.request.urlopen(BD_RAW_URL, timeout=30).read().decode('utf-8')

src = src.replace('12AR-132BD', '12AR-132BG')
src = src.replace('GV-12AR-132BD.py', 'GV-12AR-132BG.py')
src = src.replace('gv-avm-overlay-lab-0053.js', 'gv-avm-overlay-lab-0055.js')
src = src.replace('AVM0053', 'AVM0055')
src = src.replace('AVM 0053', 'AVM 0055')

exec(compile(src, 'GV-12AR-132BG.py <- GV-12AR-132BD.py', 'exec'), globals(), globals())
