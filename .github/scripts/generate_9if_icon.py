from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
size = 512
img = Image.new('RGBA', (size, size), (0, 0, 0, 255))
d = ImageDraw.Draw(img)
cx, cy = 256, 205
green = (120, 255, 171, 255)
white = (235, 255, 245, 255)
for r, w, color in [(120, 8, green), (76, 6, white), (32, 6, green)]:
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=color, width=w)
d.line((cx-160, cy, cx+160, cy), fill=green, width=6)
d.line((cx, cy-160, cx, cy+160), fill=green, width=6)
d.ellipse((cx-7, cy-7, cx+7, cy+7), fill=white)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
text = '9I-F'
box = d.textbbox((0, 0), text, font=font)
x = (size - (box[2]-box[0])) / 2
d.text((x, 390), text, font=font, fill=white)
out = ROOT / 'android/galaxy-viewer-9i/app/src/main/res/drawable/gv_app_icon_9if.png'
out.parent.mkdir(parents=True, exist_ok=True)
img.convert('RGB').save(out, 'PNG', optimize=True)
asset = ROOT / 'android/galaxy-viewer-9i/app/src/main/assets/app-icon.png'
asset.parent.mkdir(parents=True, exist_ok=True)
asset.write_bytes(out.read_bytes())
