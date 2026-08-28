#!/usr/bin/env python3
"""Galaxy Viewer registration engine 0003.

Preserves the 0001 registration math and the 0002 HTTPS-origin Aladin fix,
while fixing Python 3.12 dataclass/importlib loading by registering the loaded
0001 module in sys.modules before exec_module().

Uses only real published source images + real Aladin Lite renders.
No generated imagery.
"""
from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "gv-orientation-register-0001.py"
MODULE_NAME = "gv_orientation_register_0001_for_0003"

spec = importlib.util.spec_from_file_location(MODULE_NAME, BASE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {BASE}")
mod = importlib.util.module_from_spec(spec)
sys.modules[MODULE_NAME] = mod
spec.loader.exec_module(mod)

_original_render_aladin = mod.render_aladin

async def render_aladin_with_https_origin(page, ra, dec, fov, out, size=640):
    """Ensure Aladin runs under a normal HTTPS origin before set_content()."""
    if not str(page.url).startswith(("http://", "https://")):
        await page.goto(
            "https://gear66me-ui.github.io/Galaxy_Viewer/",
            wait_until="domcontentloaded",
            timeout=60000,
        )
    return await _original_render_aladin(page, ra, dec, fov, out, size)

mod.render_aladin = render_aladin_with_https_origin

if __name__ == "__main__":
    raise SystemExit(asyncio.run(mod.run(mod.parse_args())))
