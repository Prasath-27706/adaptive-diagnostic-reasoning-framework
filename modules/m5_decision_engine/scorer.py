"""
Multi-Objective Scorer for Module 5.
Scores candidate mutated diagnostic graphs using information gain, duration, confidence, and graph complexity.
"""

from typing import Dict, Any
from modules.m2_graph import DiagnosticGraph


class MultiObjectiveScorer:
    """
    Multi-objective scoring function for evaluating candidate graph transformations.
    Score = w1*IG + w2*(1/Time) + w3*Confidence + w4*History - w5*Complexity
    """

    def __init__(
        self,
        w1_ig: float = 0.30,
        w2_time: float = 0.20,
        w3_confidence: float = 0.20,
        w4_history: float = 0.20,
        w5_complexity: float = 0.10
    ):
        self.w1 = w1_ig
        self.w2 = w2_time
        self.w3 = w3_confidence
        self.w4 = w4_history
        self.w5 = w5_complexity

    def score_candidate(self, graph: DiagnosticGraph, experience_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the multi-objective fitness score for a candidate DiagnosticGraph.
        """
        nodes = graph.graph.nodes(data=True)
        node_count = len(nodes)
        edge_count = len(graph.graph.edges)

        if node_count == 0:
            return {"score": 0.0, "details": {}}

        total_ig = 0.0
        total_time_s = 0
        total_confidence = 0.0
        total_history = 0.0

        for n, data in nodes:
            total_ig += data.get("info_gain", 0.0)
            total_time_s += data.get("avg_duration_s", 3)
            total_confidence += data.get("historical_success_rate", 0.7)
            total_history += data.get("historical_success_rate", 0.7)

        avg_ig = total_ig / node_count
        avg_dur = total_time_s / node_count
        avg_conf = total_confidence / node_count
        avg_hist = total_history / node_count

        # Normalize metrics
        ig_norm = min(1.0, avg_ig / 1.0)
        time_norm = min(1.0, 10.0 / max(1.0, avg_dur))
        conf_norm = min(1.0, avg_conf)
        hist_norm = min(1.0, avg_hist)

        # Graph complexity penalty (smaller focused graphs with lower overhead get lower penalty)
        complexity_penalty = min(1.0, (node_count + edge_count) / 50.0)

        total_score = (
            self.w1 * ig_norm +
            self.w2 * time_norm +
            self.w3 * conf_norm +
            self.w4 * hist_norm -
            self.w5 * complexity_penalty
        )

        final_score = round(max(0.0, total_score), 4)

        return {
            "score": final_score,
            "details": {
                "ig_norm": round(ig_norm, 3),
                "time_norm": round(time_norm, 3),
                "confidence_norm": round(conf_norm, 3),
                "history_norm": round(hist_norm, 3),
                "complexity_penalty": round(complexity_penalty, 3)
            }
        }
