import json
from shapely.geometry import Polygon
from shapely.ops import triangulate
j=json.load(open('work/references/vatican_relations.json'));out=[]
for e in j['elements']:
 outer=[];inner=[]
 for m in e.get('members',[]):
  g=m.get('geometry',[])
  if len(g)<4:continue
  p=[((q['lat']-41.902165)*111195,(q['lon']-12.455025)*82770) for q in g]
  (inner if m['role']=='inner' else outer).append(p)
 for op in outer:
  shell=Polygon(op)
  holes=[ip for ip in inner if shell.covers(Polygon(ip).representative_point())]
  poly=Polygon(op,holes).buffer(0)
  if poly.is_empty:continue
  tris=[list(t.exterior.coords)[:-1] for t in triangulate(poly) if poly.covers(t.representative_point())]
  out.append({'id':e['id'],'tags':e.get('tags',{}),'loops':[op]+holes,'triangles':tris})
json.dump(out,open('work/references/relations_mesh.json','w'))
print(len(out))
