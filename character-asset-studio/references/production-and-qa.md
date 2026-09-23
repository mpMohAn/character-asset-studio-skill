# Production and QA

Use this reference for generation, editing, background removal, correction, export, and packaging.

## Production sequence

1. Freeze the output contract and selected master versions.
2. Extract, review, and freeze the source palette before writing the generation prompt.
3. Freeze applicable physical properties and the intended instant in time.
4. Choose a pose whose gesture supports both expression and equipment.
5. Create a pose/silhouette guide for complex interaction.
6. Generate or assemble one character variant on a roomy master canvas.
7. Inspect face, anatomy, permanent details, exact palette, equipment design, grip/contact, perspective, physics, and occlusion.
8. Repair only the defective region when possible.
9. Remove the background in a distinct edit while preserving all foreground subjects.
10. Inspect alpha edges on light, dark, saturated, and checkerboard backgrounds.
11. Normalize scale, ground line, canvas, and safe margins deterministically. Treat this as mandatory whenever visible pixels touch or enter the required safe margin.
12. Run structural QA on the normalized export and inspect the final display-size preview. If padding, edge-contact, alpha, or dimensions fail, do not deliver; correct and rerun QA.
13. Approve individual assets before assembling sheets or packages.

When using an image editor/generator for transparency, use this instruction unless the user requests different treatment:

> Remove the background from this image. Keep all foreground subjects unchanged and fully intact, with clean, smooth edges. Make the background transparent.

## Visual checks

- Character identity and expression match the selected reference.
- Body scale is consistent with the set unless deliberate perspective requires otherwise.
- No unrequested teeth, garments, ornaments, outlines, patches, or duplicated parts.
- Eyes remain structurally correct, including inside helmets and glasses.
- Equipment retains approved shape, colors, patterns, rings, logos, and material.
- Generated colors remain within the approved palette/tolerances; unexpected colors require review.
- Hands contact equipment naturally; equipment does not float.
- Weight, balance, gravity, support, wind response, cloth/hair motion, and the selected motion phase agree with each other unless an intentional stylized exception is recorded.
- Pose and gesture support meaning. Sadness should not inherit a celebratory gesture without a deliberate reason.
- No subject, shadow, glow, ray, weapon, tail, horn, or tool is clipped.
- No neighboring sprite or partial equipment is present.
- Transparent regions contain real alpha rather than white, black, or checkerboard pixels.
- Edge pixels have no light/dark matte halo.

## Structural QA

Run:

```bash
python3 scripts/asset_qa.py <file-or-directory> --expected-width 2048 --expected-height 2048 --min-padding 16 --report report.json
```

Omit expected dimensions when inspecting heterogeneous masters. The script reports format, dimensions, alpha range, visible bounding box, padding, edge contact, and likely opaque-background failures.

## Export rules

- Retain an archival lossless PNG master with alpha.
- Derive delivery PNG/WebP files from the approved master.
- Resize once from the master using a high-quality resampler; never repeatedly resize an already reduced image.
- Preserve sRGB unless another color space is explicitly required.
- Keep filenames stable and meaningful, for example `set-04-sadness__battle-helmet__v1.0.1.png`.
- Include a manifest mapping output files to source asset versions and generation/edit notes.
- Build contact sheets and ZIPs only from final approved exports.

For a contact sheet, use equal cells, consistent ground lines, explicit gutters, and enough outer padding that glows or long equipment remain intact.

## Deterministic commands

Normalize an approved asset without upscaling it:

```bash
python3 scripts/asset_pipeline.py normalize source.png output.png --width 300 --height 300 --padding 8 --ground 8
```

For a skill-versus-baseline test, normalize both outputs to the same cell size, then build one labeled side-by-side comparison:

```bash
python3 scripts/asset_pipeline.py compare with-skill.png without-skill.png comparison.png --cell-width 1024 --cell-height 1024
```

Keep **With skill** on the left and **Without skill** on the right. Use the same source reference, requested change, generator/model, aspect ratio, and transparency contract for both runs. The baseline prompt may omit the skill's controls, but must not change the target outcome. Embed the comparison sheet in the final response before the assessment table; a textual statement that it was created, a standalone link, or separately displayed generations does not satisfy the comparison contract.

Build a contact sheet from approved individual exports:

```bash
python3 scripts/asset_pipeline.py contact-sheet exports preview.png --columns 4 --cell-width 300 --cell-height 300 --gutter 16
```

Create a reproducible ZIP with hashes:

```bash
python3 scripts/asset_pipeline.py package exports package.zip --manifest project.json
```
