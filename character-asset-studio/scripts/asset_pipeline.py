#!/usr/bin/env python3
"""Normalize transparent assets, build contact sheets, and create deterministic ZIP packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc

IMAGE_SUFFIXES = {".png", ".webp"}


def image_paths(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(path for path in target.rglob("*") if path.suffix.lower() in IMAGE_SUFFIXES)


def normalize(source: Path, output: Path, width: int, height: int, padding: int, ground: int) -> None:
    with Image.open(source) as opened:
        image = opened.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"{source} is fully transparent")
    cropped = image.crop(bbox)
    available_width = width - (2 * padding)
    available_height = height - padding - ground
    if available_width <= 0 or available_height <= 0:
        raise ValueError("padding and ground margin leave no usable canvas")
    scale = min(available_width / cropped.width, available_height / cropped.height, 1.0)
    resized = cropped.resize(
        (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = (width - resized.width) // 2
    y = height - ground - resized.height
    canvas.alpha_composite(resized, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def contact_sheet(files: list[Path], output: Path, columns: int, gutter: int, cell: tuple[int, int]) -> None:
    if not files:
        raise ValueError("no input images")
    rows = (len(files) + columns - 1) // columns
    cell_width, cell_height = cell
    sheet = Image.new(
        "RGBA",
        (columns * cell_width + (columns + 1) * gutter, rows * cell_height + (rows + 1) * gutter),
        (0, 0, 0, 0),
    )
    for index, path in enumerate(files):
        with Image.open(path) as opened:
            image = opened.convert("RGBA")
        if image.size != cell:
            image.thumbnail(cell, Image.Resampling.LANCZOS)
        column, row = index % columns, index // columns
        x = gutter + column * (cell_width + gutter) + (cell_width - image.width) // 2
        y = gutter + row * (cell_height + gutter) + (cell_height - image.height) // 2
        sheet.alpha_composite(image, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def package(source: Path, output: Path, manifest: Path | None) -> None:
    files = sorted(path for path in source.rglob("*") if path.is_file())
    if manifest:
        files.append(manifest)
    records = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            arcname = path.name if path == manifest else path.relative_to(source).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
            records.append({"file": arcname, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        package_manifest = json.dumps({"files": records}, indent=2).encode() + b"\n"
        info = zipfile.ZipInfo("package-manifest.json", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, package_manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    normal = commands.add_parser("normalize")
    normal.add_argument("source", type=Path)
    normal.add_argument("output", type=Path)
    normal.add_argument("--width", type=int, required=True)
    normal.add_argument("--height", type=int, required=True)
    normal.add_argument("--padding", type=int, default=0)
    normal.add_argument("--ground", type=int, default=0)
    sheet = commands.add_parser("contact-sheet")
    sheet.add_argument("source", type=Path)
    sheet.add_argument("output", type=Path)
    sheet.add_argument("--columns", type=int, default=4)
    sheet.add_argument("--gutter", type=int, default=16)
    sheet.add_argument("--cell-width", type=int, required=True)
    sheet.add_argument("--cell-height", type=int, required=True)
    pack = commands.add_parser("package")
    pack.add_argument("source", type=Path)
    pack.add_argument("output", type=Path)
    pack.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "normalize":
            normalize(args.source, args.output, args.width, args.height, args.padding, args.ground)
        elif args.command == "contact-sheet":
            contact_sheet(image_paths(args.source), args.output, args.columns, args.gutter, (args.cell_width, args.cell_height))
        else:
            package(args.source, args.output, args.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
