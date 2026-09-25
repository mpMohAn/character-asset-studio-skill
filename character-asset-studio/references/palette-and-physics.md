# Palette and Physical Properties

Use this reference before generation, pose changes, animation frames, equipment interaction, or environmental effects.

## Palette lock

Extract a candidate palette from the approved source with `scripts/palette_extract.py`. For an opaque image on a mostly flat background, use `--exclude-corner-background <tolerance>` and confirm that intentional subject colors were not removed. Review every result visually because clustering cannot determine semantic roles by itself.

```bash
python3 scripts/palette_extract.py reference.png --colors 8 --exclude-corner-background 28 --output palette.json
```

Record for each approved swatch:

- stable name and role, such as `eye-red`, `head-black`, `marking-cream`, or `shield-red`;
- sRGB hex and RGB values;
- approximate source coverage;
- whether it is identity-locked, material-specific, highlight/shadow, or optional;
- allowed tolerance or approved variants;
- source asset and version.

Separate background colors from subject colors. Do not include the removed background in a transparent asset's character palette. In prompts, state the exact locked swatches and forbid hue substitution, saturation inflation, and newly invented accent colors. Compare the output against the palette before approval.

Use a new palette version when an approved color changes. A lighting condition may transform appearance, but keep the material's base color recorded separately from the rendered color.

## Physical model

Define only properties that materially affect the requested frame:

| Property | Record |
| --- | --- |
| Scale | Character/object size and relative proportions |
| Mass | Light/medium/heavy class, distribution, center of mass |
| Gravity | Direction and strength; normally downward at 1g |
| Support | Ground plane, planted feet, seat, grip, suspension, or flight |
| Medium | Air, water, vacuum, smoke, magical field, or stylized void |
| Wind/flow | Direction, strength, gusts, turbulence, drag |
| Material | Rigid, flexible, cloth, hair, liquid, brittle, elastic |
| Motion | Velocity, acceleration, rotation, recoil, follow-through |
| Time | Still pose or motion phase: anticipation, action, impact, recovery |
| Secondary motion | Cloth, hair, tails, straps, loose equipment, particles |
| Contacts | Grip, collision, pressure, occlusion, shadow, deformation |

Use normalized screen directions where useful, for example wind `[-1, 0]` for right-to-left. Record units for measured values; otherwise use named qualitative levels consistently.

## Character anatomy, costume, and shadows

Keep the locked silhouette, torso/chest/hip shape, and visible muscle definition coherent as the pose changes. Use the recorded functional strength only to guide balance, load and muscle tension; a numeric weight is not inferred from the picture. Apply muscle contraction where an action loads the body, without changing the count of visible abdominal segments or adding anatomy hidden in the source. Move visible inner layers with the outer garments using the recorded coverage and draw order. Cast shadows follow the scene light and ground/object contacts; shadows are not a permanent color, tattoo, or body marking.

## Cause-and-effect rules

- Place the center of mass over the support area for a stable pose; shift it deliberately for running, falling, recoil, or anticipation.
- Make heavy equipment affect shoulders, elbows, stance, and balance more than light equipment.
- Keep rigid equipment geometry stable. Apply bending and flutter only to flexible parts.
- Apply wind consistently to every exposed flexible element, with smaller delayed motion for heavier parts.
- Distinguish pose from motion phase. A raised weapon at anticipation differs from the same weapon during impact or recovery.
- Preserve momentum and follow-through across sequential frames.
- Do not add wind, dust, cloth motion, blur, or particles merely to make an image dramatic.
- For stylized or impossible physics, record the intended exception and keep it consistent across the asset set.

## Prompt block

Include a compact frozen block in the production prompt:

```text
Palette: use only the approved base swatches and their allowed highlight/shadow tolerances.
Physics: gravity down; medium still air; support both feet; equipment mass medium; shield rigid; coat flexible.
Time: anticipation frame immediately before forward action.
Motion: body leaning forward; shield leads; weapon trails slightly; loose cloth follows with delayed motion.
```

Save this physical model and palette version in the variant/job manifest so retries and resumed jobs use the same conditions.
