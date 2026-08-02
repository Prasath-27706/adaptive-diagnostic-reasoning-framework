"""
Unit Tests for Module 5: Evolution Decision Engine (CORE NOVELTY).
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m2_graph import create_payment_seed_graph, DiagnosticGraph
from modules.m5_decision_engine import apply_remove_mutation, apply_reorder_mutation, MultiObjectiveScorer, EvolutionEngine
from fastapi.testclient import TestClient
from modules.api import app


class TestModule5(unittest.TestCase):

    def setUp(self):
        self.seed_graph = create_payment_seed_graph()
        self.scorer = MultiObjectiveScorer()
        self.engine = EvolutionEngine(self.scorer)
        self.client = TestClient(app)

    def test_mutations(self):
        # 1. Test REMOVE mutation
        mutated_remove = apply_remove_mutation(self.seed_graph, "check:frontend:cpu_utilization")
        self.assertTrue(mutated_remove.is_dag())
        self.assertNotIn("check:frontend:cpu_utilization", mutated_remove.graph.nodes)
        self.assertLess(len(mutated_remove.graph.nodes), len(self.seed_graph.graph.nodes))

        # 2. Test REORDER mutation
        mutated_reorder = apply_reorder_mutation(self.seed_graph, "check:payment-db:connection_pool", new_priority=2.5)
        self.assertTrue(mutated_reorder.is_dag())

    def test_multi_objective_scorer(self):
        exp_record = {"redundant_nodes": ["check:frontend:cpu_utilization"], "high_value_nodes": ["check:payment-db:connection_pool"]}
        score_res = self.scorer.score_candidate(self.seed_graph, exp_record)
        self.assertIn("score", score_res)
        self.assertGreater(score_res["score"], 0.0)

    def test_evolution_engine(self):
        exp_record = {
            "redundant_nodes": ["check:frontend:cpu_utilization", "check:network:packet_loss"],
            "high_value_nodes": ["check:payment-db:connection_pool"]
        }

        result = self.engine.evolve_graph(self.seed_graph, exp_record)

        self.assertIn("selected_graph", result)
        self.assertIn("selected_transformation", result)
        self.assertGreater(len(result["all_candidates"]), 1)

    def test_evolve_rest_endpoint(self):
        exp_payload = {
            "redundant_nodes": ["check:frontend:cpu_utilization"],
            "high_value_nodes": ["check:payment-db:connection_pool"]
        }

        response = self.client.post("/evolve", json=exp_payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("selected_transformation", data)
        self.assertIn("best_score", data)


if __name__ == "__main__":
    unittest.main()
