# BRIDGE-SEARCH-0012
from __future__ import annotations

import urllib.request

BRIDGE_VERSION = "BRIDGE-SEARCH-0012"
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/07902c7732514e46417e8362cb682fd5ea06d8e4/BRIDGE-SEARCH-0011.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

source = source.replace('BRIDGE_VERSION = "BRIDGE-SEARCH-0011"', 'BRIDGE_VERSION = "BRIDGE-SEARCH-0012"')
source = source.replace('root = "bridge_search_0011_viewer"', 'root = "bridge_search_0012_viewer"')
source = source.replace('BRIDGE-SEARCH-0011-base.py', 'BRIDGE-SEARCH-0012-base.py')
source = source.replace('BRIDGE-SEARCH-0011-runtime.py', 'BRIDGE-SEARCH-0012-runtime.py')

old_size_format = 'return f"{format_linear_size(major_ly, minor_ly)} ({major_arcmin:.2f}′ × {minor_arcmin:.2f}′)"'
new_size_format = 'return f"{format_linear_size(major_ly, minor_ly)} / {major_arcmin:.2f}′ × {minor_arcmin:.2f}′"'

if old_size_format not in source:
    raise RuntimeError("Could not locate the Bridge 11 physical/angular size format")

source = source.replace(old_size_format, new_size_format, 1)

exec(compile(source, "BRIDGE-SEARCH-0012-runtime.py", "exec"), globals())
