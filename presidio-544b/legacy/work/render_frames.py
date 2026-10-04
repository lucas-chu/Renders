import bpy,time,json,os
from pathlib import Path
R=Path('/Users/lucaschu/Documents/ChatGPT/Renders');s=bpy.context.scene
s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=12
start=int(os.environ.get('START_FRAME','1'));end=int(os.environ.get('END_FRAME','720'));frames=R/'work/frames';frames.mkdir(exist_ok=True)
for frame in range(start,end+1):
 dest=frames/('%04d.png'%frame)
 if dest.exists() and dest.stat().st_size>10000:continue
 s.frame_set(frame);s.render.filepath=str(dest);t=time.time();bpy.ops.render.render(write_still=True)
 rec={'frame':frame,'seconds':round(time.time()-t,2),'path':str(dest)}
 with (R/'work/render-progress.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print('FRAME_DONE',frame,rec['seconds'],flush=True)
print('ALL_NATIVE_FRAMES_COMPLETE',flush=True)
