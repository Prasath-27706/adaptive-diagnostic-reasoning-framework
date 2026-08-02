"""
Unit Tests for Module 7: Operational Knowledge Repository.
"""

import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m2_graph import create_payment_seed_graph
from modules.m7_repository import KnowledgeRepository
from fastapi.testclient import TestClient
from modules.api import app


class TestModule7(unittest.TestCase):

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
        self.repo = KnowledgeRepository(db_path=self.tmp_file)
        self.seed_graph = create_payment_seed_graph()
        self.client = TestClient(app)

    def tearDown(self):
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)

    def test_repository_save_and_retrieve(self):
        v_id = self.repo.save_graph_version(self.seed_graph, "INITIAL_TEST", 0.75, "APPROVED")
        self.assertEqual(v_id, self.seed_graph.version_id)

        retrieved = self.repo.get_graph_version(v_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["node_count"], len(self.seed_graph.graph.nodes))

        history = self.repo.get_transformation_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["transformation_type"], "INITIAL_TEST")

    def test_repository_mttr_logging(self):
        self.repo.log_mttr_point(self.seed_graph.version_id, 88.5)
        mttr_history = self.repo.get_mttr_history()
        self.assertEqual(len(mttr_history), 1)
        self.assertEqual(mttr_history[0]["mttr_s"], 88.5)

    def test_repository_rest_endpoints(self):
        response = self.client.get("/repository/graphs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("versions", response.json())

        response = self.client.get("/repository/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn("history", response.json())

        response = self.client.get("/repository/mttr")
        self.assertEqual(response.status_code, 200)
        self.assertIn("mttr_points", response.json())


if __name__ == "__main__":
    unittest.main()
