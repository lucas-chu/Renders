import xml.etree.ElementTree as ET,json,math
from PIL import Image,ImageDraw,ImageFont
root=ET.parse('work/references/map.osm').getroot();nodes={n.attrib['id']:(float(n.attrib['lon']),float(n.attrib['lat'])) for n in root.findall('node')}
lat0=37.797592;lon0=-122.451569
xy=lambda lon,lat:((lon-lon0)*111320*math.cos(math.radians(lat0)),(lat-lat0)*111320)
features=[]
for w in root.findall('way'):
 t={x.attrib['k']:x.attrib['v'] for x in w.findall('tag')}
 if any(k in t for k in ['building','highway','landuse','natural']):
  pts=[xy(*nodes[x.attrib['ref']]) for x in w.findall('nd') if x.attrib['ref'] in nodes]
  features.append({'id':w.attrib['id'],'tags':t,'xy':pts})
json.dump(features,open('work/site.json','w'),indent=2)
out=Image.new('RGB',(1600,1600),'#e5e6d9');d=ImageDraw.Draw(out)
conv=lambda p:(800+p[0]*3,800-p[1]*3)
for f in features:
 pts=[conv(p) for p in f['xy']];t=f['tags']
 if len(pts)<2:continue
 if 'building' in t:d.polygon(pts,fill='#cfaa7e',outline='#846752')
 elif 'highway' in t:d.line(pts,fill='#888c8c',width=12 if t['highway'] not in ['footway','path','steps'] else 3)
 if 'building' in t or t.get('name')=='Presidio Boulevard':
  x=sum(p[0] for p in pts)/len(pts);y=sum(p[1] for p in pts)/len(pts)
  label=t.get('addr:housenumber',t.get('ref',t.get('name',f['id'])))
  d.text((x,y),label,fill='black',font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',17))
  if abs(x-800)<350 and abs(y-800)<350:print(label,t, f['xy'][:4])
d.ellipse((793,793,807,807),fill='red');d.text((810,800),'Listing pin',fill='red')
out.save('work/references/site-map.png')
