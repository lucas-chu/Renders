# Château Frontenac — beauty revision

Deliver a revised 30-second, 24 fps film with O Canada and a 4K viewing copy, plus editable Blender source. Preserve the original film as a separate version.

The visual story moves from a close terrace approach to the château roofline, then spends twelve seconds inside a photo-guided reconstruction of Bar 1608, and ends on the château. Camera movement is slow and deliberate. Favor the building over empty distance.

Bar 1608 references: official Fairmont photographs 5764-24, 5764-25, and 6024-49 at https://www.chateau-frontenac.com/dine/bar-1608/. Reproduce the circular bar, contrasting stone counters, bronze ribbed base, burgundy leather stools, central marble column, glass cylinder pendants, radial mirrored ceiling, shelves, books, and river windows. Dimensions and concealed construction are estimates.

Use Cycles with Metal GPU acceleration, reflective and transmissive materials, physically scaled surface variation, and bounced interior lighting. Replace the original camera-distance emission haze with a genuine heterogeneous volume confined to the river air. Use a photographed cloudy HDR sky, not an opaque gray background. Add small exterior metalwork and garden details visible in the closer shots.

System organization: keep exterior and interior in separate named scenes within one source file; named shot cameras and timeline markers define each cut; immutable input film and original frames are retained. A single render manifest records frame ranges, scene, camera, sampling, and output paths. Numbered frames support clean restart. Verify representative shot boundaries, an interior close-up, encoded duration and audio before delivery.
