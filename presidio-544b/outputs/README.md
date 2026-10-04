# 544B Presidio Boulevard

A Blender architectural film of the building containing 544B and its Presidio streetscape.

**Final improved version:** `Presidio_544B_Improved.blend` contains the revised editable scene. `Presidio_544B_Improved_Flythrough.mp4` is the final film. The revision aligns the curved roof tile courses, removes stray footpath surfaces crossing roads, improves glass reflections, bakes reflected daylight around the porch, and adds surface and foliage color variation. `improved_verification.json` records the final encoded video checks. The original version is retained for comparison.

**Original deliverables:** `Presidio_544B.blend` is the editable scene, with packed textures, a 720-frame camera animation, and named collections. `Presidio_544B_Flythrough.mp4` is the 30-second, 1920 × 1080, 24 fps film. `verification.json` records the finished video's actual dimensions, duration and decoded frame count.

The camera starts above the boulevard, approaches the house and its paired entrance porch, then rises outward into the neighborhood. Materials include modeled overlapping mission tiles, painted sash, reflective glazing, textured stucco, aged concrete, granular asphalt, and individually modeled foliage. The house, neighboring residences, rear garages, roads and paths share a local coordinate system in meters.

## Evidence and interpretation

The reconstruction uses the NPS architectural description, public exterior and aerial listing photographs, neighboring-house photographs, and OpenStreetMap footprints. It is an artistic reconstruction, not a measured survey. Public listing pictures may show representative neighborhood buildings; their details are interpreted alongside the documented architectural type. Exact terrain elevations, tree species and placement, unseen surfaces, and minor garden and street details are inferred. No interior of 544B is claimed to be reproduced.

- [National Park Service historic district documentation, pages 133–134](https://npgallery.nps.gov/NRHP/GetAsset/NHLS/66000232_text)
- [Presidio Trust preservation report](https://wp.presidio.gov/wp-content/uploads/2023/07/EXD-700-FY2009AnnuRpt.pdf)
- [544B public listing and photo set](https://www.realtor.com/rentals/details/544-Presidio-Blvd-B_San-Francisco_CA_94129_M92439-84392)
- [544B listing streetscape](https://www.zillow.com/homedetails/544-Presidio-Blvd-B-San-Francisco-CA-94129/457348382_zpid/)
- [540A detail reference](https://www.zillow.com/homedetails/540-Presidio-Blvd-A-San-Francisco-CA-94129/2077914101_zpid/)
- [545 detail reference](https://www.zillow.com/homedetails/545-Presidio-Blvd-San-Francisco-CA-94129/2112499901_zpid/)
- [548A detail reference](https://www.zillow.com/homedetails/548A-Presidio-Blvd-San-Francisco-CA-94129/2123404739_zpid/)
- [OpenStreetMap site geometry](https://www.openstreetmap.org/#map=18/37.797592/-122.451569), © OpenStreetMap contributors, ODbL.

Vegetation, sky and material source assets from [Poly Haven](https://polyhaven.com/license), CC0: Pine Tree 01, Tree Small 02, Shrub 01, Grass Medium 01, Kloofendal 48d Partly Cloudy Pure Sky, Leafy Grass, White Plaster Rough 01, Bark Bluegum and Brown Mud Leaves 01. Additional woodland trees, architecture and street details are generated geometry.

## Editing and rendering

The Blender scene's numbered collections separate architecture, mapped ground and streets, woodland, garden detail, street furniture, and cinematography. Frame range: 1–720. Camera and focus motion are baked per frame for predictable playback. The `READ ME` text inside Blender contains the original scene brief.

The production folder is outside synced Documents to keep frame sequences resident during rendering. All textures needed by the final Blender scene are packed into the file.
