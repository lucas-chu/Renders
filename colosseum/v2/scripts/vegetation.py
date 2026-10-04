import bpy,sys,math,random,bmesh,json
from mathutils import Vector
from pathlib import Path
from math import sin,cos,pi,exp,sqrt
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import *
G.MATS.update({m.name:m for m in bpy.data.materials});s=bpy.context.scene;random.seed(991)
# Remove coarse ground faces under the high-resolution local terrain patch.
for ob in bpy.data.objects:
 if ob.type=='MESH' and ob.name.startswith('18 |'):
  bm=bmesh.new();bm.from_mesh(ob.data);rm=[]
  for f in bm.faces:
   c=f.calc_center_median()
   if abs(c.x)<800 and abs(c.y)<800:rm.append(f)
  bmesh.ops.delete(bm,geom=rm,context='FACES');bm.to_mesh(ob.data);bm.free()
# Opaque modeled foliage catches real light and casts naturally broken shadows.
for k,c in enumerate([(.072,.112,.032),(.12,.16,.045),(.18,.20,.065),(.065,.085,.026)]):
 m=bpy.data.materials.new(f'Pine needles {k}');m.use_nodes=True;m.diffuse_color=(*c,1);bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=.61;G.MATS[m.name]=m

def leaf(c,angle,length,width,material):
 axis=Vector((cos(angle),sin(angle),random.uniform(-.25,.55)));side=Vector((-sin(angle),cos(angle),0));p=Vector(c)
 geo([p-axis*length/2,p-side*width/2,p+axis*length/2,p+side*width/2,p+Vector((0,0,.025))],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],material,False)
prototypes=[]
for variant in range(6):
 name=f'22p | Botanical prototype {variant}'
 with group(name):
  if variant<4:
   beam((0,0,0),(.35,.13,7.1),.28,'Bark',12,.13)
   for b in range(15):
    a=2*pi*b/15;rr=random.uniform(2.0,4.1);tip=(rr*cos(a),rr*sin(a),random.uniform(7.8,9.7));beam((.3,.1,5.7),tip,.095,'Bark',8,.025)
    for twig in range(7):
     aa=random.uniform(0,2*pi);rr=random.uniform(.3,1.4);c=Vector(tip)+Vector((rr*cos(aa),rr*sin(aa),random.uniform(-.2,.6)));beam(tip,c,.022,'Bark',5,.005)
     for j in range(33):
      q=c+Vector((random.gauss(0,.65),random.gauss(0,.60),random.gauss(0,.28)));leaf(q,random.uniform(0,2*pi),random.uniform(.32,.64),random.uniform(.10,.20),f'Pine needles {random.randrange(3)}')
  else:
   beam((0,0,0),(.08,.0,12),.21,'Bark',10,.03)
   for j in range(1900):
    z=random.uniform(1.6,12);r=(.82*(1-(z-1.6)/11)+.17)*sqrt(random.random());a=random.uniform(0,2*pi);leaf((r*cos(a),r*sin(a),z),a,random.uniform(.3,.55),.12,f'Pine needles {random.choice([0,1,3])}')
 flush();prototypes.append([o for o in bpy.data.objects if o.name.startswith(name)])

def ground(x,y):
 b=28*exp(-((x+285)/165)**4-((y+235)/155)**4)+17*exp(-((x-90)/240)**4-((y-275)/140)**4);r=sqrt(x*x+y*y);a=max(0,min(1,(r-650)/900));return b+a*(28+24*sin(x*.0021)*cos(y*.0018)+24*exp(-((x-1100)/550)**2-((y-1000)/600)**2))-.35
buildings=[]
# Random seed matches the builder's occupied grid only approximately; place most
# trees in protected landscaped precinct edges, streets and palace gardens.
spots=[(-169,-112,ground(-169,-112)),(-176,-130,ground(-176,-130)),(-194,-140,ground(-194,-140)),(119,127,ground(119,127)),(137,127,ground(137,127)),(-340,102,ground(-340,102))]
for i in range(18):spots.append((-331+i*6.4,-191,24.4))
for i in range(130):
 x=random.uniform(-800,800);y=random.uniform(-780,800)
 if (x/190)**2+(y/167)**2<1:continue
 if (-350<x<-90 and -100<y<100) or (-390<x<-170 and -327<y<-130) or (145<x<275 and -52<y<70) or (-95<x<175 and 195<y<395):continue
 # Follow open arterial edges rather than scatter through the house blocks.
 y=min([-178,185,315,-354],key=lambda q:abs(q-y))+random.uniform(-3,3)
 spots.append((x,y,ground(x,y)))
for i in range(250):
 a=random.uniform(0,2*pi);r=random.uniform(1620,2450);x=r*cos(a);y=r*sin(a);spots.append((x,y,ground(x,y)))
col=bpy.data.collections.new('22 | Landscape — Mediterranean trees');s.collection.children.link(col)
for idx,(x,y,z) in enumerate(spots):
 var=(4+idx%2) if 6<=idx<24 else idx%6;sc=random.uniform(.78,1.34);angle=random.uniform(0,2*pi)
 for src in prototypes[var]:
  ob=bpy.data.objects.new(f'Tree {idx:03} — {src.data.materials[0].name}',src.data);col.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler[2]=angle;ob.scale=(sc,sc,sc)
for proto in prototypes:
 for ob in proto:bpy.data.objects.remove(ob,do_unlink=True)
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'));print('BOTANICAL DETAIL SAVED',flush=True)
