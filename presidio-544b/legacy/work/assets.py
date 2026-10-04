import subprocess,json,concurrent.futures,pathlib
P=pathlib.Path('work/assets');P.mkdir(exist_ok=True)
ids=['island_tree_01','island_tree_02','island_tree_03','tree_small_02','shrub_01','grass_medium_01','kloofendal_48d_partly_cloudy_puresky']
def meta(a):
 p=P/(a+'.json');subprocess.run(['curl','-L','-s','-A','Mozilla/5.0','https://api.polyhaven.com/files/'+a,'-o',str(p)])
 try:
  j=json.loads(p.read_text());print(a,[(k,j.get(k,{}).get('1k',{})) for k in ['blend']][:1],flush=True)
 except:pass
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(meta,ids))
