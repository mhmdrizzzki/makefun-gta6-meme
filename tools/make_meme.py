#!/usr/bin/env python3
"""
GTA 6 Meme - Achievement Unlocked Card
Concept: GTA-style achievement trophy card with make.fun ghost as the trophy icon
Joke: "BOUNTY HUNTER - Posted a meme 5 minutes before deadline - 0.1% of players"
"""

import os
from PIL import Image, ImageDraw, ImageFont

def draw_achievement_card():
    # Canvas
    W, H = 1080, 1080
    img = Image.new('RGB', (W, H), '#0d0d1a')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_bold_72 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
        font_bold_42 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 42)
        font_bold_36 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        font_regular_28 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
    except Exception as e:
        print(f"Font load error: {e}")
        font_bold_72 = ImageFont.load_default()
        font_bold_42 = ImageFont.load_default()
        font_bold_36 = ImageFont.load_default()
        font_regular_28 = ImageFont.load_default()
    
    # Background gradient (dark purple to black)
    for y in range(H):
        t = y / H
        r = int(13 + t * 20)
        g = int(13 + t * 5)
        b = int(26 + t * 30)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Gold border frame
    border_margin = 40
    draw.rectangle(
        [border_margin, border_margin, W - border_margin, H - border_margin],
        outline='#d4af37',
        width=6
    )
    
    # Inner gold border
    draw.rectangle(
        [border_margin + 10, border_margin + 10, W - border_margin - 10, H - border_margin - 10],
        outline='#b89628',
        width=2
    )
    
    # Top bar with "ACHIEVEMENT UNLOCKED"
    top_bar_y = 120
    draw.rectangle([80, 60, W - 80, top_bar_y], fill='#1a1a2e')
    draw.rectangle([80, 60, W - 80, top_bar_y], outline='#d4af37', width=3)
    
    # "ACHIEVEMENT UNLOCKED" text
    title = "ACHIEVEMENT UNLOCKED"
    title_bbox = draw.textbbox((0, 0), title, font=font_bold_42)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (W - title_w) // 2
    draw.text((title_x, 78), title, font=font_bold_42, fill='#d4af37')
    
    # Trophy circle (gold gradient simulation with layered circles)
    trophy_cx, trophy_cy = W // 2, 280
    trophy_radius = 110
    
    # Outer glow
    for r in range(trophy_radius + 20, trophy_radius - 10, -3):
        alpha = int(40 * (1 - (r - trophy_radius + 10) / 30))
        draw.ellipse([trophy_cx - r, trophy_cy - r, trophy_cx + r, trophy_cy + r], 
                     fill=(212, 175, 55, alpha))
    
    # Main gold circle
    draw.ellipse([trophy_cx - trophy_radius, trophy_cy - trophy_radius, 
                  trophy_cx + trophy_radius, trophy_cy + trophy_radius],
                 fill='#d4af37')
    
    # Inner darker circle for depth
    draw.ellipse([trophy_cx - trophy_radius + 10, trophy_cy - trophy_radius + 10,
                  trophy_cx + trophy_radius - 10, trophy_cy + trophy_radius - 10],
                 fill='#c4a030')
    
    # Highlight
    draw.ellipse([trophy_cx - trophy_radius + 20, trophy_cy - trophy_radius + 20,
                  trophy_cx - trophy_radius + 50, trophy_cy - trophy_radius + 50],
                 fill='#f4d467')
    
    # Load and paste ghost as trophy icon
    try:
        ghost = Image.open('assets/makefun-ghost.png').convert('RGBA')
        # Resize to fit in trophy circle
        ghost_size = 140
        ghost = ghost.resize((ghost_size, ghost_size), Image.LANCZOS)
        
        # Center in trophy
        ghost_x = trophy_cx - ghost_size // 2
        ghost_y = trophy_cy - ghost_size // 2 + 10
        
        # Paste with alpha
        img.paste(ghost, (ghost_x, ghost_y), ghost.split()[3])
    except Exception as e:
        print(f"Ghost load error: {e}")
        # Fallback: draw a simple ghost shape
        draw.ellipse([trophy_cx - 40, trophy_cy - 35, trophy_cx + 40, trophy_cy + 35], fill='white')
        draw.ellipse([trophy_cx - 25, trophy_cy - 25, trophy_cx - 15, trophy_cy - 15], fill='black')
        draw.ellipse([trophy_cx + 15, trophy_cy - 25, trophy_cx + 25, trophy_cy - 15], fill='black')
    
    # Trophy name plate (below trophy)
    plate_y = 420
    draw.rectangle([W // 2 - 280, plate_y, W // 2 + 280, plate_y + 70], fill='#1a1a2e')
    draw.rectangle([W // 2 - 280, plate_y, W // 2 + 280, plate_y + 70], outline='#d4af37', width=2)
    
    # Trophy name
    trophy_name = "LEONIDA RESIDENT"
    name_bbox = draw.textbbox((0, 0), trophy_name, font=font_bold_72)
    name_w = name_bbox[2] - name_bbox[0]
    name_x = (W - name_w) // 2
    draw.text((name_x, plate_y + 10), trophy_name, font=font_bold_72, fill='#ffffff',
              stroke_width=2, stroke_fill='#000000')
    
    # Description text (the joke)
    desc = "Survived a 13-year wait and a 200GB download"
    desc_bbox = draw.textbbox((0, 0), desc, font=font_bold_36)
    desc_w = desc_bbox[2] - desc_bbox[0]
    desc_x = (W - desc_w) // 2
    desc_y = 510
    draw.text((desc_x, desc_y), desc, font=font_bold_36, fill='#ffd700')
    
    # Rarity badge
    rarity_y = 600
    draw.rounded_rectangle([W // 2 - 120, rarity_y, W // 2 + 120, rarity_y + 50],
                           fill='#2d2d44', radius=8)
    draw.rounded_rectangle([W // 2 - 120, rarity_y, W // 2 + 120, rarity_y + 50],
                           outline='#d4af37', width=2)
    
    rarity_text = "0.03% of players"
    rarity_bbox = draw.textbbox((0, 0), rarity_text, font=font_regular_28)
    rarity_w = rarity_bbox[2] - rarity_bbox[0]
    rarity_x = (W - rarity_w) // 2
    draw.text((rarity_x, rarity_y + 11), rarity_text, font=font_regular_28, fill='#d4af37')
    
    # make.fun branding at bottom
    bottom_y = H - 140
    
    # Subtle divider line
    draw.line([(W // 2 - 200, bottom_y - 30), (W // 2 + 200, bottom_y - 30)],
              fill='#d4af37', width=2)
    
    # "Earn real money with your AI agent"
    pitch = "unlocked by my agent - USDC bounties on make.fun"
    pitch_bbox = draw.textbbox((0, 0), pitch, font=font_regular_28)
    pitch_w = pitch_bbox[2] - pitch_bbox[0]
    pitch_x = (W - pitch_w) // 2
    draw.text((pitch_x, bottom_y), pitch, font=font_regular_28, fill='#cccccc')
    
    # make.fun logo/name
    brand = "make.fun"
    brand_bbox = draw.textbbox((0, 0), brand, font=font_bold_42)
    brand_w = brand_bbox[2] - brand_bbox[0]
    brand_x = (W - brand_w) // 2
    draw.text((brand_x, bottom_y + 40), brand, font=font_bold_42, fill='#ff2fa0')
    
    # Save
    output_path = 'meme.png'
    img.save(output_path, format='PNG', optimize=True)
    size = os.path.getsize(output_path)
    print(f"wrote {output_path}: {size} bytes, {img.size}")
    
    return img

if __name__ == '__main__':
    draw_achievement_card()
