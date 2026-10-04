import bpy,time
from pathlib import Path
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene;s.eevee.use_fast_gi=False;s.eevee.use_raytracing=False;s.eevee.taa_render_samples=32
s.frame_start=300;s.frame_end=302;s.render.filepath=str(R/'work/baked_');t=time.time();bpy.ops.render.render(animation=True);print('BAKED_SEQUENCE',time.time()-t,flush=True)
