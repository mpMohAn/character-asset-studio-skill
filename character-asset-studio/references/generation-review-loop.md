# Generation review loop

Apply this workflow to every generation and correction. The user's latest explicit instructions take priority. The score measures reviewed requirement coverage. Visual judgments require the reviewing agent to inspect the image and reference. Python cannot establish semantic fidelity by itself.

## Before generation

Create a frozen JSON contract with a criteria array. Give every criterion a unique id, the exact requirement, its source (user instruction or reference/version), a positive weight, and a critical boolean. Default critical to true. Default threshold to 95. Include every requested detail and prohibition. Check the complete conversation for accepted revisions. Track superseded requirements explicitly. Resolve conflicting requirements before rendering. Never silently drop a requirement to increase the score.

Cover user intent, identity, exact geometry, requested counts, costume/closures, equipment, pose, style, composition, colors, lighting, framing and export requirements where applicable. Translate vague requests into observable checks. For a logo, check the actual letterform, silhouette, negative space and small-size legibility. Describe tolerances only when supported by the brief. Explain assumptions and record unknown details. Preserve original references and approved masters.

Read the relevant skill references. Check tool availability, source versions, canvas and file requirements. Include the critical requirements and explicit exclusions in the generation prompt. Create a new output per attempt.

## During generation

Check the request sent to the generator against the contract before submitting. Supply the approved reference images. Record the prompt, references and attempt number. Observe tool errors or missing outputs and handle them before review. If the tool exposes only a completed render, perform visual QA immediately after it returns. Never claim to inspect intermediate frames that the tool does not expose.

## After each generation

Inspect the actual image beside its sources at full size and at intended display size. Check each criterion separately, especially counts, occluded details, lettering geometry, additions and omissions. Mark pass, fail or unknown. Record a concrete observation for every pass, and a localized correction for every fail. Unknown counts as unpassed. Never infer that a prompt was followed merely because it contained the instruction.

Run asset_qa.py for transparent exports and their expected dimensions and padding. For intentionally opaque logos or scenes, check file decoding, dimensions, format and requested background instead; do not require transparency that the user did not request. Save the structural report. Hash the exact image bytes after all normalization, and hash the canonical contract JSON with sorted keys and compact separators.

The review JSON must include imageSha256, contractSha256, structuralQa with status and evidence, and checks containing id, status, evidence and correction. Run:

```sh
python3 scripts/review_gate.py contract.json review.json final.png --output gate.json
```

All critical criteria must pass with evidence, structural QA must pass, and the weighted score must reach the contract threshold. A high score cannot override a failed critical detail. This score is a review aid and does not certify artistic quality or replace user approval.

## Targeted second attempt

If the first result fails, use the failed image as an edit reference and the original source as the identity reference. Feed the exact observations and required corrections into one targeted edit. List approved regions and attributes to preserve. Prefer masks or localized edits when available. Repair deterministic dimension and padding failures with the image pipeline.

Review the entire second result against the same contract, including previously passed checks. Recompute hashes and structural QA after any edit. Compare attempts and retain the stronger candidate. Keep the previous image and review for traceability. Do not claim a guaranteed second-attempt success. If the second result still fails, explain the remaining specific defects and return it as a draft with a recommended next correction. Continue further only within the user's requested scope and available generation budget. Never silently approve or present a failed candidate as finished.

## Delivery

Deliver an approved output with a concise account of checks, corrections and any uncertainty. For failed attempts, clearly state draft status and outstanding requirements. Store the contract, per-attempt images, prompts, structural reports, visual reviews and gate reports with the project manifest. A user-approved change creates a revised contract and triggers a fresh review.
