# Phase 1: Foundation & Simulator

Create the foundation structure and build the synthetic incident simulator (`/simulator/`) to generate realistic topology diagrams, metrics, alerts, symptoms, and decision paths.

## User Review Required

> [!IMPORTANT]
> The simulator will generate synthetic microservice topologies and propagate faults. We need to define:
> 1. The default network configurations (e.g., service types like `gateway`, `service`, `database`).
> 2. Specific failure/fault types (e.g., `connection_pool_exhausted`, `cpu_saturation`, `memory_leak`, `network_delay`).
> 3. Suboptimal paths: how we generate realistic suboptimal paths (e.g. searching irrelevant components or following generic checks).

Please review the proposed architecture and CLI interface.

## Proposed Changes

### Simulator Component

#### [NEW] [topology_generator.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/topology_generator.py)
Generates a microservice topology (DAG) using NetworkX.
- Implements a `TopologyGenerator` class.
- Configurable number of services.
- Assigns types (e.g., frontend, API gateway, backend service, database, cache) and dependencies.
- Assigns typical metrics to check for each type (e.g., database: query latency, connection pool; service: error rate, latency, CPU).

#### [NEW] [fault_injector.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/fault_injector.py)
Simulates failure events and propagates symptoms through the topology.
- Implements a `FaultInjector` class.
- Injects a primary root cause (e.g. `connection_pool_exhausted` on a database).
- Propagates anomalies to dependent upstream services (e.g. database latency causes backend service latency, backend service latency causes gateway errors).
- Returns list of anomalous symptoms with values, baselines, and timestamps.

#### [NEW] [trace_recorder.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/trace_recorder.py)
Generates and records optimal and suboptimal diagnostic paths.
- **Optimal Path**: A direct traversal from the alarm symptom to the root cause using logical diagnostic steps (e.g. checking dependency metrics).
- **Suboptimal Path**: Simulates a traditional static checklist approach (e.g., checking unrelated services/metrics, wasting time and computing resources) to establish a baseline.
- Records info gain and time taken per step.

#### [NEW] [dataset_exporter.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/dataset_exporter.py)
Handles exporting incident data to structured JSON files in `/data/`.
- Validates the generated object against the output JSON schema.
- Handles file I/O operations and directories creation safely.

#### [NEW] [incident_simulator.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/incident_simulator.py)
The orchestrator class `IncidentSimulator` that binds topology generation, fault injection, path recording, and exporting together.

#### [NEW] [__init__.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/__init__.py)
Exposes the clean public APIs for the simulator package.

#### [NEW] [generate.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/simulator/generate.py)
Command line interface for generating datasets.
- Parses options: `--count`, `--services`, `--output`.
- Initializes and executes `IncidentSimulator`.

### Test Component

#### [NEW] [test_simulator.py](file:///media/prasath/Local%20disk%28E:%29/Softwares/Obsidian/My%20Vault/Cloud%20Project/tests/test_simulator.py)
Unit and integration tests for the simulator components to ensure:
- Graph generation creates valid DAGs.
- Fault propagation flows correctly.
- Outputs conform exactly to the required JSON schema.

## Verification Plan

### Automated Tests
- Run `pytest tests/test_simulator.py` to verify simulator code correctness.

### Manual Verification
- Run `python simulator/generate.py --count 10 --services 15 --output data/test_incidents.json` and inspect the generated JSON file for schema compatibility.
