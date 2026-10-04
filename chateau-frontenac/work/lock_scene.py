import bpy,os,math,time
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));s=bpy.context.scene
# Replace the finite ground meshes with a continuous coastline.
for name in ['Cap Diamant terrain','River and far bank']:
 ob=bpy.data.objects.get(name)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
N=240;vs=[]
for j in range(N+1):
 y=-3000+j*25
 for i in range(N+1):
  x=-3000+i*25;edge=88 if x<100 else 62-(x-100);d=max(y-edge,x-115)
  z=-.8 if d<0 else (-.8-45*(d/42)**.72 if d<42 else -45.8)
  shore=175-.35*max(0,x-100)
  if y>shore:z=-54
  elif y>shore-15:z=min(z,-45.8-(y-(shore-15))/15*8.2)
  vs.append((x,y,z))
faces=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(N) for i in range(N)]
me=bpy.data.meshes.new('Continuous coastline');me.from_pydata(vs,[],faces);me.materials.append(bpy.data.materials['Earth and escarpment']);me.update();ob=bpy.data.objects.new('Cap Diamant terrain',me);bpy.data.collections['03 Terrain and river'].objects.link(ob)
me=bpy.data.meshes.new('River surface');me.from_pydata([(-6000,-6000,-47.5),(6000,-6000,-47.5),(6000,6000,-47.5),(-6000,6000,-47.5)],[],[(0,1,2,3)]);me.materials.append(bpy.data.materials['St Lawrence water']);me.update();ob=bpy.data.objects.new('St Lawrence River',me);bpy.data.collections['03 Terrain and river'].objects.link(ob)
# Static bevel baking avoids per-load/per-frame modifier costs.
hotel=bpy.data.objects['Chateau masonry, roofs and ornament'];bpy.context.view_layer.objects.active=hotel
for mod in list(hotel.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
s.frame_set(350);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(R,'outputs','Chateau_Frontenac.blend'))
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.resolution_percentage=50;s.cycles.samples=16;s.render.use_persistent_data=True
for f in [350,650]:
 s.frame_set(f);s.render.filepath=os.path.join(R,'work','locked_%03d.png'%f);t=time.time();bpy.ops.render.render(write_still=True);print('CHECK',f,time.time()-t,flush=True)
s.render.resolution_percentage=100;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.5;s.eevee.use_raytracing=False
for f in [350,351]:
 s.frame_set(f);s.render.filepath=os.path.join(R,'work','eevee_%03d.png'%f);t=time.time();bpy.ops.render.render(write_still=True);print('EEVEE',f,time.time()-t,flush=True)
