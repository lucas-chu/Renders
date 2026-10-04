import bpy,time,os,json,sys
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa';W=R+'/work/beauty'
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
print('DEVICES',[(d.name,d.type,d.use) for d in p.devices],flush=True)
shots=json.load(open(W+'/shots.json'))
frames=[int(f) for f in sys.argv[sys.argv.index('--')+1:]] if '--' in sys.argv else [96,275,445,602,680]
for f in frames:
 sh=next(x for x in shots if x['start']<=f<=x['end']);s=bpy.data.scenes[sh['scene']];bpy.context.window.scene=s;s.frame_set(f);s.camera=bpy.data.objects[sh['camera']];s.cycles.device='GPU';s.cycles.samples=24;s.render.resolution_percentage=50;s.render.filepath=W+'/preview_%03d.png'%f;t=time.time();bpy.ops.render.render(write_still=True);print('RENDERED',f,time.time()-t,flush=True)
