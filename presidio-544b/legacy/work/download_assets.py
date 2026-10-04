import pathlib,json,subprocess,concurrent.futures
P=pathlib.Path('work/assets');jobs=[]
for a in ['pine_tree_01','island_tree_02','tree_small_02','shrub_01','grass_medium_01']:
 src=pathlib.Path('work/references/pine-files.json') if a=='pine_tree_01' else P/(a+'.json')
 j=json.loads(src.read_text())['blend']['1k']['blend'];d=P/a;d.mkdir(exist_ok=True)
 jobs.append((d/(a+'.blend'),j['url']))
 for n,v in j['include'].items():jobs.append((d/n,v['url']))
j=json.loads((P/'kloofendal_48d_partly_cloudy_puresky.json').read_text());print('HDR',list(j),flush=True)
if 'hdri' in j:
 v=j['hdri']['4k']['hdr'];jobs.append((P/'sky.hdr',v['url']))
def dl(it):
 p,u=it;p.parent.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['curl','-L','-s','--fail','--retry','2','--max-time','240','-A','Mozilla/5.0',u,'-o',str(p)])
 print(p.name,p.stat().st_size if p.exists() else 'FAIL',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(dl,jobs))
