import bpy,random,math
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa'
inside=bpy.data.scenes['Interior | Bar 1608'];ext=bpy.data.scenes['Exterior | Château and Dufferin']
for ob in inside.objects:
 if ob.type=='LIGHT' and ob.data.type=='AREA':
  ob.visible_glossy=False
  ob.visible_transmission=False
# Keep light-softened paneling readable without mirror-like wood highlights.
for name in ['1608 | dark walnut paneling','1608 | oxblood leather']:
 p=bpy.data.materials[name].node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.42
# Distant upper-city continuity uses linked context geometry, never the camera-distance haze material.
col=bpy.data.collections.new('08 Upper city | distant context');ext.collection.children.link(col)
source=bpy.data.objects['Old Quebec buildings and street pattern']
random.seed(34)
for row in range(4):
 for j in range(7):
  ob=bpy.data.objects.new('Upper city context %d %d'%(row,j),source.data);col.objects.link(ob);ob.location=((j-3)*350,-490-row*350,-1);ob.scale=(.70,.70,.70);ob.rotation_euler[2]=random.choice([0,math.pi])
ext['Upper city context']='The principal château and terrace follow the researched plan; far upper-city blocks are indicative linked context.'
bpy.context.window.scene=inside;inside.frame_set(445)
bpy.ops.wm.save_as_mainfile(filepath=R+'/outputs/Chateau_Frontenac_Beauty.blend')
