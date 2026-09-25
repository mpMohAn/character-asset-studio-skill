---
name: character-asset-studio
description: Plan, generate, inspect, and package consistent reusable character, expression, pose, equipment, clothing, vehicle, sprite, or mascot assets, including controlled fusion of two or three distinct characters. Use when visual identity and recurring object details must remain stable across an asset set; do not use for an unrelated one-off image edit.
---

# Character Asset Studio

Build a controlled asset system rather than a collection of unrelated generations. Preserve approved character identity, equipment geometry, materials, colors, proportions, and export rules across every variant.

## Route the request

1. Determine whether the task is exploration, master-asset creation, variant production, correction, QA, packaging, 2D rigging, or 3D planning.
2. For a new project or materially incomplete brief, read [intake-and-planning.md](references/intake-and-planning.md).
3. When creating or registering reusable assets, read [asset-specification.md](references/asset-specification.md) and create versioned character/equipment specs with size, shape, palette, style, and behavior locks.
4. Before generation, correction, background removal, QA, or export, read [production-and-qa.md](references/production-and-qa.md).
5. For multi-angle, animation, vehicle, game, VFX, or 3D deliverables, also read [rigging-and-3d.md](references/rigging-and-3d.md).
6. For reusable constraints or project labels, read [rule-labels.md](references/rule-labels.md).
7. For manifests, lifecycle states, long-running work, or a web implementation, read [project-system.md](references/project-system.md).
8. Before any render or pose change, read [palette-and-physics.md](references/palette-and-physics.md) and freeze the source palette and applicable physical properties.
9. For two or more characters in one frame, selected-trait fusion, hybrid characters, or fusion exploration, read [composition-and-fusion.md](references/composition-and-fusion.md). For fusion, enforce its two-or-three-source limit, component inventory, equipment ledger, source-style lock, fidelity targets, and post-render review before approval.
10. For any scene, poster, key art, montage, or multi-character composition, read [professional-game-art-direction.md](references/professional-game-art-direction.md) and apply its story, staging, appeal, and anti-AI review gates.
11. Before rendering a scene, action, equipment interaction, portrait, or key art, read [camera-and-equipment-direction.md](references/camera-and-equipment-direction.md). Freeze a motivated camera package and an equipment-use plan before posing subjects.

Ask only for missing decisions that materially change the result. Prefer one compact intake round. If references already establish an answer, state the inference and proceed.

## Core decisions

- Prefer locked reusable masters plus controlled generation and deterministic assembly. Do not regenerate approved equipment merely to place it on another character.
- Treat the character, expression, pose, equipment, environment, and export as separate controllable concerns.
- Use sketch, silhouette, or line-art approval before rendering only when the design or interaction is new, unclear, or geometrically complex.
- Generate each final character variant separately at a generous master resolution. Assemble sheets only from approved individual assets.
- Make pose and gesture support the expression and equipment. Avoid repeating the same hands, shoulders, or stance when their meaning changes.
- Perform background removal as a separate edit after generation when clean transparency is required. A checkerboard appearance is not proof of alpha transparency.
- Use deterministic processing for canvas size, alignment, padding, alpha checks, filenames, contact sheets, and ZIP packaging.
- Never deliver a raw generated transparent asset when its visible bounds touch the canvas edge. Normalize it to the output contract, rerun QA, and deliver only the normalized file.
- Preserve the original upload and every approved master. Create a new version instead of silently overwriting visual identity.
- Resolve reusable rule labels before production. Record the resolved rules in the job manifest so a resumed task behaves identically.
- For work that may exceed one execution quota, divide the matrix into idempotent chunks and checkpoint after every completed asset.
- Extract and approve a source-derived palette before generation. Treat palette changes as explicit revisions, not creative freedom.
- Define only the physical properties that affect the frame: scale, mass distribution, gravity, support, wind or medium, material response, motion phase, and time. Preserve deliberate stylization while keeping cause and effect coherent.
- Keep source identities separate by default. Merge traits only when the user explicitly selects a fusion mode.
- Count unique master identities, not rendered instances. Multiple poses or expressions of one master remain one character; a multi-character cast requires at least two different master IDs.
- Support any practical cast size; two is the minimum, not the maximum. Build montages and casts in staged, resumable passes instead of asking one generation to solve the entire frame at once.
- Infer character and prop placement from scene composition, role, scale, eye line, contact, and occlusion. Treat placement plans and blocking diagrams as internal production controls; do not ask the user where to place each item unless multiple placements would materially change the requested story and the references do not resolve the choice.
- Lock each source's visual medium and rendering style as part of identity. Do not convert painted, cel-shaded, hand-drawn, pixel, or flat concept-art characters into generic 3D renders unless the user explicitly requests a style conversion.
- Art-direct the whole frame as a professional game designer would. Coordinate gaze, facing, action, expression, silhouette, hierarchy, props, environment, and lighting around one readable story beat; reject technically valid but visually unrelated character placements.
- Remove anything that does not strengthen character, story, gameplay readability, world-building, navigation, or mood. More detail is not automatically better.
- Choose lens, focal length, camera distance, height, angle, focus, depth of field, shutter behavior, and movement from the intended story and action. Do not add camera terminology that has no visible consequence.
- Resolve the locked character and equipment versions and their attachment/grip anchors before designing the pose. Identify equipment before designing the pose. Determine ownership, function, geometry, weight, material, handedness, grip, active state, contacts, and tactical use; then make the body respond to it.
- Treat every approved fusion as a new master with its own identity, version, palette, and provenance; never overwrite the source masters.

## Approval gates

Use two gates for substantial asset sets:

1. **Design lock:** approve character identity, expression map, equipment masters, palette, style, proportions, views, and output contract.
2. **Production lock:** approve representative variants after transparency and QA, before batch expansion or packaging.

For a single correction, keep the gate proportional: show the corrected asset and its QA result.

## Tool selection

- Use image generation/editing for raster illustration, pose changes, localized correction, or transparent cutouts.
- Use masks or localized editing when only one region is defective; preserve approved regions unchanged.
- Use deterministic image tools for resizing, compositing, padding, alpha cleanup, sheet assembly, and format conversion.
- Prefer layered/vector composition for rigid recurring accessories when exact reuse matters.
- Prefer a 3D source or proxy for repeated angle changes, vehicles, hard-surface equipment, or animation-ready deliverables.

Do not claim pixel-identical consistency from a generative model. Explain when an output is reference-conditioned versus assembled from locked source assets.

## Completion contract

Before delivery, report:

- what was created or changed;
- which masters and versions were used;
- master and delivery dimensions;
- file format, color space, and transparency status;
- automated QA findings and any human-review items;
- manifest/package location when multiple files are delivered.

Run `scripts/validate_asset_locks.py` on character and equipment specs and the fusion manifest before production. The validator checks the referenced exact IDs and versions, required locks, and an interaction for each retained tool. Do not mark a draft approved to bypass missing details.

Run `scripts/asset_qa.py` on PNG/WebP exports when local files are available. Treat its report as structural QA, not a substitute for visual review. A fusion draft needs every source-fidelity review field passed before it is called an approved master.

For requested skill-versus-baseline tests, keep the reference, requested change, export contract, and model/tool constant. Show the final results next to each other in one labeled comparison sheet, with **With skill** on the left and **Without skill** on the right. Embed that comparison image directly in the final response, then place the concise assessment table immediately below it. Do not deliver only the table, a file link, or two images shown separately, and do not make the user correlate outputs across earlier messages.

Use `scripts/asset_pipeline.py` for deterministic normalization, contact sheets, and ZIP packaging. Use `scripts/project_manifest.py` to initialize or validate project manifests from `assets/templates/`.
Use `scripts/palette_extract.py` to derive a candidate palette from approved reference pixels before writing generation prompts.
