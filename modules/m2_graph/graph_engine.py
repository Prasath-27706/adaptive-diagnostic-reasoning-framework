"""
Diagnostic Reasoning Graph Engine for Module 2.
Encodes diagnostic reasoning hypothesis checks and decision rules using NetworkX.
"""

from typing import Dict, List, Any, Optional
import networkx as nx
import json


class DiagnosticGraph:
    """
    Directed Graph representing diagnostic reasoning workflows.
    Nodes = Hypotheses / Checks / Actions.
    Edges = Conditional traversal paths with priority weights.
    """

    def __init__(self, version_id: str = "v1.0.0"):
        self.version_id = version_id
        self.graph = nx.DiGraph(version_id=version_id)

    def add_diagnostic_node(
        self,
        node_id: str,
        label: str,
        node_type: str,  # 'entry', 'hypothesis', 'check', 'action'
        target_service: str,
        target_metric: Optional[str] = None,
        info_gain: float = 0.0,
        avg_duration_s: int = 3,
        historical_success_rate: float = 0.5
    ):
        """
        Adds or updates a diagnostic reasoning node.
        """
        self.graph.add_node(
            node_id,
            id=node_id,
            label=label,
            node_type=node_type,
            target_service=target_service,
            target_metric=target_metric,
            info_gain=info_gain,
            avg_duration_s=avg_duration_s,
            historical_success_rate=historical_success_rate
        )

    def add_decision_edge(
        self,
        source_id: str,
        target_id: str,
        priority_weight: float = 1.0,
        condition: str = "on_anomaly"  # 'on_anomaly', 'on_normal', 'always'
    ):
        """
        Adds a directed decision edge between checks/hypotheses.
        """
        self.graph.add_edge(
            source_id,
            target_id,
            weight=priority_weight,
            condition=condition
        )

    def remove_diagnostic_node(self, node_id: str):
        """
        Deletes a node and reconnects incoming/outgoing edges.
        """
        if self.graph.has_node(node_id):
            in_edges = list(self.graph.in_edges(node_id, data=True))
            out_edges = list(self.graph.out_edges(node_id, data=True))
            for in_src, _, in_data in in_edges:
                for _, out_dst, out_data in out_edges:
                    if not self.graph.has_edge(in_src, out_dst):
                        self.graph.add_edge(in_src, out_dst, weight=in_data.get("weight", 1.0), condition=in_data.get("condition", "on_anomaly"))
            self.graph.remove_node(node_id)

    def is_dag(self) -> bool:
        """
        Verifies that the graph is acyclic.
        """
        return nx.is_directed_acyclic_graph(self.graph)

    def get_entry_nodes(self) -> List[str]:
        """
        Returns all nodes marked as entry points or with in-degree 0.
        """
        entries = [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == "entry"]
        if not entries:
            entries = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
        return entries

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the diagnostic graph to a dictionary.
        """
        nodes_list = []
        for n, data in self.graph.nodes(data=True):
            nodes_list.append(data)

        edges_list = []
        for u, v, data in self.graph.edges(data=True):
            edges_list.append({
                "source": u,
                "target": v,
                "weight": data.get("weight", 1.0),
                "condition": data.get("condition", "on_anomaly")
            })

        return {
            "version_id": self.version_id,
            "node_count": len(nodes_list),
            "edge_count": len(edges_list),
            "nodes": nodes_list,
            "edges": edges_list
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiagnosticGraph":
        """
        Deserializes dictionary to a DiagnosticGraph instance.
        """
        dg = cls(version_id=data.get("version_id", "v1.0.0"))
        for n in data.get("nodes", []):
            dg.add_diagnostic_node(
                node_id=n["id"],
                label=n.get("label", n["id"]),
                node_type=n.get("node_type", "check"),
                target_service=n.get("target_service", "unknown"),
                target_metric=n.get("target_metric"),
                info_gain=n.get("info_gain", 0.0),
                avg_duration_s=n.get("avg_duration_s", 3),
                historical_success_rate=n.get("historical_success_rate", 0.5)
            )

        for e in data.get("edges", []):
            dg.add_decision_edge(
                source_id=e["source"],
                target_id=e["target"],
                priority_weight=e.get("weight", 1.0),
                condition=e.get("condition", "on_anomaly")
            )
        return dg
