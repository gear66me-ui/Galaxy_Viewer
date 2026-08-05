#!/usr/bin/env python3
"""Build GV Coordinate Digits 0005 from exact 0004 baseline.

Authorized change:
- Replace only U+0030 DIGIT ZERO with the authoritative slashed-zero outline
  from Space Age GV-9A.
- Fit that source outline to the existing 0004 zero bounding box, then center it
  in the existing 670-unit advance cell.
- Preserve every other encoded glyph exactly.
"""

from pathlib import Path
import hashlib
import json
import fontforge
import psMat

ROOT = Path(__file__).resolve().parents[4]
SOURCE_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/Space Age GV-9A.otf"
BASELINE_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0004.otf"
OUTPUT_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0005.otf"
ZERO = ord("0")
TARGET_ADVANCE = 670


def outline_signature(glyph):
    contours = []
    for contour in glyph.foreground:
        points = []
        for point in contour:
            points.append((round(float(point.x), 6), round(float(point.y), 6), bool(point.on_curve)))
        contours.append((bool(contour.closed), tuple(points)))
    payload = {
        "width": round(float(glyph.width), 6),
        "vwidth": round(float(glyph.vwidth), 6),
        "bbox": tuple(round(float(v), 6) for v in glyph.boundingBox()),
        "contours": tuple(contours),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def encoded_signatures(font):
    return {
        glyph.encoding: outline_signature(glyph)
        for glyph in font.glyphs()
        if glyph.encoding >= 0
    }


def fit_source_zero_to_baseline(source, target):
    sx0, sy0, sx1, sy1 = source.boundingBox()
    tx0, ty0, tx1, ty1 = target.boundingBox()
    sw, sh = sx1 - sx0, sy1 - sy0
    tw, th = tx1 - tx0, ty1 - ty0
    if sw <= 0 or sh <= 0 or tw <= 0 or th <= 0:
        raise RuntimeError("Invalid zero-glyph bounding box")

    scale_x = tw / sw
    scale_y = th / sh
    source.transform(psMat.translate(-sx0, -sy0))
    source.transform(psMat.scale(scale_x, scale_y))
    source.transform(psMat.translate(tx0, ty0))


def build():
    if not SOURCE_FONT.is_file():
        raise FileNotFoundError(SOURCE_FONT)
    if not BASELINE_FONT.is_file():
        raise FileNotFoundError(BASELINE_FONT)
    if OUTPUT_FONT.exists():
        raise FileExistsError(f"Refusing to overwrite {OUTPUT_FONT}")

    source = fontforge.open(str(SOURCE_FONT))
    baseline = fontforge.open(str(BASELINE_FONT))
    try:
        before = encoded_signatures(baseline)
        baseline_zero_bbox = tuple(float(v) for v in baseline[ZERO].boundingBox())
        baseline_zero_width = float(baseline[ZERO].width)
        source_zero_signature = outline_signature(source[ZERO])

        # Copy only the authoritative source zero into the 0004 baseline.
        source.selection.none()
        source.selection.select(ZERO)
        source.copy()
        baseline.selection.none()
        baseline.selection.select(ZERO)
        baseline.paste()

        fit_source_zero_to_baseline(baseline[ZERO], type("Box", (), {"boundingBox": lambda self: baseline_zero_bbox})())
        baseline[ZERO].width = baseline_zero_width

        # Re-center the visible zero in the existing advance cell.
        x0, _, x1, _ = baseline[ZERO].boundingBox()
        shift = (TARGET_ADVANCE / 2.0) - ((x0 + x1) / 2.0)
        baseline[ZERO].transform(psMat.translate(shift, 0))
        baseline[ZERO].width = TARGET_ADVANCE

        baseline.familyname = "GV Coordinate Digits 0005"
        baseline.fullname = "GV Coordinate Digits 0005 Regular"
        baseline.fontname = "GVCoordinateDigits0005"
        baseline.version = "1.000"

        after = encoded_signatures(baseline)
        changed = [cp for cp in before if before[cp] != after.get(cp)]
        if changed != [ZERO]:
            raise RuntimeError(f"Unauthorized glyph changes: {[f'U+{cp:04X}' for cp in changed]}")
        if after[ZERO] == before[ZERO]:
            raise RuntimeError("Zero glyph did not change")
        if outline_signature(baseline[ZERO]) == source_zero_signature:
            print("zero outline copied without geometric fitting")

        OUTPUT_FONT.parent.mkdir(parents=True, exist_ok=True)
        baseline.generate(str(OUTPUT_FONT), flags=("opentype",))
        print(f"generated={OUTPUT_FONT}")
        print(f"zero_bbox_before={baseline_zero_bbox}")
        print(f"zero_bbox_after={baseline[ZERO].boundingBox()}")
        print(f"zero_advance={baseline[ZERO].width}")
        print(f"zero_center_shift={shift:.6f}")
    finally:
        source.close()
        baseline.close()

    # Reopen and verify all non-zero glyphs remain identical to 0004.
    baseline = fontforge.open(str(BASELINE_FONT))
    generated = fontforge.open(str(OUTPUT_FONT))
    try:
        base_sigs = encoded_signatures(baseline)
        out_sigs = encoded_signatures(generated)
        changed = [cp for cp in base_sigs if base_sigs[cp] != out_sigs.get(cp)]
        if changed != [ZERO]:
            raise RuntimeError(f"Generated-font audit failed: {[f'U+{cp:04X}' for cp in changed]}")
        if int(round(generated[ZERO].width)) != TARGET_ADVANCE:
            raise RuntimeError(f"Zero advance changed: {generated[ZERO].width}")
        print("verified_only_changed=U+0030")
    finally:
        baseline.close()
        generated.close()


if __name__ == "__main__":
    build()
