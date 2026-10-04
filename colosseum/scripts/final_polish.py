import bpy,sys,math,random
from pathlib import Path
from mathutils import Vector,Matrix
from math import sin,cos,pi,sqrt
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import *
G.MATS.update({m.name:m for m in bpy.data.materials});s=bpy.context.scene;random.seed(260)
# Hard spatial constraints: the public precinct is level, as are the palace terraces.
for ob in bpy.data.objects:
 if ob.type=='MESH' and ob.name.startswith('18 |'):
  for v in ob.data.vertices:
   x,y,z=v.co
   if (x/170)**2+(y/145)**2<1.6:v.co.z=min(z,-.42)
   elif abs(x+273)<98 and abs(y+231)<85:v.co.z=min(z,23.6)
   else:v.co.z-=.38
# A physically colored daylight sky gives the stone a cooler shadow side.
n=s.world.node_tree.nodes;l=s.world.node_tree.links
for x in list(n):n.remove(x)
sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=.47;sky.sun_rotation=3.8;
for prop,value in [('air_density',1.0),('dust_density',.6),('ozone_density',1.1)]:
 if hasattr(sky,prop):setattr(sky,prop,value)
bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.18;l.new(sky.outputs[0],bg.inputs[0]);out=n.new('ShaderNodeOutputWorld');l.new(bg.outputs[0],out.inputs[0])
bpy.data.lights['Late afternoon sun'].energy=4.4;bpy.data.lights['Late afternoon sun'].color=(1,.85,.66)
bpy.data.lights['Open sky above the cavea'].energy=45000
v=bpy.data.objects['Atmospheric depth'];v.location=(0,0,225);v.scale=(6000,6000,300)
bpy.data.materials['Distant golden air'].node_tree.nodes.get('Principled Volume').inputs['Density'].default_value=.00014
s.view_settings.exposure=-.1
mat=bpy.data.materials['Earth'];ramp=next(x for x in mat.node_tree.nodes if x.type=='VALTORGB');ramp.color_ramp.elements[0].color=(.24,.19,.10,1);ramp.color_ramp.elements[1].color=(.39,.31,.19,1)
# Modest sheen on heavy linen, no glossy plastic surface.
bs=bpy.data.materials['Linen'].node_tree.nodes.get('Principled BSDF');bs.inputs['Sheen Weight'].default_value=.35
# A continuous distant city, without spending geometry on invisible ornament.
with group('25 | Distant Rome — horizon fabric'):
 for x0 in range(-2650,2651,48):
  for y0 in range(-2650,2651,47):
   if abs(x0)<760 and abs(y0)<760:continue
   if x0*x0+y0*y0>2700*2700 or random.random()<.05:continue
   x=x0+random.uniform(-6,6);y=y0+random.uniform(-6,6);w=random.uniform(31,43);d=random.uniform(29,41);h=random.uniform(7,20);z=-.15
   box((x,y,z+h/2),(w,d,h),random.choice(['Plaster','Ochre','RosePlaster']))
   geo([(x-w/2-1,y-d/2-1,z+h),(x+w/2+1,y-d/2-1,z+h),(x-w/2-1,y+d/2+1,z+h),(x+w/2+1,y+d/2+1,z+h),(x-w/2-1,y,z+h+4),(x+w/2+1,y,z+h+4)],[(0,1,5,4),(2,4,5,3),(0,4,2),(1,3,5)],'Terracotta')
# More legible bath architecture: monumental clerestories and vaulted roofs,
# rather than small domestic windows on warehouse-sized halls.
for ob in list(bpy.data.objects):
 if ob.name.startswith('20 |') and any(k in ob.name for k in ['Window','Terracotta']):bpy.data.objects.remove(ob,do_unlink=True)
with group('20b | Oppian — thermal hall vaults'):
 z=17.0
 for cx in [14,38,62]:
  points=[(cx+12.6*cos(pi*i/40),z+26+12.6*sin(pi*i/40)) for i in range(41)]
  polyprism(points,283,341,'Terracotta')
  # Thermal windows in the tall front wall.
  for side in [-1,1]:
   yy=283 if side==-1 else 341
   pts=[(-6,0),(6,0)]+[(6*cos(pi*i/24),6*sin(pi*i/24)) for i in range(25)]
   with frame((cx,yy-.12,34)):
    polyprism(pts,-.04,.04,'Window');arc(6,6.38,0,-.08,.1,'Trim',24,.003)
    for xx in [-2.0,2.0]:box((xx,-.08,2.55),(.35,.32,5.1),'Trim')
 for x,y,w,d,h in [(-27,292,40,70,18),(103,292,40,70,18),(38,243,128,25,15)]:
  geo([(x-w/2,y-d/2,z+h),(x+w/2,y-d/2,z+h),(x-w/2,y+d/2,z+h),(x+w/2,y+d/2,z+h),(x-w/2,y,z+h+4),(x+w/2,y,z+h+4)],[(0,1,5,4),(2,4,5,3),(0,4,2),(1,3,5)],'Terracotta')
# Lobed acanthus and corner volutes on the Corinthian order.
with group('02c | Colosseum — carved acanthus capitals'):
 for bay in range(80):
  t=bay*2*pi/80;tan=Vector((-93.35*sin(t),76.85*cos(t),0)).normalized();normal=Vector((tan.y,-tan.x,0));m=Matrix(((tan.x,normal.x,0,93.35*cos(t)),(tan.y,normal.y,0,76.85*sin(t)),(0,0,1,24.45),(0,0,0,1)))
  with frame(matrix=m):
   for ring in [0,1]:
    for i in range(8):
     a=2*pi*(i+ring*.5)/8;verts=[]
     for j in range(13):
      u=j/12;r=.43+.23*u*u;zz=8.0+ring*.22+.56*u-.12*u**6;ww=.035+.12*sin(pi*u)**.7*(.73+.27*cos(u*10*pi))
      for k in [-1,0,1]:verts.append((r*cos(a)+k*ww*sin(a),1.23+r*sin(a)-k*ww*cos(a)-.035*(1-k*k),zz))
     geo(verts,[(j*3+k,j*3+k+1,(j+1)*3+k+1,(j+1)*3+k) for j in range(12) for k in [0,1]],'Trim',True)
   for a in [pi/4,3*pi/4,5*pi/4,7*pi/4]:
    pts=[]
    for j in range(22):
     tt=j/21*2.6*pi;rr=.16*(1-j/28);rad=.51+rr*cos(tt);pts.append((rad*cos(a),1.23+rad*sin(a),8.67+rr*sin(tt)))
    rope(pts,.025,'Trim',6)
flush()
# Reduce distracting convexity of the attic roundels; keep their original position.
ob=next((o for o in bpy.data.objects if o.name.startswith('03 |') and 'Bronze' in o.name),None)
if ob:
 for v in ob.data.vertices:
  theta=math.atan2(v.co.y/76.85,v.co.x/93.35);i=round(theta/(2*pi/80)-.5);t=(i+.5)*2*pi/80
  normal=Vector((cos(t)/93.35,sin(t)/76.85,0)).normalized();center=Vector((93.35*cos(t),76.85*sin(t),0));depth=(v.co-center).dot(normal);v.co-=normal*(depth-1.12)*.72
# Production settings are saved in the editable source as well as the render script.
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.eevee.use_raytracing=True

for prop,value in [('shadow_resolution_scale',.5),('shadow_ray_count',1),('shadow_step_count',6)]:
 if hasattr(s.eevee,prop):setattr(s.eevee,prop,value)
for light in bpy.data.lights:
 try:light.use_shadow_jitter=False;light.shadow_maximum_resolution=.15
 except:pass
s.render.resolution_percentage=100;s.render.use_motion_blur=True;s.render.motion_blur_shutter=.32;s.frame_set(1)
text=(P/'SCENE_PLAN.md').read_text()+'''\n## Final production refinements\n\nProtected level surfaces resolve the amphitheatre precinct, fountain basin and palace terrace against the wider terrain. The distant city uses a simpler mesh treatment beyond the detailed neighborhood, maintaining a continuous inhabited horizon. A physical atmosphere sky and directional sun provide the final daylight; the downloaded HDR is retained as a research asset. Corinthian capitals include modeled acanthus and volutes. The bath precinct uses vaulted thermal halls and large clerestories.\n\nProduction output: 1920 x 1080, 24 fps, 720 native rendered frames, Eevee with 32 temporal samples, ray tracing, restrained motion blur, and AgX color management. Each frame is written to a temporary path then atomically renamed. The render controller resumes completed frames and verifies the final encoded movie.\n'''
(P/'SCENE_PLAN.md').write_text(text);t=bpy.data.texts['READ ME — scene and evidence'];t.clear();t.write(text)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
print('FINAL POLISH COMPLETE',flush=True)
