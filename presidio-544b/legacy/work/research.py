import urllib.request,urllib.parse,re,json,concurrent.futures
from pathlib import Path
p=Path('work/references')
def fetch(item):
 n,u=item
 try:
  data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'PresidioVisualization/1.0 research'}),timeout=40).read();(p/n).write_bytes(data);print(n,len(data))
 except Exception as e: print(n,e)
s=(p/'realtor.html').read_text()
urls=list(dict.fromkeys(re.findall(r'https://ap.rdcpix.com/[^"<>\s]+s.jpg',s)))
jobs=[('listing-%02d.jpg'%i,u.replace('s.jpg','rd-w1280_h960.jpg')) for i,u in enumerate(urls)]
jobs += [('map.osm','https://www.openstreetmap.org/api/0.6/map?bbox=-122.455,37.795,-122.449,37.800'),('satellite.jpg','https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox=-122.454,37.796,-122.450,37.799&bboxSR=4326&size=1600,1500&imageSR=3857&format=jpg&f=image'),('presidio-2009.pdf','https://wp.presidio.gov/wp-content/uploads/2023/07/EXD-700-FY2009AnnuRpt.pdf')]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(fetch,jobs))
