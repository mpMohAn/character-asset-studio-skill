# Professional Game Art Direction

Apply this reference to scenes, key art, splash art, posters, montages, and any frame containing character interaction. The goal is authored game artwork, not a collection of independently generated subjects.

## Define the frame

Before generation, write a compact internal art-direction brief:

- **Player impression:** what should the viewer feel in the first two seconds?
- **Story beat:** what single moment is happening now?
- **Focal order:** primary, secondary, and supporting reads.
- **Relationship map:** who looks at, reacts to, assists, opposes, or ignores whom, and why?
- **Action logic:** what each character is doing for this shared moment.
- **Expression logic:** what each face communicates about that action and relationship.
- **Visual economy:** which characters, props, effects, and background details are necessary.

Infer these decisions from the request and references. Keep blocking and placement internal unless an unresolved choice would materially change the story.

## Coordinate the cast

Treat direction, gaze, pose, expression, and action as one system.

- Give every character a scene-specific intention. Avoid generic idle poses unless waiting is the intended action.
- Create a readable gaze graph. A character may look at another character, a shared objective, a threat, or a task. Random outward gazes require a story reason.
- Align head direction, eye direction, torso twist, hand gesture, and foot placement with the same intention.
- Make expressions respond to the shared event and role. Do not paste unrelated emotions onto unrelated actions.
- Use eye lines and gestures to lead attention toward the focal subject, objective, or next narrative beat.
- Preserve individual personality while ensuring the cast appears to occupy the same time and story.
- Avoid evenly spaced lineup staging unless the requested output is explicitly a lineup.

## Build hierarchy and appeal

- Establish one dominant focal point using silhouette, scale, contrast, value, saturation, detail, framing, and negative space.
- Keep secondary characters readable without competing equally with the focal subject.
- Create large, medium, and small shape rhythms. Avoid uniform detail everywhere.
- Preserve clean silhouettes for faces, hands, weapons, and role-defining equipment.
- Use overlaps deliberately to create depth and relationships; avoid accidental tangencies and confusing intersections.
- Reserve the strongest light, contrast, sharpness, or color accent for the intended focal region.
- Check the image at thumbnail size. The story and focal order must remain understandable.

## Control the environment

- Make every visible prop serve story, function, world-building, navigation, composition, or mood.
- Remove repeated crates, weapons, banners, particles, debris, lights, and ornaments that merely fill space.
- Avoid symmetrical prop scattering, evenly distributed detail, and repeated motifs that signal procedural generation.
- Use quiet areas and negative space to improve readability.
- Match perspective, scale, gravity, contact, shadow, wind, and light direction across all subjects.
- Let environmental details support the cast instead of competing with faces and actions.

## Avoid the generated-AI look

Reject or repair outputs containing:

- characters posed as unrelated individual portraits inside one scene;
- random gaze directions with no relationship or objective;
- expressions disconnected from the action or narrative moment;
- uniform sharpness, contrast, detail, or importance across the frame;
- excessive decorative objects, particles, banners, weapons, rubble, or lights;
- repeated props, mirrored arrangements, ornamental noise, or empty spectacle;
- inconsistent face design, age, anatomy, rendering style, or character scale;
- dramatic lighting or motion added without narrative cause;
- cinematic depth that overwrites the source medium or identity;
- technically polished imagery with no clear focal point or emotional hook.

Do not solve these failures by adding more prompt adjectives or more objects. Simplify the frame, clarify the story beat, repair the smallest affected character or region, and rebuild the gaze/action relationships.

## Review gates

### Story gate

Approve only if a reviewer can answer in two seconds:

1. Who or what matters most?
2. What is happening?
3. How are the visible characters connected to that event?

### Character-direction gate

For every character verify:

- role and intention are visible;
- head, eyes, torso, hands, and feet support the action;
- expression supports the scene and personality;
- face and style match the approved master;
- pose differs for a reason, not random variation;
- equipment belongs to and is used by the correct character.

### Composition gate

Verify focal order, silhouette clarity, value grouping, negative space, depth, tangencies, prop economy, and thumbnail readability. If every region demands equal attention, the composition fails.

### Appeal gate

Confirm the frame has a deliberate visual hook: a compelling face, gesture, shape, contrast, relationship, or story question. Attractive does not mean adding detail; it means controlling attention and emotion.

Record failures as targeted revisions such as `redirect C gaze toward map`, `lower contrast on weapon rack`, or `remove redundant foreground crates`. Avoid vague instructions such as `make cinematic` or `make professional`.
