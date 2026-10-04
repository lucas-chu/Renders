import urllib.request,concurrent.futures,json,pathlib
urls={
'official-dawn':'https://www.chateau-frontenac.com/content/uploads/2022/05/6024-43.jpg',
'official-exterior':'https://www.chateau-frontenac.com/content/uploads/2022/05/6024-45.jpg',
'official-terrace':'https://www.chateau-frontenac.com/content/uploads/2022/05/5764-13.jpg',
'official-river':'https://www.chateau-frontenac.com/content/uploads/2022/05/5764-06.jpg',
'roof-detail':'https://upload.wikimedia.org/wikipedia/commons/5/55/Ch%C3%A2teau_Frontenac2010_crop_roofs.jpg',
'facade-south':'https://upload.wikimedia.org/wikipedia/commons/b/be/Chateau_Frontenac_25.JPG',
'dormers':'https://for91days.com/photos/Montreal/Chateau%20Frontenac%20Quebec%20City/07-for91days.com.JPG',
'promenade':'https://www.ncl.com/sites/default/files/QUE_04_ChateauFrontenac_1920x1008_0.jpg',
'gazebo':'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/08/c0/84/83/terrasse-dufferin.jpg?h=1200&s=1&w=1200',
'summer':'https://carrotsandtigers.com/wp-content/uploads/2019/07/chateau-frontenac-01.jpg',
'park-aerial':'https://images.locationscout.net/2024/04/montmorency-park-quebec-city-canada-y5kw.jpg?q=60&w=1080',
'city-aerial':'https://canadiantravelhacking.com/wp-content/uploads/2019/08/frontenac-2257154_1280.jpg',
'brick-detail':'https://www.pictorem.com/uploads/collection/T/TQ10SDE1OAI/900_Darryl-Brooks_Brick_Facade_and_Dormers.jpg'}
p=pathlib.Path('work/references')
def get(kv):
 k,v=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(v,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();(p/(k+'.jpg')).write_bytes(b);return k,len(b)
 except Exception as e:return k,str(e)
print(list(concurrent.futures.ThreadPoolExecutor(8).map(get,urls.items())))
(p/'sources.json').write_text(json.dumps(urls,indent=2))
