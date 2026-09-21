#!/usr/bin/env python3
"""Initialize and validate Character Asset Studio project manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
PROJECT_LISTS = (
    "labels", "characters", "expressions", "poses", "equipment", "scenes",
    "exportProfiles", "variants", "jobs", "packages",
)
ASSET_STATES = {
    "draft", "review", "changes-requested", "design-locked",
    "production-test", "production-approved", "archived",
}
JOB_STATES = {
    "queued", "running", "waiting-for-user", "paused-quota",
    "failed-retryable", "completed", "cancelled",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("manifest root must be an object")
    return value


def validate_project(data: dict) -> list[str]:
    issues: list[str] = []
    for field in ("schemaVersion", "projectId", "name", "status"):
        if not data.get(field):
            issues.append(f"missing required field: {field}")
    project_id = data.get("projectId")
    if project_id and not ID_PATTERN.fullmatch(str(project_id)):
        issues.append("projectId must use lowercase letters, digits, dots, or hyphens")
    if data.get("status") not in ASSET_STATES:
        issues.append(f"invalid project status: {data.get('status')}")
    for field in PROJECT_LISTS:
        if not isinstance(data.get(field), list):
            issues.append(f"{field} must be an array")
    variant_ids = [item.get("variantId") for item in data.get("variants", []) if isinstance(item, dict)]
    duplicate_variants = sorted({item for item in variant_ids if item and variant_ids.count(item) > 1})
    if duplicate_variants:
        issues.append(f"duplicate variant IDs: {', '.join(duplicate_variants)}")
    for job in data.get("jobs", []):
        if not isinstance(job, dict):
            issues.append("each job must be an object")
        elif job.get("status") not in JOB_STATES:
            issues.append(f"invalid job status: {job.get('status')}")
    return issues


def initialize(template: Path, output: Path, project_id: str, name: str) -> None:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    data = load_json(template)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    data.update({"projectId": project_id, "name": name, "createdAt": now, "updatedAt": now})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for relative in (
        "originals", "masters/characters", "masters/equipment", "masters/scenes",
        "work/generations", "work/corrections", "approved", "exports", "reports", "packages",
    ):
        (output.parent / relative).mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("output", type=Path)
    init_parser.add_argument("--project-id", required=True)
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--template", type=Path)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    if args.command == "init":
        if not ID_PATTERN.fullmatch(args.project_id):
            parser.error("--project-id must use lowercase letters, digits, dots, or hyphens")
        template = args.template or Path(__file__).parents[1] / "assets/templates/project.template.json"
        try:
            initialize(template, args.output, args.project_id, args.name)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(args.output)
        return 0

    try:
        data = load_json(args.manifest)
        issues = validate_project(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps({"valid": not issues, "issues": issues}, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
