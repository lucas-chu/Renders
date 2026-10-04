# AMPHITHEATRVM — Rome, circa AD 160

A 30-second architectural film, built and rendered in Blender. An intact Colosseum amid its Roman precinct, warm Mediterranean afternoon light, an uninterrupted camera journey from city scale to architectural detail and the arena. No titles over the film.

## Spatial and historical contract

Meters. Origin at the amphitheatre center; X follows its long axis, Y the short axis, Z vertical. Outer envelope 189 x 156 m, height about 48.5 m, 80 bays in each of three arcaded orders, attic above. Arena approximately 87 x 55 m. Tuscan/Doric, Ionic and Corinthian engaged columns rise in that sequence; pilasters articulate the attic. 240 timber awning masts. White travertine, marble interiors, bronze fittings, warm lime plaster, terracotta roofing. Reconstructions and historic plans guide missing elements; modern ruin photographs guide surviving proportions and stone detailing, not damage.

The surrounding composition includes the Temple of Venus and Roma west of the amphitheatre (completed AD 141), relocated Colossus of Sol, Meta Sudans, Ludus Magnus to the east, the Palatine's imperial architecture and terraced gardens, and northern bath precincts. The Arch of Constantine and Basilica of Maxentius are excluded because they postdate this scene. Their absence is deliberate historical consistency. Relative locations follow the archaeological precinct, while distant streets/buildings, roof details, ceremonial hangings, exact statue identities and activity are artistic reconstructions. Velarium structure is a plausible hypothesis, not a settled archaeological fact.

## One connected construction system

The scene hierarchy is Site > Precincts > Buildings > Architectural orders > Bay modules > Components > Materials. Shared dimensions define both facade and interior rings. Shared mesh builders construct stone blocks, arch voussoirs, columns, moldings and roofs; instancing and material-group batches limit render overhead. Named collections expose architecture, seating, rigging, regalia, public life, city, landscape, lighting, camera. Random variation is seeded. External photographic textures are packed into the delivered blend.

The central scene generator is reproducible. A shot manifest defines the camera path and timing. Render state uses numbered frames with atomic progress and resume support, so interruptions do not invalidate earlier work. Evidence, approximations and render settings are documented together rather than scattered into implicit assumptions.

## Visual sequence

0–9 seconds: broad approach with amphitheatre dominant, temple and Roman urban fabric establishing place.
9–19 seconds: descent and lateral glide beside the south facade, revealing layered arcades, statues, column capitals, stone courses and crimson ceremonial textiles.
19–30 seconds: rising arc over the rim, linen sails and ropes passing below, the marble seating bowl and sandy arena opening into view.

The camera uses a smooth spline with continuous position and sightline; no teleportation or passage through masonry. Restrained perspective. Warm sun balanced with cooler sky light. Material-scale variation, soft shadow, atmospheric depth and gentle cloth motion support naturalism. People establish scale; avoid placing simplified background figures in hero close-ups.

## Evidence

- Parco archeologico del Colosseo, Temple of Venus and Roma: https://colosseo.it/en/marvels/temple-of-venus-and-roma/ (dates, location, scale and materials).
- Universite de Caen, Plan de Rome, Velum du Colisee: https://rome.unicaen.fr/machine/velumcolisee/ (archaeological support traces, mechanics, colored light and acknowledged reconstruction hypotheses).
- Smarthistory, Colosseum: https://smarthistory.org/colosseum/ (orders, arcades, entrance organization).
- Rome tourism authority, Meta Sudans: https://www.turismoroma.it/en/places/meta-sudans (fountain profile and dimensions).
- Architectural plans and image references: references/sources.json; reference-board.jpg. Illustrations are visual research only, not incorporated into the film.
- Material textures: Poly Haven, CC0, retrieved through its public API. Existing local sky texture is also Poly Haven CC0.
- Requested X post could not be loaded; its footage was not viewed.

## Completion gates

Inspect wide, close and interior test renders. Correct major composition/material errors before full rendering. Benchmark representative production frames. Retain 720 native frames at 24 fps. Encode a 30-second MP4, probe dimensions/duration/frame count, and inspect samples of the encoded file. Deliver the actual video, a hero still and packed editable Blender source. A running render is not a completed film.

## Sculptural treatment

The lost arcade statues use adapted public-domain Met scans of Aphrodite holding Eros (242017), Herakles (242211), and a Roman bronze boy (254613) as classical proxies, with reconstructed marble finish. These are not identified original Colosseum statues. The idealized Colossus uses an adapted anatomical proxy from Canova's Perseus (204758); this is an artistic stand-in for a lost ancient sculpture, not evidence of its exact appearance. Met object records and asset metadata are saved in references/sculpture-credits.json.

## Final production refinements

Protected level surfaces resolve the amphitheatre precinct, fountain basin and palace terrace against the wider terrain. The distant city uses a simpler mesh treatment beyond the detailed neighborhood, maintaining a continuous inhabited horizon. A physical atmosphere sky and directional sun provide the final daylight; the downloaded HDR is retained as a research asset. Corinthian capitals include modeled acanthus and volutes. The bath precinct uses vaulted thermal halls and large clerestories.

Production output: 1920 x 1080, 24 fps, 720 native rendered frames, Eevee with 32 temporal samples, ray tracing, restrained motion blur, and AgX color management. Each frame is written to a temporary path then atomically renamed. The render controller resumes completed frames and verifies the final encoded movie.

## Cinematic revision

Version two preserves the amphitheatre dimensions while replacing the uniform background with irregular neighborhoods and continuous rolling terrain. Lower sunlight, spatially varying haze, translucent linen, quieter crowd groupings and a rebuilt camera path strengthen depth and visual continuity. Fragmentary arcade figures are replaced by complete classical proxies; the Canova Perseus remains explicitly a later artistic stand-in, not a historically identified Colosseum statue. The distant topography and neighborhood plans are compositional reconstructions, not a surveyed model of ancient Rome.
