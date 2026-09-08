"""Run the public example verifier against isolated, mutated planning fixtures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/local-first"


class LocalFirstTests(unittest.TestCase):
    def check(self, mutation=None, valid=False):
        for optimized in (False, True):
            with self.subTest(optimized=optimized), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / "example"
                shutil.copytree(EXAMPLE, root)
                if mutation:
                    mutation(root)
                result = subprocess.run([sys.executable, *(["-O"] if optimized else []),
                                         str(root / "verify.py")], capture_output=True, text=True)
                if valid:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("PASS:", result.stdout)
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn("PASS:", result.stdout)

    def mutate(self, filename, change):
        def edit(root):
            path = root / filename
            value = json.loads(path.read_text())
            change(value)
            path.write_text(json.dumps(value))
        self.check(edit)

    def test_public_example(self):
        self.check(valid=True)

    def test_missing_source(self):
        self.mutate("source-ledger.json", lambda v: v["sources"].pop())

    def test_evidence_without_source(self):
        self.mutate("visual-plan.json", lambda v: v["shots"][2].update(source_ids=[]))

    def test_duplicate_source_id(self):
        self.mutate("source-ledger.json", lambda v: v["sources"].append(v["sources"][0]))

    def test_missing_source_url(self):
        self.mutate("source-ledger.json", lambda v: v["sources"][0].pop("url"))

    def test_unknown_copy(self):
        self.mutate("visual-plan.json", lambda v: v["shots"][0].update(copy_ids=["missing"]))

    def test_duplicate_shot(self):
        self.mutate("visual-plan.json", lambda v: v["shots"][1].update(id="shot-01"))

    def test_missing_paragraph_coverage(self):
        self.mutate("visual-plan.json", lambda v: v["shots"][0].update(paragraph=2))

    def test_boolean_paragraph(self):
        self.mutate("visual-plan.json", lambda v: v["shots"][0].update(paragraph=True))

    def test_wrong_timing_state(self):
        self.mutate("visual-plan.json", lambda v: v.update(timing_state="rendered"))

    def test_premature_shot_times(self):
        self.mutate("visual-plan.json", lambda v: v["shots"][0].update(start=0, end=10))

    def test_wrong_production_stage(self):
        self.check(lambda root: (root / "production-status.md").write_text(
            "# Public example status\n\n- Stage: rendered\n"))

    def test_missing_production_status(self):
        self.check(lambda root: (root / "production-status.md").unlink())
