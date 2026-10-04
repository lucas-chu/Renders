import bpy,sys,time,json,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
engine=os.environ.get('COLOSSEUM_ENGINE','CYCLES')
if engine.startswith('BLENDER_EEVEE'):
 engine=next(e.identifier for e in s.render.bl_rna.properties['engine'].enum_items if 'EEVEE' in e.identifier)
s.render.engine=engine
s.render.resolution_percentage=int(os.environ.get('COLOSSEUM_SCALE','100'))
if engine=='CYCLES':
 p=bpy.context.preferences.addons['cycles'].preferences
 try:
  p.compute_device_type='METAL';p.get_devices()
  for d in p.devices:d.use=d.type=='METAL'
  s.cycles.device='GPU'
 except:pass
 if os.environ.get('COLOSSEUM_DEVICE')=='CPU': s.cycles.device='CPU'
 s.cycles.samples=int(os.environ.get('COLOSSEUM_SAMPLES','24'));s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.07
else:
 s.eevee.taa_render_samples=int(os.environ.get('COLOSSEUM_SAMPLES','48'))
 try:s.eevee.use_raytracing=True
 except:pass
 try:
  s.eevee.shadow_resolution_scale=.5;s.eevee.shadow_ray_count=1;s.eevee.shadow_step_count=6;s.eevee.use_shadow_jitter_viewport=False
 except:pass
 for l in bpy.data.lights:
  try:l.use_shadow_jitter=False;l.shadow_maximum_resolution=.15
  except:pass
s.render.use_persistent_data=True
if hasattr(s.render,'use_motion_blur'):
 s.render.use_motion_blur=True
 s.render.motion_blur_shutter=.32
frames=[int(x) for x in os.environ.get('COLOSSEUM_FRAMES','').split(',') if x]
test=bool(frames)
if not frames:frames=list(range(1,721))
for frame in frames:
 path=P/('previews' if test else 'frames')/((os.environ.get('COLOSSEUM_PREFIX','bench_') if test else '')+f'{frame:04d}.png')
 if path.exists() and not test:continue
 t=time.time();s.frame_set(frame);temporary=path.with_name('.pending_'+path.name);s.render.filepath=str(temporary);bpy.ops.render.render(write_still=True);os.replace(temporary,path)
 state={'frame':frame,'seconds':round(time.time()-t,2),'engine':engine,'samples':int(os.environ.get('COLOSSEUM_SAMPLES','24')),'file':str(path)}
 (P/'render_status.json').write_text(json.dumps(state,indent=2));print('FRAME_DONE',json.dumps(state),flush=True)
print('RENDER_COMPLETE',flush=True)
