import bpy,os,json,math
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));s=bpy.context.scene
# Background aerial perspective using distance, without volume marching.
for m in bpy.data.materials:
 if not m.use_nodes:continue
 if m.name.startswith('Neighborhood') or m.name in ['Earth and escarpment','Blue grey standing seam','Burgundy sheet metal','Weathered zinc']:
  n=m.node_tree.nodes;l=m.node_tree.links;out=next((a for a in n if a.type=='OUTPUT_MATERIAL'),None)
  if not out or not out.inputs['Surface'].links:continue
  old=out.inputs['Surface'].links[0].from_socket;cam=n.new('ShaderNodeCameraData');ma=n.new('ShaderNodeMapRange');ma.inputs['From Min'].default_value=260;ma.inputs['From Max'].default_value=1100;ma.inputs['To Max'].default_value=.9;l.new(cam.outputs['View Distance'],ma.inputs['Value']);em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(.51,.53,.55,1);em.inputs[1].default_value=.7;mix=n.new('ShaderNodeMixShader');l.new(ma.outputs[0],mix.inputs[0]);l.new(old,mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface'])
# Model supports for mapped waterfront buildings so nothing floats over the river.
vs=[];fs=[]
def cube(x,y,z,w,d,h):
 o=len(vs)
 for xx,yy,zz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:vs.append((x+xx*w/2,y+yy*d/2,z+zz*h/2))
 fs.extend([tuple(o+i for i in f) for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]])
for e in json.load(open(os.path.join(R,'work/references/osm.json')))['elements']:
 if not e.get('tags',{}).get('building') or not e.get('geometry'):continue
 pts=[]
 for v in e['geometry']:
  east=(v['lon']+71.205283)*76130;north=(v['lat']-46.811891)*111195;pts.append((east*.88+north*.475,east*.475-north*.88))
 x=sum(p[0] for p in pts)/len(pts);y=sum(p[1] for p in pts)/len(pts);edge=88 if x<100 else 62-(x-100);dist=max(y-edge,x-115)
 if dist<42:continue
 x0=min(p[0] for p in pts)-2;x1=max(p[0] for p in pts)+2;y0=min(p[1] for p in pts)-2;y1=max(p[1] for p in pts)+2
 cube((x0+x1)/2,(y0+y1)/2,-49.2,x1-x0,y1-y0,6.8)
 # Small quay connector back to the coastal strip where required.
 shore=175-.35*max(0,x-100)
 if y>shore-20:cube(x,(y+shore-18)/2,-49.4,5,abs(y-shore+18)+5,6.4)
me=bpy.data.meshes.new('Waterfront foundations');me.from_pydata(vs,[],fs);me.materials.append(bpy.data.materials['Pale grey limestone']);me.update();ob=bpy.data.objects.new('Waterfront quays and foundations',me);bpy.data.collections['04 Old Quebec | mapped context'].objects.link(ob)
# Quiet early morning: retain the detailed public realm without close mannequin figures.
bpy.data.objects['Visitors on the promenade'].hide_render=True
s.camera.data.dof.use_dof=True;s.camera.data.dof.focus_distance=145;s.camera.data.dof.aperture_fstop=5.6
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.eevee.use_fast_gi=True;s.eevee.fast_gi_quality=.5;s.eevee.use_raytracing=False
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=720;s.frame_set(350)
s['Film renderer']='Eevee, 32 temporal samples, full HD. Cycles materials and lighting retained.'
s['Shot list']='1–240 terrace travel; 241–504 architectural sweep; 505–720 river reveal.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(R,'outputs','Chateau_Frontenac.blend'))
