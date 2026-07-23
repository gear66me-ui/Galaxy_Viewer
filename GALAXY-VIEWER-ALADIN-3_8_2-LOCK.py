from __future__ import annotations

import urllib.request

# GALAXY VIEWER ALADIN API LOCK — DO NOT EDIT
# Locks the complete reviewed VIEWER-46-4 chain and rewrites only the Aladin
# script endpoint from moving "latest" to the fixed official 3.8.2 release.
LOCKED_VIEWER_COMMIT = "7faf2b22a47244e3fa1b74fdb7b6602d4758fd53"
LOCKED_VIEWER_FILE = "VIEWER-46-4.py"
PINNED_ALADIN_VERSION = "3.8.2"

_original_urlopen = urllib.request.urlopen

class _PinnedResponse:
    def __init__(self, response):
        self._response = response

    def read(self, *args, **kwargs):
        data = self._response.read(*args, **kwargs)
        if isinstance(data, bytes):
            data = data.replace(
                b"https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js",
                b"https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js",
            )
            data = data.replace(
                b"https://aladin.u-strasbg.fr/AladinLite/api/v3/latest/aladin.js",
                b"https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js",
            )
        return data

    def __enter__(self):
        self._response.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._response.__exit__(exc_type, exc, tb)

    def __getattr__(self, name):
        return getattr(self._response, name)

def _pinned_urlopen(*args, **kwargs):
    return _PinnedResponse(_original_urlopen(*args, **kwargs))

urllib.request.urlopen = _pinned_urlopen
try:
    base_url = (
        "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
        f"{LOCKED_VIEWER_COMMIT}/{LOCKED_VIEWER_FILE}"
    )
    with _original_urlopen(base_url, timeout=60) as response:
        source = response.read().decode("utf-8")
    source = source.replace(
        "https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js",
        "https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js",
    )
    source = source.replace(
        "https://aladin.u-strasbg.fr/AladinLite/api/v3/latest/aladin.js",
        "https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js",
    )
    exec(compile(source, "GALAXY-VIEWER-ALADIN-3_8_2-LOCK.py", "exec"))
finally:
    urllib.request.urlopen = _original_urlopen
