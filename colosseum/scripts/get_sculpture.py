import pathlib,json,urllib.request,concurrent.futures,subprocess
P=pathlib.Path('colosseum');j=json.loads((P/'references/met-catalog.json').read_text());chosen=[x for x in j if x['object_id'] in [242017,242211,254613,204758]]
def get(x):
 id=x['object_id'];u=next(f['download_url'] for f in x['files'] if f['format']=='GLB')
 (P/f'assets/met_{id}.glb').write_bytes(subprocess.check_output(['curl','-Lf','--max-time','60',u]))
 try:
  data=json.loads(subprocess.check_output(['curl','-Lf','--max-time','30',f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}']));(P/f'references/met_{id}.json').write_text(json.dumps(data));u=data['primaryImageSmall'];(P/f'references/met_{id}.jpg').write_bytes(subprocess.check_output(['curl','-Lf','--max-time','30',u]))
 except Exception as e:print(e,flush=True)
 print(id,x['title'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,chosen))
(P/'references/sculpture-credits.json').write_text(json.dumps(chosen,indent=2))
