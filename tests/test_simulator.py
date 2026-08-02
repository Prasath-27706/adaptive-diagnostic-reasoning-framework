"""
Unit and Integration Tests for Synthetic Incident Simulator.
"""

import unittest
import os
import tempfile
import json
import networkx as nx

from simulator.topology_generator import TopologyGenerator
from simulator.fault_injector import FaultInjector
from simulator.trace_recorder import TraceRecorder
from simulator.dataset_exporter import DatasetExporter
from simulator.incident_simulator import IncidentSimulator


class TestSimulator(unittest.TestCase):

    def test_topology_generator(self):
        gen = TopologyGenerator(service_count=10, seed=42)
        graph = gen.generate()

        self.assertIsInstance(graph, nx.DiGraph)
        self.assertGreaterEqual(len(graph.nodes), 8)
        self.assertTrue(nx.is_directed_acyclic_graph(graph))

        top_dict = gen.to_dict()
        self.assertIn("nodes", top_dict)
        self.assertIn("edges", top_dict)
        self.assertEqual(len(top_dict["nodes"]), len(graph.nodes))

    def test_fault_injector(self):
        gen = TopologyGenerator(service_count=10, seed=42)
        graph = gen.generate()

        injector = FaultInjector(seed=42)
        root_cause, symptoms = injector.inject_fault(graph)

        self.assertIn("service", root_cause)
        self.assertIn("fault_type", root_cause)
        self.assertGreaterEqual(len(symptoms), 1)
        self.assertEqual(symptoms[0]["service"], root_cause["service"])

    def test_trace_recorder(self):
        recorder = TraceRecorder(seed=42)
        root_cause = {"service": "payment-db", "metric": "connection_pool_usage", "fault_type": "connection_pool_exhausted"}
        symptoms = [{"service": "payment-api", "metric": "error_rate", "value": 0.5, "baseline": 0.01}]

        opt_path, subopt_paths, mttr = recorder.record_paths(root_cause, symptoms)

        self.assertEqual(len(opt_path), 3)
        self.assertEqual(len(subopt_paths), 1)
        self.assertGreater(len(subopt_paths[0]), len(opt_path))
        self.assertGreater(mttr, 120)

    def test_dataset_exporter_and_simulator(self):
        sim = IncidentSimulator(service_count=8, seed=123)
        incidents = sim.generate_incidents(count=5)

        self.assertEqual(len(incidents), 5)
        for inc in incidents:
            self.assertTrue(DatasetExporter.validate_incident(inc))

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            sim.generate_and_export(count=5, output_path=tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0]["incident_id"], "INC-PAY-00001")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
