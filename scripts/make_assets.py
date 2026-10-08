"""Generate the icon set and the social preview image.

Run from the repo root: python3 -I scripts/make_assets.py
The icon is the calligraphic O from Latin Modern Math, with gold speed lines.
It needs the TeX Live Latin Modern fonts and the DejaVu fonts.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
MATH_FONT = "/usr/share/texmf/fonts/opentype/public/lm-math/latinmodern-math.otf"
DARK = (18, 18, 18)
WHITE = (255, 255, 255)
GOLD = (255, 196, 0)
BLUE = (11, 92, 173)
INK = (27, 27, 27)
PAPER = (253, 253, 252)

S = 2048  # Draw at this size, and then downscale for smooth edges.
CALLIGRAPHIC_O = "\U0001D4AA"
# Speed lines as (vertical offset, left x, right x), in fractions of the tile.
LINES = [(-0.14, 0.12, 0.33), (0.0, 0.07, 0.36), (0.14, 0.12, 0.33)]
LINE_THICKNESS = 110


def draw_icon(size: int, rounded: bool = True) -> Image.Image:
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22 if rounded else 0, fill=DARK)
    font = ImageFont.truetype(MATH_FONT, 1800)
    left, top, right, bottom = d.textbbox((0, 0), CALLIGRAPHIC_O, font=font)
    cx, cy = 0.60 * S, 0.5 * S
    d.text((cx - (left + right) / 2, cy - (top + bottom) / 2), CALLIGRAPHIC_O, font=font, fill=WHITE)
    t = LINE_THICKNESS
    for dy, x0, x1 in LINES:
        y = S * (0.5 + dy)
        d.rounded_rectangle([x0 * S, y - t / 2, x1 * S, y + t / 2], radius=t / 2, fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)


def write_og() -> None:
    w, h = 1200, 630
    im = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(im)
    icon = draw_icon(240)
    im.paste(icon, (90, (h - 240) // 2), icon)
    serif = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 66)
    sans = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    x = 390
    d.text((x, 190), "The era of Big O", font=serif, fill=INK)
    d.text((x, 275), "speedrunning?", font=serif, fill=INK)
    d.text((x, 385), "bigOspeedrun.com", font=sans, fill=BLUE)
    d.rectangle([0, h - 12, w, h], fill=GOLD)
    im.save(ROOT / "og.png", optimize=True)


def main() -> None:
    draw_icon(256).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    draw_icon(32).save(ROOT / "favicon-32.png", optimize=True)
    # Apple applies its own corner mask, so the touch icon is square.
    draw_icon(180, rounded=False).convert("RGB").save(ROOT / "apple-touch-icon.png", optimize=True)
    draw_icon(192).save(ROOT / "icon-192.png", optimize=True)
    draw_icon(512).save(ROOT / "icon-512.png", optimize=True)
    write_og()


if __name__ == "__main__":
    main()
