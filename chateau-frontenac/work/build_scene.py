import bpy, math, random, json, os, sys, time
from mathutils import Vector
from math import sin,cos,pi,sqrt
random.seed(412)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'outputs');WORK=os.path.join(ROOT,'work')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials):bpy.data.materials.remove(d)
scene=bpy.context.scene
COL={}
def collection(n):
 if n not in COL:
  c=bpy.data.collections.new(n);scene.collection.children.link(c);COL[n]=c
 return COL[n]
def material(n,color,rough=.65,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m
brick=material('Warm historic red brick',(0.30,.107,.062))
stone=material('Pale grey limestone',(.51,.49,.43))
copper=material('Weathered verdigris copper',(.105,.23,.185),.56,.42)
seam=material('Raised copper seams',(.065,.14,.105),.48,.5)
iron=material('Deep green painted iron',(.018,.063,.046),.34,.6)
white=material('Aged ivory paint',(.78,.77,.66),.55)
wood=material('Weathered terrace cedar',(.39,.31,.22),.83)
slate=material('Blue grey standing seam',(.14,.18,.21),.6,.2)
asphalt=material('Warm grey street',(.16,.165,.16),.93)
grass=material('Grass',(.12,.19,.043),.95)
earth=material('Earth and escarpment',(.13,.14,.084),1)
trunk=material('Bark',(.15,.095,.049),.95)
dark=material('Deep window recess',(.008,.013,.014),.75)
water=material('St Lawrence water',(.055,.115,.14),.2,.3)
bronze=material('Patinated bronze',(.055,.092,.072),.56,.68)
glass=[]
for i in range(8):
 m=material('Window reflection %02d'%i,(.035+i*.006,.065+i*.008,.078+i*.010),.17,.46)
 if i==7:
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.29,.20,.11,1);p.inputs['Emission Color'].default_value=(.7,.38,.12,1);p.inputs['Emission Strength'].default_value=.25
 glass.append(m)
foliage=[material('Leaf tone %02d'%i,c,.86) for i,c in enumerate([(.055,.13,.018),(.095,.20,.028),(.18,.27,.044),(.26,.29,.060),(.07,.17,.03),(.32,.24,.056)])]
for m in foliage:
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.08;p.inputs['Subsurface Radius'].default_value=(.25,.5,.1)
# Shader textures in physical metres, with smaller-scale surface relief.
def noise_surface(m,c1,c2,scale,bump=.07,detail=3):
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale;tex.inputs['Detail'].default_value=detail
 coord=n.new('ShaderNodeTexCoord');l.new(coord.outputs['Generated'],tex.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(*c1,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(*c2,1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.3;b.inputs['Distance'].default_value=bump;l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
noise_surface(copper,(.045,.095,.056),(.16,.24,.14),35,.025,5)
noise_surface(stone,(.31,.30,.27),(.52,.49,.43),210,.025)
noise_surface(earth,(.075,.083,.045),(.24,.25,.15),65,.5)
noise_surface(grass,(.06,.12,.016),(.22,.29,.065),180,.045)
noise_surface(trunk,(.055,.032,.017),(.20,.13,.067),90,.03)
n=brick.node_tree.nodes;l=brick.node_tree.links;p=n.get('Principled BSDF');uv=n.new('ShaderNodeTexCoord');b=n.new('ShaderNodeTexBrick');l.new(uv.outputs['UV'],b.inputs['Vector']);b.inputs['Color1'].default_value=(.37,.135,.075,1);b.inputs['Color2'].default_value=(.20,.063,.034,1);b.inputs['Mortar'].default_value=(.30,.25,.19,1);b.inputs['Scale'].default_value=1;b.inputs['Mortar Size'].default_value=.009;b.inputs['Mortar Smooth'].default_value=.004;b.inputs['Brick Width'].default_value=.29;b.inputs['Row Height'].default_value=.095;l.new(b.outputs['Color'],p.inputs['Base Color']);bu=n.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.45;bu.inputs['Distance'].default_value=.02;l.new(b.outputs['Fac'],bu.inputs['Height']);l.new(bu.outputs[0],p.inputs['Normal'])
n=wood.node_tree.nodes;l=wood.node_tree.links;p=n.get('Principled BSDF');uv=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(.7,65,3);l.new(uv.outputs['UV'],mapping.inputs[0]);tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=1;tex.inputs['Detail'].default_value=3;l.new(mapping.outputs[0],tex.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.19,.15,.105,1);r.color_ramp.elements[1].color=(.51,.43,.32,1);l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color']);bu=n.new('ShaderNodeBump');bu.inputs['Distance'].default_value=.012;bu.inputs['Strength'].default_value=.32;l.new(tex.outputs['Fac'],bu.inputs['Height']);l.new(bu.outputs[0],p.inputs['Normal'])
n=water.node_tree.nodes;l=water.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=260;tex.inputs['Detail'].default_value=3;bu=n.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.34;bu.inputs['Distance'].default_value=.32;l.new(tex.outputs['Fac'],bu.inputs['Height']);l.new(bu.outputs[0],p.inputs['Normal'])
# Material-batched mesh builder, keeps scene light despite thousands of details.
class Batch:
 def __init__(self,name):self.name=name;self.v=[];self.f=[];self.mi=[];self.mats=[]
 def add(self,verts,faces,mat):
  off=len(self.v);self.v.extend(verts);self.f.extend([tuple(off+i for i in f) for f in faces]);
  if mat not in self.mats:self.mats.append(mat)
  self.mi.extend([self.mats.index(mat)]*len(faces))
 def finish(self,col):
  me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.materials.clear()
  for m in self.mats:me.materials.append(m)
  me.update();ob=bpy.data.objects.new(self.name,me);collection(col).objects.link(ob)
  uv=me.uv_layers.new(name='Metres')
  for poly,idx in zip(me.polygons,self.mi):
   poly.material_index=idx;normal=poly.normal;axis=max(range(3),key=lambda k:abs(normal[k]));axes=[(1,2),(0,2),(0,1)][axis]
   for li in poly.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
  return ob
B=Batch('Chateau masonry, roofs and ornament')
def box(c,s,m=stone,a=0,b=None):
 b=b or B;x,y,z=c;w,d,h=[v/2 for v in s];verts=[]
 for xx,yy,zz in [(-w,-d,-h),(w,-d,-h),(w,d,-h),(-w,d,-h),(-w,-d,h),(w,-d,h),(w,d,h),(-w,d,h)]:verts.append((x+xx*cos(a)-yy*sin(a),y+xx*sin(a)+yy*cos(a),z+zz))
 b.add(verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],m)
def rod(p,q,r,m=iron,n=8,b=None,r2=None):
 b=b or B;p=Vector(p);q=Vector(q);v=q-p;t=v.normalized();u=t.cross(Vector((0,0,1)))
 if u.length<.01:u=t.cross(Vector((0,1,0)))
 u.normalize();w=t.cross(u);vs=[]
 for c,rr in [(p,r),(q,r if r2 is None else r2)]:
  for i in range(n):vs.append(tuple(c+rr*(cos(2*pi*i/n)*u+sin(2*pi*i/n)*w)))
 b.add(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],m)
def cyl(x,y,z,r,h,m=stone,n=24,b=None,r2=None):rod((x,y,z),(x,y,z+h),r,m,n,b,r2)
def ball(c,r,m,b=None,scale=(1,1,1),n=10,rings=6):
 b=b or B;vs=[]
 for j in range(rings+1):
  th=pi*j/rings
  for i in range(n):
   ph=2*pi*i/n;vs.append((c[0]+r*sin(th)*cos(ph)*scale[0],c[1]+r*sin(th)*sin(ph)*scale[1],c[2]+r*cos(th)*scale[2]))
 b.add(vs,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(rings) for i in range(n)],m)
def hip(x,y,z,w,d,h,m=copper,a=0,b=None):
 b=b or B
 # flat ridge along longest axis
 if d>w:vs=[(-w/2,-d/2,0),(w/2,-d/2,0),(w/2,d/2,0),(-w/2,d/2,0),(0,-d/2+w*.40,h),(0,d/2-w*.40,h)]
 else:vs=[(-w/2,-d/2,0),(w/2,-d/2,0),(w/2,d/2,0),(-w/2,d/2,0),(-w/2+d*.4,0,h),(w/2-d*.4,0,h)]
 fs=[(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5)] if d>w else [(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]
 pts=[(x+u*cos(a)-v*sin(a),y+u*sin(a)+v*cos(a),z+t) for u,v,t in vs];b.add(pts,fs,m)
 # Fine standing seams drawn across each trapezoid or triangle as interpolated strips.
 for face in fs:
  p0,p1=Vector(pts[face[0]]),Vector(pts[face[1]]);q0=Vector(pts[face[-1]]);q1=Vector(pts[face[2]]) if len(face)==4 else q0
  count=max(2,int((p1-p0).length/.65))
  for i in range(1,count):
   t=i/count;aa=p0.lerp(p1,t);bb=q0.lerp(q1,t);aa.z+=.025;bb.z+=.025;rod(aa,bb,.018,seam,5,b)
def win(x,y,z,w=1.25,h=2.0,a=0,mat=None,b=None,trim=True):
 b=b or B
 def bx(dx,dy,dz,s,m):box((x+dx*cos(a)-dy*sin(a),y+dx*sin(a)+dy*cos(a),z+dz),s,m,a,b)
 bx(0,0,0,(w+.18,.07,h+.18),dark);bx(0,.047,0,(w,.045,h),mat or random.choice(glass));
 if trim:
  for dx in [-w/2-.10,w/2+.10]:bx(dx,.065,0,(.16,.23,h+.42),stone)
  for dz in [-h/2-.12,h/2+.12]:bx(0,.065,dz,(w+.36,.28,.18),stone)
 bx(0,.105,0,(.055,.08,h),white);bx(0,.105,.12,(w,.08,.06),white)
 bx(0,.12,-h*.27,(w,.06,.035),white)
def dormer(x,y,z,w=1.6,h=2.0,a=0,b=None):
 b=b or B
 box((x,y,z+h/2),(w+.5,1.2,h),stone,a,b);win(x-.63*sin(a),y+.63*cos(a),z+h*.48,w,h*.7,a,b=b)
 local=[(-w*.66,-.6,h),(w*.66,-.6,h),(0,-.6,h+1.45),(-w*.66,.72,h),(w*.66,.72,h),(0,.72,h+1.45)]
 vs=[(x+u*cos(a)-v*sin(a),y+u*sin(a)+v*cos(a),z+t) for u,v,t in local];b.add(vs,[(0,1,2),(3,5,4)],brick);b.add(vs,[(0,2,5,3),(2,1,4,5)],copper)
 for u in [-1,1]:rod((x+u*w*.67*cos(a)-.77*sin(a),y+u*w*.67*sin(a)+.77*cos(a),z+h),(x-.77*sin(a),y+.77*cos(a),z+h+1.5),.075,stone,6,b)
def facade(x,y,length,height,floors,a=0,b=None,spacing=3.2):
 b=b or B;n=max(1,int(length/spacing));step=length/n
 for f in range(floors):
  z=2.1+f*3.65
  if z+1.2>height:continue
  for k in range(n):
   u=-length/2+step*(k+.5);win(x+u*cos(a),y+u*sin(a),z,1.22,2.05,a,b=b)
 for z in [4.05,height-.45,height-.12]:box((x,y,z),(length+.2,.38,.23),stone,a,b)
def wing(x,y,w,d,height=23,a=0,b=None,roofh=10,front=True):
 b=b or B;box((x,y,height/2),(w,d,height),brick,a,b);box((x,y,1.5),(w+.1,d+.1,3),stone,a,b)
 for dz in [3.2,7.7,15.0,height-.4,height]:box((x,y,dz),(w+.35,d+.35,.23 if dz<height else .45),stone,a,b)
 hip(x,y,height+.2,w+1,d+1,roofh,a=a,b=b)
 for side in [-1,1]:
  ang=a if side==1 else a+pi;xx=x-side*d/2*sin(a);yy=y+side*d/2*cos(a);facade(xx,yy,w,height,int(height/3.65),ang,b)
  for k in range(max(1,int(w/4.5))):
   u=-w/2+2.3+k*4.5
   if u>w/2-1:continue
   dormer(x+u*cos(a)-side*(d/2-.75)*sin(a),y+u*sin(a)+side*(d/2-.75)*cos(a),height+.2,1.4,1.85,ang,b)
 for side in [-1,1]:
  ang=a-side*pi/2;facade(x+side*w/2*cos(a),y+side*w/2*sin(a),d,height,int(height/3.65),ang,b)
def turret(x,y,r=4,height=25,roofh=11,b=None):
 b=b or B;cyl(x,y,0,r,height,brick,40,b)
 for z,hh in [(0,3),(7.2,.27),(14.5,.25),(height-3,3)]:cyl(x,y,z,r+.13,hh,stone,40,b)
 for f in range(int(height/3.65)):
  for i in range(max(6,int(r*1.5))):
   a=2*pi*i/max(6,int(r*1.5));win(x+(r+.02)*cos(a),y+(r+.02)*sin(a),2.1+f*3.65,1.15,1.9,a-pi/2,b=b)
 cyl(x,y,height,r+.45,.4,stone,40,b);cyl(x,y,height+.4,r+.6,roofh,copper,48,b,.03)
 for i in range(32):
  a=2*pi*i/32;rod((x+(r+.6)*cos(a),y+(r+.6)*sin(a),height+.4),(x,y,height+roofh+.4),.022,seam,5,b)
 rod((x,y,height+roofh),(x,y,height+roofh+3),.065,iron,8,b);ball((x,y,height+roofh+.8),.15,bronze,b)
# Plan dimensions reconstructed against OSM and photographic silhouette.
wing(-28,28,110,16,23,roofh=10.5)
wing(-78,5,19,58,23,roofh=12)
wing(-28,-32,44,19,22,roofh=10)
wing(5,-31,22,22,28,roofh=13)
wing(28,-31,28,17,24,roofh=12)
# northeast diagonal wing (actual offset footprint)
wing(47,18,16,36,24,a=-.51,roofh=11)
wing(50,-18,18,28,25,a=.42,roofh=10)
# Front prominent round bays and the corner turrets.
turret(59,-1,8,25,13)
turret(27,36.5,4.1,25,11)
wing(-44,28,18,17,28,roofh=14)
turret(-65,33,2,25,8)
turret(-90,33,2.2,25,7)
turret(46,-34,5.5,28,12)
turret(42,-1,3.3,28,9)
# Great central tower: rectangular, fourteen levels, elaborate stone crown.
box((5,.5,28.6),(21.4,42,57.2),brick)
for z in [1.7,4.5,39.5,40.5,53.8,57.1]:box((5,.5,z),(22,42.6,.34 if z<53 else .65),stone)
for side in [-1,1]:
 facade(5,.5+side*21,21.4,56,15,0 if side==1 else pi,spacing=3.05)
 facade(5+side*10.7,.5,42,56,15,-side*pi/2,spacing=3.15)
# quoins, buttress accents and corbel balcony band
for xx in [-5.75,15.75]:
 for yy in [-20.55,21.55]:
  for z in [i*.65+.35 for i in range(86)]:box((xx,yy,z),(1.15,1.05,.51),stone)
  cyl(xx,yy,40,1.55,17,stone,16);cyl(xx,yy,57,1.8,8.6,copper,24,B,.04);rod((xx,yy,65.6),(xx,yy,68),.055,iron)
for side in [-1,1]:
 for j in range(52):
  y=-20+j*.80;box((5+side*10.95,y,40.1),(.6,.22,1.05),stone)
 for j in range(26):box((-5+j*.82,.5+side*21.25,40.1),(.22,.6,1.05),stone)
hip(5,.5,57.4,22.7,43.3,20.8)
# Great stone crown and recessed double-height windows.
for side in [-1,1]:
 for j in range(5):
  yy=-14+j*7
  box((5+side*10.9,yy,59.3),(.8,2.9,4.0),stone)
  win(5+side*11.33,yy,59.4,1.7,3.3,-side*pi/2)
# Huge gabled dormers, plus small rows recessed into the high roof.
for side in [-1,1]:
 for j in range(5):
  y=-14+j*7;dormer(5+side*10.0,y,59.6,2.3,3.4,-side*pi/2)
 for j in range(3):dormer(5+side*7.0,-10+j*10,65.0,1.15,1.4,-side*pi/2)
 for j in range(3):dormer(5+side*3.8,-10+j*10,72.0,.75,.7,-side*pi/2)
 for j in range(3):dormer(-1+j*6,.5+side*20.2,57.5,2.2,4.3,0 if side==1 else pi)
for y in [-12.1,13.1]:rod((5,y,77.9),(5,y,83.3),.07,iron);ball((5,y,79),.20,bronze)
# Decorative corbel frieze on the river wing.
for x in range(-81,23):
 if x%2==0:box((x,36.25,22.3),(.22,.4,.65),stone)
# Chimneys, copper flashing and dark conservatory bay.
for x,y,z in [(-73,17,32),(-60,27,31),(-29,28,31),(-14,-32,30),(32,-30,33),(50,10,33)]:
 box((x,y,z+1.6),(1.2,1.45,3.2),brick);box((x,y,z+3.2),(1.5,1.8,.25),stone)
for x,y,w in [(-15,37.5,21),(52,19,9)]:
 box((x,y,4.4),(w,4.5,4),stone);box((x,y+2.4,6.3),(w,1,3.5),glass[2]);hip(x,y,8.1,w+1,5.2,1.8,iron)
 for u in range(int(w)):
  box((x-w/2+u,y+2.96,6.25),(.10,.15,3.6),iron)
# Ground-level arched entrance appearance with real voussoir blocks.
def arch(x,y,z,w,h,a=0,b=None):
 b=b or B;win(x,y,z+h/2,w,h,a,glass[0],b)
 for i in range(13):
  t=pi*i/12;dx=(w/2+.16)*cos(t);dz=(w/2+.16)*sin(t)
  box((x+dx*cos(a)-.04*sin(a),y+dx*sin(a)+.04*cos(a),z+h/2+dz),(.27,.32,.29),stone,a,b)
for x in [-70,-57,-33,-21,-9,4,15]:arch(x,36.3,.1,2.0,3.6)
hotel=B.finish('01 Château | architecture')
bev=hotel.modifiers.new('Masonry edge highlights','BEVEL');bev.width=.045;bev.segments=2;bev.limit_method='ANGLE';bev.angle_limit=.60
print('HOTEL',len(B.v),flush=True)
# Terrace and landscape.
B=Batch('Boardwalk, pavilions, railings and furniture')
box((-35,63,-.5),(300,44,1),stone)
# Individual narrow cedar boards, avoiding a flat texture close to the camera.
for j in range(218):
 y=41.25+j*.20
 for i in range(31):box((-184+i*9.65+(4.82 if j%2 else 0),y,.028),(9.62,.193,.10),wood)
# Terrace retaining face and pillars.
box((-35,85,-4),(300,1.4,8),stone)
for x in range(-184,116,6):box((x,85,-4),(1.1,1.9,8.4),stone)
# Boardwalk near the east end turns north toward the monument.
box((89,17,-.4),(44,88,.8),stone)
for j in range(218):box((89,-26+j*.4,.035),(43.9,.388,.11),wood)
def railing(p,q):
 p=Vector(p);q=Vector(q);n=int((q-p).length/.28);t=(q-p).normalized()
 for z in [.14,.94,1.14]:rod(p+Vector((0,0,z)),q+Vector((0,0,z)),.034,iron)
 for i in range(n+1):
  r=p.lerp(q,i/n);rod(r+Vector((0,0,.12)),r+Vector((0,0,1.13)),.019,iron,6)
 for i in range(int((q-p).length/2.5)+1):
  r=p+t*i*2.5;rod(r,r+Vector((0,0,1.32)),.059,iron,8);ball(r+Vector((0,0,1.35)),.087,iron)
railing((-185,85,0),(115,85,0));railing((111,85,0),(111,-26,0))
def gazebo(x,y,r=4.5):
 cyl(x,y,.1,r,.5,iron,16)
 for i in range(8):
  a=2*pi*i/8;xx=x+r*.87*cos(a);yy=y+r*.87*sin(a);rod((xx,yy,.5),(xx,yy,4),.075,iron,10)
  ball((xx,yy,3.6),.13,white)
  for side in [-1,1]:
   da=side*.36;rod((xx,yy,3.0),(x+r*.87*cos(a+da),y+r*.87*sin(a+da),4),.032,iron,6)
 # Curved tent profile, alternating twenty-four ivory/green metal gores.
 n=32;rings=[(r*1.12,3.95),(r*.86,4.13),(r*.52,4.63),(r*.16,5.42),(.05,5.70)];vs=[]
 for rr,z in rings:
  for i in range(n):vs.append((x+rr*cos(2*pi*i/n),y+rr*sin(2*pi*i/n),z))
 for j in range(4):
  for i in range(n):B.add([vs[j*n+i],vs[j*n+(i+1)%n],vs[(j+1)*n+(i+1)%n],vs[(j+1)*n+i]],[(0,1,2,3)],white if i%4 in [0,1] else iron)
 for i in range(8):
  a=i*pi/4;c=(x+r*.84*cos(a),y+r*.84*sin(a),1.45);box(c,(r*.68,.11,.9),iron,a+pi/2)
 rod((x,y,5.65),(x,y,9.1),.045,white,8);ball((x,y,5.9),.15,bronze)
 # Canadian flag with modelled cloth ripples and maple leaf silhouette.
 red=flagred
 verts=[]
 for j in range(5):
  for i in range(17):
   u=i/16;v=j/4;verts.append((x+u*2.3,y+.12*sin(u*9+v*2)*u,8.8-v*1.15-.13*u))
 for j in range(4):
  for i in range(16):B.add([verts[j*17+i],verts[j*17+i+1],verts[(j+1)*17+i+1],verts[(j+1)*17+i]],[(0,1,2,3)],red if i<4 or i>=12 else white)
 # Stylized maple leaf on central white panel.
 leaf=[(0,-.33),(.05,-.12),(.25,-.17),(.18,-.03),(.33,.07),(.19,.12),(.23,.28),(.08,.20),(0,.39),(-.08,.20),(-.23,.28),(-.19,.12),(-.33,.07),(-.18,-.03),(-.25,-.17),(-.05,-.12)]
 B.add([(x+1.15+u,y-.04,8.12+v) for u,v in leaf],[tuple(range(len(leaf)))],red)
flagred=material('Canadian flag red',(.54,.016,.027),.8)
for x,y,r in [(-143,76,4.6),(-85,76,4.8),(-24,76,4.8),(44,76,4.5),(99,6,4.8)]:gazebo(x,y,r)
def bench(x,y,a=0):
 for dy in [-.24,-.08,.08,.24]:box((x-dy*sin(a),y+dy*cos(a),.54),(2.0,.13,.075),wood,a)
 for z in [.72,.88,1.04]:box((x-.32*sin(a),y+.32*cos(a),z),(2,.07,.12),wood,a)
 for dx in [-.75,.75]:
  xx=x+dx*cos(a);yy=y+dx*sin(a);rod((xx,yy,.05),(xx,yy,.55),.04,iron)
  rod((xx-.3*sin(a),yy+.3*cos(a),.1),(xx-.3*sin(a),yy+.3*cos(a),1.13),.03,iron)
for x in range(-178,110,9):bench(x,81)
for y in range(-19,62,9):bench(107,y,-pi/2)
lampglass=material('Warm lantern glass',(.79,.61,.32),.25)
p=lampglass.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.58,.21,1);p.inputs['Emission Strength'].default_value=.7
def lamp(x,y):
 cyl(x,y,0,.22,.17,iron,12);cyl(x,y,.17,.105,3.6,iron,12)
 for dx in [-.43,.43]:
  rod((x,y,3.1),(x+dx,y,3.55),.045,iron)
  box((x+dx,y,3.78),(.34,.34,.56),lampglass);cyl(x+dx,y,4.07,.28,.22,iron,4,B,.015)
  for sx in [-.18,.18]:
   for sy in [-.18,.18]:rod((x+dx+sx,y+sy,3.47),(x+dx+sx,y+sy,4.08),.017,iron,5)
for x in range(-180,112,14):lamp(x,83.5)
for y in range(-21,69,14):lamp(109,y)
# Green lawn between hotel and promenade, path and stone retaining edge.
box((-86,44.8,.3),(110,12,.5),grass)
box((-87,51,.15),(111,.45,.6),stone)
# Cannons on wheeled carriages overlooking the river.
for x in [-126,-61,10,75]:
 box((x,69,.4),(1.15,1.8,.36),iron)
 rod((x,68.6,.85),(x,70.4,1.15),.18,bronze,16)
 for sx in [-.65,.65]:rod((x+sx-.09,69,.5),(x+sx+.09,69,.5),.43,iron,16)
# Champlain monument, limestone plinth and bronze silhouette.
for z,w,d,h in [(0,6.5,6.5,.4),(.4,5.2,5.2,.6),(1,3.8,3.8,.7),(1.7,2.8,2.8,4.9),(6.6,3.3,3.3,.5)]:box((92,-12,z+h/2),(w,d,h),stone)
cyl(92,-12,7.1,.32,1.6,bronze,12);ball((92,-12,9.1),.3,bronze);rod((92,-12,8.0),(92.8,-12,8.6),.13,bronze);rod((92,-12,7.6),(91.6,-12,7.0),.17,bronze)
terrace=B.finish('02 Dufferin Terrace')
print('TERRACE',len(B.v),flush=True)
# Terrain based on a continuous cap and lower riverside shelf.
B=Batch('Cap Diamant terrain')
def height(x,y):
 # eastern escarpment transitions from the terrace to the narrow lower town.
 edge=88 if x<100 else 62-(x-100)*1.0
 d=max(y-edge,x-115)
 if d<0:return -0.8
 if d<42:return -.8-45*(d/42)**.72
 return -45.8
vs=[];N=90
for j in range(N+1):
 y=-450+j*10
 for i in range(N+1):
  x=-500+i*10;z=height(x,y)
  if z<-2:z+=1.0*sin(x*.21)*sin(y*.16)
  vs.append((x,y,z))
B.add(vs,[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(N) for i in range(N)],earth)
terrain=B.finish('03 Terrain and river')
B=Batch('River and far bank');box((-1150,-950,-3),(2300,1900,3),earth);box((450,700,-48),(2300,2400,1),water)
# Far Lévis shoreline: long, irregular tree-covered ridge.
vs=[]
for i in range(101):
 x=-1600+i*42;y=1700+sin(i*.21)*65;z=-25+sin(i*.17)*9+sin(i*.57)*4;vs.extend([(x,y,-49),(x,y+120,z),(x,y+650,z-3)])
B.add(vs,[(i*3+j,(i+1)*3+j,(i+1)*3+j+1,i*3+j+1) for i in range(100) for j in range(2)],grass)
B.finish('03 Terrain and river')
# Exact OSM surrounding footprints. Heights and roof forms estimated from context.
B=Batch('Old Quebec buildings and street pattern')
bgmat=[material('Neighborhood plaster %d'%i,c) for i,c in enumerate([(.36,.32,.25),(.29,.28,.24),(.28,.19,.13),(.49,.43,.32),(.34,.25,.19),(.48,.46,.39)])]
bgroof=[slate,copper,material('Burgundy sheet metal',(.21,.045,.04),.65,.1),material('Weathered zinc',(.34,.36,.35),.55,.25)]
def geo(v):
 e=(v['lon']+71.205283)*76130;n=(v['lat']-46.811891)*111195;return(e*.88+n*.475,e*.475-n*.88)
OSM=json.load(open(os.path.join(WORK,'references/osm.json')))
build_polys=[]
for e in OSM['elements']:
 t=e.get('tags',{});g=e.get('geometry',[])
 if not g:continue
 pts=[geo(v) for v in g];cx=sum(v[0] for v in pts)/len(pts);cy=sum(v[1] for v in pts)/len(pts)
 if t.get('building') and len(pts)>3:
  if -99<cx<76 and -50<cy<45:continue
  if -187<cx<115 and 40<cy<87:continue
  if cx>110 and cy>210:continue
  pts=pts[:-1] if pts[0]==pts[-1] else pts
  area=abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))/2)
  if area<22:continue
  z=height(cx,cy)+.3;h=min(23,max(6,float(t.get('building:levels','3').split(';')[0]) *3 if t.get('building:levels','3').split(';')[0].isdigit() else 10));h+=random.uniform(-1,1);n=len(pts)
  verts=[(x,y,z) for x,y in pts]+[(x,y,z+h) for x,y in pts];B.add(verts,[tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],random.choice(bgmat));build_polys.append((pts,z,h))
  # Roof with elevated inner polygon prevents generic flat city blocks.
  roofmat=random.choice(bgroof);roofh=random.uniform(2.5,5.0)
  rv=[(x,y,z+h+.12) for x,y in pts]+[(cx+(x-cx)*.32,cy+(y-cy)*.32,z+h+roofh) for x,y in pts]
  B.add(rv,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]+[tuple(range(n,2*n))],roofmat)
  if abs(cx)<300 and abs(cy)<300:
   # Determine outward normal, and lay out windows in metres along each wall.
   area_signed=sum(pts[i][0]*pts[(i+1)%n][1]-pts[(i+1)%n][0]*pts[i][1] for i in range(n))
   for j in range(n):
    p0=Vector(pts[j]);p1=Vector(pts[(j+1)%n]);v=p1-p0;length=v.length
    if length<3:continue
    a=math.atan2(v.y,v.x)+(pi if area_signed>0 else 0);mid=(p0+p1)/2;cols=int(length/3.1)
    for f in range(int(h/3)):
     for k in range(cols):
      p0a=p0.lerp(p1,(k+.5)/cols);win(p0a.x-.055*sin(a),p0a.y+.055*cos(a),z+1.65+f*3,1.1,1.65,a,b=B,trim=False)
    if length>6:box((mid.x,mid.y,z+h), (length,.28,.25),stone,math.atan2(v.y,v.x),B)
 elif t.get('highway') in ['residential','pedestrian','service','tertiary','unclassified']:
  if -95<cx<74 and -47<cy<45:continue
  width=4 if t['highway']=='pedestrian' else 6
  for u,v in zip(pts[:-1],pts[1:]):
   mid=((u[0]+v[0])/2,(u[1]+v[1])/2);z=height(*mid)+.12
   if -180<mid[0]<112 and 42<mid[1]<86:continue
   length=math.dist(u,v);a=math.atan2(v[1]-u[1],v[0]-u[0]);box((*mid,z),(length+.2,width,.08),asphalt,a,B)
B.finish('04 Old Quebec | mapped context')
print('CITY',len(B.v),flush=True)
# Five shared broadleaf tree meshes, fine leaf cards and branching rather than spheres.
for typ in range(5):
 random.seed(88+typ);B=Batch('Broadleaf prototype %d'%typ)
 rod((0,0,0),(.18,.13,6),.28,trunk,9,B,.09)
 for k in range(20):
  a=random.uniform(0,2*pi);zz=random.uniform(2.5,6.0);rr=random.uniform(1.3,3.2);c=Vector((rr*cos(a),rr*sin(a),zz+random.uniform(1,2.5)))
  rod((.12,.08,zz),c,.075,trunk,6,B,.015)
  # airy crown clusters carrying bent diamond leaves at natural angles.
  for j in range(150):
   while True:
    v=Vector((random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)))
    if v.length<1:break
   pos=c+Vector((v.x*1.5,v.y*1.5,v.z*1.25));a2=random.uniform(0,2*pi);u=Vector((cos(a2),sin(a2),random.uniform(-.5,.5)))*random.uniform(.08,.17);v2=Vector((-sin(a2),cos(a2),random.uniform(-.8,.8)))*random.uniform(.05,.1)
   B.add([tuple(pos-u),tuple(pos+v2),tuple(pos+u),tuple(pos-v2),tuple(pos+Vector((0,0,.04)))],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],random.choice(foliage[:5]))
 ob=B.finish('05 Trees and planting');ob.hide_render=True;ob.hide_viewport=True
random.seed(315)
protos=[bpy.data.objects['Broadleaf prototype %d'%i] for i in range(5)]
def tree(x,y,z,s=1):
 base=random.choice(protos);ob=bpy.data.objects.new('Maple • escarpment',base.data);collection('05 Trees and planting').objects.link(ob);ob.location=(x,y,z);ob.scale=(s,s,s*random.uniform(.9,1.1));ob.rotation_euler[2]=random.random()*2*pi
for i in range(370):
 x=random.uniform(-310,172);y=random.uniform(88,128)
 if x>109:y=random.uniform(-65,123)
 z=height(x,y)
 if z< -42:continue
 tree(x,y,z,random.uniform(.72,1.28))
for i in range(90):
 x=random.uniform(-340,-112);y=random.uniform(-150,34);tree(x,y,height(x,y),random.uniform(.8,1.35))
# Small garden trees south of the château.
for x,y in [(-124,39),(-143,34),(-163,28),(-190,25),(-110,-40),(-98,-72)]:tree(x,y,-.3,1.1)
# Funicular rails descend beside the east terrace.
B=Batch('Funicular and distant ferry')
p0=Vector((112,13,-1));p1=Vector((150,63,-45))
for dd in [-1.6,-.8,.8,1.6]:rod(p0+Vector((dd,0,0)),p1+Vector((dd,0,0)),.085,slate,8)
for i in range(45):
 c=p0.lerp(p1,i/44);rod(c+Vector((-2,0,0)),c+Vector((2,0,0)),.10,trunk,6)
for t in [.25,.70]:
 c=p0.lerp(p1,t);box(c+Vector((0,0,1.5)),(3.9,3.6,2.6),white);box(c+Vector((0,1.82,1.6)),(3.5,.1,1.6),glass[1]);box(c+Vector((0,0,2.95)),(4.1,3.8,.15),iron)
# Ferry in the mid-distance: restrained scale reference on the river.
box((390,520,-45),(40,12,4),white);box((389,520,-41.6),(29,10,3),white);box((390,520,-43),(37,12.1,.6),slate)
for x in range(377,402,2):box((x,526.1,-41.3),(1.3,.06,1.3),glass[2])
B.finish('06 Site details')
# A sparse handful of human figures provides scale at a distance.
B=Batch('Visitors on the promenade')
clothes=[material('Visitor clothing '+str(i),c) for i,c in enumerate([(.04,.065,.12),(.22,.06,.04),(.42,.39,.30),(.19,.21,.20),(.58,.51,.37)])]
skin=material('Skin',(.43,.27,.17),.8)
for i in range(26):
 x=random.uniform(-170,100);y=random.uniform(57,74);h=random.uniform(1.52,1.84);m=random.choice(clothes)
 rod((x-.12,y,.08),(x-.11,y,h*.47),.075,m);rod((x+.13,y,.08),(x+.1,y,h*.47),.075,m);ball((x,y,h*.66),.28,m,scale=(.70,.43,1.25));ball((x,y,h*.91),h*.075,skin,n=10,rings=6)
 rod((x-.17,y,h*.76),(x-.24,y+.1,h*.45),.06,m);rod((x+.17,y,h*.76),(x+.25,y-.1,h*.47),.06,m)
B.finish('06 Site details')
# Lighting, atmosphere, cinematic camera.
world=bpy.data.worlds.new('Photographic dawn sky');scene.world=world;world.use_nodes=True;nodes=world.node_tree.nodes;links=world.node_tree.links;nodes.clear();out=nodes.new('ShaderNodeOutputWorld');bg=nodes.new('ShaderNodeBackground');env=nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(os.path.join(WORK,'references/dawn.hdr'));env.image.pack();bg.inputs['Strength'].default_value=.65;links.new(env.outputs[0],bg.inputs[0]);links.new(bg.outputs[0],out.inputs[0])
ld=bpy.data.lights.new('Low morning sun','SUN');ld.energy=3.2;ld.angle=math.radians(1.5);ld.color=(1,.77,.51);lo=bpy.data.objects.new('Low morning sun',ld);collection('07 Light and camera').objects.link(lo);lo.rotation_euler=(Vector((0,0,0))-Vector((-90,180,115))).to_track_quat('-Z','Y').to_euler()
# Subtle blue fill preserves architectural detail in shadow.
ld=bpy.data.lights.new('Sky fill','AREA');ld.energy=12000;ld.shape='DISK';ld.size=180;ld.color=(.61,.76,1);lo=bpy.data.objects.new('Sky fill',ld);collection('07 Light and camera').objects.link(lo);lo.location=(80,130,150);lo.rotation_euler=(Vector((0,0,25))-lo.location).to_track_quat('-Z','Y').to_euler()
# Distant haze volume only: density fades the shoreline without veiling the hero.
fog=bpy.data.materials.new('River aerial perspective');fog.use_nodes=True;nn=fog.node_tree.nodes;nn.clear();oo=nn.new('ShaderNodeOutputMaterial');vv=nn.new('ShaderNodeVolumePrincipled');vv.inputs['Density'].default_value=.00065;vv.inputs['Color'].default_value=(.64,.73,.82,1);vv.inputs['Anisotropy'].default_value=.25;fog.node_tree.links.new(vv.outputs['Volume'],oo.inputs['Volume'])
B=Batch('Distant river haze');box((100,1100,70),(3600,1400,240),fog,b=B);B.finish('07 Light and camera')
camd=bpy.data.cameras.new('Cinema camera');cam=bpy.data.objects.new('Cinema camera',camd);collection('07 Light and camera').objects.link(cam);scene.camera=cam;camd.lens=36;camd.clip_end=6000
scene.render.fps=24;scene.frame_start=1;scene.frame_end=720
# Catmull-Rom path: deliberate approach, then gradual rising reveal.
keys=[(1,(-165,225,65),(-7,8,34),40),(180,(-116,174,42),(-7,16,35),35),(360,(-56,145,25),(0,18,37),29),(540,(64,174,66),(0,6,35),38),(720,(146,235,109),(-3,1,27),42)]
# Bake smooth path and look-at to every frame for portable interpolation.
def cat(p0,p1,p2,p3,t):return .5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)
for frame in range(1,721):
 idx=next((i for i in range(len(keys)-1) if keys[i][0]<=frame<=keys[i+1][0]),len(keys)-2);t=(frame-keys[idx][0])/(keys[idx+1][0]-keys[idx][0]);inds=[max(0,idx-1),idx,idx+1,min(len(keys)-1,idx+2)]
 loc=cat(*[Vector(keys[i][1]) for i in inds],t);target=cat(*[Vector(keys[i][2]) for i in inds],t);cam.location=loc;cam.rotation_euler=(target-loc).to_track_quat('-Z','Y').to_euler();camd.lens=keys[idx][3]*(1-t)+keys[idx+1][3]*t;cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_euler',frame=frame);camd.keyframe_insert('lens',frame=frame)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.04
try:
 pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='METAL';pref.get_devices()
 for d in pref.devices:d.use=d.type=='METAL'
 scene.cycles.device='GPU'
except Exception as e:print(e)
scene.cycles.max_bounces=5;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=3;scene.cycles.transparent_max_bounces=4
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.1
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False
scene.render.use_file_extension=True
scene.frame_set(100)
# Good opening view for the editable file.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
scene['Location']='Fairmont Le Château Frontenac / Terrasse Dufferin, Québec';scene['Reference origin']='46.811891, -71.205283';scene['Accuracy']='Reference-guided reconstruction using OpenStreetMap footprints and photographic details; heights and small sculptural elements are estimates.'
scene['Source URL']='https://www.chateau-frontenac.com/en/gallery/'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Chateau_Frontenac.blend'))
print('SAVED',flush=True)
scene.render.resolution_percentage=50;scene.cycles.samples=16;scene.render.filepath=os.path.join(WORK,'preview_100.png');bpy.ops.render.render(write_still=True)
print('PREVIEW DONE',flush=True)
