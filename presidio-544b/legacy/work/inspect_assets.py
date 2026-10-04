import bpy,os
from pathlib import Path
base=Path('/Users/lucaschu/Documents/ChatGPT/Renders/work/assets')
for asset in ['island_tree_02','tree_small_02','shrub_01','grass_medium_01','pine_tree_01']:
 p=base/asset/(asset+'.blend')
 if not p.exists():continue
 print('\nASSET',asset,p.stat().st_size,flush=True)
 try:
  with bpy.data.libraries.load(str(p),link=False) as (src,dst):
   print('COLLECTIONS',src.collections,flush=True);dst.objects=src.objects
  for o in dst.objects:
   if o:print('OBJ',o.name,o.type,tuple(round(v,2) for v in o.dimensions),len(o.data.vertices) if o.type=='MESH' else '',[(m.name,m.type) for m in o.modifiers],flush=True)
  for o in dst.objects:
   if o:bpy.data.objects.remove(o,do_unlink=True)
 except Exception as e:print(e)
