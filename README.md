# Adaptive Diagnostic Reasoning Framework for Autonomous Cloud Operations

A self-evolving AIOps diagnostic framework that represents diagnostic knowledge as a **Directed Reasoning Graph** (NetworkX), investigates cloud microservice outages, extracts empirical Shannon entropy & Information Gain from decision traces, and **structurally mutates the graph** (ADD, REMOVE, SPLIT, MERGE, REORDER) using multi-objective optimization to continuously reduce Mean Time to Resolution (MTTR).

---

## 📋 Prerequisites

- **Python**: Version 3.10, 3.11, or 3.12+
- **Git**: Installed on system
- **OS**: Linux, macOS, or Windows (WSL / Powershell / CMD)

---

## 🚀 Quickstart Guide: Running on Another Machine

### Step 1: Clone the Repository
```bash
git clone https://github.com/Prasath-27706/adaptive-diagnostic-reasoning-framework.git
cd adaptive-diagnostic-reasoning-framework
```

### Step 2: Create and Activate a Virtual Environment

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧪 Step 4: Verify the Installation (Run Tests)

Execute the comprehensive system test suite (24 unit & integration tests across all 7 modules):

```bash
PYTHONPATH=. python verify_all.py
```

Expected output:
```text
Ran 24 tests in 0.48s
OK
✅ All 24 Unit Tests Passed Successfully.
```

---

## 🖥️ Step 5: Launch the Interactive Streamlit UI Dashboard

Launch the Streamlit UI dashboard to view visual microservice topologies, interactive decision graphs, before-vs-after storyboards, and 1-click incident triage:

```bash
streamlit run modules/m7_repository/dashboard.py
```

Then open your browser at **`http://localhost:8501`**.

---

## ⚡ Step 6: Run the Benchmark Simulation Script (CLI)

To run a closed-loop evolution benchmark across 50 simulated payment subsystem incidents:

```bash
python run_demo.py --incidents 50 --batch-size 10
```

Results will be exported to `data/benchmark_results.json`.

---

## 🔌 Step 7: (Optional) Run the FastAPI REST Server

To start the REST API server for external telemetry ingestion and graph endpoints:

```bash
uvicorn modules.api:app --reload --port 8000
```

Access automatic OpenAPI documentation at **`http://localhost:8000/docs`**.

---

## 🏗️ Architecture Overview

- **Module 1**: Telemetry Collection API (`modules/m1_collection/`)
- **Module 2**: Diagnostic Reasoning Graph Engine (`modules/m2_graph/`)
- **Module 3**: Incident Analyzer Engine (`modules/m3_analyzer/`)
- **Module 4**: Experience Extractor (`modules/m4_extractor/`)
- **Module 5**: Evolution Decision Engine (`modules/m5_decision_engine/`)
- **Module 6**: Graph Verification Engine Safety Gate (`modules/m6_verification/`)
- **Module 7**: Operational Knowledge Repository & UI (`modules/m7_repository/`)

---

## 📄 License & Patent Information

For patent details and technical specifications, refer to [`docs/PATENT_DISCLOSURE.md`](docs/PATENT_DISCLOSURE.md) and [`docs/Novelty_Report.md`](docs/Novelty_Report.md).
