import bpy,sys,os,math,random,json,time
from pathlib import Path
from mathutils import Vector,Matrix
from math import sin,cos,pi,sqrt
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import *
random.seed(160)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials):bpy.data.materials.remove(d)
SC=bpy.context.scene
SC.unit_settings.system='METRIC'

def material(name,color,rough=.6,metal=0,texture=None,scale=1,bump=.12):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 geo=n.new('ShaderNodeNewGeometry');vm=n.new('ShaderNodeVectorMath');vm.operation='SCALE';vm.inputs[3].default_value=scale;l.new(geo.outputs['Position'],vm.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=3;l.new(vm.outputs[0],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.1;ramp.color_ramp.elements[0].color=(*[c*.72 for c in color],1);ramp.color_ramp.elements[1].position=.9;ramp.color_ramp.elements[1].color=(*color,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
 bu=n.new('ShaderNodeBump');bu.inputs['Strength'].default_value=bump;bu.inputs['Distance'].default_value=.045;l.new(noise.outputs['Fac'],bu.inputs['Height']);l.new(bu.outputs[0],bs.inputs['Normal'])
 if texture:
  for key,sock in [('diff','Base Color'),('rough','Roughness')]:
   paths=list((P/'assets').glob(texture+'_'+key+'.*'))
   if paths:
    im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(paths[0]),check_existing=True);im.projection='BOX';im.projection_blend=.22;l.new(vm.outputs[0],im.inputs[0])
    if key=='rough':im.image.colorspace_settings.name='Non-Color';l.new(im.outputs[0],bs.inputs[sock])
    else:
     mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.28;mix.inputs[2].default_value=(*color,1);l.new(im.outputs[0],mix.inputs[1]);l.new(mix.outputs[0],bs.inputs[sock])
  # photograph normal used as fine bump independent of block joints
  paths=list((P/'assets').glob(texture+'_nor_gl.*'))
  if paths:
   im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(paths[0]),check_existing=True);im.image.colorspace_settings.name='Non-Color';im.projection='BOX';im.projection_blend=.25;l.new(vm.outputs[0],im.inputs[0]);nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=bump;l.new(im.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],bs.inputs['Normal'])
 # cavity shading supports the stone detail without hard black crevices
 if name in ['Travertine','Trim','Marble']:
  ao=n.new('ShaderNodeAmbientOcclusion');ao.inputs['Distance'].default_value=1.2;ao.inputs['Color'].default_value=(*color,1);mx=n.new('ShaderNodeMixRGB');mx.blend_type='MULTIPLY';mx.inputs[0].default_value=.35
  prev=bs.inputs['Base Color'].links[0].from_socket;l.new(prev,mx.inputs[1]);l.new(ao.outputs['Color'],mx.inputs[2]);l.new(mx.outputs[0],bs.inputs['Base Color'])
 G.MATS[name]=m;return m
material('Travertine',(.72,.63,.48),.67,scale=1.4,bump=.2)
material('Trim',(.82,.75,.59),.57,scale=2.2,bump=.09)
material('Marble',(.83,.79,.69),.38,texture='marble_01',scale=.32,bump=.09)
material('ShadowStone',(.32,.27,.19),.8,scale=1.1)
material('Paving',(.52,.47,.36),.78,texture='cobblestone_floor_08',scale=.32,bump=.32)
material('Sand',(.63,.49,.29),.88,texture='sand_01',scale=.13,bump=.23)
material('Earth',(.24,.21,.14),.95,scale=.035,bump=.35)
material('Grass',(.18,.22,.075),.9,scale=.1)
material('Bronze',(.48,.29,.08),.28,.78,scale=1,bump=.08)
material('Gold',(.75,.46,.13),.23,.82,scale=2,bump=.04)
material('Crimson',(.30,.012,.019),.72,scale=8,bump=.09)
material('Linen',(.79,.68,.47),.88,scale=12,bump=.08)
material('Rope',(.22,.15,.078),.85,scale=5)
material('Timber',(.16,.074,.023),.8,scale=3)
material('Terracotta',(.37,.105,.047),.8,texture='clay_roof_tiles_02',scale=.36,bump=.45)
material('Plaster',(.69,.54,.35),.82,scale=.3)
material('RosePlaster',(.43,.21,.13),.87,scale=.3)
material('Ochre',(.57,.35,.12),.85,scale=.3)
material('Window',(.036,.027,.018),.92,scale=1)
material('Foliage',(.092,.145,.038),.86,scale=.5)
material('FoliageLight',(.16,.22,.071),.85,scale=.4)
material('Bark',(.16,.085,.037),.9,scale=2)
material('Skin',(.42,.245,.135),.7,scale=1)
material('Hair',(.042,.026,.017),.85,scale=1)
for name,color in [('Toga',(.69,.67,.57)),('Rust',(.35,.13,.065)),('Indigo',(.10,.15,.19)),('Umber',(.24,.19,.105)),('Saffron',(.66,.39,.10))]:material(name,color,.85,scale=3)
water=material('Water',(.10,.23,.18),.12,.25,scale=.35,bump=.16);water.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.3
print('MATERIALS READY',flush=True)

# Ellipse tangent frame. Local X follows facade, Y points out.
def bayframe(a,b,t,z=0):
 tangent=Vector((-a*sin(t),b*cos(t),0)).normalized();normal=Vector((tangent.y,-tangent.x,0));m=Matrix(((tangent.x,normal.x,0,a*cos(t)),(tangent.y,normal.y,0,b*sin(t)),(0,0,1,z),(0,0,0,1)));return m

with group('01 | Colosseum — foundation'):
 ellipse_slab(99,82.5,.22,.6,'Travertine')
 for z,w in [(0,2.1),(.2,1.4),(.4,.8)]:ellring(94.5,78,[(0,z),(w,z),(w,z+.18),(0,z+.18)],'Trim')
with group('02 | Colosseum — outer orders'):
 for tier,(z,h,spring) in enumerate([(0.6,10.3,5.0),(12.6,9.6,4.5),(24.4,9.2,4.45)]):
  for i in range(80):
   t=(i+.5)*2*pi/80;width=sqrt((93.35*sin(t))**2+(76.85*cos(t))**2)*2*pi/80
   with frame(matrix=bayframe(93.35,76.85,t,z)):
    archbay(width+.07,h,4.2,spring,2.3,'Travertine')
    # grooved archivolt cap band above each opening
    arc(2.64,2.76,spring,1.16,1.24,'Trim',18,.004)
   t=i*2*pi/80
   with frame(matrix=bayframe(93.35,76.85,t,z)):
    column(0,1.23,.05,h-.1,.54,tier,'Trim',True)
    box((0,1.20,.18),(1.5,1.32,.3),'Trim')
  # sculpted continuous string courses, fascia, cornice and shadow reveals
  zz=z+h
  for dz,width,height,mat in [(0,1.25,.23,'Trim'),(.23,1.02,.32,'Travertine'),(.55,1.02,.76,'Travertine'),(1.31,1.36,.15,'Trim'),(1.46,1.58,.25,'Trim')]:
   ellring(93.35,76.85,[(-1.18,zz+dz),(width,zz+dz),(width,zz+dz+height),(-1.18,zz+dz+height)],mat)
  for i in range(800):
   with frame(matrix=bayframe(94.52,78.02,2*pi*i/800,zz+1.22)):box((0,0,0),(.28,.5,.24),'Trim')
with group('03 | Colosseum — attic & clipei'):
 z=36
 for i in range(80):
  t=(i+.5)*2*pi/80;width=sqrt((93.35*sin(t))**2+(76.85*cos(t))**2)*2*pi/80
  with frame(matrix=bayframe(93.35,76.85,t,z)):
   if i%2==0:
    box((0,0,1.65),(width+.05,2.1,3.3),'Travertine');box((0,0,9.5),(width+.05,2.1,4.4),'Travertine')
    for s in [-1,1]:box((s*(width/4+.55),0,5.3),(width/2-1.1,2.1,4),'Travertine')
    box((0,1.2,3.3),(2.6,.45,.25),'Trim');box((0,1.2,7.32),(2.6,.45,.28),'Trim')
    for s in [-1,1]:box((s*1.2,1.15,5.3),(.22,.3,4),'Trim')
   else:
    box((0,0,5.85),(width+.05,2.1,11.7),'Travertine')
    # bronze shields on solid attic bays
    with frame((0,1.12,5.4),matrix=Matrix.Translation(Vector((0,1.12,5.4)))@Matrix.Rotation(pi/2,4,'X')):
     lathe((0,0,0),[(0,0),(.91,0),(.96,.10),(.90,.18),(.3,.3),(0,.32)],'Bronze',32)
  with frame(matrix=bayframe(93.35,76.85,i*2*pi/80,z)):
   box((0,1.1,5.7),(1.04,.43,11.4),'Trim');box((0,1.15,.3),(1.5,.7,.45),'Trim');box((0,1.2,11.35),(1.5,.75,.4),'Trim')
 ellring(93.35,76.85,[(-1.2,47.6),(1.3,47.6),(1.3,47.95),(1.75,48.10),(1.75,48.50),(-1.2,48.50)],'Trim')
 for i in range(800):
  with frame(matrix=bayframe(94.52,78.02,2*pi*i/800,47.77)):box((0,0,0),(.3,.48,.32),'Trim')
 # The backside of the attic bounds the upper ambulatory.
 ellring(90.6,74.1,[(0,36),(1,36),(1,47.5),(0,47.5)],'Travertine')
print('EXTERIOR READY',flush=True)

with group('04 | Colosseum — vaulted ambulatory'):
 for z in [.6,12.6,24.4]:
  ellring(88.7,72.2,[(-.5,z),(3.8,z),(3.8,z+.32),(-.5,z+.32)],'Travertine')
  for i in range(80):
   t=(i+.5)*2*pi/80;width=sqrt((86*sin(t))**2+(69.5*cos(t))**2)*2*pi/80
   with frame(matrix=bayframe(86,69.5,t,z)):archbay(width+.05,9.0,3.4,4.2,1.4,'ShadowStone',False)
with group('05 | Colosseum — sculpture'):
 for tier,z in enumerate([12.8,24.6]):
  for i in range(80):
   t=(i+.5)*2*pi/80
   with frame(matrix=bayframe(93.35,76.85,t,z)):
    box((0,.05,.32),(1.5,1.3,.65),'Marble');human(0,.05,.64,2.07,'Marble',True,i)
with group('06 | Colosseum — marble cavea'):
 ellipse_slab(43.5,27.5,.67,.7,'Sand')
 ellring(44,28,[(-.1,.5),(.9,.5),(.9,4.5),(-.1,4.5)],'Marble')
 ellring(44,28,[(-.3,4.5),(1.4,4.5),(1.4,4.83),(-.3,4.83)],'Trim')
 # Two principal circulation terraces break up the rake.
 for row in range(48):
  extra=1.5*(row>=14)+1.5*(row>=32)
  a=45.4+row*.74+extra;b=29.4+row*.74+extra;z=4.7+row*.59
  for sector in range(40):
   start=2*pi*sector/40+.012;end=2*pi*(sector+1)/40-.012
   ellring(a,b,[(0,z-.5),(.74,z-.5),(.74,z+.11),(0,z+.11)],'Marble',n=10,start=start,end=end)
  if row in [13,31]:
   ellring(a+.74,b+.74,[(0,z+.11),(1.5,z+.11),(1.5,z+.22),(0,z+.22)],'Trim')
 for sec in range(40):
  t=2*pi*sec/40
  for row in range(96):
   rr=row/2;extra=1.5*(rr>=14)+1.5*(rr>=32);a=45.4+rr*.74+extra;b=29.4+rr*.74+extra;z=4.7+rr*.59
   with frame(matrix=bayframe(a,b,t,z)):box((0,.2,-.15),(1.36,.42,.3),'Trim')
 # Rear colonnaded gallery, open to the seating bowl.
 ellring(85,68.5,[(-1.2,34),(2.7,34),(2.7,34.5),(-1.2,34.5)],'Marble')
 for i in range(120):
  t=i*2*pi/120;column(84.7*cos(t),68.2*sin(t),34.5,7.8,.36,2,'Marble',False)
 ellring(85,68.5,[(-1.1,42.3),(2.5,42.3),(2.5,43.3),(-1.1,43.3)],'Trim')
 # Inner parapet with marble panels and red pier accents.
 for i in range(80):
  with frame(matrix=bayframe(84.0,67.5,i*2*pi/80,33.0)):box((0,0,.55),(1.1,.5,1.1),'Crimson')
 # Portal heads set into the terraces and principal arena gates.
 for level in [14,32]:
  rr=level;extra=1.5*(rr>=14)+1.5*(rr>=32);a=45.4+rr*.74+extra;b=29.4+rr*.74+extra;z=4.7+rr*.59
  for sec in range(0,40,2):
   t=2*pi*(sec+.5)/40
   with frame(matrix=bayframe(a,b,t,z)):
    box((0,-.1,.85),(2.4,.06,1.7),'Window');archbay(3.4,2.4,2.3,1.0,.4,'Trim',False)
 for t in [0,pi]:
  with frame(matrix=bayframe(44.15,28.15,t,.7)):
   box((0,0,1.8),(4.6,.1,3.6),'Timber')
   for x in [-1.8,-1.2,-.6,0,.6,1.2,1.8]:box((x,-.13,1.8),(.07,.1,3.6),'Bronze')
print('INTERIOR READY',flush=True)
with group('07 | Regalia — imperial pulvinar'):
 for side in [-1,1]:
  with frame((0,side*32,4.7)):
   box((0,0,0),(13,6,.75),'Marble');box((0,-side*3,1),(13,.4,1.8),'Crimson')
   for x in [-5.8,5.8]:
    column(x,side*2,.4,5,.28,2,'Marble')
    beam((x,side*2,5.4),(x,-side*3,5.4),.12,'Gold')
   box((0,0,5.45),(13,6,.15),'Crimson')
   for x in range(-6,7):box((x,-side*3.05,1.5),(.045,.035,.8),'Gold')
with group('08 | Rigging — 240 masts and cables'):
 for i in range(240):
  t=2*pi*i/240;a,b=95.1,78.6;x,y=a*cos(t),b*sin(t)
  beam((x,y,43.6),(x,y,56.0),.12,'Timber',10,.08)
  with frame(matrix=bayframe(a,b,t,44.0)):box((0,0,0),(.5,.65,.55),'Trim')
  # inward radial cables with a restrained catenary
  pts=[]
  for k in range(9):
   u=k/8;pts.append(((a*(1-u)+60*u)*cos(t),(b*(1-u)+42*u)*sin(t),56*(1-u)+44.3*u-1.2*sin(pi*u)))
  rope(pts,.025)
  if i%3==0:
   pts=[((a+q*7)*cos(t),(b+q*7)*sin(t),56-q*11-.5*sin(pi*q)) for q in [0,.25,.5,.75,1]];rope(pts,.025)
 ellring(60,42,[(-.035,44.25),(.035,44.25),(.035,44.32),(-.035,44.32)],'Rope',n=480)
with group('09 | Velarium — linen sails'):
 for i in range(80):
  # Awning drawn over the sunny perimeter, with select retracted bays.
  t0=2*pi*i/80+.001;t1=2*pi*(i+1)/80-.001;v=[];nu=14;nv=8
  extension=.96 if i%20 not in [0,1,2] else .35
  for j in range(nu+1):
   u=j/nu*extension
   for k in range(nv+1):
    t=t0+(t1-t0)*k/nv;a=91.5*(1-u)+60*u;b=75*(1-u)+42*u
    z=49.25-5*u-1.1*sin(pi*u)-.8*sin(pi*k/nv)*sin(pi*u)+.08*sin(u*37+k*.7)
    v.append((a*cos(t),b*sin(t),z))
  geo(v,[(j*(nv+1)+k,j*(nv+1)+k+1,(j+1)*(nv+1)+k+1,(j+1)*(nv+1)+k) for j in range(nu) for k in range(nv)],'Linen',True)
  for side in [0,1]:
   t=t0 if side==0 else t1;pts=[]
   for j in range(nu+1):
    u=j/nu*extension;pts.append(((91.5*(1-u)+60*u)*cos(t),(75*(1-u)+42*u)*sin(t),49.27-5*u-1.1*sin(pi*u)))
   rope(pts,.035,'Rope')
with group('10 | Regalia — ceremonial hangings'):
 for i in range(0,80,4):
  t=i*2*pi/80
  with frame(matrix=bayframe(95.15,78.65,t,15.7)):
   beam((-1,0,0),(1,0,0),.06,'Gold')
   # Fabric hangs from a crossbar, with gold borders and weighted hems.
   v=[]
   for j in range(16):
    u=j/15
    for k in range(9):
     x=(k/8-.5)*1.7;y=.10+.17*sin(k/8*3*pi+u*3)*u;v.append((x,y,-3.4*u))
   geo(v,[(j*9+k,j*9+k+1,(j+1)*9+k+1,(j+1)*9+k) for j in range(15) for k in range(8)],'Crimson',True)
   for s in [-1,1]:rope([(s*.82,.1,-j/15*3.4) for j in range(16)],.019,'Gold')
   for k in range(12):beam((-.8+k*.145,.1,-3.4),(-.8+k*.145,.1,-3.63),.022,'Gold',5)
   # Gold laurel wreath device on each vexillum.
   for k in range(16):
    a=2*pi*k/16;ellipsoid((.4*cos(a),.30,-1.15+.5*sin(a)),(.075,.018,.13),'Gold',8,4)
with group('11 | Public life — seated spectators'):
 for row in range(46):
  extra=1.5*(row>=14)+1.5*(row>=32);a=45.75+row*.74+extra;b=29.75+row*.74+extra;z=4.8+row*.59;n=int(2*pi*sqrt((a*a+b*b)/2)/.86)
  for i in range(n):
   t=2*pi*(i+random.random()*.25)/n
   if abs((t/(2*pi)*40+.5)%1-.5)<.10 or random.random()>.72:continue
   x,y=a*cos(t),b*sin(t);cloth=random.choices(['Toga','Linen','Rust','Umber','Indigo','Saffron'],[48,17,9,13,8,5])[0]
   # Small seated meshes remain spatial, with separate heads and shoulders.
   with frame((x,y,z),t-pi/2):
    geo([(-.22,-.13,.22),(.22,-.13,.22),(.23,.10,.23),(-.23,.10,.23),(-.19,-.13,.68),(.19,-.13,.68),(.15,.12,.71),(-.15,.12,.71)],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],cloth,True)
    ellipsoid((0,0,.84),(.12,.105,.155),'Skin',6,4)
    box((0,.21,.21),(.39,.43,.15),cloth)
with group('12 | Public life — precinct gathering'):
 for i in range(900):
  t=random.uniform(0,2*pi);r=random.uniform(1.09,1.53);x=94.5*r*cos(t);y=78*r*sin(t)
  if -145<x<-110 and -85<y<40:continue
  with frame((x,y,.28),random.uniform(0,2*pi)):
   human(0,0,0,random.uniform(.91,1.06),random.choice(['Toga','Linen','Rust','Umber','Indigo']),False,i)
 # Small attendants establish arena scale without staging violence.
 for x,y in [(-18,3),(-16,4),(14,-5),(16,-4),(0,14)]:human(x,y,.72,1,'Toga')
print('RIGGING AND LIFE READY',flush=True)

# Architectural precinct toolkit. All buildings share materials and proportions.
def roof(x,y,z,w,d,rise,mat='Terracotta'):
 v=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x-w/2,y+d/2,z),(x+w/2,y+d/2,z),(x-w/2,y,z+rise),(x+w/2,y,z+rise)]
 geo(v,[(0,1,5,4),(2,4,5,3),(0,4,2),(1,3,5)],mat)
 # Individually modeled imbrices along visible roof slope.
 if w*d<2500:
  for xx in range(int(w/.9)+1):
   q=x-w/2+xx*.9
   for side in [-1,1]:beam((q,y,z+rise+.05),(q,y+side*d/2,z+.05),.075,mat,6)
 beam((x-w/2,y,z+rise+.08),(x+w/2,y,z+rise+.08),.14,mat,8)
def house(x,y,z,w,d,h,mat='Plaster',rich=False):
 box((x,y,z+h/2),(w,d,h),mat);box((x,y,z+.45),(w+.1,d+.1,.8),'ShadowStone')
 roof(x,y,z+h+.15,w+1,d+1,min(4,d*.23))
 floors=max(1,int(h/3.3))
 for side in [-1,1]:
  for i in range(max(2,int(w/3))):
   xx=x+(i+.5)*w/max(2,int(w/3))-w/2
   for j in range(floors):
    zz=z+2+j*3.3
    box((xx,y+side*(d/2+.02),zz),(.85,.055,1.45),'Window')
    box((xx,y+side*(d/2+.13),zz-.78),(1.1,.3,.14),'Trim')
  box((x,y+side*(d/2+.04),z+1.35),(1.7,.12,2.7),'Timber')
 for side in [-1,1]:
  for i in range(max(2,int(d/3.5))):
   yy=y+(i+.5)*d/max(2,int(d/3.5))-d/2
   for j in range(floors):box((x+side*(w/2+.02),yy,z+2+j*3.3),(.055,.8,1.35),'Window')
 if rich:
  box((x,y-d/2-2,z+4),(w+1,4,.45),'Trim')
  for i in range(int(w/3)+1):column(x-w/2+i*w/int(w/3),y-d/2-3.6,z,4,.24,1,'Trim',False)
def temple(cx,cy,z,length=105,width=52,height=19,grand=True):
 # Long axis X. The east front faces the amphitheatre.
 with frame((cx,cy,z)):
  for k in range(6):box((0,0,k*.3),(length+5-k*.7,width+5-k*.7,.32),'Marble')
  box((0,0,2+height*.46),(length-27,width-18,height*.92),'Plaster')
  for side in [-1,1]:
   for i in range(10):column(side*(length/2-2),-width/2+2+i*(width-4)/9,1.8,height, .82 if grand else .5,2,'Marble',grand)
   for i in range(1,20):column(-length/2+2+i*(length-4)/20,side*(width/2-2),1.8,height,.82 if grand else .5,2,'Marble',False)
  box((0,0,height+2.1),(length+1,width+1,1.4),'Marble');box((0,0,height+3),(length+2,width+2,.4),'Gold')
  # Gabled long roof, pediments on east and west ends.
  roof(0,0,height+3.5,length+3,width+3,7,'Terracotta')
  for side in [-1,1]:
   with frame((side*(length/2+1.5),0,0),pi/2):
    polyprism([(-width/2,height+3.7),(width/2,height+3.7),(0,height+10.5)],-.4,.4,'Marble')
    beam((-width/2,0,height+3.9),(0,0,height+10.7),.27,'Trim');beam((0,0,height+10.7),(width/2,0,height+3.9),.27,'Trim')
    for xx in [-18,-12,-6,0,6,12,18]:
     if abs(xx)<width/2-2:human(xx,-.48,height+4,1.2+(1-abs(xx)/(width/2))*1.1,'Marble',True,int(xx))
   for yy in [-width/2,0,width/2]:human(side*(length/2+1),yy,height+4+(7 if yy==0 else 0),2,'Marble',True,1)
with group('13 | Site — paving and Via Sacra'):
 box((0,0,-.7),(2200,2200,1),'Earth')
 ellipse_slab(149,130,-.02,.35,'Paving')
 # ceremonial approach and connecting streets
 box((-213,-63,-.015),(232,24,.25),'Paving');box((235,0,-.015),(262,18,.25),'Paving')
 for side in [-1,1]:box((-215,-63+side*12,.1),(230,.8,.35),'Travertine')
 for y in [-165,170,300,-340]:box((0,y,-.04),(1100,12,.22),'Paving')
 for x in [-390,170,310,455]:box((x,10,-.03),(11,1100,.25),'Paving')
 # Paving curb ring and original precinct boundary stones
 ellring(116,99.5,[(0,0),(1,0),(1,.2),(0,.2)],'Trim')
 for i in range(80):
  t=2*pi*i/80;column(113*cos(t),96.5*sin(t),.15,2.3,.33,0,'Travertine',False)
with group('14 | Velia — Temple of Venus and Roma'):
 box((-217,17,4),(175,100,8),'Travertine')
 for side in [-1,1]:
  for i in range(25):
   with frame((-301+i*7,17+side*49,1.1)):
    archbay(6.9,6.3,4.1,2.5,1.5,'Travertine',False)
 # staircase across eastern end of precinct
 for i in range(27):box((-115-i*.62,17,i*.29/2),(1.3,82,i*.29+.12),'Marble')
 temple(-216,17,8,105,52,18,True)
 # precinct side porticoes
 for side in [-1,1]:
  for i in range(35):column(-298+i*4.9,17+side*43,8,8,.46,1,'Trim',False)
  box((-214,17+side*43,16.4),(174,5,.8),'Trim');roof(-214,17+side*43,16.8,174,6,1.2)
with group('15 | Meta Sudans — fountain'):
 x,y=-115,-72
 with frame((x,y,.2)):
  cylinder((0,0,.30),8.0,.6,'Travertine',96)
  ellring(7.65,7.65,[(0,.4),(.65,.4),(.65,1.3),(0,1.3)],'Marble',96)
  cylinder((0,0,.85),7.6,.12,'Water',96)
  lathe((0,0,.8),[(3.4,0),(3.4,1),(3,1.3),(3,5.3),(2.6,5.6),(2.0,6),(1.4,10),(.7,14),(0,15.5)],'Marble',64)
  for i in range(24):
   t=2*pi*i/24;pts=[((2.1*(1-u)+.5*u)*cos(t),(2.1*(1-u)+.5*u)*sin(t),6.8+8.1*u) for u in [0,.2,.4,.6,.8,1]];rope(pts,.028,'Water',5)
with group('16 | Colossus of Sol'):
 with frame((-126,57,0)):
  for k in range(3):box((0,0,k*.5),(12-k,12-k,.5),'Marble')
  box((0,0,5),(8.8,8.8,7),'Travertine');box((0,0,8.7),(9.8,9.8,.5),'Trim')
  # Idealized bronze colossus: nude anatomical forms with raised right hand.
  with frame((0,0,9),scale=14):
   for side in [-1,1]:
    beam((side*.16,0,.15),(side*.14,0,.79),.115,'Bronze',14,.14);ellipsoid((side*.14,.08,.1),(.12,.24,.1),'Bronze',16,8)
   ellipsoid((0,0,.83),(.27,.17,.21),'Bronze',20,10);ellipsoid((0,0,1.17),(.3,.16,.39),'Bronze',20,12)
   for side in [-1,1]:ellipsoid((side*.12,.1,1.3),(.16,.1,.14),'Bronze',16,8)
   cylinder((0,0,1.5),.088,.18,'Bronze',16);ellipsoid((0,0,1.69),(.13,.13,.19),'Bronze',20,12)
   beam((-.27,0,1.4),(-.39,0,1.12),.1,'Bronze',14,.075);beam((-.39,0,1.12),(-.43,.12,.91),.07,'Bronze',12)
   beam((.27,0,1.4),(.55,0,1.57),.10,'Bronze',14,.08);beam((.55,0,1.57),(.6,.03,1.94),.07,'Bronze',12,.055)
   ellipsoid((.61,.03,1.95),(.06,.05,.10),'Bronze',12,6)
   for i in range(7):
    t=pi*i/6;beam((.13*cos(t),0,1.73+.15*sin(t)),(.30*cos(t),0,1.73+.32*sin(t)),.025,'Gold',8,0)
with group('17 | Ludus Magnus — gladiatorial school'):
 cx,cy=209,11
 for side in [-1,1]:
  house(cx,cy+side*38,0,90,13,10,'RosePlaster')
  house(cx+side*39,cy,0,13,64,10,'RosePlaster')
  for i in range(17):column(cx-35+i*4.4,cy+side*28,0,5,.28,0,'Trim',False)
  box((cx,cy+side*28,5.2),(75,4,.4),'Trim')
 with frame((cx,cy,.12)):
  ellipse_slab(27,18,.1,.2,'Sand')
  for i in range(9):ellring(27+i*.77,18+i*.77,[(0,i*.42),(.78,i*.42),(.78,i*.42+.35),(0,i*.42+.35)],'Travertine',128)
print('MONUMENTS READY',flush=True)
# Broader terrain and the inhabited city make the horizon continuous.
def ground(x,y):
 return 28*math.exp(-((x+285)/165)**4-((y+235)/155)**4)+17*math.exp(-((x-90)/240)**4-((y-275)/140)**4)
with group('18 | Landscape — Roman hills'):
 v=[];n=120
 for j in range(n+1):
  y=-1100+j*2200/n
  for i in range(n+1):
   x=-1100+i*2200/n;z=ground(x,y)-.27+.5*sin(x*.017)*sin(y*.023);v.append((x,y,z))
 geo(v,[(j*(n+1)+i,j*(n+1)+i+1,(j+1)*(n+1)+i+1,(j+1)*(n+1)+i) for j in range(n) for i in range(n)],'Earth',True)
with group('19 | Palatine — imperial terraces'):
 for lev in range(3):box((-273,-231,lev*8+4),(180-lev*13,150-lev*12,8),'Travertine')
 # Garden courts and four palace ranges on the plateau.
 for x,y,w,d,h in [(-340,-220,24,80,18),(-210,-235,24,98,18),(-275,-290,112,24,20),(-275,-177,112,20,17),(-270,-260,30,20,24)]:house(x,y,24,w,d,h,'Plaster',True)
 box((-274,-226,24.1),(94,57,.4),'Marble');box((-274,-226,24.35),(43,20,.45),'Water')
 for side in [-1,1]:
  for i in range(20):column(-320+i*4.8,-226+side*29,24.3,8,.4,1,'Trim',False)
  box((-274,-226+side*29,32.5),(96,3,.5),'Trim')
 # Supporting arcades along the palace face.
 for i in range(25):
  with frame((-357+i*7,-157,1)):
   archbay(7,7,4.1,3.8,2,'Travertine',False)
   with frame((0,0,8)):archbay(7,7,4.1,3.8,2,'Travertine',False)
with group('20 | Oppian — bath precinct'):
 cx,cy=38,292;z=ground(cx,cy)
 box((cx,cy,z),(230,160,2),'Travertine')
 for x,y,w,d,h in [(cx,cy+20,72,56,26),(cx-65,cy,40,70,18),(cx+65,cy,40,70,18),(cx,cy-49,128,25,15)]:house(x,y,z,w,d,h,'RosePlaster')
 for side in [-1,1]:
  for i in range(38):column(cx-105+i*5.7,cy+side*72,z,8,.42,0,'Trim',False)
  box((cx,cy+side*72,z+8.4),(219,6,.8),'Trim')
with group('21 | City — insulae and courtyard houses'):
 for xx in range(-700,801,39):
  for yy in range(-680,801,37):
   x=xx+random.uniform(-5,5);y=yy+random.uniform(-4,4)
   if (x/175)**2+(y/147)**2<1:continue
   if -327<x<-100 and -43<y<82:continue
   if 148<x<265 and -45<y<62:continue
   if -382<x<-174 and -320<y<-137:continue
   if -85<x<160 and 205<y<382:continue
   if any(abs(y-r)<13 for r in [-165,170,300,-340]):continue
   if any(abs(x-r)<11 for r in [-390,170,310,455]):continue
   if random.random()<.14:continue
   z=ground(x,y);w=random.uniform(16,28);d=random.uniform(15,25);h=random.choice([7,10,13,16])
   house(x,y,z,w,d,h,random.choice(['Plaster','Plaster','Ochre','RosePlaster']))
 # Street stalls, awnings and shop canopies in the east precinct.
 for i in range(14):
  x=155+i*8;y=-107;house(x,y,0,6,8,3.7,'Plaster')
  for s in [-1,1]:beam((x+s*2.9,y-8,0),(x+s*2.9,y-8,3.0),.08,'Timber')
  geo([(x-3,y-4,3.5),(x+3,y-4,3.5),(x+3,y-8,3.0),(x-3,y-8,3.0)],[(0,1,2,3)],'Linen')
print('CITY READY',flush=True)

# Irregular Mediterranean pines and cypresses, kept outside the paved precinct.
def tuft(c,r,mat,seed):
 rng=random.Random(seed);n=12;m=8;v=[]
 for j in range(m+1):
  p=pi*j/m
  for i in range(n):
   a=2*pi*i/n;rr=rng.uniform(.77,1.22);v.append((c[0]+r[0]*sin(p)*cos(a)*rr,c[1]+r[1]*sin(p)*sin(a)*rr,c[2]+r[2]*cos(p)*rr))
 geo(v,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(m) for i in range(n)],mat,True)
def tree(x,y,z,s,cyprus=False):
 with frame((x,y,z),random.random()*2*pi,scale=s):
  if cyprus:
   beam((0,0,0),(.2,.1,12),.3,'Bark',10,.06)
   for k in range(8):tuft((.1*sin(k),.1*cos(k),3+k), (1.15*(1-k/12),1.1*(1-k/12),2.1),'Foliage',random.randrange(10000))
  else:
   beam((0,0,0),(.7,.3,8),.4,'Bark',12,.22)
   for k in range(9):
    a=2*pi*k/9;bx,by=.7+3.6*cos(a),.3+3.6*sin(a);h=random.uniform(8,10.5)
    beam((.5,.2,5.5),(bx,by,h),.17,'Bark',8,.06)
    for j in range(7):
     aa=2*pi*j/7;tuft((bx+1.6*cos(aa),by+1.6*sin(aa),h+random.uniform(-.3,.6)),(2,1.8,1.25),random.choice(['Foliage','FoliageLight']),random.randrange(10000))
with group('22 | Landscape — pines and cypresses'):
 for i in range(210):
  x=random.uniform(-530,530);y=random.uniform(-470,490)
  if (x/155)**2+(y/138)**2<1:continue
  if -330<x<-100 and -40<y<84:continue
  if 145<x<270 and -48<y<70:continue
  if -380<x<-178 and -318<y<-143:continue
  if -90<x<165 and 200<y<385:continue
  if random.random()<.3:continue
  tree(x,y,ground(x,y),random.uniform(.85,1.5),i%3==0)
 for i in range(12):
  tree(-313+i*7,-187,24.4,.77,True)
 for x,y in [(-161,-108),(-169,-125),(-188,-134),(118,127),(134,126),(151,134),(-334,92),(-347,107)]:tree(x,y,ground(x,y),1.15,False)
# Distant ridge silhouettes soften the horizon, not visible modern mountains.
with group('23 | Landscape — distant horizon'):
 for i in range(18):
  t=2*pi*i/18;tuft((1400*cos(t),1400*sin(t),-18),(350,300,random.uniform(45,95)),'Foliage',i)
flush()
print('ALL GEOMETRY FLUSHED',flush=True)

# Numerals over the public entrances. Four axial ceremonial entrances stay unnumbered.
def roman(n):
 vals=[(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IIII'),(1,'I')];s=''
 for v,c in vals:
  while n>=v:s+=c;n-=v
 return s
col=bpy.data.collections.new('24 | Epigraphy');SC.collection.children.link(col)
for i in range(80):
 if i%20==0:continue
 t=(i+.5)*2*pi/80;m=bayframe(94.59,78.09,t,8.42);tt=Vector((m[0][0],m[1][0],0));nn=Vector((m[0][1],m[1][1],0))
 curve=bpy.data.curves.new('Entrance '+roman(i+1),'FONT');curve.body=roman(i+1);curve.align_x='CENTER';curve.size=.36;curve.extrude=.002;curve.materials.append(G.MATS['ShadowStone'])
 ob=bpy.data.objects.new(curve.name,curve);col.objects.link(ob);ob.matrix_world=Matrix(((tt.x,0,nn.x,m[0][3]),(tt.y,0,nn.y,m[1][3]),(0,1,0,8.42),(0,0,0,1)))
# A gentle repeating billow animates the linen sails without changing rigging.
for ob in bpy.data.objects:
 if ob.type=='MESH' and ob.name.startswith('09 |') and 'Linen' in ob.name:
  ob.shape_key_add(name='Rest');key=ob.shape_key_add(name='Wind through linen')
  for j,v in enumerate(key.data):
   x,y,z=v.co;weight=max(0,sin(pi*min(1,max(0,(49.3-z)/6))))
   v.co.z+=.20*weight*sin(x*.35+y*.2)
  for fr,val in [(1,0),(91,1),(181,0),(271,1),(361,0),(451,1),(541,0),(631,1),(720,0)]:key.value=val;key.keyframe_insert('value',frame=fr)

# Daylight. Real sky texture, an analytic sun, and subtle bounded atmospheric scatter.
world=bpy.data.worlds.new('Mediterranean afternoon');SC.world=world;world.use_nodes=True;n=world.node_tree.nodes;l=world.node_tree.links;bg=n.get('Background');bg.inputs['Strength'].default_value=.55
sky_path=P/'assets/sky.hdr'
if sky_path.exists():
 env=n.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(sky_path));l.new(env.outputs[0],bg.inputs[0]);tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=.7;l.new(tex.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs[0],env.inputs[0])
else:
 sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=.48;sky.sun_rotation=3.9;l.new(sky.outputs[0],bg.inputs[0]);bg.inputs['Strength'].default_value=.2
sun=bpy.data.lights.new('Late afternoon sun','SUN');sun.energy=3.2;sun.color=(1,.84,.65);sun.angle=.035
ob=bpy.data.objects.new('Late afternoon sun',sun);SC.collection.objects.link(ob);ob.rotation_euler=Vector((.7,.55,-.82)).to_track_quat('-Z','Y').to_euler()
sun.use_shadow=True
try:sun.use_shadow_jitter=False;sun.shadow_maximum_resolution=.10
except:pass
# soft fill into the arena, complementing sky irradiance
area=bpy.data.lights.new('Open sky above the cavea','AREA');area.energy=85000;area.shape='DISK';area.size=145;area.color=(.67,.79,1);ob=bpy.data.objects.new(area.name,area);SC.collection.objects.link(ob);ob.location=(0,0,135)
# Atmosphere in a finite volume, minimal extinction over the close architectural pass.
vol=bpy.data.materials.new('Distant golden air');vol.use_nodes=True;nn=vol.node_tree.nodes;nn.clear();out=nn.new('ShaderNodeOutputMaterial');scat=nn.new('ShaderNodeVolumePrincipled');scat.inputs['Density'].default_value=.00038;scat.inputs['Color'].default_value=(.74,.79,.83,1);scat.inputs['Anisotropy'].default_value=.22;vol.node_tree.links.new(scat.outputs['Volume'],out.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=2,location=(0,0,140));ob=bpy.context.object;ob.name='Atmospheric depth';ob.scale=(1050,1050,170);ob.data.materials.append(vol);ob.display_type='WIRE'

# Single continuous, eased camera flight. Baked once per native output frame.
keys=[
 (1,(-195,-280,118),(-6,0,22),34),
 (145,(-142,-200,70),(-2,-8,26),32),
 (241,(-84,-151,43),(0,-30,29),30),
 (361,(-12,-119,29),(14,-40,29),29),
 (457,(62,-108,40),(0,-14,24),29),
 (565,(114,-48,78),(-5,0,18),28),
 (720,(74,72,124),(-13,-11,12),29)]
camd=bpy.data.cameras.new('Cinema camera');cam=bpy.data.objects.new('Cinema camera',camd);SC.collection.objects.link(cam);SC.camera=cam;camd.sensor_width=36;camd.clip_end=3500;camd.clip_start=.1;camd.dof.use_dof=False
# Catmull-Rom with time-aware Hermite tangents gives continuous, unhurried motion.
def interp(f,component):
 i=next((j for j in range(len(keys)-1) if keys[j][0]<=f<=keys[j+1][0]),len(keys)-2);a=keys[i];b=keys[i+1];dt=b[0]-a[0];u=(f-a[0])/dt
 def val(k):q=keys[k][component];return Vector(q) if isinstance(q,tuple) else q
 p0=val(i);p1=val(i+1);m0=(p1-val(max(0,i-1)))/(keys[i+1][0]-keys[max(0,i-1)][0]);m1=(val(min(len(keys)-1,i+2))-p0)/(keys[min(len(keys)-1,i+2)][0]-keys[i][0])
 return (2*u**3-3*u*u+1)*p0+(u**3-2*u*u+u)*dt*m0+(-2*u**3+3*u*u)*p1+(u**3-u*u)*dt*m1
for f in range(1,721):
 pos=interp(f,1);target=interp(f,2);cam.location=pos;cam.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler();camd.lens=interp(f,3);cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f);camd.keyframe_insert('lens',frame=f)
for action in bpy.data.actions:
 try:
  for fc in action.fcurves:
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 except:pass
SC.frame_start=1;SC.frame_end=720;SC.render.fps=24;SC.render.resolution_x=1920;SC.render.resolution_y=1080;SC.render.resolution_percentage=100
SC.render.engine='CYCLES' if '--cycles' in sys.argv else 'CYCLES'
SC.cycles.samples=24;SC.cycles.use_denoising=True;SC.cycles.adaptive_threshold=.07
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 SC.cycles.device='GPU'
except:pass
SC.cycles.max_bounces=5;SC.cycles.diffuse_bounces=3;SC.cycles.glossy_bounces=3;SC.cycles.transmission_bounces=3;SC.cycles.volume_bounces=0
SC.render.image_settings.file_format='PNG';SC.render.image_settings.color_mode='RGB';SC.render.image_settings.color_depth='8';SC.render.image_settings.compression=20
SC.render.film_transparent=False;SC.view_settings.view_transform='AgX';SC.view_settings.look='AgX - Medium High Contrast';SC.view_settings.exposure=.35
SC.render.use_persistent_data=True
SC['Scene']='AMPhitheatrum — Rome circa AD 160';SC['Reconstruction']='Evidence-based proportions; missing ornament, colors, awning design and secondary city fabric are interpretive.';SC['Native frames']=720
# The project opens on the establishing composition.
SC.frame_set(1)
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
# Save source and packed texture data before any render.
bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
(P/'shot_manifest.json').write_text(json.dumps({'fps':24,'frames':720,'size':[1920,1080],'keyframes':keys},indent=2))
print('BUILD COMPLETE',len(bpy.data.objects),'objects',flush=True)
if '--preview' in sys.argv:
 SC.render.resolution_percentage=50;SC.cycles.samples=16
 for f in [1,350,650]:
  SC.frame_set(f);SC.render.filepath=str(P/f'previews/test_{f:04d}.png');t=time.time();bpy.ops.render.render(write_still=True);print('PREVIEW',f,time.time()-t,flush=True)
