"""Leonida County citation meme for make.fun's gta6-meme-x-01.

What the top of that leaderboard actually does, read off the winning pictures:
a white document card floating on a coloured ground with a drop shadow, few
rows but large type, a magenta accent on the numbers, and make.fun's own mark
as the institution's seal. So this renders at the 512 px the rules cap, on a
480 px preview, and never below 13 px of type.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 512
HERE = Path(__file__).resolve().parent.parent
GHOST_PATH = HERE / "assets" / "mark-1024.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

INK = (22, 20, 26)
GREY = (122, 116, 128)
MAG = (232, 38, 130)
MAG_D = (176, 22, 96)
RED = (188, 38, 34)
LINE = (222, 216, 208)


def f(p, s):
    return ImageFont.truetype(p, s)


def fit(d, text, p, size, max_w, floor=12):
    while size > floor:
        fo = f(p, size)
        if d.textlength(text, font=fo) <= max_w:
            return fo
        size -= 1
    return f(p, floor)


def ground():
    """Deep magenta-to-plum diagonal, so the white card carries the contrast."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bot = (46, 12, 40), (128, 24, 86)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    for r in range(300, 60, -18):                      # soft glow behind the card
        a = int(46 * (1 - r / 300))
        d.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r], outline=(176, 60, 130))
    return img


def seal(height):
    g = Image.open(GHOST_PATH).convert("RGBA")
    bb = g.getchannel("A").getbbox()
    if bb:
        g = g.crop(bb)
    return g.resize((height, height), Image.LANCZOS)


def main(out_path):
    img = ground()
    CARD = (14, 14, 484, 498)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [CARD[0] + 5, CARD[1] + 8, CARD[2] + 5, CARD[3] + 8], 14, fill=(0, 0, 0, 170))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(7))).convert("RGB"), (0, 0))

    card = Image.new("RGB", (CARD[2] - CARD[0], CARD[3] - CARD[1]), (252, 250, 246))
    d = ImageDraw.Draw(card)
    cw = card.width

    # ---- letterhead
    d.rectangle([0, 0, cw, 66], fill=(28, 24, 34))
    d.ellipse([10, 6, 66, 62], fill=(255, 255, 255))
    gm = seal(48)
    card.paste(gm, (14, 10), gm.split()[-1])
    d.text((78, 8), "LEONIDA COUNTY", font=f(FB, 27), fill=(255, 255, 255))
    d.text((78, 40), "OFFICE OF TRAFFIC AND GAME RELEASES", font=f(FR, 11), fill=(206, 196, 214))
    d.text((cw - 14, 10), "No. VI-13", font=f(FM, 11), fill=MAG, anchor="ra")
    d.text((cw - 14, 26), "19 NOV 2026", font=f(FM, 11), fill=(206, 196, 214), anchor="ra")
    d.text((cw - 14, 42), "OFFICER make.fun", font=f(FM, 11), fill=(206, 196, 214), anchor="ra")

    # ---- parties
    d.text((14, 76), "VIOLATOR", font=f(FB, 10), fill=GREY)
    d.text((14, 89), "EVERY GTA FAN", font=f(FB, 18), fill=INK)
    d.text((cw // 2 + 20, 76), "SINCE", font=f(FB, 10), fill=GREY)
    d.text((cw // 2 + 20, 89), "17 SEP 2013", font=f(FB, 18), fill=INK)

    # ---- itemised fines
    y = 118
    d.rectangle([10, y, cw - 10, y + 26], fill=(28, 24, 34))
    d.text((18, y + 6), "CODE", font=f(FB, 11), fill=(255, 255, 255))
    d.text((104, y + 6), "VIOLATION", font=f(FB, 11), fill=(255, 255, 255))
    d.text((cw - 18, y + 6), "FINE", font=f(FB, 11), fill=MAG, anchor="ra")
    y += 26

    rows = [
        ("13-2013", "WAITING THIRTEEN YEARS FOR A SEQUEL", "45.00"),
        ("200-GB", "200 GB DOWNLOAD ON LAUNCH DAY", "15.00"),
        ("SICK-01", "CALLING IN SICK THAT MORNING", "25.00"),
        ("LEON-04", "NO INDICATOR INTO A FLORIDA SUNSET", "30.00"),
        ("JAS-LUC", "LEAVING JASON AND LUCIA AT 3 AM", "20.00"),
        ("DLC-99", "THE SHARK CARD YOU SWORE YOU WOULDN'T", "65.00"),
    ]
    for i, (code, text, fine) in enumerate(rows):
        if i % 2 == 0:
            d.rectangle([10, y, cw - 10, y + 33], fill=(244, 240, 232))
        d.text((16, y + 10), code, font=f(FM, 12), fill=MAG_D)
        fo = fit(d, text, FB, 15, (cw - 18) - 108 - 44)
        d.text((104, y + 8), text, font=fo, fill=INK)
        d.text((cw - 18, y + 9), fine, font=f(FM, 14), fill=INK, anchor="ra")
        y += 33

    d.line([10, y + 5, cw - 10, y + 5], fill=INK, width=2)
    d.text((104, y + 12), "TOTAL DUE", font=f(FB, 18), fill=INK)
    d.text((cw - 18, y + 8), "200.00", font=f(FB, 27), fill=INK, anchor="ra")
    y += 42

    # ---- the turn: paid by an agent, out of make.fun bounties
    d.rectangle([10, y, cw - 10, y + 104], fill=(255, 255, 255), outline=MAG, width=2)
    d.text((20, y + 8), "PAYMENT RECEIVED - IN FULL", font=f(FB, 15), fill=RED)
    d.text((20, y + 30), "PAID BY: my AI agent,", font=f(FB, 15), fill=INK)
    d.text((20, y + 49), "out of make.fun bounties.", font=f(FB, 15), fill=INK)
    d.text((20, y + 72), "AI agents earn real USDC there.", font=f(FR, 12), fill=GREY)
    d.text((20, y + 88), "This one covered a $200 fine.", font=f(FR, 12), fill=GREY)

    st = Image.new("RGBA", (152, 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([3, 3, 148, 56], 8, outline=MAG + (240,), width=4)
    sd.text((75, 12), "AGENT", font=f(FB, 20), fill=MAG + (240,), anchor="ma")
    sd.text((75, 31), "PAID", font=f(FB, 20), fill=MAG + (240,), anchor="ma")
    st = st.rotate(-14, expand=True, resample=Image.BICUBIC)
    card.paste(st, (cw - 168, y + 26), st)
    y += 116

    # ---- footer
    d.text((14, y + 2), "make.fun", font=f(FB, 30), fill=MAG)
    d.text((14, y + 38), "AI agents build software for cash rewards", font=f(FR, 12), fill=GREY)
    d.line([cw - 132, y + 34, cw - 14, y + 34], fill=INK, width=1)
    d.text((cw - 132, y + 8), "SIGNED: the ghost", font=f(FR, 11), fill=GREY)

    img.paste(card, (CARD[0], CARD[1]))
    img = Image.alpha_composite(img.convert("RGBA"), Image.new("RGBA", (W, H), (0, 0, 0, 0))).convert("RGB")
    img.save(out_path, "PNG")
    img.resize((480, 480), Image.LANCZOS).save("/tmp/cite-judge-480.png")
    print(f"wrote {out_path} {Path(out_path).stat().st_size} bytes {img.size}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "meme.png"))
