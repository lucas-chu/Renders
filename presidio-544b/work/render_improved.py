import bpy,time,json,os
from pathlib import Path
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene
s.render.resolution_percentage=100
s.eevee.taa_render_samples=32
s.eevee.use_fast_gi=False
s.eevee.use_raytracing=True;s.render.image_settings.file_format='JPEG';s.render.image_settings.color_mode='RGB';s.render.image_settings.quality=97
s.frame_start=int(os.environ.get('START_FRAME','1'));s.frame_end=720;s.render.filepath=str(R/'work/improved_frames'/'####')
if s.frame_start==1:
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B_Improved.blend'))
last=time.time()
def completed(scene,*args):
 global last
 now=time.time();rec={'frame':scene.frame_current,'seconds':round(now-last,2)};last=now
 with (R/'work/improved-progress.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print('FRAME_DONE',rec['frame'],rec['seconds'],flush=True)
bpy.app.handlers.render_write.append(completed)
bpy.ops.render.render(animation=True)
print('ALL_NATIVE_FRAMES_COMPLETE',flush=True)
