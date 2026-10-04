import bpy
s=bpy.context.scene
s.frame_start=1;s.frame_end=720;s.frame_set(1)
s.render.filepath='//renders/frame_'
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False;a.spaces.active.shading.type='RENDERED'
t=bpy.data.texts.get('READ ME — scene and sources')
if t:t.clear();t.write(open('/Users/lucaschu/Documents/Codex/2026-09-04/make/outputs/Scene_notes.md').read())
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath='/Users/lucaschu/Documents/Codex/2026-09-04/make/outputs/Saint_Peters_Basilica.blend')
