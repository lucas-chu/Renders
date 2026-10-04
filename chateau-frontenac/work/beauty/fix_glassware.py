import bpy, math
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa';s=bpy.data.scenes['Interior | Bar 1608'];bpy.context.window.scene=s
ob=bpy.data.objects['Backbar bottles, stemware and service details']
for v in ob.data.vertices:
 x,y,z=v.co
 if -2.31<y<-2.23 and -1.75<x<1.58 and 1.115<z<1.22:
  cx=-1.7+round((x+1.7)/.17)*.17
  v.co.y+=(.25-math.sqrt(3.12**2-cx**2))-(-2.27);v.co.z-=.014
 elif -.62<x<-.20 and -2.49<y<-2.37 and 1.11<z<1.33:v.co.y-=.55;v.co.z-=.006
 elif x*x+(y-.25)**2<1.5**2 and 1.219<z<1.65:v.co.z-=.035
ob.data.update()
m=bpy.data.materials.new('1608 | amber cocktail');m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.45,.15,.028,1);p.inputs['Roughness'].default_value=.08;p.inputs['Transmission Weight'].default_value=.82;p.inputs['IOR'].default_value=1.33
for x,y in [(-1.8,-2.5),(.4,-2.78),(2.18,-2.2)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.029,depth=.048,location=(x,y,1.153));o=bpy.context.object;o.name='Cocktail | amber liquid';o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 o.data.set_sharp_from_angle(angle=.6)
s.frame_set(445)
bpy.ops.wm.save_as_mainfile(filepath=R+'/outputs/Chateau_Frontenac_Beauty.blend')
