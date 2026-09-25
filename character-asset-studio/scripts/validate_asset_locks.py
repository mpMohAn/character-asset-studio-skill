#!/usr/bin/env python3
"""Check that a character, equipment, or fusion manifest is ready for production."""

import argparse
import json
import re
from pathlib import Path

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def required(data, paths):
    issues = []
    for path in paths:
        value = data
        for key in path.split("."):
            value = value.get(key) if isinstance(value, dict) else None
        if value is None or value == "" or value == []:
            issues.append(f"missing {path}")
    return issues


def palette_issues(data):
    colors = data.get("palette", [])
    if not colors:
        return ["missing palette"]
    return [f"palette[{index}] needs a role, hex color, tolerance, and source"
            for index, color in enumerate(colors)
            if not color.get("role") or not HEX.fullmatch(str(color.get("hex", "")))
            or not color.get("tolerance") or not color.get("sourceReference")]


def validate(data, base_dir=None):
    kind = data.get("kind", "fusion" if data.get("mode") == "selected-fusion" else "")
    issues = required(data, ["assetId", "version", "source.reference", "source.sourceId"])
    if kind == "character":
        issues += required(data, ["identity.description", "identity.face.shape", "identity.expression",
            "identity.hair.shape", "identity.body.silhouette", "identity.clothing.top",
            "identity.clothing.bottom", "size.canvasPx.width", "size.canvasPx.height",
            "size.characterBoundsNormalized.width", "size.characterBoundsNormalized.height",
            "size.groundLineNormalized", "style.medium", "style.edges", "style.shading",
            "anchors.leftHand", "anchors.rightHand", "anchors.leftHip", "anchors.rightHip",
            "anchors.backUpper", "movement.dominantHand"])
        issues += palette_issues(data)
    elif kind == "equipment":
        issues += required(data, ["description", "dimensions.masterPx.width",
            "dimensions.masterPx.height", "dimensions.silhouetteBoundsNormalized.width",
            "dimensions.silhouetteBoundsNormalized.height",
            "dimensions.relativeToCharacter.lengthInHeadUnits",
            "dimensions.relativeToCharacter.widthInHeadUnits", "dimensions.aspectRatio",
            "dimensions.allowedScaleRange", "geometry.silhouette", "style.medium",
            "style.edges", "style.shading", "behavior.function",
            "behavior.massClass", "behavior.balancePointNormalized", "behavior.requiredHands",
            "attachment.zOrder"])
        issues += palette_issues(data)
        if not data.get("behavior", {}).get("permittedActions"):
            issues.append("missing behavior.permittedActions")
        if not data.get("behavior", {}).get("gripPointsNormalized"):
            issues.append("missing behavior.gripPointsNormalized")
    elif kind == "fusion":
        issues = required(data, ["newMasterId", "traitMap.face.sourceId", "traitMap.body.sourceId",
            "traitMap.hair.sourceId", "traitMap.expression.sourceId", "traitMap.style.sourceId",
            "actionPlan.pose", "actionPlan.motionPhase", "actionPlan.gazeTarget",
            "actionPlan.centerOfMass", "actionPlan.supportFeet"])
        sources = data.get("sources", [])
        if not 2 <= len(sources) <= 3 or len({s.get("sourceId") for s in sources}) != len(sources):
            issues.append("fusion needs two or three distinct source IDs")
        for index, source in enumerate(sources):
            if not source.get("characterSpec", {}).get("designLock"):
                issues.append(f"sources[{index}] character spec is not design locked")
            spec = source.get("characterSpec", {})
            if not spec.get("ref") or not spec.get("assetId") or not spec.get("version"):
                issues.append(f"sources[{index}] lacks character spec ref/id/version")
            elif base_dir is not None:
                issues += verify_reference(base_dir, spec["ref"], "character",
                                           spec["assetId"], spec["version"], f"sources[{index}]")
        for index, item in enumerate(data.get("equipmentLedger", [])):
            if not item.get("specRef") or not item.get("version"):
                issues.append(f"equipmentLedger[{index}] lacks locked spec/version")
            if not item.get("assetId") or item.get("specDesignLock") is not True:
                issues.append(f"equipmentLedger[{index}] lacks approved spec/id")
            elif base_dir is not None and item.get("specRef") and item.get("version"):
                issues += verify_reference(base_dir, item["specRef"], "equipment",
                                           item["assetId"], item["version"], f"equipmentLedger[{index}]")
            if item.get("role") not in ("active", "stowed-waist", "stowed-back", "excluded-by-user"):
                issues.append(f"equipmentLedger[{index}] has invalid role")
            if item.get("role") != "excluded-by-user" and (not item.get("attachmentAnchor")
                    or not item.get("relativeScaleInHeadUnits") or not item.get("state")):
                issues.append(f"equipmentLedger[{index}] lacks scale/attachment/state")
        checks = data.get("lockChecks", {})
        for name in ("characterSpecsApproved", "equipmentSpecsApproved",
                     "sizeShapeColorStyleVerified", "gripAndCarryVerified"):
            if checks.get(name) is not True:
                issues.append(f"lockChecks.{name} is not true")
        if not data.get("actionPlan", {}).get("equipmentInteractions"):
            issues.append("missing actionPlan.equipmentInteractions")
        interaction_ids = [entry.get("assetId") for entry in data.get("actionPlan", {}).get("equipmentInteractions", [])]
        for item in data.get("equipmentLedger", []):
            if item.get("role") != "excluded-by-user" and interaction_ids.count(item.get("assetId")) != 1:
                issues.append(f"equipment {item.get('assetId')} needs exactly one action interaction")
        return issues
    else:
        return ["unknown manifest kind"]
    if data.get("status") not in ("design-locked", "production-test", "production-approved"):
        issues.append("asset status is not design locked")
    if not data.get("approval", {}).get("designLock"):
        issues.append("approval.designLock is not true")
    for name, state in data.get("locks", {}).items():
        if state != "locked":
            issues.append(f"locks.{name} is not locked")
    return issues


def verify_reference(base_dir, ref, kind, asset_id, version, label):
    path = (base_dir / ref).resolve()
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{label} cannot read spec {ref}: {exc}"]
    if spec.get("kind") != kind or spec.get("assetId") != asset_id or spec.get("version") != version:
        return [f"{label} spec identity/version does not match {ref}"]
    return [f"{label} spec {ref}: {issue}" for issue in validate(spec)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    issues = validate(data, args.manifest.parent)
    print(json.dumps({"ready": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
