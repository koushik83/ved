"""Turn any picture into a card image for the home page and the tool pages:
a 1024x1024 WebP on the site's cream background, the figure centred.

    python tools/make_card_image.py <input image> <name>            e.g. shiv, durga
    python tools/make_card_image.py <input image> <name> --duotone  recolour in saffron on cream

Without --duotone the picture keeps its own colours (for generated saffron line
art). The result is written to images/<name>.webp; a transparent PNG is
flattened onto the cream, an opaque one is padded with it.
"""
import pathlib
import sys

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
CREAM = (253, 244, 231)
ORANGE = (211, 84, 0)
DARK = (120, 40, 0)


def ramp(v):
    if v < 0.55:
        t, a, b = v / 0.55, DARK, ORANGE
    else:
        t, a, b = (v - 0.55) / 0.45, ORANGE, CREAM
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main(src, name, duotone):
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, CREAM + (255,))
        im = Image.alpha_composite(bg, im).convert("RGB")
    else:
        im = im.convert("RGB")
    side = max(im.size)
    canvas = Image.new("RGB", (side, side), CREAM)
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    canvas = canvas.resize((1024, 1024), Image.LANCZOS)
    if duotone:
        g = ImageOps.autocontrast(canvas.convert("L"), cutoff=1)
        lut = [ramp(i / 255.0) for i in range(256)]
        px = g.load()
        out = Image.new("RGB", g.size)
        op = out.load()
        for y in range(g.height):
            for x in range(g.width):
                op[x, y] = lut[px[x, y]]
        canvas = out
    dest = ROOT / "images" / f"{name}.webp"
    canvas.save(dest, quality=85, method=6)
    print("wrote", dest.relative_to(ROOT), dest.stat().st_size, "bytes")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], "--duotone" in sys.argv)
