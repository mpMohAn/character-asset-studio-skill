# Rigging and 3D

Read this reference for interactive mascots, multiple angles, animation, games, vehicles, or VFX.

## Choose the representation

| Requirement | Representation |
| --- | --- |
| Fixed UI thumbnails and a modest pose set | Layered 2D |
| Eye/head tracking and expression changes | Rigged 2D or 2.5D |
| Frequent camera-angle changes | 3D |
| Vehicles or rigid mechanical equipment | 3D master or proxy |
| Film/VFX interchange | 3D source plus rendered deliveries |

## Multi-direction character turnaround

Treat a request for “different directions” as a view matrix, not a four-side limit. Start from a locked neutral character master and choose the requested views explicitly. A practical full set covers front, front-left three-quarter, left profile, rear-left three-quarter, back, rear-right three-quarter, right profile, front-right three-quarter, overhead/high camera, and low camera. Add direct top or underside views only when the user actually asks for those literal views; distinguish a low camera looking up at a standing character from an underside view. For interactive head tracking, specify head directions separately from body/camera directions.

For each view record camera azimuth/elevation, character facing, projection (orthographic for comparable turnaround views; perspective for dramatic high/low views), frame bounds, visible face/hair/garment/equipment details, and occlusion. Lock the front/side/back orthographic views to a shared apparent height, ground line, neutral pose, light, palette, and rendering style. High and low camera views may change apparent proportions through perspective but must preserve the same physical proportions and construction. Never substitute a three-quarter pose for a true side or rear view.

Generate and inspect each view individually at sufficient resolution, then assemble only approved views into a labeled sheet. Verify full body and both feet fit with margins in every panel, especially low views; verify garment front/back construction, hair and ornament placement, weapon count, grip, silhouette and scale. A labeled panel with clipped feet or incompatible clothing fails the turnaround and must be repaired before delivery. For exact repeatability across many angles, use a 3D or 2.5D proxy and preserve the source design's 2D rendering style.

## Layered 2D/2.5D source

Separate at least the parts that need independent movement or occlusion: head, pupils, eyelids, brows, mouth shapes, torso, upper/lower arms, hands, legs, feet, tail, horns, ears, belt, front/back equipment, shadows, and effects. Define pivots, attachment anchors, masks, draw order, and neutral transforms.

For head-follow interaction, preserve the character's screen-space footprint and ground position across states. Test idle, extreme look directions, click reaction, and return-to-idle without layout jumps.

## 3D source

Keep:

- editable source such as `.blend`;
- production interchange such as `.glb`/`.gltf`, with `.fbx` only when required;
- mesh, UVs, textures, materials, skeleton, blend shapes, constraints, attachment sockets, cameras, and lighting specification;
- named equipment sockets on head, hands, back, waist, feet, and vehicles;
- turntable and orthographic approval renders.

Use the same camera, focal length, lights, tone mapping, and render scale for a comparable 2D set. If an AI stylization stage follows rendering, retain the raw render and use it as structural conditioning.

## Transition strategy

Design the 2D manifest so it can later reference a 3D source, view name, camera, animation clip, socket, and render preset. Do not force a full 3D pipeline into an icon-only first release; add it when angle reuse or animation savings justify the setup cost.
