import bpy,math,os
from mathutils import Vector
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa'
# Preserve hard joinery edges while smoothing glass, curved metal, and stone.
inside=bpy.data.scenes['Interior | Bar 1608']
for ob in inside.objects:
 if ob.type=='MESH':
  for p in ob.data.polygons:p.use_smooth=True
  ob.data.set_sharp_from_angle(angle=math.radians(32))
# Slightly more diffused smoked ceiling reflection, and warmer visible lamp cores.
p=bpy.data.materials['1608 | smoked mirrored ceiling'].node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.19;p.inputs['Base Color'].default_value=(.085,.105,.12,1)
p=bpy.data.materials['1608 | tungsten filament'].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.27,.045,1);p.inputs['Emission Strength'].default_value=10
# Eliminate giant visible softbox reflections in the ceiling and column.
for ob in inside.objects:
 if ob.type=='LIGHT' and ob.data.type=='AREA':ob.data.specular_factor=.15
# The exterior ends on a complete silhouette against the sky, without cropping the spire.
def move(n,start,end,a,b,ta,tb,lens,fstop):
 ob=bpy.data.objects[n];ob.animation_data_clear();ob.data.animation_data_clear();ob.data.lens=lens;ob.data.dof.aperture_fstop=fstop
 for f in range(start,end+1):
  t=(f-start)/(end-start);u=t*t*(3-2*t);loc=Vector(a).lerp(Vector(b),u);tar=Vector(ta).lerp(Vector(tb),u);ob.location=loc;ob.rotation_euler=(tar-loc).to_track_quat('-Z','Y').to_euler();ob.data.dof.focus_distance=(tar-loc).length;ob.keyframe_insert('location',frame=f);ob.keyframe_insert('rotation_euler',frame=f);ob.data.keyframe_insert('dof.focus_distance',frame=f)
move('02 | Copper and stone',193,360,(-95,183,36),(12,182,44),(-6,14,39),(0,13,40),36,8)
move('05 | Château closing portrait',649,720,(-82,154,28),(-76,148,30),(-3,16,42),(-3,16,43),34,8)
move('03 | Enter Bar 1608',361,552,(-1.8,-6.9,1.72),(-.50,-6.45,1.74),(0,.4,2.05),(0,.4,2.1),22,6.3)
move('04 | Onyx, crystal and warm light',553,648,(1.15,-4.4,1.65),(.10,-4.2,1.60),(-.40,-2.48,1.36),(-.42,-2.38,1.40),46,3.5)
inside.frame_set(445);bpy.context.window.scene=inside
bpy.ops.wm.save_as_mainfile(filepath=R+'/outputs/Chateau_Frontenac_Beauty.blend')
