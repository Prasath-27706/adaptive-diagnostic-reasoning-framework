"""
Operational Knowledge Repository for Module 7.
Provides persistent versioning for diagnostic graphs, transformation logs, and MTTR metrics.
"""

from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime, timezone
from modules.m2_graph import DiagnosticGraph


class KnowledgeRepository:
    """
    JSON-backed persistent store for diagnostic graphs, evolution history, and operational MTTR metrics.
    """

    def __init__(self, db_path: str = "data/repository_db.json"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        out_dir = os.path.dirname(self.db_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            initial_data = {
                "graphs": {},
                "transformations": [],
                "mttr_history": []
            }
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def _read_db(self) -> Dict[str, Any]:
        self._ensure_db_exists()
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_db(self, data: Dict[str, Any]):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def save_graph_version(
        self,
        graph: DiagnosticGraph,
        transformation_type: str = "INITIAL",
        score: float = 0.5,
        verification_status: str = "APPROVED"
    ) -> str:
        """
        Stores a versioned DiagnosticGraph with metadata and transformation log.
        """
        db = self._read_db()
        graph_dict = graph.to_dict()
        version_id = graph.version_id
        now_iso = datetime.now(timezone.utc).isoformat()

        db["graphs"][version_id] = {
            "version_id": version_id,
            "created_at": now_iso,
            "graph": graph_dict,
            "node_count": len(graph.graph.nodes),
            "edge_count": len(graph.graph.edges)
        }

        db["transformations"].append({
            "timestamp": now_iso,
            "version_id": version_id,
            "transformation_type": transformation_type,
            "score": score,
            "verification_status": verification_status
        })

        self._write_db(db)
        return version_id

    def log_mttr_point(self, version_id: str, mttr_s: float):
        """
        Records an MTTR measurement point for a specific graph version.
        """
        db = self._read_db()
        db["mttr_history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version_id": version_id,
            "mttr_s": round(mttr_s, 2)
        })
        self._write_db(db)

    def get_graph_version(self, version_id: str) -> Optional[Dict[str, Any]]:
        db = self._read_db()
        return db["graphs"].get(version_id)

    def get_all_graph_versions(self) -> List[Dict[str, Any]]:
        db = self._read_db()
        return list(db["graphs"].values())

    def get_transformation_history(self) -> List[Dict[str, Any]]:
        db = self._read_db()
        return db["transformations"]

    def get_mttr_history(self) -> List[Dict[str, Any]]:
        db = self._read_db()
        return db["mttr_history"]
