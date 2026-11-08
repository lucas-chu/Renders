# Build with Blender 5.x: blender -b -P build.py
import bpy, math, random, os
from mathutils import Vector
from math import sin,cos,pi
from pathlib import Path
D=Path(__file__).resolve().parent
random.seed(1527)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
def mat(name,code,metal=0,rough=.7,emit=0):
 rgb=tuple(((int(code[i:i+2],16)/255+.055)/1.055)**2.4 for i in (0,2,4))
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emit:p.inputs['Emission Color'].default_value=(*rgb,1);p.inputs['Emission Strength'].default_value=emit
 return m
stone=mat('Travertine | honey','C2A086'); ivory=mat('Limestone | pale edges','E0C7A5');shade=mat('Weathered blocks','937665');brick=mat('Roman brick','995E4A');roof=mat('Burnished terracotta','AA543C');wood=mat('Walnut','52392C');oak=mat('Oiled ash','906244');deep=mat('Deep arcade','2D2B2C');red=mat('Madder silk','9E2432');blue=mat('Indigo wool','25465C');gold=mat('Gold embroidery','DFAB51',.35);brass=mat('Aged bronze','94774D',.62);steel=mat('Hammered steel','88939A',.67,.32);darksteel=mat('Blued armour','45505A',.65);skin=mat('Warm skin','CA9673');hair=mat('Beard and shoes','49362F');white=mat('Ivory linen','EFE2C2');mud=mat('Warm paving','9E8778');orange=mat('Embers','FFAB46',0,.5,3);black=mat('Imperial charcoal','38383C');olive=mat('Olive broadcloth','66634E');vermilion=mat('Oxide red','A14730');tiles=[mat('Stone %d'%i,c) for i,c in enumerate(['AA9685','AE9988','AC9383','B49E8D','A38B7B'])]; pine=mat('Cypress foliage','465343')
# Batch by semantic object; reusable figure geometry, with separate articulated upper bodies.
col=None
def group(n):
 global col
 col=bpy.data.collections.new(n);s.collection.children.link(col)
class Batch:
 def __init__(self):self.v=[];self.f=[];self.mi=[];self.ms=[]
 def poly(self,pts,faces,m):
  a=len(self.v);self.v.extend(pts)
  if m not in self.ms:self.ms.append(m)
  j=self.ms.index(m)
  for f in faces:self.f.append(tuple(a+k for k in f));self.mi.append(j)
 def box(self,c,sz,m):
  x,y,z=c;a,b,h=[v/2 for v in sz];self.poly([(x+i*a,y+j*b,z+k*h) for k in (-1,1) for j in (-1,1) for i in (-1,1)],[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],m)
 def tube(self,a,b,r,t,m,n=10):
  a,b=Vector(a),Vector(b);w=(b-a).normalized();u=w.cross(Vector((0,1,0)) if abs(w.y)<.85 else Vector((1,0,0))).normalized();v=w.cross(u);self.poly([tuple(p+h*(u*cos(i*2*pi/n)+v*sin(i*2*pi/n))) for p,h in [(a,r),(b,t)] for i in range(n)],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],m)
 def egg(self,c,r,m,n=12):
  x,y,z=c;a,b,h=r;q=8;self.poly([(x+a*cos(i*2*pi/n)*sin(j*pi/q),y+b*sin(i*2*pi/n)*sin(j*pi/q),z+h*cos(j*pi/q)) for j in range(q+1) for i in range(n)],[(j*n+i,(j+1)*n+i,(j+1)*n+(i+1)%n,j*n+(i+1)%n) for j in range(q) for i in range(n)],m)
 def finish(self,n):
  me=bpy.data.meshes.new(n);me.from_pydata(self.v,[],self.f);me.materials.clear()
  for m in self.ms:me.materials.append(m)
  me.polygons.foreach_set('material_index',self.mi);me.update();o=bpy.data.objects.new(n,me);col.objects.link(o);return o
def arch(B,x,y,z,r,th,depth,m):
 for i in range(15):
  a=i*pi/15+.003;b=(i+1)*pi/15-.003
  B.poly([(x+cos(t)*h,y+v,z+sin(t)*h) for v in (-depth/2,depth/2) for h,t in [(r,a),(r+th,a),(r+th,b),(r,b)]],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],ivory if i==7 else m)
def gable(B,x,y,z,w,l,h,m):
 B.poly([(x+i*w/2,y+j*l/2,z+k*h) for j in [-1,1] for i,k in [(-1,0),(1,0),(0,1)]],[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],m)
def cross(B,x,y,z,sz,m):
 B.box((x,y,z),(sz*.13,sz*.12,sz),m);B.box((x,y,z+sz*.18),(sz*.6,sz*.12,sz*.13),m)
group('01 • Old Saint Peter’s / fabric and works')
B=Batch();B.box((0,0,-.37),(280,280,.68),mud)
for j in range(55):
 for i in range(52):
  x=(i-26)*1.2+(j%2)*.6;y=(j-29)*.83;B.box((x,y,-.041+random.uniform(0,.005)),(1.19,.82,.08),random.choice(tiles))
# nave, aisles, narthex and medieval campanile
B.box((0,29,6.9),(19,22,13.8),stone);gable(B,0,29,13.8,19.8,23,4.4,roof)
for side in [-1,1]:
 B.box((side*12,29,4),(5.8,22,8),shade);gable(B,side*12,29,8,6.2,22.6,1.75,roof)
for x in [-6,-3,0,3,6]:
 B.box((x,17.95,10.5),(1.22,.18,2.65),deep);arch(B,x,17.78,11.82,.63,.18,.2,ivory)
 for u in [-.32,0,.32]:B.box((x+u,17.75,10.6),(.07,.12,2.6),brass)
for i in range(8):B.box((0,11+i*.41,.09+i*.13),(30-i*.12,1,.18+i*.22),ivory)
B.box((0,15.95,1.05),(30,3.3,.3),stone)
for x in range(-14,15,4):
 B.tube((x,14.6,1),(x,14.6,5.25),.4,.34,stone,18);B.box((x,14.6,1.36),(1,1,.3),ivory);B.box((x,14.6,5.24),(1.1,1,.35),ivory)
 if x<14:arch(B,x+2,14.6,5.24,1.7,.39,.85,stone)
B.box((0,15.3,7.48),(30,2.8,.49),ivory);gable(B,0,16,7.72,30.2,3.7,.95,roof)
for x in [-8,-4,0,4,8]:B.box((x,17.79,3.8),(2.2,.3,5.4),deep)
cross(B,0,18.1,18.85,1.8,gold)
for z in [5,9.2,13.4,17.6,21.8]:
 B.box((-15.7,22,z-2),(4.1,4.2,4.2),brick);B.box((-15.7,22,z+.08),(4.5,4.6,.28),ivory)
 for x in [-16.6,-15.7,-14.8]:
  B.box((x,19.86,z-1.4),(.55,.16,1.75),deep);arch(B,x,19.75,z-.52,.29,.12,.21,ivory)
gable(B,-15.7,22,22,4.8,4.8,2,roof)
for x,y in [(-10,44),(10,44),(-10,56),(10,56)]:
 B.box((x,y,9),(6,7,18),stone)
 for j in range(8):
  for k in [-1,1]:B.tube((x+k*3.8,y-4,j*3),(x+k*3.8,y-4,j*3+3),.095,.085,wood)
  B.box((x,y-4,j*3+1),(8,.8,.14),oak);B.tube((x-3.8,y-4,j*3),(x+3.8,y-4,j*3+3),.09,.09,wood)
arch(B,0,44,17,7,1.2,3,stone)
for side in [-1,1]:
 for j in range(12):
  x=side*random.uniform(22,35);y=-32+j*5.2;h=random.uniform(5,9);w=random.uniform(4,7)
  B.box((x,y,h/2),(w,5,h),random.choice([stone,brick,shade]));gable(B,x,y,h,w+.6,5.4,1.9,roof)
  for dx in [-1,1]:B.box((x+dx,y-2.52,h-1.8),(.82,.12,1.35),deep)
for i in range(48):
 x=random.choice([-1,1])*random.uniform(33,78);y=random.uniform(-16,74);h=random.uniform(4,9);B.tube((x,y,0),(x,y,h*.7),.19,.14,wood);B.egg((x,y,h*.66),(1,1,h*.5),pine)
B.finish('Borgo • pavers, portico, brick campanile and crossing works')
# articulated pikemen in polychrome carved-figure style
group('02 • Swiss and Imperial companies')
def soldier(guard,variant):
 L=Batch();U=Batch();cloth=(blue if guard else [olive,black,vermilion][variant%3]);sleeve=red if guard else [vermilion,stone,olive][variant%3];accent=gold if guard else ivory
 for k in [-1,1]:
  hip=(.14*k,0,.9);knee=(.20*k,k*.23+.06,.57);foot=(.225*k,k*.38,.12)
  L.tube(hip,knee,.153,.117,cloth);L.tube(knee,foot,.113,.081,sleeve if k==1 else cloth);L.egg((foot[0],foot[1]+.052,.086),(.105,.195,.086),hair)
  L.egg((.15*k,k*.09,.78),(.154,.175,.24),cloth);L.tube((knee[0],knee[1],.49),(knee[0],knee[1],.55),.115,.119,accent)
 U.egg((0,0,1.12),(.266,.17,.34),cloth);U.egg((0,.026,1.29),(.26,.175,.24),darksteel);U.tube((0,0,.965),(0,0,1.04),.212,.214,hair);U.box((0,.215,1.005),(.091,.024,.06),brass)
 U.egg((0,.025,1.64),(.132,.139,.171),skin);U.egg((0,.152,1.63),(.034,.051,.041),skin)
 for k in [-1,1]:U.egg((k*.055,.152,1.675),(.022,.012,.009),hair)
 U.egg((0,.075,1.53),(.107,.097,.068),hair);U.egg((0,.01,1.764),(.163,.169,.126),steel if guard or variant%2 else sleeve);U.egg((0,.026,1.724),(.192,.202,.025),darksteel if guard or variant%2 else cloth)
 U.tube((-.10,-.03,1.78),(-.23,-.12,2.00),.044,.007,accent)
 # Two hands grasp one halberd haft.
 a=Vector((-.34,-.65,.91));d=Vector((.255,1,.43+variant*.135)).normalized()
 for k,h in [(-1,.44),(1,1.13)]:
  hand=a+d*h;shoulder=(k*.249,0,1.40);elbow=(k*.34,.034 if k==-1 else .21,1.12)
  U.tube(shoulder,elbow,.111,.088,sleeve);U.egg((k*.26,.01,1.36),(.15,.146,.137),sleeve)
  for dx in [-.062,.045]:U.tube((k*.26+dx,.129,1.43),(k*.27+dx,.131,1.30),.018,.014,accent)
  U.tube(elbow,hand,.087,.059,cloth);U.egg(hand,(.064,.067,.064),skin)
 tip=a+d*(2.9 if guard else 3.6);U.tube(a-d*.4,tip,.024,.020,oak,8);U.tube(tip,tip+d*.43,.067,.001,steel,5)
 if guard:
  v=Vector((0,-d.z,d.y))*.24;p=tip-d*.16;U.poly([tuple(t) for t in [p-d*.2,p+v-d*.17,p+v*1.32+d*.15,p+d*.09,p-v*.68+d*.15]],[(0,1,2,3),(0,3,4)],steel)
 U.tube((-.19,-.02,.95),(-.34,-.37,.41),.036,.021,hair);U.tube((-.25,.03,1.09),(-.17,-.035,.92),.029,.026,brass)
 return L.finish('Hose | template').data,U.finish('Harness and polearm | template').data
models={}
for g in [True,False]:
 for v in range(4):models[g,v]=soldier(g,v)
for o in list(col.objects):bpy.data.objects.remove(o,do_unlink=True)
def obj(n,data):
 o=bpy.data.objects.new(n,data);col.objects.link(o);return o
def keys(o,prop,vals):
 for f,val in vals:setattr(o,prop,val);o.keyframe_insert(data_path=prop,frame=f)
def man(x,y,z,theta,g,i,active=True):
 root=obj(('Guard' if g else 'Landsknecht')+' %03d'%i,None);root.location=(x,y,z);root.rotation_euler.z=theta;k=random.uniform(.94,1.07);root.scale=(k,)*3
 leg,body=models[g,i%4];l=obj('Footing',leg);l.parent=root;b=obj('Polearm stance',body);b.parent=root
 if active:
  ph=random.random()*6;dt=random.randint(14,23);vals=[(f,(.13*cos(f/dt+ph),.047*sin(f/dt+ph),.105*sin(f/dt+ph))) for f in range(1,368,5)];keys(b,'rotation_euler',vals)
  if not g:keys(root,'location',[(1,(x,y-2.8,z)),(100,(x,y-1.5,z)),(202,(x,y+.16,z)),(360,(x,y+.32,z))])
 return root
for g,rows,cols,cy,theta in [(True,3,9,3,pi),(False,5,12,.0,0)]:
 for j in range(rows):
  for i in range(cols):
   x=(i-(cols-1)/2)*1.16+random.uniform(-.18,.18);y=cy+(j*1.48 if g else -j*1.57)+random.uniform(-.22,.22)
   man(x,y,0,theta+random.uniform(-.19,.19),g,j*cols+i)
group('03 • Silk standards and battle debris')
def flag(x,y,z,theta,swiss):
 B=Batch();B.tube((0,0,0),(0,0,4.4),.042,.028,wood);B.tube((0,0,4.37),(0,0,4.71),.085,0,brass)
 nx,ny=26,16;w,h=2.10,1.44
 for i in range(nx):
  for j in range(ny):
   u=(i+.5)/nx;v=(j+.5)/ny
   m=(white if ((.30<u<.69 and .42<v<.58) or (.445<u<.555 and .22<v<.78)) else red) if swiss else (vermilion if abs(u-v)<.09 or abs(1-u-v)<.09 else gold)
   B.poly([(a*w,.28*a*sin(9*a+b*2)+.09*a*sin(15*a-2*b),4.26-b*h-a*.19+.105*a*sin(8*a+b*1.5)) for a,b in [(i/nx,j/ny),((i+1)/nx,j/ny),((i+1)/nx,(j+1)/ny),(i/nx,(j+1)/ny)]],[(0,1,2,3)],m)
 o=B.finish('Cantonal cross' if swiss else 'Imperial saltire');o.location=(x,y,z);keys(o,'rotation_euler',[(f,(.035*sin(f/22+x),.055*cos(f/31),theta+.075*sin(f/29+y))) for f in range(1,368,8)])
for x,y,t,g in [(-3.9,4.8,.05,1),(2.7,6.4,-.37,1),(-4.4,-4.7,.27,0),(4,-2.7,-.29,0),(.6,-8,.6,0)]:flag(x,y,0,t,g)
B=Batch()
for i in range(38):
 x=random.uniform(-10,10);y=random.uniform(-11,10)
 if abs(x)<4 and y>4:continue
 B.tube((x,y,.043),(x+random.uniform(-1.2,1.2),y+random.uniform(.4,1.4),.046),.023,.018,wood)
for x,y in [(-4.9,1.8),(5.65,-.8),(-3,-7)]:
 B.egg((x,y,.12),(.19,.2,.13),darksteel);B.egg((x,y,.065),(.25,.23,.026),steel)
B.finish('Broken shafts and discarded helmets')
group('04 • Passetto / the escape')
B=Batch();X=108
B.box((X,0,-.12),(6,46,.24),stone)
for side in [-1,1]:
 for j in range(-5,6):
  y=j*4;B.box((X+side*2.5,y,2.2),(.7,2.9,4.4),shade);B.box((X+side*2.5,y+2,.65),(.7,1.12,1.30),stone);B.box((X+side*2.5,y+2,3.97),(.7,1.12,.86),stone)
for j in range(28):
 a=pi*j/28;b=pi*(j+1)/28;B.poly([(X+2.62*cos(t),y,3.55+2.62*sin(t)) for y,t in [(-22,a),(-22,b),(22,b),(22,a)]],[(0,1,2,3)],brick)
for j in range(-5,6):
 arch(B,X,j*4,3.55,2.18,.38,.42,stone)
 for side in [-1,1]:
  B.box((X+side*2.35,j*4,1.75),(.55,.67,3.5),stone);B.box((X+side*2.31,j*4,3.53),(.7,.89,.26),ivory)
for j in range(-20,21):
 for i in range(-2,3):B.box((X+i*.95+(j%2)*.1,j*.97,.008),(.94,.956,.014),random.choice(tiles))
B.finish('Fortified passage • transverse ribs and arrow lights')
group('05 • Escort of Clement VII')
P=Batch();P.tube((0,0,.09),(0,0,1.28),.38,.19,white,20);P.tube((0,0,.93),(0,0,1.46),.35,.21,red,18);P.tube((0,0,.93),(0,0,.99),.36,.35,ivory,18);P.egg((0,0,1.64),(.145,.15,.176),skin);P.egg((0,-.055,1.54),(.136,.126,.105),hair);P.egg((0,.015,1.773),(.153,.155,.09),white);cross(P,0,-.246,1.25,.15,gold)
p=P.finish('Clement VII • travelling mozzetta');keys(p,'location',[(1,(X,-2,0)),(190,(X,-2,0)),(299,(X,-7,0)),(360,(X,-9,0))])
for i,(x,y) in enumerate([(-.88,-2.87),(.94,-1.3),(-.88,.3),(.75,1.6)]):
 o=man(X+x,y,0,pi,True,i,False);keys(o,'location',[(1,(X+x,y,0)),(190,(X+x,y,0)),(299,(X+x,y-5,0)),(360,(X+x,y-7,0))])
# Daylight, sky and reflected warm light along the passage.
group('06 • Daylight and torchlight')
def light(name,kind,loc,energy,color,target=None,size=1):
 d=bpy.data.lights.new(name,kind);o=obj(name,d);o.location=loc;d.energy=energy;d.color=color
 if kind=='AREA':d.shape='DISK';d.size=size
 if kind=='POINT':d.shadow_soft_size=size
 if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 return o
sun=light('Low morning sun','SUN',(-28,-19,21),3.3,(1,.79,.59),(0,3,0));sun.data.angle=.055
for y in [-14,-6,2,10,18]:
 B=Batch();B.tube((X-2.15,y,1.62),(X-1.91,y,2.28),.065,.092,wood);B.egg((X-1.91,y,2.42),(.094,.089,.24),orange);B.finish('Pitch torch')
 light('Reflected torchlight','POINT',(X-1.71,y,2.44),85,(1,.41,.13),size=.29)
 light('Window daylight','AREA',(X+2.12,y+1.8,3.05),220,(1,.81,.59),(X-.9,y+1,1.1),1.65)
light('Passage skylight fill','AREA',(X,-12,4.5),280,(.62,.73,1),(X,-3,1),3)
W=bpy.data.worlds.new('Pearl and ochre morning sky');s.world=W;W.use_nodes=True;N=W.node_tree.nodes;lk=W.node_tree.links.new;tex=N.new('ShaderNodeTexCoord');sep=N.new('ShaderNodeSeparateXYZ');lk(tex.outputs['Normal'],sep.inputs[0]);ramp=N.new('ShaderNodeValToRGB');lk(sep.outputs['Z'],ramp.inputs[0]);ramp.color_ramp.elements[0].color=(.82,.68,.51,1);ramp.color_ramp.elements[1].position=.7;ramp.color_ramp.elements[1].color=(.23,.38,.54,1);lk(ramp.outputs[0],N['Background'].inputs[0]);N['Background'].inputs[1].default_value=.75
group('07 • Cinematography')
def shot(name,first,last,pta,ptb,ta,tb,lens):
 d=bpy.data.cameras.new(name);o=obj(name,d);d.lens=lens
 for f,pt,target in [(first,pta,ta),(last,ptb,tb)]:
  o.location=pt;o.rotation_euler=(Vector(target)-Vector(pt)).to_track_quat('-Z','Y').to_euler();o.keyframe_insert(data_path='location',frame=f);o.keyframe_insert(data_path='rotation_euler',frame=f)
 m=s.timeline_markers.new(name,frame=first);m.camera=o;return o
a=shot('I — The approach',1,96,(-19,-32,11.5),(-13,-25,7),(0,7,5.2),(0,7,3.5),32)
shot('II — Hold the line',97,192,(-6.8,1.37,1.49),(-3.2,1.03,1.25),(.25,3.25,1.48),(2.1,2.55,1.4),28)
shot('III — The Passetto',193,288,(X+.26,-9.2,1.70),(X+.39,-13.2,1.74),(X,-1.57,1.50),(X,-6.7,1.52),34)
shot('IV — For those who stayed',289,360,(7.7,-4.2,2.47),(11,-8.7,4.35),(-1,3.2,1.88),(-1,4.9,2.7),37)
s.camera=a;s.frame_start=1;s.frame_end=360;s.render.fps=12;s.frame_set(1)
s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=True
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=95;s.render.filepath='//frames/f_'
s.render.film_transparent=False;s.view_settings.view_transform='AgX'
# Photographic rendering preset; EEVEE for animation on Apple Silicon.
# Recesses, sills, brick courses, a mosaic and construction site.
group('08 • Weathering and iconography')
B=Batch()
for z in (8.90,9.17,12.60,13.44):
 B.box((0,17.82,z),(19.25,.34,.14),ivory)
for x in [-6,-3,0,3,6]:
 B.box((x,17.73,9.12),(1.62,.51,.14),ivory)
for x in [-9,-7.55,-4.5,-1.5,1.5,4.5,7.55,9]:
 B.box((x,17.83,11.25),(.26,.38,4.25),shade)
# Gold mosaic of a blessing figure in the tympanum, an artistic motif.
for r,yy,m in [(1.82,17.46,ivory),(1.69,17.39,brass),(1.53,17.31,blue)]:
 B.tube((0,yy+.14,15.14),(0,yy,15.14),r,r,m,48)
B.tube((0,17.32,15.63),(0,17.26,15.63),.49,.49,gold,36);B.egg((0,17.23,15.58),(.28,.09,.34),skin)
B.poly([(-.76,17.24,14.18),(.76,17.24,14.18),(.45,17.24,15.25),(0,17.24,15.36),(-.4,17.24,15.23)],[(0,1,2,3,4)],red)
for k in range(55):
 a=2*pi*k/55;B.box((1.6*cos(a),17.28,15.14+1.6*sin(a)),(.085,.05,.085),gold)
for x in [-6,-2,2,6,10,-10]:
 B.box((x,14.55,5.05),(.95,.99,.11),brass)
for x in range(-14,15):
 B.box((x,14.04,7.5),(.5,.2,.22),shade)
B.box((X,21.6,2.95),(5,.7,6.4),shade);B.box((X,21.17,1.47),(2.3,.2,3.0),deep);arch(B,X,21.02,2.9,1.15,.22,.4,ivory)
B.finish('Mosaic, mouldings and distant stair door')
# Mineral, woven and oxidised surfaces (object-space, no screen noise).
for m in [stone,brick,shade,roof,wood,oak,ivory,red,blue,darksteel,steel]+tiles:
 n=m.node_tree.nodes;lk=m.node_tree.links.new;pbr=n.get('Principled BSDF');rgb=m.diffuse_color[:3];tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.8;noise.inputs['Detail'].default_value=4;lk(tc.outputs['Object'],noise.inputs[0]);cr=n.new('ShaderNodeValToRGB');cr.color_ramp.elements[0].position=.21;cr.color_ramp.elements[1].position=.79
 cr.color_ramp.elements[0].color=tuple(q*.60 for q in rgb)+(1,);cr.color_ramp.elements[1].color=tuple(min(1,q*1.15) for q in rgb)+(1,);lk(noise.outputs['Fac'],cr.inputs[0]);lk(cr.outputs[0],pbr.inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.19;bump.inputs['Distance'].default_value=.042;lk(noise.outputs['Fac'],bump.inputs['Height']);lk(bump.outputs[0],pbr.inputs['Normal'])
# A few local reversals break the parade-ground cadence.
for idx in [1,4,7,10]:
 o=bpy.data.objects['Guard %03d'%idx];t=o.rotation_euler.z;f=[127,159,218,261][[1,4,7,10].index(idx)]
 keys(o,'rotation_euler',[(1,(0,0,t)),(f,(0,0,t)),(f+5,(-.32,.11,t)),(f+12,(-1.44,.16,t+.12)),(360,(-1.44,.16,t+.12))])
for idx in [3,7,10,14]:
 o=bpy.data.objects['Landsknecht %03d'%idx];t=o.rotation_euler.z;f=117+idx*3;keys(o,'rotation_euler',[(1,(0,0,t)),(f,(0,0,t)),(f+5,(.31,-.12,t+.19)),(f+12,(1.43,-.12,t+.25)),(360,(1.43,-.12,t+.25))])
# Papal face, ruched sleeves, clasped hands and embroidered folds.
B=Batch()
for k in [-1,1]:
 B.egg((k*.055,-.141,1.665),(.019,.014,.012),hair);B.egg((k*.25,-.064,1.23),(.115,.13,.19),red);B.tube((k*.268,-.063,1.18),(k*.115,-.245,1.10),.096,.071,white);B.egg((k*.085,-.252,1.122),(.083,.059,.063),skin)
B.egg((0,-.154,1.625),(.033,.047,.039),skin)
for ix in range(18):
 a=2*pi*ix/18;B.tube((.332*cos(a),.332*sin(a),.18),(.235*cos(a),.235*sin(a),.9),.038,.017,white,9)
B.egg((.025,-.11,.097),(.114,.17,.085),vermilion)
o=B.finish('Clement • features and vestment folds');o.parent=p
# Split the escort legs at the hip and animate their stride through the passage.
import bmesh
for o in [o for o in list(bpy.data.objects) if o.name.startswith('Footing') and o.parent and o.parent.location.x>90]:
 for k in [-1,1]:
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.x*k < .0001],context='VERTS')
  for v in bm.verts:v.co.z-=.88
  me=bpy.data.meshes.new('Walking hose');bm.to_mesh(me);bm.free()
  for m in o.data.materials:me.materials.append(m)
  l=obj('Escort stride',me);l.parent=o.parent;l.location.z=.88;ph=o.parent.location.y;keys(l,'rotation_euler',[(f,(.32*k*sin((f-193)*.30+ph),0,0)) for f in range(189,306,2)])
 bpy.data.objects.remove(o,do_unlink=True)
# Cloud colour over the warm horizon.
N=W.node_tree.nodes;lk=W.node_tree.links.new;tex=N.new('ShaderNodeTexCoord');noise=N.new('ShaderNodeTexNoise');lk(tex.outputs['Normal'],noise.inputs[0]);noise.inputs['Scale'].default_value=4.2;noise.inputs['Detail'].default_value=5
r=N.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.30;r.color_ramp.elements[0].color=(.30,.365,.44,1);r.color_ramp.elements[1].position=.7;r.color_ramp.elements[1].color=(1,.825,.60,1);lk(noise.outputs[0],r.inputs[0]);lk(r.outputs[0],N['Background'].inputs[0])
N['Background'].inputs[1].default_value=.54
s.view_settings.look='AgX - Medium High Contrast'
# Time the pose animation at an actual 24 frames per second.
for act in bpy.data.actions:
 for layer in act.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:
      for pt in [k.co,k.handle_left,k.handle_right]:pt.x=pt.x*2-1
     fc.update()
for m in s.timeline_markers:m.frame=m.frame*2-1
s.frame_end=720;s.render.fps=24;s.frame_set(1)
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=12
s.render.resolution_x=1440;s.render.resolution_y=810

# Pack the inherited score for timeline playback. The finish script adds titles and foley.
editor=s.sequence_editor_create()
audio=editor.strips.new_sound('Schubert • Ave Maria',str(D/'Ave Maria.m4a'),1,1)
audio.frame_final_duration=720
bpy.ops.file.pack_all()
s.render.use_sequencer=False
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(D/"The Last Stand.blend"),compress=True)
