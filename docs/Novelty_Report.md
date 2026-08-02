# Novelty Report: Operational Decision Graph Architecture

---

## Assumptions Across Prior Art

### GraphMind (Microsoft, arXiv 2605.17617, 2026)
**Assumption:** Workflow graph topology is fixed after construction; only edge/node weights evolve via ATR reinforcement and decay.

### EoG / Explanations over Graphs (IBM Research, arXiv 2601.17915, 2026)
**Assumption:** Dependency graph is given and static; explanatory graph is regenerated per investigation; no cross-incident persistence.

### MetaRCA (arXiv 2603.02032, 2026)
**Assumption:** Meta Causal Graph is defined at metadata level; evolution is belief weight updates only, not structural changes.

### DBAIOps (VLDB 2026)
**Assumption:** Graph only grows (add-only enrichment via synonym edges); never prunes, splits, merges, or reorders.

### Log2Graph (IJACSA 2025)
**Assumption:** Graph represents system topology (services, dependencies), not diagnostic reasoning; sliding window expiration replaces structural evolution.

### TopoEvo (arXiv 2605.15611, 2026)
**Assumption:** Memory stores compact records (topology fingerprints + symptom tokens), not a graph structure; evolution is encoder/weight adaptation.

### ESRO (Salesforce, arXiv 2309.07230, 2023)
**Assumption:** Graph is constructed offline and remains static after training; no online evolution mechanism.

### RAG+GNN+LLM (FAIR 2025)
**Assumption:** Graph is regenerated per incident; incremental learning updates model parameters, not graph structure.

### ProPlay (arXiv 2606.12780, 2026)
**Assumption:** Procedure graph for game/RL environments; not applicable to cloud operational diagnosis.

### MAGE (arXiv 2605.10064, 2026)
**Assumption:** General agent reasoning domain; no cloud-specific diagnostic graph concept.

### GSEM (arXiv 2603.22096, 2026)
**Assumption:** Medical domain; evolution updates node quality + edge weights only, not structural transformations.

### SEARL (arXiv 2604.07791, 2026)
**Assumption:** Tool graph for agentic learning; graph represents tool dependencies, not diagnostic reasoning.

### Graph-PReFLexOR (arXiv 2502.13025, 2025)
**Assumption:** Scientific discovery domain; add-only node/edge expansion; no remove/split/merge operations.

### AFlow / Evoflux / ComfyClaw
**Assumption:** Agent workflow graphs (procedural, not diagnostic); mutation/crossover for structure search; no cloud operational context.

### Dynamic Skills Survey (2026)
**Assumption:** Abstract mathematical framework; not applied or evaluated in any specific domain.

### NetCause (arXiv 2606.13543, 2026)
**Assumption:** Counterfactual simulation is for root cause ranking, not for guiding graph evolution.

### CPS Bigraph (Nature Sci Rep 2025)
**Assumption:** Formal verification applies to physical system architecture, not diagnostic reasoning graphs.

### Self-Play Papers (SSP, SeRL, MAGE)
**Assumption:** Self-play is for training LLM agents, not for evolving diagnostic graph structures.

---

## 1. Closest Patent

**US12360878B1 — "Addressing root cause anomaly" (Granted 2025)**

| Dimension | Detail |
|---|---|
| **Similarity** | Graph-based dependency analysis for RCA. Generates a graph from infrastructure templates + metrics, determines dependencies between nodes, uses traversal algorithms to pinpoint root cause anomalies. Shares the concept of a graph as primary diagnostic artifact. |
| **Difference** | Graph is a static dependency topology, not a diagnostic reasoning graph. No evolution mechanism — graph is constructed once from infrastructure templates. No structural transformations. No cross-incident reuse. The graph encodes "what depends on what" not "what the system believes about the failure." |
| **Risk** | **LOW.** Static dependency graph is conceptually distant from an evolving diagnostic reasoning graph. |

**Next closest: US11271795B2 — "Systems and methods for proactive network operations" (Granted 2022)**

| Dimension | Detail |
|---|---|
| **Similarity** | AI-driven feedback loop for adaptive network control. Includes RCA, prescriptive actions, and feedback mechanism. Shares the concept of learning from operational experience. |
| **Difference** | No graph artifact. Feedback loop updates rules/policies, not a graph structure. No diagnostic reasoning graph at all. |
| **Risk** | **LOW.** No graph concept, no structural evolution. |

**Third closest: US8001527B1 — "Automated root cause analysis of problems" (Expired 2011)**

| Dimension | Detail |
|---|---|
| **Similarity** | Knowledge base maps known problems to features/conditions. Early (2011) prior art for automated RCA using structured knowledge. |
| **Difference** | Knowledge base is a flat mapping, not a graph. No evolution (static rules). No structural transformations. Significantly predates modern AIOps concepts. |
| **Risk** | **VERY LOW.** Too old, too different. |

---

## 2. Closest Paper

**GraphMind — Microsoft Research (arXiv 2605.17617, May 2026)**

| Dimension | Detail |
|---|---|
| **Similarity** | Covers 4/5 invention criteria. Workflow graph as primary artifact representing diagnostic actions/procedures (C1, C2). Adaptive Traversal Reinforcement (ATR) evolves graph from execution feedback (C3). Evolved graphs reused for future incidents (C5). Deployed on 4 production cloud services. 12-week field study. 98.5% mitigation reach. Expert score 4.95/5. |
| **Difference** | ATR is weight-based reinforcement + decay, NOT structural transformation (C4 ⚠️). Graph topology is fixed after construction. Edge/node weights change but no add/remove/reorder/split/merge. The graph represents procedural workflows (what actions to take) not diagnostic beliefs (what entities are faulty). 8× less retrieval context than Trace-RAG baseline. |
| **Risk** | **HIGH.** Closest single prior art. 4/5 criteria met. The main defense: workflow graphs ≠ diagnostic reasoning graphs, and weight updates ≠ structural transformations. But for obviousness purposes, this is the most threatening reference. |

**EoG — IBM Research (arXiv 2601.17915, Jan 2026)**

| Dimension | Detail |
|---|---|
| **Similarity** | Perfect match on C1 and C2. Explanatory Graph G_S stores beliefs (Origin/Symptom/Healthy) — explicitly a diagnostic reasoning graph, not topology. "Operational-graph abstraction for investigations under partial observability." Semantic Belief Propagation (SBP) revises beliefs during investigation. 7× higher Majority@k F1 on ITBench. |
| **Difference** | Fails C3 (evolution is intra-incident only — no cross-incident persistence), C4 (belief revision, not structural transformation), C5 (each investigation starts fresh). The graph lasts only for the duration of one investigation. |
| **Risk** | **MEDIUM.** Perfect on core concept (diagnostic reasoning graph) but lacks all evolution/reuse elements. Dangerous in combination with GraphMind for obviousness arguments. |

**MetaRCA (arXiv 2603.02032, Mar 2026)**

| Dimension | Detail |
|---|---|
| **Similarity** | Meta Causal Graph (MCG) is a reusable causal knowledge base (C1 ✓). Evidence-driven belief evolution algorithm with Bayesian updates (C3 ✓). MCG reused across incidents via online instantiation (C5 ✓). Surpasses strongest baseline by 29pp (service-level) and 48pp (metric-level). |
| **Difference** | Graph defined at metadata/abstract level — instantiated into localized graphs per incident. Evolution is weight/confidence updates (Causal Belief Score), not structural. No add/remove/split/merge (C4 ✗). Cross-system accuracy >80%. |
| **Risk** | **MEDIUM-HIGH.** Reusable evolving causal graph is very close conceptually. Weight-based evolution is the key distinction. |

**DBAIOps — Tsinghua (PVLDB Vol 19, 2026)**

| Dimension | Detail |
|---|---|
| **Similarity** | ExperienceGraph is a heterogeneous O&M knowledge graph (C1 ✓). Captures diagnosis knowledge/procedures (C2 ✓). Graphs enriched incrementally with new anomaly scenarios — "over 2,000 vertices and 800+ anomaly scenarios for 25 database systems" (C3 ✓). ExperienceRetriever explores graph for new anomalies (C5 ✓). |
| **Difference** | Evolution is ADD-ONLY (enrichment adds synonym edges). Never removes, splits, merges, or reorders. Graph only grows. Semi-automatic construction requires manual validation. No structural transformation (C4 ✗). |
| **Risk** | **MEDIUM-HIGH.** Operational knowledge graph with incremental growth but no structural transformation. |

**TopoEvo (arXiv 2605.15611, May 2026)**

| Dimension | Detail |
|---|---|
| **Similarity** | Self-Evolving Mechanism refreshes hierarchical incident memory (C3 ✓). Memory stores validated hypotheses with evidence (C2 partial). Evolved memory reused for future incidents (C5 ✓). Conservative test-time adaptation. |
| **Difference** | Not graph-based. Memory stores "compact records consisting of candidate-centric topology fingerprints, symptom-token sets." No graph structure at all. Evolution is encoder weight adaptation, not graph transformation (C1, C4 ✗). |
| **Risk** | **MEDIUM.** Self-evolution concept is relevant, but different artifact type weakens the threat. |

---

## 3. Products

No commercial product surveyed implements the full architecture. None even comes close.

| Product | Graph Type | Evolution | Reuse | Risk |
|---|---|---|---|---|
| **Datadog** | Watchdog + topology maps | None (static alerts) | Anomaly detection only | VERY LOW |
| **Dynatrace** | Davis AI + Smartscape topology | None (static dependency map) | Baseline comparison only | VERY LOW |
| **Grafana** | No graph artifact | None | None | VERY LOW |
| **Prometheus** | No graph artifact | None | None | VERY LOW |
| **OpenTelemetry** | No graph (instrumentation only) | None | None | VERY LOW |
| **New Relic** | NRQL + topology | None | Historical comparison only | VERY LOW |
| **Splunk** | ITSI + KPI base | None | Static thresholding | VERY LOW |
| **Rootly** | KG from incident data | Graphify builds static KG | Query-based retrieval | LOW |
| **DrDroid** (claimed) | Experience graph | "Every alert strengthens graph" | Yes (claimed) | LOW-MEDIUM (unverifiable claims) |

**Verdict:** Products pose no threat. They lack diagnostic reasoning graphs, structural evolution, and cross-incident reuse of graph structure. The closest (Rootly) builds a static knowledge graph from incidents — no evolution, no reasoning.

---

## 4. Novelty Score

| Criterion | Score (0–10) | Justification |
|---|---|---|
| C1: Graph represents diagnostic reasoning (not topology) | 4 | EoG has this with the Explanatory Graph. Not novel alone. |
| C2: Graph is primary artifact for investigation | 5 | GraphMind, DBAIOps, MetaRCA all use graphs as primary artifacts. Not novel alone. |
| C3: Graph evolves after incidents | 4 | GraphMind (ATR), MetaRCA (Bayesian), TopoEvo (memory refresh), DBAIOps (enrichment). Evolution concept is well-established. Not novel alone. |
| C4: Evolution through structural transformations | 9 | NO prior art does this for diagnostic reasoning graphs. Structural ops exist in agent workflows (AFlow/Evoflux) and abstract theory (Dynamic Skills) but never on diagnostic graphs. HIGHLY NOVEL. |
| C5: Evolved graphs reused | 5 | GraphMind, DBAIOps, MetaRCA all reuse evolved graphs. Not novel alone. |
| **Combined: C1–C5 architecture** | **7** | The specific combination is novel — no single prior art has all 5. But faces obviousness risk because individual elements exist separately and could be combined. |

**Overall Novelty Score: 6.5 / 10**
*Moderately novel. The specific architecture combination is new, but individual components are well-established. Strongest claim is C4 (structural transformations on diagnostic reasoning graphs) which is genuinely unexplored.*

---

## 5. Remaining White Space

### Identified Gap
No prior art combines diagnostic reasoning graphs + structural transformations + cross-incident reuse within a single architecture.

### White Space Map

| Axis | Explored | Unexplored |
|---|---|---|
| **Graph type** | Workflow/procedure graphs (GraphMind), Causal metadata graphs (MetaRCA), Topology graphs (DBAIOps, Log2Graph), Belief graphs (EoG) | **Hybrid belief+procedure graphs** that encode both diagnostic state AND investigative actions in one unified graph |
| **Evolution method** | Weight reinforcement (GraphMind), Add-only enrichment (DBAIOps), Belief updates (MetaRCA, GSEM), Weight decay (GraphMind), Random mutation (AFlow) | **Information-guided structural transformation** — choose add/remove/split/merge operations based on expected information gain |
| **Verification** | None — transformations applied blindly | **Formal pre-application verification** — prove consistency, soundness, completeness before committing a transformation |
| **Learning signal** | Real incidents only (all systems) | **Self-play counterfactual simulation** — generate synthetic fault scenarios to proactively evolve the graph |
| **Domain** | Cloud ops (most), medical (GSEM, GraphDx), science (Graph-PReFLexOR), games (ProPlay) | **Cross-domain transfer** — evolve graph in one system, adapt and transfer to a different system architecture |
| **Multi-objective** | Single objective — accuracy (all) | **Pareto-optimal evolution** — simultaneously optimize accuracy, speed, cognitive load, robustness |
| **Operator collaboration** | None (fully automated) | **Human-machine collaborative graph evolution** — operator validates/steers structural transformations |
| **Graph governance** | None | **Meta-cognitive monitoring** — a higher-order controller that detects graph stagnation, overfitting, or drift and triggers exploratory transformations |
| **Multi-perspective fusion** | Single graph (all) | **Consensus-based multi-graph fusion** — multiple graphs per operator team/AI system, periodically merged |
| **Active probing** | Passive incident waiting (all) | **Active uncertainty reduction** — proactively probe the system to resolve uncertainty in graph structure |

### Highest-Value White Space

1. **Counterfactual-guided structural evolution with information gain** — closest unexplored extension
2. **Self-play graph evolution** — simulate millions of faults to evolve without waiting
3. **Formally verified graph transformations** — provably correct evolution
4. **Human-machine collaborative graph refinement** — operator-in-the-loop structural changes with explanations

---

## 6. Patent Risk

| Factor | Assessment |
|---|---|
| **Single prior art invalidates?** | NO — no single document covers all 5 criteria |
| **Obviousness combination risk?** | **MEDIUM-HIGH** — GraphMind (4/5) + EoG (diagnostic reasoning) + Dynamic Skills/Agent Workflow Evolution (structural ops) could be argued to teach all elements |
| **Best obviousness defense** | GraphMind's workflow graphs encode procedures (what actions to execute), while EoG's belief graphs encode diagnostic state (what entities are faulty). These serve fundamentally different purposes. Structural transformations on procedural graphs do not obviously transfer to belief/semantic graphs — restructuring a belief graph would break propagation paths and invalidate beliefs. A person skilled in the art would NOT be motivated to apply workflow graph mutations to diagnostic belief graphs. |
| **Product prior art risk** | NONE — no commercial product close |
| **Patent thicket risk** | LOW — few competing patents in this specific niche |

### Overall Patent Risk: MEDIUM

---

## 7. Recommendations

### Should we pivot, proceed, or modify?

**RECOMMENDATION: PROCEED with NARROW CLAIMS**

### Rationale

| Option | Assessment |
|---|---|
| **Pivot?** | ❌ Not necessary. The architecture is novel enough to pursue, especially with C4 (structural transformations) as the centerpiece. Pivot would waste the work done. |
| **Proceed as-is?** | ❌ Risky. Broad claims covering "graph evolves after incidents" would be rejected against GraphMind/MetaRCA/DBAIOps. |
| **Proceed with narrow claims?** | ✅ **Recommended.** Focus claims on the specific mechanism that is genuinely novel. |

### Recommended Claim Strategy

**Claim 1 (core novel element):** A diagnostic reasoning graph where each node stores a belief state (cause/symptom/healthy) and where the graph undergoes explicit structural transformations — at least one of: add node, remove node, split node, merge node, reorder nodes — after each incident.

**Claim 2 (differentiator from GraphMind):** The structural transformation is selected based on expected information gain computed via counterfactual simulation over historical incidents, distinguishing it from weight-based reinforcement (GraphMind) and growth-only enrichment (DBAIOps).

**Claim 3 (differentiator from EoG):** The evolved graph is persisted and retrieved as the starting state for future incident investigations, enabling cross-incident learning.

**Claim 4 (differentiator from all):** The method further comprising verifying that the structural transformation preserves at least one property selected from: diagnostic consistency, belief soundness, or causal completeness before applying the transformation to the graph.

### Differentiation from Closest Prior Art

| Prior Art | How to Distinguish in Claims |
|---|---|
| **GraphMind** | "Wherein the graph encodes diagnostic beliefs for each entity, not procedural actions; and wherein evolution comprises at least one structural transformation selected from add, remove, split, merge, or reorder" |
| **EoG** | "Wherein the evolved graph is persisted beyond a single investigation and retrieved as an initial state for a subsequent investigation" |
| **MetaRCA** | "Wherein evolution comprises structural transformation of the graph topology, not only updating belief weights or confidence scores on existing edges" |
| **DBAIOps** | "Wherein evolution comprises at least one operation that reduces the graph, selected from remove, split, merge, or reorder, and is not limited to additive enrichment" |

### Avoid These Claim Elements

❌ "A graph that evolves" — too broad, rejected against GraphMind ATR
❌ "A diagnostic reasoning graph" — too broad, rejected against EoG
❌ "Reusing knowledge across incidents" — too broad, rejected against GraphMind/DBAIOps/MetaRCA
❌ "Structural transformation" without specifying what kind — could be rejected against Dynamic Skills abstract theory

### Timeline Risk

| Year | Risk Level | Reason |
|---|---|---|
| 2026 | LOW | Peer papers (GraphMind, EoG, MetaRCA) are very recent; the combination is still novel |
| 2027 | MEDIUM | Follow-up work may close the gap (e.g., GraphMind v2 with structural ops) |
| 2028+ | HIGH | The field is moving fast; file soon or risk prior art catching up |

### Final Verdict

| Dimension | Rating |
|---|---|
| **Patentability** | Moderate (6.5/10). Novel but faces obviousness risk. |
| **Best filing date** | ASAP (2026). The field is moving rapidly. |
| **Claim scope** | NARROW — focus on structural transformations of diagnostic reasoning graphs with verification |
| **Key differentiator** | C4 (structural transformation) + verification — this is genuinely unexplored |
| **Risk of rejection** | Medium. Strongest examiner argument: obviousness combination of GraphMind + EoG + Dynamic Skills. Strongest defense: workflow graphs ≠ diagnostic belief graphs; transformation methods are not interchangeable. |
