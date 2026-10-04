import bpy,os,time,sys
R='/Users/lucaschu/Documents/Codex/2026-09-04/make'
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.25;s.eevee.fast_gi_ray_count=2;s.eevee.fast_gi_step_count=8;s.eevee.shadow_ray_count=1;s.eevee.shadow_step_count=4
bpy.data.lights['Morning sun'].use_shadow_jitter=False
s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=5
s.render.fps=24;s.render.filepath=R+'/work/frames/frame_';s.render.use_persistent_data=True
# Flowing normal detail provides subtle motion on the basin and cascades.
for mn in ['Fountain water','Sunlit fine water']:
 m=bpy.data.materials[mn];n=m.node_tree.nodes;l=m.node_tree.links
 if n.get('Flowing water detail') is None:
  tex=n.new('ShaderNodeTexNoise');tex.name='Flowing water detail';tex.noise_dimensions='4D';tex.inputs['Scale'].default_value=18
  tex.inputs['W'].default_value=0;tex.inputs['W'].keyframe_insert('default_value',frame=1)
  tex.inputs['W'].default_value=15;tex.inputs['W'].keyframe_insert('default_value',frame=720)
  bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.20;bump.inputs['Distance'].default_value=.045;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],n.get('Principled BSDF').inputs['Normal'])
s.frame_start=1;s.frame_end=720;s.frame_set(1)
s['film_renderer']='Eevee, 16 temporal samples, screen-space indirect illumination'
bpy.ops.wm.save_as_mainfile(filepath=R+'/outputs/Saint_Peters_Basilica.blend')
start=int(os.environ.get('START_FRAME','1'));end=int(os.environ.get('END_FRAME','720'))
s.frame_start=start;s.frame_end=end
print('RENDER START',start,end,time.time(),flush=True)
bpy.ops.render.render(animation=True)
print('RENDER FINISHED',time.time(),flush=True)
