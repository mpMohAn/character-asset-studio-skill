# Character Asset Studio

Character Asset Studio is a reusable ChatGPT and Codex skill for producing consistent character assets, pose and expression variants, multi-character scenes, equipment, clothing, vehicles, sprites, and mascots.

It adds a structured production workflow around image generation: identity and style locks, palette extraction, physical behavior, professional game-art direction, camera planning, equipment choreography, quality checks, and resumable project state.

> **Distribution status:** the skill is complete and usable by developers today. A skills-only ChatGPT plugin is the next packaging step. The plugin will provide the user-friendly installation route while keeping the skill itself unchanged.

## Install in ChatGPT

### One-click plugin installation

**Coming with the skills-only plugin release.** The public **Install in ChatGPT** link will be added here after the plugin package is published and its installation route is available.

The plugin will:

- install the existing `character-asset-studio` skill without changing its workflow;
- make the skill available from ChatGPT's plugin and skill interface;
- run with each user's own ChatGPT account and image-generation access;
- allow users to receive future skill updates through the plugin package.

Until that release, use the developer installation below.

## Manual download for developers

[Download the latest repository ZIP](https://github.com/mpMohAn/character-asset-studio-skill/archive/refs/heads/main.zip) or clone it:

```bash
git clone https://github.com/mpMohAn/character-asset-studio-skill.git
cd character-asset-studio-skill
```

Install the skill for your user:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R character-asset-studio "$HOME/.agents/skills/character-asset-studio"
```

Or install it only for one repository:

```bash
mkdir -p .agents/skills
cp -R /path/to/character-asset-studio-skill/character-asset-studio \
  .agents/skills/character-asset-studio
```

Then ask ChatGPT or Codex to use `@character-asset-studio`. In interfaces that use dollar-prefixed skill names, use `$character-asset-studio`.

## Example prompts

### Single-character variants

```text
Use @character-asset-studio with this reference image. Create four actions—running,
jumping, attacking, and defending—and four expressions—happy, angry, surprised,
and focused. Preserve the face, silhouette, palette, clothing, and equipment.
```

### Skill-versus-normal comparison

```text
Use @character-asset-studio to create a happy running version of this character.
Also create the same request without the skill. Show both images side by side and
include a comparison table for identity, palette, equipment, pose, and physics.
```

### Multi-character scene

```text
Use @character-asset-studio to combine these selected characters in a deadly
warzone. Build the scene step by step, place the characters one at a time, make
their eye lines and actions respond to one another, and make one leader stand out.
Preserve each character's original visual style.
```

### Professional game-art direction

```text
Use @character-asset-studio to stage these two characters fighting each other.
Identify how their equipment should be used, choreograph a readable exchange,
choose a cinematic lens and focal length, and preserve their faces, costumes,
weapons, proportions, and source rendering style.
```

### Resume a larger job

```text
Use @character-asset-studio to continue this character project from its saved
manifest. Report what is complete, what failed validation, and the next smallest
generation batch required to finish it.
```

## Skill versus normal generation

The left side of every comparison uses Character Asset Studio's identity, style, palette, equipment, physics, and composition controls. The right side uses a shorter direct image request without the skill. The same source character is used on both sides. These are representative tests rather than a promise of identical output from every generation.

### Test reference

The reference supplies the authoritative front and back design, shield construction, symbols, palette, proportions, and illustration style.

![Dwarf warrior source reference](docs/images/dwarf-reference.webp)

### 1. Transparent master, angles, actions, expressions, equipment, and physics

Both sides requested the same eight outputs in the same order:

| Row | Panels |
|---|---|
| Turnaround | Front master · three-quarter left · profile · back |
| Variants | Happy run · angry attack · focused shield defense · surprised reaction |

![Character Asset Studio full asset-system comparison](docs/images/dwarf-asset-system-comparison.webp)

The checkerboard exposes transparency. The controlled sheet preserves alpha, the supplied back emblem, the shoulder shield, the costume palette, and a more consistent source style while coordinating balance, grip, weight, beard motion, and clothing motion with each action.

<details>
<summary>Open the controlled transparent PNG</summary>

![Transparent multi-angle dwarf character asset sheet](docs/images/dwarf-asset-system-with-skill.png)

</details>

### 2. Camera, lens intent, equipment use, perspective, and scene direction

Both sides requested four matching shots:

| Panel | Direction |
|---|---|
| Top left | 85 mm close portrait with readable face and shallow depth of field |
| Top right | 50 mm medium defense with shield grip, weight, contact, and occlusion |
| Bottom left | 35 mm full-body charge with grounded momentum and secondary motion |
| Bottom right | 24 mm low-angle hero shot with a strong readable silhouette |

![Character Asset Studio camera and equipment direction comparison](docs/images/dwarf-direction-comparison.webp)

The skill-directed result deliberately separates shot purpose, protects character identity, keeps the shield functional, controls perspective, and limits environmental detail to what supports the focal action. The baseline favors spectacle and additional effects, but changes more design details and makes the four shots less distinct in purpose.

### 3. Focused action and expression tests

These earlier tests isolate smaller requests so action or expression fidelity can be inspected without the larger capability sheet.

<details>
<summary>Happy running comparison</summary>

![Character Asset Studio happy running comparison](docs/images/running-happy-comparison.webp)

</details>

<details>
<summary>Neutral attack comparison</summary>

![Character Asset Studio neutral attack comparison](docs/images/attack-neutral-comparison.webp)

</details>

<details>
<summary>Angry idle comparison</summary>

![Character Asset Studio angry idle comparison](docs/images/idle-angry-comparison.webp)

</details>

## Available production modes

Character Asset Studio is not limited to expressions and actions. Choose the mode that matches the deliverable:

| Mode | What it produces | Recommended source |
|---|---|---|
| Exploration | Clearly marked concept directions before identity is locked | Description, mood board, or rough sketch |
| Character master | Approved neutral identity, proportions, palette, costume, style, and permanent details | Front or three-quarter reference |
| Transparent master | Clean lossless PNG with alpha, safe padding, and no clipped details | Approved character master |
| Multi-angle pack | Front, three-quarter, profile, back, and optional turntable views | Front/back references, multi-view pack, or 3D proxy |
| Action variants | Running, jumping, attacking, defending, idle, custom actions, and equipment-aware poses | Approved character and action brief |
| Expression variants | Neutral, happy, angry, surprised, focused, custom expressions, and expression/gesture coordination | Approved face and expression map |
| Equipment and clothing | Extracted or designed masters, angle variants, worn/held/carried placement, attachment anchors, grip, masks, and occlusion | Equipment image, sheet, or written design |
| Palette control | Sampled source colors, semantic color roles, tolerances, and drift checks | Approved reference |
| Physics direction | Mass, gravity, balance, inertia, wind, hair, beard, cloth, secondary motion, contact, and collision | Action plus environment |
| Camera direction | Lens intent, focal length, framing, camera height, angle, depth of field, perspective, and motion treatment | Shot or scene brief |
| Professional game-art scene | Focal hierarchy, coordinated eyelines, readable silhouettes, purposeful actions, controlled detail, and scene storytelling | Character cast plus scene goal |
| Multi-character cast | Several distinct characters placed one by one with individual identity locks and shared interaction planning | One approved master per character |
| Single-character montage | One identity shown performing several coordinated jobs, actions, or expressions in one frame | One approved character master |
| Trait fusion | A new character combining selected, traceable traits from several sources with provenance and approval gates | Multiple references plus an explicit trait map |
| Vehicle and mount assets | Character/vehicle scale, seating, hand and foot contact, attachment sockets, perspective, and angle reuse | Character plus vehicle reference |
| Layered 2D/2.5D plan | Head, face, limbs, hands, equipment, masks, pivots, draw order, and animation states | Approved master and motion list |
| 3D transition plan | Mesh, materials, skeleton, blend shapes, sockets, camera presets, turntable, and `.blend`/`.glb` deliverables | Multi-view design pack |
| Correction and regional repair | Targeted repair of face, hands, equipment, edges, or one failed region while preserving approved areas | Failed asset plus approved master |
| QA and packaging | Alpha checks, size normalization, safe margins, filenames, manifests, contact sheets, sprite sheets, WebP/PNG exports, and ZIP packaging | Approved final assets |
| Resumable project | Checkpoints, completed/pending variants, retry state, validation failures, versions, and the next smallest batch | Saved project manifest |

## Supported features

| Area | Support |
|---|---|
| Character consistency | Identity, silhouette, proportions, face, costume, and recurring-detail locks |
| Color | Palette extraction, semantic color roles, tolerances, and palette validation |
| Poses and expressions | Presets, custom actions, custom expressions, and action/expression validation |
| Motion and physics | Mass, gravity, balance, inertia, wind, cloth, hair, and secondary-motion planning |
| Equipment | Equipment identification, hand assignment, grip logic, contact, collision, and functional use |
| Camera | Lens intent, focal length, framing, angle, depth of field, motion treatment, and perspective checks |
| Art direction | Professional game-art composition, focal hierarchy, eye-line coordination, scene readability, and style preservation |
| Multiple characters | Cast scenes, character-by-character placement, interaction planning, montages, and selected-trait fusion |
| Production | Transparent masters, variants, contact sheets, sprites, normalization, manifests, and delivery packaging |
| Reliability | Validation gates, regional repair, retry logic, checkpoints, resumable jobs, and structured failure reports |

## Limitations

- Image generation is probabilistic. The skill improves consistency but cannot guarantee pixel-identical faces, hands, clothing, or equipment across every result.
- Exact animation-ready control requires a layered 2D rig, vector artwork, or a 3D model. A flat PNG alone cannot provide independent bone, hand, leg, or facial controls.
- Transparent edges, small accessories, complex grips, and overlapping weapons may need a focused repair or cleanup pass.
- Large casts may require staged generation because image tools limit how many references can be used effectively in one pass.
- Fusion can combine selected traits, but it should not be used as a shortcut when the user needs several distinct characters to remain separately identifiable.
- Results depend on the available image model, reference quality, resolution, and the user's generation quota or plan.
- The one-click ChatGPT plugin installer is not published yet. Manual installation is currently intended for developer workflows.

## Repository structure

```text
character-asset-studio-skill/
├── README.md
├── docs/images/                 # Public comparison screenshots
└── character-asset-studio/      # Installable skill (kept unchanged)
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/
    ├── references/
    ├── scripts/
    └── tests/
```

The planned plugin will wrap the `character-asset-studio/` folder as its skills-only installation payload. User documentation and screenshots stay at the repository root so they do not add unnecessary context to the skill itself.

## Version and updates

**Current documentation version:** `0.2.1-pre`

**Status:** pre-release skill; plugin packaging pending

| Version | Update |
|---|---|
| `0.2.1-pre` | Added the dwarf reference showcase, transparent multi-angle asset-system comparison, camera/lens/equipment comparison, and the complete production-mode catalog |
| `0.2.0-pre` | Added professional game-art direction, camera and lens planning, equipment choreography, multi-character scenes, montage and fusion modes, palette/physics controls, and resumable workflows |
| `0.1.0` | Initial consistent character-asset workflow, reference intake, asset specification, generation, and quality checks |

Developers can update a cloned copy with:

```bash
git pull origin main
cp -R character-asset-studio "$HOME/.agents/skills/character-asset-studio"
```

After the ChatGPT plugin is published, plugin users will receive the skill through that installation package instead of copying the folder manually. Release notes and the current installation route will remain in this README.

## Plugin packaging roadmap

- [x] Complete and validate the reusable skill folder
- [x] Add user-facing examples, comparison screenshots, features, limitations, and update information
- [ ] Convert the repository into a skills-only ChatGPT plugin package
- [ ] Publish and add the **Install in ChatGPT** route
- [ ] Add tagged releases and plugin update notes
