"""Resume native frames, restart a stalled render, then verify and encode."""
from pathlib import Path
import subprocess,os,time,json,signal
from PIL import Image
P=Path(__file__).resolve().parents[1];BLENDER='/Applications/Blender.app/Contents/MacOS/Blender'
engine=os.environ.get('COLOSSEUM_ENGINE','BLENDER_EEVEE');samples=os.environ.get('COLOSSEUM_SAMPLES','32')
env=os.environ.copy();env.update(COLOSSEUM_ENGINE=engine,COLOSSEUM_SAMPLES=samples,COLOSSEUM_SCALE='100');env.pop('COLOSSEUM_FRAMES',None)
frames=P/'frames';frames.mkdir(exist_ok=True)
def done():return sorted(frames.glob('[0-9][0-9][0-9][0-9].png'))
restarts=0
while len(done())<720:
 with open(P/'animation.log','a',buffering=1) as log:
  proc=subprocess.Popen([BLENDER,'-b',str(P/'output/Colosseum_AD160.blend'),'-t','6','--python',str(P/'scripts/render_film.py')],stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
  count=len(done());last=time.time();start=time.time()
  while proc.poll() is None:
   time.sleep(10);files=done()
   if len(files)>count:
    count=len(files);last=time.time();print(f'PROGRESS {count}/720',flush=True)
   if time.time()-last>(900 if count<3 else 420):
    print('RESTART: frame timed out',flush=True);os.killpg(proc.pid,signal.SIGTERM);time.sleep(3)
    if proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL)
    restarts+=1;break
  if len(done())<720 and proc.returncode is not None:
   restarts+=1
   if restarts>6:raise RuntimeError('Repeated renderer failures; inspect animation.log')
   time.sleep(3)
for i in range(1,721):
 p=frames/f'{i:04d}.png'
 with Image.open(p) as im:
  im.load()
  if im.size!=(1920,1080):raise ValueError((str(p),im.size))
out=P/'output/Colosseum_30s_Flythrough.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','24','-start_number','1','-i',str(frames/'%04d.png'),'-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(out)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));(P/'output/verification.json').write_text(json.dumps(probe,indent=2))
s=probe['streams'][0];assert s['nb_read_frames']=='720';assert abs(float(probe['format']['duration'])-30)<.01
print('COMPLETE',str(out),flush=True)
