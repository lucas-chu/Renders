import bpy,sys,math,random,json,ast
from pathlib import Path
from mathutils import Vector,Matrix
from math import sin,cos,pi,sqrt,exp
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import *
G.MATS.update({m.name:m for m in bpy.data.materials});s=bpy.context.scene;random.seed(162)
# Preserve the underlying amphitheatre, rebuild weak contextual layers.
for ob in list(bpy.data.objects):
 if ob.name.startswith(('18 |','21 |','22 |','23 |','25 |','12 |')):bpy.data.objects.remove(ob,do_unlink=True)
# Recover only reusable architectural functions, without executing the old builder.
source=ast.parse((P.parent/'scripts/build_scene.py').read_text())
for n in source.body:
 if isinstance(n,ast.FunctionDef) and n.name in ['house','roof']:
  exec(compile(ast.Module(body=[n],type_ignores=[]),'toolkit','exec'))

def mat(name,c,rough=.65,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal;G.MATS[name]=m;return m
mat('Pale limestone plaster',(.57,.52,.43));mat('Warm lime plaster',(.56,.43,.29));mat('Faded rose plaster',(.39,.25,.18));mat('Garden earth',(.17,.19,.08),.96)
for i,c in enumerate([(.22,.071,.029),(.31,.106,.052),(.41,.19,.09),(.24,.14,.083)]):
 m=bpy.data.materials['Terracotta'].copy();m.name=f'Roof variation {i}';G.MATS[m.name]=m
 ns=m.node_tree.nodes;ls=m.node_tree.links;bs=ns.get('Principled BSDF');prev=bs.inputs['Base Color'].links[0].from_socket;mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.5;mix.inputs[2].default_value=(*[v/.42 for v in c],1);ls.new(prev,mix.inputs[1]);ls.new(mix.outputs[0],bs.inputs['Base Color'])
# Continuous terrain: local archaeological plateaux plus distant rolling ground.
def ground(x,y):
 base=28*exp(-((x+285)/165)**4-((y+235)/155)**4)+17*exp(-((x-90)/240)**4-((y-275)/140)**4)
 r=sqrt(x*x+y*y);far=max(0,min(1,(r-650)/900));h=far*(28+24*sin(x*.0021)*cos(y*.0018)+24*exp(-((x-1100)/550)**2-((y-1000)/600)**2))
 if (x/172)**2+(y/150)**2<1.5:return -.38
 if abs(x+273)<99 and abs(y+231)<85:return min(23.6,base-.4)
 return base+h-.4
with group('18 | Landscape — continuous rolling terrain'):
 n=220;v=[]
 for j in range(n+1):
  y=-5500+j*11000/n
  for i in range(n+1):
   x=-5500+i*11000/n;z=ground(x,y);v.append((x,y,z))
 geo(v,[(j*(n+1)+i,j*(n+1)+i+1,(j+1)*(n+1)+i+1,(j+1)*(n+1)+i) for j in range(n) for i in range(n)],'Earth',True)
# High resolution near-ground patch, below paving at all protected precincts.
with group('18b | Landscape — local contours'):
 n=160;v=[]
 for j in range(n+1):
  y=-800+j*1600/n
  for i in range(n+1):
   x=-800+i*1600/n;v.append((x,y,ground(x,y)+.015))
 geo(v,[(j*(n+1)+i,j*(n+1)+i+1,(j+1)*(n+1)+i+1,(j+1)*(n+1)+i) for j in range(n) for i in range(n)],'Earth',True)

def protected(x,y):
 return (x/181)**2+(y/158)**2<1 or (-350<x<-98 and -95<y<91) or (145<x<275 and -52<y<70) or (-390<x<-170 and -327<y<-135) or (-90<x<170 and 200<y<390)
# Irregular neighborhoods follow curved lanes and hill contours; roof terraces and
# courtyard ranges interrupt the repeated box/roof silhouette of version one.
cells={};buildings=[]
for attempt in range(22000):
 x=random.uniform(-1550,1550);y=random.uniform(-1550,1550);r=sqrt(x*x+y*y)
 if r>1580 or protected(x,y):continue
 # Interrupted arterial approaches, with narrow lanes through domestic blocks.
 if r<750 and (min(abs(y-q) for q in [-165,170,300,-340])<12 or min(abs(x-q) for q in [-390,170,310,455])<12):continue
 if abs(y-(.11*x+45*sin(x*.005)+470))<10:continue
 key=(int(x//30),int(y//30));near=[q for dx in [-1,0,1] for dy in [-1,0,1] for q in cells.get((key[0]+dx,key[1]+dy),[])]
 if any((x-a)**2+(y-b)**2<31**2 for a,b in near):continue
 cells.setdefault(key,[]).append((x,y));buildings.append((x,y))
with group('21 | City — irregular neighborhoods'):
 for idx,(x,y) in enumerate(buildings):
  r=sqrt(x*x+y*y);z=ground(x,y);w=random.uniform(13,23);d=random.uniform(12,22);h=random.choices([5.5,8.5,11.5,14.5,17.5],[18,30,28,17,7])[0]
  angle=.15*sin(y*.006)+(.0 if x<250 else .23)+random.uniform(-.12,.12)
  wall=random.choice(['Pale limestone plaster','Pale limestone plaster','Warm lime plaster','Faded rose plaster']);roofmat=f'Roof variation {idx%4}'
  with frame((x,y,z),angle):
   if r<680:
    house(0,0,0,w,d,h,wall)
    # Shop porticoes, roof access and restrained balconies add readable scale.
    if idx%4==0:
     box((0,-d/2-1.25,3.5),(w+1,2.7,.3),'Trim')
     for xx in [-w*.43,0,w*.43]:column(xx,-d/2-2.2,0,3.3,.16,0,'Trim',False)
    if idx%3==0:
     box((0,-d/2-.65,h-2.7),(w*.45,1.5,.2),'Timber')
     for xx in [-w*.22,0,w*.22]:box((xx,-d/2-1.35,h-2.2),(.1,.1,1.0),'Timber')
     box((0,-d/2-1.35,h-1.7),(w*.47,.12,.1),'Timber')
   else:
    box((0,0,h/2),(w,d,h),wall);roof(0,0,h,w+.6,d+.6,min(3,d*.19),roofmat)
   # Smaller adjoining wings make each silhouette less uniform.
   if idx%3==1:
    hh=h*.59;box((w*.4,d*.45,hh/2),(w*.7,d*.5,hh),wall);roof(w*.4,d*.45,hh,w*.7+.5,d*.5+.5,1.5,roofmat)
   if idx%7==0:
    box((-w*.25,0,h+1.3),(w*.22,d*.28,2.5),wall);roof(-w*.25,0,h+2.55,w*.22+.3,d*.28+.3,.8,roofmat)
print('CITY',len(buildings),flush=True)
# Complete classical figure proxies: retain the intact Roman youth, replace the
# fragmentary Cypriot statues with a complete Perseus mesh. Interpretation explicit.
col=bpy.data.collections.get('05 | Colosseum — sculpture');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(P/'assets/met_204758.glb'));bpy.context.view_layer.update();imp=set(bpy.data.objects)-before;verts=[];faces=[]
for ob in imp:
 if ob.type!='MESH':continue
 off=len(verts);verts.extend([ob.matrix_world@v.co for v in ob.data.vertices]);faces.extend([tuple(off+i for i in f.vertices) for f in ob.data.polygons])
lo=Vector(tuple(min(v[i] for v in verts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in verts) for i in range(3)));center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));height=hi.z-lo.z
me=bpy.data.meshes.new('Complete classical figure — Perseus proxy');me.from_pydata([(v-center)/height for v in verts],[],faces);me.update();ob=bpy.data.objects.new('Sculpture master',me);col.objects.link(ob)
bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;dec=ob.modifiers.new('Film scale detail','DECIMATE');dec.ratio=min(1,30000/max(1,len(me.polygons)));bpy.ops.object.modifier_apply(modifier=dec.name);me=ob.data
statmat=mat('Sculptural ivory marble',(.72,.69,.62),.35);bs=statmat.node_tree.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.045;bs.inputs['Subsurface Radius'].default_value=(.5,.3,.18)
me.materials.append(statmat)
for p in me.polygons:p.use_smooth=True
for q in imp:bpy.data.objects.remove(q,do_unlink=True)
for q in list(bpy.data.objects):
 if q.name.startswith('Order ') and q.type=='MESH':
  if '254613' not in q.data.name:q.data=me;q.scale=(3.8,3.8,3.8)
  else:
   if q.data.materials:q.data.materials[0]=statmat
bpy.data.objects.remove(ob,do_unlink=True)
# Small social groups and people following circulation paths, with quiet poses.
with group('12 | Public life — gathered groups and circulation'):
 for k in range(145):
  t=random.uniform(0,2*pi);r=random.uniform(1.16,1.48);cx=94.5*r*cos(t);cy=78*r*sin(t)
  if -150<cx<-110 and -85<cy<40:continue
  for j in range(random.choice([2,3,3,4])):
   a=j*2*pi/3+random.uniform(-.3,.3);x=cx+cos(a)*random.uniform(.7,1.4);y=cy+sin(a)*random.uniform(.7,1.4)
   with frame((x,y,.19),a+pi/2):human(0,0,0,random.uniform(.88,1.03),random.choices(['Toga','Linen','Rust','Umber','Indigo'],[5,5,1,2,1])[0],False,0)
 for x,y in [(-18,3),(-16,4),(14,-5),(16,-4),(0,14)]:
  with frame((x,y,.72),.6):human(0,0,0,.95,'Toga',False,0)
flush()
# Atmosphere and physically coherent low sunlight. Density builds outside the
# hero precinct, preserving close-up contrast while softening distant geometry.
sun=bpy.data.lights['Late afternoon sun'];sun.energy=3.3;sun.color=(1,.82,.64);sun.angle=.012
bpy.data.objects['Late afternoon sun'].rotation_euler=Vector((.65,.76,-.32)).to_track_quat('-Z','Y').to_euler()
sky=next(n for n in s.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=.31;sky.sun_rotation=3.85;s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.035
bpy.data.lights['Open sky above the cavea'].energy=18000
vol=bpy.data.materials['Distant golden air'];ns=vol.node_tree.nodes;ls=vol.node_tree.links;bs=ns.get('Principled Volume');bs.inputs['Color'].default_value=(.72,.79,.86,1);bs.inputs['Anisotropy'].default_value=.3
pos=ns.new('ShaderNodeTexCoord');dist=ns.new('ShaderNodeVectorMath');dist.operation='LENGTH';ls.new(pos.outputs['Object'],dist.inputs[0])
# World geometry coordinates provide a consistent radial density field.
geoNode=ns.new('ShaderNodeNewGeometry');ls.new(geoNode.outputs['Position'],dist.inputs[0]);mapn=ns.new('ShaderNodeMapRange');mapn.inputs['From Min'].default_value=160;mapn.inputs['From Max'].default_value=1400;mapn.inputs['To Min'].default_value=.00010;mapn.inputs['To Max'].default_value=.00105;ls.new(dist.outputs['Value'],mapn.inputs[0]);ls.new(mapn.outputs[0],bs.inputs['Density'])
# Linen transmits soft light rather than behaving like painted solid plastic.
m=bpy.data.materials['Linen'];ns=m.node_tree.nodes;ls=m.node_tree.links;bs=ns.get('Principled BSDF');out=ns.get('Material Output');tr=ns.new('ShaderNodeBsdfTranslucent');tr.inputs['Color'].default_value=(.72,.65,.49,1);mix=ns.new('ShaderNodeMixShader');mix.inputs[0].default_value=.22;ls.new(bs.outputs[0],mix.inputs[1]);ls.new(tr.outputs[0],mix.inputs[2]);ls.new(mix.outputs[0],out.inputs['Surface'])
s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.0
# Continuous movement with no focal-length retreat in the opening.
keys=[(1,(-245,-335,125),(-8,0,22),48),(193,(-130,-186,69),(0,-8,26),39),(361,(-21,-121,34),(12,-31,27),33),(505,(91,-102,70),(0,-8,20),31),(720,(101,61,146),(-9,-6,13),36)]
def interp(f,c):
 i=next((i for i in range(len(keys)-1) if keys[i][0]<=f<=keys[i+1][0]),len(keys)-2);a,b=keys[i:i+2];dt=b[0]-a[0];u=(f-a[0])/dt
 def v(j):q=keys[j][c];return Vector(q) if isinstance(q,tuple) else q
 p0,p1=v(i),v(i+1);m0=(p1-v(max(0,i-1)))/(keys[i+1][0]-keys[max(0,i-1)][0]);m1=(v(min(len(keys)-1,i+2))-p0)/(keys[min(len(keys)-1,i+2)][0]-keys[i][0])
 return (2*u**3-3*u*u+1)*p0+(u**3-2*u*u+u)*dt*m0+(-2*u**3+3*u*u)*p1+(u**3-u*u)*dt*m1
cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear();cam.data.clip_end=12000;cam.data.dof.use_dof=False;clearance=[]
for f in range(1,721):
 pos=interp(f,1);target=interp(f,2);cam.location=pos;cam.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler();cam.data.lens=interp(f,3);cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f);cam.data.keyframe_insert('lens',frame=f)
 if pos.z<60:clearance.append(sqrt((pos.x/95)**2+(pos.y/79)**2))
assert min(clearance)>1.2
(P/'camera_validation.json').write_text(json.dumps({'frames':720,'minimum_horizontal_clearance_ratio_below_masts':min(clearance)},indent=2));(P/'shot_manifest.json').write_text(json.dumps({'fps':24,'frames':720,'keyframes':keys},indent=2))
s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.045;s.cycles.max_bounces=5;s.cycles.diffuse_bounces=3;s.cycles.glossy_bounces=3;s.cycles.volume_bounces=1;s.render.use_motion_blur=True;s.render.motion_blur_shutter=.24
s.render.resolution_percentage=100;s.frame_set(1)
(P/'SCENE_PLAN.md').write_text((P/'SCENE_PLAN.md').read_text()+'''\n## Cinematic revision\n\nVersion two preserves the amphitheatre dimensions while replacing the uniform background with irregular neighborhoods and continuous rolling terrain. Lower sunlight, spatially varying haze, translucent linen, quieter crowd groupings and a rebuilt camera path strengthen depth and visual continuity. Fragmentary arcade figures are replaced by complete classical proxies; the Canova Perseus remains explicitly a later artistic stand-in, not a historically identified Colosseum statue. The distant topography and neighborhood plans are compositional reconstructions, not a surveyed model of ancient Rome.\n''')
t=bpy.data.texts['READ ME — scene and evidence'];t.clear();t.write((P/'SCENE_PLAN.md').read_text());bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'));print('REVISION SAVED',flush=True)
