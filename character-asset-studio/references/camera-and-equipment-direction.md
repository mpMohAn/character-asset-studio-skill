# Camera Direction and Equipment Choreography

Use this reference before rendering portraits, action, combat, equipment interaction, scenes, posters, key art, or sequential frames. Treat camera and equipment as storytelling systems.

## Camera intent first

Define what the viewer must notice and feel before selecting settings. Record:

- subject and exact focus target;
- desired intimacy, power, speed, scale, tension, or isolation;
- camera position, height, yaw, pitch, roll, distance, and movement;
- lens family, focal length, perspective effect, framing, and focus behavior;
- exposure or motion settings only when they change the visible result.

For illustration and concept art, camera values describe an optical look rather than claiming literal photographic capture.

## Lens and focal-length guide

| Range | Typical visual use | Risks |
| --- | --- | --- |
| 14–24 mm | extreme scale, environment, fast close action | distorted faces, stretched limbs, enlarged near weapons |
| 28–35 mm | immersive action, two-character combat, environmental storytelling | edge distortion when faces are near frame borders |
| 40–50 mm | natural perspective, dialogue, balanced full-body scenes | may feel neutral without strong blocking |
| 70–105 mm | portraits, compressed duels, isolated emotional moments | reduced environment and flatter depth cues |
| 135 mm+ | surveillance, distant battle, strong compression | weak spatial clarity and disconnected subjects |

Choose focal length from the relationship between subjects and environment. Never default every scene to an unspecified cinematic wide lens.

## Advanced camera package

Record only parameters that affect the frame:

- **Sensor/aspect:** sensor analogy and delivery aspect ratio.
- **Focal length:** perspective and field of view.
- **Camera distance:** subject scale; do not fake framing by changing focal length alone.
- **Camera height:** low for dominance/scale, eye level for immediacy, high for vulnerability or tactical overview.
- **Yaw/pitch/roll:** facing, elevation, and deliberate Dutch angle. Avoid accidental horizon tilt.
- **Aperture/depth of field:** keep all interacting hands, faces, and contact points readable when required.
- **Focus distance/plane:** name the exact face, eye, weapon contact, or object held sharp.
- **Shutter look:** frozen action, readable controlled blur, or long-exposure effect. Apply blur only to moving elements and in the correct direction.
- **ISO/noise and dynamic range:** use only when grain, highlight retention, or shadow detail is visually relevant.
- **Camera movement:** static, pan, tilt, dolly, truck, crane, orbit, handheld, or follow. Represent movement through perspective, motion phase, and selective blur.
- **Lens character:** clean, soft, anamorphic, spherical, flare, bloom, distortion, chromatic aberration, or vignette. Use restrained effects with narrative cause.

## Camera decision rules

- Keep important faces away from heavily distorted wide-angle edges.
- Keep interacting subjects on compatible perspective and focus planes.
- Focus on the narrative event, not automatically on the nearest object.
- Use depth of field to simplify, never to hide broken anatomy or equipment.
- Match motion blur to shutter intent, velocity, rotation, and camera movement.
- Use foreground occlusion only when it increases depth without hiding identity or action.
- Preserve headroom, lead room, weapon clearance, and safe margins.
- Keep the horizon, vanishing points, ground contact, and character scale coherent.
- In multi-character scenes, verify every eye line against camera position and subject coordinates.

## Equipment identification

Before posing, inventory every important item:

- owner and master/version;
- name and category;
- intended function and available actions;
- rigid and flexible components;
- dimensions, silhouette, balance point, center of mass, and perceived weight;
- material, edge, articulation, moving parts, ammunition, straps, controls, and attachment points;
- dominant or required hand, grip type, contact points, and carry/rest states;
- current state: stored, held, aimed, loaded, drawn, charged, blocked, released, recoiling, damaged, or dropped;
- safety, collision, range, line of action, and plausible clearance;
- identity-locked colors, markings, geometry, and non-transferable motifs.

If the item is unfamiliar, infer its function from geometry and context, mark uncertainty internally, and choose a conservative physically plausible use. Ask the user only when different interpretations would materially change the result.

## Equipment choreography

Design the action from equipment affordances:

1. Select the action and exact motion phase: anticipation, initiation, action, impact, recoil, or recovery.
2. Place the equipment line of action and target/contact point.
3. Establish grip, wrist, elbow, shoulder, spine, pelvis, feet, and center of mass from the equipment's weight and force.
4. Add clearance so blades, bows, tools, shields, straps, and limbs do not intersect accidentally.
5. Apply resistance, recoil, tension, leverage, drag, momentum, and follow-through.
6. Apply secondary movement to straps, cloth, hair, cables, ammunition, and loose parts.
7. Align gaze and expression with the equipment task and target.
8. Verify ownership and continuity; never swap or duplicate equipment across characters.

Examples of functional consequences:

- A drawn bow bends, the string aligns through the nocking point, the drawing shoulder loads, and the archer's gaze follows the target.
- A heavy axe shifts stance and shoulder load; it cannot be held like a weightless prop.
- Dual blades require separate clear arcs, intentional hand roles, and non-colliding trajectories.
- A shield changes torso angle, visibility, balance, and the available weapon path.
- A staff used for support contacts the ground and carries weight differently from a staff used to strike or cast.
- A firearm requires correct stock/hand contacts, sight alignment, muzzle direction, ammunition state, and recoil phase.

## Prompt block

Use a compact, visible-results camera and equipment block:

```text
Camera: 35 mm full-frame look; camera 1.2 m high at close-medium distance; slight low angle; level horizon; focus plane on the blade-arrow contact and both faces; f/5.6-equivalent depth so hands, faces, and weapons remain readable; 1/1000-equivalent frozen impact with minimal directional blur on loose cloth only.
Equipment: identify owner, function, handedness, grip, mass, state, target, contact, and motion phase for every important item. Pose the complete body around the equipment forces and preserve its locked geometry and palette.
```

Do not copy these values blindly. Select values that produce the requested visual result.

## Validation

Reject or repair when:

- the stated focal length conflicts with visible perspective;
- focus or blur hides the narrative action;
- subjects appear shot from incompatible camera positions;
- faces distort without intent;
- a weapon, tool, or prop is held decoratively rather than functionally;
- grips, strings, straps, controls, hinges, ammunition, contacts, or trajectories are impossible;
- body balance ignores equipment mass or force;
- equipment changes owner, hand, geometry, color, scale, or state without reason;
- added lens flare, grain, bloom, blur, or Dutch angle has no narrative purpose.

Record camera and equipment decisions in the job or cast manifest so retries and revisions preserve continuity.
