import bpy,math,random,os,time
from math import sin,cos,pi,sqrt
from mathutils import Vector
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));scene=bpy.context.scene
# Load the reusable geometry functions, using the existing materials/collections.
COL={c.name:c for c in bpy.data.collections}
def collection(n):
 if n not in COL:
  c=bpy.data.collections.new(n);scene.collection.children.link(c);COL[n]=c
 return COL[n]
M=bpy.data.materials
brick=M['Warm historic red brick'];stone=M['Pale grey limestone'];copper=M['Weathered verdigris copper'];seam=M['Raised copper seams'];iron=M['Deep green painted iron'];white=M['Aged ivory paint'];dark=M['Deep window recess'];bronze=M['Patinated bronze'];glass=[M['Window reflection %02d'%i] for i in range(8)]
code=open(os.path.join(R,'work/build_scene.py')).read();exec(code[code.index('class Batch:'):code.index('# Plan dimensions')])
random.seed(123)
# Meter-scale copper weathering rather than broad artificial mottling.
n=copper.node_tree.nodes;l=copper.node_tree.links
for tex in n:
 if tex.type=='TEX_NOISE':
  uv=n.new('ShaderNodeTexCoord');l.new(uv.outputs['UV'],tex.inputs['Vector']);tex.inputs['Scale'].default_value=.65
 if tex.type=='VALTORGB':tex.color_ramp.elements[0].color=(.063,.13,.085,1);tex.color_ramp.elements[1].color=(.14,.22,.15,1)
# Regrade the shoreline: descend under the water beyond the narrow lower-town shelf.
ob=bpy.data.objects['Cap Diamant terrain']
for v in ob.data.vertices:
 x,y,z=v.co;edge=88 if x<100 else 62-(x-100);d=max(y-edge,x-115)
 if d>72:v.co.z=-52
 elif d>55:v.co.z=-45.8-(d-55)/17*6.2
# No expensive solid-volume box in the animation; the photographic horizon carries the distant haze.
bpy.data.objects['Distant river haze'].hide_render=True
# Detailed historic central pavilion: stone bays and steep pointed gables.
B=Batch('Pavilion stone tracery and roof dormers')
for x in [-50,-44,-38]:
 box((x,36.65,17.8),(2.35,.34,19.4),stone)
 for f in range(5):win(x,36.87,9.2+f*3.6,1.45,2.5)
 dormer(x,35.9,28.1,2.0,3.1)
 # narrow vertical stone finials at the gable corners
 for dx in [-1.4,1.4]:rod((x+dx,36.8,27.5),(x+dx,36.8,31.7),.085,stone,8)
# Upper arcade and paired windows on the oldest river wing.
for x in [-22,-18,-14,-10,-6,-2,2,6,10,14,18,22]:
 win(x,36.2,20.2,1.5,1.7)
 for i in range(9):
  t=pi*i/8;box((x+.9*cos(t),36.29,20.5+.9*sin(t)),(.23,.2,.27),stone)
# Secondary small dormers higher up the long copper roof, as in the photos.
for x in range(-77,25,8):dormer(x,30.3,29.5,.78,1.0)
# Deep entrance canopies, doors and masonry stair treads.
for x in [-60,-30,0,18]:
 box((x,37.7,3.4),(3.0,2.7,.20),iron)
 for dx in [-1.25,1.25]:rod((x+dx,38.8,.15),(x+dx,38.8,3.45),.065,iron)
 for i in range(3):box((x,38.3+i*.3,.09*(3-i)),(3.4,1.8,.15),stone)
B.finish('01 Château | architecture')
# Lower-town infill, modest individual townhouses with steep roofs and chimneys.
B=Batch('Lower Town waterfront houses')
slate=M['Blue grey standing seam'];plasters=[M['Neighborhood plaster %d'%i] for i in range(6)]
for row in range(2):
 for i in range(27):
  x=-225+i*11.3+random.uniform(-1,1);y=139+row*14+random.uniform(-1,1);w=random.uniform(7.0,10.3);d=random.uniform(7,11);h=random.choice([7.2,9.4,11.3]);z=-44.7
  box((x,y,z+h/2),(w,d,h),random.choice(plasters));hip(x,y,z+h,w+.6,d+.6,random.uniform(3,5),random.choice([slate,copper,M['Burgundy sheet metal'],M['Weathered zinc']]))
  for side in [-1,1]:
   a=0 if side==1 else pi
   for f in range(int(h/3)):
    for k in [-1,0,1]:win(x+k*w*.28,y+side*(d/2+.025),z+1.7+f*3,1.0,1.5,a,trim=True)
  box((x+w*.26,y,z+h+2.7),(.8,.85,2),brick)
B.finish('04 Old Quebec | mapped context')
# Continuous far land and a few skyline roofs prevent the scene ending at the map bounds.
B=Batch('Distant city skyline')
for i in range(160):
 x=random.uniform(-680,30);y=random.uniform(-470,-270);h=random.uniform(8,20);w=random.uniform(9,22);d=random.uniform(9,18)
 box((x,y,h/2-1),(w,d,h),random.choice(plasters));hip(x,y,h-1,w,d,random.uniform(3,6),slate)
B.finish('04 Old Quebec | mapped context')
# Three deliberate travelling shots, 30 seconds total, 24 fps.
cam=scene.camera;cam.animation_data_clear();cam.data.animation_data_clear()
shots=[(1,240,(-157,103,5.5),(-108,108,8),(-4,20,31),(-1,20,33),26,27),
(241,504,(-89,166,46),(110,181,83),(-2,9,34),(1,7,33),36,40),
(505,720,(-141,-124,107),(-199,-163,134),(0,33,21),(0,42,17),35,38)]
for start,end,a,b,ta,tb,la,lb in shots:
 for f in range(start,end+1):
  t=(f-start)/(end-start);u=t*t*(3-2*t);loc=Vector(a).lerp(Vector(b),u);target=Vector(ta).lerp(Vector(tb),u)
  # Slight arc in the middle aerial shot.
  if start==241:loc.y+=16*sin(pi*t)
  cam.location=loc;cam.rotation_euler=(target-loc).to_track_quat('-Z','Y').to_euler();cam.data.lens=la+(lb-la)*u;cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f);cam.data.keyframe_insert('lens',frame=f)
for n,f in [('01 • Along the terrace',1),('02 • The château revealed',241),('03 • Over the St Lawrence',505)]:scene.timeline_markers.new(n,frame=f)
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100;scene.render.fps=24;scene.frame_end=720
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.adaptive_threshold=.065;scene.cycles.use_denoising=True
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
for d in pref.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.render.use_persistent_data=True
scene.frame_set(320);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(R,'outputs','Chateau_Frontenac.blend'))
scene.render.resolution_percentage=50;scene.cycles.samples=16
for f in [80,350,650]:
 scene.frame_set(f);scene.render.filepath=os.path.join(R,'work','finalcheck_%03d.png'%f);t=time.time();bpy.ops.render.render(write_still=True);print('CHECK',f,time.time()-t,flush=True)
