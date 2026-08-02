"""
Seed Diagnostic Reasoning Graph for E-Commerce Payment Subsystem.
"""

from .graph_engine import DiagnosticGraph


def create_payment_seed_graph() -> DiagnosticGraph:
    """
    Constructs the initial seed diagnostic reasoning graph for Payment failures.
    Includes baseline static checklist nodes (some redundant) to demonstrate future graph evolution.
    """
    dg = DiagnosticGraph(version_id="seed-v1.0.0")

    # 1. Entry Point Node
    dg.add_diagnostic_node(
        node_id="entry:payment-api:error_rate",
        label="Check Payment API High 5xx Error Rate",
        node_type="entry",
        target_service="payment-api",
        target_metric="error_rate",
        info_gain=0.0,
        avg_duration_s=2
    )

    # 2. Redundant Static Checklist Nodes (Initial unoptimized graph)
    dg.add_diagnostic_node(
        node_id="check:frontend:cpu_utilization",
        label="Check Frontend Web UI CPU Saturation",
        node_type="check",
        target_service="frontend",
        target_metric="cpu_utilization",
        info_gain=0.01,
        avg_duration_s=4
    )

    dg.add_diagnostic_node(
        node_id="check:network:packet_loss",
        label="Check Core Gateway Network Packet Loss",
        node_type="check",
        target_service="api-gateway",
        target_metric="packet_loss",
        info_gain=0.02,
        avg_duration_s=5
    )

    # 3. Microservice Diagnostic Checks
    dg.add_diagnostic_node(
        node_id="check:payment-api:p99_latency",
        label="Check Payment API p99 Latency Anomaly",
        node_type="check",
        target_service="payment-api",
        target_metric="p99_latency",
        info_gain=0.45,
        avg_duration_s=2
    )

    dg.add_diagnostic_node(
        node_id="check:payment-db:connection_pool",
        label="Check Payment PostgreSQL Connection Pool Exhaustion",
        node_type="check",
        target_service="payment-db",
        target_metric="connection_pool_usage",
        info_gain=0.88,
        avg_duration_s=3,
        historical_success_rate=0.85
    )

    dg.add_diagnostic_node(
        node_id="check:payment-db:query_latency",
        label="Check Payment DB Slow Query Latency",
        node_type="check",
        target_service="payment-db",
        target_metric="query_latency_ms",
        info_gain=0.72,
        avg_duration_s=3
    )

    dg.add_diagnostic_node(
        node_id="check:auth-svc:token_validation",
        label="Check Auth Service Token Validation Latency",
        node_type="check",
        target_service="auth-svc",
        target_metric="token_validation_latency",
        info_gain=0.65,
        avg_duration_s=4
    )

    dg.add_diagnostic_node(
        node_id="check:ext-payment-gateway:status",
        label="Check External Payment Gateway Timeout Rate",
        node_type="check",
        target_service="ext-payment-gateway",
        target_metric="timeout_rate",
        info_gain=0.80,
        avg_duration_s=4
    )

    # 4. Action Remediation Nodes
    dg.add_diagnostic_node(
        node_id="action:expand_db_connection_pool",
        label="Remediation: Scale Up Payment DB Connection Pool Size",
        node_type="action",
        target_service="payment-db",
        avg_duration_s=10
    )

    dg.add_diagnostic_node(
        node_id="action:restart_auth_service",
        label="Remediation: Restart Authentication Service Pods",
        node_type="action",
        target_service="auth-svc",
        avg_duration_s=15
    )

    # 5. Connect Edges (Default Static Traversal Order)
    # Entry -> Redundant checklist sweeps (always) -> Payment API checks -> Conditional branch to DB / Auth / External
    dg.add_decision_edge("entry:payment-api:error_rate", "check:frontend:cpu_utilization", priority_weight=1.0, condition="always")
    dg.add_decision_edge("check:frontend:cpu_utilization", "check:network:packet_loss", priority_weight=1.0, condition="always")
    dg.add_decision_edge("check:network:packet_loss", "check:payment-api:p99_latency", priority_weight=1.0, condition="always")
    dg.add_decision_edge("check:payment-api:p99_latency", "check:payment-db:connection_pool", priority_weight=1.0, condition="always")
    dg.add_decision_edge("check:payment-api:p99_latency", "check:auth-svc:token_validation", priority_weight=0.8, condition="always")
    dg.add_decision_edge("check:payment-api:p99_latency", "check:ext-payment-gateway:status", priority_weight=0.7, condition="always")
    dg.add_decision_edge("check:payment-db:connection_pool", "check:payment-db:query_latency", priority_weight=1.0, condition="always")
    dg.add_decision_edge("check:payment-db:connection_pool", "action:expand_db_connection_pool", priority_weight=1.0, condition="on_anomaly")
    dg.add_decision_edge("check:auth-svc:token_validation", "action:restart_auth_service", priority_weight=1.0, condition="on_anomaly")

    return dg
