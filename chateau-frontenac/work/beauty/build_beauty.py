import bpy, math, random, os, json, time
from mathutils import Vector
from math import sin,cos,pi,sqrt
random.seed(1608)
ROOT='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa'
WORK=ROOT+'/work/beauty'; OUT=ROOT+'/outputs'
scene=bpy.context.scene; scene.name='Exterior | Château and Dufferin'
COL={c.name:c for c in scene.collection.children}
def collection(n):
 if n not in COL:
  c=bpy.data.collections.new(n);scene.collection.children.link(c);COL[n]=c
 return COL[n]
def material(n,col,rough=.4,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*col,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m
stone=bpy.data.materials['Pale grey limestone'];iron=bpy.data.materials['Deep green painted iron'];white=bpy.data.materials['Aged ivory paint'];dark=bpy.data.materials['Deep window recess'];copper=bpy.data.materials['Weathered verdigris copper'];seam=bpy.data.materials['Raised copper seams'];bronze=bpy.data.materials['Patinated bronze'];brick=bpy.data.materials['Warm historic red brick'];glass=[bpy.data.materials['Window reflection %02d'%i] for i in range(8)]
code=open(ROOT+'/work/build_scene.py').read();exec(code[code.index('class Batch:'):code.index('# Plan dimensions')])
def finish(batch,col,bevel=0):
 ob=batch.finish(col)
 if bevel:
  mod=ob.modifiers.new('Small edge highlights','BEVEL');mod.width=bevel;mod.segments=2
  bpy.context.view_layer.objects.active=ob
  try:bpy.ops.object.modifier_apply(modifier=mod.name)
  except:pass
 return ob

def texture(m,c1,c2,scale=(1,1,1),freq=4,bump=.003):
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');coord=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=scale;l.new(coord.outputs['Object'],v.inputs[0]);tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=freq;tex.inputs['Detail'].default_value=3;l.new(v.outputs[0],tex.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.2;r.color_ramp.elements[0].color=(*c1,1);r.color_ramp.elements[1].position=.8;r.color_ramp.elements[1].color=(*c2,1);l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.24;b.inputs['Distance'].default_value=bump;l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
 return tex

def marble(n,c1,c2):
 m=material(n,c1,.21);ns=m.node_tree.nodes;ls=m.node_tree.links;p=ns.get('Principled BSDF');p.inputs['Coat Weight'].default_value=.22
 tc=ns.new('ShaderNodeTexCoord');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1.8;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.7;ls.new(tc.outputs['Object'],noise.inputs[0]);vm=ns.new('ShaderNodeVectorMath');vm.operation='SCALE';vm.inputs[3].default_value=.46;ls.new(noise.outputs['Color'],vm.inputs[0]);add=ns.new('ShaderNodeVectorMath');add.operation='ADD';ls.new(tc.outputs['Object'],add.inputs[0]);ls.new(vm.outputs[0],add.inputs[1]);wv=ns.new('ShaderNodeTexWave');wv.wave_type='BANDS';wv.bands_direction='DIAGONAL';wv.inputs['Scale'].default_value=2.8;wv.inputs['Distortion'].default_value=7;wv.inputs['Detail Scale'].default_value=2.1;ls.new(add.outputs[0],wv.inputs[0]);r=ns.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.46;r.color_ramp.elements[0].color=(*c1,1);r.color_ramp.elements[1].position=.54;r.color_ramp.elements[1].color=(*c2,1);e=r.color_ramp.elements.new(.59);e.color=(*c1,1);ls.new(wv.outputs[0],r.inputs[0]);ls.new(r.outputs[0],p.inputs['Base Color']);return m

def light(n,loc,power,col,size=1,target=None,kind='AREA'):
 ld=bpy.data.lights.new(n,kind);ld.energy=power;ld.color=col
 if kind=='AREA':ld.shape='DISK';ld.size=size
 elif kind=='POINT':ld.shadow_soft_size=size
 ob=bpy.data.objects.new(n,ld);collection('Lighting').objects.link(ob);ob.location=loc
 if target:ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
 return ob

def render_settings(s):
 s.render.engine='CYCLES';s.cycles.device='GPU';s.cycles.samples=48;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.045;s.cycles.max_bounces=7;s.cycles.diffuse_bounces=3;s.cycles.glossy_bounces=4;s.cycles.transmission_bounces=6;s.cycles.transparent_max_bounces=8;s.cycles.volume_bounces=1;s.cycles.sample_clamp_indirect=4
 s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=720;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.use_persistent_data=True;s.render.film_transparent=False
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0

def camshot(n,start,end,a,b,ta,tb,lens,fstop=8):
 cd=bpy.data.cameras.new(n);ob=bpy.data.objects.new(n,cd);collection('Cameras | edit').objects.link(ob);cd.lens=lens;cd.clip_end=10000;cd.dof.use_dof=True;cd.dof.aperture_fstop=fstop
 for f in range(start,end+1):
  t=(f-start)/(end-start);u=t*t*(3-2*t);loc=Vector(a).lerp(Vector(b),u);tar=Vector(ta).lerp(Vector(tb),u);ob.location=loc;ob.rotation_euler=(tar-loc).to_track_quat('-Z','Y').to_euler();cd.dof.focus_distance=(tar-loc).length
  ob.keyframe_insert('location',frame=f);ob.keyframe_insert('rotation_euler',frame=f);cd.keyframe_insert('dof.focus_distance',frame=f)
 mark=scene.timeline_markers.new(n,frame=start);mark.camera=ob
 return ob
# Completely remove camera-distance pseudo-fog from material surfaces.
for m in bpy.data.materials:
 if not m.use_nodes:continue
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');out=next((a for a in n if a.type=='OUTPUT_MATERIAL'),None)
 if p and out:l.new(p.outputs[0],out.inputs['Surface'])
 for node in list(n):
  if node.type=='CAMERA':n.remove(node)
# Photographic cloud sky, with directional sunlight aligned for facade texture.
w=bpy.data.worlds.new('Clouds | Poly Haven Kloofendal');w.use_nodes=True;n=w.node_tree.nodes;l=w.node_tree.links;n.clear();out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');env=n.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(WORK+'/references/cloud_sky.hdr');env.image.pack();tc=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeMapping');mp.inputs['Rotation'].default_value[2]=math.radians(105);l.new(tc.outputs['Generated'],mp.inputs[0]);l.new(mp.outputs[0],env.inputs[0]);l.new(env.outputs[0],bg.inputs[0]);bg.inputs[1].default_value=.48;l.new(bg.outputs[0],out.inputs[0]);scene.world=w
sun=bpy.data.objects['Low morning sun'];sun.data.energy=2.3;sun.data.color=(1,.84,.66);sun.data.angle=math.radians(2);sun.rotation_euler=(Vector((0,0,20))-Vector((-160,200,165))).to_track_quat('-Z','Y').to_euler()
bpy.data.objects['Sky fill'].data.energy=3500
for i,m in enumerate(glass):
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Metallic'].default_value=.8;p.inputs['Roughness'].default_value=.09;p.inputs['Base Color'].default_value=(.19+i*.015,.26+i*.016,.30+i*.016,1)
# Replace broad generated-coordinate stains with physical-scale patina.
texture(copper,(.06,.13,.10),(.21,.32,.225),freq=.9,bump=.012);copper.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.65
texture(stone,(.38,.36,.31),(.64,.61,.53),freq=7,bump=.006)
# Actual density field. Thin river mist lives below the upper terrace, not over the camera.
old=bpy.data.objects.get('Distant river haze')
if old:old.hide_render=True
fog=material('Simulated river mist | heterogeneous volume',(.8,.86,.94));n=fog.node_tree.nodes;l=fog.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');v=n.new('ShaderNodeVolumePrincipled');v.inputs['Color'].default_value=(.83,.89,.97,1);v.inputs['Anisotropy'].default_value=.25;tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=6;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Generated'],noise.inputs[0]);sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Generated'],sep.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.05;r.color_ramp.elements[0].color=(1,1,1,1);r.color_ramp.elements[1].position=.9;r.color_ramp.elements[1].color=(0,0,0,1);l.new(sep.outputs['Z'],r.inputs[0]);mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(r.outputs[0],mul.inputs[0]);l.new(noise.outputs['Fac'],mul.inputs[1]);density=n.new('ShaderNodeMath');density.operation='MULTIPLY';density.inputs[1].default_value=.0012;l.new(mul.outputs[0],density.inputs[0]);l.new(density.outputs[0],v.inputs['Density']);l.new(v.outputs['Volume'],out.inputs['Volume']);B=Batch('Physical river fog volume');box((140,400,-27),(1000,450,39),fog);B.finish('Atmosphere | real volume')
# Foreground gardens, copper guttering, downpipes, roof finials.
B=Batch('Close-up architectural metalwork')
for x in [-78,-57,-32,-8,16]:
 rod((x,36.5,1),(x,36.5,22.5),.06,seam,12)
 for z in range(2,23,3):box((x,36.42,z),(.22,.20,.075),iron)
rod((-82,36.5,22.7),(25,36.5,22.7),.11,copper,16)
for x in range(-75,23,5):
 rod((x,28,33.7),(x,28,34.4),.028,iron,8);ball((x,28,34.3),.055,bronze,n=10)
finish(B,'01 Château | architecture')
flowergreen=material('Garden sage foliage',(.075,.19,.037),.7);petals=[material('Garden flower '+str(i),c,.55) for i,c in enumerate([(.63,.14,.34),(.91,.71,.48),(.48,.23,.57)])]
B=Batch('Terrace planters and flowers')
for x in [-98,-82,-62,-42,-22,-2,18]:
 box((x,44, .35),(2.5,1.1,.7),stone);box((x,44,.70),(2.24,.87,.05),dark)
 for j in range(42):
  xx=x+random.uniform(-1.05,1.05);yy=44+random.uniform(-.36,.36);zz=random.uniform(.83,1.27);rod((xx,yy,.73),(xx,yy,zz),.01,flowergreen,5);ball((xx,yy,zz-.07),.09,flowergreen,n=6,rings=3);ball((xx,yy,zz),.045,random.choice(petals),n=6,rings=3)
finish(B,'05 Trees and planting')
scene.timeline_markers.clear();scene.camera=camshot('01 | Terrace intimacy',1,192,(-110,86,8),(-83,80,10),(-30,24,29),(-17,22,32),28)
camshot('02 | Copper and stone',193,360,(-85,150,59),(-17,165,67),(-5,12,37),(2,10,39),43)
camshot('05 | Château closing portrait',649,720,(-73,136,64),(-65,130,65),(1,9,44),(1,9,45),50)
render_settings(scene);ext=scene
# Interior is an independent, explicitly photo-guided set, sharing the real sky.
scene=bpy.data.scenes.new('Interior | Bar 1608');bpy.context.window.scene=scene;COL={};scene.world=w.copy();scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.8
walnut=material('1608 | dark walnut paneling',(.043,.027,.022),.28);texture(walnut,(.018,.011,.009),(.065,.039,.024),(8,8,.18),5,.0015)
gold=material('1608 | aged satin brass',(.48,.28,.10),.27,.83)
black=material('1608 | blackened bronze frames',(.016,.018,.017),.28,.65)
cream=material('1608 | warm plaster',(.53,.43,.29),.83)
leather=material('1608 | oxblood leather',(.20,.028,.020),.3);texture(leather,(.15,.019,.016),(.25,.041,.027),freq=95,bump=.0007)
velvet=material('1608 | espresso banquette leather',(.035,.022,.02),.32)
marb=marble('1608 | Portoro marble',(.024,.017,.012),(.26,.17,.066));onyx=marble('1608 | illuminated honey onyx',(.58,.41,.23),(.87,.76,.52))
marb.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.17
mirror=material('1608 | smoked mirrored ceiling',(.16,.19,.21),.085,.95)
clear=material('1608 | crystal glass',(.97,.99,1),.055);p=clear.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
bulb=material('1608 | tungsten filament', (1,.52,.15));p=bulb.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.52,.19,1);p.inputs['Emission Strength'].default_value=7
books=[material('1608 | book cloth '+str(i),c,.65) for i,c in enumerate([(.12,.025,.022),(.20,.095,.038),(.032,.052,.046),(.31,.22,.13),(.025,.028,.04)])]
paper=material('1608 | ivory paper',(.67,.61,.47),.85)
# Annular mesh, used for the actual curved bar, shelves, rails, and circular ceiling.
def ring(x,y,z,ri,ro,h,m,a0=0,a1=2*pi,b=None,N=100):
 b=b or B;vs=[]
 for zz in [z,z+h]:
  for r in [ri,ro]:
   for i in range(N+1):
    a=a0+(a1-a0)*i/N;vs.append((x+r*cos(a),y+r*sin(a),zz))
 k=N+1;fs=[]
 for i in range(N):fs.extend([(i,i+1,k+i+1,k+i),(2*k+i,3*k+i,3*k+i+1,2*k+i+1),(i,2*k+i,2*k+i+1,i+1),(k+i,k+i+1,3*k+i+1,3*k+i)])
 fs.extend([(0,k,3*k,2*k),(N,2*k+N,3*k+N,k+N)]);b.add(vs,fs,m)
# Physical plank floor: individually shaded boards and narrow joints.
planks=[]
for i in range(12):
 m=material('1608 | oak plank %02d'%i,(.2,.09,.028),.31);f=random.uniform(.78,1.20);texture(m,(.095*f,.037*f,.012*f),(.34*f,.16*f,.047*f),(.13,18,5),4,.0015);planks.append(m)
B=Batch('Oak parquet and floor border');box((0,0,-.10),(17,17,.16),black)
for j in range(78):
 y=-7.8+j*.2
 for i in range(10):
  x=-8+i*1.7+(j%3)*.55
  if x*x+y*y<7.65**2:box((x,y,-.014),(1.686,.192,.035),random.choice(planks))
ring(0,0,-.011,7.3,7.75,.04,walnut);ring(0,0,.027,7.29,7.32,.002,gold);finish(B,'Room | shell')
# Twelve-sided salon. River windows occupy the far half; panelled walls and doorway behind camera.
B=Batch('Panelled salon walls and window mullions');radius=7.5;H=4.65
for i in range(12):
 a=i*2*pi/12;rad=Vector((cos(a),sin(a),0));tan=Vector((-sin(a),cos(a),0));center=rad*radius;angle=a+pi/2;width=2*radius*math.tan(pi/12)
 def panel(u,z,sz,mat,depth=0):box(center+tan*u-rad*depth+Vector((0,0,z)),sz,mat,angle)
 iswindow=sin(a)>-.1
 # top frieze, plinth, sill and posts
 panel(0,.14,(width,.22,.28),walnut);panel(0,4.31,(width,.30,.68),cream)
 for z,hh,dd in [(.28,.09,.29),(3.95,.12,.36),(4.08,.08,.28),(4.53,.12,.36),(4.62,.10,.43)]:panel(0,z,(width,dd,hh),walnut,.04)
 for u in [-width/2+.14,width/2-.14]:
  panel(u,2.05,(.28,.3,3.8),walnut)
  for off in [-.105,.105]:panel(u+off,2.04,(.025,.04,3.58),gold,.18)
 if iswindow:
  # Side panels and tall clear window panes.
  for u in [-1.56,1.56]:panel(u,2.1,(.62,.23,3.64),walnut)
  panel(0,.55,(2.7,.22,.7),walnut)
  for z in [.93,2.65,3.93]:panel(0,z,(2.66,.18,.11),walnut,.10)
  for u in [-1.32,0,1.32]:panel(u,2.43,(.09,.16,3.0),walnut,.11)
  for u in [-.66,.66]:
   for z,h in [(1.78,1.61),(3.30,1.19)]:panel(u,z,(1.23,.018,h),clear,-.02)
  panel(0,.88,(2.94,.44,.12),walnut,.12)
 else:
  panel(0,2.0,(width,.18,3.7),walnut)
  for u in [-1.1,0,1.1]:
   for z,h in [(1.0,1.35),(2.74,1.66)]:
    for zz in [z-h/2,z+h/2]:panel(u,zz,(.93,.055,.045),black,.12)
    for xx in [u-.465,u+.465]:panel(xx,z,(.045,.055,h),black,.12)
finish(B,'Room | shell',.007)
# Ceiling segmented mirrors with brass radial inlay and moulded perimeter.
B=Batch('Radial smoked mirror ceiling');cyl(0,0,4.68,7.9,.15,walnut,96)
for i in range(24):
 a=i*2*pi/24;b=(i+1)*2*pi/24
 B.add([(.70*cos(a),.70*sin(a),4.645),(7.4*cos(a+.009),7.4*sin(a+.009),4.645),(7.4*cos(b-.009),7.4*sin(b-.009),4.645),(.70*cos(b),.70*sin(b),4.645)],[(0,1,2,3)],mirror)
 rod((0,0,4.61),(7.4*cos(a),7.4*sin(a),4.61),.027,gold,8)
for r in [.75,4.2,7.25,7.45]:ring(0,0,4.58,r,r+.07,.07,gold)
finish(B,'Room | ceiling')
# Horseshoe bar, polished stone counter and individually fluted brass front.
B=Batch('Horseshoe bar | bronze and stone');cy=.25
ring(0,cy,0,2.8,3.34,1.0,black,a0=-pi*1.06,a1=pi*.16)
ring(0,cy,1.015,2.69,3.55,.09,onyx,a0=-pi*.97,a1=.07*pi)
ring(0,cy,1.015,2.69,3.55,.09,marb,a0=-pi*1.06,a1=-pi*.97)
for i in range(212):
 a=-pi*1.06+(pi*1.22)*i/211;rod((3.35*cos(a),cy+3.35*sin(a),.13),(3.35*cos(a),cy+3.35*sin(a),.94),.014,gold,8)
for z in [.10,.92]:ring(0,cy,z,3.34,3.38,.035,gold,a0=-pi*1.06,a1=.16*pi)
ring(0,cy,.22,3.58,3.615,.035,gold,a0=-pi*1.06,a1=.16*pi)
for a in [-2.9,-2.5,-2.1,-1.7,-1.3,-.9,-.5,-.1]:rod((3.32*cos(a),cy+3.32*sin(a),.22),(3.60*cos(a),cy+3.60*sin(a),.22),.025,gold,8)
# central column, service counters and backbar curved shelves
cyl(0,cy,0,.59,4.64,marb,96)
for z in [.18,1.12,1.58,2.22,2.93]:ring(0,cy,z,.61,1.25 if z<1.6 else .85,.065,marb)
for z in [1.15,1.82,2.52,3.18]:
 ring(0,cy,z,2.0,2.62,.055,walnut,a0=.06*pi,a1=.94*pi)
 ring(0,cy,z+.057,2.60,2.625,.018,gold,a0=.06*pi,a1=.94*pi)
for a in [pi*.07,pi*.23,pi*.40,pi*.60,pi*.77,pi*.93]:rod((2.62*cos(a),cy+2.62*sin(a),.05),(2.62*cos(a),cy+2.62*sin(a),3.55),.022,gold,12)
finish(B,'Bar | cabinetry',.007)
# Upholstered chairs have separate rounded cushions and slim bronze frames.
B=Batch('Oxblood leather bar stools')
for i in range(11):
 a=-pi*.98+i*pi*.97/10;x=4.0*cos(a);y=cy+4.0*sin(a);ang=a+pi/2
 def q(u,v,z):return (x+u*cos(ang)-v*sin(ang),y+u*sin(ang)+v*cos(ang),z)
 box(q(0,0,.78),(.51,.52,.13),leather,ang)
 box(q(0,-.235,1.12),(.53,.10,.61),leather,ang)
 for u in [-.26,.26]:
  for v in [-.22,.22]:rod(q(u,v,.045),q(u,v,.79),.019,black,10)
  rod(q(u,-.25,.07),q(u,.25,.07),.023,black,10)
  rod(q(u,-.24,1.12),q(u,.23,1.04),.018,gold,10)
  rod(q(u,.23,.78),q(u,.23,1.04),.018,black,10)
 rod(q(-.26,.23,.34),q(.26,.23,.34),.021,gold,12)
finish(B,'Furniture | stools',.022)
# Side bookcases, hand-sized volumes and low window banquettes.
B=Batch('Library bookcases and banquettes')
for side in [-1,1]:
 x=side*5.85;y=1.4;ang=side*pi/2
 def q(u,v,z):return (x+u*cos(ang)-v*sin(ang),y+u*sin(ang)+v*cos(ang),z)
 box(q(0,0,1.85),(2.0,.42,3.6),walnut,ang)
 for z in [.18,.70,1.28,1.86,2.44,3.02,3.60]:box(q(0,-.27,z),(2.08,.59,.065),walnut,ang)
 for u in [-1.03,1.03]:box(q(u,-.23,1.9),(.11,.58,3.58),walnut,ang)
 for row in range(6):
  u=-.87
  while u<.88:
   ww=random.uniform(.045,.10);hh=random.uniform(.20,.39)
   if random.random()<.17:u+=.25;continue
   box(q(u,-.35,.25+row*.58+hh/2),(ww,.22,hh),random.choice(books),ang)
   for z in [.25+row*.58+.055,.25+row*.58+hh-.055]:box(q(u,-.464,z),(ww*.78,.003,.008),gold,ang)
   u+=ww+.014
 # banquettes set against angled river window bays
 for yy in [4.0]:
  box((side*4.0,yy,.30),(2.15,.83,.24),walnut,side*.38)
  box((side*4.0,yy,.47),(2.12,.78,.18),velvet,side*.38)
  box((side*4.0,yy+.38,.85),(2.15,.13,.78),velvet,side*.38)
finish(B,'Furniture | library',.01)
# Cylindrical pendant lights hang in concentric loose clusters, as in the reference.
B=Batch('Glass pendant chandelier | individual tubes')
for i in range(76):
 a=i*2.39996;r=1.0+2.45*sqrt((i+.5)/76);x=r*cos(a);y=cy+r*sin(a);z=random.uniform(2.68,3.55);h=random.uniform(.22,.48)
 rod((x,y,z+h),(x,y,4.61),.0035,black,6)
 ring(x,y,z,.052,.058,h,clear,N=16);cyl(x,y,z+.014,.059,.018,black,16);cyl(x,y,z+h-.016,.059,.019,black,16)
 rod((x,y,z+.07),(x,y,z+h-.07),.003,bulb,6)
 if i%8==0:light('Pendant warm pool %02d'%i,(x,y,z+.14),12,(1,.64,.32),.10,kind='POINT')
finish(B,'Lighting | pendant glass')
# Warm continuous light below the onyx counter and shelves.
for a in [-2.8,-2.2,-1.6,-1.0,-.4]:light('Under-counter honey glow',(3.2*cos(a),cy+3.2*sin(a),.92),16,(1,.61,.24),.65,(3.6*cos(a),cy+3.6*sin(a),.45))
light('Chandelier bounced key',(0,-.2,3.9),260,(1,.73,.48),3.8,(0,0,.8))
for x in [-4,4]:light('River window daylight',(x,5.4,2.8),320,(.72,.84,1),3.1,(x*.25,-1,1))
light('Soft camera side bounce',(-3,-5,3.1),100,(1,.82,.66),3.0,(0,0,1.5))
# Glassware lathe profile (open bowl with thickness) and varied labelled bottles.
def lathe(x,y,z,profile,mat,b=None,n=24):
 b=b or B;vs=[]
 for r,hh in profile:
  for i in range(n):
   a=i*2*pi/n;vs.append((x+r*cos(a),y+r*sin(a),z+hh))
 b.add(vs,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)],mat)
def wine(x,y,z):
 lathe(x,y,z,[(0,0),(.042,0),(.043,.006),(.010,.01),(.004,.075),(.037,.095),(.047,.135),(.035,.185),(.032,.185),(.044,.135),(.034,.100),(.002,.084)],clear)
def tumbler(x,y,z):lathe(x,y,z,[(0,0),(.032,0),(.036,.09),(.032,.09),(.029,.009),(0,.009)],clear,n=20)
bottlecols=[(.045,.12,.045),(.29,.105,.027),(.18,.21,.14),(.38,.19,.045)]
bottles=[]
for i,c in enumerate(bottlecols):
 m=material('1608 | bottle glass '+str(i),c,.14);m.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.55;bottles.append(m)
label=material('1608 | bottle labels',(.71,.62,.42),.6)
B=Batch('Backbar bottles, stemware and service details')
for row,z in enumerate([1.21,1.88,2.58]):
 for i in range(33):
  a=.10*pi+.80*pi*(i/32);r=2.33;x=r*cos(a);y=cy+r*sin(a)
  if row==2 or (row==1 and i%3):wine(x,y,z)
  else:
   h=random.uniform(.23,.35);rr=random.uniform(.030,.046)
   lathe(x,y,z,[(0,0),(rr,0),(rr,h*.66),(rr*.40,h*.77),(rr*.39,h),(0,h)],random.choice(bottles))
   cyl(x,y,z+h*.22,rr+.001,h*.30,label,16);cyl(x,y,z+h-.025,rr*.43,.03,gold,12)
for i in range(20):
 a=random.uniform(0,2*pi);r=random.uniform(.72,1.15);x=r*cos(a);y=cy+r*sin(a);h=random.uniform(.21,.35)
 lathe(x,y,1.22,[(0,0),(.039,0),(.039,h*.65),(.016,h*.8),(.016,h),(0,h)],random.choice(bottles));cyl(x,y,1.27,.040,.12,label,16)
for i in range(20):
 x=-1.7+i*.17;y=cy-2.52;tumbler(x,y,1.12)
# Three still-life cocktails on the counter, napkins and polished shakers.
linen=material('1608 | linen cocktail napkins',(.70,.65,.55),.88)
for x,y in [(-1.8,-2.50),(.4,-2.78),(2.18,-2.20)]:
 box((x,y,1.116),(.23,.22,.004),linen,.17);tumbler(x,y,1.12)
 for xx,yy in [(x-.014,y-.012),(x+.012,y+.009)]:box((xx,yy,1.167),(.023,.023,.023),clear,.3)
 rod((x+.022,y+.01,1.15),(x+.048,y+.04,1.32),.0025,gold,6)
for i in range(3):lathe(-.55+i*.14,cy-2.68,1.112,[(0,0),(.046,0),(.054,.16),(.046,.18),(.04,.21),(0,.21)],gold)
fruit=[material('1608 | citrus '+str(i),c,.36) for i,c in enumerate([(.8,.51,.013),(.15,.33,.008),(.75,.22,.012)])]
for i in range(11):ball((1.1+random.uniform(-.2,.2),cy-2.66+random.uniform(-.08,.08),1.155+random.uniform(0,.05)),.044,random.choice(fruit),n=14,rings=8)
finish(B,'Bar | glassware and small objects')
# Restrained river vista seen through actual windows, with a low far-bank silhouette.
river=material('1608 | river outside windows',(.12,.25,.34),.18,.35);texture(river,(.085,.18,.25),(.21,.34,.39),(1,4,1),.4,.04)
hill=material('1608 | distant Lévis bank',(.08,.12,.105),.85)
B=Batch('River and Lévis seen through the salon windows');box((0,800,-10),(4000,4000,.2),river)
vs=[]
for i in range(101):
 x=-2000+i*40;z=4+4*sin(i*.11)+2*sin(i*.41);vs.extend([(x,1500,-10),(x,1500,z)])
B.add(vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(100)],hill);finish(B,'View | river')
scene.camera=camshot('03 | Enter Bar 1608',361,552,(-3.5,-6.20,1.75),(-1.5,-5.5,1.80),(.05,.5,2.30),(0,.5,2.25),23,5.6)
camshot('04 | Onyx, crystal and warm light',553,648,(1.0,-4.20,1.55),(.30,-4.05,1.55),(.15,-2.1,1.55),(-.35,-1.6,1.65),40,2.8)
render_settings(scene);scene.cycles.samples=64;scene['Accuracy']='Photo-guided reconstruction of Bar 1608. Furniture dimensions, concealed construction and vista are estimated, not a measured interior survey.'
scene['Reference photographs']='https://www.chateau-frontenac.com/dine/bar-1608/'
# Save all scenes and a machine-readable edit manifest.
manifest=[{'scene':ext.name,'start':1,'end':192,'camera':'01 | Terrace intimacy'},{'scene':ext.name,'start':193,'end':360,'camera':'02 | Copper and stone'},{'scene':scene.name,'start':361,'end':552,'camera':'03 | Enter Bar 1608'},{'scene':scene.name,'start':553,'end':648,'camera':'04 | Onyx, crystal and warm light'},{'scene':ext.name,'start':649,'end':720,'camera':'05 | Château closing portrait'}]
json.dump(manifest,open(WORK+'/shots.json','w'),indent=2)
for s in [ext,scene]:s['Film renderer']='Cycles path tracing on Apple Metal';s['Fog']='Heterogeneous participating medium, river volume only. Camera-distance emission haze removed.';s['Shot manifest']='work/beauty/shots.json'
bpy.context.window.scene=scene;scene.frame_set(445)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Chateau_Frontenac_Beauty.blend')
print('BEAUTY BUILD COMPLETE',flush=True)
