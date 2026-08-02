"""
Topology Generator for E-Commerce Payment Subsystem using NetworkX.
"""

from typing import Dict, List, Any
import networkx as nx
import random


class TopologyGenerator:
    """
    Generates realistic microservice DAG topologies centered on an E-Commerce Payment Subsystem.
    """

    def __init__(self, service_count: int = 10, seed: int = None):
        self.service_count = max(5, service_count)
        if seed is not None:
            random.seed(seed)
        self.graph = nx.DiGraph()

    def generate(self) -> nx.DiGraph:
        """
        Builds the microservice DAG with node attributes (type, metrics) and dependency edges.
        """
        self.graph.clear()

        # Core E-Commerce Payment Services
        core_nodes = [
            {
                "id": "frontend",
                "name": "Web Frontend UI",
                "type": "frontend",
                "metrics": ["error_rate", "p99_latency", "cpu_utilization"]
            },
            {
                "id": "api-gateway",
                "name": "API Gateway",
                "type": "gateway",
                "metrics": ["error_rate", "p99_latency", "active_requests", "cpu_utilization"]
            },
            {
                "id": "order-svc",
                "name": "Order Management Service",
                "type": "service",
                "metrics": ["error_rate", "p99_latency", "memory_usage_mb", "cpu_utilization"]
            },
            {
                "id": "payment-api",
                "name": "Payment API Service",
                "type": "service",
                "metrics": ["error_rate", "p99_latency", "http_5xx_rate", "cpu_utilization"]
            },
            {
                "id": "auth-svc",
                "name": "Authentication Service",
                "type": "service",
                "metrics": ["error_rate", "token_validation_latency", "cpu_utilization"]
            },
            {
                "id": "payment-db",
                "name": "Payment PostgreSQL Database",
                "type": "database",
                "metrics": ["query_latency_ms", "connection_pool_usage", "disk_io_utilization"]
            },
            {
                "id": "redis-cache",
                "name": "Payment Session Cache",
                "type": "cache",
                "metrics": ["hit_ratio", "memory_usage_mb", "eviction_rate"]
            },
            {
                "id": "ext-payment-gateway",
                "name": "Third-Party Payment Provider (Stripe/PayPal)",
                "type": "external_api",
                "metrics": ["http_status_code", "timeout_rate", "response_time_ms"]
            }
        ]

        for node in core_nodes:
            self.graph.add_node(node["id"], **node)

        # Standard Payment Core Edges (Dependencies: Source -> Target)
        core_edges = [
            ("frontend", "api-gateway", "http"),
            ("api-gateway", "order-svc", "grpc"),
            ("api-gateway", "auth-svc", "grpc"),
            ("order-svc", "payment-api", "grpc"),
            ("payment-api", "auth-svc", "grpc"),
            ("payment-api", "payment-db", "sql"),
            ("payment-api", "redis-cache", "redis_protocol"),
            ("payment-api", "ext-payment-gateway", "https")
        ]

        for src, dst, proto in core_edges:
            self.graph.add_edge(src, dst, protocol=proto)

        # Add optional helper microservices if service_count > len(core_nodes)
        extra_count = self.service_count - len(core_nodes)
        for i in range(extra_count):
            extra_id = f"microservice-aux-{i+1}"
            extra_node = {
                "id": extra_id,
                "name": f"Auxiliary Service {i+1}",
                "type": "service",
                "metrics": ["error_rate", "p99_latency", "cpu_utilization"]
            }
            self.graph.add_node(extra_id, **extra_node)
            # Connect from order-svc or payment-api
            parent = random.choice(["order-svc", "payment-api"])
            self.graph.add_edge(parent, extra_id, protocol="http")

        return self.graph

    def to_dict(self) -> Dict[str, Any]:
        """
        Exports the generated topology into JSON-serializable dictionary format.
        """
        nodes_data = []
        for node_id, data in self.graph.nodes(data=True):
            # Calculate dependencies (out-edges)
            deps = list(self.graph.successors(node_id))
            nodes_data.append({
                "id": node_id,
                "name": data.get("name", node_id),
                "type": data.get("type", "service"),
                "metrics": data.get("metrics", []),
                "dependencies": deps
            })

        edges_data = []
        for src, dst, data in self.graph.edges(data=True):
            edges_data.append({
                "source": src,
                "target": dst,
                "protocol": data.get("protocol", "http")
            })

        return {
            "nodes": nodes_data,
            "edges": edges_data
        }
