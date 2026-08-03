#!/usr/bin/env python3
"""Build coordinate font 0004 and viewer 7K from exact O3/7J baselines."""

from pathlib import Path
import sys
import fontforge
import psMat

ROOT = Path(__file__).resolve().parents[4]
SOURCE_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0003.otf"
OUTPUT_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0004.otf"
SOURCE_VIEWER = ROOT / "viewer/GV-beta-0007J.py"
OUTPUT_VIEWER = ROOT / "viewer/GV-beta-0007K.py"
AUTHORIZED = "0123456789."
DIGITS = "0123456789"
DIGIT_ADVANCE = 670
DECIMAL_ADVANCE = 279
MAX_CENTER_ERROR = 0.5


def snap(glyph):
    return {
        "width": float(glyph.width),
        "bbox": tuple(float(v) for v in glyph.boundingBox()),
    }


def center_error(glyph):
    x_min, _, x_max, _ = glyph.boundingBox()
    return ((x_min + x_max) / 2.0) - (float(glyph.width) / 2.0)


def build_font():
    if OUTPUT_FONT.exists():
        raise FileExistsError(f"Refusing to overwrite {OUTPUT_FONT}")
    font = fontforge.open(str(SOURCE_FONT))
    try:
        before = {glyph.encoding: snap(glyph) for glyph in font.glyphs() if glyph.encoding >= 0}
        expected_shapes = {ord(c): snap(font[ord(c)]) for c in AUTHORIZED}

        for char in AUTHORIZED:
            glyph = font[ord(char)]
            expected_advance = DIGIT_ADVANCE if char in DIGITS else DECIMAL_ADVANCE
            if int(round(glyph.width)) != expected_advance:
                raise RuntimeError(f"Unexpected {char!r} advance: {glyph.width}")
            x_min, _, x_max, _ = glyph.boundingBox()
            shift = (expected_advance / 2.0) - ((x_min + x_max) / 2.0)
            glyph.transform(psMat.translate(shift, 0))
            glyph.width = expected_advance
            print(f"center {char}: shift={shift:.3f}")

        font.familyname = "GV Coordinate Digits 0004"
        font.fullname = "GV Coordinate Digits 0004 Regular"
        font.fontname = "GVCoordinateDigits0004"
        font.version = "1.000"

        for codepoint, original in before.items():
            if chr(codepoint) in AUTHORIZED:
                continue
            if snap(font[codepoint]) != original:
                raise RuntimeError(f"Unauthorized in-memory glyph change U+{codepoint:04X}")

        for char in AUTHORIZED:
            current = snap(font[ord(char)])
            original = expected_shapes[ord(char)]
            if abs((current["bbox"][2] - current["bbox"][0]) - (original["bbox"][2] - original["bbox"][0])) > 0.001:
                raise RuntimeError(f"Outline width changed for {char!r}")
            if current["bbox"][1:] [0] != original["bbox"][1:] [0] or current["bbox"][3] != original["bbox"][3]:
                raise RuntimeError(f"Vertical bounds changed for {char!r}")

        OUTPUT_FONT.parent.mkdir(parents=True, exist_ok=True)
        font.generate(str(OUTPUT_FONT), flags=("opentype",))
    finally:
        font.close()


def verify_font():
    source = fontforge.open(str(SOURCE_FONT))
    generated = fontforge.open(str(OUTPUT_FONT))
    try:
        for char in DIGITS:
            glyph = generated[ord(char)]
            if int(round(glyph.width)) != DIGIT_ADVANCE:
                raise RuntimeError(f"Digit {char} advance failed: {glyph.width}")
            error = abs(center_error(glyph))
            if error > MAX_CENTER_ERROR:
                raise RuntimeError(f"Digit {char} center error {error}")
            src = snap(source[ord(char)])
            dst = snap(glyph)
            if abs((src["bbox"][2]-src["bbox"][0])-(dst["bbox"][2]-dst["bbox"][0])) > 0.001:
                raise RuntimeError(f"Digit {char} outline width changed")
            if src["bbox"][1] != dst["bbox"][1] or src["bbox"][3] != dst["bbox"][3]:
                raise RuntimeError(f"Digit {char} vertical bounds changed")
            print(f"verified {char}: bbox={dst['bbox']} center_error={center_error(glyph):.3f}")

        decimal = generated[ord(".")]
        if int(round(decimal.width)) != DECIMAL_ADVANCE:
            raise RuntimeError(f"Decimal advance failed: {decimal.width}")
        if abs(center_error(decimal)) > MAX_CENTER_ERROR:
            raise RuntimeError(f"Decimal center error {center_error(decimal)}")
        print(f"verified .: bbox={snap(decimal)['bbox']} center_error={center_error(decimal):.3f}")

        for glyph in source.glyphs():
            cp = glyph.encoding
            if cp < 0 or chr(cp) in AUTHORIZED:
                continue
            if snap(generated[cp]) != snap(glyph):
                raise RuntimeError(f"Unauthorized generated glyph change U+{cp:04X}")
    finally:
        source.close()
        generated.close()


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {label}, found {count}")
    return text.replace(old, new, 1)


def build_viewer():
    if OUTPUT_VIEWER.exists():
        raise FileExistsError(f"Refusing to overwrite {OUTPUT_VIEWER}")
    source = SOURCE_VIEWER.read_text(encoding="utf-8")
    text = source
    text = replace_once(
        text,
        "# GV-beta-0007J\n# Standalone Galaxy Viewer release created from the exact verified GV-beta-0007I baseline.\n# USER INSTRUCTION: Preserve all approved 7I behavior; use coordinate font 0003, equalize digit 1 width, anchor both decimal points, and remove value-driven horizontal scaling.",
        "# GV-beta-0007K\n# Standalone Galaxy Viewer release created from the exact verified GV-beta-0007J baseline.\n# USER INSTRUCTION: Preserve all approved 7J behavior; use centered coordinate font 0004 and explicitly apply it to every numeric child span.",
        "release header",
    )
    text = replace_once(
        text,
        "GV-Coordinate-Digits-0003.otf?v=7J-coordinate-digits-0003",
        "GV-Coordinate-Digits-0004.otf?v=7K-centered-coordinate-digits-0004",
        "font reference",
    )
    text = replace_once(
        text,
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-integer{grid-column:1!important;display:block!important;min-width:0!important;text-align:right!important;white-space:nowrap!important}',
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-integer{grid-column:1!important;display:block!important;min-width:0!important;text-align:right!important;white-space:nowrap!important;font-family:"GV Coordinate Digits",sans-serif!important}',
        "integer font rule",
    )
    text = replace_once(
        text,
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-decimal{grid-column:2!important;display:block!important;width:.279em!important;text-align:center!important;white-space:nowrap!important}',
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-decimal{grid-column:2!important;display:block!important;width:.279em!important;text-align:center!important;white-space:nowrap!important;font-family:"GV Coordinate Digits",sans-serif!important}',
        "decimal font rule",
    )
    text = replace_once(
        text,
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-fraction{grid-column:3!important;display:block!important;width:2.68em!important;text-align:left!important;white-space:nowrap!important}',
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-fraction{grid-column:3!important;display:block!important;width:2.68em!important;text-align:left!important;white-space:nowrap!important;font-family:"GV Coordinate Digits",sans-serif!important}',
        "fraction font rule",
    )
    text = replace_once(text, 'versionLabel.textContent="V-7J"', 'versionLabel.textContent="V-7K"', "version label")
    text = replace_once(text, '# GV-beta-0007J staged', '# GV-beta-0007K staged', "staged marker")
    for token in ["GV-Coordinate-Digits-0003.otf?v=7J-coordinate-digits-0003", 'versionLabel.textContent="V-7J"']:
        if token in text:
            raise RuntimeError(f"Forbidden 7J token remains: {token}")
    OUTPUT_VIEWER.write_text(text, encoding="utf-8")
    print(f"generated viewer={OUTPUT_VIEWER} chars={len(text)}")


def main():
    if not SOURCE_FONT.is_file() or not SOURCE_VIEWER.is_file():
        raise FileNotFoundError("Missing exact O3 or 7J baseline")
    build_font()
    verify_font()
    build_viewer()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
