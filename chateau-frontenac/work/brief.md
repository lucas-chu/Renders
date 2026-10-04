# Château Frontenac — first light over Cap Diamant

Deliver an editable Blender scene and a 30-second, 24 fps rendered film. The map pin is 46.811891, -71.205283. This is a reference-guided reconstruction, not a survey model.

## Spatial system
Metres; origin at the supplied map pin; local X follows the long southwest–northeast wings, local Y points toward the southeast terrace. OpenStreetMap geometry supplies the hotel footprint, tower positions, street pattern, and surrounding building footprints. Photos guide heights, roofs, bay rhythm, materials, pavilions, and landscape. Heights without surveyed values remain estimates. Keep source data separate from scene parameters and generated meshes.

## Perceptual priorities
1. Recognizable silhouette and relative tower/wing proportions.
2. Continuous place: broad wooden terrace, escarpment, dense Lower Town, wide river and opposite bank.
3. Human-scale depth: recessed dark glazing, light stone reveals, courses, steep seamed copper roofs, layered dormers, cornices, railings and striped pavilions.
4. Natural light: warm low sun, cool skylight, atmospheric depth, restrained contrast.
5. Camera: deliberate continuous motion with a wide opening, an intimate terrace approach, then a rising architectural reveal. No text or artificial frame decoration.

## Scene organization
Named collections for hotel massing, architectural detail, terrace, topography, neighborhood, planting, lighting and camera. Deterministic procedural construction, shared vegetation meshes, material-batched static geometry, real-unit UVs. All delivery dependencies packed into the .blend. Camera can be re-rendered without rebuilding geometry.

## Validation
Inspect several camera positions as stills before animation rendering; revise silhouette, framing and lighting. Verify final video duration, resolution, frame rate, successful decode, and sample frames. Deliver source scene, MP4 and a preview still with a concise sources/limitations document.
