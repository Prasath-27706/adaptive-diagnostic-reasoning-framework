"""
FastAPI REST API Server for Modules 1, 2, 3, 4, 5, 6, and 7.
"""

from fastapi import FastAPI, HTTPException, Body
from typing import Dict, List, Any
import sys
import os

# Add root path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.m1_collection import MetricSignal, AlertSignal, TelemetryReceiver
from modules.m2_graph import DiagnosticGraph, create_payment_seed_graph
from modules.m3_analyzer import IncidentAnalyzer
from modules.m4_extractor import ExperienceExtractor
from modules.m5_decision_engine import EvolutionEngine
from modules.m6_verification import GraphVerifier
from modules.m7_repository import KnowledgeRepository

app = FastAPI(
    title="Adaptive Diagnostic Reasoning Framework API",
    version="1.0.0",
    description="REST Endpoints for Telemetry (M1), Graph (M2), Analyzer (M3), Experience (M4), Evolution (M5), Verification (M6), and Repository (M7)"
)

# Global in-memory state
receiver = TelemetryReceiver()
current_graph: DiagnosticGraph = create_payment_seed_graph()
analyzer = IncidentAnalyzer()
extractor = ExperienceExtractor()
evolution_engine = EvolutionEngine()
verifier = GraphVerifier()
repository = KnowledgeRepository()

# Save initial seed graph
repository.save_graph_version(current_graph, "INITIAL_SEED", 0.5, "APPROVED")


@app.get("/")
def read_root():
    return {
        "system": "Adaptive Diagnostic Reasoning Framework",
        "status": "online",
        "graph_version": current_graph.version_id,
        "nodes": len(current_graph.graph.nodes)
    }


# --- Module 1: Telemetry Endpoints ---

@app.post("/telemetry/metrics")
def ingest_metrics(metrics: List[MetricSignal]):
    anomalous_count = receiver.ingest_metrics(metrics)
    return {
        "status": "success",
        "ingested": len(metrics),
        "anomalous": anomalous_count
    }


@app.post("/telemetry/alert")
def ingest_alert(alert: AlertSignal):
    receiver.ingest_alert(alert)
    return {"status": "success", "alert_id": alert.alert_id}


@app.get("/telemetry/anomalies")
def get_anomalies():
    anomalies = receiver.get_active_anomalies()
    return {"count": len(anomalies), "anomalies": [a.model_dump() for a in anomalies]}


# --- Module 2: Reasoning Graph Endpoints ---

@app.get("/graph/latest")
def get_latest_graph():
    return current_graph.to_dict()


@app.post("/graph/save")
def save_graph(graph_data: Dict[str, Any] = Body(...)):
    global current_graph
    try:
        new_graph = DiagnosticGraph.from_dict(graph_data)
        if not new_graph.is_dag():
            raise HTTPException(status_code=400, detail="Graph verification failed: Graph contains cycles.")
        current_graph = new_graph
        repository.save_graph_version(current_graph, "MUTATED_PERSISTED", 0.8, "APPROVED")
        return {"status": "success", "version_id": current_graph.version_id, "nodes": len(current_graph.graph.nodes)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/graph/seed")
def reset_to_seed_graph():
    global current_graph
    current_graph = create_payment_seed_graph()
    repository.save_graph_version(current_graph, "RESET_SEED", 0.5, "APPROVED")
    return {"status": "success", "message": "Reset to default payment seed graph", "graph": current_graph.to_dict()}


# --- Module 3: Incident Analyzer Endpoint ---

@app.post("/analyze")
def analyze_incident(incident: Dict[str, Any] = Body(...)):
    """
    Traverses the active diagnostic graph and returns root cause isolation + decision trace.
    """
    try:
        result = analyzer.analyze_incident(current_graph, incident)
        repository.log_mttr_point(current_graph.version_id, result["mttr_s"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# --- Module 4: Experience Extractor Endpoint ---

@app.post("/experience/extract")
def extract_experience(decision_traces: List[List[Dict[str, Any]]] = Body(...)):
    """
    Parses historical decision traces and computes Information Gain & redundant node recommendations.
    """
    try:
        record = extractor.extract_experience(decision_traces)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Experience extraction failed: {str(e)}")


# --- Module 5: Evolution Decision Engine Endpoint ★ CORE NOVELTY ---

@app.post("/evolve")
def evolve_graph(experience_record: Dict[str, Any] = Body(...)):
    """
    Generates candidate graph mutations (REMOVE, REORDER, ADD), scores via multi-objective optimization, and selects top-1 evolved graph.
    """
    try:
        evolution_result = evolution_engine.evolve_graph(current_graph, experience_record)
        return evolution_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph evolution failed: {str(e)}")


# --- Module 6: Graph Verification Endpoint ---

@app.post("/verify")
def verify_graph(payload: Dict[str, Any] = Body(...)):
    """
    Performs structural DAG/reachability checks and performance replay verification on a candidate graph.
    """
    try:
        candidate_data = payload.get("candidate_graph", {})
        historical_incidents = payload.get("historical_incidents", [])

        candidate_graph = DiagnosticGraph.from_dict(candidate_data)
        verification_report = verifier.verify_candidate_graph(
            current_graph=current_graph,
            candidate_graph=candidate_graph,
            historical_incidents=historical_incidents
        )
        return verification_report
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")


# --- Module 7: Operational Knowledge Repository Endpoints ---

@app.get("/repository/graphs")
def get_all_graphs():
    return {"versions": repository.get_all_graph_versions()}


@app.get("/repository/history")
def get_transformation_history():
    return {"history": repository.get_transformation_history()}


@app.get("/repository/mttr")
def get_mttr_history():
    return {"mttr_points": repository.get_mttr_history()}
