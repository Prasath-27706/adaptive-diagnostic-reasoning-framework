"""
Integration Tests for Phase 8 Pipeline Orchestrator.
"""

import unittest
import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from run_demo import run_benchmark


class TestPhase8Pipeline(unittest.TestCase):

    def setUp(self):
        self.tmp_output = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name

    def tearDown(self):
        if os.path.exists(self.tmp_output):
            os.remove(self.tmp_output)

    def test_pipeline_benchmark_execution(self):
        # Run small 20-incident benchmark with batch size 5
        summary = run_benchmark(
            incidents_count=20,
            batch_size=5,
            seed=42,
            output_path=self.tmp_output
        )

        self.assertIsNotNone(summary)
        self.assertEqual(summary["total_incidents"], 20)
        self.assertIn("initial_mttr_s", summary)
        self.assertIn("final_mttr_s", summary)

        # Check output JSON file existence & readability
        self.assertTrue(os.path.exists(self.tmp_output))
        with open(self.tmp_output, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["total_incidents"], 20)


if __name__ == "__main__":
    unittest.main()
