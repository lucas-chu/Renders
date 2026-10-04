import bpy,os,time
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=bpy.context.scene
s.render.resolution_percentage=50;s.cycles.samples=16
for f in [1,270,360,540,720]:
 s.frame_set(f);s.render.filepath=os.path.join(R,'work','check_%03d.png'%f);t=time.time();bpy.ops.render.render(write_still=True);print('CHECK',f,time.time()-t,flush=True)
