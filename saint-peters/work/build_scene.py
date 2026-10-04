import bpy, math, random, os, sys
from mathutils import Vector
from math import sin,cos,pi,sqrt
ROOT='/Users/lucaschu/Documents/Codex/2026-09-04/make'
random.seed(19)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for datablock in bpy.data.materials: bpy.data.materials.remove(datablock)

def material(name,color,rough=.65,metal=0,noise=False):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if noise:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=2.5;tex.inputs['Detail'].default_value=4;tex.inputs['Roughness'].default_value=.72
  coord=n.new('ShaderNodeTexCoord');l.new(coord.outputs['Object'],tex.inputs['Vector'])
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*(v*.68 for v in color),1);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(*(min(1,v*1.13) for v in color),1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
  fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=65;fine.inputs['Detail'].default_value=2;l.new(coord.outputs['Object'],fine.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.23;b.inputs['Distance'].default_value=.028;l.new(fine.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
 return m
stone=material('Travertine | warm ivory, mineral pores',(.66,.60,.47),noise=True)
trim=material('Carved pale travertine',(.77,.72,.61),noise=True)
aged=material('Recessed and weathered limestone',(.42,.39,.31),noise=True)
lead=material('Dome | weathered lead',(.25,.285,.28),.49,.35,True)
gold=material('Gilded bronze',(.58,.37,.09),.3,.72)
dark=material('Deep portal shadow',(.026,.029,.026))
glass=material('Old window glass',(.10,.16,.19),.24,.3)
roof=material('Roman terracotta roofs',(.30,.14,.085),noise=True)
paving=material('Sampietrini basalt',(.20,.205,.20),noise=True)
water=material('Fountain water',(.16,.24,.23),.17,.2)
water.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.25
spray=material('Sunlit fine water',(.60,.70,.70),.19,.15)
green=material('Umbrella pine canopy',(.09,.15,.065),noise=True)
trunk=material('Pine bark',(.17,.12,.075),noise=True)
plasters=[material('Roman plaster '+str(i),c,noise=True) for i,c in enumerate([(.62,.49,.33),(.72,.64,.49),(.56,.40,.25),(.70,.56,.40),(.57,.51,.41)])]
# Basalt blocks, in real metre coordinates.
n=paving.node_tree.nodes;l=paving.node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');brick=n.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=.32;brick.inputs['Row Height'].default_value=.23;brick.inputs['Mortar Size'].default_value=.009;brick.inputs['Color1'].default_value=(.19,.20,.195,1);brick.inputs['Color2'].default_value=(.30,.29,.26,1);brick.inputs['Mortar'].default_value=(.09,.09,.085,1);l.new(tc.outputs['Object'],brick.inputs['Vector']);l.new(brick.outputs['Color'],p.inputs['Base Color']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.42;b.inputs['Distance'].default_value=.025;l.new(brick.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
# Geometry batches retain clear architectural collections without thousands of draw calls.
batches={}; group='Site'
def mesh(v,f,mat,smooth=False):
 key=(group,mat.name,smooth)
 if key not in batches:batches[key]=[[],[]]
 vv,ff=batches[key];off=len(vv);vv.extend(v);ff.extend([tuple(i+off for i in face) for face in f])
def box(c,s,mat=stone,ang=0):
 x,y,z=c;a,b,h=[v/2 for v in s];v=[]
 for zz in [-h,h]:
  for xx,yy in [(-a,-b),(a,-b),(a,b),(-a,b)]:v.append((x+xx*cos(ang)-yy*sin(ang),y+xx*sin(ang)+yy*cos(ang),z+zz))
 mesh(v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
def lathe(c,prof,mat=stone,n=32):
 x,y,z=c;v=[(x+r*cos(j*2*pi/n),y+r*sin(j*2*pi/n),z+h) for r,h in prof for j in range(n)];f=[]
 for k in range(len(prof)-1):
  for j in range(n):a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
 f.extend([tuple(range(n-1,-1,-1)),tuple((len(prof)-1)*n+j for j in range(n))]);mesh(v,f,mat,True)
def sphere(c,s,mat=stone,n=12,rings=8):
 x,y,z=c;v=[]
 for i in range(rings+1):
  a=pi*i/rings
  for j in range(n):t=2*pi*j/n;v.append((x+s[0]*sin(a)*cos(t),y+s[1]*sin(a)*sin(t),z+s[2]*cos(a)))
 mesh(v,[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(rings) for j in range(n)],mat,True)
def tube(points,r,mat=trim,n=8):
 v=[]
 for i,pt in enumerate(points):
  p=Vector(pt);d=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);d.normalize();u=d.cross(Vector((0,0,1)))
  if u.length<.01:u=d.cross(Vector((0,1,0)))
  u.normalize();w=d.cross(u)
  for j in range(n):v.append(tuple(p+r*(u*cos(2*pi*j/n)+w*sin(2*pi*j/n))))
 mesh(v,[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(points)-1) for j in range(n)],mat,True)
def beam(a,b,width,mat=trim):tube([a,b],width,mat,8)
def ring(c,r,zthick,width,mat=trim,n=96):lathe(c,[(r-width/2,0),(r+width/2,0),(r+width/2,zthick),(r-width/2,zthick),(r-width/2,0)],mat,n)
def column(x,y,z,h,r,corinth=False):
 prof=[(r*1.32,0),(r*1.32,.035*h),(r*1.14,.045*h),(r*1.13,.062*h),(r,.08*h),(r*.97,.13*h),(r*.86,.87*h),(r*.87,.90*h),(r*.99,.915*h),(r*.99,.93*h),(r*1.21,.97*h),(r*1.28,h)]
 lathe((x,y,z),prof,stone,28);box((x,y,z+h*.99),(r*2.8,r*2.8,h*.03),trim)
 if corinth:
  for row in range(2):
   for j in range(8):
    a=2*pi*(j+row*.5)/8
    # tiered acanthus foliage, curled tips, alternating leaf lobes
    cx=x+r*.97*cos(a);cy=y+r*.97*sin(a);cz=z+h*(.90+row*.028)
    sphere((cx,cy,cz),(r*.30,r*.30,h*.028),trim,8,6)
    beam((cx,cy,cz-h*.021),(x+r*1.22*cos(a),y+r*1.22*sin(a),cz+h*.018),r*.085,trim)
  for a in [pi/4,3*pi/4,5*pi/4,7*pi/4]:sphere((x+r*1.17*cos(a),y+r*1.17*sin(a),z+h*.966),(r*.23,r*.23,r*.21),trim)
def statue(x,y,z,h,seed=0,angle=0):
 rng=random.Random(seed);w=h*.16;depth=h*.105
 # Individually varied drapery silhouette and folds.
 v=[];nr=24;nz=17;lean=rng.uniform(-.08,.08)*h
 for k in range(nz):
  t=k/(nz-1); ww=(.95 if t<.12 else .82 if t<.42 else .68 if t<.58 else 1.02 if t<.84 else .62)*w
  for j in range(nr):
   a=2*pi*j/nr;rr=1+.085*sin(a*9+t*8+seed)+.035*cos(a*15-t*5);xx=ww*cos(a)*rr+lean*t;yy=depth*sin(a)*rr
   v.append((x+xx*cos(angle)-yy*sin(angle),y+xx*sin(angle)+yy*cos(angle),z+h*(.06+t*.76)))
 mesh(v,[(k*nr+j,k*nr+(j+1)%nr,(k+1)*nr+(j+1)%nr,(k+1)*nr+j) for k in range(nz-1) for j in range(nr)],trim,True)
 sphere((x+lean,y,z+h*.9),(h*.082,h*.073,h*.112),trim,16,12)
 sphere((x+lean,y+h*.065,z+h*.905),(h*.022,h*.027,h*.026),trim,8,6)
 for side in [-1,1]:
  a=(x+side*w*.8,y,z+h*.75);bb=(x+side*w*1.30,y+h*.03,z+h*(.59 if side<0 else .69));cc=(x+side*w*(.6 if side<0 else 1.48),y+h*.09,z+h*(.55 if side<0 else .80))
  tube([a,bb,cc],h*.053,trim,10);sphere(cc,(h*.039,h*.031,h*.05),trim)
  sphere((x+side*w*.45,y+h*.06,z+h*.035),(h*.055,h*.09,h*.035),trim)
 if seed%3==0:beam((x+w*1.5,y+h*.1,z+h*.34),(x+w*1.5,y+h*.1,z+h*1.12),h*.013,gold if seed==999 else trim)
 if seed%7==0:beam((x+w*1.15,y+h*.1,z+h*1.02),(x+w*1.85,y+h*.1,z+h*1.02),h*.014,trim)
def balustrade(a,b,z,spacing=.85,h=1.25):
 d=Vector(b)-Vector(a);length=d.length;num=max(2,int(length/spacing));ang=math.atan2(d.y,d.x);mid=(Vector(a)+Vector(b))/2
 box((mid.x,mid.y,z+h),(length,.4,.2),trim,ang);box((mid.x,mid.y,z+.08),(length,.45,.16),trim,ang)
 for i in range(num+1):
  p=Vector(a)+d*i/num
  lathe((p.x,p.y,z),[(.12,0),(.12,.18),(.09,.3),(.16,.49),(.14,.68),(.07,h-.2),(.13,h)],trim,8)
def frontshape(x,y,z,w,h,mat=dark,arch=True):
 v=[(x-w/2,y,z),(x+w/2,y,z)]
 if arch:
  for j in range(17):a=j*pi/16;v.append((x+w/2*cos(a),y,z+h-w/2+w/2*sin(a)))
 else:v.extend([(x+w/2,y,z+h),(x-w/2,y,z+h)])
 mesh(v,[tuple(range(len(v)))],mat)
def frame(x,y,z,w,h,arch=False,mat=trim,t=.28):
 for s in [-1,1]:box((x+s*(w/2+t/2),y,z+(h-w/2 if arch else h)/2),(t,.48,h-w/2 if arch else h),mat)
 if arch:
  tube([(x+(w/2+t/2)*cos(a*pi/24),y,z+h-w/2+(w/2+t/2)*sin(a*pi/24)) for a in range(25)],t/2,mat,8)
 else:box((x,y,z+h+t/2),(w+2*t,.5,t),mat)
 box((x,y,z-.12),(w+2*t,.6,.24),mat)
def pediment(x,y,z,w,h):
 mesh([(x-w/2,y,z),(x+w/2,y,z),(x,y,z+h)],[(0,1,2)],stone)
 for yy,r in [(y+.2,.22),(y+.4,.12)]:tube([(x-w/2,yy,z),(x,yy,z+h),(x+w/2,yy,z)],r,trim)
 box((x,y+.15,z),(w+1,.7,.4),trim)
def text_obj(body,loc,size,name):
 cr=bpy.data.curves.new(name,'FONT');cr.body=body;cr.align_x='CENTER';cr.size=size;cr.extrude=.012;cr.space_character=1.12
 try:cr.font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Times New Roman.ttf')
 except:pass
 ob=bpy.data.objects.new(name,cr);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(pi/2,0,pi);ob.data.materials.append(aged)
 return ob
# Ground and plaza
box((0,20,-.65),(20000,20000,1),paving)
box((0,180,-.08),(224,177,.15),paving)
# white travertine spokes and concentric pavements
for r in [8,19,37,58,73]:
 pts=[(r*1.30*cos(i*2*pi/160),180+r*sin(i*2*pi/160),.025) for i in range(161)];tube(pts,.17,trim,4)
for i in range(16):
 a=i*2*pi/16;tube([(9*cos(a),180+9*sin(a),.03),(95*cos(a),180+72*sin(a),.03)],.19,trim,4)
# Basilica steps
for i in range(12):box((0,12-i*.62,.07+i*.125),(99-i*.1,25-i*1.15,.20),trim)
# Obelisk and bronze mounts
group='Square | Vatican obelisk'
for s,z,h in [(8,.2,.4),(6.8,.65,.5),(5,1.3,.8),(3.8,3.0,2.6),(3.4,4.5,.5)]:box((0,180,z),(s,s,h),trim)
for x in [-1.15,1.15]:
 for y in [178.85,181.15]:sphere((x,y,4.85),(.35,.35,.32),gold)
# tapered monolith actual shaft 25.5m
v=[(x,y,z) for z,r in [(5,1.32),(28.5,.70)] for x,y in [(-r,180-r),(r,180-r),(r,180+r),(-r,180+r)]];v.append((0,180,30.5));mesh(v,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,8),(5,6,8),(6,7,8),(7,4,8)],material('Rose granite obelisk',(.46,.34,.26),noise=True))
lathe((0,180,30.5),[(.16,0),(.18,.8)],gold);sphere((0,180,31.5),(.40,.40,.4),gold);beam((0,180,31.7),(0,180,33.5),.075,gold);beam((-.6,180,32.9),(.6,180,32.9),.075,gold)
# Twin fountains with stone profiles and trajectories
for fx in [-50,50]:
 group='Square | '+('Maderno' if fx<0 else 'Bernini')+' fountain'
 lathe((fx,180,.02),[(6.6,0),(6.6,.2),(6.25,.4),(5.7,.46),(5.7,.7),(5.25,.78),(5.2,.4),(0,.4)],trim,96)
 lathe((fx,180,.46),[(0,0),(5.23,0),(5.23,.035)],water,96)
 lathe((fx,180,.55),[(1.7,0),(1.7,.35),(1.2,.48),(.8,1.0),(.72,1.9),(1.2,2.2),(2.9,2.5),(3.2,2.8),(3.2,3.1),(2.8,3.2),(.7,3.2),(.52,3.5),(.5,4.0),(.8,4.2),(1.9,4.55),(2.15,4.8),(1.9,4.95),(.3,5.1),(.24,5.6)],trim,64)
 for j in range(80):
  a=j*2*pi/80;rr=2+random.uniform(-.12,.12)
  tube([(fx+(rr+t*.6)*cos(a),180+(rr+t*.6)*sin(a),5.38-4.9*t*t) for t in [k/12 for k in range(13)]],.015+random.random()*.015,spray,4)
 for j in range(40):
  a=j*2*pi/40;tube([(fx+(3.12+t*1.1)*cos(a),180+(3.12+t*1.1)*sin(a),3.5-3*t*t) for t in [k/10 for k in range(11)]],.024,spray,4)
 for j in range(12):
  a=j*2*pi/12;tube([(fx+t*.8*cos(a),180+t*.8*sin(a),6.1+2.5*t-3.7*t*t) for t in [k/15 for k in range(16)]],.025,spray,5)
# Sweeping colonnade: 4 ranks, 35 stations per hemicycle = 280 plus four terminal columns.
for side in [-1,1]:
 group='Bernini colonnade | '+str(side)
 for j in range(35):
  a=math.radians(-68+136*j/34)
  for row in range(4):
   rx=98+row*3.65;ry=74.5+row*3.65;x=side*rx*cos(a);y=180+ry*sin(a);column(x,y,.30,14.6,1.05)
 for end in [-1,1]:
  a=math.radians(end*68);column(side*103*cos(a),180+79.5*sin(a),.3,14.6,1.05)
 # continuous curved architrave and cornices, separated profiles
 for r1,r2,z,h in [(96.5,111.6,14.9,1),(96,112.1,15.9,.4),(96.8,111.3,16.3,1.25),(95.9,112.2,17.55,.36),(95.5,112.6,17.91,.25)]:
  v=[]
  for k in range(101):
   a=math.radians(-69+138*k/100)
   for r,zz in [(r1,z),(r2,z),(r2,z+h),(r1,z+h)]:v.append((side*r*cos(a),180+(r-23.5)*sin(a),zz))
  f=[]
  for k in range(100):
   for m in range(4):f.append((4*k+m,4*k+(m+1)%4,4*(k+1)+(m+1)%4,4*(k+1)+m))
  mesh(v,f,trim)
 # roof balustrade, 70 statues per arm
 for j in range(70):
  a=math.radians(-68+136*j/69);x=side*98*cos(a);y=180+74.5*sin(a);box((x,y,18.55),(1.1,1.1,.85),trim);statue(x,y,19,3.2,j+(100 if side==1 else 0))
 for j in range(230):
  a=math.radians(-69+138*j/229);x=side*98*cos(a);y=180+74.5*sin(a);lathe((x,y,18.1),[(.11,0),(.12,.2),(.19,.5),(.10,.85),(.12,1.0)],trim,8)
 tube([(side*98*cos(math.radians(-69+138*k/180)),180+74.5*sin(math.radians(-69+138*k/180)),19.15) for k in range(181)],.17,trim)
 # the straight enclosed arms opening onto the trapezoidal forecourt
 a=Vector((side*58,8,0));b=Vector((side*37,109,0));d=b-a;ang=math.atan2(d.y,d.x);mid=(a+b)/2
 box((mid.x,mid.y,8.25),(d.length,9,16),stone,ang)
 box((mid.x,mid.y,16.5),(d.length+1,10.5,.65),trim,ang)
 for k in range(22):
  p=a+d*k/21;box((p.x-side*4,p.y,8),(1.0,2,15),trim)
# Basilica body
group='Basilica | nave and transept'
box((0,-100,22),(82,176,42),stone);box((0,-94,44),(42,180,5),stone)
box((0,-113,22),(144,47,44),stone)
lathe((0,-108,44),[(30,0),(30,8),(27,8.5)],stone,16)
# apse at west
lathe((0,-185,0),[(35,0),(35,49),(33,51)],stone,64)
for xx in [-41,41]:
 for yy in range(-175,-15,14):
  box((xx,yy,20),(2.5,4,37),trim)
  box((xx,yy,42),(4,5,1),trim)
for xx in [-25,25]:box((xx,-84,45),(4,165,1),trim)
# roof shallow pitched nave
mesh([(-24,-185,46),(24,-185,46),(0,-185,53),(-24,-10,46),(24,-10,46),(0,-10,53)],[(0,3,5,2),(2,5,4,1)],lead)
# facade, main backing plane and articulated frontage
group='Maderno façade'
box((0,-3,23.5),(116,10,44),stone)
# rustication courses, fine recessed joints
for z in [2+i*1.15 for i in range(39)]:box((0,2.015,z),(115,.025,.035),aged)
# outer pilasters
for xx in [-56,-44,-27,-16,-10,10,16,27,44,56]:
 box((xx,2.5,16),(2.8,1.0,28),trim)
# portals and deep windows, precisely spaced façade bays
for idx,xx in enumerate([-48,-33,-23,-7,0,7,23,33,48]):
 w=6.4 if abs(xx)==48 else 4.5 if abs(xx) in [33,0] else 3.3
 h=14.0 if abs(xx)==48 else 9.8 if abs(xx) in [33,0] else 7.8
 frontshape(xx,2.56,1.6,w,h,dark,abs(xx)==48 or abs(xx)==7);frame(xx,2.83,1.6,w,h,abs(xx)==48 or abs(xx)==7,t=.32)
 if abs(xx)!=48:
  for dx in [-w*.35,0,w*.35]:box((xx+dx,2.68,5.2),(.07,.09,6.6),gold)
  box((xx,2.72,6.8),(w,.12,.13),gold)
  frontshape(xx,2.60,19.4,w*.93,7.7,glass,True);frame(xx,2.87,19.4,w*.93,7.7,True,t=.28)
  for dx in [-.32,0,.32]:box((xx+dx*w,2.9,22.5),(.065,.09,6.1),trim)
  for zz in [20,21.3,22.6,23.9,25.2]:box((xx,2.9,zz),(w*.90,.08,.06),trim)
  pediment(xx,2.85,27.55,w+1,1.2)
  box((xx,3.25,18.9),(w+1.1,2,.40),trim)
  balustrade((xx-w*.55,4.1,0),(xx+w*.55,4.1,0),19,.6,1)
  if xx in [-33,0,33]:
   box((xx,2.8,14.7),(w+.6,.6,2.5),trim);box((xx,3.13,14.7),(w,.08,1.95),aged)
# colossal Corinthian order
for xx in [-54,-40,-29,-13,-9,9,13,29,40,54]:column(xx,4,1.8,27.48,1.385,True)
# layered entablature
for z,h,depth in [(29.5,.5,4),(30.1,.7,4.6),(31.5,2.1,3.5),(33,.35,4.5),(33.5,.4,5.0),(34.1,.55,5.8)]:box((0,2,z),(117,depth,h),trim if h<1 else stone)
for xx in range(-57,58):box((xx,4.4,33.55),(.4,.65,.3),trim)
ob=text_obj('IN HONOREM PRINCIPIS APOST · PAVLVS V BVRGHESIVS ROMANVS PONT MAX · AN MDCXII · PONT VII',(0,4.05,31),1.28,'Dedication in carved Roman capitals')
# upper attic and pediment
for xx in [-55,-40,-29,-16,16,29,40,55]:box((xx,2.6,39.3),(1.4,1.1,9.5),trim)
for xx in [-47,-34,-23,-10,10,23,34,47]:
 frontshape(xx,2.62,36.2,3.2,4.1,dark,False);frame(xx,2.9,36.2,3.2,4.1,False,t=.32)
 if abs(xx)==23:pediment(xx,3,40.8,5.2,1.6)
pediment(0,5.0,34.8,30,7.5)
# papal coat of arms relief
sphere((0,5.35,37.3),(1.1,.25,1.55),trim,16,12)
for dx in [-.65,.65]:beam((dx-1,5.7,36.5),(-dx+1,5.7,38.5),.13,trim)
for z,w in [(44.2,117),(44.7,118),(45.15,118.6)]:box((0,2.1,z),(w,6,.35),trim)
balustrade((-57,4,0),(57,4,0),45.4,.60,1.3)
for j,xx in enumerate([-55,-40,-29,-18,-12,-6,0,6,12,18,29,40,55]):
 box((xx,4,46.1),(2.1,2,1.4),trim);statue(xx,4,46.8,6 if xx==0 else 5.65,999 if xx==0 else j+230)
# twin clock faces, radial markers and ornamental crowns
for xx in [-47.5,47.5]:
 sphere((xx,3.3,48.8),(3.2,.65,3.5),trim,24,16)
 # face disc in x-z plane
 v=[(xx,4.02,48.8)]+[(xx+2.5*cos(j*2*pi/64),4.03,48.8+2.5*sin(j*2*pi/64)) for j in range(64)];mesh(v,[(0,j+1,(j+1)%64+1) for j in range(64)],trim)
 tube([(xx+2.57*cos(j*2*pi/64),4.08,48.8+2.57*sin(j*2*pi/64)) for j in range(65)],.12,gold)
 for j in range(12):
  a=j*2*pi/12;beam((xx+2*cos(a),4.12,48.8+2*sin(a)),(xx+2.32*cos(a),4.12,48.8+2.32*sin(a)),.065,dark)
 beam((xx,4.15,48.8),(xx-.7,4.15,50),.08,dark);beam((xx,4.15,48.8),(xx+1.6,4.15,49.1),.06,dark)
 sphere((xx,3.5,52.3),(1,.6,1),trim);beam((xx,3.5,52.8),(xx,3.5,54.4),.08,gold);beam((xx-.5,3.5,54),(xx+.5,3.5,54),.07,gold)
# drum, dome, ribs, lantern

def dome(cx,cy,base,r,height,main=False):
 global group
 dr=height*.32; shell=height*.49
 lathe((cx,cy,base),[(r*1.13,0),(r*1.13,1),(r,1.3),(r,dr-.6),(r*1.08,dr),(r*1.08,dr+1),(r,dr+1.4)],stone,96 if main else 48)
 n=16 if main else 12
 for j in range(n):
  a=j*2*pi/n
  # drum window as dark plane, vertical rectangle oriented tangentially
  rr=r*1.012;wx=cx+rr*cos(a);wy=cy+rr*sin(a);tang=a+pi/2
  box((wx,wy,base+dr*.56),(r*.23,.1,dr*.56),dark,tang)
  for s in [-1,1]:
   aa=a+s*.09;column(cx+r*1.04*cos(aa),cy+r*1.04*sin(aa),base+1.5,dr-1.9,r*.047,main)
  # cornice above opening
  box((cx+r*1.04*cos(a),cy+r*1.04*sin(a),base+dr*.89),(r*.29,1,.5),trim,tang)
 prof=[]
 for k in range(49):
  t=k/48;rr=r*(cos(t*pi/2)**.83)*.99;zz=base+dr+1.1+shell*sin(t*pi/2)
  prof.append((max(rr,r*.125),zz-base))
 lathe((cx,cy,base),prof,lead,128 if main else 64)
 for j in range(n):
  a=j*2*pi/n;tube([(cx+rr*cos(a),cy+rr*sin(a),base+zz+.16) for rr,zz in prof[:-3]],r*.024,trim,8)
  if main:
   # two rows of small dormers on shell
   for t in [.23,.48]:
    a=(j+.5)*2*pi/n
    k=int(t*48);rr,zz=prof[k];px=cx+(rr+.3)*cos(a);py=cy+(rr+.3)*sin(a)
    sphere((px,py,base+zz),(.95,.95,1.4),trim)
    box((px+1.0*cos(a),py+1.0*sin(a),base+zz),(.8,.12,1.2),dark,a+pi/2)
 # fine horizontal lead seams
 for k in range(5,45,4):
  rr,zz=prof[k];ring((cx,cy,base+zz),rr,.045,.065,aged,96)
 top=base+dr+1.1+shell
 lr=r*.155;lh=height*.12
 lathe((cx,cy,top),[(lr*1.3,0),(lr*1.3,.6),(lr,.9),(lr,lh),(lr*1.3,lh+.4)],trim,48)
 for j in range(12):
  a=j*2*pi/12
  box((cx+lr*1.01*cos(a),cy+lr*1.01*sin(a),top+lh*.5),(lr*.36,.12,lh*.65),dark,a+pi/2)
  column(cx+lr*1.09*cos(a),cy+lr*1.09*sin(a),top+.7,lh-.5,lr*.13)
 lathe((cx,cy,top+lh+.4),[(lr*1.23,0),(lr*.9,1),(lr*.6,2),(lr*.32,3),(lr*.18,4)],lead,48)
 sphere((cx,cy,top+lh+4.9),(lr*.3,lr*.3,lr*.3),gold)
 beam((cx,cy,top+lh+5.4),(cx,cy,top+lh+7.3),.10 if main else .05,gold)
 beam((cx-.6,cy,top+lh+6.6),(cx+.6,cy,top+lh+6.6),.10 if main else .05,gold)
 if main:
  for j in range(32):
   a=j*2*pi/32;box((cx+r*1.075*cos(a),cy+r*1.075*sin(a),base+dr+.35),(1.2,1.2,.5),trim)
group='Michelangelo dome | ribbed shell, drum and lantern'
dome(0,-108,52,23.6,82,True)
for xx in [-35,35]:
 group='Subsidiary domes';dome(xx,-30,34,9.1,24)
# exterior corner pilasters on crossing
for xx in [-45,45]:
 for yy in [-139,-90]:box((xx,yy,27),(4,5,48),trim)
# Saints Peter and Paul at foot of steps
for j,xx in enumerate([-52,52]):
 group='Forecourt | apostle monuments';box((xx,19,2.3),(3.7,3.4,4.5),stone);box((xx,19,4.65),(4,3.7,.4),trim);statue(xx,19,4.9,5.55,401+j)
# Apostolic Palace, Vatican wings, Rome context

def building(x,y,w,d,h,mat,detail=True):
 box((x,y,h/2),(w,d,h),mat);box((x,y,h-.3),(w+1,d+1,.8),trim)
 # pitched tiled roof
 mesh([(x-w/2-1,y-d/2-1,h),(x+w/2+1,y-d/2-1,h),(x+w/2+1,y+d/2+1,h),(x-w/2-1,y+d/2+1,h),(x,y-d/2-1,h+3.5),(x,y+d/2+1,h+3.5)],[(0,1,4),(0,4,5,3),(4,1,2,5),(3,5,2)],roof)
 if detail:
  for zz in range(5,int(h)-2,5):
   box((x,y+d/2+.03,zz-1.9),(w,.22,.22),trim)
   for xx in range(int(-w/2)+3,int(w/2)-2,5):
    box((x+xx,y+d/2+.08,zz),(1.45,.12,2.4),dark);box((x+xx,y+d/2+.18,zz-1.3),(1.8,.35,.2),trim)
   for yy in range(int(-d/2)+3,int(d/2)-2,5):
    for s in [-1,1]:box((x+s*(w/2+.08),y+yy,zz),(.12,1.5,2.4),dark)
 for k in range(max(1,int(w/15))):box((x-w*.3+k*12,y,h+2),(1,1.1,3),mat)
# Georeferenced surrounding building footprints, © OpenStreetMap contributors.
import json
osm=json.load(open(ROOT+'/work/references/vatican_buildings.json'))
group='Vatican and Borgo | OpenStreetMap footprints'
for el in osm['elements']:
 tags=el.get('tags',{});geo=el.get('geometry',[])
 if len(geo)<4 or el['id']==244159210 or 'Colonnato' in tags.get('name',''):continue
 pts=[((p['lat']-41.902165)*111195,(p['lon']-12.455025)*82770) for p in geo[:-1]]
 cx=sum(p[0] for p in pts)/len(pts);cy=sum(p[1] for p in pts)/len(pts)
 if abs(cx)<88 and -230<cy<15:continue
 if abs(cx)<120 and 105<cy<270:continue
 if abs(cx)<62 and 0<cy<115:continue
 if tags.get('building') in ['roof','carport']:continue
 area=abs(sum(pts[k][0]*pts[(k+1)%len(pts)][1]-pts[(k+1)%len(pts)][0]*pts[k][1] for k in range(len(pts))))/2
 if area<12 or area>27000:continue
 rng=random.Random(el['id']);ma=plasters[rng.randrange(len(plasters))]
 try:hh=float(tags.get('height',str(float(tags.get('building:levels','5'))*3.4)).replace(' m',''))
 except:hh=20
 hh=max(5,min(42,hh));N=len(pts)
 verts=[(x,y,z) for z in [0,hh] for x,y in pts]
 mesh(verts,[(k,(k+1)%N,(k+1)%N+N,k+N) for k in range(N)],ma)
 # Raised warm tile rooftop, following the surveyed perimeter.
 mesh([(x,y,hh+.16) for x,y in pts],[tuple(range(N))],roof)
 for k in range(N):
  ax,ay=pts[k];bx,by=pts[(k+1)%N];dx=bx-ax;dy=by-ay;length=sqrt(dx*dx+dy*dy)
  if length<2:continue
  angle=math.atan2(dy,dx);nx=dy/length;ny=-dx/length
  box(((ax+bx)/2,(ay+by)/2,hh-.25),(length,.6,.55),trim,angle)
  if abs(cx)<420 and abs(cy)<550 and length>3:
   for zz in range(4,int(hh)-1,4):
    for k2 in range(max(1,int(length/4.2))):
     t=(k2+.5)/max(1,int(length/4.2));xx=ax+dx*t;yy=ay+dy*t
     # Windows on both sides of wall ensure correct visibility for either polygon winding.
     box((xx,yy,zz),(1.25,.25,2.05),dark,angle)
     box((xx,yy,zz-1.12),(1.65,.46,.19),trim,angle)
  # fine eave shadow at roof edge
  box(((ax+bx)/2,(ay+by)/2,hh+.1),(length,.4,.2),aged,angle)
 # chimneys and roof service forms add the scale of a lived-in city
 if area>180:
  for k in range(min(5,int(area/220))):
   pp=pts[k%N];xx=cx*.35+pp[0]*.65;yy=cy*.35+pp[1]*.65
   box((xx,yy,hh+.8),(.8,1,1.6),ma)

# Multipolygon palaces, including their open internal courtyards.
group='Vatican | mapped palace courtyards'
for rel in json.load(open(ROOT+'/work/references/relations_mesh.json')):
 tags=rel['tags']
 if 'Colonnato' in tags.get('name',''):continue
 rng=random.Random(rel['id']);ma=plasters[rng.randrange(len(plasters))]
 try:hh=float(tags.get('height',str(float(tags.get('building:levels','6'))*3.5)))
 except:hh=24
 if rel['id']==49690:hh=34
 hh=max(8,min(42,hh))
 for tri in rel['triangles']:mesh([(x,y,hh) for x,y in tri],[(0,1,2)],roof)
 for loop in rel['loops']:
  for k in range(len(loop)-1):
   ax,ay=loop[k];bx,by=loop[k+1];dx=bx-ax;dy=by-ay;length=sqrt(dx*dx+dy*dy)
   if length<.05:continue
   mesh([(ax,ay,0),(bx,by,0),(bx,by,hh),(ax,ay,hh)],[(0,1,2,3)],ma)
   ang=math.atan2(dy,dx);box(((ax+bx)/2,(ay+by)/2,hh),(length,.6,.5),trim,ang)
   if length<3:continue
   for zz in range(4,int(hh)-1,4):
    for j in range(max(1,int(length/4.1))):
     t=(j+.5)/max(1,int(length/4.1));xx=ax+dx*t;yy=ay+dy*t
     box((xx,yy,zz),(1.4,.26,2.2),dark,ang);box((xx,yy,zz-1.2),(1.8,.45,.18),trim,ang)

# Vatican gardens / umbrella pines
group='Vatican gardens'
box((-70,-375,-.05),(460,330,.12),green)
for j in range(180):
 x=random.uniform(-290,145);y=random.uniform(-530,-218)
 if x>65 and y>-260:continue
 h=random.uniform(10,17);tube([(x,y,0),(x+.5,y,h*.8)],.4,trunk)
 for k in range(5):
  a=k*2*pi/5;beam((x,y,h*.6),(x+3*cos(a),y+3*sin(a),h),.20,trunk);sphere((x+2.5*cos(a),y+2.5*sin(a),h),(4,4,1.8),green,12,8)
# Small human-scale visitors, restrained numbers (morning).
group='Square | visitors'
cloth=[material('Visitor clothing '+str(i),c) for i,c in enumerate([(.11,.14,.18),(.35,.28,.19),(.55,.50,.41),(.19,.23,.25),(.41,.23,.16)])];skin=material('Skin',(.44,.29,.20))
for j in range(130):
 x=random.uniform(-77,77);y=random.uniform(24,245)
 if (x/88)**2+((y-180)/70)**2>1 and y>110:continue
 h=random.uniform(1.55,1.87);c=random.choice(cloth);sphere((x,y,h*.90),(.115,.11,.15),skin)
 lathe((x,y,h*.38),[(.13,0),(.19,h*.32),(.17,h*.40)],c,8)
 for s in [-1,1]:
  beam((x+s*.08,y,h*.40),(x+s*.13,y+s*.10,.08),.065,c)
  beam((x+s*.18,y,h*.73),(x+s*.23,y+.06,h*.47),.045,c)
# Lamp posts at approach
group='Street furniture'
for side in [-1,1]:
 for yy in [278,318,368,418,468]:
  xx=side*25;lathe((xx,yy,0),[(.3,0),(.3,.5),(.11,.8),(.09,6)],gold,12)
  for dx in [-.8,0,.8]:
   beam((xx,yy,5.4),(xx+dx,yy,6),.065,gold);box((xx+dx,yy,6.25),(.32,.32,.55),trim)
# Curved exterior apses and their lead half-domes.
group='Basilica | articulated apses and roof terraces'
for cx,cy,rr,hh in [(-60,-113,23,45),(60,-113,23,45),(0,-185,35,45)]:
 lathe((cx,cy,0),[(rr,0),(rr,hh),(rr+1,hh+.6),(rr+1,hh+1.1)],stone,64)
 lathe((cx,cy,hh+1),[(rr*cos(k*pi/64),13*sin(k*pi/64)) for k in range(33)],lead,64)
 for j in range(20):
  a=j*2*pi/20;xx=cx+(rr+.25)*cos(a);yy=cy+(rr+.25)*sin(a)
  box((xx,yy,23),(1.7,1.2,40),trim,a+pi/2)
  aa=a+pi/20;xx=cx+(rr+.09)*cos(aa);yy=cy+(rr+.09)*sin(aa)
  box((xx,yy,27),(2.6,.16,8),dark,aa+pi/2)
  box((xx,yy,32),(3.4,.55,.4),trim,aa+pi/2)
for side in [-1,1]:
 for yy in range(-170,-18,12):
  box((side*41.1,yy,27),(.12,3.5,8.5),glass)
  for off in [-2,2]:box((side*41.3,yy+off,27),(.4,.35,9),trim)
  box((side*41.4,yy,31.7),(.7,4.7,.4),trim)
 for zz in [3,15,36,42]:box((side*41.5,-100,zz),(1.2,176,.55),trim)
 # protective rails on nave terrace
 balustrade((side*40,-176,0),(side*40,-12,0),43,.9,1.15)
# Fine coffering below the entablature and rusticated forecourt arms.
for side in [-1,1]:
 a=Vector((side*58,8,0));b=Vector((side*37,109,0));d=b-a;mid=(a+b)/2;ang=math.atan2(d.y,d.x)
 for zz in [1.2,3.5,14.8]:box((mid.x-side*4.6,mid.y,zz),(d.length,.4,.4),trim,ang)
# Architectural bevels catch light at stone corners.

# Material batches -> objects with named architectural collections
for (name,mn,smooth),(v,f) in batches.items():
 col=bpy.data.collections.get(name)
 if col is None:col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
 me=bpy.data.meshes.new(name+' geometry');me.from_pydata(v,[],f);me.materials.append(bpy.data.materials[mn]);me.update();ob=bpy.data.objects.new(name+' • '+mn,me);col.objects.link(ob)
 if not smooth and mn in ['Travertine | warm ivory, mineral pores','Carved pale travertine']:
  mod=ob.modifiers.new('Subtle dressed stone edges','BEVEL');mod.width=.045;mod.segments=2
 if smooth:
  for poly in me.polygons:poly.use_smooth=True
print('GEOMETRY',sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH'),flush=True)
# Atmospheric physical daylight
world=bpy.data.worlds.new('Roman morning sky');world.use_nodes=True;bpy.context.scene.world=world
n=world.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(135);sky.air_density=1.15;sky.aerosol_density=1.5;sky.ozone_density=1;sky.sun_disc=False;bg.inputs['Strength'].default_value=.12;world.node_tree.links.new(sky.outputs[0],bg.inputs['Color']);world.node_tree.links.new(bg.outputs[0],out.inputs[0])
sun_data=bpy.data.lights.new('Morning sun','SUN');sun_data.energy=3.0;sun_data.angle=math.radians(1.8);sun_data.color=(1,.82,.61);sun=bpy.data.objects.new('Morning sun',sun_data);bpy.context.collection.objects.link(sun);sun.rotation_euler=(math.radians(65),0,math.radians(150))
# Camera shots, sample every frame for deterministic eased motion and perfect look-at.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
try:
 pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
 for d in pref.devices:d.use=d.type=='METAL'
 scene.cycles.device='GPU'
except Exception as e:print(e)
scene.render.use_persistent_data=True
scene.cycles.adaptive_threshold=.06
scene.cycles.max_bounces=5;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100;scene.render.fps=24;scene.frame_start=1;scene.frame_end=720
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.10
scene.render.image_settings.color_depth='8'
scene.render.use_file_extension=True
ng=bpy.data.node_groups.new('Roman atmosphere','CompositorNodeTree');scene.compositing_node_group=ng
ng.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
cn=ng.nodes;cl=ng.links;cn.clear()
rl=cn.new('CompositorNodeRLayers');mix=cn.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MIX';mix.inputs[7].default_value=(.40,.46,.49,1)
scene.view_layers[0].use_pass_mist=True
world.mist_settings.start=140;world.mist_settings.depth=1100;world.mist_settings.falloff='QUADRATIC'
mult=cn.new('ShaderNodeMath');mult.operation='MULTIPLY';mult.inputs[1].default_value=.7
cl.new(rl.outputs['Mist'],mult.inputs[0]);cl.new(mult.outputs[0],mix.inputs[0]);cl.new(rl.outputs['Image'],mix.inputs[6])
comp=cn.new('NodeGroupOutput');cl.new(mix.outputs[2],comp.inputs[0])
# Three purposeful movements; no titles and no artificial transition effects.
shots=[('01 · The embrace',1,240,(130,450,215),(92,395,180),(0,100,26),(0,85,38),26),('02 · Stone and water',241,480,(71,229,10),(62,204,12),(-7,0,36),(-4,0,43),26),('03 · Above the saints',481,720,(86,30,95),(100,-24,116),(0,-102,100),(0,-114,100),28)]
for name,start,end,pa,pb,ta,tb,lens in shots:
 data=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(cam);data.lens=lens;data.clip_end=3000;data.clip_start=.3;data.dof.use_dof=False
 for fr in range(start,end+1):
  t=(fr-start)/(end-start);t=t*t*(3-2*t)*.35+t*.65
  cam.location=Vector(pa).lerp(Vector(pb),t);target=Vector(ta).lerp(Vector(tb),t);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=fr);cam.keyframe_insert('rotation_euler',frame=fr)
 marker=scene.timeline_markers.new(name,frame=start);marker.camera=cam
 if start==1:scene.camera=cam
# Metadata and readable scene brief inside blend file.
text=bpy.data.texts.new('READ ME — scene and sources');text.write(open(ROOT+'/work/scene_brief.md').read())
scene['duration_seconds']=30;scene['reconstruction_note']='Architecturally referenced procedural reconstruction. Sculpture and city blocks approximated; not a survey or photogrammetry model.'
scene.render.filepath=ROOT+'/work/frames/'
scene.frame_set(1)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/outputs/Saint_Peters_Basilica.blend')
# Endpoint checks in the video renderer.
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=8;scene.eevee.use_fast_gi=True;scene.eevee.fast_gi_quality=.25;scene.eevee.fast_gi_ray_count=2;scene.eevee.fast_gi_step_count=8
sun.data.use_shadow_jitter=False
scene.render.resolution_percentage=40
for fr in [1,240,241,480,481,720]:
 scene.frame_set(fr);scene.render.filepath=ROOT+'/work/check_'+str(fr)+'.png';bpy.ops.render.render(write_still=True)
