import bpy,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
# Object-space triplanar image lookup must not use tangent normals without UVs.
# Height-derived bump remains consistent across the large paving triangle fan.
for name in ['Paving','Marble','Terracotta']:
 mat=bpy.data.materials[name];n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bump=next((x for x in n if x.type=='BUMP'),None)
 if bump:
  img=next((x for x in n if x.type=='TEX_IMAGE' and x.image and '_rough' in x.image.name),None)
  if img:l.new(img.outputs['Color'],bump.inputs['Height'])
  bump.inputs['Strength'].default_value=.20 if name=='Paving' else .08;bump.inputs['Distance'].default_value=.025 if name=='Paving' else .012;l.new(bump.outputs[0],bs.inputs['Normal'])
s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.06
s.view_settings.exposure=.12
# Compress the establishing perspective slightly to keep the distant city in frame
# without a strip of empty horizon. The path and clearance remain unchanged.
cam=s.camera
for f in range(1,145):
 s.frame_set(f);u=(f-1)/144;delta=4*(1-u)*(1-u)*(1+2*u);cam.data.lens+=delta;cam.data.keyframe_insert('lens',frame=f)
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
print('PICTURE LOCK SAVED',flush=True)
os.environ.update(COLOSSEUM_ENGINE='BLENDER_EEVEE',COLOSSEUM_SAMPLES='32',COLOSSEUM_SCALE='100',COLOSSEUM_PREFIX='locked_',COLOSSEUM_FRAMES='1,350,650')
exec(compile((P/'scripts/render_film.py').read_text(),str(P/'scripts/render_film.py'),'exec'))
