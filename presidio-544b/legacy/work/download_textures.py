import pathlib,json,subprocess,concurrent.futures
P=pathlib.Path('work/assets/textures');P.mkdir(exist_ok=True)
ids=['asphalt_02','leafy_grass','white_plaster_rough_01','bark_bluegum','brown_mud_leaves_01']
def get(a):
 p=P/(a+'.json');subprocess.run(['curl','-L','-s','-A','Mozilla/5.0','https://api.polyhaven.com/files/'+a,'-o',str(p)])
 try:
  j=json.loads(p.read_text())
  for k in ['diff','nor_gl','rough']:
   q=j.get(k,{}).get('2k',{});v=q.get('jpg',q.get('png',q.get('exr')))
   if not v:continue
   ext=v['url'].split('.')[-1];dst=P/(a+'_'+k+'.'+ext)
   subprocess.run(['curl','-L','-s','--fail','--max-time','90','-A','Mozilla/5.0',v['url'],'-o',str(dst)])
   print(dst.name,flush=True)
 except Exception as e:print(a,e,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,ids))
