"""
Dataset Exporter for E-Commerce Payment Incident Simulator.
Exports generated incidents to structured JSON files.
"""

from typing import Dict, List, Any
import json
import os


class DatasetExporter:
    """
    Handles JSON file serialization and output schema validation.
    """

    @staticmethod
    def validate_incident(incident: Dict[str, Any]) -> bool:
        """
        Validates required fields in the incident schema.
        """
        required_keys = [
            "incident_id", "topology", "root_cause",
            "symptoms", "optimal_investigation_path",
            "suboptimal_paths", "mttr_s", "services_affected"
        ]
        return all(key in incident for key in required_keys)

    @classmethod
    def export_to_json(cls, incidents: List[Dict[str, Any]], output_path: str):
        """
        Saves a list of incidents to a JSON file.
        """
        # Ensure directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        for inc in incidents:
            if not cls.validate_incident(inc):
                raise ValueError(f"Incident {inc.get('incident_id')} failed schema validation.")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(incidents, f, indent=2)
