"""
Evolution Decision Engine Module (Module 5 ★ CORE NOVELTY).
Orchestrates candidate generation, multi-objective scoring, and selects optimal mutated graphs.
"""

from typing import Dict, List, Any, Tuple
from modules.m2_graph import DiagnosticGraph
from .mutations import apply_remove_mutation, apply_reorder_mutation, apply_add_mutation
from .scorer import MultiObjectiveScorer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("m5_decision_engine")


class EvolutionEngine:
    """
    Core Evolution Decision Engine selecting structural transformations on reasoning graphs.
    """

    def __init__(self, scorer: MultiObjectiveScorer = None):
        self.scorer = scorer or MultiObjectiveScorer()

    def evolve_graph(
        self,
        current_graph: DiagnosticGraph,
        experience_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates candidate mutated graphs, scores them via multi-objective optimization, and selects top-1.
        """
        candidates: List[Tuple[DiagnosticGraph, str, Dict[str, Any]]] = []

        # 1. Base Score of Unmodified Graph
        base_score_info = self.scorer.score_candidate(current_graph, experience_record)
        candidates.append((current_graph, "NO_CHANGE", base_score_info))

        redundant_nodes = experience_record.get("redundant_nodes", [])
        high_value_nodes = experience_record.get("high_value_nodes", [])

        # 2. Generate REMOVE Candidate Mutations
        for red_node in redundant_nodes:
            if current_graph.graph.has_node(red_node):
                mutated_graph = apply_remove_mutation(current_graph, red_node)
                score_info = self.scorer.score_candidate(mutated_graph, experience_record)
                candidates.append((mutated_graph, f"REMOVE:{red_node}", score_info))

        # 3. Generate REORDER Candidate Mutations
        for hv_node in high_value_nodes:
            if current_graph.graph.has_node(hv_node):
                mutated_graph = apply_reorder_mutation(current_graph, hv_node, new_priority=2.5)
                score_info = self.scorer.score_candidate(mutated_graph, experience_record)
                candidates.append((mutated_graph, f"REORDER:{hv_node}", score_info))

        # 4. Generate ADD Candidate Mutations (Deep Scenario-Specific Diagnostic Probes)
        suggested_additions = experience_record.get("suggested_additions", [])
        for add_spec in suggested_additions:
            node_id = add_spec["node_id"]
            if not current_graph.graph.has_node(node_id):
                parent_id = add_spec.get("parent_id", "entry:payment-api:error_rate")
                mutated_graph = apply_add_mutation(
                    current_graph,
                    node_id=node_id,
                    label=add_spec.get("label", node_id),
                    node_type=add_spec.get("node_type", "check"),
                    target_service=add_spec.get("target_service", "unknown"),
                    target_metric=add_spec.get("target_metric", "unknown"),
                    parent_id=parent_id
                )
                score_info = self.scorer.score_candidate(mutated_graph, experience_record)
                candidates.append((mutated_graph, f"ADD:{node_id}", score_info))

        # Sort candidates by score descending

        sorted_candidates = sorted(candidates, key=lambda x: x[2]["score"], reverse=True)
        top_graph, top_action, top_score_info = sorted_candidates[0]

        candidate_logs = []
        for g, act, score in sorted_candidates:
            candidate_logs.append({
                "version_id": g.version_id,
                "transformation": act,
                "score": score["score"],
                "details": score["details"]
            })

        logger.info(f"Evolution complete: Selected '{top_action}' with score {top_score_info['score']} (Version: {top_graph.version_id})")

        return {
            "selected_graph": top_graph.to_dict(),
            "selected_version_id": top_graph.version_id,
            "selected_transformation": top_action,
            "best_score": top_score_info["score"],
            "score_details": top_score_info["details"],
            "all_candidates": candidate_logs
        }
