"""
Unit Tests for Module 1 (Telemetry) and Module 2 (Diagnostic Reasoning Graph API).
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m1_collection import MetricSignal, AlertSignal, TelemetryReceiver
from modules.m2_graph import DiagnosticGraph, create_payment_seed_graph
from fastapi.testclient import TestClient
from modules.api import app


class TestModules1And2(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_module1_telemetry_receiver(self):
        receiver = TelemetryReceiver()
        metrics = [
            MetricSignal(service_id="payment-db", metric_name="connection_pool_usage", value=0.95, baseline=0.15),
            MetricSignal(service_id="payment-api", metric_name="error_rate", value=0.01, baseline=0.01)
        ]
        anomalous_count = receiver.ingest_metrics(metrics)
        self.assertEqual(anomalous_count, 1)

        anomalies = receiver.get_active_anomalies()
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0].service_id, "payment-db")

    def test_module2_diagnostic_graph(self):
        dg = create_payment_seed_graph()
        self.assertTrue(dg.is_dag())
        self.assertGreaterEqual(len(dg.graph.nodes), 8)

        # Test Graph serialization
        graph_dict = dg.to_dict()
        self.assertIn("version_id", graph_dict)
        self.assertIn("nodes", graph_dict)
        self.assertIn("edges", graph_dict)

        # Test Deserialization
        reconstructed = DiagnosticGraph.from_dict(graph_dict)
        self.assertTrue(reconstructed.is_dag())
        self.assertEqual(len(reconstructed.graph.nodes), len(dg.graph.nodes))

    def test_fastapi_endpoints(self):
        # 1. Test Root
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("graph_version", response.json())

        # 2. Test Get Latest Graph
        response = self.client.get("/graph/latest")
        self.assertEqual(response.status_code, 200)
        self.assertIn("nodes", response.json())

        # 3. Test Ingest Metrics
        payload = [
            {"service_id": "payment-api", "metric_name": "error_rate", "value": 0.45, "baseline": 0.01}
        ]
        response = self.client.post("/telemetry/metrics", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["anomalous"], 1)

        # 4. Test Reset Seed Graph
        response = self.client.get("/graph/seed")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")


if __name__ == "__main__":
    unittest.main()
