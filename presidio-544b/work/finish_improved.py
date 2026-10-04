from pathlib import Path
import subprocess,time,os,json
R=Path('/Users/lucaschu/.codex/artifacts/presidio-544b');F=R/'work/improved_frames';B='/Applications/Blender.app/Contents/MacOS/Blender';blend=R/'outputs/Presidio_544B_Improved.blend';retries=0
while True:
 todo=[i for i in range(1,721) if not (F/('%04d.jpg'%i)).exists() or (F/('%04d.jpg'%i)).stat().st_size<10000]
 if not todo:break
 if retries>=8:raise RuntimeError('Repeated renderer failure; inspect render.log before resuming.')
 env=os.environ.copy();env['START_FRAME']=str(min(todo));env['END_FRAME']='720'
 with open(R/'work/improved_render.log','a') as log:
  p=subprocess.Popen([B,'-b',str(blend),'-t','8','--python',str(R/'work/render_improved.py')],stdout=log,stderr=subprocess.STDOUT,env=env,cwd=R)
  print('RENDER_STARTED',p.pid,'remaining',len(todo),flush=True);last_change=time.time();last_count=720-len(todo)
  while p.poll() is None:
   time.sleep(10);count=len(list(F.glob('*.jpg')))
   if count!=last_count:last_count=count;last_change=time.time();print('PROGRESS',count,'/720',flush=True)
   if time.time()-last_change>(600 if last_count==0 else 180):
    print('RESTART_STALLED_RENDER',p.pid,flush=True);p.terminate()
    try:p.wait(timeout=15)
    except subprocess.TimeoutExpired:p.kill()
    break
  print('RENDER_EXIT',p.poll(),flush=True)
 retries+=1
print('ENCODING',flush=True);out=R/'outputs/Presidio_544B_Improved_Flythrough.mp4'
with open(R/'work/improved_encode.log','w') as log:subprocess.run(['ffmpeg','-y','-framerate','24','-start_number','1','-i',str(F/'%04d.jpg'),'-frames:v','720','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(out)],check=True,stdout=log,stderr=log)
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,nb_read_frames,r_frame_rate:format=duration,size','-of','json',str(out)],text=True));(R/'outputs/improved_verification.json').write_text(json.dumps(j,indent=2));s=j['streams'][0]
assert s['width']==1920 and s['height']==1080 and int(s['nb_read_frames'])==720 and abs(float(j['format']['duration'])-30)<.02
print('COMPLETE',str(out),flush=True)
