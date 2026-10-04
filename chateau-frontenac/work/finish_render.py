import subprocess,time,pathlib,os,json
R=pathlib.Path(__file__).resolve().parent.parent
os.chdir(R)
frames=R/'work/frames';log=R/'work/render_watchdog.log'
def count():return len(list(frames.glob('*.png')))
restarts=0
while count()<720:
 before=count();print('RESUME',before,flush=True)
 with log.open('a') as out:
  p=subprocess.Popen(['/Applications/Blender.app/Contents/MacOS/Blender','-b','outputs/Chateau_Frontenac.blend','-t','8','--python','work/render_film.py'],stdout=out,stderr=subprocess.STDOUT)
  last=time.monotonic();lastcount=before;started=False
  while p.poll() is None:
   time.sleep(3);n=count()
   if n>lastcount:lastcount=n;last=time.monotonic();started=True
   limit=65 if started else 180
   if time.monotonic()-last>limit:
    print('RESTART stalled renderer; completed',n,flush=True);p.terminate()
    try:p.wait(timeout=8)
    except subprocess.TimeoutExpired:p.kill();p.wait()
    restarts+=1;break
  if p.returncode not in [0,None,-15,-9]:print('RENDER EXIT',p.returncode,flush=True)
 # Verify any most recent PNG, which may have been interrupted while saving.
 from PIL import Image
 for f in sorted(frames.glob('*.png'))[-2:]:
  try:
   with Image.open(f) as im:im.verify()
  except Exception:f.rename(f.with_suffix('.incomplete'))
 if count()==before:time.sleep(3)
print('ENCODING',flush=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','warning','-framerate','24','-start_number','1','-i','work/frames/%04d.png','-frames:v','720','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart','outputs/Chateau_Frontenac_Flythrough.mp4'],check=True)
print('COMPLETE',flush=True)
