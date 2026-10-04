import bpy,time
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=8;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.25;s.eevee.fast_gi_ray_count=2;s.eevee.fast_gi_step_count=8
s.render.resolution_percentage=100;s.render.use_persistent_data=True
s.eevee.shadow_ray_count=1;s.eevee.shadow_step_count=4
print('SUN',[(p.identifier,p.type) for p in bpy.data.lights['Morning sun'].bl_rna.properties if 'shadow' in p.identifier],flush=True)
if hasattr(bpy.data.lights['Morning sun'],'use_shadow_jitter'):bpy.data.lights['Morning sun'].use_shadow_jitter=False
for f in [360,361]:
 s.frame_set(f);s.render.filepath='/Users/lucaschu/Documents/Codex/2026-09-04/make/work/fast_'+str(f)+'.png';t=time.time();bpy.ops.render.render(write_still=True);print('BENCH',f,time.time()-t,flush=True)
