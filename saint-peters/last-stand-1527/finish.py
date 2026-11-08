"""Finish the 4K film. Usage: python3 finish.py path/to/frame-directory.
Requires NumPy and FFmpeg (libass, libx264) and installed Baskerville/Gill Sans or font substitutes.
"""
from pathlib import Path
import sys,subprocess,tempfile
from foley import make
D=Path(__file__).resolve().parent
F=Path(sys.argv[1]).resolve()
assert all((F/('f_%04d.jpg'%i)).is_file() for i in range(1,721))
ass=r"""[Script Info]
ScriptType: v4.00+
PlayResX: 1440
PlayResY: 810
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Title,Baskerville,76,&H00F4F4F5,&H0,&H80262421,&H90201B17,0,0,0,0,100,100,0,0,1,0.3,1,7,0,0,0,1
Style: Label,Gill Sans,18,&H00B8D8F1,&H0,&H80332922,&H90201B17,0,0,0,0,100,100,3,0,1,0.4,1,7,0,0,0,1
Style: Copy,Baskerville,31,&H00E7F0F4,&H0,&H90221F1B,&H90201B17,0,0,0,0,100,100,0,0,1,0.5,1,7,0,0,0,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
Dialogue: 0,0:00:00.15,0:00:05.85,Label,,0,0,0,,{\pos(78,570)\fad(450,850)}ROME   /   6 MAY 1527
Dialogue: 0,0:00:00.35,0:00:05.85,Title,,0,0,0,,{\pos(74,604)\fad(700,850)}The Last Stand
Dialogue: 0,0:00:00.65,0:00:05.85,Copy,,0,0,0,,{\pos(79,696)\fad(700,850)}The Swiss Guard at Old Saint Peter’s
Dialogue: 0,0:00:09.00,0:00:13.85,Label,,0,0,0,,{\pos(77,677)\fad(350,650)}THE DEFENSE
Dialogue: 0,0:00:09.15,0:00:13.85,Copy,,0,0,0,,{\pos(76,708)\fad(500,650)}Imperial troops close on the Swiss line.
Dialogue: 0,0:00:16.40,0:00:22.70,Label,,0,0,0,,{\pos(77,677)\fad(350,650)}PASSETTO DI BORGO
Dialogue: 0,0:00:16.55,0:00:22.70,Copy,,0,0,0,,{\pos(76,708)\fad(500,650)}Forty-two guards escort Clement VII to Castel Sant’Angelo.
Dialogue: 0,0:00:25.40,0:00:29.92,Label,,0,0,0,,{\an8\pos(720,322)\fad(700,350)}IN MEMORIAM
Dialogue: 0,0:00:25.75,0:00:29.92,Copy,,0,0,0,,{\an8\pos(720,385)\fs47\fad(700,350)}147 Swiss Guards died defending the pope.
"""
with tempfile.TemporaryDirectory() as td:
 Path(td,'titles.ass').write_text(ass)
 make(Path(td,'foley.wav'))
 # A graded lower edge protects caption contrast; the image fades to a memorial plate.
 vf="vignette=angle=PI/5:eval=init,drawbox=x=0:y=ih*0.8:w=iw:h=ih*0.2:color=black@0.55:t=fill:enable='between(t,9,13.85)+between(t,16.4,22.7)',fade=t=in:st=0:d=0.6,fade=t=out:st=25:d=2.4,subtitles=titles.ass,scale=3840:2160:flags=lanczos,setsar=1,format=yuv420p"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','24','-start_number','1','-i',str(F/'f_%04d.jpg'),'-i',str(D/'Ave Maria.m4a'),'-i','foley.wav','-filter_complex','[1:a][2:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.97:latency=1[a]','-map','0:v','-map','[a]','-vf',vf,'-t','30','-c:v','libx264','-preset','veryfast','-crf','19','-c:a','aac','-b:a','256k','-movflags','+faststart',str(D/'The Last Stand - 1527.mp4')],cwd=td,check=True)
