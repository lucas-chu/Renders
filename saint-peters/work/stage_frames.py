from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import tempfile,subprocess,time,shutil
R=Path('/Users/lucaschu/Documents/Codex/2026-09-04/make')
dest=Path(tempfile.mkdtemp(prefix='saint_peters_frames_'));(R/'work/staging_path.txt').write_text(str(dest));src=R/'work/frames'
def copy(i):
 p=src/f'frame_{i:04d}.png'
 for attempt in range(15):
  try:
   data=p.read_bytes()
   assert data[:8]==b'\x89PNG\r\n\x1a\n' and len(data)>10000
   (dest/p.name).write_bytes(data);return i
  except OSError:
   subprocess.run(['brctl','download',str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   time.sleep(1)
 raise RuntimeError(f'Could not restore frame {i}')
with ThreadPoolExecutor(max_workers=8) as ex:
 fs=[ex.submit(copy,i) for i in range(1,721)]
 for k,f in enumerate(as_completed(fs),1):
  f.result()
  if k%60==0:print('RESTORED',k,flush=True)
print('READY',dest,flush=True)
