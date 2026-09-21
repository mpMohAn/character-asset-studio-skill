# Asset Specification

Use this reference when defining, extracting, approving, or versioning reusable character and equipment masters.

## Character identity pack

Record the approved:

- front and useful three-quarter/side views;
- body proportions and height-to-width ratio;
- head/body relationship;
- face construction, eye geometry, mouth and tooth rules;
- horns, ears, hair, hands, feet, tail, belt, rings, shoes, markings, and other permanent details;
- source-derived palette with sampled sRGB values, coverage, tolerances, and locked/optional roles;
- outline, shading, material, and rendering style;
- expression map with stable names and ordering;
- attachment landmarks for head, eyes, ears, neck, hands, waist, feet, back, and vehicle seat.

Do not infer a tooth, garment, ornament, or facial detail that is absent from the selected expression reference.

Extract the palette from the approved source before producing variants. Separate foreground colors from background colors; do not allow an old background color to become part of the character palette after extraction. Record exact values for identity-critical colors such as eye, skin, markings, equipment symbols, and primary clothing.

## Equipment master

Each reusable item should have:

- stable asset ID and human-readable name;
- immutable original reference;
- cleaned transparent master;
- version and approval state;
- canonical dimensions and aspect ratio;
- palette, patterns, logos, materials, and distinguishing geometry;
- physical properties that affect depiction, including approximate mass class, rigidity/flexibility, grip point, balance point, wind response, and collision/contact surfaces;
- one or more angle variants when perspective changes matter;
- attachment points, scale range, z-order, and occlusion masks;
- interaction notes such as hand grip, head clearance, or horn cutouts.

This applies to small accessories and large objects: glasses, hats, coats, shoes, armor, tools, books, bikes, cars, and scenery modules.

## Suggested manifest

```json
{
  "assetId": "equipment.battle-helmet",
  "version": "1.0.0",
  "status": "approved",
  "source": "original-reference.png",
  "master": "battle-helmet.front.png",
  "views": ["front", "three-quarter-left", "three-quarter-right"],
  "canvas": { "width": 2048, "height": 2048 },
  "anchors": { "headCenter": [0.5, 0.46] },
  "zOrder": "front-of-head-behind-horns",
  "safePadding": 0.04,
  "notes": ["Preserve both eye openings", "Do not cover horns"]
}
```

Use normalized coordinates from 0 to 1 for anchors so masters can scale across export sizes.

## Versioning

- Patch: cleanup that does not change design or fit.
- Minor: new view, mask, anchor, or compatible detail.
- Major: visible redesign or incompatible proportions.

Never silently replace an approved master. Link derivatives to the exact character and equipment versions used.
