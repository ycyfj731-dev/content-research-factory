#!/usr/bin/env python3
"""Two actual archive-led 1920x1080 styleframes. NOT archival forgery or video."""
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageOps,ImageFilter
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
B=lambda n:ImageFont.truetype(FONT,n)
S=lambda n:ImageFont.truetype(SERIF,n)
W,H=1920,1080
PAPER=(228,224,214);INK=(22,23,24)
def fit(im,w,h):
  scale=max(w/im.width,h/im.height);im=im.resize((int(im.width*scale)+1,int(im.height*scale)+1),Image.Resampling.LANCZOS)
  x=(im.width-w)//2;y=(im.height-h)//2;return im.crop((x,y,x+w,y+h))
def paper():
  im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
  for k in range(34):d.line((0,k*32,W,k*32),fill=(225,221,211),width=1)
  return im
def label(d,xy,msg,color=(65,64,60),size=23):
  d.text(xy,msg,font=B(size),fill=color,stroke_width=0)
def archive_card(bg,photo,box,rot=0):
  x,y,w,h=box
  pic=ImageOps.grayscale(photo).convert('RGB')
  pic=ImageEnhance.Contrast(pic).enhance(1.13)
  pic=fit(pic,w-30,h-55)
  sheet=Image.new('RGB',(w,h),(246,243,235));sheet.paste(pic,(15,15))
  dr=ImageDraw.Draw(sheet);dr.line((14,h-27,w-14,h-27),fill=(55,55,55),width=1)
  dr.text((17,h-24),'ARCHIVAL PUBLICITY PHOTOGRAPH / 1944',fill=INK,font=B(11))
  if rot: sheet=sheet.rotate(rot,resample=Image.Resampling.BICUBIC,expand=True,fillcolor=PAPER)
  shadow=Image.new('RGBA',sheet.size,(0,0,0,55)).filter(ImageFilter.GaussianBlur(13));bg.paste(shadow,(x+18,y+20),shadow)
  bg.paste(sheet,(x,y))
# Frame A is an intentionally modern historical reference composition;
# there is no invented '1938 poster' or archival stage photograph.
poster=Image.open(ROOT/'gaslight_poster1944.jpg')
portrait=Image.open(ROOT/'bergman1944.jpg')
bg=paper();d=ImageDraw.Draw(bg)
d.rectangle((0,0,23,H),fill=INK)
label(d,(96,86),'AN IDEA BEFORE IT BECAME AN EXPRESSION',size=22)
d.line((95,145,1825,145),fill=INK,width=2)
d.text((91,196),'Gas Light',font=S(115),fill=INK)
d.text((99,336),'Patrick Hamilton  /  1938',font=B(31),fill=(54,53,51))
d.text((100,415),'A British stage play',font=S(33),fill=(79,75,68))
d.line((104,533,735,533),fill=(90,90,85),width=2)
d.text((99,595),'1938',font=S(153),fill=(50,48,44))
label(d,(104,797),'MODERN BIBLIOGRAPHIC LAYOUT',size=17)
label(d,(104,831),'Not presented as an original theatre programme',size=17)
archive_card(bg,poster,(865,105,690,855),rot=-2)
d=ImageDraw.Draw(bg);d.line((100,1009,1820,1009),fill=INK,width=2)
label(d,(103,1023),'EDITORIAL DOCUMENTARY  /  RESEARCH MOCKUP',size=16)
label(d,(1564,1023),'SOURCE: WIKIMEDIA COMMONS',size=15)
bg.save(OUT/'gaslight_styleframe_A.png')
# Frame B puts the authenticated publicity image at cinematic scale and
# identifies its origin rather than using aesthetic 'old film' inventions.
bg=paper();d=ImageDraw.Draw(bg)
bg.paste(fit(ImageOps.grayscale(portrait).convert('RGB'),820,1080),(0,0))
d.rectangle((817,0,835,H),fill=INK);d.rectangle((825,0,W,H),fill=(236,232,220))
d.text((905,117),'1944',font=S(182),fill=INK)
label(d,(920,335),'GASLIGHT / FILM ADAPTATION',size=26)
d.line((923,401,1804,401),fill=INK,width=3)
d.text((916,465),'Ingrid Bergman',font=S(61),fill=INK)
d.text((920,556),'George Cukor',font=B(30),fill=(79,75,68))
d.text((921,627),'MGM publicity photograph',font=B(25),fill=(79,75,68))
d.line((922,852,1805,852),fill=(112,105,95),width=1)
label(d,(923,876),'ARCHIVAL IMAGE, NOT A FILM FRAME',size=21)
label(d,(923,920),'Original: Wikimedia Commons',size=21)
label(d,(922,1016),'STILL FRAME / CINEMATIC ARCHIVE STUDY',size=17)
bg.save(OUT/'gaslight_styleframe_B.png')
with open(OUT/'qa.json','w') as fh:json.dump({'dimensions':[W,H],'frames':2,'archival_photos':['gaslight_poster1944.jpg','bergman1944.jpg'],'notice':'US public-domain claims per Commons; worldwide distribution must be assessed. 1938 title is modern typography, not a historic artifact.'},fh,indent=2)
print('Wrote',OUT)
