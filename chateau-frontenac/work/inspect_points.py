import bpy
from mathutils import Vector
s=bpy.context.scene;s.frame_set(650);c=s.camera;dg=bpy.context.evaluated_depsgraph_get();v=c.data.view_frame(scene=s)
for px,py in [(186,218),(303,229),(355,254),(470,50)]:
 x=px/960;y=1-py/540
 left=v[2].lerp(v[1],y);right=v[3].lerp(v[0],y);d=c.matrix_world.to_quaternion()@left.lerp(right,x).normalized();hit,loc,no,index,ob,mat=s.ray_cast(dg,c.location,d)
 print(px,py,hit,tuple(loc),ob.name if ob else '',flush=True)
print('TERRAIN bounds',[(min(v.co[i] for v in bpy.data.objects['Cap Diamant terrain'].data.vertices),max(v.co[i] for v in bpy.data.objects['Cap Diamant terrain'].data.vertices)) for i in range(3)])
