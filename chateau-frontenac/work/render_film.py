import bpy,os,time,sys,json
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));s=bpy.context.scene
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.5;s.eevee.use_raytracing=False;s.cycles.samples=16;s.cycles.adaptive_threshold=.08;s.cycles.use_denoising=True;s.render.use_persistent_data=True
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=12
for light in bpy.data.lights:
 light.shadow_maximum_resolution=.35
 light.use_shadow_jitter=False
s.eevee.shadow_resolution_scale=.5;s.eevee.shadow_ray_count=1;s.eevee.shadow_step_count=4
s.eevee.fast_gi_ray_count=2;s.eevee.fast_gi_step_count=8
folder=os.path.join(R,'work','frames');os.makedirs(folder,exist_ok=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
start,end=map(int,args[:2]) if len(args)>=2 else (1,720)
t0=time.time();n=0
for f in range(start,end+1):
 path=os.path.join(folder,'%04d.png'%f)
 if os.path.isfile(path):continue
 s.frame_set(f);s.render.filepath=path;t=time.time();bpy.ops.render.render(write_still=True);n+=1
 print('FRAME %d / 720 | %.2fs | average %.2fs'%(f,time.time()-t,(time.time()-t0)/n),flush=True)
 with open(os.path.join(R,'work','render_progress.json'),'w') as fp:json.dump({'frame':f,'elapsed':time.time()-t0,'average':(time.time()-t0)/n},fp)
print('RENDER RANGE COMPLETE',start,end,flush=True)
