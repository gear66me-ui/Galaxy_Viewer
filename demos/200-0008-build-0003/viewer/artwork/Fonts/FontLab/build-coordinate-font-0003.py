#!/usr/bin/env python3
"""Build or verify coordinate font 0003 and generate viewer 7J from exact 7I.

Authorized changes:
- Preserve every font glyph except U+0031 DIGIT ONE.
- Preserve the visible DIGIT ONE outline, translate it horizontally only,
  center it in a 670-unit advance cell, and set its advance width to 670.
- Generate standalone viewer 7J from exact viewer 7I using guarded substitutions.
- Use font 0003, fixed decimal anchors, and no value-driven horizontal scaling.
"""

from pathlib import Path
import sys

import fontforge
import psMat

ROOT = Path(__file__).resolve().parents[4]
SOURCE_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0002.otf"
OUTPUT_FONT = ROOT / "viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0003.otf"
SOURCE_VIEWER = ROOT / "viewer/GV-beta-0007I.py"
OUTPUT_VIEWER = ROOT / "viewer/GV-beta-0007J.py"
TARGET_ADVANCE = 670
DIGIT_ONE = ord("1")
AUDIT_CODEPOINTS = [ord(char) for char in "0123456789.-"]


def glyph_snapshot(font, codepoint):
    glyph = font[codepoint]
    return {
        "width": int(round(glyph.width)),
        "bbox": tuple(int(round(value)) for value in glyph.boundingBox()),
    }


def verify_font_0003():
    generated = fontforge.open(str(OUTPUT_FONT))
    try:
        after = {codepoint: glyph_snapshot(generated, codepoint) for codepoint in AUDIT_CODEPOINTS}
        digit_widths = {chr(cp): after[cp]["width"] for cp in map(ord, "0123456789")}
        if set(digit_widths.values()) != {TARGET_ADVANCE}:
            raise RuntimeError(f"Digits are not uniformly {TARGET_ADVANCE} units: {digit_widths}")
        if after[ord(".")]["width"] != 279:
            raise RuntimeError(f"Decimal advance changed: {after[ord('.')]['width']}")
        if after[ord("-")]["width"] != 577:
            raise RuntimeError(f"Minus advance changed: {after[ord('-')]['width']}")

        print(f"verified_digit_widths={digit_widths}")
        print(f"verified_digit_one_bbox={after[DIGIT_ONE]['bbox']}")
        print(f"verified_decimal_advance={after[ord('.')]['width']}")
        print(f"verified_minus_advance={after[ord('-')]['width']}")
    finally:
        generated.close()


def build_font_0003():
    font = fontforge.open(str(SOURCE_FONT))
    try:
        before = {codepoint: glyph_snapshot(font, codepoint) for codepoint in AUDIT_CODEPOINTS}
        one = font[DIGIT_ONE]
        if int(round(one.width)) != 539:
            raise RuntimeError(f"Expected DIGIT ONE advance 539, found {one.width}")

        x_min, _, x_max, _ = one.boundingBox()
        shift = int(round(TARGET_ADVANCE / 2.0 - (x_min + x_max) / 2.0))
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
                raise RuntimeError(f"Unauthorized font change for {chr(codepoint)!r}")

        OUTPUT_FONT.parent.mkdir(parents=True, exist_ok=True)
        font.generate(str(OUTPUT_FONT), flags=("opentype",))
        print(f"generated_font={OUTPUT_FONT}")
        print(f"digit_one_shift={shift}")
    finally:
        font.close()


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one {label} block, found {count}")
    return text.replace(old, new, 1)


def generate_viewer_7j():
    if not SOURCE_VIEWER.is_file():
        raise FileNotFoundError(f"Missing exact viewer baseline: {SOURCE_VIEWER}")
    if OUTPUT_VIEWER.exists():
        raise FileExistsError(f"Refusing to overwrite existing viewer release: {OUTPUT_VIEWER}")

    source = SOURCE_VIEWER.read_text(encoding="utf-8")
    text = source

    text = replace_once(
        text,
        "# GV-beta-0007I\n# Standalone Galaxy Viewer release created from the exact verified GV-beta-0007H baseline.\n# USER INSTRUCTION: Preserve all approved 7H behavior; reduce the frame-label region to 52 pixels, floor-align the 60 percent final D, and stabilize equal X/lambda/Y geometry.",
        "# GV-beta-0007J\n# Standalone Galaxy Viewer release created from the exact verified GV-beta-0007I baseline.\n# USER INSTRUCTION: Preserve all approved 7I behavior; use coordinate font 0003, equalize digit 1 width, anchor both decimal points, and remove value-driven horizontal scaling.",
        "release header",
    )

    text = replace_once(
        text,
        "GV-Coordinate-Digits-0002.otf?v=6Z-coordinate-digits-0002",
        "GV-Coordinate-Digits-0003.otf?v=7J-coordinate-digits-0003",
        "coordinate font reference",
    )

    old_axis_css = '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-axis{position:relative!important;z-index:1!important;display:block!important;min-width:0!important;overflow:hidden!important;font-family:"GV Coordinate Digits",sans-serif!important;font-variant-numeric:normal!important;font-feature-settings:normal!important;letter-spacing:0!important;white-space:pre!important;transform:scaleX(var(--gv-coordinate-fit))!important}'
    new_axis_css = '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-axis{position:relative!important;z-index:1!important;display:grid!important;grid-template-columns:2.01em .279em 2.68em!important;align-items:center!important;width:4.969em!important;min-width:4.969em!important;max-width:4.969em!important;overflow:hidden!important;font-family:"GV Coordinate Digits",sans-serif!important;font-variant-numeric:normal!important;font-feature-settings:normal!important;letter-spacing:0!important;white-space:nowrap!important;transform:none!important}\n#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-integer{grid-column:1!important;display:block!important;min-width:0!important;text-align:right!important;white-space:nowrap!important}\n#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-decimal{grid-column:2!important;display:block!important;width:.279em!important;text-align:center!important;white-space:nowrap!important}\n#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-fraction{grid-column:3!important;display:block!important;width:2.68em!important;text-align:left!important;white-space:nowrap!important}'
    text = replace_once(text, old_axis_css, new_axis_css, "coordinate axis CSS")

    text = replace_once(
        text,
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-longitude{grid-column:2!important;justify-self:stretch!important;text-align:right!important;transform-origin:right center!important;box-sizing:border-box!important}',
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-longitude{grid-column:2!important;justify-self:end!important;text-align:right!important;transform-origin:right center!important;box-sizing:border-box!important}',
        "longitude alignment CSS",
    )
    text = replace_once(
        text,
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-latitude{grid-column:6!important;justify-self:stretch!important;text-align:left!important;transform-origin:left center!important;box-sizing:border-box!important}',
        '#aladin-cosmic-command-test .gv-coordinate-display .gv-coordinate-latitude{grid-column:6!important;justify-self:start!important;text-align:left!important;transform-origin:left center!important;box-sizing:border-box!important}',
        "latitude alignment CSS",
    )

    old_fit = '            function fitCoordinatePair(display){const longitude=display?.querySelector(".gv-coordinate-longitude"),latitude=display?.querySelector(".gv-coordinate-latitude");if(!longitude||!latitude)return;display.style.setProperty("--gv-coordinate-fit","1");requestAnimationFrame(()=>{const available=Math.max(1,Math.min(longitude.clientWidth,latitude.clientWidth)),needed=Math.max(1,longitude.scrollWidth,latitude.scrollWidth),fit=Math.min(1,available/needed);display.style.setProperty("--gv-coordinate-fit",String(fit))})}\n'
    text = replace_once(text, old_fit, "", "value-driven fitting function")

    old_render = '            function renderCoordinateGlyphs(container,value,digitCells){const text=String(value);if(container.dataset.gvCoordinateValue===text)return false;container.dataset.gvCoordinateValue=text;if(digitCells){container.textContent=text;return true}const fragment=document.createDocumentFragment();for(let index=0;index<text.length;index++){const character=text[index],glyph=document.createElement("span");glyph.className="gv-coordinate-glyph";if(text==="ICRSD"&&index===text.length-1)glyph.classList.add("gv-coordinate-frame-small-d");glyph.textContent=character;fragment.appendChild(glyph)}container.replaceChildren(fragment);return true}\n'
    new_render = '            function renderCoordinateGlyphs(container,value){const text=String(value);if(container.dataset.gvCoordinateValue===text)return false;container.dataset.gvCoordinateValue=text;const fragment=document.createDocumentFragment();for(let index=0;index<text.length;index++){const character=text[index],glyph=document.createElement("span");glyph.className="gv-coordinate-glyph";if(text==="ICRSD"&&index===text.length-1)glyph.classList.add("gv-coordinate-frame-small-d");glyph.textContent=character;fragment.appendChild(glyph)}container.replaceChildren(fragment);return true}\n            function renderFixedCoordinate(container,value){const text=String(value),match=text.match(/^([+-]?\\d+)\\.(\\d{4})$/);if(!match)return false;if(container.dataset.gvCoordinateValue===text)return false;container.dataset.gvCoordinateValue=text;let integer=container.querySelector(".gv-coordinate-integer"),decimal=container.querySelector(".gv-coordinate-decimal"),fraction=container.querySelector(".gv-coordinate-fraction");if(!integer||!decimal||!fraction){integer=document.createElement("span");integer.className="gv-coordinate-integer";decimal=document.createElement("span");decimal.className="gv-coordinate-decimal";fraction=document.createElement("span");fraction.className="gv-coordinate-fraction";container.replaceChildren(integer,decimal,fraction)}integer.textContent=match[1];decimal.textContent=".";fraction.textContent=match[2];return true}\n'
    text = replace_once(text, old_render, new_render, "coordinate rendering function")

    old_format_tail = 'const changed=renderCoordinateGlyphs(framePart,frame,false)|renderCoordinateGlyphs(longitudePart,values[0],true)|renderCoordinateGlyphs(latitudePart,values[1],true);if(changed){markCoordinateMovement(display);fitCoordinatePair(display)}}'
    new_format_tail = 'const changed=renderCoordinateGlyphs(framePart,frame)|renderFixedCoordinate(longitudePart,values[0])|renderFixedCoordinate(latitudePart,values[1]);if(changed)markCoordinateMovement(display)}'
    text = replace_once(text, old_format_tail, new_format_tail, "coordinate update tail")

    old_resize = ';window.addEventListener("resize",()=>{const display=findCoordinateBox()?.querySelector(".gv-coordinate-display");if(display)fitCoordinatePair(display)});'
    text = replace_once(text, old_resize, ';', "coordinate resize fitting listener")

    text = replace_once(text, 'versionLabel.textContent="V-7I"', 'versionLabel.textContent="V-7J"', "version label")
    text = replace_once(text, '# GV-beta-0007I staged', '# GV-beta-0007J staged', "staged marker")

    forbidden = [
        "GV-Coordinate-Digits-0002.otf?v=6Z-coordinate-digits-0002",
        "available/needed",
        "fitCoordinatePair",
        'versionLabel.textContent="V-7I"',
    ]
    for token in forbidden:
        if token in text:
            raise RuntimeError(f"Forbidden inherited token remains in 7J: {token}")

    if text == source:
        raise RuntimeError("Viewer 7J generation produced no changes")

    OUTPUT_VIEWER.write_text(text, encoding="utf-8")
    print(f"generated_viewer={OUTPUT_VIEWER}")
    print(f"viewer_characters={len(text)}")


def main():
    if not SOURCE_FONT.is_file():
        raise FileNotFoundError(f"Missing exact source font: {SOURCE_FONT}")

    if OUTPUT_FONT.exists():
        verify_font_0003()
    else:
        build_font_0003()
        verify_font_0003()

    generate_viewer_7j()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
