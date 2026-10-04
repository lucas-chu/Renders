import bpy,sys,json,math
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
import geometry as G
from geometry import group,ellring,flush
s=bpy.context.scene
G.MATS.update({m.name:m for m in bpy.data.materials})
with group('02b | Colosseum — floor continuity'):
 for low,high in [(23.90,24.40),(35.30,36.0)]:ellring(93.35,76.85,[(-1.18,low),(1.02,low),(1.02,high),(-1.18,high)],'Travertine')
flush()
for name,file in [('READ ME — scene and evidence','SCENE_PLAN.md'),('SHOT MANIFEST','shot_manifest.json')]:
 text=bpy.data.texts.get(name) or bpy.data.texts.new(name);text.clear();text.write((P/file).read_text())
for f,name in [(1,'01 — Rome reveals itself'),(241,'02 — The order of the arcades'),(457,'03 — Rise toward the velarium'),(650,'04 — The marble cavea')]:s.timeline_markers.new(name,frame=f)
s['Model envelope, meters']='189 x 156 x 48.5';s['Design period']='circa AD 160';s['Facade']='80 bays per order; 240 awning masts';s['Evidence and assumptions']='See embedded READ ME — scene and evidence'
# Analytical check of the camera envelope, excluding the interval above the roof.
clearance=[]
for f in range(1,721):
 s.frame_set(f);p=s.camera.location
 if p.z<59:
  r=math.sqrt((p.x/96)**2+(p.y/79.5)**2);clearance.append((r,f,p.z))
assert min(c[0] for c in clearance)>1.12
(P/'camera_validation.json').write_text(json.dumps({'minimum_normalized_exterior_radius_below_59m':min(clearance),'checked_frames':720},indent=2))
# Respond to the draft: restore sunlight contrast and remove schematic hills.
for ob in list(bpy.data.objects):
 if ob.name.startswith('23 |'):bpy.data.objects.remove(ob,do_unlink=True)
s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.20
sun=bpy.data.lights.get('Late afternoon sun');sun.energy=3.8;sun.color=(1,.86,.68);sun.angle=.025
from mathutils import Vector
bpy.data.objects.get('Late afternoon sun').rotation_euler=Vector((.7,.55,-.46)).to_track_quat('-Z','Y').to_euler()
bpy.data.lights.get('Open sky above the cavea').energy=22000
bpy.data.lights.get('Open sky above the cavea').use_shadow=False
bpy.data.materials['Distant golden air'].node_tree.nodes.get('Principled Volume').inputs['Density'].default_value=.00016
s.view_settings.exposure=0
s.frame_set(1)
for sc in bpy.data.screens:
 for area in sc.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.shading.color_type='MATERIAL';area.spaces.active.clip_end=3500;area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'output/Colosseum_AD160.blend'))
print('REFINEMENT COMPLETE',flush=True)
