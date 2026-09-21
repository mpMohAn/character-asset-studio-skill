# Reusable Rule Labels

Use labels to apply stable production rules to a project, character, expression, pose, equipment item, scene, variant, or export profile.

## Label model

Each label has a unique kebab-case `id`, semantic `version`, `scope`, `priority`, optional parameters, and one or more enforceable rules. Store definitions in `project.json`; store assigned label IDs on the target object.

Scopes resolve from broad to narrow:

`project → character → expression/pose/equipment/scene → variant → export`

Narrower assignments override broader assignments only when the label definition permits overrides. Higher priority wins between labels at the same scope. An unresolved equal-priority conflict blocks production and requires an explicit choice.

## Core labels

| Label | Meaning | Enforcement |
| --- | --- | --- |
| `identity-locked` | Preserve approved permanent character details | Visual review; compare against identity pack |
| `face-locked` | Preserve face construction and feature placement | Local edits only outside face unless approved |
| `body-fixed` | Preserve body proportions and footprint | Bounding-box and ground-line comparison |
| `same-size` | Use an exact delivery canvas | Deterministic normalization |
| `equipment-locked` | Reuse an approved equipment master | Composite or reference exact asset/version |
| `transparent-background` | Require real alpha | Structural QA |
| `no-teeth` | Do not introduce visible teeth | Visual review |
| `no-outline` | Do not add a new outer stroke | Visual review |
| `safe-padding` | Preserve transparent margin | Structural QA |
| `preserve-ground-line` | Keep feet/baseline stable | Deterministic alignment |
| `first-without-equipment` | First variant is expression-only | Matrix validation |
| `manual-approval` | Stop before dependent batch work | Workflow gate |

## Parameterized assignment

```json
{
  "label": "same-size",
  "parameters": { "width": 300, "height": 300 },
  "scope": "export",
  "priority": 100
}
```

Do not encode project-specific dimensions inside the reusable definition. Put them in assignment parameters.

## Resolution output

Before creating a job, resolve all inherited labels and save:

- source label IDs and versions;
- final parameters;
- winning scope and priority;
- overridden values;
- conflicts and their resolution;
- a deterministic hash of the resolved rule set.

A resumed job must use the stored resolved rules. Do not silently apply a newly edited label version to an existing job; create a new job revision.
