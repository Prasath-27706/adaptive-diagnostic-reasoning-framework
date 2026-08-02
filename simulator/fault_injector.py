"""
Fault Injector for E-Commerce Payment Subsystem.
Simulates root-cause failures and propagates anomalous symptoms upstream.
"""

from typing import Dict, List, Any, Tuple
import networkx as nx
import random
from datetime import datetime, timezone


class FaultInjector:
    """
    Injects root cause faults into the payment topology and propagates anomaly symptoms.
    """

    FAULT_PRESETS = [
        {
            "service": "payment-db",
            "fault_type": "connection_pool_exhausted",
            "primary_metric": "connection_pool_usage",
            "anomaly_value": 0.99,
            "baseline_value": 0.15,
            "severity": "critical",
            "summary": "Database connection pool exhausted on payment-db"
        },
        {
            "service": "auth-svc",
            "fault_type": "auth_token_timeout",
            "primary_metric": "token_validation_latency",
            "anomaly_value": 4800,
            "baseline_value": 80,
            "severity": "high",
            "summary": "Authentication token validation timing out"
        },
        {
            "service": "payment-api",
            "fault_type": "memory_leak_oom",
            "primary_metric": "http_5xx_rate",
            "anomaly_value": 0.55,
            "baseline_value": 0.002,
            "severity": "critical",
            "summary": "High 5xx error rate on payment-api due to memory saturation"
        },
        {
            "service": "ext-payment-gateway",
            "fault_type": "third_party_timeout",
            "primary_metric": "timeout_rate",
            "anomaly_value": 0.88,
            "baseline_value": 0.01,
            "severity": "critical",
            "summary": "External payment gateway API timeouts"
        },
        {
            "service": "redis-cache",
            "fault_type": "cache_stampede",
            "primary_metric": "hit_ratio",
            "anomaly_value": 0.05,
            "baseline_value": 0.95,
            "severity": "medium",
            "summary": "Redis cache hit ratio drop causing cache stampede"
        }
    ]

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def inject_fault(self, graph: nx.DiGraph) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Selects a fault, injects root cause, and computes upstream propagated symptoms.
        Returns: (root_cause_dict, list_of_symptoms)
        """
        preset = random.choice(self.FAULT_PRESETS)
        root_service = preset["service"]

        # Ensure node exists in graph
        if not graph.has_node(root_service):
            root_service = list(graph.nodes())[0]

        root_cause = {
            "service": root_service,
            "metric": preset["primary_metric"],
            "fault_type": preset["fault_type"],
            "severity": preset["severity"],
            "summary": preset["summary"]
        }

        now_iso = datetime.now(timezone.utc).isoformat()

        # Primary root cause symptom
        symptoms = [
            {
                "service": root_service,
                "metric": preset["primary_metric"],
                "value": preset["anomaly_value"],
                "baseline": preset["baseline_value"],
                "timestamp": now_iso
            }
        ]

        # Propagate upstream (find ancestors in DAG)
        # Predecessors in DiGraph (A -> B means A depends on B; so predecessors of B depend on B)
        try:
            ancestors = list(nx.ancestors(graph, root_service))
        except Exception:
            ancestors = []

        # Add propagated symptoms to upstream dependents
        for ancestor_id in ancestors:
            node_data = graph.nodes[ancestor_id]
            metrics = node_data.get("metrics", ["error_rate", "p99_latency"])
            selected_metric = random.choice(metrics)

            if "error_rate" in selected_metric:
                value, baseline = round(random.uniform(0.30, 0.70), 2), 0.01
            elif "latency" in selected_metric:
                value, baseline = round(random.uniform(3000, 8000), 1), 150.0
            else:
                value, baseline = round(random.uniform(0.75, 0.95), 2), 0.20

            symptoms.append({
                "service": ancestor_id,
                "metric": selected_metric,
                "value": value,
                "baseline": baseline,
                "timestamp": now_iso
            })

        return root_cause, symptoms
