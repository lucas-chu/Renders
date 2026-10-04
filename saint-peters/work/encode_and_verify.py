from pathlib import Path
import json, subprocess
R=Path('/Users/lucaschu/Documents/Codex/2026-09-04/make')
frames=Path((R/'work/staging_path.txt').read_text().strip())
missing=[i for i in range(1,721) if not (frames/f'frame_{i:04d}.png').is_file()]
if missing:raise RuntimeError(f'Missing {len(missing)} frames; first {missing[:8]}')
out=R/'outputs/Saint_Peters_Basilica_30s.mp4'
subprocess.run(['/opt/homebrew/bin/ffmpeg','-hide_banner','-nostdin','-xerror','-y','-framerate','24','-start_number','1','-i',str(frames/'frame_%04d.png'),'-frames:v','720','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-metadata','title=Morning at Saint Peter’s','-metadata','comment=Architectural reconstruction. Map outlines © OpenStreetMap contributors. See Scene_notes.md.',str(out)],check=True)
p=subprocess.run(['/opt/homebrew/bin/ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=width,height,r_frame_rate,nb_read_frames:format=duration','-of','json',str(out)],capture_output=True,text=True,check=True)
j=json.loads(p.stdout);v=j['streams'][0]
assert v['width']==1920 and v['height']==1080 and v['r_frame_rate']=='24/1' and v['nb_read_frames']=='720',j
assert abs(float(j['format']['duration'])-30)<.01,j
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
(R/'work/video_verification.json').write_text(json.dumps(j,indent=2))
# Decoded contact sheet, spanning the completed encoded video.
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(out),'-vf','fps=1/5,scale=640:360,tile=3x2','-frames:v','1',str(R/'work/final_contact_sheet.jpg')],check=True)
print('VERIFIED',p.stdout,flush=True)
