#!/usr/bin/env python3
"""Resolve reusable Character Asset Studio label assignments deterministically."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCOPE_RANK = {"project": 0, "character": 1, "asset": 2, "variant": 3, "export": 4}


def resolve(document: dict) -> dict:
    definitions = {item["id"]: item for item in document.get("definitions", [])}
    assignments = document.get("assignments", [])
    issues: list[str] = []
    candidates: dict[str, list[dict]] = {}
    sources: list[dict] = []
    for assignment in assignments:
        label_id = assignment.get("label")
        definition = definitions.get(label_id)
        if definition is None:
            issues.append(f"unknown label: {label_id}")
            continue
        scope = assignment.get("scope", "project")
        if scope not in SCOPE_RANK:
            issues.append(f"invalid scope for {label_id}: {scope}")
            continue
        rules = {**definition.get("rules", {}), **assignment.get("parameters", {})}
        source = {
            "label": label_id,
            "version": definition.get("version"),
            "scope": scope,
            "priority": int(assignment.get("priority", 0)),
            "overridable": bool(definition.get("overridable", True)),
            "rules": rules,
        }
        sources.append(source)
        for key, value in rules.items():
            candidates.setdefault(key, []).append({**source, "value": value})

    resolved: dict = {}
    winners: dict = {}
    for key, options in candidates.items():
        ordered = sorted(options, key=lambda item: (SCOPE_RANK[item["scope"]], item["priority"]), reverse=True)
        winner = ordered[0]
        for option in ordered[1:]:
            same_rank = (SCOPE_RANK[option["scope"]], option["priority"]) == (
                SCOPE_RANK[winner["scope"]], winner["priority"]
            )
            if same_rank and option["value"] != winner["value"]:
                issues.append(f"unresolved conflict for {key}: {winner['label']} vs {option['label']}")
            if not option["overridable"] and option["value"] != winner["value"]:
                issues.append(f"non-overridable rule {key} from {option['label']} was overridden")
        resolved[key] = winner["value"]
        winners[key] = {field: winner[field] for field in ("label", "version", "scope", "priority")}

    canonical = json.dumps({"resolved": resolved, "sources": sources}, sort_keys=True, separators=(",", ":"))
    return {
        "valid": not issues,
        "resolved": resolved,
        "winners": winners,
        "sources": sources,
        "issues": sorted(set(issues)),
        "resolvedRuleHash": hashlib.sha256(canonical.encode()).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        result = resolve(document)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
