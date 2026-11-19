"""Render the Leonida DMV vision-test chart for make.fun bounty gta6-meme-x-01.

The entry is a 512x512 optotype chart. The make.fun ghost is the top line, the
biggest mark on the card, and each line below it shrinks through GTA 6 specifics
until the smallest row is the thirteen-year wait. Everything is drawn at 4x and
downsampled with LANCZOS so the small type survives the judge's 480px shrink.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = 512
SCALE = 4
ROOT = Path(__file__).resolve().parent.parent
GHOST = ROOT / "assets" / "mark-1024.png"
DEFAULT_OUT = ROOT / "meme-eyechart.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

INK = (24, 22, 28)
PAPER = (252, 251, 247)
MUTED = (124, 118, 129)
MAGENTA = (232, 40, 132)
FAIL_RED = (186, 36, 33)
HEADER_TEXT = (255, 255, 255)
HEADER_DIM = (202, 197, 208)

MARGIN = 18
RIGHT = CANVAS - MARGIN

HEADER_H = 56
PATIENT_Y = 64
RULE_Y = 88
CAPTION_Y = 92

CHART_TOP = 105
GHOST_H = 72
GHOST_GAP = 8
TEXT_GAP = 8
ROWS = [
    ("A E F P", 54),
    ("LEONIDA", 40),
    ("VICE CITY", 30),
    ("JASON + LUCIA", 22),
    ("200 GB", 17),
    ("13 YEARS", 14),
]

BOX_PAD_TOP = 8
BOX_H = 58
BOX_INNER = 10


def px(value: float) -> int:
    return int(round(value * SCALE))


def font(path: str, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, px(size))


def load_ghost(height: int) -> Image.Image:
    art = Image.open(GHOST).convert("RGBA")
    bounds = art.getchannel("A").getbbox()
    if bounds:
        art = art.crop(bounds)
    width = max(1, round(art.width * height / art.height))
    return art.resize((width, height), Image.LANCZOS)


def draw_text(draw: ImageDraw.ImageDraw, xy, text, face, color, anchor=None):
    draw.text((px(xy[0]), px(xy[1])), text, font=face, fill=color, anchor=anchor)


def draw_header(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle([0, 0, px(CANVAS), px(HEADER_H)], fill=INK)
    draw_text(draw, (MARGIN, 8), "LEONIDA", font(FONT_BOLD, 26), HEADER_TEXT)
    draw_text(draw, (MARGIN, 37), "DEPARTMENT OF MOTOR VEHICLES", font(FONT_REG, 10), HEADER_DIM)
    draw_text(draw, (RIGHT, 11), "FORM V-13", font(FONT_MONO, 11), MAGENTA, anchor="ra")
    draw_text(draw, (RIGHT, 29), "VISION TEST", font(FONT_MONO, 11), HEADER_DIM, anchor="ra")


def draw_patient(draw: ImageDraw.ImageDraw) -> None:
    draw_text(draw, (MARGIN, PATIENT_Y), "PATIENT: EVERY GTA FAN", font(FONT_BOLD, 15), INK)
    draw_text(draw, (RIGHT, PATIENT_Y), "SINCE 17 SEP 2013", font(FONT_BOLD, 15), INK, anchor="ra")
    draw.line([px(MARGIN), px(RULE_Y), px(RIGHT), px(RULE_Y)], fill=INK, width=px(0.5))
    draw_text(draw, (MARGIN, CAPTION_Y), "COVER ONE EYE. START AT THE GHOST.", font(FONT_REG, 9), MUTED)


def draw_chart(img: Image.Image, draw: ImageDraw.ImageDraw) -> float:
    cursor = CHART_TOP
    ghost = load_ghost(px(GHOST_H))
    img.paste(ghost, ((px(CANVAS) - ghost.width) // 2, px(cursor)), ghost.getchannel("A"))
    cursor += GHOST_H + GHOST_GAP

    for text, size in ROWS:
        face = font(FONT_BOLD, size)
        width = draw.textlength(text, font=face)
        draw_text(draw, ((CANVAS - width / SCALE) / 2, cursor), text, face, INK)
        cursor += size + TEXT_GAP
    return cursor


def draw_result(draw: ImageDraw.ImageDraw, top: float) -> float:
    left, total_w = MARGIN, RIGHT - MARGIN
    draw.rectangle(
        [px(left), px(top), px(RIGHT), px(top + BOX_H)],
        fill=(255, 255, 255), outline=INK, width=px(0.5),
    )
    x = left + BOX_INNER
    draw_text(draw, (x, top + 6), "RESULT: 20/13 - PASSED", font(FONT_BOLD, 15), FAIL_RED)
    draw_text(draw, (x, top + 25), "Corrected with make.fun: agents earn USDC in", font(FONT_REG, 10), MUTED)
    draw_text(draw, (x, top + 37), "bounties there, so the thirteen years cost me nothing.", font(FONT_REG, 10), MUTED)
    draw_text(draw, (RIGHT - BOX_INNER, top + 27), "make.fun", font(FONT_BOLD, 19), MAGENTA, anchor="ra")
    return top + BOX_H


def draw_footer(draw: ImageDraw.ImageDraw, top: float) -> float:
    y = top + 8
    draw_text(draw, (MARGIN, y), "EXAMINER: the ghost", font(FONT_REG, 10), MUTED)
    draw.line([px(304), px(y + 10), px(RIGHT), px(y + 10)], fill=INK, width=px(0.4))
    draw_text(draw, (304, y + 13), "SIGNATURE", font(FONT_REG, 9), MUTED)
    return y + 20


def render(out_path: Path, scale: int = SCALE) -> tuple[int, float]:
    del scale
    img = Image.new("RGB", (px(CANVAS), px(CANVAS)), PAPER)
    draw = ImageDraw.Draw(img)

    draw_header(draw)
    draw_patient(draw)
    chart_end = draw_chart(img, draw)
    box_end = draw_result(draw, chart_end + BOX_PAD_TOP)
    end = draw_footer(draw, box_end)

    final = img.resize((CANVAS, CANVAS), Image.LANCZOS)
    final.save(out_path, "PNG")
    final.resize((480, 480), Image.LANCZOS).save(ROOT / "out" / "eyechart-480.png")
    return out_path.stat().st_size, end


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    target.parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "out").mkdir(parents=True, exist_ok=True)
    size, layout_end = render(target)
    print(f"{target} | {size} bytes | 512x512 | layout ends at y={layout_end:.0f}")
    if layout_end > CANVAS:
        print(f"WARNING: footer overflows the {CANVAS}px canvas by {layout_end - CANVAS:.0f}px")
