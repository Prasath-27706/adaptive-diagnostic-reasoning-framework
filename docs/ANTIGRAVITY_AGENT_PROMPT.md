# Antigravity Agent Prompt — Adaptive Diagnostic Reasoning Framework

You are an Antigravity agent tasked with building a complete cloud computing project from scratch. Read this entire prompt carefully before starting. It contains the full project context, the architecture, the build plan, and your instructions.

---

## PART 1: PROJECT CONTEXT (Read this first to understand WHAT we're building)

### The Problem

Cloud operations teams today face a fundamental limitation: when a microservice fails, the diagnostic system starts from scratch every single time. It follows a fixed checklist — check CPU, check memory, check network, check database — even if the last 10 incidents were all caused by the database. There is no memory of past investigations. There is no learning. Every incident is treated as if it's the first.

Existing AIOps systems (Datadog Watchdog, Dynatrace Davis, Grafana, Prometheus, OpenTelemetry) collect telemetry but have zero cross-incident learning. The closest research systems (GraphMind, EoG, MetaRCA, DBAIOps, OpsAgent) all fall short:
- **GraphMind** (Microsoft) — evolves edge weights only, graph topology is fixed
- **EoG** (IBM) — belief graphs but each investigation starts fresh
- **MetaRCA** — updates belief scores only, no structural changes
- **DBAIOps** — add-only enrichment, never removes or restructures
- **OpsAgent** — evolves agent policy weights, not graph structure

None of them perform **structural transformations** (add/remove/split/merge/reorder nodes) on a diagnostic reasoning graph.

### The Solution

We are building a **7-module adaptive diagnostic reasoning framework** that:

1. Represents diagnostic knowledge as a **directed graph** (not a topology map — a reasoning graph)
2. Uses that graph to **investigate incidents** by traversing hypothesis nodes
3. After each incident, **extracts experience** from the investigation trace
4. Generates candidate **graph mutations** (add/remove/split/merge/reorder nodes)
5. **Scores each candidate** using multi-objective optimization (information gain, investigation time, diagnostic confidence, historical success rate, graph complexity)
6. **Verifies** the mutated graph for structural soundness AND performance improvement before persisting
7. **Persists** the evolved graph and loads it for the next incident — creating a closed-loop learning system

### The Architecture (7 Modules)

```
┌─────────────────────────────────────────────────────────────────────┐
│ Module 1: Telemetry Collection                                      │
│ (Prometheus + OpenTelemetry + K8s → FastAPI ingestion)              │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Module 2: Diagnostic Reasoning Graph (NetworkX DiGraph)             │
│ Nodes = hypothesis checks · Edges = conditional ordering            │
│ NOT a topology map — encodes diagnostic reasoning steps             │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Module 3: Incident Analyzer ★                                       │
│ Traverses graph · Validates hypotheses · Emits Decision Trace       │
│ Output: root cause + recovery action + full investigation path      │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Module 4: Experience Extractor (OFFLINE) ★                          │
│ Parses Decision Trace · Computes Information Gain per node          │
│ Detects redundant steps · Mines recurring patterns                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Module 5: Evolution Decision Engine ★★★ (CORE NOVELTY)              │
│ ┌─────────────────────┐   ┌──────────────────────────────────────┐  │
│ │ Candidate Generator │ → │ Multi-Objective Scorer               │  │
│ │ (ADD/REMOVE/SPLIT/  │   │ w1*IG + w2*(1/time) + w3*confidence │  │
│ │  MERGE/REORDER)     │   │ + w4*history - w5*complexity         │  │
│ └─────────────────────┘   └──────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Module 6: Graph Verification ★                                       │
│ Structural: cycles · reachability · completeness · consistency      │
│ Performance: replay historical incidents, check MTTR no regression  │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Module 7: Operational Knowledge Repository                          │
│ PostgreSQL · Versioned graphs · Transformation history · MTTR logs  │
│ Streamlit dashboard · Grafana metrics                               │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
              ← ← ← FEEDBACK LOOP ← ← ← (loads latest graph for next incident)
```

### Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python 3.12 | NetworkX, FastAPI, ML ecosystem |
| API Framework | FastAPI | Async, auto-docs, high perf |
| Graph Engine | NetworkX | Mature, DAG algorithms built-in |
| Database | PostgreSQL + JSONB | Versioning, JSON query support |
| Metrics | Prometheus + OpenTelemetry | Industry standard telemetry |
| UI | Streamlit + Grafana | Quick dashboards |
| Container | Docker | Reproducible builds |
| Orchestration | Kubernetes (Minikube) | Local dev cluster |

### Novelty Claims (for Patent)

- **C1:** Graph represents diagnostic reasoning beliefs, not service topology
- **C2:** Graph is the primary artifact used for incident investigation
- **C3:** Graph evolves structurally after incidents (not just weight updates)
- **C4:** ★ Evolution uses structural transformations (add/remove/split/merge/reorder) selected by multi-objective scoring
- **C5:** Evolved graphs are persisted and reused across incidents

### Patent Filing Context

- Filing through **VIT Vellore IPR cell** → Indian Patent Office
- **Section 3(k)** of Indian Patents Act excludes algorithms/business methods
- All framing must emphasize **technical effect**: reduced MTTR, fewer redundant DB queries, lower CPU during diagnosis
- NEVER describe as "improves trading" or "algorithm" — describe as "method for computing system to dynamically reconfigure diagnostic procedures"

---

## PART 2: BUILD PLAN (The roadmap for HOW to build it)

Read the file `ANTIGRAVITY_BUILD_PLAN.md` in the project root. This contains the complete 9-phase build plan with specific tasks, deliverables, dataset requirements, algorithm specs, and success metrics.

**Key files already in the project folder:**
- `architecture_diagram.html` — visual architecture reference
- `presentation.html` — slide deck with problem/solution narrative
- `Novelty_Report.md` — prior art comparison
- `prior_art_database.json` — analysis of 81 documents
- `Cloud_Prior_Art_Analysis.xlsx` — capability matrices
- `Claude-Cloud computing project patent filing.md` — full conversation history with design decisions

---

## PART 3: YOUR INSTRUCTIONS

### Your Task

Start building this project by executing **Phase 1** (Foundation & Simulator) as defined in the build plan. Work through each phase sequentially.

### What to Build First (Phase 1)

Create the following structure and files in the project folder:

```
/simulator/
  __init__.py
  topology_generator.py    — Generates random microservice DAGs using NetworkX
  fault_injector.py        — Injects failures, propagates symptoms through topology
  trace_recorder.py        — Records optimal + suboptimal investigation paths
  dataset_exporter.py      — Exports to structured JSON schema
  incident_simulator.py    — Main orchestrator class
  generate.py              — CLI entry point (argparse: --count, --services, --output)
/data/                     — Generated datasets (gitignored)
/tests/
  test_simulator.py
```

### Output Schema Per Incident

```json
{
  "incident_id": "INC-00001",
  "topology": {
    "nodes": [
      {"id": "frontend", "type": "service", "dependencies": ["api-gateway"]},
      {"id": "api-gateway", "type": "service", "dependencies": ["payment-svc", "order-svc"]}
    ],
    "edges": [
      {"source": "frontend", "target": "api-gateway", "protocol": "http"},
      {"source": "api-gateway", "target": "payment-svc", "protocol": "grpc"}
    ]
  },
  "root_cause": {
    "service": "payment-db",
    "metric": "query_latency_ms",
    "fault_type": "connection_pool_exhausted",
    "severity": "critical"
  },
  "symptoms": [
    {"service": "payment-api", "metric": "error_rate", "value": 0.45, "baseline": 0.01, "timestamp": "2026-07-29T10:00:05Z"},
    {"service": "order-svc", "metric": "p99_latency", "value": 5200, "baseline": 200, "timestamp": "2026-07-29T10:00:06Z"}
  ],
  "optimal_investigation_path": [
    {"step": 1, "node_id": "check:payment-api:error_rate", "check_type": "metric_query", "result": "anomaly", "info_gain": 0.0, "time_taken_s": 2},
    {"step": 2, "node_id": "check:payment-db:query_latency", "check_type": "metric_query", "result": "anomaly", "info_gain": 0.82, "time_taken_s": 2},
    {"step": 3, "node_id": "check:payment-db:connection_pool", "check_type": "db_status", "result": "exhausted", "info_gain": 0.18, "time_taken_s": 5}
  ],
  "suboptimal_paths": [
    [{"step": 1, "node_id": "check:frontend:cpu", "result": "normal", "info_gain": 0.0, "time_taken_s": 3},
     {"step": 2, "node_id": "check:frontend:memory", "result": "normal", "info_gain": 0.0, "time_taken_s": 3},
     {"step": 3, "node_id": "check:network:throughput", "result": "normal", "info_gain": 0.0, "time_taken_s": 5}]
  ],
  "mttr_s": 320,
  "services_affected": ["frontend", "payment-api", "order-svc"],
  "alert_metadata": {
    "severity": "P1",
    "source": "Prometheus AlertManager",
    "summary": "High error rate on payment-api"
  }
}
```

### Guidelines

- Write production-quality Python with type hints
- Every module gets a `__init__.py` with clean public API
- Use `argparse` for CLI tools, not hardcoded paths
- Write tests alongside code (pytest)
- Add docstrings to all public classes and methods
- Keep algorithms deterministic where possible (set random seeds)
- Log progress with Python's `logging` module
- Save generated datasets to `/data/` (add to `.gitignore`)

### After Phase 1

Once the simulator is complete and generating valid incident data, signal completion and wait for instructions to proceed to Phase 2.

---

**File reference:** `ANTIGRAVITY_BUILD_PLAN.md` (in same directory) for the complete phased plan covering all 9 phases with detailed steps, deliverables, and algorithm specifications.
