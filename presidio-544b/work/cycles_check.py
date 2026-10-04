import bpy,time
from pathlib import Path
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.055;s.cycles.max_bounces=4;s.cycles.diffuse_bounces=2;s.cycles.glossy_bounces=2;s.cycles.transparent_max_bounces=6
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.use_persistent_data=True
for frame in [300,301]:
 s.frame_set(frame);s.render.filepath=str(R/'work'/('cycles_%04d.png'%frame));t=time.time();bpy.ops.render.render(write_still=True);print('CYCLES_CHECK',frame,round(time.time()-t,2),flush=True)
