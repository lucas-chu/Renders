import bpy,os,time
from pathlib import Path
R=Path('/Users/lucaschu/Documents/ChatGPT/Renders');s=bpy.context.scene
s.frame_set(300);s.render.resolution_percentage=100
engine=os.environ.get('ENGINE','BLENDER_EEVEE')
s.render.engine=engine
if engine=='BLENDER_EEVEE':
 e=s.eevee
 for name,val in [('taa_render_samples',48),('use_raytracing',True),('shadow_ray_count',1),('shadow_step_count',4),('use_shadow_jitter_viewport',False)]:
  if hasattr(e,name):setattr(e,name,val)
 for name in ['use_fast_gi','fast_gi_method','fast_gi_quality','fast_gi_ray_count','fast_gi_step_count','shadow_pool_size']:
  if hasattr(e,name):print(name,getattr(e,name),flush=True)
 if hasattr(e,'use_fast_gi'):e.use_fast_gi=True
 if hasattr(e,'fast_gi_quality'):e.fast_gi_quality=.5
 if hasattr(e,'fast_gi_ray_count'):e.fast_gi_ray_count=2
 if hasattr(e,'fast_gi_step_count'):e.fast_gi_step_count=8
 if hasattr(e,'ray_tracing_options'):
  e.ray_tracing_options.resolution_scale='2'
 for l in bpy.data.lights:
  if hasattr(l,'use_shadow_jitter'):l.use_shadow_jitter=False
  if hasattr(l,'shadow_maximum_resolution'):l.shadow_maximum_resolution=.08
else:
 s.cycles.samples=32;s.cycles.use_denoising=True
s.render.filepath=str(R/'work'/('benchmark_'+engine+'.png'));t=time.time();bpy.ops.render.render(write_still=True);print('BENCHMARK',engine,round(time.time()-t,2),flush=True)
if engine=='BLENDER_EEVEE':
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B_Eevee.blend'))
 s.frame_set(301);s.render.filepath=str(R/'work'/('benchmark_'+engine+'_warm.png'));t=time.time();bpy.ops.render.render(write_still=True);print('WARM BENCHMARK',round(time.time()-t,2),flush=True)
