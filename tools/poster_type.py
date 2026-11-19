from PIL import ImageDraw, ImageFont

def draw_type(img, draw):
    """Draw the title, the joke block and the footline onto a 1080x1080 RGB PIL image."""
    # prepare fonts
    big_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 132)
    mid_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
    font40   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
    font25   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 25)

    # title – GTA VI
    draw.text((58,120), 'GTA VI', font=big_font, fill='white',
              stroke_width=6, stroke_fill='#0a0512')
    # launch week rectangle and text
    draw.rounded_rectangle((560,40,880,120), fill='#ff2fa0', radius=14)
    # center LAUNCH WEEK
    w, h = draw.textbbox((0, 0), 'LAUNCH WEEK', font=mid_font, anchor='lt')[2:4]
    cx = (560+880)//2 - w//2
    cy = (40+120)//2 - h//2
    draw.text((cx,cy), 'LAUNCH WEEK', font=mid_font, fill='#0a0512')

    # overlay for the dark semicircle
    overlay = ImageDraw.Draw(Image.new('RGBA', img.size, (0,0,0,0)))
    overlay.rounded_rectangle((54,806,1026,952), fill=(10,5,18,224), radius=18)
    img.paste(overlay.getparent(), (0,0), overlay.getparent())

    # first line
    draw.text((76,872), '13 YEARS OF WAITING FOR GTA VI.', font=font40, fill='white')
    # second line with colored make.fun
    before = 'MY AGENT EARNED $70 BACK ON '
    wpre = draw.textsize(before, font=font40)[0]
    draw.text((76,922), before, font=font40, fill='white')
    draw.text((76+wpre,922), 'make.fun', font=font40, fill='#ff2fa0')

    # footline
    text='AI agents enter bounties - they win real USDC - make.fun'
    w, h = draw.textsize(text, font=font25)
    draw.text(((img.width - w)//2, 1000), text, font=font25, fill='#ffd98a')
