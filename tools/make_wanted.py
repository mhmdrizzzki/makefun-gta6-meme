"""A Leonida PD wanted poster for make.fun's ghost — the top-10 attempt.

The fifth-star wanted meter is the one piece of GTA interface every player reads
instantly, no entry in the top twelve uses it, and it lets the ghost be the
subject of the picture instead of its letterhead.
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

INK = (16, 14, 18)
CREAM = (238, 228, 204)
MAG = (232, 38, 130)
RED = (186, 34, 32)
GOLD = (226, 176, 58)


def f(p, s):
    return ImageFont.truetype(p, s)


def fit(d, text, p, size, max_w, floor=10):
    while size > floor:
        fo = f(p, size)
        if d.textlength(text, font=fo) <= max_w:
            return fo
        size -= 1
    return f(p, floor)


def star(d, cx, cy, r, fill, outline=None, rot=-90):
    import math
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=outline, width=2)


def main(out_path):
    img = Image.new("RGB", (W, H), (36, 26, 22))
    d = ImageDraw.Draw(img)
    for i in range(H):                                   # aged paper vignette
        t = abs(i - H / 2) / (H / 2)
        c = tuple(int(v * (1 - 0.45 * t)) for v in (58, 42, 34))
        d.line([(0, i), (W, i)], fill=c)

    P = (12, 12, 500, 500)
    poster = Image.new("RGB", (P[2] - P[0], P[3] - P[1]), CREAM)
    p = ImageDraw.Draw(poster)
    pw, ph = poster.size

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([P[0] + 6, P[1] + 10, P[2] + 6, P[3] + 10], 6, fill=(0, 0, 0, 190))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(8))).convert("RGB"), (0, 0))

    # ---- five wanted stars, the GTA read at a glance
    for i in range(5):
        star(p, 122 + i * 66, 34, 22, GOLD, (120, 80, 18))

    p.text((pw // 2, 96), "WANTED", font=f(FB, 54), fill=RED, anchor="ma")
    p.text((pw // 2, 156), "LEONIDA POLICE DEPARTMENT", font=f(FB, 14), fill=INK, anchor="ma")

    # ---- mugshot: height chart behind the ghost, booking placard under it
    PHH = 162
    photo = Image.new("RGB", (214, PHH), (206, 198, 180))
    pd = ImageDraw.Draw(photo)
    for x in range(0, 214, 22):
        pd.line([(x, 0), (x, PHH)], fill=(178, 170, 152), width=1)
    for yy in range(0, PHH, 22):
        pd.line([(0, yy), (214, yy)], fill=(178, 170, 152), width=1)
    g = Image.open(GHOST_PATH).convert("RGBA")
    bb = g.getchannel("A").getbbox()
    if bb:
        g = g.crop(bb)
    gw = 150
    gh = int(g.height * gw / g.width)
    g = g.resize((gw, gh), Image.LANCZOS)
    photo.paste(g, ((214 - gw) // 2, PHH - gh - 34), g.split()[-1])
    pd.rectangle([0, PHH - 34, 214, PHH], fill=(232, 226, 210))
    pd.text((107, PHH - 30), "make.fun", font=f(FB, 20), fill=INK, anchor="ma")
    pd.text((107, PHH - 11), "BOOKED 19 NOV 2026", font=f(FM, 9), fill=(90, 84, 78), anchor="ma")
    poster.paste(photo, ((pw - 214) // 2, 182))
    p.rectangle([(pw - 214) // 2, 182, (pw - 214) // 2 + 214, 182 + PHH], outline=INK, width=3)

    # ---- charges: the jokes live here
    y = 352
    p.text((30, y), "CHARGED WITH", font=f(FB, 13), fill=(120, 100, 84))
    y += 17
    charges = [
        "PAYING FINES FOR CRIMES IT DIDN'T COMMIT",
        "WAITING THIRTEEN YEARS WITHOUT COMPLAINING",
        "200 GB DOWNLOAD ON A WORK LAPTOP",
        "BOUNTY HUNTING UNDER A HUMAN'S NAME",
    ]
    usable = pw - 30 - 48 - 4
    for c in charges:
        p.rectangle([30, y + 4, 38, y + 12], fill=MAG)
        p.text((48, y), c, font=fit(p, c, FB, 14, usable, floor=13), fill=INK)
        y += 20

    # ---- the reward line: make.fun pays, in USDC
    p.rectangle([0, ph - 60, pw, ph], fill=INK)
    p.text((26, ph - 50), "REWARD", font=f(FB, 12), fill=GOLD)
    rt = "PAID IN USDC BY make.fun BOUNTIES"
    p.text((26, ph - 33), rt, font=fit(p, rt, FB, 17, pw - 26 - 128, floor=12), fill=(255, 255, 255))
    st = Image.new("RGBA", (110, 44), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([2, 2, 106, 40], 6, outline=MAG + (245,), width=4)
    sd.text((54, 8), "AGENT", font=f(FB, 15), fill=MAG + (245,), anchor="ma")
    sd.text((54, 23), "PAID", font=f(FB, 15), fill=MAG + (245,), anchor="ma")
    st = st.rotate(-12, expand=True, resample=Image.BICUBIC)
    poster.paste(st, (pw - 132, ph - 50), st)

    img.paste(poster, (P[0], P[1]))
    img.save(out_path, "PNG")
    img.resize((480, 480), Image.LANCZOS).save("/tmp/wanted-judge-480.png")
    print(f"wrote {out_path} {Path(out_path).stat().st_size} bytes {img.size}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "meme.png"))
