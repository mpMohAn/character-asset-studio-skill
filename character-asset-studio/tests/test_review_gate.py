import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('review_gate', Path(__file__).parents[1] / 'scripts/review_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.image = Path(self.temp.name) / 'image.png'
        self.image.write_bytes(b'image-version-one')
        self.contract = {'criteria': [
            {'id': 'shape', 'requirement': 'Circular C', 'weight': 99, 'critical': True},
            {'id': 'detail', 'requirement': 'Exact nose', 'weight': 1, 'critical': True},
        ]}
        self.review = {
            'imageSha256': hashlib.sha256(self.image.read_bytes()).hexdigest(),
            'contractSha256': hashlib.sha256(json.dumps(self.contract, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'structuralQa': {'status': 'pass', 'evidence': 'Dimensions and decode checked'},
            'checks': [
                {'id': 'shape', 'status': 'pass', 'evidence': 'Circular arc visible'},
                {'id': 'detail', 'status': 'pass', 'evidence': 'Profile matches reference'},
            ],
        }

    def result(self):
        return gate.evaluate(self.contract, self.review, self.image)

    def test_complete_review_passes(self):
        self.assertTrue(self.result()['approved'])

    def test_high_score_cannot_override_critical_failure(self):
        self.review['checks'][1]['status'] = 'fail'
        self.review['checks'][1]['correction'] = 'Restore nose'
        result = self.result()
        self.assertEqual(result['score'], 99)
        self.assertFalse(result['approved'])
        self.assertEqual(result['corrections'][0]['correction'], 'Restore nose')

    def test_unknown_missing_and_unsupported_pass_are_blocked(self):
        for checks in ([], [{'id': 'shape', 'status': 'unknown'}],
                       [{'id': 'shape', 'status': 'pass', 'evidence': ''}]):
            self.review['checks'] = checks
            self.assertFalse(self.result()['approved'])

    def test_modified_image_and_contract_require_new_review(self):
        self.image.write_bytes(b'image-version-two')
        self.assertFalse(self.result()['approved'])
        self.contract['criteria'][0]['requirement'] = 'Different arc'
        self.assertIn('review does not match the frozen contract', self.result()['issues'])

    def test_duplicates_and_structural_failure_block(self):
        self.review['checks'].append(self.review['checks'][0])
        self.review['structuralQa']['status'] = 'fail'
        self.assertFalse(self.result()['approved'])

    def test_invalid_weight_rejected(self):
        self.contract['criteria'][0]['weight'] = float('nan')
        with self.assertRaises(ValueError):
            self.result()


if __name__ == '__main__':
    unittest.main()
