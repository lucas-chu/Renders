import bpy, json, os, shutil
R='/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa';W=R+'/work/beauty';O=R+'/outputs'
old=bpy.data.scenes.get('Film | 30-second edit')
if old:bpy.data.scenes.remove(old)
s=bpy.data.scenes.new('Film | 30-second edit');s.frame_start=1;s.frame_end=720;s.render.fps=24;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
ed=s.sequence_editor_create()
for sh in json.load(open(W+'/shots.json')):
 strip=ed.strips.new_scene(sh['camera'],bpy.data.scenes[sh['scene']],channel=1,frame_start=1)
 strip.frame_final_start=sh['start'];strip.frame_final_end=sh['end']+1;strip.scene_camera=bpy.data.objects[sh['camera']];strip.scene_input='CAMERA'
 s.timeline_markers.new(sh['camera'],frame=sh['start'])
audio=O+'/O_Canada_Beauty_Soundtrack.wav';shutil.copy2(R+'/work/beauty/O_Canada_30s.wav',audio)
strip=ed.strips.new_sound('O Canada | Toronto Symphony Orchestra',audio,channel=2,frame_start=1);strip.frame_final_end=721
strip.sound.filepath='//O_Canada_Beauty_Soundtrack.wav'
s['Delivery']='30 seconds, 24 fps. Select this scene to render the entire edit with music.'
s['Music credit']='Toronto Symphony Orchestra, conducted by Peter Oundjian. Canadian Heritage official instrumental O Canada recording.'
inside=bpy.data.scenes['Interior | Bar 1608'];bpy.context.window.scene=inside;inside.frame_set(445)
for scene in bpy.data.scenes:
 if scene.name.startswith(('Exterior','Interior')):scene.render.use_motion_blur=False;scene.render.motion_blur_shutter=.35;scene.cycles.denoising_use_gpu=True
bpy.ops.wm.save_as_mainfile(filepath=O+'/Chateau_Frontenac_Beauty.blend')
print('EDIT VERIFIED',[(v.name,v.frame_final_start,v.frame_final_end) for v in ed.strips],flush=True)
