# Colosseum — completed cinematic revision

An artistic reconstruction of the Colosseum and its Roman precinct around AD 160, delivered as an editable Blender scene and a continuous 30-second film.

- [Finished film](output/Colosseum_30s_Flythrough.mp4): H.264, 1920 × 1080, 24 fps, exactly 30 seconds; approximately 64 MB. Silent architectural film.
- [Editable Blender scene](output/Colosseum_AD160.blend): packed materials, named architectural collections and the animated camera.
- [Opening still](output/Colosseum_Hero.png).
- [Revision details and rebuild instructions](REVISION.md).
- [Research and reconstruction boundaries](SCENE_PLAN.md).

The revision adds physically traced lighting, stronger shadows within the arcades, complete classical sculpture proxies, irregular neighborhoods with more façade detail, modeled vegetation, small pedestrian groups, atmospheric depth and a rebuilt camera approach. The earlier film is preserved in the parent project.

Lost decoration, statue identities, awning details, distant terrain and neighborhood plans remain artistic interpretations. The complete Perseus sculpture is a later classical stand-in, not an identified original Colosseum statue. Source credits are retained with the project.

## Verification

All 720 native frames passed image decoding and dimension checks before encoding. The finished MP4 reports 1920 × 1080, 24 fps, 720 decoded frames and 30.000000 seconds. A complete video decode returned no errors. Encoded samples at 0, 5, 10, 15, 20 and 25 seconds, plus the closing frame, were visually inspected. See `output/verification.json`, `previews/encoded_review.png` and `previews/encoded_final.png`.
