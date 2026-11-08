# The Last Stand · Rome, 6 May 1527

A 30-second animated Blender diorama of the Swiss Guard during the Sack of Rome. A companion to the modern St. Peter’s flythrough, with its Ave Maria excerpt carried into this edition.

- **Watch:** [The Last Stand – 1527](The%20Last%20Stand%20-%201527.mp4)
- **Edit:** [Blender scene](The%20Last%20Stand.blend). Timeline camera markers switch between four shots. Collections separate the architecture, companies, standards, passage, escort, lights and cameras.
- **Rebuild:** run Blender 5.2 with `blender -b -P build.py`; render with `blender -b "The Last Stand.blend" -o "/tmp/stand_frames/f_####" -F JPEG -a`. From the film directory run `python3 finish.py /tmp/stand_frames`. The finish requires NumPy and FFmpeg and adds titles, the original contact and footstep sounds in `foley.py`, music and an upscale from 1440 × 810 to 3840 × 2160. Keep the audio beside the scripts.

| Time | Shot | Narrative |
|---|---|---|
| 0–8 s | The approach | Two companies close beneath Old St. Peter’s, with unfinished construction rising beyond. |
| 8–16 s | Hold the line | The camera enters the space between pikes and halberds as men thrust, recoil and fall. |
| 16–24 s | The Passetto | Clement VII travels under guard through the fortified passage. |
| 24–30 s | For those who stayed | A return to the contested standard, then a dedication. |

## Historical basis and interpretation

The [Vatican’s Swiss Guard history](https://www.vatican.va/content/romancuria/en/guardia-svizzera-pontificia/corpo-della-guardia-svizzera-pontificia/profilo.html) identifies the defense of Clement VII and his escape via the Passetto. The [Vatican’s anniversary homily](https://www.vatican.va/content/benedict-xvi/en/homilies/2006/documents/hf_ben-xvi_hom_20060506_swiss-guard.html) records 147 guards killed and 42 escorting the pope to Castel Sant’Angelo. The [Swiss National Museum account](https://blog.nationalmuseum.ch/en/2023/05/the-darkest-day-in-the-history-of-the-swiss-guard/) gives the larger context.

This is a dramatization in the style of painted miniatures. Figure counts are representative. Old St. Peter’s, its campanile, unfinished crossing, nearby buildings, mosaic, passage, heraldry, dress, lighting and individual fighting movements are interpretive, not a surveyed reconstruction or a literal order of battle. Neither the later dome nor Bernini’s colonnade appears.

## Music and license

Schubert: *Ave Maria*, D.839. Tomaz Kovacic, baritone; Michael Stenov, organ. Live recording, 2019, published by Michael Stenov, [IMSLP recording 577775](https://imslp.org/wiki/Ave_Maria_(Schubert,_Franz)). The previously excerpted, filtered, normalized and faded performance is synchronized to a new animation. Recording and synchronized film: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). No endorsement is implied.
