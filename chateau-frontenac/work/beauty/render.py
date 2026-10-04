import bpy,time,os,json,sys
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa';W=R+'/work/beauty'
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.kernel_optimization_level='OFF';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
shots=json.load(open(W+'/shots.json'));check='--check' in sys.argv
frames=[1,193,361,445,552,553,602,648,649,720] if check else sorted(set(f for sh in shots for f in list(range(sh['start'],sh['end']+1,2))+[sh['end']]))
archive_path='/private/tmp/frontenac_archived.json'
archived=set(json.load(open(archive_path))['frames']) if os.path.exists(archive_path) else set()
rendered_this_pass=0
for f in frames:
 path=W+'/frames/%04d.png'%f
 if f in archived or os.path.exists(path):continue
 sh=next(x for x in shots if x['start']<=f<=x['end']);s=bpy.data.scenes[sh['scene']];bpy.context.window.scene=s;s.frame_set(f);s.camera=bpy.data.objects[sh['camera']];s.cycles.device='GPU';s.cycles.samples=16;s.cycles.adaptive_threshold=.1;s.cycles.denoising_quality='BALANCED';s.cycles.denoising_use_gpu=True;s.render.resolution_percentage=100;s.render.threads_mode='FIXED';s.render.threads=6;s.render.use_motion_blur=False;s.render.motion_blur_shutter=.35
 s.render.filepath=W+'/frames/%04d.tmp.png'%f;t=time.monotonic();bpy.ops.render.render(write_still=True);os.replace(s.render.filepath,path)
 count=len(archived | {int(p[:4]) for p in os.listdir(W+'/frames') if p.endswith('.png') and '.tmp' not in p});elapsed=time.monotonic()-t
 print('FRAME %d | %d / 365 | %.2fs'%(f,count,elapsed),flush=True)
 json.dump({'last_frame':f,'completed':count,'seconds':round(elapsed,2),'stage':'check' if check else 'film'},open(W+'/progress.json','w'))
 rendered_this_pass+=1
 if not check and rendered_this_pass>=32:break
print('CHECK COMPLETE' if check else 'RENDER PASS COMPLETE',flush=True)
