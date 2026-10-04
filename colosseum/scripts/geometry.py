import bpy,math,random,bmesh
from mathutils import Vector,Matrix
from contextlib import contextmanager
from collections import defaultdict
from math import sin,cos,pi,sqrt
T=Matrix.Identity(4); GROUP='Architecture'; B={}; MATS={}
@contextmanager
def frame(loc=(0,0,0),angle=0,scale=1,matrix=None):
 global T
 old=T.copy();T=T@(matrix if matrix is not None else Matrix.Translation(Vector(loc))@Matrix.Rotation(angle,4,'Z')@Matrix.Diagonal((scale,scale,scale,1)))
 yield
 T=old
@contextmanager
def group(name):
 global GROUP
 old=GROUP;GROUP=name;yield;GROUP=old

def geo(verts,faces,mat,smooth=False):
 key=(GROUP,mat);v,f,s=B.setdefault(key,([],[],[]));n=len(v);v.extend([tuple(T@Vector(x)) for x in verts]);f.extend([tuple(n+i for i in p) for p in faces]);s.extend([smooth]*len(faces))
def box(c,d,mat):
 x,y,z=c;a,b,h=[q*.5 for q in d]
 v=[(x+u*a,y+w*b,z+k*h) for k in [-1,1] for w in [-1,1] for u in [-1,1]]
 geo(v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat)
def polyprism(points,y0,y1,mat):
 n=len(points);v=[(x,y,z) for y in [y0,y1] for x,z in points];f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];geo(v,f,mat)
def lathe(c,profile,mat,n=24,flutes=0):
 x,y,z=c;v=[]
 for r,h in profile:
  for i in range(n):
   a=2*pi*i/n;rr=r*(1-.065*(1+cos(flutes*a))*.5) if flutes else r;v.append((x+rr*cos(a),y+rr*sin(a),z+h))
 f=[tuple(range(n-1,-1,-1))]
 for j in range(len(profile)-1):
  for i in range(n):f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 f.append(tuple(range((len(profile)-1)*n,len(profile)*n)));geo(v,f,mat,True)
def cylinder(c,r,h,mat,n=16,r2=None):lathe((c[0],c[1],c[2]-h/2),[(r,0),(r if r2 is None else r2,h)],mat,n)
def ellipsoid(c,r,mat,n=12,m=8):
 v=[]
 for j in range(m+1):
  p=pi*j/m
  for i in range(n):
   a=2*pi*i/n;v.append((c[0]+r[0]*sin(p)*cos(a),c[1]+r[1]*sin(p)*sin(a),c[2]+r[2]*cos(p)))
 geo(v,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(m) for i in range(n)],mat,True)
def beam(a,b,r,mat,n=8,r2=None):
 a,b=Vector(a),Vector(b);v=b-a;basis=v.to_track_quat('Z','Y').to_matrix().to_4x4();basis.translation=a
 with frame(matrix=basis):lathe((0,0,0),[(r,0),(r if r2 is None else r2,v.length)],mat,n)
def rope(points,r,mat='Rope',n=5):
 for a,b in zip(points[:-1],points[1:]):beam(a,b,r,mat,n)
def ellring(a,b,profile,mat,n=320,start=0,end=2*pi):
 # profile radius offset, height, clockwise boundary cross section
 v=[((a+dr)*cos(start+(end-start)*i/n),(b+dr)*sin(start+(end-start)*i/n),z) for i in range(n+1) for dr,z in profile];k=len(profile)
 f=[(i*k+j,(i+1)*k+j,(i+1)*k+(j+1)%k,i*k+(j+1)%k) for i in range(n) for j in range(k)]
 f += [tuple(range(k-1,-1,-1)),tuple(range(n*k,(n+1)*k))];geo(v,f,mat)
def ellipse_slab(a,b,z,th,mat,n=256):
 v=[(0,0,z),(0,0,z-th)]+[(a*cos(2*pi*i/n),b*sin(2*pi*i/n),zz) for zz in [z,z-th] for i in range(n)]
 f=[]
 for i in range(n):j=(i+1)%n;f += [(0,2+i,2+j),(1,2+n+j,2+n+i),(2+i,2+n+i,2+n+j,2+j)]
 geo(v,f,mat)
def arc(r,outer,spring,y0,y1,mat,n=18,joints=.013):
 for i in range(n):
  a=pi*i/n+joints*.5;b=pi*(i+1)/n-joints*.5
  polyprism([(r*cos(a),spring+r*sin(a)),(outer*cos(a),spring+outer*sin(a)),(outer*cos(b),spring+outer*sin(b)),(r*cos(b),spring+r*sin(b))],y0,y1,mat)
def archbay(width,height,opening,spring,depth,stone,detail=True):
 r=opening/2;outer=r+.48;piw=(width-opening)/2
 # coursed piers
 courses=max(1,int(spring/.68));h=spring/courses
 for side in [-1,1]:
  for k in range(courses):box((side*(r+piw/2),0,h*(k+.5)),(piw-.014,depth,h-.018),stone)
 arc(r,outer,spring,-depth/2,depth/2,stone,18 if detail else 12)
 # stone above arch curved extrados, in left/right quadrants
 for side in [-1,1]:
  for i in range(12):
   x0=side*width/2*i/12;x1=side*width/2*(i+1)/12
   z0=spring+sqrt(max(0,outer*outer-x0*x0));z1=spring+sqrt(max(0,outer*outer-x1*x1))
   polyprism([(x0,z0),(x1,z1),(x1,height),(x0,height)],-depth/2,depth/2,stone)
 if detail:
  for side in [-1,1]:box((side*(r+piw/2),.04,spring-.08),(piw+.18,depth+.2,.22),'Trim')
  polyprism([(-.25,spring+r-.1),(.25,spring+r-.1),(.35,spring+outer+.2),(-.35,spring+outer+.2)],depth/2,depth/2+.16,'Trim')
def column(x,y,z,h,r,order=0,mat='Trim',detailed=True):
 n=48 if detailed else 12
 # separate torus fillets and entasis silhouette
 p=[(r*1.27,0),(r*1.27,.13*h),(r*1.04,.15*h),(r,.18*h),(r*.94,.45*h),(r*.85,.85*h),(r*.92,.87*h),(r*.92,.9*h)]
 # shorten oversized base; absolute base heights scaled to h
 p=[(r*1.18,0),(r*1.18,.15),(r,.26),(r,.4),(r*.95,h*.38),(r*.83,h*.85),(r*.88,h*.88)]
 lathe((x,y,z),p,mat,n,flutes=16 if order>=2 and detailed else 0)
 cap=z+h*.88
 if order==0:
  lathe((x,y,cap),[(r*.88,0),(r*1.08,h*.055),(r*1.2,h*.07)],mat,n)
  box((x,y,z+h-.12),(r*2.5,r*2.5,.24),mat)
 elif order==1:
  box((x,y,z+h-.12),(r*2.7,r*2.1,.24),mat)
  lathe((x,y,cap),[(r*.88,0),(r*1.1,h*.08)],mat,n)
  if detailed:
   for side in [-1,1]:
    pts=[]
    for k in range(23):
     t=k/22*3*pi;rr=r*.37*(1-k/27);pts.append((x+side*r*.95+rr*cos(t),y+r*.86,z+h-.4+rr*sin(t)))
    rope(pts,r*.065,mat,6)
 else:
  lathe((x,y,cap),[(r*.85,0),(r*1.18,h*.09)],mat,n)
  box((x,y,z+h-.12),(r*2.6,r*2.6,.24),mat)
  if detailed:
   for ring in [0,1]:
    for i in range(8):
     a=2*pi*(i+.5*ring)/8;vv=[]
     for k in range(5):
      t=k/4;rr=r*(.8+.42*t*t);zz=cap+ring*h*.035+t*h*.065;ww=r*.28*sin(pi*t)+.025
      for sign in [-1,1]:vv.append((x+rr*cos(a)+sign*ww*sin(a),y+rr*sin(a)-sign*ww*cos(a),zz))
     geo(vv,[(2*k,2*k+1,2*k+3,2*k+2) for k in range(4)],mat,True)
def human(x,y,z,s=1,cloth='Linen',statue=False,pose=0):
 # draped bodies and contrapposto rather than billboard silhouettes
 mat='Marble' if statue else cloth;skin='Marble' if statue else 'Skin';hair='Marble' if statue else 'Hair'
 with frame((x,y,z),scale=s):
  # draped garment as folded varying elliptical radial mesh
  n=20 if statue else 8;v=[]
  levels=[(.35,.23,.1),(.33,.22,.35),(.29,.21,.72),(.23,.18,1.08),(.32,.18,1.37),(.23,.16,1.44)]
  for rx,ry,h in levels:
   for i in range(n):
    a=2*pi*i/n;fold=1+.13*sin(a*7+h*2);v.append((rx*cos(a)*fold,ry*sin(a)*fold,h))
  geo(v,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(levels)-1) for i in range(n)],mat,True)
  cylinder((0,0,1.48),.085,.16,skin,10);ellipsoid((.018,0,1.65),(.125,.12,.17),skin,16 if statue else 8,10 if statue else 5)
  ellipsoid((.012,-.025,1.71),(.132,.11,.12),hair,10,5)
  if statue:
   ellipsoid((.015,.117,1.64),(.035,.04,.045),skin,8,5)
   # diagonal mantle fold and its rim
   rope([(-.25,-.16,1.38),(-.12,-.24,1.18),(.12,-.27,.98),(.28,-.18,.76)],.043,mat)
  beam((-.27,0,1.34),(-.36,.08,.94),.074,skin,10)
  beam((-.36,.08,.94),(-.23,.16,.78),.06,skin,10)
  if pose%2:
   beam((.27,0,1.34),(.49,.02,1.5),.078,skin,10);beam((.49,.02,1.5),(.58,.04,1.88),.062,skin,10)
  else:
   beam((.27,0,1.34),(.36,-.05,1.04),.075,skin,10);beam((.36,-.05,1.04),(.22,.18,1.02),.06,skin,10)
  for side in [-1,1]:ellipsoid((side*.14,.09,.08),(.1,.2,.07),skin,8,5)
def flush():
 for (g,mat),(v,f,s) in B.items():
  mesh=bpy.data.meshes.new(g+' | '+mat);mesh.from_pydata(v,[],f);mesh.materials.append(MATS[mat]);mesh.update()
  ob=bpy.data.objects.new(g+' | '+mat,mesh)
  col=bpy.data.collections.get(g)
  if not col:col=bpy.data.collections.new(g);bpy.context.scene.collection.children.link(col)
  col.objects.link(ob)
  for p,sm in zip(mesh.polygons,s):p.use_smooth=sm
  # Ensure consistency even for locally mirrored facade frames.
  bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(mesh);bm.free()
  print('MESH',g,mat,len(v),len(f),flush=True)
 B.clear()
