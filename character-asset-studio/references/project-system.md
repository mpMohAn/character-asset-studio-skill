# Project System and Resumable Website Jobs

Use this reference for project manifests, approvals, account storage, long-running work, and the future Character Asset Studio website.

## Canonical project model

Use `assets/templates/project.template.json` as the starting point. A project owns references to versioned characters, expressions, poses, equipment, scenes, export profiles, label definitions, variants, jobs, and packages. Files remain immutable once approved; revisions create new versions.

Recommended project layout:

```text
project/
  project.json
  originals/
  masters/{characters,equipment,scenes}/
  work/{generations,corrections}/
  approved/
  exports/
  reports/
  packages/
```

## State machines

Asset lifecycle:

`draft → review → changes-requested → design-locked → production-test → production-approved → archived`

Job lifecycle:

`queued → running → waiting-for-user | paused-quota | failed-retryable | completed | cancelled`

Only approved assets may enter final packages. Rejected attempts remain linked for audit but never enter exports.

## Variant matrix

Represent each requested character/expression/pose/equipment combination as a stable variant ID. Mark excluded combinations explicitly. The first item of a set may enforce `first-without-equipment`. Each variant records dependencies, status, attempt count, approved output, and QA report.

## Website identity and storage

The website must require authentication before persistent work. Offer **Continue with ChatGPT** when an officially supported OpenAI identity/OAuth capability is available for the deployed product. Do not imitate a ChatGPT login, collect ChatGPT passwords, reuse browser session cookies, or assume that a ChatGPT subscription automatically grants API quota.

If official ChatGPT-connected authentication is unavailable, use a normal application account and let the user explicitly connect supported providers. Keep application identity, provider authorization, billing, and generation quota as separate concepts.

Store account-scoped project metadata, manifests, approvals, job checkpoints, usage records, and asset references. Store binary originals/masters in private object storage with per-account authorization and short-lived download URLs. Encrypt data in transit and at rest. Record retention, export, and deletion controls. Never expose one account's assets or prompts to another account.

## Quota-aware chunking and resume

Before a large task:

1. Expand the variant matrix.
2. Estimate provider calls, deterministic operations, and storage.
3. Choose a small chunk boundary, normally one variant or one correction.
4. Save a job manifest with input asset versions, resolved-label hash, provider settings, and pending variant IDs.
5. Process chunks idempotently.
6. Save output, QA report, usage, and checkpoint after every chunk.
7. Stop safely before quota exhaustion.

When quota or execution time is insufficient, set the job to `paused-quota` and show **Resume**. Display completed, failed, and pending counts plus the next chunk. Resume from the last committed checkpoint; never regenerate completed approved variants unless the user selects retry or creates a revision.

Use an idempotency key derived from `account + project + job revision + variant + attempt`. A worker must verify ownership and current state before processing. Lease each chunk so duplicate workers cannot commit the same attempt.

## Minimum website screens

1. Sign in and account connection
2. Projects and master library
3. Intake, labels, and output contract
4. Variant matrix and estimate
5. Generation/correction queue
6. Compare, QA, and approval
7. Paused-job resume view
8. Export/package builder
9. Account storage, usage, export, and deletion

Keep this as implementation architecture until the website phase begins; do not make deployment-provider or OAuth claims without verifying current official support.
