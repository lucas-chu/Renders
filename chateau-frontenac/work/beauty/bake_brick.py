import bpy,os
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa';O=R+'/outputs';W=R+'/work/beauty'
original=bpy.data.materials['Warm historic red brick'];mat=original.copy();mat.name='Temporary CPU brick bake'
s=bpy.data.scenes.new('Temporary brick bake');bpy.context.window.scene=s;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1;s.render.threads_mode='FIXED';s.render.threads=6
bpy.ops.mesh.primitive_plane_add(size=2);plane=bpy.context.object;plane.data.materials.append(mat)
n=mat.node_tree.nodes;l=mat.node_tree.links;b=next(x for x in n if x.type=='TEX_BRICK');uv=n.new('ShaderNodeTexCoord');scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(18.56,12.16,1);l.new(uv.outputs['UV'],scale.inputs[0]);l.new(scale.outputs[0],b.inputs['Vector']);out=next(x for x in n if x.type=='OUTPUT_MATERIAL');em=n.new('ShaderNodeEmission');l.new(em.outputs[0],out.inputs['Surface']);dest=n.new('ShaderNodeTexImage');n.active=dest
images=[]
for label,socket,cs in [('albedo','Color','sRGB'),('height','Fac','Non-Color')]:
 im=bpy.data.images.new('Frontenac brick '+label,2048,2048,alpha=False);im.colorspace_settings.name=cs;dest.image=im;n.active=dest;l.new(b.outputs[socket],em.inputs[0]);bpy.ops.object.bake(type='EMIT',margin=2,use_clear=True);im.filepath_raw=W+'/brick_'+label+'.png';im.file_format='PNG';im.save();im.pack();images.append(im);print('BAKED',label,flush=True)
# Keep the original physically scaled brick pattern, with stable image lookups.
n=original.node_tree.nodes;l=original.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=.65;uv=n.new('ShaderNodeTexCoord');scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(1/18.56,1/12.16,1);l.new(uv.outputs['UV'],scale.inputs[0]);tex=n.new('ShaderNodeTexImage');tex.image=images[0];tex.extension='REPEAT';l.new(scale.outputs[0],tex.inputs[0]);l.new(tex.outputs['Color'],p.inputs['Base Color']);height=n.new('ShaderNodeTexImage');height.image=images[1];height.extension='REPEAT';l.new(scale.outputs[0],height.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.45;bump.inputs['Distance'].default_value=.02;l.new(height.outputs['Color'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal']);l.new(p.outputs[0],out.inputs['Surface'])
bpy.context.window.scene=bpy.data.scenes['Interior | Bar 1608'];bpy.data.objects.remove(plane,do_unlink=True);bpy.data.scenes.remove(s);bpy.data.materials.remove(mat)
for s in bpy.data.scenes:s['Brick material']='CPU-baked albedo and mortar relief maps, packed into this file; procedural shader replaced for stable Metal rendering.'
bpy.ops.wm.save_as_mainfile(filepath=O+'/Chateau_Frontenac_Beauty.blend')
p=O+'/Chateau_Frontenac_Beauty.blend1'
if os.path.exists(p):os.remove(p)
print('STABLE BRICK SAVED',flush=True)
