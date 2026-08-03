#!/usr/bin/env python3
"""Build GV Coordinate Digits 0003 from the exact checked-in 0002 font.

Authorized change:
- Preserve every glyph except U+0031 DIGIT ONE.
- Preserve the visible DIGIT ONE outline, translate it horizontally only,
  center it in a 670-unit advance cell, and set its advance width to 670.
"""

from pathlib import Path
import math
import sys

import fontforge
import psMat

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0002.otf"
OUTPUT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0003.otf"
TARGET_ADVANCE = 670
DIGIT_ONE = ord("1")
AUDIT_CODEPOINTS = [ord(char) for char in "0123456789.-"]


def glyph_snapshot(font, codepoint):
    glyph = font[codepoint]
    return {
        "width": int(round(glyph.width)),
        "bbox": tuple(int(round(value)) for value in glyph.boundingBox()),
    }


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Missing exact source font: {SOURCE}")
    if OUTPUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing release font: {OUTPUT}")

    font = fontforge.open(str(SOURCE))
    try:
        before = {codepoint: glyph_snapshot(font, codepoint) for codepoint in AUDIT_CODEPOINTS}
        one = font[DIGIT_ONE]
        old_width = int(round(one.width))
        if old_width != 539:
            raise RuntimeError(f"Expected DIGIT ONE advance 539, found {old_width}")

        x_min, _, x_max, _ = one.boundingBox()
        visual_center = (x_min + x_max) / 2.0
        target_center = TARGET_ADVANCE / 2.0
        shift = int(round(target_center - visual_center))

        one.transform(psMat.translate(shift, 0))
        one.width = TARGET_ADVANCE

        font.familyname = "GV Coordinate Digits 0003"
        font.fullname = "GV Coordinate Digits 0003 Regular"
        font.fontname = "GVCoordinateDigits0003"
        font.version = "1.000"

        after = {codepoint: glyph_snapshot(font, codepoint) for codepoint in AUDIT_CODEPOINTS}

        for codepoint in AUDIT_CODEPOINTS:
            if codepoint == DIGIT_ONE:
                continue
            if after[codepoint] != before[codepoint]:
                char = chr(codepoint)
                raise RuntimeError(
                    f"Unauthorized metric or bounding-box change for {char!r}: "
                    f"before={before[codepoint]} after={after[codepoint]}"
                )

        if after[DIGIT_ONE]["width"] != TARGET_ADVANCE:
            raise RuntimeError(
                f"DIGIT ONE advance is {after[DIGIT_ONE]['width']}, expected {TARGET_ADVANCE}"
            )

        old_bbox = before[DIGIT_ONE]["bbox"]
        new_bbox = after[DIGIT_ONE]["bbox"]
        expected_bbox = (
            old_bbox[0] + shift,
            old_bbox[1],
            old_bbox[2] + shift,
            old_bbox[3],
        )
        if new_bbox != expected_bbox:
            raise RuntimeError(
                f"DIGIT ONE outline changed beyond translation: expected bbox "
                f"{expected_bbox}, found {new_bbox}"
            )

        new_center = (new_bbox[0] + new_bbox[2]) / 2.0
        if abs(new_center - target_center) > 0.5:
            raise RuntimeError(
                f"DIGIT ONE is not centered: center={new_center}, target={target_center}"
            )

        digit_widths = {chr(cp): after[cp]["width"] for cp in map(ord, "0123456789")}
        if set(digit_widths.values()) != {TARGET_ADVANCE}:
            raise RuntimeError(f"Digits are not uniformly {TARGET_ADVANCE} units: {digit_widths}")

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        font.generate(str(OUTPUT), flags=("opentype",))

        print(f"source={SOURCE}")
        print(f"output={OUTPUT}")
        print(f"digit_one_shift={shift}")
        print(f"digit_one_advance={after[DIGIT_ONE]['width']}")
        print(f"digit_one_bbox_before={old_bbox}")
        print(f"digit_one_bbox_after={new_bbox}")
        print(f"digit_widths={digit_widths}")
        print(f"decimal_unchanged={after[ord('.')] == before[ord('.')]}")
        print(f"minus_unchanged={after[ord('-')] == before[ord('-')]}")
    finally:
        font.close()

    if not OUTPUT.is_file() or OUTPUT.stat().st_size == 0:
        raise RuntimeError("Generated font is missing or empty")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
