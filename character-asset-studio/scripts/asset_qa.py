#!/usr/bin/env python3
"""Structural QA for transparent PNG/WebP character assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc


def inspect(path: Path, args: argparse.Namespace) -> dict:
    with Image.open(path) as source:
        image = source.convert("RGBA")
        width, height = image.size
        alpha = image.getchannel("A")
        bbox = alpha.getbbox()
        alpha_min, alpha_max = alpha.getextrema()
        if bbox:
            left, top, right, bottom = bbox
            padding = {"left": left, "top": top, "right": width - right, "bottom": height - bottom}
        else:
            padding = {"left": width, "top": height, "right": width, "bottom": height}

        issues: list[str] = []
        if args.expected_width and width != args.expected_width:
            issues.append(f"width {width} != {args.expected_width}")
        if args.expected_height and height != args.expected_height:
            issues.append(f"height {height} != {args.expected_height}")
        if alpha_min == 255:
            issues.append("image is fully opaque; transparent background is absent")
        if bbox is None:
            issues.append("image is fully transparent")
        if bbox and any(value < args.min_padding for value in padding.values()):
            issues.append(f"visible content is inside the {args.min_padding}px safe margin or clipped")

        edge_alpha = []
        for edge in (
            alpha.crop((0, 0, width, 1)),
            alpha.crop((0, height - 1, width, height)),
            alpha.crop((0, 0, 1, height)),
            alpha.crop((width - 1, 0, width, height)),
        ):
            pixels = edge.get_flattened_data() if hasattr(edge, "get_flattened_data") else edge.getdata()
            edge_alpha.extend(pixels)
        if max(edge_alpha, default=0) > 0:
            issues.append("visible pixels touch the canvas edge")

        return {
            "file": str(path),
            "format": source.format,
            "mode": source.mode,
            "width": width,
            "height": height,
            "alpha": {"min": alpha_min, "max": alpha_max},
            "visibleBoundingBox": list(bbox) if bbox else None,
            "padding": padding,
            "status": "pass" if not issues else "review",
            "issues": issues,
        }


def candidates(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(path for path in target.rglob("*") if path.suffix.lower() in {".png", ".webp"})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--expected-width", type=int)
    parser.add_argument("--expected-height", type=int)
    parser.add_argument("--min-padding", type=int, default=0)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    files = candidates(args.target)
    if not files:
        print("No PNG or WebP files found", file=sys.stderr)
        return 2
    results = [inspect(path, args) for path in files]
    report = {
        "summary": {
            "files": len(results),
            "passed": sum(item["status"] == "pass" for item in results),
            "review": sum(item["status"] == "review" for item in results),
        },
        "results": results,
    }
    output = json.dumps(report, indent=2)
    if args.report:
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["summary"]["review"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
