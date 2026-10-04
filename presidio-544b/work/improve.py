import bpy,math,random,time,bmesh,ast
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene;random.seed(5442)
# Clip accidental mapped footpaths and approach strips against the actual carriageway.
road=bpy.data.objects['Boulevard, Sumner lane and connecting streets'];bv=BVHTree.FromObject(road,bpy.context.evaluated_depsgraph_get())
def overroad(p):
 q=road.matrix_world.inverted()@Vector((p.x,p.y,100));return bv.ray_cast(q,Vector((0,0,-1)),200)[0] is not None
removed=0
for o in list(bpy.data.objects):
 if o.type!='MESH' or not ('Mapped public paths' in o.name or 'garden approach walks' in o.name):continue
 bm=bmesh.new();bm.from_mesh(o.data);bad=[]
 for f in bm.faces:
  if overroad(o.matrix_world@f.calc_center_median()):bad.append(f)
 removed+=len(bad);bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(o.data);bm.free()
print('ROAD CROSSINGS REMOVED',removed,flush=True)
# Natural, softer coastal daylight.
s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.65
sun=bpy.data.lights['Low morning sun from the bay'];sun.energy=2.1;sun.color=(1,.91,.79);sun.angle=math.radians(4.5)
s.view_settings.exposure=.10
# Reflection-driven glazing with very subtle irregularity in old panes.
m=bpy.data.materials['Old glass | cool reflected sky'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
p.inputs['Base Color'].default_value=(.27,.32,.34,1);p.inputs['Metallic'].default_value=.86;p.inputs['Roughness'].default_value=.055;p.inputs['Coat Weight'].default_value=.2
tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=2.8;tex.inputs['Detail'].default_value=2
b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.045;b.inputs['Distance'].default_value=.009;l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
# Real-world coordinate texture sizes, avoiding one grain pattern stretched across a mesh.
for name in ['Aged concrete | steps and sills','Painted warm white joinery','Warm ivory | fine historic stucco','Weathered asphalt']:
 m=bpy.data.materials[name];n=m.node_tree.nodes;l=m.node_tree.links;tc=n.new('ShaderNodeTexCoord')
 for no in list(n):
  if no.type=='TEX_NOISE' and not no.inputs['Vector'].is_linked:l.new(tc.outputs['Object'],no.inputs['Vector'])
# Gentle mineral variation in concrete.
m=bpy.data.materials['Aged concrete | steps and sills'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4;tex.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],tex.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.27,.28,.26,1);r.color_ramp.elements[1].color=(.44,.44,.40,1);l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
# Less uniform lawns, with pale blades and shaded green between them.
m=bpy.data.materials['Coastal lawn | living ground'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=.18;tex.inputs['Detail'].default_value=4;l.new(tc.outputs['Object'],tex.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.045,.075,.023,1);r.color_ramp.elements[1].color=(.21,.245,.11,1);l.new(tex.outputs['Fac'],r.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.45;src=p.inputs['Base Color'].links[0].from_socket;l.new(src,mix.inputs[1]);l.new(r.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
# Rebuild the tile courses on a continuous grid, preventing the zig-zag gaps of the earlier mesh.
source=Path('/Users/lucaschu/Documents/ChatGPT/Renders/work/build_scene.py').read_text();tree=ast.parse(source);cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='Mesh');exec(compile(ast.Module(body=[cls],type_ignores=[]),'mesh','exec'))
from math import sin,cos,pi
M=list(bpy.data.materials);COL={c.name[:2]:c for c in bpy.data.collections if c.name[:2].isdigit()};terra=[M.index(bpy.data.materials['Clay roof tile %02d'%i]) for i in range(12)]
def roof(m,w,d,z,rise,center=(0,0)):
 cx,cy=center;w2=w/2;d2=d/2;ridge=max(.1,w2-d2);pitch=rise/d2
 pts=[(-w2,-d2,z),(w2,-d2,z),(w2,d2,z),(-w2,d2,z),(-ridge,0,z+rise),(ridge,0,z+rise)]
 for f in [(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]:m.poly([(pts[i][0]+cx,pts[i][1]+cy,pts[i][2]) for i in f],terra[4])
 for axis in [0,1]:
  for side in [-1,1]:
   for j in range(int(d2/.32)+1):
    t=j*.32;half=(w2 if axis==0 else d2)-t;length=min(.40,d2-t+.015)
    if length<.045:continue
    for i in range(math.ceil((-half+.12)/.24),math.floor((half-.12)/.24)+1):
     cross=i*.24;ma=random.choice(terra)
     for k in range(10):
      v=[]
      for tt,ang in [(0,k*pi/10),(0,(k+1)*pi/10),(length,(k+1)*pi/10),(length,k*pi/10)]:
       cc=cross+cos(ang)*.118;depth=side*((d2 if axis==0 else w2)-t-tt);zz=z+(t+tt)*pitch+.036+sin(ang)*.063+.017*(1-tt/length)
       v.append((cx+(cc if axis==0 else depth),cy+(depth if axis==0 else cc),zz))
      m.poly(v,ma)
 for k in range(int(2*ridge/.30)+1):
  x=-ridge+k*.30;m.tube((cx+x,cy,z+rise+.07),(cx+min(ridge,x+.33),cy,z+rise+.07),.115,terra[4],n=12)
 for end in [-1,1]:
  for side in [-1,1]:
   for j in range(int(d2/.30)):
    t=j*.30;m.tube((cx+end*(w2-t),cy+side*(d2-t),z+t*pitch+.07),(cx+end*(w2-t-.31),cy+side*(d2-t-.31),z+(t+.31)*pitch+.07),.10,terra[4],n=10)
for old in list(bpy.data.objects):
 if ' | individual overlapping mission tiles' not in old.name:continue
 num=int(old.name.split(' |')[0]);duplex=num in [540,541,542,544,546,548,550,551];w=19.4 if duplex else 12.3;d=11.6 if duplex else 11.5;pw=10 if duplex else 2.8;pd=2.3 if duplex else 1.4;py=-d/2-pd/2;m=Mesh();roof(m,w+1.05,d+1.1,7.29,2.48);roof(m,pw+.6,pd+.65,4.26 if duplex else 3.86,.65,(0,py));roof(m,4.8,1.8,3.24,.32,(0,d/2+.7));ob=m.emit(old.name+' | aligned courses','02' if num==544 else '03',old.location,old.rotation_euler.z);bpy.data.objects.remove(old,do_unlink=True)
print('TILE COURSES REBUILT',flush=True)
# Restore reflected light and contact shading in Eevee.
s.render.engine='BLENDER_EEVEE';e=s.eevee;e.taa_render_samples=48;e.use_raytracing=True;e.use_fast_gi=True;e.fast_gi_quality=.5;e.fast_gi_ray_count=2;e.fast_gi_step_count=8;e.shadow_ray_count=2;e.shadow_step_count=5
if hasattr(e,'ray_tracing_options'):e.ray_tracing_options.resolution_scale='2'
# Put a reflection probe in the front garden, giving windows an off-screen neighborhood reflection.
pr=bpy.data.lightprobes.new('Front garden reflections','SPHERE');po=bpy.data.objects.new('Front garden reflection probe',pr);s.collection.objects.link(po);po.location=(12,0,5);pr.influence_distance=38
s.render.image_settings.file_format='PNG';s.render.resolution_percentage=75;s.frame_set(300)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B_Improved.blend'))
for f in [300,1,450]:
 s.frame_set(f);s.render.filepath=str(R/'work'/('improved_%04d.png'%f));t=time.time();bpy.ops.render.render(write_still=True);print('IMPROVED',f,round(time.time()-t,2),flush=True)
