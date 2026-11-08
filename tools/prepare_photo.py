#!/usr/bin/env python3
"""
Turn a photo into the two image assets the profile needs:

  assets/avatar.jpg    round avatar shown in the hero banner
  assets/portrait.json dot-matrix portrait shown in the About section

Usage:
    python tools/prepare_photo.py path/to/photo.jpg
    python tools/prepare_photo.py path/to/photo.jpg --cx 500 --cy 640 --size 740

--cx/--cy/--size choose the square crop (centre x, centre y, side) in the
ORIGINAL photo's pixels, so you can aim it at your face. Needs: pip install pillow
After running this, run:  python build.py
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageEnhance, ImageOps
except ImportError:
    sys.exit("This tool needs Pillow:  pip install pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def square(im, cx, cy, size):
    half = size // 2
    left = max(0, min(im.width - size, cx - half))
    top = max(0, min(im.height - size, cy - half))
    return im.crop((left, top, left + size, top + size))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("--cx", type=int)
    ap.add_argument("--cy", type=int)
    ap.add_argument("--size", type=int)
    ap.add_argument("--cols", type=int, default=72, help="portrait grid size (dots per side)")
    a = ap.parse_args()

    im = ImageOps.exif_transpose(Image.open(a.photo)).convert("RGB")
    w, h = im.size
    size = a.size or int(min(w, h) * 0.68)
    cx = a.cx if a.cx is not None else w // 2
    cy = a.cy if a.cy is not None else int(h * 0.42)
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)

    # 1) avatar
    avatar = square(im, cx, cy, size).resize((360, 360), Image.LANCZOS)
    avatar.save(os.path.join(ROOT, "assets", "avatar.jpg"), quality=84, optimize=True)

    # 2) dot-matrix portrait: a grid of coloured cells, build.py draws each as a dot
    wide = square(im, cx, cy + int(size * 0.04), int(size * 1.12))
    wide = ImageEnhance.Contrast(ImageEnhance.Color(wide).enhance(1.25)).enhance(1.2)
    n = a.cols
    small = wide.resize((n, n), Image.LANCZOS)
    px = small.load()
    hexes = ["%02x%02x%02x" % px[x, y] for y in range(n) for x in range(n)]
    with open(os.path.join(ROOT, "assets", "portrait.json"), "w") as f:
        json.dump({"cols": n, "rows": n, "hex": hexes}, f, separators=(",", ":"))
    print(f"ok: assets/avatar.jpg + assets/portrait.json ({n}x{n} dots)  -> now run: python build.py")


if __name__ == "__main__":
    main()
