import pathlib, urllib.request, concurrent.futures,json,re
from PIL import Image,ImageOps,ImageDraw
P=pathlib.Path(__file__).resolve().parents[1]; R=P/'references'; A=P/'assets'
refs={
'01-elevation-section':'https://antique.totalarch.com/files/gha/roma/589_2_full.jpg',
'02-plan-section':'https://wiki-ead.b-cdn.net/images/9/9a/Cortes_Coliseo_Romano.jpg',
'03-detailed-plan':'https://2.bp.blogspot.com/-i6tG8WXiW5U/UUx3hvEEG0I/AAAAAAAAAAk/mAyXQG14w6k/s1600/The%2BColosseum.jpg',
'04-facade':'https://bluprint-onemega.com/wp-content/uploads/2021/03/colosseum.jpg',
'05-facade-light':'https://images.posarellivillas.com/website_static/11/custom/asra10%3A16%3A480%3Ax/lazioregion.jpg',
'06-velarium':'https://www.rzym.it/wp-content/uploads/rzym-koloseum-velarium-1.jpg',
'07-interior':'https://www.studiarapido.it/wp-content/uploads/2014/06/interno-colosseo-600x450.jpg',
'08-reconstruction':'https://www.italyguides.it/movie/lazio/roma/before-after/colosseum-before-after-01/img/colosseum-01/Colosseum-before.jpg',
'09-interior-section':'https://novikov-architect.ru/images/rome_arch/rome_arch-23.jpg',
'10-seating-plan':'https://ebrary.net/htm/img/9/1318/9.png',
'11-colored-plan':'https://2.bp.blogspot.com/-PEA81pCM9S0/To3WwUqFl-I/AAAAAAAABN4/l4k2MEZ0huY/s1600/a41-coliseo-de-roma-planta-y-alzado.jpg',
'12-arena':'https://www.walksinsiderome.com/uploads/2024/05/colar1.png',
'13-seating':'https://www.walksinsiderome.com/uploads/2024/09/Untitled-design-1.png',
'14-velarium-drawing':'https://i0.wp.com/www.glosarioarquitectonico.com/wp-content/uploads/2016/01/velarium.jpg',
}
def fetch(u,p):
 try:
  data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read();p.write_bytes(data); return True
 except Exception as e:print(p.name,str(e),flush=True);return False
def ref(it):
 n,u=it;p=R/(n+'.jpg');fetch(u,p)
 try:im=Image.open(p);im.load();print(n,im.size,flush=True)
 except: p.unlink(missing_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(ref,refs.items()))
(R/'sources.json').write_text(json.dumps(refs,indent=2))
imgs=list(R.glob('*.jpg'));sheet=Image.new('RGB',(1800,((len(imgs)+3)//4)*340),(29,29,26));d=ImageDraw.Draw(sheet)
for i,p in enumerate(imgs):
 im=ImageOps.contain(Image.open(p).convert('RGB'),(442,306));x=(i%4)*450;y=(i//4)*340;sheet.paste(im,(x+(450-im.width)//2,y));d.text((x+8,y+311),p.stem,fill='white')
sheet.save(R/'reference-board.jpg',quality=94)
def tex(a):
 p=A/(a+'.json');fetch('https://api.polyhaven.com/files/'+a,p)
 try:
  j=json.loads(p.read_text())
  for k in ['diff','nor_gl','rough']:
   q=j.get(k,{}).get('2k',{});v=q.get('jpg',q.get('png')); 
   if v:fetch(v['url'],A/(a+'_'+k+'.'+v['url'].split('.')[-1]))
  print('TEXTURE',a,flush=True)
 except Exception as e:print(a,e,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(tex,['white_sandstone_blocks_02','marble_01','cobblestone_floor_08','clay_roof_tiles_02','sand_01']))
