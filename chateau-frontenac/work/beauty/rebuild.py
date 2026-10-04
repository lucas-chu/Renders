"""Run inside Blender after opening the original Chateau_Frontenac.blend."""
import runpy,os
base=os.path.dirname(os.path.abspath(__file__))
for stage in ['build_beauty.py','refine.py','add_finish.py','context_and_light.py','fix_glassware.py','master_edit.py','bake_brick.py']:
 runpy.run_path(os.path.join(base,stage),run_name='__main__')
