"""
Trace Recorder for E-Commerce Payment Subsystem.
Generates optimal diagnostic paths and baseline suboptimal paths.
"""

from typing import Dict, List, Any, Tuple
import random


class TraceRecorder:
    """
    Generates investigation paths (optimal vs suboptimal) and calculates MTTR.
    """

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def record_paths(
        self,
        root_cause: Dict[str, Any],
        symptoms: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[List[Dict[str, Any]]], int]:
        """
        Generates optimal path, suboptimal paths, and MTTR in seconds.
        """
        root_service = root_cause["service"]
        root_metric = root_cause["metric"]

        # Find primary alarm symptom (e.g., API Gateway or Payment API error)
        alarm_symptom = symptoms[0] if symptoms else {
            "service": "payment-api", "metric": "error_rate"
        }

        # 1. Build Optimal Investigation Path
        optimal_path = [
            {
                "step": 1,
                "node_id": f"check:{alarm_symptom['service']}:{alarm_symptom['metric']}",
                "check_type": "metric_query",
                "result": "anomaly",
                "info_gain": 0.0,
                "time_taken_s": 2
            },
            {
                "step": 2,
                "node_id": f"check:{root_service}:health",
                "check_type": "service_health",
                "result": "degraded",
                "info_gain": 0.82,
                "time_taken_s": 3
            },
            {
                "step": 3,
                "node_id": f"check:{root_service}:{root_metric}",
                "check_type": "metric_query",
                "result": root_cause["fault_type"],
                "info_gain": 0.18,
                "time_taken_s": 5
            }
        ]

        # 2. Build Suboptimal Path (Static checklist baseline)
        unrelated_checks = [
            {"node_id": "check:frontend:cpu_utilization", "check_type": "metric_query"},
            {"node_id": "check:frontend:memory_usage", "check_type": "metric_query"},
            {"node_id": "check:network:packet_loss", "check_type": "network_ping"},
            {"node_id": "check:api-gateway:disk_space", "check_type": "disk_query"},
            {"node_id": "check:order-svc:jvm_garbage_collection", "check_type": "metric_query"},
            {"node_id": "check:redis-cache:hit_ratio", "check_type": "cache_status"},
        ]

        # Pick 3-5 redundant checks before reaching root cause
        redundant_sample = random.sample(unrelated_checks, k=random.randint(3, 5))
        suboptimal_steps = []
        step_idx = 1
        total_time_suboptimal = 0

        for check in redundant_sample:
            time_spent = random.randint(3, 8)
            total_time_suboptimal += time_spent
            suboptimal_steps.append({
                "step": step_idx,
                "node_id": check["node_id"],
                "check_type": check["check_type"],
                "result": "normal",
                "info_gain": 0.0,
                "time_taken_s": time_spent
            })
            step_idx += 1

        # Append root cause checks at the end of suboptimal path
        for opt_step in optimal_path[1:]:
            time_spent = opt_step["time_taken_s"] + random.randint(2, 5)
            total_time_suboptimal += time_spent
            suboptimal_steps.append({
                "step": step_idx,
                "node_id": opt_step["node_id"],
                "check_type": opt_step["check_type"],
                "result": opt_step["result"],
                "info_gain": opt_step["info_gain"],
                "time_taken_s": time_spent
            })
            step_idx += 1

        # Calculate MTTR (in seconds) for the suboptimal run (baseline)
        mttr_s = total_time_suboptimal + 120  # +120s baseline triage delay

        return optimal_path, [suboptimal_steps], mttr_s
