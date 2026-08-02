"""
Interactive Streamlit Dashboard for Module 7.
Visualizes real-time diagnostic graph evolution, MTTR reduction trends, and incident decision traces.
"""

import streamlit as st
import pandas as pd
import json
import os
import sys

# Add root path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from modules.m2_graph import create_payment_seed_graph, DiagnosticGraph
from modules.m3_analyzer import IncidentAnalyzer
from modules.m4_extractor import ExperienceExtractor
from modules.m5_decision_engine import EvolutionEngine
from modules.m6_verification import GraphVerifier
from modules.m7_repository.repository import KnowledgeRepository

st.set_page_config(
    page_title="Adaptive Diagnostic Reasoning Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Initialize Session State & Repository
repo = KnowledgeRepository(db_path="data/repository_db.json")
analyzer = IncidentAnalyzer()
extractor = ExperienceExtractor()
evolution_engine = EvolutionEngine()
verifier = GraphVerifier()

if "current_graph" not in st.session_state:
    st.session_state["current_graph"] = create_payment_seed_graph()
    repo.save_graph_version(st.session_state["current_graph"], "INITIAL", 0.5, "APPROVED")


# --- Title & Header ---
st.title("⚡ Adaptive Diagnostic Reasoning Framework")
st.caption("Self-Evolving AIOps Decision Graph Engine for Autonomous Cloud Operations (E-Commerce Payment Domain)")

# Top Metric Banner
col1, col2, col3, col4 = st.columns(4)
current_g = st.session_state["current_graph"]
nodes = current_g.graph.nodes(data=True)

with col1:
    st.metric("Graph Version", current_g.version_id)
with col2:
    st.metric("Active Nodes", len(nodes))
with col3:
    st.metric("Active Edges", len(current_g.graph.edges))
with col4:
    st.metric("Status", "ONLINE", delta="Verification APPROVED")

st.divider()

# --- Main Navigation Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Diagnostic Reasoning Graph",
    "📈 MTTR & Performance Trends",
    "🚨 Incident Triage & Traces",
    "⚙️ Evolution Control Engine"
])

# --- TAB 1: Graph Visualization ---
with tab1:
    st.subheader("Current Diagnostic Reasoning Graph Structure")
    st.write("Encodes diagnostic hypotheses and check steps (not raw topology maps).")

    nodes_data = []
    for n_id, data in nodes:
        nodes_data.append({
            "Node ID": n_id,
            "Label": data.get("label", n_id),
            "Type": data.get("node_type", "check").upper(),
            "Target Service": data.get("target_service", "-"),
            "Target Metric": data.get("target_metric", "-"),
            "Avg Duration (s)": data.get("avg_duration_s", 3),
            "Historical Success Rate": data.get("historical_success_rate", 0.7)
        })

    df_nodes = pd.DataFrame(nodes_data)
    st.dataframe(df_nodes, use_container_width=True)

    st.subheader("Decision Edges (Conditional Traversal Rules)")
    edges_data = []
    for u, v, data in current_g.graph.edges(data=True):
        edges_data.append({
            "Source Node": u,
            "Target Node": v,
            "Priority Weight": data.get("weight", 1.0),
            "Traversal Condition": data.get("condition", "on_anomaly")
        })
    df_edges = pd.DataFrame(edges_data)
    st.dataframe(df_edges, use_container_width=True)

# --- TAB 2: MTTR Trends ---
with tab2:
    st.subheader("Mean Time to Resolution (MTTR) Reduction Trends")

    mttr_history = repo.get_mttr_history()
    if mttr_history:
        df_mttr = pd.DataFrame(mttr_history)
        st.line_chart(df_mttr, x="version_id", y="mttr_s", use_container_width=True)
    else:
        st.info("No MTTR history points logged yet. Execute an evolution run in Tab 4 to observe MTTR reduction.")

    st.subheader("Transformation Mutation History")
    history = repo.get_transformation_history()
    if history:
        df_hist = pd.DataFrame(history)
        st.dataframe(df_hist, use_container_width=True)

# --- TAB 3: Incident Triage ---
with tab3:
    st.subheader("Run Automated Incident Diagnostic Triage")

    sample_inc = {
        "incident_id": "INC-DEMO-999",
        "root_cause": {
            "service": "payment-db",
            "metric": "connection_pool_usage",
            "fault_type": "connection_pool_exhausted"
        },
        "symptoms": [
            {"service": "payment-api", "metric": "error_rate", "value": 0.45, "baseline": 0.01},
            {"service": "payment-db", "metric": "connection_pool_usage", "value": 0.99, "baseline": 0.15}
        ]
    }

    if st.button("Run Diagnostic Triage on Payment Incident"):
        analysis = analyzer.analyze_incident(current_g, sample_inc)
        st.success(f"Isolated Root Cause: {analysis['root_cause']['service']} ({analysis['root_cause']['fault_type']})")
        st.info(f"Recommended Action: {analysis['recommended_action']}")
        st.metric("Total MTTR", f"{analysis['mttr_s']} seconds")

        st.write("### Decision Trace Emitted:")
        df_trace = pd.DataFrame(analysis["decision_trace"])
        st.dataframe(df_trace, use_container_width=True)

# --- TAB 4: Evolution Control Engine ---
with tab4:
    st.subheader("Execute Closed-Loop Graph Evolution Cycle")

    if st.button("Run Auto-Evolution Cycle (Modules 4 ➔ 5 ➔ 6)"):
        with st.spinner("Extracting experience, generating candidate mutations, scoring & verifying..."):
            # Simulate 5 traces
            sim_traces = []
            for _ in range(5):
                res = analyzer.analyze_incident(current_g, sample_inc)
                sim_traces.append(res["decision_trace"])

            exp_rec = extractor.extract_experience(sim_traces)
            evo_res = evolution_engine.evolve_graph(current_g, exp_rec)

            candidate_g = DiagnosticGraph.from_dict(evo_res["selected_graph"])
            v_report = verifier.verify_candidate_graph(current_g, candidate_g, [sample_inc])

            if v_report["status"] == "APPROVED":
                st.session_state["current_graph"] = candidate_g
                repo.save_graph_version(candidate_g, evo_res["selected_transformation"], evo_res["best_score"], "APPROVED")
                repo.log_mttr_point(candidate_g.version_id, res["mttr_s"])
                st.balloons()
                st.success(f"Successfully evolved graph to {candidate_g.version_id}! Transformation: {evo_res['selected_transformation']}")
            else:
                st.error(f"Graph evolution rejected by verification gate: {v_report['rejection_reasons']}")

    if st.button("Reset to Default Payment Seed Graph"):
        st.session_state["current_graph"] = create_payment_seed_graph()
        st.success("Reset active graph to baseline PaymentSeedGraph.")
