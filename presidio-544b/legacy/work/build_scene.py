import bpy,math,random,json,os,time
from pathlib import Path
from mathutils import Vector,Matrix
from math import sin,cos,pi
ROOT=Path('/Users/lucaschu/Documents/ChatGPT/Renders');AS=ROOT/'work/assets';OUT=ROOT/'outputs'
random.seed(544)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
COL={}
for name in ['01 | Ground and surveyed streets','02 | 544 — architectural fabric','03 | Neighbors and garages','04 | Mature woodland','05 | Garden and understory','06 | Street furniture','07 | Cinematography','08 | Asset prototypes']:
 c=bpy.data.collections.new(name);sc.collection.children.link(c);COL[name[:2]]=c
M=[]
def mat(name,color,rough=.7,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;M.append(m);return len(M)-1

def textured(name,base,col,scale,normal=.4,diff=True):
 idx=mat(name,col);m=M[idx];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 tc=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='SCALE';v.inputs[3].default_value=scale;l.new(tc.outputs['Object'],v.inputs[0])
 for typ in ['diff','rough','nor_gl']:
  files=list((AS/'textures').glob(base+'_'+typ+'.*'))
  if not files or (typ=='diff' and not diff):continue
  im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(files[0]),check_existing=True);im.projection='BOX';im.projection_blend=.2;l.new(v.outputs[0],im.inputs['Vector'])
  if typ=='diff':l.new(im.outputs['Color'],p.inputs['Base Color'])
  else:
   im.image.colorspace_settings.name='Non-Color'
   if typ=='rough':l.new(im.outputs['Color'],p.inputs['Roughness'])
   else:
    nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=normal;l.new(im.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal'])
 return idx
stucco=textured('Warm ivory | fine historic stucco','white_plaster_rough_01',(.72,.69,.59),1.8,.22,False)
trim=mat('Painted warm white joinery',(.78,.77,.70),.55)
concrete=mat('Aged concrete | steps and sills',(.38,.39,.36),.86)
wood=mat('Dark umber painted sash',(.055,.037,.023),.44)
black=mat('Recess shadow',(.008,.011,.01),.82)
glass=mat('Old glass | cool reflected sky',(.018,.032,.033),.065,.72)
p=M[glass].node_tree.nodes.get('Principled BSDF');p.inputs['Coat Weight'].default_value=.65
asphalt=textured('Weathered asphalt','clean_asphalt',(.08,.09,.1),.28,.55)
grass=textured('Coastal lawn | living ground','leafy_grass',(.11,.18,.05),.28,.45)
gm=M[grass];gn=gm.node_tree.nodes;gl=gm.node_tree.links;gp=gn.get('Principled BSDF');source=gp.inputs['Base Color'].links[0].from_socket
gray=gn.new('ShaderNodeRGBToBW');gl.new(source,gray.inputs[0]);ramp=gn.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.08;ramp.color_ramp.elements[0].color=(.024,.047,.009,1);ramp.color_ramp.elements[1].position=.65;ramp.color_ramp.elements[1].color=(.16,.245,.046,1);gl.new(gray.outputs[0],ramp.inputs[0]);gl.new(ramp.outputs['Color'],gp.inputs['Base Color'])
mulch=textured('Eucalyptus leaf litter','brown_mud_leaves_01',(.14,.11,.055),.45,.8)
bark=textured('Blue gum | peeling bark','bark_bluegum',(.36,.31,.23),.6,.7)
red=mat('Faded red curb paint',(.29,.045,.03),.9)
yellow=mat('Worn road yellow',(.69,.46,.045),.8)
white=mat('Road marking white',(.76,.75,.64),.9)
metal=mat('Galvanized steel',(.24,.26,.25),.42,.65)
bronze=mat('Blackened bronze',(.048,.06,.044),.38,.68)
door=mat('Painted mahogany entrance',(.095,.049,.029),.5)
brass=mat('Aged brass',(.32,.22,.075),.28,.76)
terra=[]
for i in range(12):
 v=random.uniform(.73,1.12);terra.append(mat('Clay roof tile %02d'%i,(.255*v,.078*v,.031*v),random.uniform(.67,.86)))
foliage=[]
for i in range(6):
 q=mat('Evergreen leaf %02d'%i,(.027+i*.009,.067+i*.014,.014+i*.004),.63)
 p=M[q].node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.045;foliage.append(q)
dry=mat('Sun-bleached grass',(.26,.26,.095),.9)
# Subtle mineral roughness on surfaces that should catch natural grazing light.
for idx in [concrete,stucco,trim]+terra:
 m=M[idx];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 if p.inputs['Normal'].is_linked:continue
 tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=65;tex.inputs['Detail'].default_value=3
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.18;b.inputs['Distance'].default_value=.025;l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])

class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def poly(self,pts,ma):
  off=len(self.v);self.v.extend([tuple(p) for p in pts]);self.f.append(tuple(range(off,off+len(pts))));self.mi.append(ma)
 def box(self,c,s,ma,rot=0):
  x,y,z=c;a,b,h=[q*.5 for q in s];cs=cos(rot);sn=sin(rot);off=len(self.v)
  for dx,dy,dz in [(-a,-b,-h),(a,-b,-h),(a,b,-h),(-a,b,-h),(-a,-b,h),(a,-b,h),(a,b,h),(-a,b,h)]:self.v.append((x+dx*cs-dy*sn,y+dx*sn+dy*cs,z+dz))
  for f in [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]:self.f.append(tuple(off+i for i in f));self.mi.append(ma)
 def tube(self,a,b,r,ma,r2=None,n=8):
  a=Vector(a);b=Vector(b);d=(b-a).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.01:u=Vector((1,0,0))
  u.normalize();v=d.cross(u);o=len(self.v);r2=r if r2 is None else r2
  for p,rr in [(a,r),(b,r2)]:
   for k in range(n):self.v.append(tuple(p+rr*(cos(k*2*pi/n)*u+sin(k*2*pi/n)*v)))
  for k in range(n):self.f.append((o+k,o+(k+1)%n,o+(k+1)%n+n,o+k+n));self.mi.append(ma)
  self.f.extend([tuple(o+i for i in range(n-1,-1,-1)),tuple(o+n+i for i in range(n))]);self.mi.extend([ma,ma])
 def emit(self,name,col,loc=(0,0,0),rot=0,bevel=0):
  me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update();o=bpy.data.objects.new(name,me);COL[col].objects.link(o)
  for ma in M:me.materials.append(ma)
  for p,idx in zip(me.polygons,self.mi):p.material_index=idx
  o.location=loc;o.rotation_euler[2]=rot
  if bevel:
   mod=o.modifiers.new('Light-catching edges','BEVEL');mod.width=bevel;mod.segments=2
  return o

def terrain(x,y):
 return -.037*y-.054*x+4.0/(1+math.exp(max(-50,min(50,(x+42)/13))))+.16*sin(x*.09)*sin(y*.045)

features=json.load(open(ROOT/'work/site.json'))
BUILD=[]
for f in features:
 t=f['tags'];num=t.get('addr:housenumber','')
 if num.isdigit() and 540<=int(num)<=558:
  pts=[Vector(p) for p in f['xy'][:-1]];edges=[(pts[(i+1)%len(pts)]-p) for i,p in enumerate(pts)]
  # Main wall axes follow longest footprint edges; use facade axis nearest N/S for east-facing row.
  e=max(edges,key=lambda v:v.length).normalized();ang=math.atan2(e.y,e.x)
  if cos(ang)<0:ang+=pi
  # The facade is the long axis on duplexes; derive bounds in both principal directions.
  ca,sa=cos(ang),sin(ang);local=[(p.x*ca+p.y*sa,-p.x*sa+p.y*ca) for p in pts]
  mn=[min(p[i] for p in local) for i in (0,1)];mx=[max(p[i] for p in local) for i in (0,1)]
  cen=[(mn[i]+mx[i])/2 for i in (0,1)];cx=cen[0]*ca-cen[1]*sa;cy=cen[0]*sa+cen[1]*ca
  # Choose orientation so facade's outward normal points toward nearest boulevard segment.
  if sin(ang)<0:ang+=pi
  if num=='544':ang=math.radians(98.2);cx=.0;cy=.5
  BUILD.append(dict(num=int(num),cx=cx,cy=cy,a=ang,w=mx[0]-mn[0],d=mx[1]-mn[1]))

def coord(x,y,b):return (b['cx']+x*cos(b['a'])-y*sin(b['a']),b['cy']+x*sin(b['a'])+y*cos(b['a']))

def window(m,x,y,z,w=1.03,h=1.75,side=0):
 # Window centered on z; facade normal local -Y. Actual wall is recessed behind this opening assembly.
 tmp=Mesh();tmp.box((x,y+.045,z),(w+.18,.13,h+.18),black)
 tmp.box((x,y-.025,z),(w,.09,h),glass)
 for dx in [-w/2,w/2]:tmp.box((x+dx,y-.105,z),(.073,.10,h+.12),wood)
 for dz in [-h/2,0,h/2]:tmp.box((x,y-.112,z+dz),(w+.07,.11,.07),wood)
 for dx in [-w/6,w/6]:tmp.box((x+dx,y-.13,z),(.024,.06,h-.05),wood)
 for dz in [-h/3,-h/6,h/6,h/3]:tmp.box((x,y-.13,z+dz),(w,.055,.022),wood)
 tmp.box((x,y-.11,z-h/2-.10),(w+.26,.32,.12),trim)
 # Thin partially lowered linen blinds vary gently across rooms.
 if random.random()<.5:
  tmp.box((x,y+.004,z+h*.30),(w-.13,.015,h*.31),trim)
 if side:
  for i,(xx,yy,zz) in enumerate(tmp.v):tmp.v[i]=(xx*cos(side)-yy*sin(side),xx*sin(side)+yy*cos(side),zz)
 off=len(m.v);m.v+=tmp.v;m.f += [tuple(i+off for i in f) for f in tmp.f];m.mi+=tmp.mi

def hiproof(m,w,d,z,rise,ma,detailed=True,center=(0,0)):
 cx,cy=center;w2=w/2;d2=d/2;ridge=max(.1,w2-d2)
 pts=[(-w2,-d2,z),(w2,-d2,z),(w2,d2,z),(-w2,d2,z),(-ridge,0,z+rise),(ridge,0,z+rise)]
 for f in [(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]:m.poly([(pts[i][0]+cx,pts[i][1]+cy,pts[i][2]) for i in f],ma)
 if not detailed:return
 # Curved overlapping mission tiles follow each of the four slopes, assembled into one editable mesh.
 pitch=rise/d2;step=.34;tilew=.23
 for side in [-1,1]:
  for j in range(int(d2/step)+1):
   t=j*step;yy=side*(d2-t);half=w2-t
   for i in range(int(2*half/tilew)):
    xx=-half+(i+.5)*tilew;length=min(.41,d2-t+.04)
    if length<.07:continue
    col=random.choice(terra);seg=5
    for k in range(seg):
     a0=k*pi/seg;a1=(k+1)*pi/seg
     # Tile crest rises 7 cm off its pan; lower lip gives each course a crisp shadow.
     v=[]
     for tt,aa in [(0,a0),(0,a1),(length,a1),(length,a0)]:
      v.append((cx+xx+cos(aa)*tilew*.48,cy+yy-side*tt,z+(t+tt)*pitch+.025+sin(aa)*.072))
     m.poly(v,col)
 for side in [-1,1]:
  for j in range(int(d2/step)+1):
   t=j*step;xx=side*(w2-t);half=d2-t
   for i in range(int(2*half/tilew)):
    yy=-half+(i+.5)*tilew;length=min(.41,d2-t+.03)
    if length<.07:continue
    col=random.choice(terra)
    for k in range(5):
     a0=k*pi/5;a1=(k+1)*pi/5
     m.poly([(cx+xx-side*tt,cy+yy+cos(aa)*tilew*.48,z+(t+tt)*pitch+.025+sin(aa)*.072) for tt,aa in [(0,a0),(0,a1),(length,a1),(length,a0)]],col)
 for k in range(int(2*ridge/.32)+1):
  x=-ridge+k*.32;m.tube((cx+x,cy,z+rise+.07),(cx+min(ridge,x+.36),cy,z+rise+.07),.13,random.choice(terra),n=8)
 for end in [-1,1]:
  for sy in [-1,1]:
   for j in range(int(d2/.3)):
    t=j*.3;m.tube((cx+end*(w2-t),cy+sy*(d2-t),z+t*pitch+.065),(cx+end*(w2-t-.31),cy+sy*(d2-t-.31),z+(t+.31)*pitch+.065),.115,random.choice(terra),n=6)

def house(b):
 num=b['num'];duplex=num in [540,541,542,544,546,548,550,551];hero=num==544
 w=19.4 if duplex else 12.3;d=11.6 if duplex else 11.5
 b['w']=w;b['d']=d;base=terrain(b['cx'],b['cy']);col='02' if hero else '03'
 struct=Mesh();join=Mesh();roof=Mesh();porch=Mesh();ground=Mesh();h=7.0;foundation=1.0
 # Solid shell ends just behind window faces; relief and recess depth remain visible at oblique angles.
 struct.box((0,0,3.0),(w,d,8.0),stucco)
 struct.box((0,0,.34),(w+.06,d+.06,.95),stucco)
 struct.box((0,0,7.02),(w+.55,d+.5,.2),trim)
 struct.box((0,0,7.17),(w+.92,d+.84,.14),trim)
 for xx in [(-w/2+i*.48) for i in range(int(w/.48)+1)]:
  for yy in [-d/2-.28,d/2+.28]:join.box((xx,yy,6.91),(.105,.75,.17),trim)
 # eight distinct upper sash on duplexes; tripled lower windows at single houses.
 xs=[-8,-5.95,-3.8,-1.65,1.65,3.8,5.95,8] if duplex else [-4,0,4]
 for x in xs:window(join,x,-d/2-.03,5.65,1.0,1.65)
 lower=[-8,-5.95,-1.1,1.1,5.95,8] if duplex else [-4.9,-3.85,-2.8,2.8,3.85,4.9]
 for x in lower:window(join,x,-d/2-.03,2.55,1.0,1.95)
 for sy in [-1,1]:
  for zz in [2.55,5.65]:
   for xx in [-3.4,0,3.4]:window(join,xx,-w/2-.03,zz,1.03,1.8,side=sy*pi/2)
 for x in xs[::2]:window(join,x,d/2+.03,5.65,1.0,1.6,side=pi) if False else None
 for x in [-7.8,-5.95,5.95,7.8] if duplex else [-4.5,-3.2,3.2,4.5]:
  join.box((x,-d/2-.06,.26),(1.03,.07,.46),black)
  for dx in [-.37,-.18,0,.18,.37]:join.box((x+dx,-d/2-.13,.26),(.025,.04,.46),metal)
 # Mirrored portico, white solid parapets, two separate approach stairs.
 pw=10.0 if duplex else 2.8;pd=2.3 if duplex else 1.4;py=-d/2-pd/2
 porch.box((0,py,-.04),(pw,pd,2.05),stucco)
 porch.box((0,py,.97),(pw,pd,.28),concrete)
 if duplex:
  for x in [-pw/2+.18,0,pw/2-.18]:
   porch.box((x,py-pd/2+.17,2.55),(.26,.29,2.9),trim)
   porch.box((x,py-pd/2+.17,1.19),(.43,.45,.27),trim)
   porch.box((x,py-pd/2+.17,3.96),(.5,.48,.19),trim)
   for dx in [-.34,.34]:porch.box((x+dx,py-pd/2+.17,4.035),(.55,.26,.13),trim)
  for x in [-pw/2+.12,pw/2-.12]:porch.box((x,py,1.57),(.22,pd,.9),stucco);porch.box((x,py,2.07),(.33,pd+.1,.12),trim)
  porch.box((0,py-pd/2,1.52),(3.2,.22,.92),stucco);porch.box((0,py-pd/2,2.02),(3.4,.36,.13),trim)
 porch.box((0,py,4.15 if duplex else 3.75),(pw+.5,pd+.28,.18),trim)
 hiproof(roof,pw+.6,pd+.65,4.26 if duplex else 3.86,.65,terra[3],True,center=(0,py))
 doors=[-3.1,3.1] if duplex else [0]
 for x in doors:
  yy=-d/2-.10;join.box((x,yy,2.17),(1.21,.12,2.3),wood);join.box((x,yy-.06,2.18),(1.07,.08,2.13),door)
  join.box((x,yy-.115,2.65),(.79,.02,.97),glass)
  for dx in [-.38,.38]:join.box((x+dx,yy-.15,2.65),(.045,.05,1.03),wood)
  for dz in [2.12,3.17]:join.box((x,yy-.15,dz),(.8,.05,.05),wood)
  for zz in [1.4,1.73]:
   join.box((x,yy-.13,zz),(.8,.02,.24),black);join.box((x,yy-.15,zz),(.73,.035,.18),door)
  join.tube((x+.39,yy-.22,1.91),(x+.39,yy-.22,2.09),.025,brass,n=8)
  # Concrete stairs resolve from actual local terrain to porch level.
  stairEnd=py-pd/2;stepCount=7;run=.29
  for i in range(stepCount):
   top=1.10-i*.235;porch.box((x,stairEnd-(i+.5)*run,top-1.4),(2.37,run+.025,2.8),concrete)
  for side in [-1,1]:
   xx=x+side*1.30;yb=stairEnd;ya=stairEnd-stepCount*run
   for dx in [-.13,.13]:porch.poly([(xx+dx,ya,-1.7),(xx+dx,yb,-1.7),(xx+dx,yb,1.88),(xx+dx,ya,.39)],stucco)
   porch.poly([(xx-.13,ya,.39),(xx+.13,ya,.39),(xx+.13,yb,1.88),(xx-.13,yb,1.88)],trim)
   porch.box((xx,ya,-.25),(.30,.30,1.3),stucco);porch.box((xx,ya,.43),(.39,.42,.12),trim)
  # Route each front walk out to the public sidewalk (the slope is shared with the landscape).
  for i in range(18):
   y0=stairEnd-2.1-i*.45;y1=y0-.45;gx0,gy0=coord(x,y0,b);gx1,gy1=coord(x,y1,b)
   z0=terrain(gx0,gy0)-base+.045;z1=terrain(gx1,gy1)-base+.045
   ground.poly([(x-1.05,y0,z0),(x+1.05,y0,z0),(x+1.05,y1,z1),(x-1.05,y1,z1)],concrete)
   if i%3==0:ground.poly([(x-1.04,y0,z0+.002),(x+1.04,y0,z0+.002),(x+1.04,y0-.014,z0+.002),(x-1.04,y0-.014,z0+.002)],black)
 # Roof and chimneys.
 hiproof(roof,w+1.05,d+1.1,7.29,2.48,terra[5],True)
 for x in [-w/2+.72,w/2-.72] if duplex else [2.8]:
  struct.box((x,.0,8.25),(.63,.78,3.45),stucco);struct.box((x,0,9.98),(.73,.88,.16),trim);join.box((x,0,10.08),(.4,.56,.07),black)
 struct.box((0,3.9,8.55),(.49,.6,1.8),stucco)
 # Rear service porch.
 struct.box((0,d/2+.7,2.08),(4.6,1.4,2.2),stucco);hiproof(roof,4.8,1.8,3.24,.32,terra[4],True,center=(0,d/2+.7))
 for x in [-w/2+.12,w/2-.12]:
  join.tube((x,-d/2-.14,.2),(x,-d/2-.14,7.1),.055,trim,n=10)
  for zz in [1,3.1,5.9]:join.box((x,-d/2-.14,zz),(.15,.14,.075),metal)
 struct.emit('%s | stucco shell and chimneys'%num,col,(b['cx'],b['cy'],base),b['a'],.025)
 join.emit('%s | sash glazing joinery and drainage'%num,col,(b['cx'],b['cy'],base),b['a'],.009 if hero else 0)
 porch.emit('%s | entry portico and steps'%num,col,(b['cx'],b['cy'],base),b['a'],.018)
 roof.emit('%s | individual overlapping mission tiles'%num,col,(b['cx'],b['cy'],base),b['a'])
 ground.emit('%s | garden approach walks'%num,'01',(b['cx'],b['cy'],base),b['a'])
 if hero:
  for x,label in [(-2.28,'544 A'),(2.23,'544 B')]:
   cv=bpy.data.curves.new('Cast address numerals','FONT');cv.body=label;cv.size=.11;cv.extrude=.002;cv.align_x='CENTER';o=bpy.data.objects.new(label,cv);COL['02'].objects.link(o);cv.materials.append(M[bronze]);gx,gy=coord(x,-d/2-.20,b);o.location=(gx,gy,base+2.52);o.rotation_euler=(pi/2,0,b['a'])
 return b

for b in BUILD:
 if b['num']<=551:house(b)
 else:
  base=terrain(b['cx'],b['cy']);m=Mesh();r=Mesh();w=max(b['w'],b['d']);d=min(b['w'],b['d']);m.box((0,0,1.55),(w,d,3.1),stucco);hiproof(r,w+.5,d+.5,3.12,.8,terra[2],True)
  for x in [-w/2+1.6+i*2.75 for i in range(max(1,int(w/2.75)))]:
   m.box((x,-d/2-.035,1.3),(2.4,.05,2.4),trim)
   for z in [.25,.65,1.05,1.45,1.85,2.25]:m.box((x,-d/2-.07,z),(2.35,.04,.025),concrete)
  m.emit('%s | historic garage'%b['num'],'03',(b['cx'],b['cy'],base),b['a'],.02);r.emit('%s | garage tile roof'%b['num'],'03',(b['cx'],b['cy'],base),b['a'])
print('ARCHITECTURE COMPLETE',len(bpy.data.objects),flush=True)
# Terrain spans the neighborhood, not a floating display base.
ground=Mesh();NX=150;NY=170
for j in range(NY):
 y=-330+j*5
 for i in range(NX):
  x=-340+i*5;ground.poly([(xx,yy,terrain(xx,yy)) for xx,yy in [(x,y),(x+5,y),(x+5,y+5),(x,y+5)]],grass)
ground.emit('Continuous rolling Presidio terrain','01')

def smoothpath(points,res=.9):
 ps=[Vector(p) for p in points];out=[]
 for i in range(len(ps)-1):
  a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(len(ps)-1,i+2)];count=max(2,int((c-b).length/res))
  for j in range(count):
   t=j/count;v=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t);out.append(v)
 out.append(ps[-1]);return out

def ribbon(m,ps,width,ma,offset=0,z=.025,dash=None):
 dist=0
 for i in range(len(ps)-1):
  a,b=ps[i],ps[i+1];dl=(b-a).length
  if dl<.001:continue
  if dash and int(dist/dash[0])%dash[1]:dist+=dl;continue
  na=Vector((-(b-a).y,(b-a).x)).normalized();pts=[]
  for p,s in [(a,-1),(b,-1),(b,1),(a,1)]:
   v=p+na*(offset+s*width/2);pts.append((v.x,v.y,terrain(v.x,v.y)+z))
  m.poly(pts,ma);dist+=dl
roads=[];road=Mesh();mark=Mesh();walks=Mesh()
for f in features:
 t=f['tags'];hw=t.get('highway')
 if not hw or len(f['xy'])<2:continue
 ps=smoothpath(f['xy']);name=t.get('name','')
 if hw in ['footway','path','steps','pedestrian','cycleway']:
  if t.get('footway')=='crossing':continue
  ribbon(walks,ps,1.65,concrete,z=.04);roads.append((ps,.9));continue
 wid=10.3 if name=='Presidio Boulevard' else (8.5 if name in ['Lombard Street','Simonds Loop'] else 4.4)
 if hw=='service':wid=4.4
 ribbon(road,ps,wid,asphalt,z=.026);roads.append((ps,wid/2))
 for side in [-1,1]:
  ribbon(walks,ps,.22,concrete,offset=side*(wid/2+.05),z=.13)
 if name=='Presidio Boulevard':
  for off in [-.11,.11]:ribbon(mark,ps,.10,yellow,offset=off,z=.04)
  ribbon(mark,ps,.115,white,offset=-wid/2+1.65,z=.045)
  ribbon(mark,ps,.115,white,offset=wid/2-1.65,z=.045,dash=(2.5,2))
  ribbon(mark,ps,.18,red,offset=wid/2+.04,z=.15)
road.emit('Boulevard, Sumner lane and connecting streets','01');walks.emit('Mapped public paths and raised curb lines','01');mark.emit('Double centerline, cycle lane and curb paint','06')
# Distant built context taken directly from map footprints.
distant=Mesh()
for f in features:
 t=f['tags'];num=t.get('addr:housenumber','')
 if 'building' not in t or (num.isdigit() and 540<=int(num)<=558):continue
 ps=f['xy'][:-1]
 if len(ps)<3:continue
 cx=sum(p[0] for p in ps)/len(ps);cy=sum(p[1] for p in ps)/len(ps)
 if max(abs(cx),abs(cy))>420:continue
 z=terrain(cx,cy);h=float(t.get('height','9').split(' ')[0]) if t.get('height','9').split(' ')[0].replace('.','').isdigit() else 9
 for i,a in enumerate(ps):
  b=ps[(i+1)%len(ps)];distant.poly([(a[0],a[1],z),(b[0],b[1],z),(b[0],b[1],z+h),(a[0],a[1],z+h)],stucco)
  v=Vector(b)-Vector(a);ln=v.length
  if ln>3:
   n=Vector((v.y,-v.x)).normalized();u=v.normalized()
   for k in range(1,int(ln/2.3)):
    p=Vector(a)+u*k*2.3+n*.02
    for zz in range(2,int(h),3):
     q=[p-u*.46,p+u*.46];distant.poly([(q[0].x,q[0].y,z+zz-.65),(q[1].x,q[1].y,z+zz-.65),(q[1].x,q[1].y,z+zz+.65),(q[0].x,q[0].y,z+zz+.65)],wood)
 distant.poly([(p[0],p[1],z+h+.02) for p in ps],terra[5])
distant.emit('Map-based distant neighborhood silhouettes','03')

# Asset loading picks baked LOD meshes; it never evaluates an unbounded procedural forest.
def load_asset(asset,selector):
 p=AS/asset/(asset+'.blend')
 with bpy.data.libraries.load(str(p),link=False) as (src,dst):dst.objects=[n for n in src.objects if selector(n)]
 out=[]
 for o in dst.objects:
  if o and o.type=='MESH':
   for img in bpy.data.images:
    if img.source=='FILE' and not img.packed_file:
     pp=Path(bpy.path.abspath(img.filepath));cand=AS/asset/'textures'/pp.name
     if cand.exists():img.filepath=str(cand)
   # Remove any saved asset-space placement while preserving authored geometry scales.
   o.location=(0,0,0);o.hide_render=False;o.hide_viewport=False
   out.append(o)
 print('ASSET LOADED',asset,[o.name for o in out],flush=True)
 return out
island=load_asset('island_tree_02',lambda n:n=='island_tree_02_LOD1')
small=load_asset('tree_small_02',lambda n:n=='tree_small_02_LOD1')
pines=load_asset('pine_tree_01',lambda n:n.endswith('LOD2') and ('tree_01_' in n) and 'trunk' not in n and 'branch' not in n and 'twig' not in n)
shrubs=load_asset('shrub_01',lambda n:n in ['shrub_01_a_LOD2','shrub_01_b_LOD2','shrub_01_c_LOD2','shrub_01_i_LOD3'])
grasses=load_asset('grass_medium_01',lambda n:n in ['grass_medium_01_small_a_LOD1','grass_medium_01_small_b_LOD1','grass_medium_01_tall_a_LOD2'])

def instance(proto,name,loc,scale,col='04',rotation=None):
 o=bpy.data.objects.new(name,proto.data);COL[col].objects.link(o);o.location=loc;o.rotation_euler[2]=random.random()*2*pi if rotation is None else rotation
 o.scale=tuple(s*scale if isinstance(scale,(float,int)) else s*t for s,t in zip(proto.scale,(scale,)*3 if isinstance(scale,(float,int)) else scale))
 return o

# Custom blue-gum and Monterey-cypress silhouettes. Branches are real tubes and foliage consists of individual curved leaves.
def tree_proto(seed,kind):
 rng=random.Random(seed);m=Mesh();leaves=Mesh();H=rng.uniform(18,24) if kind=='gum' else rng.uniform(16,21)
 trunkRadius=.39 if kind=='gum' else .52;lean=Vector((rng.uniform(-1.4,1.4),rng.uniform(-.9,.9),0));last=Vector((0,0,0))
 for k in range(12):
  f=(k+1)/12;p=Vector((lean.x*f+sin(f*5)*.14,lean.y*f,H*f));m.tube(last,p,trunkRadius*(1-k/13),bark,r2=trunkRadius*(1-(k+1)/13),n=9);last=p
 crowns=[]
 for k in range(32 if kind=='gum' else 42):
  f=rng.uniform(.32,.90);a=rng.uniform(0,2*pi);L=rng.uniform(3.0,6.2)*(1-f*.55);origin=Vector((lean.x*f,lean.y*f,H*f))
  reach=Vector((cos(a)*L,sin(a)*L,rng.uniform(2,4.8) if kind=='gum' else rng.uniform(.2,2.2)))
  mid=origin+reach*.47+Vector((0,0,.35));end=origin+reach
  m.tube(origin,mid,.13*(1-f*.55),bark,r2=.067,n=7);m.tube(mid,end,.067,bark,r2=.018,n=6)
  for j in range(4):
   ang=a+rng.uniform(-1.3,1.3);en=end+Vector((cos(ang)*rng.uniform(.6,1.8),sin(ang)*rng.uniform(.6,1.8),rng.uniform(-.4,1.6)))
   m.tube(mid.lerp(end,.65),en,.032,bark,r2=.007,n=5);crowns.append((en,kind))
 for center,_ in crowns:
  for k in range(190 if kind=='gum' else 235):
   rr=rng.random()**(1/3);theta=rng.uniform(0,2*pi);zz=rng.uniform(-1,1);rad=math.sqrt(1-zz*zz)
   c=center+Vector((cos(theta)*rad*rr*1.55,sin(theta)*rad*rr*1.55,zz*rr*(1.10 if kind=='gum' else .67)))
   a=rng.uniform(0,2*pi);L=rng.uniform(.10,.22) if kind=='gum' else rng.uniform(.10,.20);W=L*(.21 if kind=='gum' else .55)
   u=Vector((cos(a),sin(a),rng.uniform(-1.8,.2))).normalized()*L;v=Vector((-sin(a),cos(a),0))*W
   ma=rng.choice(foliage);leaves.poly([c-u,c+v,c+Vector((0,0,.018))],ma);leaves.poly([c+v,c+u,c+Vector((0,0,.018))],ma);leaves.poly([c+u,c-v,c+Vector((0,0,.018))],ma);leaves.poly([c-v,c-u,c+Vector((0,0,.018))],ma)
 trunk=m.emit(('Eucalyptus' if kind=='gum' else 'Coastal cypress')+' prototype trunk %d'%seed,'08');leaf=leaves.emit('Individual leaves %d'%seed,'08')
 # Keep prototypes out of the shot while their mesh data remains editable.
 trunk.hide_render=True;leaf.hide_render=True;trunk.hide_set(True);leaf.hide_set(True)
 return trunk,leaf,H
custom=[tree_proto(544+i,'gum' if i<3 else 'cypress') for i in range(6)]

def customtree(x,y,scale=1,idx=None):
 proto=custom[random.randrange(len(custom)) if idx is None else idx];z=terrain(x,y);angle=random.random()*2*pi
 for p in proto[:2]:instance(p,p.name.split(' prototype')[0],(x,y,z),scale,'04',angle)
 # Irregular leaf-litter island, with no perfectly circular lawn border.
 m=Mesh();pts=[]
 for i in range(24):
  a=2*pi*i/24;r=random.uniform(1.7,2.4)*scale;xx=x+cos(a)*r;yy=y+sin(a)*r;pts.append((xx,yy,terrain(xx,yy)+.018))
 m.poly(pts,mulch);m.emit('Fallen leaves below canopy','05')

def valid_tree(x,y,margin=4):
 for b in BUILD:
  dx=x-b['cx'];dy=y-b['cy'];ca=cos(b['a']);sa=sin(b['a']);u=dx*ca+dy*sa;v=-dx*sa+dy*ca
  if abs(u)<b['w']/2+margin and abs(v)<b['d']/2+margin:return False
 for ps,w in roads:
  # Broad-phase sampling sufficient for scattering, exact meshes still define roads.
  for p in ps[::3]:
   if (p.x-x)**2+(p.y-y)**2<(w+margin)**2:return False
 return True
# Curated foreground placement leaves the building legible during the entire flight.
for x,y,s,i in [(10,-15,1.04,3),(-12,-13,.82,0),(-29,21,1.12,3),(39,-45,1.2,0),(58,-12,1.1,1),(56,42,1.1,2),(-61,-45,1.16,3),(-83,12,1.16,4),(-62,58,1.0,5),(-80,88,1.25,3),(34,72,.83,0),(-30,-75,1.0,4)]:
 if valid_tree(x,y,1.5):customtree(x,y,s,i)
for k in range(360):
 x=random.uniform(-230,175);y=random.uniform(-220,325)
 # Open grass behind the officers' row; dense woods farther west and across the boulevard.
 if -108<x<-30 and -45<y<100 and random.random()<.86:continue
 if -20<x<42 and -45<y<50:continue
 if not valid_tree(x,y,4):continue
 customtree(x,y,random.uniform(.75,1.35),random.randrange(6))
# Dense park woodland hems the residential clearing. Repeat mesh data, not construction work.
for k in range(265):
 x=random.uniform(-245,-78) if k<155 else random.uniform(48,180);y=random.uniform(-185,290)
 if valid_tree(x,y,2.8):customtree(x,y,random.uniform(.83,1.32),random.randrange(6))
# Real leaf geometry broadleaf ornamentals supplement the custom dominant woodland.
for x,y,s in [(11,11,1.05),(12,-29,1.1),(-12,19,1.3),(-19,39,1.1),(9,35,1.3),(-3,-47,1.4),(-20,-48,1.1),(-40,77,1.3)]:
 if small:instance(small[0],'Small garden tree',(x,y,terrain(x,y)),s)
# Garden shrubs: clipped low borders with individual leaves, never solid green primitives.
for b in BUILD:
 if b['num']>551:continue
 for side in [-1,1]:
  for j in range(24):
   xx=side*(b['w']/2-1.8)+random.uniform(-1.2,1.2);yy=-b['d']/2-.7+random.uniform(-.4,.4);x,y=coord(xx,yy,b)
   proto=random.choice(shrubs[:3]);instance(proto,'Foundation planting',(x,y,terrain(x,y)),random.uniform(3.7,4.8),'05')
# Lawn tufts concentrated around the hero, with continuous textured grass farther out.
hero=next(b for b in BUILD if b['num']==544)
for k in range(3000):
 u=random.uniform(-12,12);v=random.uniform(-18,-7);x,y=coord(u,v,hero)
 if any(abs(u-d)<1.13 for d in [-3.1,3.1]):continue
 if v<-16.5:continue
 instance(random.choice(grasses),'Short coastal grass',(x,y,terrain(x,y)+.017),random.uniform(.75,1.10),'05')
# Scattered natural leaves along pavement edges and garden paths.
leaf=Mesh()
for k in range(1300):
 u=random.uniform(-14,14);v=random.uniform(-21,-7);x,y=coord(u,v,hero);z=terrain(x,y)+.054;a=random.random()*pi;L=random.uniform(.035,.12)
 leaf.poly([(x-cos(a)*L,y-sin(a)*L,z),(x-sin(a)*.018,y+cos(a)*.018,z+.008),(x+cos(a)*L,y+sin(a)*L,z),(x+sin(a)*.018,y-cos(a)*.018,z+.007)],dry if k%3 else terra[0])
leaf.emit('Windblown eucalyptus leaves','05')
print('LANDSCAPE COMPLETE',len(bpy.data.objects),flush=True)
# Additional conifers use documented, baked Poly Haven meshes at sensible distance.
if pines:
 for x,y,s in [(10,-15,.96),(-19,9,.98),(-43,31,1.07),(-66,-22,1.15),(-58,88,1.0),(-108,32,1.2),(-132,4,1.12),(-99,-66,1.3),(50,98,1.05),(97,27,.92),(-45,-102,.94),(-167,120,1.2)]:
  if valid_tree(x,y,1.0):instance(random.choice(pines),'Mature conifer',(x,y,terrain(x,y)),s)
# Rear sash and back-lane details make the elevated view complete.
for b in BUILD:
 if b['num']>551:continue
 m=Mesh();w=b['w'];d=b['d'];xs=[-w/2+2+i*2.7 for i in range(int((w-2)/2.7))]
 for xx in xs:
  for zz in [2.55,5.65]:window(m,xx,-d/2-.03,zz,1.0,1.7,side=pi)
 m.emit('%d | rear sash'%b['num'],'03' if b['num']!=544 else '02',(b['cx'],b['cy'],terrain(b['cx'],b['cy'])),b['a'])

street=Mesh()
for x,y in [(20,-19),(22,-67),(0,55),(-45,113),(43,-121)]:
 z=terrain(x,y);street.tube((x,y,z),(x,y,z+7.7),.11,metal,r2=.065,n=12)
 street.tube((x,y,z+7.5),(x+1.3,y,z+8.0),.047,metal,n=8)
 street.box((x+1.42,y,z+7.98),(.67,.26,.14),metal)
 street.box((x+1.42,y,z+7.90),(.51,.20,.025),trim)
 street.box((x,y,z+.16),(.32,.32,.32),concrete)
# Traditional park bench; all slats and curved armatures are modeled.
def bench(x,y,a):
 m=Mesh()
 for yy in [-.20,-.1,0,.1,.2]:m.box((0,yy,.49),(1.95,.08,.045),bronze)
 for z in [.7,.82,.94,1.06]:m.box((0,.27,z),(1.95,.04,.075),bronze)
 for xx in [-.77,.77]:
  m.tube((xx,-.19,0),(xx,-.19,.48),.033,bronze);m.tube((xx,.23,0),(xx,.29,1.14),.033,bronze)
  m.tube((xx,-.19,.75),(xx,.29,.75),.033,bronze);m.tube((xx,-.19,.48),(xx,-.19,.75),.026,bronze)
 m.emit('Presidio bench | individual steel slats','06',(x,y,terrain(x,y)+.06),a)
bench(17,-13,hero['a']);bench(-1,78,math.radians(65))
# Simple public road signage.
x,y=38,-31;z=terrain(x,y);street.tube((x,y,z),(x,y,z+2.45),.036,metal)
street.box((x,y,z+2.30),(.70,.075,.70),yellow,rot=pi/4)
# Utility covers and drains are set flush with their host surface.
for x,y in [(22,-9),(18,21),(28,-43),(-19,-3)]:
 z=terrain(x,y);street.box((x,y,z+.055),(.66,1.05,.035),metal)
 for j in range(8):street.box((x,y-.43+j*.12,z+.076),(.53,.035,.025),black)
# Bike-lane arrow markings near the hero.
for x,y in [(28,-39),(31,-15),(20,25)]:
 z=terrain(x,y)+.06;street.box((x,y,z),(.12,1.6,.008),white)
 street.poly([(x-.45,y+.4,z),(x,y+1.1,z),(x+.45,y+.4,z),(x+.22,y+.4,z),(x,y+.7,z),(x-.22,y+.4,z)],white)
street.emit('Street lamps signs drains and lane details','06')

# Window lighting is restrained: a warm reflection of occupied rooms, no orange floodlights.
world=bpy.data.worlds.new('Cool maritime morning sky');sc.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;n.clear();out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.65
if (AS/'sky.hdr').exists():
 tex=n.new('ShaderNodeTexEnvironment');tex.image=bpy.data.images.load(str(AS/'sky.hdr'));tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=math.radians(108);l.new(tc.outputs['Generated'],mapping.inputs['Vector']);l.new(mapping.outputs['Vector'],tex.inputs['Vector']);l.new(tex.outputs['Color'],bg.inputs['Color'])
else:bg.inputs['Color'].default_value=(.45,.61,.82,1)
l.new(bg.outputs[0],out.inputs[0])
light=bpy.data.lights.new('Low morning sun from the bay','SUN');light.energy=2.3;light.color=(1.0,.88,.73);light.angle=math.radians(3.0)
sun=bpy.data.objects.new('Morning sun',light);COL['07'].objects.link(sun);direction=Vector((-1,.28,-.70));sun.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
# Broad cool skylight fill subtly illuminates portico recesses.
ld=bpy.data.lights.new('Sky bounce','AREA');ld.energy=1300;ld.shape='DISK';ld.size=35;ld.color=(.65,.78,1.0)
lo=bpy.data.objects.new('Sky bounce',ld);COL['07'].objects.link(lo);lo.location=(24,-3,24);lo.rotation_euler=(Vector((0,0,3))-lo.location).to_track_quat('-Z','Y').to_euler()
camd=bpy.data.cameras.new('Architectural cinema | 36 mm sensor');cam=bpy.data.objects.new('Camera | continuous 30 second flight',camd);COL['07'].objects.link(cam);sc.camera=cam;camd.lens=36;camd.sensor_width=36;camd.clip_end=1500
focus=bpy.data.objects.new('Focus and attention point',None);COL['07'].objects.link(focus);focus.empty_display_size=.3
camd.dof.use_dof=True;camd.dof.focus_object=focus;camd.dof.aperture_fstop=8.0;camd.dof.aperture_blades=7
# Hermite spline gives a continuous velocity through key views and a soft start/finish.
keys=[(1,(68,-58,36),(-3,14,4.8),36),(150,(39,-30,17),(0,3,4.2),36),(300,(25,-11,7.0),(0,.8,3.65),34),(450,(20,5,4.8),(0,2,3.0),33),(570,(28,24,10.8),(0,4,4.3),35),(720,(53,49,26),(-8,14,5.8),37)]
def interp(t,index):
 i=next((i for i in range(len(keys)-1) if keys[i][0]<=t<=keys[i+1][0]),len(keys)-2)
 a=keys[i];b=keys[i+1];u=(t-a[0])/(b[0]-a[0]);dt=b[0]-a[0]
 val=lambda k:Vector(k[index]) if index in [1,2] else k[index]
 p=val(a);q=val(b);prev=keys[max(0,i-1)];nxt=keys[min(len(keys)-1,i+2)]
 m0=(val(b)-val(prev))/(b[0]-prev[0]) if i else (q-p)/dt*.25
 m1=(val(nxt)-val(a))/(nxt[0]-a[0]) if i<len(keys)-2 else (q-p)/dt*.25
 return (2*u**3-3*u*u+1)*p+(u**3-2*u*u+u)*dt*m0+(-2*u**3+3*u*u)*q+(u**3-u*u)*dt*m1
for f in range(1,721):
 cam.location=interp(f,1);focus.location=interp(f,2);cam.rotation_euler=(focus.location-cam.location).to_track_quat('-Z','Y').to_euler();camd.lens=interp(f,3)
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f);focus.keyframe_insert('location',frame=f);camd.keyframe_insert('lens',frame=f)
sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=True;sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.035
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for device in prefs.devices:device.use=device.type=='METAL'
 sc.cycles.device='GPU'
except Exception as e:print('GPU setup',e)
sc.cycles.max_bounces=5;sc.cycles.diffuse_bounces=2;sc.cycles.glossy_bounces=3;sc.cycles.transparent_max_bounces=6
sc.render.resolution_x=1920;sc.render.resolution_y=1080;sc.render.resolution_percentage=100;sc.render.fps=24;sc.frame_start=1;sc.frame_end=720
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB';sc.render.image_settings.color_depth='8';sc.render.image_settings.compression=18
sc.render.film_transparent=False
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=.45
sc.render.use_persistent_data=True
# Record source and practical uncertainty in the editable scene itself.
text=bpy.data.texts.new('READ ME — scene provenance and controls');text.write((ROOT/'work/BRIEF.md').read_text())
sc['Site reference']='37.797592 N, -122.451569 E; x East, y North; meters'
sc['Production']='720 native frames at 24 fps. Check work/BRIEF.md for evidence and inferred details.'
sc.frame_set(300)
# All externally sourced textures are packed, so the scene travels as one file.
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Presidio_544B.blend'))
print('SAVED',len(bpy.data.objects),'objects',flush=True)
if os.environ.get('PREVIEW','1')=='1':
 sc.render.resolution_percentage=60;sc.cycles.samples=20
 for f in [300,1,450,720]:
  sc.frame_set(f);sc.render.filepath=str(ROOT/'work'/('preview_%04d.png'%f));t=time.time();bpy.ops.render.render(write_still=True);print('PREVIEW',f,round(time.time()-t,2),flush=True)
