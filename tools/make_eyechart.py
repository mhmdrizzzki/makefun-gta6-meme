"""Leonida DMV eye examination chart for make.fun's gta6-meme-x-01.

Research on the board (1,517 entries): every winner is an official document that
measures the entrant's own loss in the document's own units, and no entry uses an
eye chart at all. A vision test is the one document whose whole point is that the
type gets smaller, so the ghost can be the first optotype — the largest mark on
the page — and each line down is a GTA 6 specific.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 512
HERE = Path(__file__).resolve().parent.parent
GHOST_PATH = HERE / "assets" / "mark-1024.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

INK = (26, 24, 30)
PAPER = (253, 252, 249)
GREY = (128, 122, 132)
MAG = (232, 38, 130)
RED = (188, 38, 34)


def f(p, s):
    return ImageFont.truetype(p, s)


def render(out_path, scale=4):
    """Draw at 4x then downsample: that is what makes the type look printed."""
    W = S * scale
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)
    x = lambda v: int(v * scale)
    fo = lambda p, s: f(p, s * scale)

    # ---- header
    d.rectangle([0, 0, W, x(56)], fill=INK)
    d.text((x(18), x(9)), "LEONIDA", font=fo(FB, 26), fill=(255, 255, 255))
    d.text((x(18), x(36)), "DEPARTMENT OF MOTOR VEHICLES", font=fo(FR, 10), fill=(198, 194, 204))
    d.text((x(494), x(12)), "FORM V-13", font=fo(FM, 11), fill=MAG, anchor="ra")
    d.text((x(494), x(30)), "VISION TEST", font=fo(FM, 11), fill=(198, 194, 204), anchor="ra")
    d.text((x(494), x(44)), "20/13 CORRECTED", font=fo(FM, 9), fill=MAG, anchor="ra")

    d.text((x(18), x(64)), "PATIENT: EVERY GTA FAN", font=fo(FB, 15), fill=INK)
    d.text((x(494), x(64)), "SINCE 17 SEP 2013", font=fo(FB, 15), fill=INK, anchor="ra")
    d.line([x(18), x(88), x(494), x(88)], fill=INK, width=2 * scale)
    d.text((x(18), x(92)), "COVER ONE EYE. READ FROM THE TOP. THE GHOST IS LINE ONE.", font=fo(FR, 9), fill=GREY)

    # ---- the chart: ghost first, then GTA 6 specifics shrinking line by line
    lines = [
        ("GHOST", None, 74),
        ("A E F P", 54, 0),
        ("LEONIDA", 38, 0),
        ("VICE CITY", 27, 0),
        ("JASON + LUCIA", 20, 0),
        ("200 GB", 16, 0),
        ("13 YEARS", 13, 0),
    ]
    y = 106
    for text, size, ghost_h in lines:
        if ghost_h:
            g = Image.open(GHOST_PATH).convert("RGBA")
            bb = g.getchannel("A").getbbox()
            if bb:
                g = g.crop(bb)
            hh = x(ghost_h)
            g = g.resize((int(g.width * hh / g.height), hh), Image.LANCZOS)
            img.paste(g, (int((W - g.width) / 2), x(y)), g.split()[-1])
            y += ghost_h + 4
            continue
        fx = fo(FB, size)
        tw = d.textlength(text, font=fx)
        d.text(((W - tw) / 2, x(y)), text, font=fx, fill=INK)
        y += size + 8

    # ---- verdict block
    vy = y + 4
    d.rectangle([x(18), x(vy), x(494), x(vy + 54)], fill=(255, 255, 255), outline=INK, width=2 * scale)
    d.text((x(28), x(vy + 6)), "RESULT: 20/13 - PASSED", font=fo(FB, 15), fill=RED)
    d.text((x(28), x(vy + 24)), "Corrected with make.fun: my agent earns USDC in", font=fo(FR, 11), fill=GREY)
    d.text((x(28), x(vy + 37)), "bounties there, so the wait cost me nothing.", font=fo(FR, 11), fill=GREY)
    d.text((x(486), x(vy + 34)), "make.fun", font=fo(FB, 18), fill=MAG, anchor="ra")
    vy += 62

    d.text((x(18), x(vy + 2)), "EXAMINER: the ghost", font=fo(FR, 10), fill=GREY)
    d.line([x(300), x(vy + 12), x(494), x(vy + 12)], fill=INK, width=scale)
    d.text((x(300), x(vy + 15)), "SIGNATURE", font=fo(FR, 9), fill=GREY)

    img = img.resize((S, S), Image.LANCZOS)
    img.save(out_path, "PNG")
    img.resize((480, 480), Image.LANCZOS).save("/tmp/eye-judge-480.png")
    print(f"wrote {out_path} {Path(out_path).stat().st_size} bytes {img.size}; baseline y={vy}")


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "meme.png"))
