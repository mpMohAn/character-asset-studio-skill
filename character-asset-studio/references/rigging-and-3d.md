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
