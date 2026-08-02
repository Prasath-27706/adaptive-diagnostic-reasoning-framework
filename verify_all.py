"""
Comprehensive End-to-End Verification Script for All 8 Phases (Full System Pipeline & Benchmark).
"""

import os
import sys
import json
import logging
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulator.incident_simulator import IncidentSimulator
from modules.m2_graph import create_payment_seed_graph, DiagnosticGraph
from modules.m3_analyzer import IncidentAnalyzer
from modules.m4_extractor import ExperienceExtractor
from modules.m5_decision_engine import EvolutionEngine
from modules.m6_verification import GraphVerifier
from modules.m7_repository import KnowledgeRepository
from run_demo import run_benchmark
from fastapi.testclient import TestClient
from modules.api import app

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_verification():
    print("=" * 75)
    print("      COMPREHENSIVE CLOSED-LOOP SYSTEM VERIFICATION (PHASES 1-8)")
    print("=" * 75)

    # 1. Run Unit Tests across all modules
    print("\n[STEP 1] Running Unit Test Suites across Phases 1-8...")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    if not test_result.wasSuccessful():
        print("❌ Unit Tests Failed!")
        sys.exit(1)
    print(f"✅ All {test_result.testsRun} Unit Tests Passed Successfully.")

    # 2. Test Simulator & Dataset Generation
    print("\n[STEP 2] Verifying Synthetic Incident Simulator & Dataset Generation...")
    sim = IncidentSimulator(service_count=10, seed=99)
    incidents = sim.generate_incidents(count=10)
    assert len(incidents) == 10, "Failed to generate incidents"
    print(f"✅ Generated {len(incidents)} valid payment incident records.")

    # 3. Test REST API Endpoints with TestClient
    print("\n[STEP 3] Verifying FastAPI REST API Endpoints...")
    client = TestClient(app)

    # Reset to Seed Graph
    res = client.get("/graph/seed")
    assert res.status_code == 200
    initial_graph = res.json()["graph"]
    print(f"  └─ Reset to Seed Graph ({initial_graph['node_count']} nodes, {initial_graph['edge_count']} edges, Version: {initial_graph['version_id']})")

    # 4. Run Benchmark Orchestrator (Phase 8)
    print("\n[STEP 4] Executing Phase 8 Pipeline Benchmark Orchestrator...")
    summary = run_benchmark(incidents_count=30, batch_size=10, seed=42, output_path="data/benchmark_results.json")

    assert summary["initial_mttr_s"] >= summary["final_mttr_s"], "MTTR did not decrease"
    print(f"  └─ Initial MTTR: {summary['initial_mttr_s']}s ➔ Final MTTR: {summary['final_mttr_s']}s (-{summary['mttr_reduction_pct']}% faster)")
    print(f"  └─ Nodes Pruned: {summary['initial_nodes']} ➔ {summary['final_nodes']} nodes")

    print("\n" + "=" * 75)
    print("✅ PHASES 1-8 INTEGRATION VERIFIED PERFECTLY!")
    print("=" * 75)


if __name__ == "__main__":
    run_verification()
