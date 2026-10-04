# Saint Peter’s Basilica — light and stability revision

A 30-second architectural film with an exterior approach, a new nave interior and a rising view beneath the dome. Created in Blender using a reference-based geometric reconstruction. Sculptures, mosaics outside the dome, and several architectural details are simplified interpretations rather than survey-accurate reproductions.

## Changes

- New three-dimensional nave and crossing with arches, pendentives, a coffered barrel vault and a sixteen-part dome drum.
- Inlaid marble pavement, fluted pilasters, ornamental panels, bronze spiral Baldachin columns, gilded canopy, papal altar, candles and a simplified Cathedra glory window.
- Layered stone, bronze, gold, glass, water and paving materials; ray-traced light and reflections.
- Film: every new frame uses Blender Cycles path tracing on Apple Metal, including diffuse indirect illumination, reflections and shadowing. Fixed sample seeds, 64 maximum samples, at least 32 adaptive samples, OpenImageDenoise, indirect firefly clamping and a 0.35-frame shutter are used to reduce flickering. The Mac uses Apple Metal hardware ray tracing, not NVIDIA RTX.
- Interior: photograph-based marble materials with subtle mineral detail, separate carved-stone shaders, restrained gold and bronze roughness, fully shadowed window lighting and warm clerestory illumination. Clear air preserves architectural contrast.
- Closed the missing transept ceilings and added vaulted side roofs, gilded ribs and enclosing walls.
- Exterior: photographed partly cloudy sky; revised camera framing; depth-limited haze affects distant geometry while preserving the sky.
- Ave Maria retained from the preceding version, including its gentle fades.

## Architectural references

- Fabbrica di San Pietro, Basilica and points of interest: https://www.basilicasanpietro.va/en/san-pietro
- The Cathedra of Saint Peter: https://www.basilicasanpietro.va/en/san-pietro/the-cathedra-of-saint-peter
- The Baldachin: https://www.basilicasanpietro.va/en/faq/who-designed-the-baldachin-inside-st-peters-basilica
- Vatican virtual tour: https://www.vatican.va/various/basiliche/san_pietro/vr_tour/index-en.html
- Reference-only nave photograph: https://www.througheternity.com/vatican/private-sistine-chapel-tour

## Dome artwork texture

“Dome of Saint Peter’s Basilica (Interior).jpg” by Livioandronico2013 (2017), Wikimedia Commons, CC BY-SA 4.0.

Source: https://commons.wikimedia.org/wiki/File:Dome_of_Saint_Peter%27s_Basilica_(Interior).jpg

License: https://creativecommons.org/licenses/by-sa/4.0/

Changes: UV projection onto a newly modeled curved dome, with new lighting and modeled ribs. The photograph is packed into the Blender file. This is photographic surface detail on a three-dimensional shell; it is not a three-dimensional reconstruction of every mosaic tessera.

## Music

Ave Maria, D.839, Franz Schubert (public-domain composition). Tomaz Kovacic, baritone; Michael Stenov, organ. Live Latin performance, 2019. Published by Michael Stenov, IMSLP recording 577775.

Source: https://imslp.org/wiki/Ave_Maria_(Schubert,_Franz)

Recording license: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/

Changes: excerpt at approximately 00:34.5–01:04.5, rumble reduction, loudness normalization, fades and synchronization.

The resulting audiovisual adaptation is distributed under CC BY-SA 4.0. No endorsement by photographers, performers, or the Basilica is implied.

Exterior map-derived geometry: © OpenStreetMap contributors, https://www.openstreetmap.org/copyright. Original scene notes remain beside the original scene file.

## Delivery format

The film is rendered at 1920 × 1080, 24 fps, then upscaled to 3840 × 2160 with mild temporal noise cleanup and Lanczos resampling; additional sharpening is omitted to avoid edge shimmer. All 720 frames are individually rendered; no AI-generated camera motion or optical-flow interpolation is used.

## New CC0 materials

- Kloofendal 48d Partly Cloudy (Pure Sky), Greg Zaal and Jarod Guest, Poly Haven, CC0: https://polyhaven.com/a/kloofendal_48d_partly_cloudy_puresky
- Marble 01, Rob Tuytel, Poly Haven, CC0: https://polyhaven.com/a/marble_01

The sky is rotated and exposure-adjusted. Marble photographs are mapped to the modeled surfaces and tinted to suit the stone palette. Source textures are packed in the editable Blender project.
