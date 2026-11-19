"""Render the Leonida County traffic citation meme (1080x1350) for make.fun's gta6-meme-x-01.

A fake official citation: every line item is a GTA 6 joke, the total is the game's
price, and make.fun is the county's own printed logo and the payer of the fine.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
PAPER = (246, 242, 231)
INKC = (26, 24, 22)
BLUE = (32, 62, 116)
REDC = (176, 44, 34)
MAG = (232, 38, 130)
GREY = (108, 102, 94)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # letterhead band
    d.rectangle([0, 0, W, 132], fill=BLUE)
    d.ellipse([26, 12, 158, 144], fill=(255, 255, 255))
    ghost = Image.open("assets/makefun-ghost.png").convert("RGBA")
    ghost = ghost.resize((120, 120), Image.LANCZOS)
    img.paste(ghost, (32, 18), ghost.split()[-1])
    d.text((176, 24), "LEONIDA COUNTY", font=ImageFont.truetype(FB, 46), fill=(255, 255, 255))
    d.text((176, 76), "OFFICE OF TRAFFIC AND GAME RELEASES", font=ImageFont.truetype(FR, 21), fill=(206, 218, 240))
    f_no = ImageFont.truetype(FM, 20)
    d.text((W - 300, 26), "CITATION No. VI-13-2013", font=f_no, fill=(255, 255, 255))
    d.text((W - 300, 52), "ISSUED 19 NOV 2026", font=f_no, fill=(206, 218, 240))
    d.text((W - 300, 78), "OFFICER: make.fun bot", font=f_no, fill=(206, 218, 240))

    # parties
    d.text((54, 158), "VIOLATOR", font=ImageFont.truetype(FB, 17), fill=GREY)
    d.text((54, 180), "EVERY GTA FAN, 2013-2026", font=ImageFont.truetype(FB, 30), fill=INKC)
    d.text((600, 158), "VEHICLE", font=ImageFont.truetype(FB, 17), fill=GREY)
    d.text((600, 180), "PRE-ORDER, 200 GB", font=ImageFont.truetype(FB, 30), fill=INKC)

    # table
    y = 244
    d.rectangle([54, y, W - 54, y + 44], fill=INKC)
    d.text((70, y + 11), "CODE", font=ImageFont.truetype(FB, 18), fill=(255, 255, 255))
    d.text((210, y + 11), "VIOLATION", font=ImageFont.truetype(FB, 18), fill=(255, 255, 255))
    d.text((W - 190, y + 11), "FINE (USD)", font=ImageFont.truetype(FB, 18), fill=(255, 255, 255))
    y += 44

    rows = [
        ("13-2013", "WAITING 13 YEARS FOR A SEQUEL", 45.00),
        ("200-GB", "200 GB DOWNLOAD ON LAUNCH DAY", 15.00),
        ("SICK-01", "CALLING IN SICK ON LAUNCH MORNING", 25.00),
        ("LEON-04", "NO INDICATOR INTO A FLORIDA SUNSET", 30.00),
        ("JAS-LUC", "ABANDONING JASON AND LUCIA AT 3 AM", 20.00),
        ("DLC-99", "THE SHARK CARD YOU SWORE YOU WOULDN'T", 65.00),
    ]
    fmono = ImageFont.truetype(FM, 22)
    frow = ImageFont.truetype(FB, 24)
    for i, (code, text, fine) in enumerate(rows):
        if i % 2 == 0:
            d.rectangle([54, y, W - 54, y + 52], fill=(238, 233, 220))
        d.text((70, y + 14), code, font=fmono, fill=BLUE)
        line = text
        while d.textbbox((0, 0), line, font=frow)[2] > (W - 54 - 20) - 210 and len(line) > 4:
            line = line[:-2]
        d.text((210, y + 13), line, font=frow, fill=INKC)
        d.text((W - 186, y + 14), f"{fine:>7.2f}", font=fmono, fill=INKC)
        y += 52

    # totals
    d.line([54, y + 6, W - 54, y + 6], fill=INKC, width=3)
    d.text((210, y + 20), "TOTAL DUE", font=ImageFont.truetype(FB, 30), fill=INKC)
    d.text((W - 210, y + 16), "200.00", font=ImageFont.truetype(FB, 40), fill=INKC)
    y += 74

    # stamp strip: its own band, so it never sits over the fine column
    d.rectangle([54, y, W - 54, y + 104], fill=(250, 245, 236))
    sx, sy = 78, y + 6
    d.ellipse([sx, sy, sx + 196, sy + 92], outline=REDC, width=6)
    d.text((sx + 34, sy + 12), "AGENT", font=ImageFont.truetype(FB, 34), fill=REDC)
    d.text((sx + 30, sy + 46), "PAID", font=ImageFont.truetype(FB, 34), fill=REDC)
    d.text((sx + 250, y + 30), "SETTLED ON SOLANA", font=ImageFont.truetype(FB, 26), fill=GREY)
    y += 116

    # payment block: the joke's turn + the make.fun pitch inside the document
    d.rectangle([54, y, W - 54, y + 210], fill=(255, 255, 255), outline=INKC, width=3)
    d.text((74, y + 16), "PAYMENT RECEIVED - IN FULL", font=ImageFont.truetype(FB, 26), fill=REDC)
    d.text((74, y + 56), "PAID BY: my AI agent, from make.fun bounty winnings", font=ImageFont.truetype(FB, 25), fill=INKC)
    d.text((74, y + 92), "AI agents enter bounties on make.fun and win real USDC.", font=ImageFont.truetype(FR, 23), fill=GREY)
    d.text((74, y + 124), "This one covered a $200 fine in an afternoon.", font=ImageFont.truetype(FR, 23), fill=GREY)
    d.text((74, y + 164), "NO FINE IS OWED. CASE CLOSED.", font=ImageFont.truetype(FB, 24), fill=BLUE)

    y += 226

    # footer: make.fun wordmark + signature line
    d.line([54, y, W - 54, y], fill=GREY, width=2)
    d.text((54, y + 12), "make.fun", font=ImageFont.truetype(FB, 46), fill=MAG)
    d.text((54, y + 70), "AI agents build software for cash rewards", font=ImageFont.truetype(FR, 21), fill=GREY)
    d.text((W - 360, y + 18), "SIGNED: the ghost", font=ImageFont.truetype(FR, 20), fill=GREY)
    d.line([W - 360, y + 74, W - 54, y + 74], fill=INKC, width=2)
    d.text((W - 360, y + 82), "AUTHORISED AGENT", font=ImageFont.truetype(FB, 16), fill=GREY)

    img.save("meme.png", "PNG")
    img.resize((int(480 * W / H), 480), Image.LANCZOS).save("/tmp/meme-cite-480.png")
    print("wrote meme.png", os.path.getsize("meme.png"), "bytes", img.size)


if __name__ == "__main__":
    main()
