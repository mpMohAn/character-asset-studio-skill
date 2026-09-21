---
name: character-asset-studio
description: Plan, generate, inspect, and package consistent reusable character, expression, pose, equipment, clothing, vehicle, sprite, or mascot assets. Use when visual identity and recurring object details must remain stable across an asset set; do not use for an unrelated one-off image edit.
---

# Character Asset Studio

Build a controlled asset system rather than a collection of unrelated generations. Preserve approved character identity, equipment geometry, materials, colors, proportions, and export rules across every variant.

## Route the request

1. Determine whether the task is exploration, master-asset creation, variant production, correction, QA, packaging, 2D rigging, or 3D planning.
2. For a new project or materially incomplete brief, read [intake-and-planning.md](references/intake-and-planning.md).
3. When creating or registering reusable assets, read [asset-specification.md](references/asset-specification.md).
4. Before generation, correction, background removal, QA, or export, read [production-and-qa.md](references/production-and-qa.md).
5. For multi-angle, animation, vehicle, game, VFX, or 3D deliverables, also read [rigging-and-3d.md](references/rigging-and-3d.md).
6. For reusable constraints or project labels, read [rule-labels.md](references/rule-labels.md).
7. For manifests, lifecycle states, long-running work, or a web implementation, read [project-system.md](references/project-system.md).

Ask only for missing decisions that materially change the result. Prefer one compact intake round. If references already establish an answer, state the inference and proceed.

## Core decisions

- Prefer locked reusable masters plus controlled generation and deterministic assembly. Do not regenerate approved equipment merely to place it on another character.
- Treat the character, expression, pose, equipment, environment, and export as separate controllable concerns.
- Use sketch, silhouette, or line-art approval before rendering only when the design or interaction is new, unclear, or geometrically complex.
- Generate each final character variant separately at a generous master resolution. Assemble sheets only from approved individual assets.
- Make pose and gesture support the expression and equipment. Avoid repeating the same hands, shoulders, or stance when their meaning changes.
- Perform background removal as a separate edit after generation when clean transparency is required. A checkerboard appearance is not proof of alpha transparency.
- Use deterministic processing for canvas size, alignment, padding, alpha checks, filenames, contact sheets, and ZIP packaging.
- Preserve the original upload and every approved master. Create a new version instead of silently overwriting visual identity.
- Resolve reusable rule labels before production. Record the resolved rules in the job manifest so a resumed task behaves identically.
- For work that may exceed one execution quota, divide the matrix into idempotent chunks and checkpoint after every completed asset.

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

Run `scripts/asset_qa.py` on PNG/WebP exports when local files are available. Treat its report as structural QA, not a substitute for visual review.

Use `scripts/asset_pipeline.py` for deterministic normalization, contact sheets, and ZIP packaging. Use `scripts/project_manifest.py` to initialize or validate project manifests from `assets/templates/`.
