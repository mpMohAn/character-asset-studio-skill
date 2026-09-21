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


class ManifestTests(unittest.TestCase):
    def test_template_is_valid(self):
        data = manifest.load_json(ROOT / "assets/templates/project.template.json")
        self.assertEqual(manifest.validate_project(data), [])

    def test_duplicate_variant_is_rejected(self):
        data = manifest.load_json(ROOT / "assets/templates/project.template.json")
        data["variants"] = [{"variantId": "v1"}, {"variantId": "v1"}]
        self.assertTrue(any("duplicate" in issue for issue in manifest.validate_project(data)))


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


if __name__ == "__main__":
    unittest.main()
