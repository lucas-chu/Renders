import bpy,time
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.75
s.render.resolution_percentage=100;s.render.use_persistent_data=True
for f in [120,121,360]:
 s.frame_set(f);s.render.filepath='/Users/lucaschu/Documents/Codex/2026-09-04/make/work/eevee_full_'+str(f)+'.png';t=time.time();bpy.ops.render.render(write_still=True);print('BENCH',f,time.time()-t,flush=True)
