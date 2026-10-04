# Colosseum — cinematic revision

Status: completed. The revised MP4 contains 720 native frames, exactly 30 seconds at 1920 × 1080 and 24 fps. The full video decodes without errors; representative encoded frames and the closing frame have been inspected. Deliverables and verification details are listed in `README.md`.

The first film remains in the parent `output/` folder. This version addresses its most visible weaknesses: uniform background blocks, flat atmospheric depth, coarse vegetation, fragmentary close-up statues and an opening camera move whose changing lens weakened the approach.

## Changes

- Preserve the amphitheatre's dimensions, bay system, cavea, masts and mapped precinct.
- Replace the regular city grid with irregular neighborhoods, varied building heights, adjoining wings, balconies and porticoes.
- Build continuous terrain and distance-dependent haze so the city recedes into the landscape.
- Replace polygonal canopy masses with instanced Mediterranean trees made from branches and modeled foliage.
- Replace fragmentary arcade sculptures with complete classical stand-ins. The retained Roman youth and the later Perseus proxy are interpretive ornament, not identified original Colosseum statues.
- Gather pedestrians into small groups and use quieter poses.
- Lower the sun, warm the direct light, reduce fill light and allow linen to transmit light.
- Rebuild the continuous 30-second camera movement around a steady approach, façade detail and a rising arena reveal.

## Production

Start from the first delivered Blender scene. Run `scripts/cinematic_revision.py`, then `scripts/vegetation.py`. The revision is saved to this version's `output/Colosseum_AD160.blend`; source assets and research link to the parent project. The Blender file packs its image assets.

Compare wide, close and interior renders before launching the film. Keep the native frames in this version's `frames/` directory so the original film remains intact. Deliver only after the revised MP4 passes duration, frame-count, full decode and visual checks.

The final production choice is Cycles with Metal acceleration, 24 samples and denoising at native 1920 × 1080. Additional stages after vegetation are `light_polish.py` and `distant_detail.py`. The latter extends distant façade detail while replacing roof tile rods that were smaller than a pixel with simpler roof surfaces. Broad heterogeneous haze uses larger integration steps; native rendered frames are inspected to ensure the visible atmospheric treatment remains coherent.

Start or resume the film with `COLOSSEUM_ENGINE=CYCLES COLOSSEUM_SAMPLES=24 python3 scripts/finish_render.py`. Progress is in `finish.log` and `animation.log`. The controller validates 720 native frames before encoding a 30-second H.264 movie.
