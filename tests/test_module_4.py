"""
Unit Tests for Module 4: Experience Extractor.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m4_extractor import compute_shannon_entropy, calculate_empirical_info_gain, ExperienceExtractor
from fastapi.testclient import TestClient
from modules.api import app


class TestModule4(unittest.TestCase):

    def setUp(self):
        self.extractor = ExperienceExtractor()
        self.client = TestClient(app)

    def test_entropy_math(self):
        # Equal probabilities (highest uncertainty)
        h = compute_shannon_entropy([0.5, 0.5])
        self.assertEqual(h, 1.0)

        # Single outcome (zero uncertainty)
        h_zero = compute_shannon_entropy([1.0, 0.0])
        self.assertEqual(h_zero, 0.0)

    def test_experience_extraction_logic(self):
        sample_traces = [
            [
                {"node_id": "check:frontend:cpu", "result": "normal", "info_gain": 0.0, "time_taken_s": 4},
                {"node_id": "check:payment-db:pool", "result": "anomaly", "info_gain": 0.88, "time_taken_s": 3}
            ],
            [
                {"node_id": "check:frontend:cpu", "result": "normal", "info_gain": 0.0, "time_taken_s": 4},
                {"node_id": "check:payment-db:pool", "result": "anomaly", "info_gain": 0.88, "time_taken_s": 3}
            ]
        ]

        record = self.extractor.extract_experience(sample_traces)

        self.assertEqual(record["total_incidents_analyzed"], 2)
        self.assertIn("check:frontend:cpu", record["redundant_nodes"])
        self.assertIn("check:payment-db:pool", record["high_value_nodes"])

    def test_extract_rest_endpoint(self):
        traces_payload = [
            [
                {"node_id": "check:network:loss", "result": "normal", "info_gain": 0.0, "time_taken_s": 5},
                {"node_id": "check:auth-svc:token", "result": "anomaly", "info_gain": 0.75, "time_taken_s": 4}
            ]
        ]

        response = self.client.post("/experience/extract", json=traces_payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["total_incidents_analyzed"], 1)
        self.assertIn("check:network:loss", data["redundant_nodes"])


if __name__ == "__main__":
    unittest.main()
