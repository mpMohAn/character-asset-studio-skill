# Composition and Fusion

Use this workflow whenever one or more registered identities appear multiple times or multiple identities contribute to one output. First select exactly one mode.

| Mode | Meaning | Default production method |
| --- | --- | --- |
| `single-master-montage` | One identity appears multiple times with different actions or expressions | Produce locked variants from one master, then compose them |
| `cast-composition` | Two or more genuinely distinct identities, such as Max and Jax, share one frame | Register each master, generate or approve separately, then compose deterministically |
| `selected-fusion` | User-selected traits form one new character | Create a source map, approve a silhouette, then generate a new master |
| `fusion-exploration` | Explore possible hybrids before choosing | Produce 2–4 clearly labeled concepts, then convert the chosen concept to `selected-fusion` |

Count unique approved master IDs before selecting a mode. Different poses, actions, expressions, clothing states, or camera angles of the same master do not create new characters. Never infer fusion merely because references appear together. When the user says "different characters" but fewer than two unique masters are available, request the missing character reference instead of cloning the available master.

## Single-master montage

Use this mode for one person repeated in several states, such as Max running, planning, fighting, and resting in one composition.

1. Register one master ID and version.
2. Register every instance as a variant of that master with its action, expression, view, clothing state, equipment state, and placement.
3. Preserve the same identity across every instance while making the requested states visually distinct.
4. Do not report the instances as different characters. Report one character with multiple variants.
5. Retain this mode when the user requests it; do not replace it with cast composition.

## Cast composition

Create a cast manifest from `assets/templates/cast.template.json`. Do not proceed as a multi-character cast until it contains at least two different `masterId` values. Two is only the minimum: accept any practical number of unique masters. If the cast is too dense for readable faces, propose multiple frames, panels, or depth groups instead of dropping identities.

1. Register every source character independently with a stable master ID and version, for example `character.max` and `character.jax`.
2. Freeze a visibly discriminating identity card for each: face, silhouette, body proportions, hair, palette, materials, clothing, equipment, scale, and non-transferable motifs.
3. Map each named character to exactly one role, action, expression, position, facing, depth, scale, eye line, contact, occlusion, and lighting plan.
4. Approve each character variant independently before assembly when there is no required body-to-body interaction.
5. Prefer deterministic compositing for lineups, parties, posters, and scenes without complex contact. Match light, shadow, perspective, and edge treatment after placement.
6. Use joint generation only when contact or occlusion cannot be assembled credibly. Lock every identity by name and master ID in the prompt and repair contaminated regions locally.
7. Inspect for identity collapse and cross-identity leakage: one source cloned into another role; swapped faces, palettes, motifs, clothing, equipment, scale, or handedness; or an omitted cast member silently replaced by a duplicate.
8. Verify the final frame contains the requested number of unique characters and that every cast-manifest entry is visually traceable.

## Staged scene assembly

Use staged assembly for both `single-master-montage` and `cast-composition`. Do not generate the complete group in one uncontrolled pass by default.

Choose one starting strategy:

- **Scene-first:** use when camera, architecture, landscape, furniture, or a shared map/table controls placement. Create and approve an empty background plate, then add characters from back to front.
- **Characters-first:** use when body interaction, poses, scale relationships, or silhouette are primary. Approve the character blocking first, then build the environment around it.

Apply this sequence:

1. Lock aspect ratio, camera, horizon, ground plane, light direction, palette, wind, and scene geometry.
2. Register every unique master and every required montage instance. Never omit an entry because of tool reference limits.
3. Create a blocking plan with bounding region, depth, facing, scale, eye line, action, expression, contact points, and occlusion for every entry.
   Infer this blocking from the scene, role, visual hierarchy, action, and available negative space. Keep it as an internal production artifact. Do not make the user place routine characters or props one by one; ask only when two unresolved alternatives would materially alter the story.
4. Produce or approve one character/variant at a time on a transparent or easily isolated layer when possible.
5. Place characters in depth order. After each placement, verify identity, scale, anatomy, equipment ownership, contact, safe margins, and overlap before proceeding.
6. Build tightly interacting pairs or small groups separately when a shared grip, embrace, collision, or mutual occlusion cannot be assembled from independent layers. Composite the approved group into the main frame.
7. Add shared props, contact shadows, reflected light, atmospheric depth, and consistent edge treatment only after all characters pass placement checks.
8. Run a final cast audit against the manifest: every requested identity/instance present exactly as specified, no clones, substitutions, identity leakage, or missing roles.

Preserve a style fingerprint for every master: medium, edge treatment, line weight, shape language, shading depth, texture, and detail density. Perspective and scene lighting may affect the character, but must not silently convert its native 2D or painterly treatment into a generic 3D-rendered character. When exact style and face fidelity matter more than unified rendering, prefer isolated source-style character layers plus deterministic compositing; use shared contact shadows and restrained color grading to integrate them.

Checkpoint the background plate, blocking plan, every approved character layer, each staged composite, and the final integration. Resume from the last approved stage rather than regenerating the complete scene.

## Selected fusion

Fuse exactly two or three **distinct source identities** into one new character. Count identities, not images or poses. For more than three identities, do not generate a single fusion: ask the user to select two or three, or propose staged separate fusions that the user explicitly chooses. Cast compositions may contain more characters; this limit applies only to fusion.

Create a fusion manifest from `assets/templates/fusion.template.json` before generation. Keep originals immutable.

1. Inventory **each** source at full available resolution: face, expression, hair and headwear, body proportions, clothing by slot (top, bottom, outerwear, footwear, accessories), all held and worn equipment, palette, materials, and rendering style. Avoid a small roster thumbnail when a larger source exists.
2. Assign a source ID to every output component. Name the exact feature inherited, including the face/expression, hair, body, each garment, and every tool. Use one source for the underlying face and body anatomy unless the user specifically requests a different split. A recognizable contribution from every source must survive; do not rely on a color or tiny ornament as the sole contribution.
3. Preserve selected components' shapes, motifs, colors, materials, and function. The fusion is an assembly of source-derived features, not permission to invent new armor, hybrid tools, emblems, hair, jewelry, or decorative parts. Do not add `new` traits or fabricate a visual bridge; if physical joining needs a neutral seam, keep it visually unobtrusive and record it as assembly, not as a new feature.
4. Resolve collisions by choosing which existing source item occupies each anatomy or clothing slot. Document rejected alternatives. Do not merge two faces, average expressions, combine incompatible body proportions, or layer all clothing indiscriminately. If the user named an expression, use it; otherwise choose and record one source expression.
5. Resolve every selected character and equipment source to its locked asset spec and exact version. Use the equipment's head-unit dimensions and aspect ratio to scale it to the selected body; retain its silhouette, component shapes, palette, material, and style. Never treat the equipment ledger's item name alone as an adequate lock.
6. Build a complete equipment ledger from all selected sources. Preserve each distinct requested tool at most once, unless the user explicitly excludes it. Choose the active tool based on the pose and grip. Place a second tool in the other hand only if its use is anatomically credible; otherwise stow it. Stow remaining tools visibly at the waist or on the back with believable sheaths, straps, anchors, clearances, and weight. For a three-source fusion with three tools, the default is one in hand and two visibly stowed. Keep long tools on the back when waist carry would be implausible. Never turn tools into new hybrids or float them around the body.
7. Choose one source rendering style as the visual anchor, or follow the user's explicit style choice. Record its medium, linework, edge treatment, shading depth, texture, and detail density. Match the output to that source; do not silently shift painterly, drawn, or stylized references into glossy 3D or photoreal rendering. If styles differ and no source clearly anchors the intended result, present the style choice with the concept before final rendering.
8. Approve a silhouette/component plan before rendered exploration when shapes differ materially. For a small preview request, create one draft from the documented plan, inspect it, and present it for review. Do not call a generated draft an approved reusable master.
9. Freeze one equipment-to-pose contract for each action: active tool, held/stowed states, body grip/contact, mounting anchors, weapon clearance, gaze, expression, and load-bearing stance. Keep the other tools visible and attached. Inspect the result against the inventory and ledger: all assigned traits visible, every selected source traceable, clothing slots coherent, expression readable, all equipment present exactly once at the locked scale, shape, colors and attachment, no unassigned feature, style matched, no clipping or anatomy errors. Repair a local defect if possible; regenerate from the component plan when drift is widespread. After approval, record the new master ID/version and full provenance.

## Fusion exploration

- Explore at most 2–4 materially different allocations of **the same two or three sources** when the user requests options.
- Label outputs as drafts. Vary which existing source contributes each component and the active/stowed equipment assignment, not random decoration.
- After selection, complete the trait map and equipment ledger before the selected-fusion design gate.

## Validation

Reject or repair an output when any of these occur:

- merged, duplicated, or unrecognizable faces;
- extra, missing, or fused limbs;
- equipment duplication or unintended hybridization;
- palette or motif leakage between cast members;
- variants of one master incorrectly reported as different characters;
- one identity cloned to fill the role of a missing identity;
- a requested named character omitted or replaced by another cast member;
- left/right swaps or inconsistent handedness;
- incoherent scale, contact, gravity, shadow, wind, or occlusion;
- fusion traits, expressions, clothing, or equipment with no declared source;
- more than three source identities in a single fusion;
- invented hybrid gear, missing or duplicated equipment, or an impossible carrying position;
- a generic 3D or photoreal style replacing the selected source medium;
- accidental replacement of a source master.

Repair the smallest defective region first. If contamination spans multiple identities, regenerate the affected character separately and composite it. If the trait map itself is contradictory, stop and request the user’s choice rather than inventing precedence.

## Output contract

For a single-master montage, deliver the assembled frame plus the per-variant placement record and report it as one character. For cast compositions, deliver the assembled frame plus the completed cast manifest and confirm the unique master count. For fusions, deliver a new master ID/version and the completed provenance manifest. Report any remaining ambiguity requiring human review.
