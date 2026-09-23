from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


manifest = load_module("project_manifest", ROOT / "scripts/project_manifest.py")
pipeline = load_module("asset_pipeline", ROOT / "scripts/asset_pipeline.py")
qa = load_module("asset_qa", ROOT / "scripts/asset_qa.py")
labels = load_module("rule_labels", ROOT / "scripts/rule_labels.py")
palette = load_module("palette_extract", ROOT / "scripts/palette_extract.py")


class ManifestTests(unittest.TestCase):
    def test_template_is_valid(self):
        data = manifest.load_json(ROOT / "assets/templates/project.template.json")
        self.assertEqual(manifest.validate_project(data), [])

    def test_duplicate_variant_is_rejected(self):
        data = manifest.load_json(ROOT / "assets/templates/project.template.json")
        data["variants"] = [{"variantId": "v1"}, {"variantId": "v1"}]
        self.assertTrue(any("duplicate" in issue for issue in manifest.validate_project(data)))

    def test_fusion_template_has_provenance_and_gates(self):
        data = json.loads((ROOT / "assets/templates/fusion.template.json").read_text())
        self.assertEqual(data["mode"], "selected-fusion")
        self.assertIn("traitMap", data)
        self.assertIn("provenance", data)
        self.assertEqual(
            set(data["approval"]),
            {"concept", "designLock", "productionLock"},
        )

    def test_cast_template_requires_distinct_master_identities(self):
        data = json.loads((ROOT / "assets/templates/cast.template.json").read_text())
        master_ids = {entry["masterId"] for entry in data["cast"]}
        self.assertEqual(data["mode"], "cast-composition")
        self.assertGreaterEqual(len(master_ids), 2)
        self.assertEqual(data["validation"]["minimumUniqueMasters"], 2)
        self.assertIsNone(data["validation"]["maximumUniqueMasters"])
        self.assertTrue(data["validation"]["preventIdentityCollapse"])
        self.assertTrue(data["assembly"]["checkpointAfterEachPlacement"])
        self.assertTrue(data["validation"]["requireEveryCastEntry"])


class PipelineTests(unittest.TestCase):
    def test_normalize_and_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.png"
            output = root / "exports/normalized.png"
            image = Image.new("RGBA", (100, 60), (0, 0, 0, 0))
            image.paste((255, 0, 0, 255), (10, 5, 90, 55))
            image.save(source)
            pipeline.normalize(source, output, 300, 300, 8, 8)
            with Image.open(output) as normalized:
                self.assertEqual(normalized.size, (300, 300))
                self.assertLess(normalized.getchannel("A").getbbox()[3], 300)

            archive = root / "package.zip"
            pipeline.package(output.parent, archive, None)
            with zipfile.ZipFile(archive) as packaged:
                names = packaged.namelist()
                self.assertIn("normalized.png", names)
                self.assertIn("package-manifest.json", names)
                report = json.loads(packaged.read("package-manifest.json"))
                self.assertEqual(report["files"][0]["file"], "normalized.png")

    def test_contact_sheet_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index in range(3):
                Image.new("RGBA", (20, 20), (index * 40, 0, 0, 255)).save(root / f"{index}.png")
            output = root / "sheet.png"
            pipeline.contact_sheet(sorted(root.glob("*.png")), output, 2, 4, (20, 20))
            with Image.open(output) as sheet:
                self.assertEqual(sheet.size, (52, 52))

    def test_comparison_sheet_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with_skill = root / "with.png"
            without_skill = root / "without.png"
            output = root / "comparison.png"
            Image.new("RGBA", (20, 40), (255, 0, 0, 255)).save(with_skill)
            Image.new("RGBA", (40, 20), (0, 0, 255, 255)).save(without_skill)
            pipeline.comparison_sheet(with_skill, without_skill, output, (100, 80), 10)
            with Image.open(output) as comparison:
                self.assertEqual(comparison.size, (230, 144))


class LabelTests(unittest.TestCase):
    def test_resolves_parameters_and_hash(self):
        document = json.loads((ROOT / "assets/templates/labels.template.json").read_text())
        document["assignments"] = [
            {"label": "transparent-background", "scope": "project", "priority": 10},
            {"label": "same-size", "scope": "export", "priority": 20,
             "parameters": {"width": 300, "height": 300}},
        ]
        result = labels.resolve(document)
        self.assertTrue(result["valid"])
        self.assertEqual(result["resolved"]["width"], 300)
        self.assertTrue(result["resolved"]["alphaRequired"])
        self.assertEqual(len(result["resolvedRuleHash"]), 64)

    def test_equal_priority_conflict_blocks(self):
        document = {
            "definitions": [
                {"id": "a", "version": "1", "overridable": True, "rules": {"width": 100}},
                {"id": "b", "version": "1", "overridable": True, "rules": {"width": 200}},
            ],
            "assignments": [
                {"label": "a", "scope": "export", "priority": 10},
                {"label": "b", "scope": "export", "priority": 10},
            ],
        }
        self.assertFalse(labels.resolve(document)["valid"])


class PaletteTests(unittest.TestCase):
    def test_extracts_visible_source_colors(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "palette.png"
            image = Image.new("RGBA", (4, 1), (0, 0, 0, 0))
            image.putdata([(255, 0, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255), (1, 2, 3, 0)])
            image.save(source)
            result = palette.extract(source, 2, 16)
            self.assertEqual(result["sampledPixels"], 3)
            self.assertEqual(result["swatches"][0]["hex"], "#FF0000")
            self.assertAlmostEqual(sum(item["coverage"] for item in result["swatches"]), 1.0)

    def test_excludes_flat_corner_background(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "background.png"
            image = Image.new("RGBA", (5, 5), (240, 230, 190, 255))
            image.putpixel((2, 2), (220, 40, 20, 255))
            image.save(source)
            result = palette.extract(source, 2, 16, 20)
            self.assertEqual(result["sampledPixels"], 1)
            self.assertEqual(result["swatches"][0]["hex"], "#DC2814")


if __name__ == "__main__":
    unittest.main()
