# Asset Specification

Use this reference when defining, extracting, approving, or versioning reusable character and equipment masters.

Use `assets/templates/character.template.json` and `assets/templates/equipment.template.json` for versioned, machine-checkable specifications. A source image alone is not a lock: record the reference, measured relationships, colors, shapes, style, and behavior, then approve the lock before producing action variants.

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

Record a concise physical description that another artist could use without seeing the source. Specify normalized character bounds, head-to-body and shoulder-to-hip ratios, ground line, dominant hand, movement limits, and hand/hip/back anchors. Keep the expression separate from permanent face construction so a pose can change without changing identity.

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

Also record a plain-language description, normalized silhouette bounds, aspect ratio, length and width relative to the character's head, permitted scale range, color swatches with tolerances, source style fingerprint, component shapes, exact motifs, available states/actions, grip and balance points, required hands, and stowed waist/back attachment. Pixel dimensions describe the master canvas; they do not alone define apparent size on the character. For rigid equipment, proportion and component geometry stay locked across pose and perspective; for flexible parts, define permissible deformation.

This applies to small accessories and large objects: glasses, hats, coats, shoes, armor, tools, books, bikes, cars, and scenery modules.

## Locking and revision

Each template has an immutable source reference and version, an approval state, and per-field locks. Run `python3 scripts/validate_asset_locks.py path/to/spec.json` to check completeness; production accepts only a fully design-locked spec with source-based colors, dimensions, style, behavior, and anchors. Fusion validation loads the referenced character and equipment specs from disk and checks their exact IDs and versions. Set a lock to `locked` only after comparing it to the original at useful resolution. Keep uncertain values `draft` and do not claim full design lock. Store exact source/version pointers in every fusion and variant; do not silently borrow traits from a later version.

- **Character:** lock identity, face, expression reference, hair, body proportions, clothing slots, palette, style, and attachment anchors.
- **Equipment:** lock size relative to that character, silhouette/components, colors, materials, source style, function, grip, carry attachments, and permissible action states.
- **Relationship:** lock character anchor to equipment grip/strap point, scale, depth order, handedness, active/stowed state, and movement clearance per pose.
- **Gate:** do not set `approval.designLock=true` while a required field is unknown or draft. If the reference hides a crucial dimension, mark it inferred with rationale and review it before locking.
- **Change:** corrections within accepted tolerance are patches; compatible new angles/anchors are minor versions; altered silhouette, colors, size, function, or character identity require a new major design version and renewed approval.

A generative prompt can follow a lock but cannot guarantee exact geometry. Compare the resulting image to the spec; repair or reject drift rather than changing the spec to match the output.

## Versioning

- Patch: cleanup that does not change design or fit.
- Minor: new view, mask, anchor, or compatible detail.
- Major: visible redesign or incompatible proportions.

Never silently replace an approved master. Link derivatives to the exact character and equipment versions used.
