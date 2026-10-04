import bpy,time,math
from pathlib import Path
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene
m=bpy.data.materials['Weathered asphalt']
for n in m.node_tree.nodes:
 if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.040,.046,.049,1);n.color_ramp.elements[-1].color=(.064,.071,.074,1)
for m in bpy.data.materials:
 if m.name.startswith('Evergreen leaf'):
  n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');oi=n.new('ShaderNodeObjectInfo');r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.65,.78,.56,1);r.color_ramp.elements[1].color=(1.1,1,.80,1);l.new(oi.outputs['Random'],r.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.65;mix.inputs[1].default_value=p.inputs['Base Color'].default_value;l.new(r.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
# A baked light field around the main building adds stable reflected daylight beneath the portico.
p=bpy.data.lightprobes.new('Porch and garden reflected daylight','VOLUME');o=bpy.data.objects.new('Baked daylight around 544',p);s.collection.objects.link(o);o.location=(2,.5,5);o.scale=(17,19,9);p.resolution_x=10;p.resolution_y=12;p.resolution_z=6;p.bake_samples=64;p.surfel_density=10;p.capture_distance=50;p.capture_world=True
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
print('BAKING_DAYLIGHT',flush=True);t=time.time();bpy.ops.object.lightprobe_cache_bake(subset='SELECTED');print('BAKED',round(time.time()-t,2),flush=True)
s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.color_mode='RGB';s.render.image_settings.quality=97;s.frame_set(300)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B_Improved.blend'))
s.render.filepath=str(R/'work/improved_final_');s.frame_start=300;s.frame_end=302
t=time.time();bpy.ops.render.render(animation=True);print('THREE_FRAMES',round(time.time()-t,2),flush=True)
