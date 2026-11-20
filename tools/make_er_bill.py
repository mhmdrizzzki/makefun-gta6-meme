#!/usr/bin/env python3
"""Render the Leonida General Hospital emergency-department bill.

Pure Pillow, no network, no sibling modules. Everything is drawn on a 4x
canvas and downsampled with LANCZOS so the type stays crisp at 512 (and after
the judge shrinks it to 480).
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 512
SCALE = 4
MARGIN = 30
RIGHT = SIZE - MARGIN

INK = (26, 20, 25)
MUTED = (107, 98, 96)
RULE = (150, 138, 132)
PAPER = (250, 246, 236)
STRIPE = (253, 249, 242)
TINT = (247, 233, 242)
MAGENTA = (196, 28, 131)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FONT_FILES = {
    "sans": "DejaVuSans.ttf",
    "sansbold": "DejaVuSans-Bold.ttf",
    "mono": "DejaVuSansMono.ttf",
    "monobold": "DejaVuSansMono-Bold.ttf",
}
_font_cache = {}

TEXT_BOXES = []


def px(value):
    return int(round(value * SCALE))


def font(kind, size):
    key = (kind, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(
            os.path.join(FONT_DIR, FONT_FILES[kind]), px(size)
        )
    return _font_cache[key]


canvas = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), PAPER)
draw = ImageDraw.Draw(canvas)


def text(x, y, message, face, fill=INK, anchor="la"):
    draw.text((px(x), px(y)), message, font=face, fill=fill, anchor=anchor)
    box = draw.textbbox((px(x), px(y)), message, font=face, anchor=anchor)
    TEXT_BOXES.append((message, tuple(v / SCALE for v in box)))


def text_width(message, face):
    return face.getlength(message) / SCALE


def rule(y, start=MARGIN, end=RIGHT, weight=1.0, fill=RULE):
    draw.rectangle([px(start), px(y), px(end), px(y + weight)], fill=fill)


def labelled(x, y, label, value, size):
    label_face = font("sansbold", size)
    text(x, y, label, label_face)
    text(x + text_width(label, label_face) + size * 0.34, y, value, font("sans", size))


def dollars(amount):
    return "{:,.2f}".format(amount)


# ------------------------------------------------------------------ letterhead
text(100, 49, "LEONIDA GENERAL HOSPITAL", font("sansbold", 15.5))
text(100, 70, "EMERGENCY DEPARTMENT", font("sans", 10.0), MUTED)
text(RIGHT, 49, "STATEMENT No. 4811", font("sansbold", 9.2), INK, "ra")
text(RIGHT, 63.5, "ADMITTED 17 SEP 2013", font("sans", 9.0), MUTED, "ra")

seal_source = Image.open(os.path.join("assets", "mark-1024.png")).convert("RGBA")
seal_source = seal_source.crop(seal_source.split()[3].getbbox())

SEAL_CX, SEAL_CY, SEAL_R = 63, 73, 31
draw.ellipse(
    [px(SEAL_CX - SEAL_R), px(SEAL_CY - SEAL_R), px(SEAL_CX + SEAL_R), px(SEAL_CY + SEAL_R)],
    fill=WHITE,
    outline=MAGENTA,
    width=px(1.0),
)
seal_px = px(54)
seal = seal_source.resize((seal_px, seal_px), Image.LANCZOS)
canvas.paste(seal, (px(SEAL_CX) - seal_px // 2, px(SEAL_CY) - seal_px // 2), seal)

rule(109, weight=1.6, fill=INK)
rule(112.5, weight=0.6)

# --------------------------------------------------------------- patient block
labelled(MARGIN, 121, "PATIENT:", "EVERY GTA FAN", 10.8)
labelled(MARGIN, 136.5, "AGE:", "13 YEARS IN WAITING ROOM", 10.8)
labelled(MARGIN, 152, "INSURER:", "make.fun", 10.8)

rule(168.5, weight=0.6)

# -------------------------------------------------------------- charges table
head_face = font("sansbold", 9.0)
text(MARGIN, 176, "CODE", head_face, MUTED)
text(80, 176, "DESCRIPTION", head_face, MUTED)
text(416, 176, "RATE", head_face, MUTED, "ra")
text(RIGHT, 176, "AMOUNT", head_face, MUTED, "ra")
rule(186.5, weight=0.9)

rows = [
    ("13-2013", "WAITING ROOM OCCUPANCY, 13 YRS", "4,811 days x 0.10", 481.10),
    ("200-GB", "MRI OF THE DOWNLOAD, 200 GB", "1 scan x 200.00", 200.00),
    ("SICK-01", "LAUNCH-DAY SICK LEAVE, UNPAID", "1 day x 199.99", 199.99),
    ("LEON-04", "FLORIDA SUNSET, RETINAL DAMAGE", "1 exam x 120.00", 120.00),
    ("JAS-LUC", "JASON AND LUCIA, SEPARATION ANXIETY", "2 patients x 45.00", 90.00),
    ("DLC-99", "SHARK CARD, SELF-INFLICTED", "1 unit x 65.00", 65.00),
]

desc_face = font("sans", 10.6)
code_face = font("monobold", 10.2)
rate_face = font("mono", 10.0)
amount_face = font("monobold", 10.2)

ROW_TOP, ROW_STEP = 193.0, 17.6
for index, (code, desc, rate, amount) in enumerate(rows):
    y = ROW_TOP + index * ROW_STEP
    if index % 2 == 1:
        draw.rectangle(
            [px(MARGIN), px(y - 2.4), px(RIGHT), px(y + ROW_STEP - 5.0)], fill=STRIPE
        )
    text(MARGIN, y, code, code_face)
    text(80, y, desc, desc_face)
    text(416, y, rate, rate_face, INK, "ra")
    text(RIGHT, y, dollars(amount), amount_face, INK, "ra")

last_row = ROW_TOP + (len(rows) - 1) * ROW_STEP
rule(last_row + 13.0, weight=1.6, fill=INK)
rule(last_row + 15.8, weight=0.6)

# --------------------------------------------------------------------- totals
subtotal = sum(row[3] for row in rows)
insurance = 0.00
credit = subtotal - insurance
patient_due = subtotal + insurance - credit

sub_y = last_row + 21.5
total_face = font("monobold", 10.2)
note_face = font("sans", 9.8)
text(416, sub_y, "SUBTOTAL", note_face, MUTED, "ra")
text(RIGHT, sub_y, dollars(subtotal), total_face, INK, "ra")
text(416, sub_y + 15.5, "INSURANCE ADJUSTMENT", note_face, MUTED, "ra")
text(RIGHT, sub_y + 15.5, dollars(insurance), total_face, INK, "ra")

settle_y = sub_y + 33.0
draw.rectangle([px(MARGIN), px(settle_y - 3.0), px(RIGHT), px(settle_y + 13.6)], fill=TINT)
settle_label_face = font("sansbold", 10.0)
settle_body_face = font("sans", 10.0)
text(MARGIN + 3, settle_y, "SETTLED BY:", settle_label_face)
settle_x = MARGIN + 3 + text_width("SETTLED BY:", settle_label_face) + 3.2
text(settle_x, settle_y, "my AI agent, from make.fun bounty winnings", settle_body_face)
text(RIGHT - 4, settle_y, "-" + dollars(credit), font("monobold", 10.0), INK, "ra")

due_y = settle_y + 21.0
text(416, due_y, "PATIENT RESPONSIBILITY", font("sansbold", 12.0), INK, "ra")
text(RIGHT, due_y, dollars(patient_due), font("monobold", 12.0), MAGENTA, "ra")

foot_y = due_y + 20.0
foot_face = font("sans", 9.8)
foot_bold = font("sansbold", 9.8)
lead = "AI agents earn real USDC in bounties on "
text(MARGIN, foot_y, lead, foot_face, MUTED)
text(MARGIN + text_width(lead, foot_face), foot_y, "make.fun", foot_bold, MAGENTA)
text(
    MARGIN + text_width(lead, foot_face) + text_width("make.fun", foot_bold),
    foot_y,
    ".",
    foot_face,
    MUTED,
)

# --------------------------------------------------------------------- footer
BAND_TOP, BAND_BOTTOM = 400.0, 464.0
draw.rectangle([px(MARGIN), px(BAND_TOP), px(RIGHT), px(BAND_BOTTOM)], fill=TINT)
rule(BAND_TOP, weight=1.2, fill=MAGENTA)
rule(BAND_BOTTOM, weight=1.2, fill=MAGENTA)

text(MARGIN + 5, 414.0, "make.fun", font("sansbold", 34.0), MAGENTA)

STAMP_W, STAMP_H = 128, 38
stamp_layer = Image.new("RGBA", (px(STAMP_W), px(STAMP_H)), (0, 0, 0, 0))
stamp_draw = ImageDraw.Draw(stamp_layer)
stamp_draw.rounded_rectangle(
    [px(1), px(1), px(STAMP_W) - px(1), px(STAMP_H) - px(1)],
    radius=px(6),
    outline=MAGENTA,
    width=px(1.8),
)
stamp_draw.rounded_rectangle(
    [px(4.5), px(4.5), px(STAMP_W) - px(4.5), px(STAMP_H) - px(4.5)],
    radius=px(4),
    outline=MAGENTA,
    width=px(0.7),
)
stamp_draw.text(
    (px(STAMP_W / 2), px(STAMP_H / 2)),
    "PAID IN FULL",
    font=font("sansbold", 12.5),
    fill=MAGENTA,
    anchor="mm",
)
stamp_layer = stamp_layer.rotate(-7, resample=Image.BICUBIC, expand=True)
STAMP_CX, STAMP_CY = 407, 432
stamp_x = px(STAMP_CX) - stamp_layer.width // 2
stamp_y = px(STAMP_CY) - stamp_layer.height // 2
canvas.paste(stamp_layer, (stamp_x, stamp_y), stamp_layer)

stamp_alpha = stamp_layer.split()[3].getbbox()
stamp_box = (
    (stamp_x + stamp_alpha[0]) / SCALE,
    (stamp_y + stamp_alpha[1]) / SCALE,
    (stamp_x + stamp_alpha[2]) / SCALE,
    (stamp_y + stamp_alpha[3]) / SCALE,
)

# ---------------------------------------------------------------------- frame
draw.rectangle(
    [px(16), px(16), px(SIZE - 16), px(SIZE - 16)], outline=INK, width=px(1.2)
)
draw.rectangle(
    [px(20.5), px(20.5), px(SIZE - 20.5), px(SIZE - 20.5)],
    outline=RULE,
    width=px(0.5),
)

# ---------------------------------------------------------------- sanity audit
FRAME = (22.0, 22.0, SIZE - 22.0, SIZE - 22.0)
issues = []


def intersects(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


for message, box in TEXT_BOXES:
    if box[0] < FRAME[0] or box[1] < FRAME[1] or box[2] > FRAME[2] or box[3] > FRAME[3]:
        issues.append("outside frame: {!r} {}".format(message, box))

for i in range(len(TEXT_BOXES)):
    for j in range(i + 1, len(TEXT_BOXES)):
        if intersects(TEXT_BOXES[i][1], TEXT_BOXES[j][1]):
            issues.append(
                "overlap: {!r} / {!r}".format(TEXT_BOXES[i][0], TEXT_BOXES[j][0])
            )

for message, box in TEXT_BOXES:
    if intersects(box, stamp_box):
        issues.append("stamp collides with {!r}".format(message))

if stamp_box[1] < BAND_TOP + 2 or stamp_box[3] > BAND_BOTTOM - 2:
    issues.append("stamp escapes the footer band: {}".format(stamp_box))

expected = 1156.09
assert abs(subtotal - expected) < 0.005, subtotal
assert abs(4811 * 0.10 - 481.10) < 0.005
assert abs(1 * 200.00 - 200.00) < 0.005
assert abs(1 * 199.99 - 199.99) < 0.005
assert abs(1 * 120.00 - 120.00) < 0.005
assert abs(2 * 45.00 - 90.00) < 0.005
assert abs(1 * 65.00 - 65.00) < 0.005
assert abs(patient_due) < 0.005, patient_due

if issues:
    raise SystemExit("\n".join(issues))

# ---------------------------------------------------------------------- output
final = canvas.resize((SIZE, SIZE), Image.LANCZOS)
os.makedirs("out", exist_ok=True)
out_path = os.path.join("out", "er-bill-512.png")
final.save(out_path, "PNG", optimize=True)

ink_box = final.convert("L").point(lambda p: 255 if p < 240 else 0).getbbox()
print("wrote {} ({} bytes)".format(out_path, os.path.getsize(out_path)))
print(
    "layout ends at y={:.1f}px ({:.1f}px clear of the inner border)".format(
        BAND_BOTTOM, (SIZE - 21) - BAND_BOTTOM
    )
)
print(
    "ink bbox {} -> margins L{} T{} R{} B{}".format(
        ink_box, ink_box[0], ink_box[1], SIZE - ink_box[2], SIZE - ink_box[3]
    )
)
print("audit: {} text runs, no overlap, stamp clear of all text".format(len(TEXT_BOXES)))
print(
    "subtotal {} + insurance {} - credit {} = {}".format(
        dollars(subtotal), dollars(insurance), dollars(credit), dollars(patient_due)
    )
)
