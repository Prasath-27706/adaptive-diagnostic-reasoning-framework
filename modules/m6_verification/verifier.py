"""
Graph Verifier Orchestrator for Module 6.
Combines Structural & Performance verification gates.
"""

from typing import Dict, List, Any, Optional
from modules.m2_graph import DiagnosticGraph
from .structural_verifier import StructuralVerifier
from .performance_verifier import PerformanceVerifier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("m6_verification")


class GraphVerifier:
    """
    Formal Safety Gate for Graph Mutations.
    """

    def __init__(self, max_regression_pct: float = 10.0):
        self.structural_verifier = StructuralVerifier()
        self.performance_verifier = PerformanceVerifier(max_regression_pct=max_regression_pct)

    def verify_candidate_graph(
        self,
        current_graph: DiagnosticGraph,
        candidate_graph: DiagnosticGraph,
        historical_incidents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executes structural and performance verification on candidate graph.
        Returns: Dict with status ('APPROVED' / 'REJECTED') and details.
        """
        # 1. Structural Check
        struct_res = self.structural_verifier.verify_structure(candidate_graph)

        # 2. Performance Check
        perf_res = self.performance_verifier.verify_performance(
            current_graph=current_graph,
            candidate_graph=candidate_graph,
            historical_incidents=historical_incidents or []
        )

        passed_both = struct_res["passed"] and perf_res["passed"]
        status = "APPROVED" if passed_both else "REJECTED"

        rejection_reasons = []
        if not struct_res["is_dag"]:
            rejection_reasons.append("Structural Error: Graph contains cycles (not a DAG).")
        if not struct_res["all_reachable"]:
            rejection_reasons.append(f"Structural Error: Orphan unreachable nodes {struct_res['orphan_nodes']}.")
        if not perf_res["passed"]:
            rejection_reasons.append(perf_res["message"])

        logger.info(f"Verification completed for candidate {candidate_graph.version_id}: {status}")

        return {
            "status": status,
            "candidate_version_id": candidate_graph.version_id,
            "structural_verification": struct_res,
            "performance_verification": perf_res,
            "rejection_reasons": rejection_reasons
        }
