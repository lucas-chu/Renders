import bpy,time
s=bpy.context.scene
s.render.engine='CYCLES'
print('ENGINE SETTINGS',[(p.identifier,p.type) for p in s.eevee.bl_rna.properties],flush=True)
s.render.engine='BLENDER_EEVEE';s.render.resolution_percentage=50
s.world.node_tree.nodes.get('Sky Texture').sun_disc=False
s.frame_set(120);s.render.filepath='/Users/lucaschu/Documents/Codex/2026-09-04/make/work/eevee_preview.png'
t=time.time();bpy.ops.render.render(write_still=True);print('RENDER SECONDS',time.time()-t,flush=True)
