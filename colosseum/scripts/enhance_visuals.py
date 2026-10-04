import bpy,sys,math,bmesh,json
from mathutils import Vector,Matrix
from pathlib import Path
from math import sin,cos,pi
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import frame,group,box,beam,ellipsoid,flush
G.MATS.update({m.name:m for m in bpy.data.materials});s=bpy.context.scene
# Give the environment texture real directional coordinates; the previous Generated
# coordinates were constant in this World context and flattened the entire sky.
n=s.world.node_tree.nodes;l=s.world.node_tree.links
for env in [x for x in n if x.type=='TEX_ENVIRONMENT']:
 for link in list(env.inputs['Vector'].links):l.remove(link)
 # Two backgrounds preserve photographic sky exposure independently of light fill.
 camera_bg=n.new('ShaderNodeBackground');camera_bg.inputs['Strength'].default_value=.65;l.new(env.outputs[0],camera_bg.inputs[0]);path=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');l.new(path.outputs['Is Camera Ray'],mix.inputs[0]);l.new(n.get('Background').outputs[0],mix.inputs[1]);l.new(camera_bg.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n.get('World Output').inputs[0])
n.get('Background').inputs['Strength'].default_value=.28
s.view_settings.exposure=.12
bpy.data.materials['Distant golden air'].node_tree.nodes.get('Principled Volume').inputs['Density'].default_value=.00046
bpy.data.lights['Open sky above the cavea'].energy=65000
# Extend the earth below the horizon and give it a warmer, dusty surface.
for ob in bpy.data.objects:
 if ob.name.startswith('13 |') and 'Earth' in ob.name:ob.scale.x=10;ob.scale.y=10
# Sandy arena. The first scanned material read as wet soil, so use fine dry grains.
mat=bpy.data.materials['Sand'];ns=mat.node_tree.nodes;ls=mat.node_tree.links;bs=ns.get('Principled BSDF');ramp=next(x for x in ns if x.type=='VALTORGB')
ramp.color_ramp.elements[0].color=(.63,.48,.28,1);ramp.color_ramp.elements[1].color=(.83,.68,.44,1);ls.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.94
for link in list(bs.inputs['Roughness'].links):ls.remove(link)
bump=next(x for x in ns if x.type=='BUMP');bump.inputs['Strength'].default_value=.15;bump.inputs['Distance'].default_value=.008;ls.new(bump.outputs[0],bs.inputs['Normal'])
# Darker aged bronze reads as worked metal rather than polished gold spheres.
mat=bpy.data.materials['Bronze'];bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.42;ramp=next(x for x in mat.node_tree.nodes if x.type=='VALTORGB');ramp.color_ramp.elements[0].color=(.12,.074,.026,1);ramp.color_ramp.elements[1].color=(.35,.21,.07,1)
# Fine travertine porosity layered over restrained, real-scale coursing.
mat=bpy.data.materials['Travertine'];ns=mat.node_tree.nodes;ls=mat.node_tree.links;bs=ns.get('Principled BSDF');orig=bs.inputs['Base Color'].links[0].from_socket
pos=ns.new('ShaderNodeNewGeometry');sep=ns.new('ShaderNodeSeparateXYZ');ls.new(pos.outputs['Position'],sep.inputs[0]);angle=ns.new('ShaderNodeMath');angle.operation='ARCTAN2';ls.new(sep.outputs['Y'],angle.inputs[0]);ls.new(sep.outputs['X'],angle.inputs[1]);mul=ns.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=86;ls.new(angle.outputs[0],mul.inputs[0]);xyz=ns.new('ShaderNodeCombineXYZ');ls.new(mul.outputs[0],xyz.inputs[0]);ls.new(sep.outputs['Z'],xyz.inputs[1]);brick=ns.new('ShaderNodeTexBrick');ls.new(xyz.outputs[0],brick.inputs['Vector']);brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=2.3;brick.inputs['Row Height'].default_value=.7;brick.inputs['Mortar Size'].default_value=.008;brick.inputs['Mortar Smooth'].default_value=.008;brick.inputs['Color1'].default_value=(.86,.84,.78,1);brick.inputs['Color2'].default_value=(1,1,1,1);brick.inputs['Mortar'].default_value=(.58,.53,.43,1);mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.45;ls.new(orig,mix.inputs[1]);ls.new(brick.outputs['Color'],mix.inputs[2]);ls.new(mix.outputs[0],bs.inputs['Base Color'])
# Remove coarse study figures in the exterior arcades, keeping source templates in scripts.
for ob in list(bpy.data.objects):
 if ob.name.startswith('05 |'):bpy.data.objects.remove(ob,do_unlink=True)
col=bpy.data.collections.get('05 | Colosseum — sculpture')
if not col:col=bpy.data.collections.new('05 | Colosseum — sculpture');s.collection.children.link(col)

def scan(id,target_faces=22000,sol=False):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(P/f'assets/met_{id}.glb'));imported=set(bpy.data.objects)-before;verts=[];faces=[]
 for ob in imported:
  if ob.type!='MESH':continue
  offset=len(verts);verts.extend([ob.matrix_world@v.co for v in ob.data.vertices]);faces.extend([tuple(offset+j for j in p.vertices) for p in ob.data.polygons])
 low=Vector((min(v.x for v in verts),min(v.y for v in verts),min(v.z for v in verts)));high=Vector((max(v.x for v in verts),max(v.y for v in verts),max(v.z for v in verts)));print('SCAN',id,'BOUNDS',tuple(low),tuple(high),flush=True)
 # glTF importer converts Y-up to Blender Z-up. Center at the base and normalize height.
 cent=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z));height=high.z-low.z
 verts=[(v-cent)/height for v in verts]
 # Adapt the neoclassical anatomical proxy into an idealized solar colossus:
 # omit the sword and the Medusa trophy, retaining the raised arm and cloak.
 if sol:
  keep=[]
  for face in faces:
   c=sum((verts[k] for k in face),Vector())/len(face)
   if (c.x>.29 and .62<c.z<.85) or (c.x<-.30 and .30<c.z<.70):continue
   keep.append(face)
  faces=keep
 mesh=bpy.data.meshes.new(f'Classical sculpture {id}');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(f'Classical sculpture {id}',mesh);col.objects.link(ob)
 bpy.context.view_layer.objects.active=ob;ob.select_set(True)
 dec=ob.modifiers.new('Retain sculptural detail at film scale','DECIMATE');dec.ratio=min(1,target_faces/max(1,len(mesh.polygons)));bpy.ops.object.modifier_apply(modifier=dec.name)
 for p in ob.data.polygons:p.use_smooth=True
 ob.data.materials.clear();ob.data.materials.append(bpy.data.materials['Marble'])
 for q in imported:bpy.data.objects.remove(q,do_unlink=True)
 mesh=ob.data;bpy.data.objects.remove(ob,do_unlink=True);return mesh
scans=[scan(242017),scan(254613),scan(242211)]
# Scan placement is explicitly interpretive: these are classical references,
# not claims to identify the amphitheatre's lost statues.
with group('05 | Colosseum — sculpture plinths'):
 for tier,z in enumerate([12.8,24.6]):
  for i in range(80):
   t=(i+.5)*2*pi/80;x=93.35*cos(t);y=76.85*sin(t);angle=math.atan2(76.85*cos(t),-93.35*sin(t))
   with frame((x,y,z),angle):box((0,0,.32),(1.5,1.3,.65),'Marble')
   ob=bpy.data.objects.new(f'Order {tier+2} — deity {i+1:02}',scans[(i+tier)%3]);col.objects.link(ob);ob.location=(x,y,z+.65);ob.scale=(3.75,3.75,3.75);ob.rotation_euler[2]=angle
flush()
# Replace the coarse colossus while retaining its architectural pedestal.
for ob in list(bpy.data.objects):
 if ob.name.startswith('16 |') and any(k in ob.name for k in ['Bronze','Gold']):bpy.data.objects.remove(ob,do_unlink=True)
sol_mesh=scan(204758,45000,True);sol_mesh.materials.clear();sol_mesh.materials.append(bpy.data.materials['Bronze']);ob=bpy.data.objects.new('Colossus of Sol — idealized sculptural reconstruction',sol_mesh);col.objects.link(ob);ob.location=(-126,57,9);ob.scale=(28,28,28);ob.rotation_euler[2]=-.6
# Packed sculptural geometry is fully editable. External museum textures are
# not required: the reconstructed finish uses this scene's fresh stone/bronze.
(P/'SCENE_PLAN.md').write_text((P/'SCENE_PLAN.md').read_text()+'''\n## Sculptural treatment\n\nThe lost arcade statues use adapted public-domain Met scans of Aphrodite holding Eros (242017), Herakles (242211), and a Roman bronze boy (254613) as classical proxies, with reconstructed marble finish. These are not identified original Colosseum statues. The idealized Colossus uses an adapted anatomical proxy from Canova's Perseus (204758); this is an artistic stand-in for a lost ancient sculpture, not evidence of its exact appearance. Met object records and asset metadata are saved in references/sculpture-credits.json.\n''')
t=bpy.data.texts.get('READ ME — scene and evidence');t.clear();t.write((P/'SCENE_PLAN.md').read_text())
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
print('VISUAL ENHANCEMENT COMPLETE',flush=True)
