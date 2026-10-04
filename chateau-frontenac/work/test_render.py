import bpy,os,time
s=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
s.cycles.device='GPU'
print('DEVICES',[(d.name,d.type,d.use) for d in pref.devices],flush=True)
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s.render.engine='CYCLES';s.render.resolution_percentage=50;s.cycles.samples=16
s.frame_set(360);s.render.filepath=os.path.join(R,'work','polish_close.png');t=time.time();bpy.ops.render.render(write_still=True);print('CYCLES TIME',time.time()-t,flush=True)
s.frame_set(680)
from mathutils import Vector
s.camera.animation_data_clear();s.camera.data.animation_data_clear();s.camera.location=(-200,-165,124);s.camera.rotation_euler=(Vector((0,30,22))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=37
s.render.filepath=os.path.join(R,'work','river_reveal.png');bpy.ops.render.render(write_still=True)
s.render.engine='CYCLES'
s.render.engine='BLENDER_EEVEE';print('EEVEE',[(p.identifier,p.type) for p in s.eevee.bl_rna.properties],flush=True)
s.eevee.taa_render_samples=64
s.render.filepath=os.path.join(R,'work','eevee_reveal.png');t=time.time();bpy.ops.render.render(write_still=True);print('EEVEE TIME',time.time()-t,flush=True)
