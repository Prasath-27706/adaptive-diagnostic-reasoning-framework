"""
Structural Verifier for Module 6.
Enforces graph DAG acyclicity, node reachability, completeness, and consistency checks.
"""

from typing import Tuple, List, Dict, Any
import networkx as nx
from modules.m2_graph import DiagnosticGraph


class StructuralVerifier:
    """
    Validates structural graph invariants before candidate graph persistence.
    """

    def verify_structure(self, graph: DiagnosticGraph) -> Dict[str, Any]:
        """
        Executes all structural verification checks.
        """
        nx_graph = graph.graph

        # 1. DAG Check
        is_dag = nx.is_directed_acyclic_graph(nx_graph)

        # 2. Reachability Check from Entry Points
        entries = graph.get_entry_nodes()
        all_nodes = set(nx_graph.nodes())
        reachable_nodes = set()

        for entry in entries:
            if entry in all_nodes:
                reachable_nodes.add(entry)
                try:
                    descendants = nx.descendants(nx_graph, entry)
                    reachable_nodes.update(descendants)
                except Exception:
                    pass

        orphan_nodes = list(all_nodes - reachable_nodes)
        all_reachable = len(orphan_nodes) == 0

        # 3. Completeness Check (Ensures graph has terminal/action/check nodes)
        terminal_nodes = [n for n in nx_graph.nodes() if nx_graph.out_degree(n) == 0]
        has_terminal_nodes = len(terminal_nodes) > 0

        # 4. Consistency Check (Validates required node properties)
        consistent = True
        missing_props_nodes = []
        for n, data in nx_graph.nodes(data=True):
            if not data.get("id") or not data.get("node_type"):
                consistent = False
                missing_props_nodes.append(n)

        passed_all = is_dag and all_reachable and has_terminal_nodes and consistent

        return {
            "passed": passed_all,
            "is_dag": is_dag,
            "all_reachable": all_reachable,
            "orphan_nodes": orphan_nodes,
            "has_terminal_nodes": has_terminal_nodes,
            "terminal_nodes": terminal_nodes,
            "consistent": consistent,
            "invalid_prop_nodes": missing_props_nodes
        }
