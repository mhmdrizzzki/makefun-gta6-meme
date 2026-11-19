import random
from PIL import ImageDraw

def draw_sky(img, draw):
    '''Paint the Vice City sunset background onto a 1080x1080 RGB PIL image.'''
    w,h=1080,1080
    stops=[(0,(18,7,38)),(420,(109,19,85)),(760,(212,53,107)),(1080,(255,122,61))]
    for i in range(48):
        y1=int(i*h/48);y2=int((i+1)*h/48);cy=(y1+y2)//2
        for (ys,c1),(ye,c2) in zip(stops[:-1],stops[1:]):
            if ys<=cy<=ye:
                t=(cy-ys)/(ye-ys);r=int(c1[0]+t*(c2[0]-c1[0]));g=int(c1[1]+t*(c2[1]-c1[1]));b=int(c1[2]+t*(c2[2]-c1[2]));fill=(r,g,b);break
        draw.rectangle([0,y1,w,y2],fill=fill)
    sx,sy,rad=540,620,170
    draw.ellipse([sx-rad,sy-rad,sx+rad,sy+rad],fill=(255,217,138))
    for d in range(1,9):draw.ellipse([sx-d*10,sx-d*10,sx+d*10,sy+d*10],outline=None,fill=(255,217,138,20))
    for i in range(7):
        hgt=5+3*i;draw.rectangle([sx-rad,sy-hgt,sx+rad,sy],fill=(212,53,107))
    base_y=720
    for i in range(26):
        bw=30+10*(i%5);bh=180-40*(i%3);x=10+i*bw
        draw.rectangle([x,base_y,x+bw,base_y+bh],fill=(10,5,18))
        for wx in range(0,bw,10):
            for wy in range(0,bh,15):
                if (i+wx+wy)%4==0:draw.rectangle([x+wx,base_y+wy,x+wx+2,base_y+wy+3],fill=(255,207,106))
    for px in (120,960):
        draw.line([px,470,px,500],fill=(10,5,18),width=5)
        for fx in (-30,-20,-10,10,20,30):
            draw.polygon([(px+fx,470),(px+fx+5,460),(px+fx-5,460)],fill=(10,5,18))
    rng=random.Random(1234)
    for y in range(h):
        for x in range(w):
            r,g,b=img.getpixel((x,y));off=rng.randint(-6,6)
            img.putpixel((x,y),(max(0,min(255,r+off)),max(0,min(255,g+off)),max(0,min(255,b+off))))
