# Local smoke test

Run from the extracted skill directory using Python 3.10 or newer with Pillow installed. Choose a fresh output directory.

## Initialize and validate

Save the supplied project template to a local file when the agent receives files as text. Pass that path explicitly.

```sh
python3 scripts/project_manifest.py init smoke-test/project.json --project-id smoke-test --name "Local smoke test" --template assets/templates/project.template.json
python3 scripts/project_manifest.py validate smoke-test/project.json
```

## Check an image

Use a user-selected PNG with visible content and transparency. Replace source.png with its local path.

```sh
python3 scripts/asset_pipeline.py normalize source.png smoke-test/exports/normalized.png --width 512 --height 512 --padding 16 --ground 16
python3 scripts/asset_qa.py smoke-test/exports/normalized.png --expected-width 512 --expected-height 512 --min-padding 16 --report smoke-test/reports/qa.json
python3 scripts/asset_pipeline.py package smoke-test/exports smoke-test/packages/assets.zip --manifest smoke-test/project.json
```

Expect a valid project, a 512 by 512 PNG, a passing structural QA report, and a readable ZIP containing the normalized image and manifest. Inspect the image visually for identity and clipping. A structural pass alone does not establish visual fidelity.

## Agent workflow check

Ask the agent to use Character Asset Studio to plan one character master and one pose variant. Confirm it loads the relevant references, records constraints, waits for design approval where needed, and reports actual file locations and QA findings. Complete rendering only when an image-generation tool is available.

Character, equipment, and fusion templates contain unfinished fields. Their lock validators should reject them until the missing source-derived details and approvals are supplied.
