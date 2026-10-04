from pathlib import Path
from PIL import Image
import fcntl
_export_lock=open('/private/tmp/frontenac_export.lock','w')
fcntl.flock(_export_lock,fcntl.LOCK_EX)
import subprocess,json,shutil,sys
R=Path('/Users/lucaschu/Documents/Codex/2026-09-04/https-maps-app-goo-gl-6kaddkvqd8j54t9fa');W=R/'work/beauty';O=R/'outputs';F=Path('/private/tmp/frontenac_beauty_frames');T=Path('/private/tmp/frontenac_encode');T.mkdir(exist_ok=True)
shots=json.loads((W/'shots.json').read_text());ff='/opt/homebrew/bin/ffmpeg';parts=[]
for idx,sh in enumerate(shots):
 n=sh['end']-sh['start']+1;duration=n/24;part=T/('shot%d.mp4'%idx)
 if part.exists():
  try:
   q=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=nb_frames:format=duration','-of','json',str(part)],stderr=subprocess.DEVNULL))
   if int(q['streams'][0].get('nb_frames',0))==n and abs(float(q['format']['duration'])-duration)<.01:
    parts.append(part);print('REUSING VERIFIED SHOT',idx+1,flush=True);continue
  except Exception:pass
 ids=list(range(sh['start'],sh['end']+1,2))+[sh['end']]
 ids=list(dict.fromkeys(ids))
 if not all((F/('%04d.png'%f)).exists() for f in ids):
  print('WAITING FOR SHOT',idx+1,flush=True);raise SystemExit(0)
 folder=T/('shot%d'%idx);folder.mkdir(exist_ok=True)
 for i,f in enumerate(ids):
  p=F/('%04d.png'%f)
  with Image.open(p) as im:
   assert im.size==(1920,1080),(f,im.size)
   if idx in (0,1,4):
    pixels=list(im.convert('RGB').resize((160,90)).crop((20,25,150,75)).getdata())
    red=sum(r>1.20*g and r>1.30*b and r>40 for r,g,b in pixels)/len(pixels)
    assert red>.025,('Brick shader validation failed',f,red)
   im.load()
  dest=folder/('%04d.png'%i)
  if dest.is_symlink() or dest.exists():dest.unlink()
  dest.symlink_to(p)
 n=sh['end']-sh['start']+1;duration=n/24;part=T/('shot%d.mp4'%idx);parts.append(part)
 if part.exists():
  q=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=nb_frames:format=duration','-of','json',str(part)]))
  if int(q['streams'][0].get('nb_frames',0))==n and abs(float(q['format']['duration'])-duration)<.01:
   print('SHOT ALREADY ENCODED',idx+1,flush=True);continue
 filt='tpad=start=2:stop=4:start_mode=clone:stop_mode=clone,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:search_param=16,trim=start=0.166666:duration=%.9f,settb=1/24,setpts=N'%duration
 subprocess.run([ff,'-y','-v','warning','-framerate','12','-start_number','0','-i',str(folder/'%04d.png'),'-vf',filt,'-frames:v',str(n),'-r','24','-fps_mode','cfr','-bf','0','-c:v','libx264','-preset','fast','-crf','17','-threads','6','-pix_fmt','yuv420p','-an',str(part)],check=True)
 print('SHOT ENCODED',idx+1,flush=True)
if '--parts-only' in sys.argv:raise SystemExit(0)
concat=T/'concat.txt';concat.write_text(''.join("file '%s'\n"%p for p in parts));native=O/'Chateau_Frontenac_Beauty_1080p.mp4';final=O/'Chateau_Frontenac_Beauty_4K_O_Canada.mp4'
subprocess.run([ff,'-y','-v','warning','-f','concat','-safe','0','-i',str(concat),'-i','/private/tmp/frontenac_beauty_audio.wav','-c:v','copy','-c:a','aac','-b:a','320k','-t','30','-movflags','+faststart',str(native)],check=True)
subprocess.run([ff,'-y','-v','warning','-i',str(native),'-vf','scale=3840:2160:flags=lanczos,unsharp=5:5:0.30:3:3:0','-c:v','libx264','-preset','fast','-crf','18','-threads','6','-r','24','-fps_mode','cfr','-bf','0','-c:a','copy','-metadata','title=Château Frontenac — Bar 1608 and the terrace','-metadata','comment=Cycles / Apple Metal path tracing; 1080p rendered at 12 fps, motion-interpolated to 24 fps and upscaled to 4K. O Canada: Toronto Symphony Orchestra, conductor Peter Oundjian; Canadian Heritage official recording.','-movflags','+faststart',str(final)],check=True)
probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(final)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');assert v['width']==3840 and v['height']==2160 and int(v['nb_frames'])==720 and v['r_frame_rate']=='24/1',v;assert abs(float(probe['format']['duration'])-30)<.05;assert a['channels']==2
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
subprocess.run(['python3',str(W/'verify_video.py'),str(final)],check=True)
shutil.copy('/private/tmp/frontenac_visual_verification.json',W/'visual_verification.json')
(W/'delivery_verification.json').write_text(json.dumps(probe,indent=2));print('Previews already retained in outputs',flush=True)
print('DELIVERY COMPLETE',str(final),flush=True)
