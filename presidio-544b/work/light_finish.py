import bpy,math,random,time,bmesh
from pathlib import Path
from mathutils import Vector
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');s=bpy.context.scene;random.seed(544)
# Set the sun low enough to pick out the relief and bring the street's trees into the light.
l=bpy.data.lights['Low morning sun from the bay'];l.energy=3.0;l.color=(1.0,.84,.68);l.angle=math.radians(2)
bpy.data.objects['Morning sun'].rotation_euler=Vector((-1,.28,-.45)).to_track_quat('-Z','Y').to_euler()
s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.40;s.view_settings.exposure=.05
m=bpy.data.materials.get('Thin marine air')
if m:
 for n in m.node_tree.nodes:
  if n.type=='VOLUME_SCATTER':n.inputs['Density'].default_value=.00018
for m in bpy.data.materials:
 if m.name.startswith('Clay roof tile'):
  p=m.node_tree.nodes.get('Principled BSDF');c=p.inputs['Base Color'].default_value;p.inputs['Base Color'].default_value=(c[0]*.70,c[1]*.70,c[2]*.70,1)
m=bpy.data.materials['Weathered asphalt'];p=m.node_tree.nodes.get('Principled BSDF')
for link in list(p.inputs['Roughness'].links):m.node_tree.links.remove(link)
p.inputs['Roughness'].default_value=.93
# Set the newly added hedge leaves down into the soil rather than against the wall.
def h(x,y):return -.037*y-.054*x+4/(1+math.exp(max(-50,min(50,(x+42)/13))))+.16*math.sin(x*.09)*math.sin(y*.045)
o=bpy.data.objects.get('Low evergreen garden borders and planter foliage')
if o:
 for p in o.data.polygons:
  pts=[o.data.vertices[i] for i in p.vertices];c=sum((v.co for v in pts),Vector())/len(pts)
  if c.z<1.60:
   target=h(c.x,c.y)+random.uniform(.04,.77);dz=target-c.z
   for v in pts:v.co.z+=dz
# Remove crossing footpath surfaces within the asphalt carriageway, preserving sidewalks and curbs.
o=bpy.data.objects.get('Mapped public paths and raised curb lines')
if o:
 cp=[(-60,20),(-45,28),(-20,31),(-12.6,30),(-4.8,28),(2,26),(8.8,23),(17.7,19),(27.5,15),(38,10.8)]
 def rx(y):
  for (a,x),(b,xx) in zip(cp[:-1],cp[1:]):
   if a<=y<=b:return x+(xx-x)*(y-a)/(b-a)
  return 10000
 bm=bmesh.new();bm.from_mesh(o.data);bad=[]
 for f in bm.faces:
  c=f.calc_center_median()
  if abs(c.x-rx(c.y))<3.85:bad.append(f)
 bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(o.data);bm.free()
s.frame_set(300);bpy.ops.wm.save_as_mainfile(filepath=str(R/'outputs/Presidio_544B.blend'))
for f in [300,1]:
 s.frame_set(f);s.render.filepath=str(R/'work'/('beauty_%04d.png'%f));t=time.time();bpy.ops.render.render(write_still=True);print('BEAUTY',f,round(time.time()-t,2),flush=True)
