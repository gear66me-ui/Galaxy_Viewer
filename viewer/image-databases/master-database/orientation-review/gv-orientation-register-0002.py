#!/usr/bin/env python3
"""Galaxy Viewer registration engine 0002.

Fixes 0001 headless Aladin startup by establishing a normal HTTPS origin before
0001 calls page.set_content(). This avoids Chromium's localStorage SecurityError
on about:blank while preserving the validated 0001 registration math.
"""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "gv-orientation-register-0001.py"

spec = importlib.util.spec_from_file_location("gv_orientation_register_0001", BASE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {BASE}")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

_original_render_aladin = mod.render_aladin

async def render_aladin_with_https_origin(page, ra, dec, fov, out, size=640):
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
