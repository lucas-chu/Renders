import bpy,math,random,time,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene;random.seed(544)
print('FINAL PASS',flush=True)
forest=bpy.data.collections['04 | Mature woodland']
# Replace the overlapping simplified foreground tree with its existing detailed conifer.
for o in list(forest.objects):
 if abs(o.location.x-10)<.01 and abs(o.location.y+15)<.01 and not o.name.startswith('Mature conifer'):bpy.data.objects.remove(o,do_unlink=True)
# Remove woodland instances inside the distant mapped homes.
centers=[o.location.copy() for o in bpy.data.objects if 'stucco shell and chimneys' in o.name]
for o in list(forest.objects):
 if o.name.startswith('Woodland') and any((o.location-c).length<15 for c in centers):bpy.data.objects.remove(o,do_unlink=True)
# Distant foliage LOD: keep canopy volume, reduce subpixel leaves. Near branches remain fully modeled.
lod={}
for o in list(forest.objects):
 if 'Individual leaves' not in o.name or math.hypot(o.location.x,o.location.y)<60:continue
 src=o.data
 if src.name not in lod:
  v=[];f=[];mi=[]
  for pi in range(0,len(src.polygons),6):
   poly=src.polygons[pi]
   pts=[src.vertices[i].co.copy() for i in poly.vertices];c=sum(pts,Vector())/len(pts);off=len(v);v.extend([tuple(c+(p-c)*2.15) for p in pts]);f.append(tuple(range(off,off+len(pts))));mi.append(poly.material_index)
  me=bpy.data.meshes.new(src.name+' | distant canopy LOD');me.from_pydata(v,[],f);me.update()
  for m in src.materials:me.materials.append(m)
  for p,idx in zip(me.polygons,mi):p.material_index=idx
  lod[src.name]=me
 o.data=lod[src.name]
print('CANOPY LOD',len(lod),flush=True)
# Garden trees are dense scans; simplify the shared mesh once while preserving texture coordinates.
garden=[o for o in forest.objects if o.name.startswith('Small garden tree')]
if garden:
 src=garden[0];temp=src.copy();temp.data=src.data.copy();forest.objects.link(temp);mod=temp.modifiers.new('Garden leaf LOD','DECIMATE');mod.ratio=.20
 bpy.context.view_layer.objects.active=temp;temp.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name)
 data=temp.data
 for o in garden:o.data=data
 bpy.data.objects.remove(temp,do_unlink=True)
# Compact material slots: no object carries the entire project's material palette.
seen=set()
for o in bpy.data.objects:
 if o.type!='MESH' or o.data in seen:continue
 me=o.data;seen.add(me)
 if not len(me.polygons) or not len(me.materials):continue
 arr=np.empty(len(me.polygons),dtype=np.int32);me.polygons.foreach_get('material_index',arr);used=np.unique(arr)
 if len(used)==len(me.materials):continue
 mats=[me.materials[int(i)] for i in used];remap=np.searchsorted(used,arr).astype(np.int32);me.materials.clear()
 for ma in mats:me.materials.append(ma)
 me.polygons.foreach_set('material_index',remap)
print('MATERIAL SLOTS COMPACTED',flush=True)
# Bake static bevels once rather than recalculate them throughout the camera flight.
deps=bpy.context.evaluated_depsgraph_get();todo=[]
for o in bpy.data.objects:
 if o.type=='MESH' and len(o.modifiers):todo.append((o,bpy.data.meshes.new_from_object(o.evaluated_get(deps))))
for o,me in todo:o.modifiers.clear();o.data=me
print('STATIC EDGES BAKED',len(todo),flush=True)
# Merge static low garden detail to avoid thousands of tiny draw calls.
for prefix,label in [('Short coastal grass','Coastal lawn tufts'),('Foundation planting','Foundation planting beds')]:
 obs=[o for o in bpy.context.scene.objects if o.name.startswith(prefix)]
 if not obs:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();bpy.context.object.name=label
print('GARDEN BATCHED',flush=True)
# Ground the garage foundations.
for o in bpy.data.objects:
 if ' | historic garage' in o.name:
  for v in o.data.vertices:
   if v.co.z<.06:v.co.z-=1.5
# More reflective neutral glazing: retain dark interiors with soft sky reflections.
p=bpy.data.materials['Old glass | cool reflected sky'].node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.07,.085,.09,1);p.inputs['Metallic'].default_value=.50;p.inputs['Roughness'].default_value=.07;p.inputs['Coat Weight'].default_value=.8
# Porch details and low leaf-built hedges.
a=math.radians(98.2);base=-.037*.5+4/(1+math.exp(42/13));col=bpy.data.collections['02 | 544 — architectural fabric']
def pos(x,y,z):return (x*math.cos(a)-y*math.sin(a),.5+x*math.sin(a)+y*math.cos(a),z)
def move(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
def cube(name,loc,sz,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos(*loc));o=bpy.context.object;o.name=name;o.dimensions=sz;o.rotation_euler[2]=a;o.data.materials.append(ma);move(o);return o
iv=bpy.data.materials['Painted warm white joinery'];iron=bpy.data.materials['Blackened bronze'];clay=bpy.data.materials['Clay roof tile 03']
cube('Restored central portico parapet',(0,-8.22,base+1.52),(3.2,.12,.92),iv)
for x,y in [(4.28,-6.75),(-4.22,-6.9)]:
 bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.15,radius2=.23,depth=.43,location=pos(x,y,base+1.33));o=bpy.context.object;o.name='Terracotta planter';o.data.materials.append(clay);move(o)
 bpy.ops.mesh.primitive_torus_add(major_radius=.222,minor_radius=.025,major_segments=24,minor_segments=8,location=pos(x,y,base+1.55));o=bpy.context.object;o.data.materials.append(clay);move(o)
for xx in [1.76,2.24]:
 for yy in [-6.9,-7.35]:cube('Porch chair leg',(xx,yy,base+1.32),(.025,.025,.44),iron)
cube('Porch chair seat',(2,-7.12,base+1.56),(.54,.52,.055),iv)
for z in [1.68,1.8,1.92]:cube('Porch chair back',(2,-6.9,base+z),(.52,.04,.075),iv)
for xx in [1.75,2.25]:cube('Porch chair frame',(xx,-6.9,base+1.72),(.025,.025,.73),iron)
verts=[];faces=[];idx=[];mats=[bpy.data.materials.get('Evergreen leaf %02d'%i) for i in range(6)]
for xx,yy,w,d,z in [(-7.0,-6.6,3.6,1.0,.68),(7,-6.6,3.6,1.0,.68),(0,-8.8,3.2,.75,.38),(4.28,-6.75,.40,.40,1.95),(-4.22,-6.9,.4,.4,1.95)]:
 for k in range(2100 if w>1 else 180):
  x=xx+random.uniform(-w/2,w/2);y=yy+random.uniform(-d/2,d/2);zz=base+z+random.uniform(-.3,.25);c=Vector(pos(x,y,zz));ang=random.random()*math.tau;u=Vector((math.cos(ang),math.sin(ang),random.uniform(-.4,.4)))*random.uniform(.035,.065);v=Vector((-math.sin(ang),math.cos(ang),.15))*.022;off=len(verts);verts += [tuple(c-u),tuple(c+v),tuple(c+u),tuple(c-v)];faces.append((off,off+1,off+2,off+3));idx.append(random.randrange(6))
me=bpy.data.meshes.new('Individual clipped hedge leaves');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Low evergreen garden borders and planter foliage',me);col.objects.link(o)
for m in mats:me.materials.append(m)
for p,i in zip(me.polygons,idx):p.material_index=i
# Measured production settings. Disable noisy screen-space GI; retain real sunlight and sky fill.
e=s.eevee;e.taa_render_samples=24;e.use_raytracing=False
if hasattr(e,'use_fast_gi'):e.use_fast_gi=False
if hasattr(e,'volumetric_samples'):e.volumetric_samples=16
s.render.resolution_percentage=100;s.render.image_settings.compression=12;s.frame_set(300)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B.blend'))
print('PRODUCTION SCENE SAVED',len(bpy.data.objects),flush=True)
for frame in [300,301,1,450,720]:
 s.frame_set(frame);s.render.filepath=str(R/'work'/('final_%04d.png'%frame));t=time.time();bpy.ops.render.render(write_still=True);print('FINAL_FRAME',frame,round(time.time()-t,2),flush=True)
