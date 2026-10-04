import bpy,os,json
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa'
s=bpy.data.scenes['Interior | Bar 1608']
t=bpy.data.node_groups.new('1608 | subtle optical glow','CompositorNodeTree');s.compositing_node_group=t
rl=t.nodes.new('CompositorNodeRLayers');rl.scene=s;gl=t.nodes.new('CompositorNodeGlare');out=t.nodes.new('NodeGroupOutput');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
print('GLARE INPUTS',[(a.name,str(a.default_value) if hasattr(a,'default_value') else '') for a in gl.inputs],flush=True)
gl.inputs['Type'].default_value='Fog Glow'
for key,val in [('Threshold',2.4),('Strength',.16),('Size',.25)]:
 if key in gl.inputs:gl.inputs[key].default_value=val
t.links.new(rl.outputs['Image'],gl.inputs['Image']);t.links.new(gl.outputs['Image'],out.inputs['Image'])
for scene in bpy.data.scenes:
 if scene.name.startswith(('Exterior','Interior')):
  scene.cycles.samples=32 if scene.name.startswith('Exterior') else 48;scene.cycles.adaptive_threshold=.06;scene.render.use_motion_blur=False
bpy.context.window.scene=s;s.frame_set(445)
bpy.ops.wm.save_as_mainfile(filepath=R+'/outputs/Chateau_Frontenac_Beauty.blend')
