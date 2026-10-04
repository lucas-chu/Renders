import subprocess,json,sys
from pathlib import Path
import numpy as np
p=Path(sys.argv[1]);ff='/opt/homebrew/bin/ffmpeg'
probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert int(v['nb_frames'])==720 and v['r_frame_rate']=='24/1'
assert abs(float(probe['format']['duration'])-30)<.05 and a['channels']==2
b=subprocess.check_output([ff,'-v','error','-i',str(p),'-vf','scale=160:90','-f','rawvideo','-pix_fmt','rgb24','-an','-'])
frames=np.frombuffer(b,np.uint8).reshape(-1,90,160,3);assert len(frames)==720
scores=[]
for i in list(range(360))+list(range(648,720)):
 im=frames[i,25:75,20:150,:].astype(float);r,g,bl=im[:,:,0],im[:,:,1],im[:,:,2];score=float(((r>1.2*g)&(r>1.3*bl)&(r>40)).mean());scores.append(score)
 assert score>.025,('Exterior brick defect',i,score)
report={'frames':720,'duration':float(probe['format']['duration']),'size':[v['width'],v['height']],'audio_channels':a['channels'],'exterior_frames_checked':len(scores),'minimum_brick_color_fraction':min(scores)}
Path('/private/tmp/frontenac_visual_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
