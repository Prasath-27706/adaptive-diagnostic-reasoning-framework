"""
Performance Verifier for Module 6.
Replays historical incidents against current vs candidate graphs and asserts MTTR non-regression.
"""

from typing import Dict, List, Any
from modules.m2_graph import DiagnosticGraph
from modules.m3_analyzer import IncidentAnalyzer


class PerformanceVerifier:
    """
    Replays incidents to verify that candidate graph mutations reduce MTTR and do not cause regressions.
    """

    def __init__(self, max_regression_pct: float = 10.0):
        self.max_regression_factor = 1.0 + (max_regression_pct / 100.0)
        self.analyzer = IncidentAnalyzer()

    def verify_performance(
        self,
        current_graph: DiagnosticGraph,
        candidate_graph: DiagnosticGraph,
        historical_incidents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Replays historical incidents and compares average MTTR.
        """
        if not historical_incidents:
            # If no historical incidents supplied, default to passing
            return {
                "passed": True,
                "mttr_current_s": 0.0,
                "mttr_candidate_s": 0.0,
                "mttr_delta_s": 0.0,
                "pct_change": 0.0,
                "message": "No historical incidents provided for replay verification."
            }

        mttr_current_list = []
        mttr_cand_list = []

        for inc in historical_incidents:
            res_curr = self.analyzer.analyze_incident(current_graph, inc)
            res_cand = self.analyzer.analyze_incident(candidate_graph, inc)
            mttr_current_list.append(res_curr["mttr_s"])
            mttr_cand_list.append(res_cand["mttr_s"])

        avg_curr = sum(mttr_current_list) / len(mttr_current_list)
        avg_cand = sum(mttr_cand_list) / len(mttr_cand_list)

        mttr_delta = avg_cand - avg_curr
        pct_change = round((mttr_delta / max(1.0, avg_curr)) * 100, 2)

        # Candidate passes if avg_cand <= avg_curr * max_regression_factor
        passed = avg_cand <= (avg_curr * self.max_regression_factor)

        return {
            "passed": passed,
            "mttr_current_s": round(avg_curr, 2),
            "mttr_candidate_s": round(avg_cand, 2),
            "mttr_delta_s": round(mttr_delta, 2),
            "pct_change": pct_change,
            "message": "Performance verification passed." if passed else f"Performance verification failed: Candidate increased MTTR by {pct_change}% (exceeds threshold)."
        }
