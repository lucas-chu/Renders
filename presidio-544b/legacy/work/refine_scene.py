import bpy,math,random,os,time
from pathlib import Path
from mathutils import Vector
R=Path('/Users/lucaschu/Documents/ChatGPT/Renders');s=bpy.context.scene
# Add render-ready refinements without reconstructing the verified site geometry.
for im in bpy.data.images:
 if 'asphalt_02_' in im.name:
  k=im.name.split('asphalt_02_')[-1].split('.')[0]
  paths=list((R/'work/assets/textures').glob('clean_asphalt_'+k+'.*'))
  if paths:
   im.unpack(method='REMOVE') if im.packed_file else None;im.filepath=str(paths[0]);im.reload()
# Low-frequency, nearly invisible stucco weathering.
m=bpy.data.materials.get('Warm ivory | fine historic stucco');n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=1.7;tex.inputs['Detail'].default_value=4
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.62,.60,.53,1);ramp.color_ramp.elements[1].color=(.77,.75,.68,1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
# Characterful, quiet objects at the entrance: two pots and a folded porch chair.
col=bpy.data.collections.get('02 | 544 — architectural fabric');a=math.radians(98.2)
def pos(x,y,z):return (x*math.cos(a)-y*math.sin(a),.5+x*math.sin(a)+y*math.cos(a),z)
base=-.037*.5+4/(1+math.exp(42/13))
def link(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
def cube(name,loc,size,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos(*loc));o=bpy.context.object;o.name=name;o.dimensions=size;o.rotation_euler[2]=a;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);link(o);be=o.modifiers.new('Worn edges','BEVEL');be.width=.015;be.segments=2;return o
ma=bpy.data.materials.get('Blackened bronze');iv=bpy.data.materials.get('Painted warm white joinery');clay=bpy.data.materials.get('Clay roof tile 03');soil=bpy.data.materials.get('Eucalyptus leaf litter')
for x,y in [(4.30,-6.8),(-4.15,-6.95)]:
 bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.15,radius2=.23,depth=.43,location=pos(x,y,base+1.33));o=bpy.context.object;o.name='Aged terracotta porch planter';o.data.materials.append(clay);link(o)
 bpy.ops.mesh.primitive_torus_add(major_radius=.222,minor_radius=.025,major_segments=24,minor_segments=8,location=pos(x,y,base+1.55));o=bpy.context.object;o.data.materials.append(clay);link(o)
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.197,depth=.02,location=pos(x,y,base+1.54));o=bpy.context.object;o.data.materials.append(soil);link(o)
 # A small leafy plant assembled from existing, fully textured stock foliage.
 proto=next((o for o in bpy.data.objects if o.name.startswith('Foundation planting') and o.type=='MESH'),None)
 if proto:
  ob=bpy.data.objects.new('Porch planter foliage',proto.data);col.objects.link(ob);ob.location=pos(x,y,base+1.55);ob.scale=(.21,.21,.30)
# Metal-framed chair sits within the portico, outside both door swings.
for xx in [1.76,2.24]:
 for yy in [-6.90,-7.35]:cube('Porch chair leg',(xx,yy,base+1.32),(.025,.025,.44),ma)
cube('Porch chair seat',(2,-7.12,base+1.56),(.54,.52,.055),iv)
for z in [1.68,1.80,1.92]:cube('Porch chair back slat',(2,-6.9,base+z),(.52,.04,.075),iv)
for xx in [1.75,2.25]:cube('Porch chair back frame',(xx,-6.9,base+1.72),(.025,.025,.73),ma)
# Restrained haze provides depth without concealing architecture.
vol=bpy.data.materials.new('Thin marine air');vol.use_nodes=True;nn=vol.node_tree.nodes;ll=vol.node_tree.links;nn.clear();vo=nn.new('ShaderNodeOutputMaterial');vs=nn.new('ShaderNodeVolumeScatter');vs.inputs['Color'].default_value=(.70,.79,.90,1);vs.inputs['Density'].default_value=.00055;vs.inputs['Anisotropy'].default_value=.2;ll.new(vs.outputs[0],vo.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=1,location=(-40,55,68));o=bpy.context.object;o.name='Maritime air | subtle distance falloff';o.dimensions=(850,1050,200);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(vol)
s.render.engine='BLENDER_EEVEE';e=s.eevee
for name,val in [('taa_render_samples',32),('use_raytracing',True),('shadow_ray_count',1),('shadow_step_count',3),('use_shadow_jitter_viewport',False),('use_fast_gi',True),('fast_gi_quality',.5),('fast_gi_ray_count',2),('fast_gi_step_count',8),('volumetric_samples',32)]:
 if hasattr(e,name):setattr(e,name,val)
if hasattr(e,'ray_tracing_options'):e.ray_tracing_options.resolution_scale='2'
for l in bpy.data.lights:
 if hasattr(l,'use_shadow_jitter'):l.use_shadow_jitter=False
 if hasattr(l,'shadow_maximum_resolution'):l.shadow_maximum_resolution=.12
s.render.resolution_percentage=100;s.render.image_settings.compression=12
bpy.ops.file.pack_all();s.frame_set(300);bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B.blend'))
for frame in [300,301,1,450,720]:
 s.frame_set(frame);s.render.filepath=str(R/'work'/('refined_%04d.png'%frame));t=time.time();bpy.ops.render.render(write_still=True);print('REFINED_FRAME',frame,round(time.time()-t,2),flush=True)
