#!/usr/bin/env python3
"""Extract a compact source-derived sRGB palette from raster references."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc


def color_distance_squared(first: tuple[int, int, int], second: tuple[int, int, int]) -> int:
    return sum((a - b) ** 2 for a, b in zip(first, second))


def extract(path: Path, colors: int, alpha_threshold: int, background_tolerance: int = 0) -> dict:
    with Image.open(path) as opened:
        image = opened.convert("RGBA")
    corner_samples = [
        image.getpixel((0, 0))[:3],
        image.getpixel((image.width - 1, 0))[:3],
        image.getpixel((0, image.height - 1))[:3],
        image.getpixel((image.width - 1, image.height - 1))[:3],
    ]
    corner_color = tuple(round(sum(pixel[channel] for pixel in corner_samples) / 4) for channel in range(3))
    pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
    visible = [
        pixel[:3]
        for pixel in pixels
        if pixel[3] >= alpha_threshold
        and (
            background_tolerance <= 0
            or color_distance_squared(pixel[:3], corner_color) > background_tolerance ** 2
        )
    ]
    if not visible:
        raise ValueError("image has no pixels above the alpha threshold")
    sample = Image.new("RGB", (len(visible), 1))
    sample.putdata(visible)
    quantized = sample.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()
    counts = sorted(quantized.getcolors() or [], reverse=True)
    total = len(visible)
    swatches = []
    for count, index in counts:
        rgb = tuple(palette[index * 3:index * 3 + 3])
        swatches.append({
            "hex": "#" + "".join(f"{value:02X}" for value in rgb),
            "rgb": list(rgb),
            "coverage": round(count / total, 6),
        })
    return {
        "source": str(path),
        "colorSpace": "sRGB",
        "alphaThreshold": alpha_threshold,
        "excludedCornerBackground": {
            "enabled": background_tolerance > 0,
            "sampledColor": list(corner_color),
            "tolerance": background_tolerance,
        },
        "sampledPixels": total,
        "swatches": swatches,
        "review": "Assign semantic roles and remove background swatches before approval.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--colors", type=int, default=8, choices=range(2, 33), metavar="2..32")
    parser.add_argument("--alpha-threshold", type=int, default=16, choices=range(0, 256), metavar="0..255")
    parser.add_argument("--exclude-corner-background", type=int, default=0, choices=range(0, 256), metavar="0..255")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = extract(args.source, args.colors, args.alpha_threshold, args.exclude_corner_background)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
