"""
Incident Simulator Orchestrator for E-Commerce Payment Subsystem.
"""

from typing import Dict, List, Any
import random
from .topology_generator import TopologyGenerator
from .fault_injector import FaultInjector
from .trace_recorder import TraceRecorder
from .dataset_exporter import DatasetExporter


class IncidentSimulator:
    """
    Main orchestrator class for generating synthetic cloud incident datasets.
    """

    def __init__(self, service_count: int = 10, seed: int = None):
        self.service_count = service_count
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        self.topology_gen = TopologyGenerator(service_count=service_count, seed=seed)
        self.fault_inj = FaultInjector(seed=seed)
        self.trace_rec = TraceRecorder(seed=seed)

    def generate_incidents(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Generates N synthetic incident records.
        """
        graph = self.topology_gen.generate()
        topology_dict = self.topology_gen.to_dict()

        incidents = []
        for i in range(1, count + 1):
            inc_id = f"INC-PAY-{i:05d}"
            root_cause, symptoms = self.fault_inj.inject_fault(graph)
            optimal_path, suboptimal_paths, mttr_s = self.trace_rec.record_paths(root_cause, symptoms)

            affected_services = list(set([s["service"] for s in symptoms]))

            incident_record = {
                "incident_id": inc_id,
                "topology": topology_dict,
                "root_cause": root_cause,
                "symptoms": symptoms,
                "optimal_investigation_path": optimal_path,
                "suboptimal_paths": suboptimal_paths,
                "mttr_s": mttr_s,
                "services_affected": affected_services,
                "alert_metadata": {
                    "severity": root_cause.get("severity", "P1").upper(),
                    "source": "Prometheus AlertManager",
                    "summary": root_cause.get("summary", f"Anomaly detected in {root_cause['service']}")
                }
            }
            incidents.append(incident_record)

        return incidents

    def generate_and_export(self, count: int = 100, output_path: str = "data/payment_incidents.json"):
        """
        Generates and saves dataset to output_path.
        """
        incidents = self.generate_incidents(count=count)
        DatasetExporter.export_to_json(incidents, output_path)
        return len(incidents)
