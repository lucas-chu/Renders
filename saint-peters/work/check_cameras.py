import bpy,time
R='/Users/lucaschu/Documents/Codex/2026-09-04/make'
s=bpy.context.scene
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.use_persistent_data=True;s.cycles.samples=20;s.render.resolution_percentage=40
for f in [1,240,241,480,481,720]:
 s.frame_set(f);s.render.filepath=R+'/work/check_'+str(f)+'.png';t=time.time();bpy.ops.render.render(write_still=True);print('FRAME',f,'SECONDS',time.time()-t,flush=True)
s.render.resolution_percentage=100;s.cycles.samples=24
for f in [120,121,122]:
 s.frame_set(f);s.render.filepath=R+'/work/full_'+str(f)+'.png';t=time.time();bpy.ops.render.render(write_still=True);print('FULL FRAME',f,'SECONDS',time.time()-t,flush=True)
