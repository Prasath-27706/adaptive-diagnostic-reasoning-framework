"""
Structural Graph Mutation Operations for Module 5.
Implements ADD, REMOVE, REORDER, SPLIT, MERGE transformations on Diagnostic Graphs.
"""

from typing import Dict, Any, List
import copy
from modules.m2_graph import DiagnosticGraph


def apply_remove_mutation(graph: DiagnosticGraph, node_id: str) -> DiagnosticGraph:
    """
    Creates a new DiagnosticGraph with the target node removed and adjacent edges reconnected.
    """
    graph_dict = graph.to_dict()
    new_graph = DiagnosticGraph.from_dict(copy.deepcopy(graph_dict))

    if new_graph.graph.has_node(node_id):
        new_graph.remove_diagnostic_node(node_id)
        new_graph.version_id = f"{graph.version_id}-rem-{node_id.split(':')[-1]}"

    return new_graph


def apply_reorder_mutation(graph: DiagnosticGraph, node_id: str, new_priority: float = 2.0) -> DiagnosticGraph:
    """
    Reorders a high-value node by increasing incoming edge priority weight.
    """
    graph_dict = graph.to_dict()
    new_graph = DiagnosticGraph.from_dict(copy.deepcopy(graph_dict))

    if new_graph.graph.has_node(node_id):
        in_edges = list(new_graph.graph.in_edges(node_id, data=True))
        for u, v, data in in_edges:
            new_graph.graph[u][v]["weight"] = new_priority
        new_graph.version_id = f"{graph.version_id}-reorder-{node_id.split(':')[-1]}"

    return new_graph


def apply_add_mutation(
    graph: DiagnosticGraph,
    node_id: str,
    label: str,
    node_type: str,
    target_service: str,
    target_metric: str,
    parent_id: str
) -> DiagnosticGraph:
    """
    Inserts a new diagnostic hypothesis node into the reasoning graph.
    """
    graph_dict = graph.to_dict()
    new_graph = DiagnosticGraph.from_dict(copy.deepcopy(graph_dict))

    new_graph.add_diagnostic_node(
        node_id=node_id,
        label=label,
        node_type=node_type,
        target_service=target_service,
        target_metric=target_metric,
        info_gain=0.75,
        avg_duration_s=3
    )

    if new_graph.graph.has_node(parent_id):
        new_graph.add_decision_edge(parent_id, node_id, priority_weight=1.5, condition="on_anomaly")

    new_graph.version_id = f"{graph.version_id}-add-{node_id.split(':')[-1]}"
    return new_graph
