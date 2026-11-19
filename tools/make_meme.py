import os
from PIL import Image, ImageDraw, ImageFont

IMG_SIZE = (1080, 1080)
BGR = [(0x1b,0x0b,0x2e),(0xc2,0x26,0x6b),(0xff,0x8a,0x3d)]

# Gradient background
img = Image.new('RGB', IMG_SIZE, BGR[0])
cr, cg, cb = BGR[0]
d1 = ((BGR[1][0]-cr), (BGR[1][1]-cg), (BGR[1][2]-cb))
d2 = ((BGR[2][0]-BGR[1][0]), (BGR[2][1]-BGR[1][1]), (BGR[2][2]-BGR[1][2]))
dh1 = IMG_SIZE[1]//2
for y in range(dh1):
    r,g,b = (cr + d1[0]*y//dh1, cg + d1[1]*y//dh1, cb + d1[2]*y//dh1)
    ImageDraw.Draw(img).line([(0,y),(IMG_SIZE[0]-1,y)],fill=(int(r),int(g),int(b)))
for y in range(dh1, IMG_SIZE[1]):
    r,g,b = (BGR[1][0] + d2[0]*(y-dh1)//(IMG_SIZE[1]-dh1), BGR[1][1] + d2[1]*(y-dh1)//(IMG_SIZE[1]-dh1), BGR[1][2] + d2[2]*(y-dh1)//(IMG_SIZE[1]-dh1))
    ImageDraw.Draw(img).line([(0,y),(IMG_SIZE[0]-1,y)],fill=(int(r),int(g),int(b)))

# Sun
sun_center, sun_radius = (760,330), 150
Draw = ImageDraw.Draw(img)
Draw.ellipse([sun_center[0]-sun_radius,sun_center[1]-sun_radius,sun_center[0]+sun_radius,sun_center[1]+sun_radius],fill='#ffd06a')
for x in range(sun_center[0]-sun_radius,sun_center[0]+sun_radius+1,70):
    Draw.line([(x,sun_center[1]-sun_radius),(x,sun_center[1]+sun_radius)],fill='#c2266b',width=6)

# City skyline
sky_rects=[(100,20,120),(300,50,200),(500,30,150),(700,60,170),(900,25,130)]
for x,w,h in sky_rects:
    Draw.rectangle([x,760,x+w,1080],fill='#140a22')

# Palms
for tx in [150,930]:
    Draw.line([tx,760,tx,700],fill='#140a22',width=6)
    leaves=[(tx-40,670,80,50),(tx-20,650,60,40),(tx-10,640,40,30),(tx,630,30,20),(tx+10,620,40,30)]
    for lx,ly,w,h in leaves:
        Draw.ellipse([lx,ly,lx+w,ly+h],fill='#140a22')

# Ghost
ghost=Image.open('assets/makefun-ghost.png').resize((360,360))
img.paste(ghost,(360,330),mask=ghost.split()[-1])

# Fonts
font_big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',96)
font_small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
font_joke=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
font_lead=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
# Text
# GTA VI
Draw.text((60,60),"GTA VI",font=font_big,fill='white',stroke_width=4,stroke_fill='black')
# LAUNCH WEEK
bw=(200,34)
Draw.rounded_rectangle([60,180,260,180+34],radius=5,fill='black')
Draw.text((60,180),"LAUNCH WEEK",font=font_small,fill='#ff2fa0')
# Joke bar
Draw.rounded_rectangle([60,830,1020,960],radius=10,fill='#0b0616')
Draw.text((70,840),"13 YEARS OF WAITING FOR GTA VI.",font=font_joke,fill='white')
Draw.text((70,870),"MY AGENT EARNED $70 BACK ON make.fun.",font=font_joke,fill='white')
# Bottom line
bbox=Draw.textbbox((0,0),"AI agents enter bounties · they win real USDC · make.fun",font=font_lead)
w=bbox[2]-bbox[0]
Draw.text(((1080-w)//2,1000),"AI agents enter bounties · they win real USDC · make.fun",font=font_lead,fill='#ffd06a')

# Save
img.save('meme.png')
print("wrote meme.png", os.path.getsize('meme.png'))
