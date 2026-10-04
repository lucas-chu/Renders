import bpy,math,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
sun=bpy.data.lights['Late afternoon sun'];sun.energy=4.1;sun.color=(1,.86,.71);sun.angle=.018
bpy.data.objects['Late afternoon sun'].rotation_euler=Vector((.65,.76,-.52)).to_track_quat('-Z','Y').to_euler()
sky=next(n for n in s.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=.48
s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.05
bpy.data.lights['Open sky above the cavea'].energy=42000
s.view_settings.exposure=.55
# Remove the museum's deep display base from the new figure proxy.
me=bpy.data.meshes.get('Complete classical figure — Perseus proxy')
if me:
 import bmesh
 bm=bmesh.new();bm.from_mesh(me);remove=[f for f in bm.faces if max(v.co.z for v in f.verts)<.155];bmesh.ops.delete(bm,geom=remove,context='FACES')
 for v in bm.verts:v.co.z=(v.co.z-.155)/.845;v.co.x/=.845;v.co.y/=.845
 bm.to_mesh(me);bm.free()
s.render.engine='BLENDER_EEVEE';s.eevee.use_raytracing=True;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.75;s.eevee.fast_gi_ray_count=4;s.eevee.fast_gi_step_count=16;s.eevee.fast_gi_distance=45;s.eevee.taa_render_samples=64
s.render.resolution_percentage=100;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
print('LIGHTING SAVED',flush=True)
os.environ.update(COLOSSEUM_ENGINE='BLENDER_EEVEE',COLOSSEUM_SAMPLES='64',COLOSSEUM_SCALE='75',COLOSSEUM_PREFIX='eevee_',COLOSSEUM_FRAMES='1,350,620')
exec(compile((P/'scripts/render_film.py').read_text(),'render_film.py','exec'))
