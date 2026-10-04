import json,math,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as p
j=json.load(open('work/references/hotel-osm.json'));k=json.load(open('work/references/osm.json'))
def xy(g):return [(v['lon']+71.205283)*76130 for v in g],[(v['lat']-46.811891)*111195 for v in g]
fig,ax=p.subplots(figsize=(12,12))
for e in k['elements']:
 g=e.get('geometry',[])
 if not g:continue
 x,y=xy(g)
 if e.get('tags',{}).get('building'):ax.fill(x,y,color='#dad9d0');
 else:ax.plot(x,y,color='#bdb9ac',linewidth=.5)
for e in j['elements']:
 if e['type']=='relation':
  for m in e['members']:
   if 'geometry'in m:
    x,y=xy(m['geometry']);ax.plot(x,y,color='red')
 else:
  x,y=xy(e['geometry']);ax.fill(x,y,alpha=.4);ax.text(sum(x)/len(x),sum(y)/len(y),str(e['id'])[-4:],fontsize=9)
ax.set_aspect('equal');ax.set_xlim(-160,160);ax.set_ylim(-190,170);ax.grid();fig.savefig('work/references/footprint.png')
