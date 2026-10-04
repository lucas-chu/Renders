import bpy,math,os,time
from mathutils import Vector
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));s=bpy.context.scene
# Bake static masonry bevels once so frame rendering does not reevaluate them.
hotel=bpy.data.objects['Chateau masonry, roofs and ornament'];bpy.context.view_layer.objects.active=hotel
for mod in list(hotel.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
# Correct the coast without submerging mapped structures on the northern shelf.
for v in bpy.data.objects['Cap Diamant terrain'].data.vertices:
 x,y,z=v.co;edge=88 if x<100 else 62-(x-100);d=max(y-edge,x-115)
 z=-.8 if d<0 else (-.8-45*(d/42)**.72 if d<42 else -45.8)
 shore=162-.35*max(0,x-100)
 if y>shore:z=-52
 elif y>shore-12:z=min(z,-45.8-(y-(shore-12))/12*6.2)
 v.co.z=z
# Widen distant inland ground beyond the view, with no visible rectangular end.
ob=bpy.data.objects['River and far bank']
# first eight vertices are the inland skirt in this mesh
for v in ob.data.vertices[:8]:
 if v.co.x<0:v.co.x=-3000
 else:v.co.x=3000
 if v.co.y< -950:v.co.y=-3000
 else:v.co.y=-400
cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear()
shots=[(1,240,(-157,64,3.2),(-109,65,4.5),(-1,21,29),(0,20,31),23,24),
(241,504,(-112,221,60),(119,228,96),(-2,9,32),(1,7,31),33,36),
(505,720,(-141,-124,107),(-199,-163,134),(0,33,21),(0,42,17),35,38)]
for start,end,a,b,ta,tb,la,lb in shots:
 for f in range(start,end+1):
  t=(f-start)/(end-start);u=t*t*(3-2*t);loc=Vector(a).lerp(Vector(b),u);target=Vector(ta).lerp(Vector(tb),u)
  if start==241:loc.y+=16*math.sin(math.pi*t)
  cam.location=loc;cam.rotation_euler=(target-loc).to_track_quat('-Z','Y').to_euler();cam.data.lens=la+(lb-la)*u;cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f);cam.data.keyframe_insert('lens',frame=f)
s.frame_set(350);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(R,'outputs','Chateau_Frontenac.blend'))
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=16;s.render.resolution_percentage=50;s.render.use_persistent_data=True
for f in [80,350,650]:
 s.frame_set(f);s.render.filepath=os.path.join(R,'work','approved_%03d.png'%f);t=time.time();bpy.ops.render.render(write_still=True);print(f,time.time()-t,flush=True)
