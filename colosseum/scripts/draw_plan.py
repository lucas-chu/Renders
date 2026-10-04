import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1];im=Image.new('RGB',(1600,1300),(240,237,226));d=ImageDraw.Draw(im)
font='/System/Library/Fonts/Supplemental/Arial.ttf';f=ImageFont.truetype(font,22);h=ImageFont.truetype(font,40);sm=ImageFont.truetype(font,17)
def pt(x,y):return (850+x*1.4,700-y*1.4)
def rect(x,y,w,h,fill):
 a=pt(x-w/2,y+h/2);b=pt(x+w/2,y-h/2);d.rectangle((*a,*b),fill=fill,outline=(145,134,110),width=2)
def ell(x,y,a,b,fill,outline=(113,104,88),width=2):
 p=pt(x-a,y+b);q=pt(x+a,y-b);d.ellipse((*p,*q),fill=fill,outline=outline,width=width)
def text(x,y,s):d.text(pt(x,y),s,font=f,fill=(45,45,36),anchor='mm')
d.text((70,54),'AMPHITHEATRVM',font=h,fill=(54,57,43));d.text((70,109),'Rome, circa AD 160  /  Scene geography and continuous camera route',font=f,fill=(103,101,84))
rect(-273,-231,180,150,(177,184,138));text(-273,-230,'Palatine terraces')
rect(38,292,230,160,(219,188,147));text(38,292,'Bath precinct')
rect(-217,17,175,100,(211,197,159));rect(-216,17,105,52,(185,176,150));text(-217,89,'Temple of Venus and Roma')
rect(209,11,90,88,(198,170,143));ell(209,11,33,23,(220,205,170));text(212,80,'Ludus Magnus')
ell(0,0,149,130,(228,220,196));ell(0,0,94.5,78,(154,139,112));ell(0,0,88,71.5,(237,226,200));ell(0,0,43.5,27.5,(210,183,132));text(0,0,'Colosseum')
ell(-115,-72,8,8,(91,139,141));text(-176,-87,'Meta Sudans')
rect(-126,57,10,10,(177,135,52));text(-159,120,'Colossus of Sol')
keys=[(1,(-195,-280,118)),(145,(-142,-200,70)),(241,(-84,-151,43)),(361,(-12,-119,29)),(457,(62,-108,40)),(565,(114,-48,78)),(720,(74,72,124))]
coords=[pt(p[0],p[1]) for _,p in keys];d.line(coords,fill=(151,48,32),width=5)
for (fr,p),(x,y) in zip(keys,coords):
 d.ellipse((x-6,y-6,x+6,y+6),fill=(151,48,32));d.text((x+12,y+7),f'{(fr-1)/24:.0f}s / {p[2]}m',font=sm,fill=(118,43,28))
d.text((70,1174),'Meters. X follows the amphitheatre’s long axis; Y follows its short axis.',font=f,fill=(81,84,66))
d.text((70,1210),'Monument proportions follow references. Secondary urban fabric and ceremonial decoration are interpretive.',font=sm,fill=(99,101,85))
im.save(P/'previews/scene-map.png')
