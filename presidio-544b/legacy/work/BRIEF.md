# 544B Presidio Boulevard — A quiet morning

Deliver a 30-second, 24 fps Blender film and an editable packed .blend. The scene is an architectural reconstruction, anchored by photographs and public map footprints; it is not a survey or photogrammetric capture.

## Coherent scene model

All site data uses meters in a local east/north/up coordinate system centered on the public listing coordinate 37.797592, -122.451569. OpenStreetMap footprints determine building location and rotation. Building geometry is generated in reusable local coordinates, then placed through one transform. The same terrain function places roads, walks, vegetation and foundations. Named collections separate architecture, ground, vegetation, street details, light and camera. Materials and asset prototypes are shared; distant repeated vegetation uses mesh instances. Random detail uses a fixed seed for reproducibility.

## Evidence hierarchy

1. NPS National Register documentation, pages 133–134: buildings 540–542, 544, 546, 548, 550–551 are 1917 two-story duplexes over basements, approximately 46 by 57 feet including projections, with mission-tile hip roofs, end chimneys, rear chimney, three-pier double entrance porticos and six-over-six sash.
2. Current 544B public listing: streetscape, aerial, floor plan and four interior photographs. Use exterior/aerial for materials, gardens, paths, facade vocabulary, relative environment.
3. OSM downloaded site geometry: specific footprint of 544, street and service-road curvature, neighbors, garages.
4. Neighbor photographs at 540, 545, 548: window construction, sills, steps, brackets, garden planting.
5. Presidio Trust 2009 preservation report: neighborhood context.

The promotional pres.house page conflicts with NPS and is excluded from geometry/history evidence. The requested X example did not open directly; text from a public indexed mirror confirms the architectural-film reference, but the clip itself was not viewed.

## Film

One continuous, smoothly eased camera move: elevated approach across the woodland street; descend to the front garden; intimate three-quarter view of the porch, windows and tile roof; slow rising departure showing 544 in its neighborhood. Use a natural perspective, restrained depth of field, no titles or interface overlays. 1920 x 1080, 720 native rendered frames. Select render engine and sample count after a representative benchmark. Save numbered frames to allow resumption.

## Detail priorities

Silhouette and terrain before ornament. Individually modeled curved clay tiles with restrained variation; deep dark wood sash and reflective glazing; white stucco with fine roughness; porch capitals, doubled brackets, stairs, parapets, basement grilles and downpipes. Lawns, rough understory, mature irregular trees, hedges, street markings, joints, curbs, lampposts and the service lane establish place. Ecologically similar stock vegetation supplements custom conifers; botanical species and exact tree positions remain approximations. Unseen rear elevations and landscape microdetails are inferred.

## Verification gates

Inspect wide, middle and close camera frames. Check spatial intersections and foliage occlusion. Time production settings before 720-frame render. Reuse completed PNGs. Verify encoded duration, resolution and frame count, then inspect frames sampled from the MP4. Never equate a saved .blend or active render with completed video delivery.
