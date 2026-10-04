import pathlib,json,urllib.request,concurrent.futures
P=pathlib.Path('colosseum');A=P/'assets';R=P/'references'
def get(it):
 p,u=it
 try:p.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read());print(p.name,flush=True)
 except Exception as e: print(e,flush=True)
jobs=[]
for a in ['white_sandstone_blocks_02','marble_01','cobblestone_floor_08','clay_roof_tiles_02','sand_01']:
 j=json.loads((A/(a+'.json')).read_text())
 for src,dst in [('Diffuse','diff'),('Rough','rough')]:
  q=j.get(src,{}).get('2k',{});v=q.get('jpg',q.get('png'))
  if v:jobs.append((A/(a+'_'+dst+'.'+v['url'].split('.')[-1]),v['url']))
refs={'15-temple-context':'https://s1.elespanol.com/2024/10/29/historia/897170702_250450063_1706x960.jpg','16-temple-plan':'https://www.cointalk.com/attachments/temple-of-venus-and-roma-floorplan-jpg.727696/','17-temple-academic':'https://books.openedition.org/puc/file/39854/tei/RA_04_fig_08.jpg/download','18-ludus':'https://colosseumrometickets.com/wp-content/uploads/2018/07/Reconstruction-Sketch-of-Ludus-Magnus-in-Ancient-Rome-2.jpg','19-palatine':'https://3.bp.blogspot.com/-pXTqmN4-zf0/W3P_OXtswLI/AAAAAAAAzRA/ieucaJBVTFEwuIM2bqOsmSSZKS5Vk6B4gCLcBGAs/s1600/palacio%2BDomiciano.jpg','20-palatine-context':'https://www.apriana.nl/afbeeldingen/Situs/Rome/Palatijn28.JPG'}
for n,u in refs.items():jobs.append((R/(n+'.jpg'),u))
old=json.loads((R/'sources.json').read_text());old.update(refs);(R/'sources.json').write_text(json.dumps(old,indent=2))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,jobs))
from PIL import Image,ImageOps,ImageDraw
imgs=sorted(R.glob('[0-9]*.jpg'));s=Image.new('RGB',(1800,((len(imgs)+3)//4)*340),(29,29,26));d=ImageDraw.Draw(s)
for i,p in enumerate(imgs):
 try:
  im=ImageOps.contain(Image.open(p).convert('RGB'),(442,306));x=i%4*450;y=i//4*340;s.paste(im,(x+(450-im.width)//2,y));d.text((x+8,y+311),p.stem,fill='white')
 except:pass
s.save(R/'reference-board.jpg',quality=94)
