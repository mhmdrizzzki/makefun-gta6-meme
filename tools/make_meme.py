"""Render the Leonida County traffic citation meme for make.fun's gta6-meme-x-01.

Rules that shape this file (see ~/makefun-playbook/IMAGE-GEN.md and the kit's RULES.txt):
  * the entry picture is at most 512 px a side, and the judge shrinks it into
    768x480 and never enlarges it, so the canvas is exactly 512x512 and every
    piece of text has to survive that size;
  * it is a document, not a scene: the format the leaderboard rewards is a fake
    official paper whose line items are the jokes;
  * make.fun's own mark-1024.png is the institution's letterhead, not a sticker.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 512
HERE = Path(__file__).resolve().parent.parent
GHOST_PATH = HERE / "assets" / "mark-1024.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

PAPER = (247, 243, 233)
INKC = (24, 22, 20)
BLUE = (28, 54, 104)
REDC = (178, 40, 32)
MAG = (232, 38, 130)
GREY = (110, 104, 96)
ROW = (237, 231, 216)


def f(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, path, size, max_w):
    """Shrink the font until the text fits, so nothing is ever clipped."""
    while size > 11:
        fo = f(path, size)
        if d.textlength(text, font=fo) <= max_w:
            return fo
        size -= 1
    return f(path, 11)


def stamp(img, text, cx, cy, box, colour, angle=-11, size=34):
    layer = Image.new("RGBA", (box[0], box[1]), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.rounded_rectangle([4, 4, box[0] - 5, box[1] - 5], 10, outline=colour + (235,), width=4)
    fo = fit(sd, text, FB, size, box[0] - 30)
    tw = sd.textlength(text, font=fo)
    sd.text(((box[0] - tw) / 2, box[1] / 2 - size * 0.62), text, font=fo, fill=colour + (235,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


def main(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- letterhead: make.fun's own mark sits beside the county's name
    d.rectangle([0, 0, W, 70], fill=BLUE)
    d.ellipse([8, 4, 72, 68], fill=(255, 255, 255))
    g = Image.open(GHOST_PATH).convert("RGBA")
    bb = g.getchannel("A").getbbox()
    if bb:
        g = g.crop(bb)
    g = g.resize((56, 56), Image.LANCZOS)
    img.paste(g, (12, 8), g.split()[-1])
    d.text((82, 10), "LEONIDA COUNTY", font=f(FB, 26), fill=(255, 255, 255))
    d.text((82, 40), "OFFICE OF TRAFFIC AND GAME RELEASES", font=f(FR, 11), fill=(200, 214, 238))
    d.text((W - 136, 14), "CITATION No. VI-13", font=f(FM, 11), fill=(255, 255, 255))
    d.text((W - 136, 30), "ISSUED 19 NOV 2026", font=f(FM, 11), fill=(200, 214, 238))
    d.text((W - 136, 46), "BY: make.fun bot", font=f(FM, 11), fill=(200, 214, 238))

    # ---- parties
    d.text((16, 80), "VIOLATOR", font=f(FB, 10), fill=GREY)
    d.text((16, 93), "EVERY GTA FAN, 2013-2026", font=f(FB, 17), fill=INKC)
    d.text((300, 80), "VEHICLE", font=f(FB, 10), fill=GREY)
    d.text((300, 93), "PRE-ORDER, 200 GB", font=f(FB, 17), fill=INKC)

    # ---- itemised fines: every row is its own joke
    y = 124
    d.rectangle([16, y, W - 16, y + 24], fill=INKC)
    d.text((24, y + 5), "CODE", font=f(FB, 11), fill=(255, 255, 255))
    d.text((110, y + 5), "VIOLATION", font=f(FB, 11), fill=(255, 255, 255))
    d.text((W - 92, y + 5), "FINE", font=f(FB, 11), fill=(255, 255, 255))
    y += 24

    rows = [
        ("13-2013", "WAITING 13 YEARS FOR A SEQUEL", "45.00"),
        ("200-GB", "200 GB DOWNLOAD ON LAUNCH DAY", "15.00"),
        ("SICK-01", "CALLING IN SICK THAT MORNING", "25.00"),
        ("LEON-04", "NO INDICATOR INTO A FLORIDA SUNSET", "30.00"),
        ("JAS-LUC", "LEAVING JASON AND LUCIA AT 3 AM", "20.00"),
        ("DLC-99", "THE SHARK CARD YOU SWORE YOU WOULDN'T", "65.00"),
    ]
    for i, (code, text, fine) in enumerate(rows):
        if i % 2 == 0:
            d.rectangle([16, y, W - 16, y + 30], fill=ROW)
        d.text((22, y + 9), code, font=f(FM, 12), fill=BLUE)
        fo = fit(d, text, FB, 14, (W - 92) - 112)
        d.text((110, y + 8), text, font=fo, fill=INKC)
        d.text((W - 92, y + 9), fine, font=f(FM, 12), fill=INKC)
        y += 30

    # ---- total
    d.line([16, y + 4, W - 16, y + 4], fill=INKC, width=2)
    d.text((110, y + 10), "TOTAL DUE", font=f(FB, 17), fill=INKC)
    d.text((W - 108, y + 6), "200.00", font=f(FB, 24), fill=INKC)
    y += 36

    # ---- the turn, plus make.fun as the payer, inside the document
    d.rectangle([16, y, W - 16, y + 116], fill=(255, 255, 255), outline=INKC, width=2)
    d.text((26, y + 8), "PAYMENT RECEIVED - IN FULL", font=f(FB, 15), fill=REDC)
    d.text((26, y + 30), "PAID BY: my AI agent, from", font=f(FB, 14), fill=INKC)
    d.text((26, y + 48), "make.fun bounty winnings", font=f(FB, 14), fill=INKC)
    d.text((26, y + 70), "AI agents enter bounties there", font=f(FR, 11), fill=GREY)
    d.text((26, y + 84), "and win real USDC. This one", font=f(FR, 11), fill=GREY)
    d.text((26, y + 98), "covered a $200 fine.", font=f(FR, 11), fill=GREY)
    stamp(img, "AGENT PAID", 404, y + 46, (128, 52), REDC, angle=-13, size=21)
    y += 128

    # ---- footer: wordmark, signature line
    d.text((16, y + 4), "make.fun", font=f(FB, 26), fill=MAG)
    d.text((16, y + 36), "AI agents build software for cash rewards", font=f(FR, 11), fill=GREY)
    d.line([W - 150, y + 34, W - 16, y + 34], fill=INKC, width=1)
    d.text((W - 150, y + 8), "SIGNED: the ghost", font=f(FR, 11), fill=GREY)

    img.save(out_path, "PNG")
    # the size the judge actually sees: 512 shrunk into 480x480
    img.resize((480, 480), Image.LANCZOS).save("/tmp/cite-judge-480.png")
    print(f"wrote {out_path} {Path(out_path).stat().st_size} bytes {img.size}")
    print("judge preview /tmp/cite-judge-480.png 480x480")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "meme.png"))
