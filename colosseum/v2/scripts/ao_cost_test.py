import bpy,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
for m in bpy.data.materials:
 if m.use_nodes:
  for n in m.node_tree.nodes:
   if n.type=='AMBIENT_OCCLUSION':
    print('AO',m.name,n.samples,'-> 1',flush=True);n.samples=1
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_Optimized_Candidate.blend'))
os.environ.update(COLOSSEUM_ENGINE='CYCLES',COLOSSEUM_SAMPLES='24',COLOSSEUM_SCALE='100',COLOSSEUM_PREFIX='ao1_',COLOSSEUM_FRAMES='1,350')
exec(compile((P/'scripts/render_film.py').read_text(),'render_film.py','exec'))
