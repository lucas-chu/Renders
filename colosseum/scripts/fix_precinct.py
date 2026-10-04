import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.frame_set(1);deps=bpy.context.evaluated_depsgraph_get()
for i in range(12):
 a=i*math.tau/12;p=Vector((128*math.cos(a),110*math.sin(a),90));hit,loc,n,idx,ob,mat=s.ray_cast(deps,p,Vector((0,0,-1)));print('FLOOR',i,ob.name if ob else None,tuple(loc),flush=True)
# One unambiguous level surface over the full public precinct.
bpy.ops.mesh.primitive_cylinder_add(vertices=256,radius=1,depth=.16,end_fill_type='NGON',location=(0,0,.10));ob=bpy.context.object;ob.name='Precinct — continuous travertine paving datum';ob.scale=(149,130,1);ob.data.materials.append(bpy.data.materials['Paving'])
for q in bpy.data.objects:
 if q.type=='MESH' and q.name.startswith('12 |'):q.location.z-=.09
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
os.environ.update(COLOSSEUM_ENGINE='BLENDER_EEVEE',COLOSSEUM_SAMPLES='32',COLOSSEUM_SCALE='100',COLOSSEUM_PREFIX='delivery_',COLOSSEUM_FRAMES='1')
exec(compile((P/'scripts/render_film.py').read_text(),str(P/'scripts/render_film.py'),'exec'))
