# Château Frontenac — scene notes

Location: the supplied map pin, 46.811891, -71.205283, in Québec City.

The Blender scene is an original procedural reconstruction. Hotel footprint and tower locations were mapped from OpenStreetMap; exterior photographs guided the silhouette, façade treatments, copper roofs, dormers, terrace pavilions and landscape. It is not a photogrammetric scan or a measured conservation model. Building heights, individual façade bays, vegetation, background roof forms, monument sculpture and small furnishings are approximations.

## Reference sources

- [Fairmont official gallery](https://www.chateau-frontenac.com/en/gallery/) — exterior, courtyard and setting photographs.
- [OpenStreetMap](https://www.openstreetmap.org/#map=18/46.811891/-71.205283) — hotel and surrounding street/building geometry; © OpenStreetMap contributors, ODbL.
- [User's visual reference](https://x.com/sharifshameem/status/2095653641164329143?s=20) — direct access was unavailable; the requested reference-led Blender workflow was followed.

Additional image references inspected:

- [official dawn](https://www.chateau-frontenac.com/content/uploads/2022/05/6024-43.jpg)
- [official exterior](https://www.chateau-frontenac.com/content/uploads/2022/05/6024-45.jpg)
- [official terrace](https://www.chateau-frontenac.com/content/uploads/2022/05/5764-13.jpg)
- [official river](https://www.chateau-frontenac.com/content/uploads/2022/05/5764-06.jpg)
- [roof detail](https://upload.wikimedia.org/wikipedia/commons/5/55/Ch%C3%A2teau_Frontenac2010_crop_roofs.jpg)
- [facade south](https://upload.wikimedia.org/wikipedia/commons/b/be/Chateau_Frontenac_25.JPG)
- [dormers](https://for91days.com/photos/Montreal/Chateau%20Frontenac%20Quebec%20City/07-for91days.com.JPG)
- [promenade](https://www.ncl.com/sites/default/files/QUE_04_ChateauFrontenac_1920x1008_0.jpg)
- [gazebo](https://dynamic-media-cdn.tripadvisor.com/media/photo-o/08/c0/84/83/terrasse-dufferin.jpg?h=1200&s=1&w=1200)
- [summer](https://carrotsandtigers.com/wp-content/uploads/2019/07/chateau-frontenac-01.jpg)
- [city aerial](https://canadiantravelhacking.com/wp-content/uploads/2019/08/frontenac-2257154_1280.jpg)
- [brick detail](https://www.pictorem.com/uploads/collection/T/TQ10SDE1OAI/900_Darryl-Brooks_Brick_Facade_and_Dormers.jpg)

Reference photographs were used for study, not pasted into the film. Scene surfaces use procedural materials.

## Lighting and film

The sky lighting uses [Qwantani Dawn (Pure Sky), Poly Haven](https://polyhaven.com/a/qwantani_dawn_puresky), a CC0 photographic HDR environment, packed into the Blender file. The film has three travelling shots: along the terrace, an architectural sweep, and an aerial river reveal.

## Deliverables

- `Chateau_Frontenac_Flythrough.mp4`: 30 seconds, 24 fps, 1920 × 1080, three travelling shots, silent.
- `Chateau_Frontenac.blend`: editable scene with packed sky texture, named collections, procedural materials, and animated camera. The animation uses Eevee with 32 temporal samples; Cycles can also render the scene.

This is an architectural visualization with simplified people, sculpture, small details and distant context, rather than a photographic reproduction. The quiet dawn film omits the simplified close-up visitor figures.

## Export verification

Verified 720 decoded frames, 1920 × 1080, 24 fps, exactly 30.000 seconds. Full-file decoding completed without errors. Sampled the opening, architectural sweep, and river reveal. The finished visual remains a stylized architectural reconstruction and does not achieve photographic realism.

## 4K edition with O Canada

`Chateau_Frontenac_4K_O_Canada.mp4` is a 3840 × 2160 upscale of the 1080p film, using Lanczos scaling and mild sharpening. Duration and frame rate remain 30 seconds and 24 fps. This is an upscale, not a new native-4K Blender render.

Soundtrack: “O Canada,” instrumental performance by the Toronto Symphony Orchestra, conducted by Peter Oundjian. Courtesy of the Toronto Symphony Orchestra, via [Canadian Heritage](https://www.canada.ca/en/canadian-heritage/services/anthem-canada.html). Source recording passage 01:03.5–01:33.5; normalized and faded to fit the film. Canadian Heritage makes this recording available for official, ceremonial and non-commercial use. Artist credits are also embedded in the MP4 metadata.
