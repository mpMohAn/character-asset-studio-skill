# Production and QA

Use this reference for generation, editing, background removal, correction, export, and packaging.

## Production sequence

1. Freeze the output contract and selected master versions.
2. Choose a pose whose gesture supports both expression and equipment.
3. Create a pose/silhouette guide for complex interaction.
4. Generate or assemble one character variant on a roomy master canvas.
5. Inspect face, anatomy, permanent details, equipment design, grip/contact, perspective, and occlusion.
6. Repair only the defective region when possible.
7. Remove the background in a distinct edit while preserving all foreground subjects.
8. Inspect alpha edges on light, dark, saturated, and checkerboard backgrounds.
9. Normalize scale, ground line, canvas, and safe margins deterministically.
10. Run structural QA and inspect the final display-size preview.
11. Approve individual assets before assembling sheets or packages.

When using an image editor/generator for transparency, use this instruction unless the user requests different treatment:

> Remove the background from this image. Keep all foreground subjects unchanged and fully intact, with clean, smooth edges. Make the background transparent.

## Visual checks

- Character identity and expression match the selected reference.
- Body scale is consistent with the set unless deliberate perspective requires otherwise.
- No unrequested teeth, garments, ornaments, outlines, patches, or duplicated parts.
- Eyes remain structurally correct, including inside helmets and glasses.
- Equipment retains approved shape, colors, patterns, rings, logos, and material.
- Hands contact equipment naturally; equipment does not float.
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
