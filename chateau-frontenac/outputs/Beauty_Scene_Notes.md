# Château Frontenac — beauty revision

This revision adds a photo-guided Bar 1608 interior, two interior camera shots, closer exterior views, a photographic cloudy sky, more detailed surface shaders, and actual volumetric river mist. The earlier film remains available separately.

## Film edit

| Time | Shot |
| --- | --- |
| 0–8 seconds | Close terrace approach |
| 8–15 seconds | Château and copper roofline |
| 15–23 seconds | Slow entrance into Bar 1608 |
| 23–27 seconds | Onyx counter, crystal, and brass close-up |
| 27–30 seconds | Closing château portrait |

## Rendering and materials

Cycles path tracing uses the Apple M4 Pro GPU through Metal. This provides ray-traced reflections, glass transmission, indirect light, and volume scattering. It does not use NVIDIA RTX hardware. The film is rendered at 1920 × 1080 with 16 adaptive samples and denoising. Camera positions are rendered at 12 fps and motion-interpolated separately within each shot to produce smooth 24 fps playback. The 4K viewing copy is upscaled to 3840 × 2160. The Blender camera animation retains every frame at 24 fps for further rendering.

The exterior's camera-distance emission haze has been disconnected. A heterogeneous density volume over the river provides light scattering; its density fades vertically and varies spatially. There is no gray distance overlay on the buildings. The photographed sky is Kloofendal 48d Partly Cloudy Pure Sky, from Poly Haven, licensed CC0.

The historic brick color and mortar relief are baked into packed texture maps to keep the material stable across GPU renders. Copper, glass, stone, leather, wood, and metal retain their physical surface shading.

The interior contains an annular stone counter, fluted brass base, marble column, leather stools, paneled walls, tall glass windows, bookcases, books, individual glass cylinder pendants, curved shelves, bottles, glasses, cocktail tools, ice, fruit, and wood planks. The warm practical lighting and window light are part of the modeled scene.

## Accuracy and sources

The château and terrace retain the previous reference-guided reconstruction using OpenStreetMap footprints and photographs. Bar 1608 is reconstructed from the official hotel's photographs, not from measured interior plans. Dimensions, concealed construction, small objects, the window vista, and distant city context are approximations. This is an architectural visualization, not a survey or photographic record.

- [Official Bar 1608 page](https://www.chateau-frontenac.com/dine/bar-1608/)
- [Main room reference](https://www.chateau-frontenac.com/content/uploads/2022/05/5764-24.jpg)
- [Side detail reference](https://www.chateau-frontenac.com/content/uploads/2022/05/5764-25.jpg)
- [Additional official reference](https://www.chateau-frontenac.com/content/uploads/2022/05/6024-49.jpg)
- [Official château gallery](https://www.chateau-frontenac.com/en/gallery/)
- [Poly Haven sky](https://polyhaven.com/a/kloofendal_48d_partly_cloudy_puresky)

## Music

“O Canada,” instrumental performance by the Toronto Symphony Orchestra, conducted by Peter Oundjian. Source: [Canadian Heritage](https://www.canada.ca/en/canadian-heritage/services/anthem-canada.html). The film uses a 30-second excerpt, with level adjustment and fades. The official source offers the recording for official, ceremonial, and non-commercial use; credit the orchestra and artists when sharing.

## Editable scene organization

`Exterior | Château and Dufferin` contains the researched exterior, added detail, sky and fog. `Interior | Bar 1608` contains the furnished room and its window vista. Numbered camera names match the edit above. Shot boundaries are marked on each scene's timeline. Materials and collections are named by their visible purpose.

The shot manifest and resumable rendering workflow are stored under `work/beauty/`. Each frame is written atomically; completed frames can be reused after interruption. Original images, film, soundtrack, and scene remain separate from the revision.

`Film | 30-second edit` is the master Blender sequence with all five scene strips and the soundtrack. Select it to render the entire edit directly. The soundtrack, sky, and brick textures are packed into the Blender file; a separate WAV is also supplied.

Rendering runs in short batches to limit GPU memory growth. Encoded shots are verified before their source frames are archived. Exterior source frames also pass a brick-color check that detects the GPU shader failure seen during development.
