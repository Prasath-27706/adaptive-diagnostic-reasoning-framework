"""
Experience Extractor Module (Module 4).
Parses decision traces, computes empirical Information Gain, and flags redundant/high-value nodes.
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
from .entropy import calculate_empirical_info_gain
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("m4_extractor")


class ExperienceExtractor:
    """
    Offline/Online learning module that extracts diagnostic experience from decision traces.
    """

    def __init__(self, ig_removal_threshold: float = 0.05, ig_priority_threshold: float = 0.15):
        self.ig_removal_threshold = ig_removal_threshold
        self.ig_priority_threshold = ig_priority_threshold

    def extract_experience(
        self,
        decision_traces: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Parses decision traces across N incidents and generates an Experience Record.
        """
        if not decision_traces:
            return {"status": "empty", "total_incidents_analyzed": 0}

        node_stats = defaultdict(lambda: {
            "visits": 0,
            "outcomes": [],
            "ig_scores": [],
            "durations": [],
            "label": "",
            "target_service": "",
            "target_metric": ""
        })

        for trace in decision_traces:
            for step in trace:
                node_id = step.get("node_id")
                if not node_id:
                    continue

                stats = node_stats[node_id]
                stats["visits"] += 1
                stats["outcomes"].append(step.get("result", "normal"))
                stats["ig_scores"].append(step.get("info_gain", 0.0))
                stats["durations"].append(step.get("time_taken_s", 3))
                if not stats["label"]:
                    stats["label"] = step.get("label", node_id)
                    stats["target_service"] = step.get("target_service", "unknown")
                    stats["target_metric"] = step.get("target_metric")

        summary_nodes = {}
        redundant_nodes = []
        high_value_nodes = []

        for node_id, stats in node_stats.items():
            visits = stats["visits"]
            avg_ig = calculate_empirical_info_gain(stats["outcomes"]) if stats["outcomes"] else 0.0
            avg_dur = sum(stats["durations"]) / visits if visits > 0 else 3.0
            anomaly_count = stats["outcomes"].count("anomaly") + stats["outcomes"].count("degraded")
            success_rate = round(anomaly_count / visits, 3) if visits > 0 else 0.0

            node_summary = {
                "node_id": node_id,
                "label": stats["label"],
                "target_service": stats["target_service"],
                "target_metric": stats["target_metric"],
                "total_visits": visits,
                "anomaly_count": anomaly_count,
                "success_rate": success_rate,
                "avg_info_gain": avg_ig,
                "avg_duration_s": round(avg_dur, 2)
            }
            summary_nodes[node_id] = node_summary

            # Categorize nodes (only check: diagnostic nodes can be candidates for removal!)
            if node_id.startswith("check:") and avg_ig < self.ig_removal_threshold:
                redundant_nodes.append(node_id)
            elif avg_ig >= self.ig_priority_threshold:
                high_value_nodes.append(node_id)

        # Sort high-value nodes by efficiency ratio (Information Gain / Duration)
        reorder_recommendations = sorted(
            [n for n in summary_nodes.values() if n["node_id"] in high_value_nodes],
            key=lambda x: (x["avg_info_gain"] / max(1.0, x["avg_duration_s"])),
            reverse=True
        )

        # Identify anomalous services to recommend deep diagnostic hypothesis additions
        anomalous_services = set()
        for nid, stats in summary_nodes.items():
            if stats["anomaly_count"] > 0:
                anomalous_services.add(stats["target_service"])

        suggested_additions = []
        if "payment-db" in anomalous_services:
            suggested_additions.append({
                "node_id": "check:payment-db:lock_contention",
                "label": "Check PostgreSQL Row Lock Contention",
                "node_type": "check",
                "target_service": "payment-db",
                "target_metric": "lock_contention",
                "parent_id": "check:payment-db:connection_pool"
            })
        if "auth-svc" in anomalous_services:
            suggested_additions.append({
                "node_id": "check:auth-svc:jwt_jwks_cache",
                "label": "Check Auth0 JWKS Public Key Cache Eviction",
                "node_type": "check",
                "target_service": "auth-svc",
                "target_metric": "jwt_jwks_cache",
                "parent_id": "check:auth-svc:token_validation"
            })
        if "ext-payment-gateway" in anomalous_services:
            suggested_additions.append({
                "node_id": "check:ext-payment-gateway:tls_handshake",
                "label": "Probe Stripe Upstream TLS Handshake Latency",
                "node_type": "check",
                "target_service": "ext-payment-gateway",
                "target_metric": "tls_handshake",
                "parent_id": "check:ext-payment-gateway:status"
            })
        if "payment-api" in anomalous_services:
            suggested_additions.append({
                "node_id": "check:payment-api:jvm_heap_exhaustion",
                "label": "Check Container Cgroup & JVM Heap Saturation",
                "node_type": "check",
                "target_service": "payment-api",
                "target_metric": "jvm_heap_exhaustion",
                "parent_id": "check:payment-api:p99_latency"
            })

        return {
            "total_incidents_analyzed": len(decision_traces),
            "unique_nodes_evaluated": len(summary_nodes),
            "redundant_nodes": redundant_nodes,
            "high_value_nodes": high_value_nodes,
            "reorder_recommendations": [n["node_id"] for n in reorder_recommendations],
            "suggested_additions": suggested_additions,
            "node_statistics": summary_nodes
        }

