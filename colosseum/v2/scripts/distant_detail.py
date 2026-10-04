import bpy,sys,math,random,json,ast
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi,sqrt,exp
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import *
G.MATS.update({m.name:m for m in bpy.data.materials});s=bpy.context.scene
# Replay the deterministic layout to place facade apertures on the distant LOD.
source=ast.parse((P/'scripts/cinematic_revision.py').read_text())
for n in source.body:
 if isinstance(n,ast.FunctionDef) and n.name in ['ground','protected']:
  exec(compile(ast.Module(body=[n],type_ignores=[]),'layout','exec'))
random.seed(162);cells={};buildings=[]
for attempt in range(22000):
 x=random.uniform(-1550,1550);y=random.uniform(-1550,1550);r=sqrt(x*x+y*y)
 if r>1580 or protected(x,y):continue
 if r<750 and (min(abs(y-q) for q in [-165,170,300,-340])<12 or min(abs(x-q) for q in [-390,170,310,455])<12):continue
 if abs(y-(.11*x+45*sin(x*.005)+470))<10:continue
 key=(int(x//30),int(y//30));near=[q for dx in [-1,0,1] for dy in [-1,0,1] for q in cells.get((key[0]+dx,key[1]+dy),[])]
 if any((x-a)**2+(y-b)**2<31**2 for a,b in near):continue
 cells.setdefault(key,[]).append((x,y));buildings.append((x,y))
# Distant roof tile rods were below pixel scale; keep only their roof silhouettes.
for ob in list(bpy.data.objects):
 if ob.type=='MESH' and ob.name.startswith('21 |') and any(m.name.startswith('Roof variation') for m in ob.data.materials):bpy.data.objects.remove(ob,do_unlink=True)
def roofplane(x,y,z,w,d,rise,mat):
 geo([(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x-w/2,y+d/2,z),(x+w/2,y+d/2,z),(x-w/2,y,z+rise),(x+w/2,y,z+rise)],[(0,1,5,4),(2,4,5,3),(0,4,2),(1,3,5)],mat)
with group('21d | City — distant facade apertures'):
 for idx,(x,y) in enumerate(buildings):
  r=sqrt(x*x+y*y);z=ground(x,y);w=random.uniform(13,23);d=random.uniform(12,22);h=random.choices([5.5,8.5,11.5,14.5,17.5],[18,30,28,17,7])[0];angle=.15*sin(y*.006)+(.0 if x<250 else .23)+random.uniform(-.12,.12);wall=random.choice(['Pale limestone plaster','Pale limestone plaster','Warm lime plaster','Faded rose plaster'])
  with frame((x,y,z),angle):
   roofmat=f'Roof variation {idx%4}'
   if r>=680:roofplane(0,0,h,w+.6,d+.6,min(3,d*.19),roofmat)
   if idx%3==1:roofplane(w*.4,d*.45,h*.59,w*.7+.5,d*.5+.5,1.5,roofmat)
   if idx%7==0:roofplane(-w*.25,0,h+2.55,w*.22+.3,d*.28+.3,.8,roofmat)
   if r<680:continue
   for side in [-1,1]:
    for j in range(max(1,int(h/3.2))):
     zz=2+j*3.1
     for i in range(max(2,int(w/3.5))):
      xx=-w/2+(i+.5)*w/max(2,int(w/3.5));yy=side*(d/2+.027);geo([(xx-.425,yy,zz-.675),(xx+.425,yy,zz-.675),(xx+.425,yy,zz+.675),(xx-.425,yy,zz+.675)],[(0,1,2,3)],'Window')
     for i in range(max(2,int(d/3.5))):
      yy=-d/2+(i+.5)*d/max(2,int(d/3.5));xx=side*(w/2+.027);geo([(xx,yy-.4,zz-.675),(xx,yy+.4,zz-.675),(xx,yy+.4,zz+.675),(xx,yy-.4,zz+.675)],[(0,1,2,3)],'Window')
    box((0,side*(d/2+.08),h-.12),(w+.2,.22,.20),'Trim')
flush()
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.07;s.render.resolution_percentage=100;s.frame_set(1)
# Record actual production choice in both the project and delivered notes.
s.cycles.volume_step_rate=16;s.cycles.volume_max_steps=128
s.cycles.sample_clamp_indirect=5
bpy.data.orphans_purge(do_recursive=True)
s['Production renderer']='Cycles, Metal, 24 samples, denoising, 1080p / 24 fps'
t=bpy.data.texts['READ ME — scene and evidence'];t.write('\nRevision production uses Cycles path tracing with denoising; fine distant facade apertures extend the city detail beyond the foreground neighborhood.\n')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'));print('DISTANT DETAIL SAVED',flush=True)
