# Colosseum — Rome circa AD 160

An editable Blender reconstruction and a continuous 30-second architectural film.

The completed cinematic revision is in [v2/README.md](v2/README.md): [revised film](v2/output/Colosseum_30s_Flythrough.mp4) and [revised Blender scene](v2/output/Colosseum_AD160.blend). The first version remains available below.

The scene includes the intact amphitheatre, its three arcaded orders and attic, sculptural decoration, marble seating, spectators, linen velarium, 240 masts and their rigging, ceremonial hangings, the Meta Sudans fountain, Colossus, Temple of Venus and Roma, Ludus Magnus, bath precinct, Palatine terraces and surrounding urban fabric.

## First version files

- `output/Colosseum_AD160.blend`: packed editable scene, camera animation, materials, named collections and embedded research notes.
- `output/Colosseum_30s_Flythrough.mp4`: completed and verified 30-second H.264 movie, 1920 × 1080 at 24 fps (720 frames), approximately 44 MB. Silent architectural film.
- `output/Colosseum_Hero.png`: full-resolution opening still.
- `SCENE_PLAN.md`: evidence, design decisions, uncertainties and production settings.
- `previews/scene-map.png`: mapped precinct and camera route.
- `references/reference-board.jpg`: architectural study board; source links are in `references/sources.json`.

## Reconstruction boundaries

The Colosseum's envelope, arcade count, architectural orders and seating arrangement follow architectural references. Lost decoration, ceremonial colors, the canopy's precise arrangement, secondary buildings and street activity are artistic interpretations. Museum sculpture scans supply detailed classical proxies; they do not identify the actual lost arcade statues. The Colossus is an idealized adaptation using a later classical sculpture as an anatomical reference. These choices are recorded in the scene plan and embedded Blender text.

Textures are from Poly Haven (CC0). Sculpture references and scans are supplied through The Metropolitan Museum of Art's public-domain collection; their records and source URLs are saved in `references/sculpture-credits.json`.

## Scene organization

Numbered collections follow the physical hierarchy: foundations; facade orders; attic; circulation; sculpture; cavea; regalia; rigging; velarium; people; paving; individual precincts; landscape; distant city. Geometry uses meters with the Colosseum at the origin. X is the long axis, Y the short axis, Z vertical. The animated camera and timeline markers expose the four phases of the flight. The embedded “READ ME — scene and evidence” text travels with the Blender file.

## Rebuild and render

Run the Blender Python stages in this order, loading the saved scene for every stage after the first:

1. `scripts/build_scene.py`
2. `scripts/refine_scene.py`
3. `scripts/enhance_visuals.py`
4. `scripts/final_polish.py`
5. `scripts/lock_picture.py`
6. `scripts/fix_precinct.py`

`scripts/geometry.py` supplies the shared component builders. `shot_manifest.json` records camera controls; `camera_validation.json` records the clearance check.

Run `python3 scripts/finish_render.py` from any directory to render and encode. The controller resumes completed native frames, restarts a stalled renderer, validates all PNGs, encodes the movie and writes `output/verification.json`. Its progress is in `finish.log` and `animation.log`. Frames are written atomically into `frames/`, preserving completed work across interruptions.

Production settings: 1920 × 1080, 24 fps, 720 native frames, Eevee, 32 temporal samples, ray tracing, restrained motion blur and AgX color management. Inspect the encoded movie as the final visual check.

## Delivery verification

All 720 native PNGs passed full image decoding and dimension checks. The final MP4 reports exactly 30.000 seconds, 1920 × 1080, 24 fps and 720 decoded frames; a complete video decode returned no errors. Encoded samples at 0, 5, 10, 15, 20 and 25 seconds, plus the closing frame, were visually inspected. The review images are `previews/encoded_review.png` and `previews/encoded_final.png`; technical metadata is in `output/verification.json`.
