# Intake and Planning

Use this reference for a new asset system, a new batch, or an ambiguous request.

## Minimum intake

Resolve these fields before expensive production:

| Area | Required decision |
| --- | --- |
| Purpose | UI icon, mascot, sprite, illustration, animation, game, film/VFX, or 3D |
| Character source | Existing approved character, reference set, or new design |
| Identity locks | Proportions, face, teeth, horns, hair, skin, permanent jewelry, belt, shoes, markings |
| Expressions | Ordered names with a reference for each |
| Equipment | Existing master, extracted from a sheet, separately supplied, or newly designed |
| Interaction | Worn, held, carried, ridden, behind, in front, or partially occluded |
| Layout | Individual files, contact sheet, sprite sheet, sequence, or layered source |
| Output | Pixel dimensions, master dimensions, aspect ratio, format, alpha, color space, size limit |
| Safe area | Minimum transparent padding in pixels or percent at delivery size |
| Quality | Draft, production, high-detail, print, game-ready, or VFX-ready |

Ask for final display size as well as export size. If an icon is displayed at 30×30 but exported larger, define the safe-area ratio at the delivery size and verify a 30×30 preview.

## Planning output

Before generation, produce a compact plan containing:

- asset inventory and variant count;
- locked versus generative elements;
- master resolution and delivery sizes;
- pose/expression/equipment matrix;
- whether sketches or angle studies are needed;
- transparency strategy;
- acceptance criteria and approval gates;
- expected export structure and filenames.

## Technique selection

| Situation | Preferred technique |
| --- | --- |
| Exact rigid equipment reused in similar angle | Composite approved master |
| Equipment changes perspective slightly | Angle-specific master or controlled local generation |
| Hands interact with a prop | Lock prop; generate pose/hands around it; repair locally |
| Clothing deforms with the body | Layered rig or controlled generation |
| Many expressions, stable front view | Layered 2D face/body rig |
| Multiple camera angles | Multi-view design pack or 3D master |
| Bike, car, armor, machinery | 3D master/proxy, then render or stylize |
| Early concept exploration | Generative drafts, clearly marked non-master |

Do not batch-produce until at least one difficult representative case has passed the production gate.
