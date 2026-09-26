from IPython.display import Javascript, display
from urllib.request import urlopen

# ECO-20260829-12AI-RANDOM-DIRECT-NAV-064
# Diagnostic shell: execute the exact frozen 12AH source from commit
# 618ffddd92e0d8bf964327d51316b373f1c83ece, change only the displayed/runtime
# Viewer identity to 12AI, then install Random Navigation 0064 as a navigation-only
# overlay. 12AH and Random Galaxy 0063 remain immutable.

_BASE_COMMIT = "618ffddd92e0d8bf964327d51316b373f1c83ece"
_BASE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    f"{_BASE_COMMIT}/viewer/GV-beta-0012AH.py"
)

_source = urlopen(_BASE_URL, timeout=30).read().decode("utf-8")

_replacements = (
    ("version.textContent='VERSION 12AH'", "version.textContent='VERSION 12AI'"),
    ("const VERSION='12AH';", "const VERSION='12AI';"),
    ("const DISPLAY_VERSION='12AH';", "const DISPLAY_VERSION='12AI';"),
)

for _old, _new in _replacements:
    _count = _source.count(_old)
    if _count != 1:
        raise RuntimeError(
            f"12AI BASELINE IDENTITY ANCHOR COUNT MISMATCH: {_old!r} -> {_count}"
        )
    _source = _source.replace(_old, _new, 1)

exec(compile(_source, _BASE_URL, "exec"), globals(), globals())

# Load the isolated 0064 navigation experiment after the frozen 12AH runtime has
# been emitted. 0064 polls until the 0063 integration/future queue is fully ready,
# then intercepts only the physical RANDOM GALAXY click before the 0063 transaction
# wrapper. All prefetch, download, HD, archive, diagnostics, and travel presentation
# remain owned by the frozen 0063/12AH baseline.
display(Javascript(r"""
(()=>{
    'use strict';
    const url='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/random-galaxy/gv-random-galaxy-0064.js?v=0064';
    const key='gvRandomNavigation0064';

    const existing=[...document.scripts].find(
        script=>script.dataset.gvLoaderKey===key
    );
    if(existing)return;

    const script=document.createElement('script');
    script.src=url;
    script.async=true;
    script.dataset.gvLoaderKey=key;
    script.addEventListener('load',()=>{
        script.dataset.ready='1';
        console.info('GALAXY VIEWER RANDOM NAVIGATION 0064 SCRIPT LOADED');
    },{once:true});
    script.addEventListener('error',()=>{
        console.error('GALAXY VIEWER RANDOM NAVIGATION 0064 SCRIPT LOAD FAILED',url);
    },{once:true});
    document.head.appendChild(script);
})();
"""))
