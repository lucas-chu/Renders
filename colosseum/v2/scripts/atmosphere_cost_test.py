import bpy,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
bpy.data.objects['Atmospheric depth'].hide_render=True
os.environ.update(COLOSSEUM_ENGINE='CYCLES',COLOSSEUM_SAMPLES='24',COLOSSEUM_SCALE='100',COLOSSEUM_PREFIX='clear_',COLOSSEUM_FRAMES='1,350')
exec(compile((P/'scripts/render_film.py').read_text(),'render_film.py','exec'))
