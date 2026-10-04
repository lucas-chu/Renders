import bpy,math,random,json,time
from pathlib import Path
from mathutils import Vector
R=Path('/Users/lucaschu/Documents/ChatGPT/Renders');s=bpy.context.scene;random.seed(544)
print('PACKED SCENE OPEN',flush=True)
# Work entirely from packed materials and geometry, avoiding external texture reloads.
gm=bpy.data.materials['Coastal lawn | living ground'];n=gm.node_tree.nodes;l=gm.node_tree.links;p=n.get('Principled BSDF');src=p.inputs['Base Color'].links[0].from_socket
gray=n.new('ShaderNodeRGBToBW');l.new(src,gray.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.08;r.color_ramp.elements[0].color=(.024,.047,.009,1);r.color_ramp.elements[1].position=.65;r.color_ramp.elements[1].color=(.16,.245,.046,1);l.new(gray.outputs[0],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
p=bpy.data.materials['Old glass | cool reflected sky'].node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.018,.032,.033,1);p.inputs['Roughness'].default_value=.065;p.inputs['Metallic'].default_value=.72;p.inputs['Coat Weight'].default_value=.65
for m in bpy.data.materials:
 if m.name.startswith('Clay roof tile'):
  p=m.node_tree.nodes.get('Principled BSDF');c=p.inputs['Base Color'].default_value;p.inputs['Base Color'].default_value=(c[0]*.80,c[1]*.85,c[2]*.9,1)
# Use a procedural, granular road material so accidental photographed markings cannot repeat.
m=bpy.data.materials['Weathered asphalt'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1.5;noise.inputs['Detail'].default_value=4;r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.032,.037,.042,1);r.color_ramp.elements[1].color=(.12,.13,.14,1);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.9
fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=155;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.38;b.inputs['Distance'].default_value=.017;l.new(fine.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
for o in bpy.data.objects:
 if o.name.startswith('Foundation planting'):o.scale*=2.15
 if o.name.startswith('Short coastal grass'):o.scale*=1.65

def h(x,y):return -.037*y-.054*x+4/(1+math.exp(max(-50,min(50,(x+42)/13))))+.16*math.sin(x*.09)*math.sin(y*.045)
# Extend porch foundations and stair masses below terrain. Replace jagged side parapets with sloped walls.
class Batch:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def box(self,c,sz,mat):
  o=len(self.v);x,y,z=c;a,b,d=[v/2 for v in sz]
  self.v += [(x+dx,y+dy,z+dz) for dx,dy,dz in [(-a,-b,-d),(a,-b,-d),(a,b,-d),(-a,b,-d),(-a,-b,d),(a,-b,d),(a,b,d),(-a,b,d)]]
  for f in [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]:self.f.append(tuple(o+i for i in f));self.mi.append(mat)
 def face(self,v,mat):
  o=len(self.v);self.v+=v;self.f.append(tuple(range(o,o+len(v))));self.mi.append(mat)
 def emit(self,name,old):
  me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update();ob=bpy.data.objects.new(name,me);old.users_collection[0].objects.link(ob);ob.matrix_world=old.matrix_world.copy()
  for m in [bpy.data.materials['Warm ivory | fine historic stucco'],bpy.data.materials['Aged concrete | steps and sills'],bpy.data.materials['Painted warm white joinery']]:me.materials.append(m)
  for p,m in zip(me.polygons,self.mi):p.material_index=m
  be=ob.modifiers.new('Weather-softened edges','BEVEL');be.width=.018;be.segments=2
for old in list(bpy.data.objects):
 if ' | entry portico and steps' not in old.name:continue
 num=int(old.name.split(' |')[0]);duplex=num in [540,541,542,544,546,548,550,551];pw=10 if duplex else 2.8;pd=2.3 if duplex else 1.4;d=11.6 if duplex else 11.5;py=-d/2-pd/2;end=py-pd/2
 # Keep the upper original columns/parapets, remove the old separate stair components by face center.
 import bmesh
 bm=bmesh.new();bm.from_mesh(old.data)
 faces=[f for f in bm.faces if f.calc_center_median().y<end-.015]
 bmesh.ops.delete(bm,geom=faces,context='FACES');bm.to_mesh(old.data);bm.free()
 b=Batch();b.box((0,py,-.07),(pw,pd,2.12),0)
 for x in [-3.1,3.1] if duplex else [0]:
  for i in range(7):
   top=1.1-i*.235;b.box((x,end-(i+.5)*.29,top-1.35),(2.37,.315,2.7),1)
  for side in [-1,1]:
   xx=x+side*1.30;ya=end-2.03;yb=end
   for dx in [-.13,.13]:b.face([(xx+dx,ya,-1.7),(xx+dx,yb,-1.7),(xx+dx,yb,1.88),(xx+dx,ya,.39)],0)
   b.face([(xx-.13,ya,.39),(xx+.13,ya,.39),(xx+.13,yb,1.88),(xx-.13,yb,1.88)],2)
   b.box((xx,ya,-.25),(.30,.30,1.3),0);b.box((xx,ya,.43),(.39,.42,.12),2)
 b.emit('%d | grounded stair and porch foundations'%num,old)
print('MATERIALS AND GROUND CONTACT FIXED',flush=True)
# Dense woodland around, but not inside, the mapped residential clearing.
forest=bpy.data.collections['04 | Mature woodland'];protos=bpy.data.collections['08 | Asset prototypes'];trunks=[o for o in protos.objects if 'prototype trunk' in o.name];pairs=[]
for o in trunks:
 seed=o.name.split()[-1];leaf=next(p for p in protos.objects if p.name=='Individual leaves '+seed);pairs.append((o,leaf))
features=json.load(open(R/'work/site.json'));centers=[];roadpts=[]
for f in features:
 ps=f['xy'];t=f['tags']
 if 'building' in t:centers.append((sum(p[0] for p in ps)/len(ps),sum(p[1] for p in ps)/len(ps),13 if t.get('addr:housenumber','') in ['540','541','542','544','546','548','550','551'] else 10))
 if t.get('highway') not in [None,'footway','path','steps']:
  for a,b in zip(ps[:-1],ps[1:]):
   ln=math.dist(a,b);n=max(1,int(ln/4))
   for j in range(n):roadpts.append((a[0]+(b[0]-a[0])*j/n,a[1]+(b[1]-a[1])*j/n))
def valid(x,y):
 if -100<x<38 and -75<y<115:return False
 if any((x-cx)**2+(y-cy)**2<r*r for cx,cy,r in centers):return False
 if any((x-cx)**2+(y-cy)**2<65 for cx,cy in roadpts):return False
 return True
count=0
for k in range(620):
 x=random.uniform(-240,165);y=random.uniform(-190,310)
 if not valid(x,y):continue
 a=random.random()*math.tau;scale=random.uniform(.8,1.28);pair=random.choice(pairs)
 for proto in pair:
  o=bpy.data.objects.new('Woodland '+proto.name,proto.data);forest.objects.link(o);o.location=(x,y,h(x,y));o.scale=(scale,)*3;o.rotation_euler[2]=a
 count+=1
print('WOODLAND ADDED',count,flush=True)
s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.65
li=bpy.data.lights['Low morning sun from the bay'];li.energy=2.3;li.color=(1,.88,.73);li.angle=math.radians(3)
s.view_settings.exposure=.45
# Refine script uses only packed/procedural textures in this execution.
code=(R/'work/refine_scene.py').read_text();begin=code.index('# Low-frequency');code=code[:code.index('for im in bpy.data.images:')]+code[begin:]
exec(compile(code,str(R/'work/refine_scene.py'),'exec'))
