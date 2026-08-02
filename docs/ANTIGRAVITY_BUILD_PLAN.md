# Operational Decision Graph — Antigravity Build Plan

## 1. Antigravity Project Initialization

### AGENTS.md (Project Context for Antigravity)

```markdown
# Project: Adaptive Diagnostic Reasoning Framework for Autonomous Cloud Operations

## Overview
A 7-module system for self-evolving diagnostic reasoning in cloud incident management.
Core novelty: structural transformations (add/remove/split/merge/reorder) on diagnostic
belief graphs, decided by multi-objective scoring, gated by formal verification.

## Architecture
Telemetry Collection → Diagnostic Reasoning Graph → Incident Analyzer →
Experience Extractor → Evolution Decision Engine → Graph Verification →
Operational Knowledge Repository → (feedback loop back to graph)

## Tech Stack
- Python 3.12+, FastAPI, NetworkX, PostgreSQL, Streamlit, Docker
- Kubernetes (Minikube), Prometheus, OpenTelemetry, Grafana
- Google Antigravity CLI/SDK for agent orchestration

## Key Novelty Claims (for patent)
1. Diagnostic Reasoning Graph as primary artifact (not topology map)
2. Structural graph transformations after incidents
3. Multi-objective scoring for transformation selection
4. Formal two-part verification (structural + performance)
5. Cross-incident persistence and reuse

## Prior Art to Distinguish From
- GraphMind (Microsoft) — weight-only evolution, workflow graphs
- EoG (IBM) — belief graphs but intra-incident only
- MetaRCA — belief weight updates only
- DBAIOps — add-only graph enrichment
- OpsAgent — evolves agent weights/prompts, not graph structure

## Agents Role Definitions

### Agent: Full-Stack Developer
- Responsibility: Build all 7 modules end-to-end
- Prohibited: None
- Tools: Python, FastAPI, NetworkX, PostgreSQL, Streamlit
- Configuration: AGENTS.md for project context

### Agent: DevOps/Infra
- Responsibility: Kubernetes manifests, Docker, OpenTelemetry, Prometheus
- Prohibited: Core business logic changes
- Connection: Minikube, Docker Hub

### Agent: Patent Documenter
- Responsibility: Generate patent disclosure docs, novelty report
- Prohibited: Code changes
- Tools: Markdown, prior_art_database.json, Novelty_Report.md

## Folder Structure
/cloud-project/
  /agents/           — Antigravity agent configs & skills
  /modules/          — 7 module implementations
    /m1_collection/
    /m2_graph/
    /m3_analyzer/
    /m4_extractor/
    /m5_decision_engine/
    /m6_verification/
    /m7_repository/
  /infra/            — K8s, Docker, OTel configs
  /simulator/        — Incident simulator & synthetic data generator
  /docs/             — Patent docs, reports, architecture diagrams
  /tests/            — Unit, integration, e2e tests
  AGENTS.md
  README.md
```

---

## 2. Dataset Requirements

### 2.1 Synthetic Cloud Incident Dataset (Primary — You Build This)

Since real cloud incident data is proprietary (Datadog, PagerDuty etc.), you need a **synthetic incident simulator** that generates:

| Data Type | Generator | Format | Volume |
|-----------|-----------|--------|--------|
| **Service topology** | Random graph generator (NetworkX) with microservice patterns | JSON (nodes=services, edges=dependencies) | 20–50 services |
| **Incident traces** | Simulate fault propagation (e.g., DB down → payment fails → order fails) | JSON (ordered list of symptom-to-root-cause path) | 500–2000 incidents |
| **Telemetry signals** | Prometheus metrics with injected anomalies (latency spikes, error rates, CPU steal) | CSV / OpenMetrics | 100K+ data points |
| **Alert metadata** | Simulated PagerDuty-style alerts with severity, timestamp, service | JSON | 500–2000 alerts |
| **Decision traces** | Step-by-step investigation paths (what was checked, in what order, outcome) | JSON | 500 paths |

### 2.2 Public Benchmark Datasets

| Dataset | Source | What It Contains | Use In |
|---------|--------|------------------|--------|
| **AIOps Challenge 2023/2024** | http://www.aiops.cn | Real-world fault injection + traces | Validating Module 3 (Incident Analyzer) |
| **Google Cloud Trace (OpenTelemetry demo)** | https://opentelemetry.io/docs/demo/ | Multi-service K8s app with tracing | Module 1 telemetry ingestion |
| **Sock Shop (Weaveworks)** | https://microservices-demo.github.io/ | Demo microservices app | Deployment target for testing |
| **DeathStarBench** | https://github.com/delimitrou/DeathStarBench | Social network microservices | Stress testing, fault injection |
| **Alibaba Cluster Trace 2022** | https://github.com/alibaba/clusterdata | Production K8s cluster telemetry | Resource usage patterns |
| **TrainTicket (Fudan)** | https://github.com/FudanSELab/train-ticket | 41-microservice train booking system | Complex topology for graph evolution |

### 2.3 Data Generation Script (To Build)

An `incident_simulator.py` that:
1. Generates a random microservice topology graph
2. Selects a root cause node
3. Propagates symptoms along dependency edges
4. Generates alert + telemetry data
5. Records the ground-truth investigation path
6. Outputs structured JSON for all 7 modules

**Output schema per incident:**

```json
{
  "incident_id": "INC-00042",
  "topology": { "nodes": [...], "edges": [...] },
  "root_cause": { "service": "payment-db", "metric": "query_latency", "fault": "connection_pool_exhausted" },
  "symptoms": [
    { "service": "payment-api", "metric": "error_rate", "value": 0.45, "timestamp": "..." },
    { "service": "order-service", "metric": "p99_latency", "value": 5200, "timestamp": "..." }
  ],
  "optimal_investigation_path": [
    {"step": 1, "check": "payment-api:error_rate", "result": "anomaly", "info_gain": 0.0},
    {"step": 2, "check": "payment-db:query_latency", "result": "anomaly", "info_gain": 0.85},
    {"step": 3, "check": "payment-db:connection_pool", "result": "exhausted", "info_gain": 0.15}
  ],
  "suboptimal_paths": [...],
  "mttr": 320
}
```

---

## 3. Implementation Phases (Antigravity Agent Tasks)

### Phase 1: Foundation & Simulator (Week 1–2)

**Antigravity task:** `Build incident simulator and data pipeline`

| Step | Action | Output |
|------|--------|--------|
| 1.1 | Create project folder structure | `/modules/`, `/simulator/`, `/infra/`, `/docs/`, `/tests/` |
| 1.2 | Build `topology_generator.py` | Generates random microservice DAGs (NetworkX) |
| 1.3 | Build `fault_injector.py` | Injects failures, propagates symptoms |
| 1.4 | Build `trace_recorder.py` | Records investigation paths |
| 1.5 | Build `dataset_exporter.py` | Exports to JSON/CSV formats |
| 1.6 | Generate initial dataset | 1000+ incidents, save to `/data/` |

**Deliverable:** CLI command `python simulator/generate.py --count 1000` produces a full dataset.

---

### Phase 2: Module 1–2 — Telemetry + Reasoning Graph (Week 2–3)

**Antigravity task:** `Build telemetry ingestion and diagnostic reasoning graph`

| Step | Action | Output |
|------|--------|--------|
| 2.1 | Build Prometheus metric scraper | FastAPI endpoint that queries Prometheus |
| 2.2 | Build OpenTelemetry trace receiver | OTel Collector → FastAPI receiver |
| 2.3 | Implement `DiagnosticGraph` class | NetworkX DiGraph with typed nodes (hypothesis/check/action) |
| 2.4 | Implement graph serialization | JSON → PostgreSQL JSONB, versioned |
| 2.5 | Implement graph loading from repo | FastAPI endpoint `GET /graph/latest` |
| 2.6 | Build seed graph template | Initial diagnostic checklist template |

**Deliverable:** Running FastAPI server with `/graph/` endpoints, seed graph in Postgres.

---

### Phase 3: Module 3 — Incident Analyzer (Week 3–4)

**Antigravity task:** `Build incident analyzer with decision trace emission`

| Step | Action | Output |
|------|--------|--------|
| 3.1 | Implement graph traversal engine | BFS/DFS traversal with priority ordering |
| 3.2 | Build query executor | Prometheus HTTP API calls per node |
| 3.3 | Implement hypothesis validation | Check metric against threshold → pass/fail |
| 3.4 | Build Decision Trace recorder | Ordered list of steps with info gain |
| 3.5 | Implement root cause isolator | Last passing node before failure cascade |
| 3.6 | Build recovery action proposer | Predefined action templates matched to fault type |

**Deliverable:** `/analyze` endpoint that takes incident, returns root cause + decision trace.

---

### Phase 4: Module 4 — Experience Extractor (Week 4–5)

**Antigravity task:** `Build experience extractor (offline learning)`

| Step | Action | Output |
|------|--------|--------|
| 4.1 | Implement decision trace parser | Extract step sequences from Module 3 output |
| 4.2 | Build information gain calculator | `IG(step) = H(before) - H(after)` using entropy |
| 4.3 | Implement redundant step detector | Flag nodes with IG < threshold across N incidents |
| 4.4 | Build pattern miner | Detect recurring decision patterns (e.g., "DB always after network") |
| 4.5 | Implement experience record schema | Structured JSON: {incident, steps, gains, redundant, patterns} |
| 4.6 | Build batch processor | Process N incidents in one offline run |

**Deliverable:** `/experience/extract` endpoint + batch processor script.

---

### Phase 5: Module 5 — Evolution Decision Engine (Week 5–6) ★ CORE NOVELTY

**Antigravity task:** `Build evolution decision engine with multi-objective scoring`

| Step | Action | Output |
|------|--------|--------|
| 5.1 | Implement Candidate Transformation Generator | Rules: IF redundant → REMOVE; IF missing check → ADD; IF order wrong → REORDER |
| 5.2 | Implement ADD node operation | Insert new hypothesis node at optimal position |
| 5.3 | Implement REMOVE node operation | Delete node, reconnect edges |
| 5.4 | Implement SPLIT node operation | Split compound node into sub-checks |
| 5.5 | Implement MERGE node operation | Combine two nodes into one |
| 5.6 | Implement REORDER operation | Change priority weights on edges |
| 5.7 | Build Multi-Objective Scorer | `score = w1*IG + w2*(1/inv_time) + w3*confidence + w4*history_success + w5*(1/complexity)` |
| 5.8 | Implement scorer with default weights | w1=0.3, w2=0.2, w3=0.2, w4=0.2, w5=0.1 |
| 5.9 | Build candidate ranker | Sort candidates by score, pick top-1 |
| 5.10 | Build decision logger | Record: candidate chosen, scores, reasoning |

**Deliverable:** `/evolve` endpoint that produces candidate mutations with ranked scores.

---

### Phase 6: Module 6 — Graph Verification (Week 6–7)

**Antigravity task:** `Build two-part graph verification (structural + performance)`

| Step | Action | Output |
|------|--------|--------|
| 6.1 | Implement cycle detection | NetworkX `is_directed_acyclic_graph()` |
| 6.2 | Implement reachability analysis | BFS from root → all nodes reachable |
| 6.3 | Implement completeness check | Every path ends in a terminal/conclusive node |
| 6.4 | Implement consistency check | No orphan nodes, no duplicate nodes |
| 6.5 | Build Performance Verifier | Replay historical incidents → compare MTTR before vs after |
| 6.6 | Implement approval/rejection logic | Pass only if ALL structural + performance checks pass |
| 6.7 | Build rejection feedback channel | Notify Module 5 with reason for rejection |

**Deliverable:** `/verify` endpoint that returns APPROVED/REJECTED + detailed report.

---

### Phase 7: Module 7 — Operational Knowledge Repository (Week 7–8)

**Antigravity task:** `Build operational knowledge repository with versioning`

| Step | Action | Output |
|------|--------|--------|
| 7.1 | Design PostgreSQL schema | Tables: `graphs`, `graph_versions`, `incidents`, `transformations` |
| 7.2 | Build graph CRUD API | FastAPI endpoints for graph storage/retrieval |
| 7.3 | Implement versioning system | Each mutation creates new version_id |
| 7.4 | Build transformation history logger | Record: what changed, why, score, verification result |
| 7.5 | Implement MTTR tracking | `mttr_before`, `mttr_after` per version |
| 7.6 | Build Streamlit dashboard | Graph evolution viz, MTTR trends, incident timeline |
| 7.7 | Build Grafana integration | Export MTTR metrics to Prometheus → Grafana |

**Deliverable:** Full REST API + Streamlit dashboard for monitoring evolution.

---

### Phase 8: Full Pipeline Integration (Week 8–9)

**Antigravity task:** `Integrate all 7 modules into one end-to-end pipeline`

| Step | Action | Output |
|------|--------|--------|
| 8.1 | Build orchestrator script | Runs: Simulator → Graph → Analyzer → Extractor → Evolution → Verify → Repo |
| 8.2 | Implement feedback loop | After every 10 incidents, auto-trigger evolution cycle |
| 8.3 | Build end-to-end test | 50 incidents, verify MTTR decreases over time |
| 8.4 | Implement Grafana dashboard | Real-time: current graph, incident rate, MTTR, evolution count |
| 8.5 | Build demo script | Single command: `python run_demo.py --incidents 100` |
| 8.6 | Write README with setup instructions | |

**Deliverable:** End-to-end demo that shows MTTR decreasing with each evolution cycle.

---

### Phase 9: Patent Documentation (Week 9–10)

**Antigravity task:** `Generate patent disclosure and novelty documentation`

| Step | Action | Output |
|------|--------|--------|
| 9.1 | Build comparative analysis table | Ours vs GraphMind vs EoG vs MetaRCA vs DBAIOps vs OpsAgent |
| 9.2 | Write technical effect statement | Frame as "method for improving computing system diagnostic efficiency" (not "algorithm") |
| 9.3 | Write provisional patent disclosure | Problem, solution architecture, claims, diagrams |
| 9.4 | Generate claim language | Narrow claims focusing on C4 |
| 9.5 | Build section 3(k) compliance note | How to frame technical effect for Indian Patent Office |
| 9.6 | Write novelty report | Evidence-based: why no single prior art invalidates |
| 9.7 | Create architecture diagrams | Updated versions of architecture_diagram.html |

**Deliverable:** Complete patent disclosure package ready for faculty/IPR cell review.

---

## 4. Tech Stack Matrix

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend API** | FastAPI (Python 3.12) | All module endpoints |
| **Graph Engine** | NetworkX | In-memory diagnostic graph |
| **Database** | PostgreSQL + JSONB | Versioned graph persistence |
| **Metrics Collection** | Prometheus + OpenTelemetry | Telemetry sources |
| **Orchestration** | Kubernetes (Minikube) | Deploy microservices |
| **Visualization** | Streamlit + Grafana | Dashboards |
| **Container** | Docker | Packaging |
| **Simulation** | Custom Python | Incident generation |
| **Agent Platform** | Google Antigravity CLI/SDK | Orchestrate builds |

---

## 5. Key Algorithm Specifications

### 5.1 Information Gain Calculation

```
H(service) = -Σ p(fault_type) * log(p(fault_type))
IG(check) = H(before_check) - H(after_check)

Thresholds:
  IG > 0.15 → high value node (keep)
  0.05 < IG < 0.15 → medium (consider merge)
  IG < 0.05 → low value (candidate for removal)
```

### 5.2 Multi-Objective Scoring

```
score(T) = w1 * IG_norm(T)
         + w2 * (1 / investigation_time_norm(T))
         + w3 * confidence_norm(T)
         + w4 * historical_success_rate(T)
         - w5 * complexity_penalty(T)

Default weights: w1=0.30, w2=0.20, w3=0.20, w4=0.20, w5=0.10
```

### 5.3 Verification Checks

```
verify(graph):
  # Structural
  assert is_dag(graph)                    # No cycles
  assert all_nodes_reachable(graph)       # No orphans
  assert all_paths_terminal(graph)        # Complete
  assert no_duplicate_nodes(graph)        # Consistent

  # Performance
  mttr_before = replay_historical(graph_previous)
  mttr_after  = replay_historical(graph_candidate)
  assert mttr_after <= mttr_before * 1.1  # No >10% regression
```

---

## 6. Antigravity CLI Commands Reference

```bash
# Initialize project in Antigravity
agy init cloud-project --template python

# Create agent for each module
agy agent create m1-telemetry --model gemini-3.5-flash
agy agent create m2-graph --model gemini-3.5-flash
agy agent create m3-analyzer --model gemini-3.5-flash
agy agent create m4-extractor --model gemini-3.5-flash
agy agent create m5-evolution --model gemini-3.5-flash
agy agent create m6-verify --model gemini-3.5-flash
agy agent create m7-repo --model gemini-3.5-flash
agy agent create full-pipeline --model gemini-3.5-pro

# Set up sub-agent orchestration
agy project add-agent m1-telemetry
agy project add-agent m2-graph
agy project add-agent m3-analyzer
agy project add-agent m4-extractor
agy project add-agent m5-evolution
agy project add-agent m6-verify
agy project add-agent m7-repo

# Scheduled evolution run
agy schedule "Run evolution cycle" --cron "0 */6 * * *"

# Run full pipeline
agy task run "Build all 7 modules and integrate" --agent full-pipeline
```

---

## 7. Patent Filing Timeline

| Milestone | Date | Dependency |
|-----------|------|------------|
| Phase 1–3 complete (Modules 1–3 working) | Week 4 | Simulator + Analyzer |
| **Provisional patent application filed** | **Week 4–5** | Core concept documented |
| Phase 4–7 complete (all modules) | Week 8 | Full pipeline |
| Complete specification filed | Week 12–16 | Full results + claims |
| Prior art search update | Week 10 | updated_prior_art.json |
| Faculty review | Week 10–11 | Full disclosure package |

**⚠️ India Section 3(k) Strategy:**
- Never frame as "algorithm" or "business method"
- Always frame as: "A method for a computing system to dynamically reconfigure diagnostic investigation procedures to reduce computational overhead and improve fault detection accuracy"
- All claims must reference measurable technical effects: reduced MTTR, lower CPU usage during diagnosis, fewer redundant database queries

---

## 8. Success Metrics

| Metric | Baseline (No Evolution) | Target (After 100 Incidents) |
|--------|------------------------|------------------------------|
| MTTR | 300s | < 60s (5× improvement) |
| Redundant steps/incident | 8 | < 2 (4× reduction) |
| Graph size (nodes) | 20 | 15–30 (evolves, not just grows) |
| Verification pass rate | — | > 95% |
| Information gain per node | 0.05 avg | > 0.20 avg (4× better) |

---

## 9. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Synthetic data doesn't reflect real incidents | Use AIOPS Challenge + DeathStarBench as validation |
| Graph evolves incorrectly (divergence) | Performance verifier rejects regressions >10% |
| Patent examiner cites OpsAgent/DBAIOps | Explicitly distinguish: structural graph mutation ≠ weight/prompt evolution |
| Section 3(k) objection | Technical-effect framing in all docs; consult VIT IPR cell early |
| Modules too complex for timeline | Build v1 with REMOVE + REORDER only; ADD/SPLIT/MERGE as v2 |
