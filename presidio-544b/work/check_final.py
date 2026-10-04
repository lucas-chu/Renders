import bpy,time
from pathlib import Path
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene
s.render.resolution_percentage=100
for f in [300,301,1,450,720]:
 s.frame_set(f);s.render.filepath=str(R/'work'/('final_%04d.png'%f));t=time.time();bpy.ops.render.render(write_still=True);print('CHECK_FRAME',f,round(time.time()-t,2),flush=True)
