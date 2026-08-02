"""
Unit Tests for Module 3: Incident Analyzer.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m2_graph import create_payment_seed_graph
from modules.m3_analyzer import IncidentAnalyzer
from fastapi.testclient import TestClient
from modules.api import app


class TestModule3(unittest.TestCase):

    def setUp(self):
        self.graph = create_payment_seed_graph()
        self.analyzer = IncidentAnalyzer()
        self.client = TestClient(app)

    def test_incident_analyzer_traversal(self):
        sample_incident = {
            "incident_id": "INC-TEST-001",
            "root_cause": {
                "service": "payment-db",
                "metric": "connection_pool_usage",
                "fault_type": "connection_pool_exhausted"
            },
            "symptoms": [
                {"service": "payment-api", "metric": "error_rate", "value": 0.45, "baseline": 0.01},
                {"service": "payment-db", "metric": "connection_pool_usage", "value": 0.99, "baseline": 0.15}
            ]
        }

        result = self.analyzer.analyze_incident(self.graph, sample_incident)

        self.assertEqual(result["incident_id"], "INC-TEST-001")
        self.assertIn("root_cause", result)
        self.assertEqual(result["root_cause"]["service"], "payment-db")
        self.assertGreaterEqual(len(result["decision_trace"]), 3)

        # Check Decision Trace fields
        trace_step = result["decision_trace"][0]
        self.assertIn("step", trace_step)
        self.assertIn("node_id", trace_step)
        self.assertIn("result", trace_step)
        self.assertIn("info_gain", trace_step)

    def test_analyze_rest_endpoint(self):
        payload = {
            "incident_id": "INC-API-TEST",
            "root_cause": {
                "service": "auth-svc",
                "metric": "token_validation_latency",
                "fault_type": "auth_token_timeout"
            },
            "symptoms": [
                {"service": "payment-api", "metric": "error_rate", "value": 0.5, "baseline": 0.01},
                {"service": "auth-svc", "metric": "token_validation_latency", "value": 4800, "baseline": 80}
            ]
        }

        response = self.client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["incident_id"], "INC-API-TEST")
        self.assertEqual(data["root_cause"]["service"], "auth-svc")
        self.assertGreater(data["mttr_s"], 0)


if __name__ == "__main__":
    unittest.main()
