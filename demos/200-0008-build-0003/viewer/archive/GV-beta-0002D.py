from IPython.display import HTML, display

# GV-beta-0002D – standalone viewer (patched Target button)
# cloned from GV-beta-0002A, layout unchanged

import textwrap, re

_original = textwrap.dedent(r"""from IPython.display import HTML, display

# GV-beta-0002A
...""")