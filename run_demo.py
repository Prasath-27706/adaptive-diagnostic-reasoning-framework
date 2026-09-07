#!/usr/bin/env python3
"""
Full Pipeline Benchmark Orchestrator Script for Adaptive Diagnostic Reasoning Framework (Phase 8).
Executes closed-loop incident analysis, experience extraction, graph mutation evolution, and verification across N incidents.
Usage:
    python3 run_demo.py --incidents 50 --batch-size 10 --seed 42 --output data/benchmark_results.json
"""

import argparse
import sys
import os
import json
import logging
from typing import Optional
from datetime import datetime, timezone

# Add root path to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulator.incident_simulator import IncidentSimulator
from modules.m2_graph import create_payment_seed_graph, DiagnosticGraph
from modules.m3_analyzer import IncidentAnalyzer
from modules.m4_extractor import ExperienceExtractor
from modules.m5_decision_engine import EvolutionEngine
from modules.m6_verification import GraphVerifier
from modules.m7_repository import KnowledgeRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_benchmark(incidents_count: int = 50, batch_size: int = 10, seed: int = 42, output_path: str = "data/benchmark_results.json", mode: str = "synthetic", floci_endpoint: Optional[str] = None):
    print("=" * 75)
    print(f"      CLOSED-LOOP GRAPH EVOLUTION BENCHMARK DEMO (PHASE 8) [{mode.upper()}]")
    print("=" * 75)

    # Initialize Simulator & Framework Modules
    simulator = IncidentSimulator(service_count=10, seed=seed)
    current_graph = create_payment_seed_graph()
    analyzer = IncidentAnalyzer()
    extractor = ExperienceExtractor()
    evolution_engine = EvolutionEngine()
    verifier = GraphVerifier()
    repository = KnowledgeRepository()

    initial_version_id = current_graph.version_id
    initial_node_count = len(current_graph.graph.nodes)
    repository.save_graph_version(current_graph, "BENCHMARK_SEED", 0.5, "APPROVED")

    print(f"\n[INIT] Starting Benchmark Run:")
    print(f"  └─ Target Incidents: {incidents_count}")
    print(f"  └─ Batch Evolution Interval: Every {batch_size} incidents")
    print(f"  └─ Initial Graph: Version '{initial_version_id}' ({initial_node_count} nodes)")

    # Generate incident pool (synthetic or Floci-backed)
    all_incidents = simulator.generate_incidents(count=incidents_count, mode=mode, floci_endpoint=floci_endpoint)

    batch_mttrs = []
    evolution_logs = []
    incident_traces_buffer = []
    initial_batch_mttr = 0.0

    num_batches = (incidents_count + batch_size - 1) // batch_size

    for b_idx in range(num_batches):
        batch_start = b_idx * batch_size
        batch_end = min(incidents_count, batch_start + batch_size)
        batch_incidents = all_incidents[batch_start:batch_end]

        batch_mttr_list = []
        for inc in batch_incidents:
            analysis = analyzer.analyze_incident(current_graph, inc)
            batch_mttr_list.append(analysis["mttr_s"])
            incident_traces_buffer.append(analysis["decision_trace"])
            repository.log_mttr_point(current_graph.version_id, analysis["mttr_s"])

        avg_batch_mttr = sum(batch_mttr_list) / len(batch_mttr_list)
        batch_mttrs.append(avg_batch_mttr)

        if b_idx == 0:
            initial_batch_mttr = avg_batch_mttr

        print(f"\n[BATCH {b_idx+1}/{num_batches}] Analyzed incidents {batch_start+1}–{batch_end} | Graph: '{current_graph.version_id}' | Avg MTTR: {avg_batch_mttr:.1f}s")

        # Execute Closed-Loop Evolution Cycle
        exp_record = extractor.extract_experience(incident_traces_buffer)
        evo_result = evolution_engine.evolve_graph(current_graph, exp_record)
        candidate_graph_dict = evo_result["selected_graph"]

        if evo_result["selected_transformation"] != "NO_CHANGE":
            candidate_graph = DiagnosticGraph.from_dict(candidate_graph_dict)
            verify_report = verifier.verify_candidate_graph(
                current_graph=current_graph,
                candidate_graph=candidate_graph,
                historical_incidents=batch_incidents
            )

            if verify_report["status"] == "APPROVED":
                current_graph = candidate_graph
                repository.save_graph_version(
                    graph=current_graph,
                    transformation_type=evo_result["selected_transformation"],
                    score=evo_result["best_score"],
                    verification_status="APPROVED"
                )
                print(f"  └─ ⚡ EVOLVED & VERIFIED: Applied '{evo_result['selected_transformation']}' ➔ Graph Version '{current_graph.version_id}' ({len(current_graph.graph.nodes)} nodes)")
                evolution_logs.append({
                    "batch": b_idx + 1,
                    "transformation": evo_result["selected_transformation"],
                    "version_id": current_graph.version_id,
                    "score": evo_result["best_score"],
                    "verification": "APPROVED"
                })
            else:
                print(f"  └─ ⚠️ REJECTED: Candidate mutation rejected by verification gate.")
        else:
            print(f"  └─ Graph optimal (no further mutations selected).")

    final_batch_mttr = batch_mttrs[-1]
    total_mttr_reduction = initial_batch_mttr - final_batch_mttr
    pct_mttr_reduction = (total_mttr_reduction / max(1.0, initial_batch_mttr)) * 100
    final_node_count = len(current_graph.graph.nodes)

    print("\n" + "=" * 75)
    print("                     FINAL BENCHMARK SUMMARY RESULTS")
    print("=" * 75)
    print(f"  Initial Baseline MTTR (Batch 1) : {initial_batch_mttr:.1f} seconds")
    print(f"  Final Evolved MTTR (Batch {num_batches})   : {final_batch_mttr:.1f} seconds")
    print(f"  Total MTTR Reduction            : -{total_mttr_reduction:.1f}s ({pct_mttr_reduction:.1f}% FASTER)")
    print(f"  Initial Graph Size              : {initial_node_count} nodes")
    print(f"  Final Graph Size                : {final_node_count} nodes (pruned redundant steps)")
    print(f"  Total Approved Mutations Applied: {len(evolution_logs)}")
    print("=" * 75)

    benchmark_summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_incidents": incidents_count,
        "batch_size": batch_size,
        "mode": mode,
        "initial_mttr_s": round(initial_batch_mttr, 2),
        "final_mttr_s": round(final_batch_mttr, 2),
        "mttr_reduction_s": round(total_mttr_reduction, 2),
        "mttr_reduction_pct": round(pct_mttr_reduction, 2),
        "initial_nodes": initial_node_count,
        "final_nodes": final_node_count,
        "approved_mutations_count": len(evolution_logs),
        "evolution_logs": evolution_logs,
        "batch_mttr_history": batch_mttrs
    }

    # Save summary JSON
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_summary, f, indent=2)

    print(f"\n✅ Benchmark results exported to '{output_path}'.")
    return benchmark_summary


def main():
    parser = argparse.ArgumentParser(description="Full Pipeline Closed-Loop Evolution Benchmark Orchestrator")
    parser.add_argument("--incidents", type=int, default=50, help="Number of incidents to process (default: 50)")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size between evolution cycles (default: 10)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--output", type=str, default="data/benchmark_results.json", help="Output JSON benchmark path")
    parser.add_argument("--floci", action="store_true", help="Use Floci-backed real AWS emulation (requires docker compose up floci)")
    parser.add_argument("--floci-endpoint", type=str, default=None, help="Floci endpoint URL (default: http://localhost:4566 or $AWS_ENDPOINT_URL)")

    args = parser.parse_args()
    mode = "floci" if args.floci else "synthetic"
    run_benchmark(
        incidents_count=args.incidents,
        batch_size=args.batch_size,
        seed=args.seed,
        output_path=args.output,
        mode=mode,
        floci_endpoint=args.floci_endpoint,
    )


if __name__ == "__main__":
    main()
