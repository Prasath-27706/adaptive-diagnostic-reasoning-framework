"""
Unit Tests for Module 6: Graph Verification Engine.
"""

import unittest
import os
import sys
import copy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m2_graph import create_payment_seed_graph, DiagnosticGraph
from modules.m6_verification import StructuralVerifier, PerformanceVerifier, GraphVerifier
from fastapi.testclient import TestClient
from modules.api import app


class TestModule6(unittest.TestCase):

    def setUp(self):
        self.seed_graph = create_payment_seed_graph()
        self.struct_verifier = StructuralVerifier()
        self.perf_verifier = PerformanceVerifier()
        self.verifier = GraphVerifier()
        self.client = TestClient(app)

    def test_structural_verification_valid_dag(self):
        res = self.struct_verifier.verify_structure(self.seed_graph)
        self.assertTrue(res["passed"])
        self.assertTrue(res["is_dag"])
        self.assertTrue(res["all_reachable"])

    def test_structural_verification_rejects_cycle(self):
        # Create a cyclic graph
        cyclic_graph = copy.deepcopy(self.seed_graph)
        cyclic_graph.add_decision_edge("check:payment-db:connection_pool", "entry:payment-api:error_rate")

        res = self.struct_verifier.verify_structure(cyclic_graph)
        self.assertFalse(res["passed"])
        self.assertFalse(res["is_dag"])

    def test_performance_verification(self):
        incidents = [
            {
                "incident_id": "INC-TEST-001",
                "root_cause": {"service": "payment-db", "metric": "connection_pool_usage"},
                "symptoms": [{"service": "payment-db", "metric": "connection_pool_usage", "value": 0.99, "baseline": 0.15}]
            }
        ]

        # Valid candidate (same or evolved)
        res = self.perf_verifier.verify_performance(self.seed_graph, self.seed_graph, incidents)
        self.assertTrue(res["passed"])
        self.assertEqual(res["pct_change"], 0.0)

    def test_verify_rest_endpoint(self):
        payload = {
            "candidate_graph": self.seed_graph.to_dict(),
            "historical_incidents": []
        }

        response = self.client.post("/verify", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "APPROVED")


if __name__ == "__main__":
    unittest.main()
