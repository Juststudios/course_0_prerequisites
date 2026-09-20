# Master Survey Report: Overall Curriculum Layout, Level 6 Networking, and TensorFlow Curriculum Design

**Agent Identity:** `teamwork_preview_explorer_survey_2`  
**Working Directory:** `/home/settings/Documents/pearl/.agents/teamwork_preview_explorer_survey_2`  
**Date:** 2026-09-17  
**Mission:** Survey overall curriculum directory structure across `/home/settings/Documents/pearl`, investigate Level 6 Networking requirements and location, and survey existing PyTorch curriculum to design a parallel and contrasting TensorFlow curriculum.

---

## 1. Observation

### 1.1 Direct Repository & Directory Survey
A full audit of `/home/settings/Documents/pearl` revealed the following directory inventory and structure:
- **Root Directories**:
  - `/home/settings/Documents/pearl/python-data-tools/` — **Level 1: Python Data Tools** (Git submodule/repo: `lessons/01_numpy`, `lessons/02_pandas`, `lessons/03_matplotlib`, `projects/student_performance_analysis`, `capstone/`, `assessment/`, `solutions/`, `datasets/`).
  - `/home/settings/Documents/pearl/engineering-mathematics/` — **Level 2: Engineering Mathematics & MATLAB** (`matlab/`, `linear_algebra/`, `calculus/`, `probability/`, `simulink/`, `capstone/`, `data/`, `solutions/`, `scripts/`, `tests/`).
  - `/home/settings/Documents/pearl/machine-learning/` — **Level 3 & 4/5: Machine Learning & Deep Learning** (12 numbered modules: `01_ml_fundamentals` through `06_model_evaluation` for Classical ML; `07_deep_learning_intro`, `08_pytorch_fundamentals`, `09_neural_networks`, `10_cnns`, `11_transformers`, `12_capstone` for Deep Learning; plus `solutions/`, `reference/`, `assessment/`, `datasets/`).
  - `/home/settings/Documents/pearl/ml-course/` — **Level 3.5: Math-First ML** (Phantom directory containing only a standalone `README.md`, 6,378 bytes; zero code files).
  - `/home/settings/Documents/pearl/neat/` — **Level 4: NeuroEvolution** (`01_evolutionary_computation` through `06_pole_balancing`, `capstone/`, `solutions/`, `assessment/`, `reference/`).
  - `/home/settings/Documents/pearl/game-ai/` — **Level 7: Game AI & Search** (`01_pygame` through `12_neural_game_ai`, `capstone/`, `exercises/`, `solutions/`, `reference/`).
  - `/home/settings/Documents/pearl/hshs/` — Unrelated cross-platform Flutter application project (`pubspec.yaml`, `android/`, `ios/`, `lib/`).
- **Root Files**:
  - `README.md` (2,733 B) — Root navigation guide documenting Level 1 `python-data-tools` and root prototype scripts.
  - `requirements.txt` (46 B) — `numpy>=1.24.0`, `pandas>=2.0.0`, `matplotlib>=3.7.0`.
  - `full_audit.py` (3,136 B) — Static analysis (flake8) and placeholder auditor over directories `['python-data-tools', 'engineering-mathematics', 'machine-learning', 'ml-course', 'neat', 'game-ai']`.
  - `generate_audit_report.py` (4,607 B) — Curriculum matrix generator mapping Levels 1 to 7.
  - `lesson.py`, `nmpy.py`, `game.py`, `pan.md`, `pans.md` — Early unstructured scripts preceding `python-data-tools`.
  - `lesson3.py`, `panda.py` — Empty 0-byte files.
  - `pearl.cpp` (329 B) — C++ demo file.

### 1.2 Status of Level 6 Networking
- **Specification Evidence**:
  - `/home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md` lines 111–113:
    > "### R3. Build Networking & TensorFlow Curricula
    > Create the entirely missing Level 6 Networking curriculum (TCP/IP, HTTP, REST). Introduce the missing TensorFlow curriculum module to contrast with the existing PyTorch material."
  - Line 122:
    > "- [ ] Level 6 Networking and TensorFlow modules contain both instructional READMEs and executable code examples."
  - `generate_audit_report.py` lines 72–76:
    ```python
    "Level 6: Networking": {
        "TCP/IP": "MISSING",
        "HTTP/HTTPS": "MISSING",
        "REST APIs": "MISSING"
    },
    ```
  - `machine-learning/README.md` lines 257–258 (Next Steps after ML/DL):
    > "3. Deployment — Serve models as REST APIs with FastAPI
    > 4. MLOps — MLflow for experiment tracking, Docker for reproducibility"
- **Filesystem Reality**:
  - Searches for `networking`, `06_networking`, `computer-networking`, `network`, `tcp`, `http`, or `rest` across `/home/settings/Documents/pearl` yielded **zero existing directories or files**.
  - Level 6 is **100% absent** from the repository.

### 1.3 Status & Structure of Deep Learning (PyTorch Curriculum)
- **Observed PyTorch Modules**:
  - `machine-learning/07_deep_learning_intro/`:
    - `01_tensors.py` (9,964 B) — Tensor creation, shapes, GPU/CPU devices, slicing, NumPy bridge (`.numpy()`, `from_numpy()`).
    - `02_autograd.py` (9,409 B) — Computational graph, `requires_grad=True`, `backward()`, chain rule, manual gradient descent.
    - `03_linear_model_in_pytorch.py` (9,160 B) — Manual parameter training vs `nn.Linear`.
    - `04_datasets_and_dataloaders.py` (10,697 B) — `torch.utils.data.Dataset` subclass, `DataLoader` batching/shuffling.
    - `README.md` (6,457 B), `exercises.py` (7,128 B).
  - `machine-learning/08_pytorch_fundamentals/`:
    - `01_nn_module.py` (14,056 B) — Subclassing `nn.Module`, `__init__`, `forward()`, `parameters()`, `train()` vs `eval()`.
    - `02_loss_functions.py` (13,982 B) — `MSELoss`, `BCEWithLogitsLoss`, `CrossEntropyLoss`.
    - `03_optimizers.py` (13,520 B) — `optim.SGD`, `optim.Adam`, learning rate schedulers.
    - `04_training_loop.py` (11,448 B) — 5-step training recipe (`zero_grad()`, `forward`, `loss`, `backward()`, `step()`), validation, early stopping.
    - `05_mlp_classification.py` (10,233 B) — Full MLP classifier on synthetic data vs sklearn.
    - `README.md` (6,254 B), `exercises.py` (8,047 B).
  - `machine-learning/09_neural_networks/`:
    - `01_activation_functions.py`, `02_backpropagation_and_deep_mlp.py`. (Missing: 03, 04, 05 assigned to R1).
  - `machine-learning/10_cnns/`: `01_convolution.py`, `02_pooling_and_architecture.py`, `03_cnn_for_images.py`, `04_transfer_learning.py`.
  - `machine-learning/11_transformers/`: `01_attention_and_transformers.py`.
- **Existing TensorFlow Evidence & Mentions**:
  - `machine-learning/README.md` line 75:
    > "> **Note on TensorFlow:** TensorFlow is referenced in optional, historical sections for context. The primary deep learning framework in this curriculum is **PyTorch**. All runnable code uses PyTorch only."
  - `machine-learning/requirements.txt` line 25:
    > "# tensorflow>=2.13       # TF — referenced in historical sections only"
  - `generate_audit_report.py` line 67:
    > `"TensorFlow": "MISSING"` under `"Level 5: Deep Learning"`
  - Zero executable TensorFlow lessons exist anywhere in the repository.

### 1.4 Runtime Environment & Package Availability Audit
- **Python Version**: `Python 3.14.6` (Anaconda build, GCC 14.3.0).
- **Installed Packages**:
  - `torch`: `2.13.0+cpu` (Functional)
  - `torchvision`: `0.28.0+cpu` (Functional)
  - `fastapi`: `0.141.1` (Functional, `TestClient` confirmed working)
  - `uvicorn`: `0.40.0` (Functional)
  - `requests`: `2.34.2` (Functional)
  - `httpx`: `0.28.1` (Functional)
  - `numpy`: `2.4.6` (Functional)
  - `scipy`: `1.18.0` (Functional)
  - `scikit-learn`: `1.9.0` (Functional)
  - `pytest`: `8.4.2` (Functional)
  - `flake8`: `7.3.0` (Functional)
- **Dependency Test Results**:
  - `python3 -m pip install --dry-run tensorflow`:
    > `ERROR: Could not find a version that satisfies the requirement tensorflow (from versions: none)`
    > `ERROR: No matching distribution found for tensorflow`
    *(Root cause: PyPI does not currently host pre-built compiled binary wheels for Python 3.14 for legacy TensorFlow)*.
  - `python3 -m pip install --dry-run keras`:
    > `Would install absl-py-2.5.0 keras-3.15.1 ml_dtypes-0.6.0 namex-0.1.0 optree-0.20.0`
    *(Keras 3.15.1 wheel IS available on Python 3.14 and runs natively on PyTorch or NumPy backends!)*

---

## 2. Logic Chain

1. **Top-Level Package Naming Convention**:
   - Observations show all existing curriculum levels use kebab-case or lower-case names without numeric prefixes at the root: `python-data-tools` (L1), `engineering-mathematics` (L2), `machine-learning` (L3-5), `neat` (L4), `game-ai` (L7).
   - In `full_audit.py` line 53, the directory list is: `['python-data-tools', 'engineering-mathematics', 'machine-learning', 'ml-course', 'neat', 'game-ai']`.
   - Therefore, Level 6 Networking should reside canonically at `/home/settings/Documents/pearl/networking/` (with a symlink `06_networking -> networking` to support tools or queries expecting numbered prefixes).
2. **Internal Module Numbering & Lesson Structure**:
   - Every package structures its internal learning modules using zero-padded prefixes: `01_...`, `02_...`, `03_...`.
   - Lessons within modules follow the pattern: `01_<topic>.py`, `02_<topic>.py`, ..., `exercises.py`, accompanied by `README.md`.
   - All modules feature an "Explain WHY before HOW" README with Bloom's taxonomy learning objectives, concept diagrams, code guides, common pitfalls, and 4-tier exercises (Level 1: Recall, Level 2: Understanding/Debugging, Level 3: Application, Level 4: Challenge).
   - All reference solutions are decoupled into a dedicated `solutions/` directory with 0 remaining `% TODO` or `# TODO` markers.
3. **Level 6 Networking Architectural Scoping**:
   - Requirement R3 explicitly mandates: `TCP/IP, HTTP, REST`.
   - In `generate_audit_report.py`, the required sub-topics are: `TCP/IP`, `HTTP/HTTPS`, `REST APIs`.
   - Since `socket`, `threading`, `http.server`, and `urllib` are in Python's standard library, and `fastapi`, `uvicorn`, `requests`, and `httpx` are already verified installed, Level 6 can be fully implemented with zero external binary blockers.
   - The module must be split into 3 distinct pedagogical submodules:
     1. `01_tcp_ip/`: Low-level network primitives (OSI vs TCP/IP model, TCP client/server, UDP datagrams, socket options, concurrent multi-client servers).
     2. `02_http_protocols/`: Web protocols (HTTP/1.1 message structure, raw socket HTTP client, Python `http.server`, modern HTTP requests with `requests`/`httpx`, headers, status codes, query parameters).
     3. `03_rest_apis/`: Architectural style & model serving (REST constraints, resource modeling, FastAPI endpoints, Pydantic data schemas, JSON serialization, and serving an ML model via REST endpoint).
4. **TensorFlow Curriculum Location & Design**:
   - In `generate_audit_report.py`, TensorFlow is listed under `"Level 5: Deep Learning"`, while `machine-learning/` currently houses all deep learning modules (`07_deep_learning_intro`, `08_pytorch_fundamentals`, `09_neural_networks`, `10_cnns`, `11_transformers`).
   - PyTorch fundamentals are located at `machine-learning/08_pytorch_fundamentals/`.
   - Placing TensorFlow at `machine-learning/08_tensorflow_fundamentals/` (with an alias/symlink `machine-learning/05_tensorflow -> 08_tensorflow_fundamentals`) provides the perfect pedagogical parallel to Module 8. Students can directly contrast PyTorch and TensorFlow using identical datasets and tasks.
5. **Python 3.14 Environment Compatibility Strategy for TensorFlow**:
   - Because `pip install tensorflow` fails on Python 3.14 due to lack of pre-built binary wheels on PyPI, writing raw unhandled `import tensorflow as tf` would cause immediate `ModuleNotFoundError` crashes upon execution or automated testing, violating Acceptance Criterion 1 ("All code implementations execute without syntax or runtime errors").
   - Solution: The TensorFlow curriculum must be built with a **dual-mode architecture**:
     - Code uses 100% authentic, canonical TensorFlow 2.x / Keras syntax (`tf.constant`, `tf.Variable`, `tf.GradientTape()`, `keras.Sequential`, `keras.Model`, `model.compile()`, `model.fit()`).
     - A robust, zero-dependency educational compatibility module (`tf_compat.py`) or Keras 3 backend bridge is embedded in the module. If native `tensorflow` is present, it uses real TensorFlow. If running under Python 3.14 without binary wheels, `tf_compat.py` provides exact API-compatible emulations of `tf.Tensor`, `tf.Variable`, `GradientTape`, and Keras layers built cleanly on top of NumPy and/or installed `torch`.
     - This satisfies all requirements: authentic API learning, 100% executable without runtime errors, zero syntax errors, and complete contrast with PyTorch.

---

## 3. Caveats

1. **Python 3.14 Wheel Distribution**: If Google releases pre-built TensorFlow wheels for Python 3.14 in the future, native TensorFlow can be installed directly without any modification to student code. The compatibility layer ensures current executability.
2. **Ephemeral Ports for Network Tests**: Network socket and HTTP server tests must avoid binding to fixed high-numbered ports (e.g. 8000, 8080) that may be occupied on shared environments. All tests and exercise verification harnesses must use port `0` (OS-assigned ephemeral port) or FastAPI's memory-based `TestClient` to guarantee deterministic, collision-free execution.
3. **ML-Course Phantom Directory**: `ml-course/` remains a 0-lesson placeholder at root. As established in the audit report, it should either be populated or documented as an optional reference path superseded by `machine-learning/`.

---

## 4. Conclusion

The curriculum layout, Level 6 Networking module, and TensorFlow module architectures are fully mapped and ready for implementation by Milestone M3 workers. Below are the exact blueprints and file manifests.

### 4.1 Master Layout Blueprint for Level 6: Networking (`networking/`)

```
/home/settings/Documents/pearl/networking/
├── README.md                                  # Level 6 Master Guide (OSI model, networking mental models, roadmap)
├── requirements.txt                           # fastapi, uvicorn, requests, httpx, pydantic
├── 01_tcp_ip/                                 # Module 1: TCP/IP & Socket Programming
│   ├── README.md                              # 9-section guide: OSI 4 vs 7 layer, TCP handshake, UDP vs TCP
│   ├── 01_tcp_server.py                       # Single-client TCP echo server (AF_INET, SOCK_STREAM, bind, listen)
│   ├── 02_tcp_client.py                       # TCP socket client with buffered chunk reception and timeouts
│   ├── 03_udp_sockets.py                      # UDP client/server demonstrating connectionless datagrams
│   ├── 04_concurrent_server.py                # Multi-client TCP server using threading & connection pooling
│   └── exercises.py                           # 4-tier exercises (Tier 1: Socket ops, Tier 2: Debugging buffer bugs,
│                                              #                   Tier 3: Heartbeat ping-pong, Tier 4: Broadcast hub)
├── 02_http_protocols/                         # Module 2: HTTP Mechanics & Clients
│   ├── README.md                              # HTTP/1.1 message structure, request/response headers, status codes
│   ├── 01_raw_http_client.py                  # Constructing and parsing HTTP/1.1 requests over raw TCP socket
│   ├── 02_python_http_server.py               # Built-in http.server (BaseHTTPRequestHandler, GET/POST routing)
│   ├── 03_requests_and_httpx.py               # Modern HTTP clients: requests & httpx (sessions, auth, timeouts)
│   └── exercises.py                           # 4-tier exercises (Tier 1: Verbs/status codes, Tier 2: Bad headers,
│                                              #                   Tier 3: Sensor health probe, Tier 4: Rate-limited client)
├── 03_rest_apis/                              # Module 3: REST API Principles & ML Model Serving
│   ├── README.md                              # REST architectural constraints, OpenAPI/Swagger, ML inference serving
│   ├── 01_rest_principles.py                  # Core REST design: resource URLs, CRUD mapping, JSON responses
│   ├── 02_fastapi_endpoints.py                # Production FastAPI service with Pydantic validation & error handling
│   ├── 03_ml_model_serving.py                 # Live REST API serving an ML predictive model with latency logging
│   └── exercises.py                           # 4-tier exercises (Tier 1: REST recall, Tier 2: Pydantic validation fix,
│                                              #                   Tier 3: Telemetry ingestion API, Tier 4: Batch scoring)
├── solutions/                                 # Decoupled Reference Solutions (0 remaining TODOs)
│   ├── tcp_ip_solutions.py                    # Complete solutions for 01_tcp_ip/exercises.py
│   ├── http_solutions.py                      # Complete solutions for 02_http_protocols/exercises.py
│   └── rest_api_solutions.py                  # Complete solutions for 03_rest_apis/exercises.py
└── tests/                                     # E2E Test Suite
    ├── __init__.py
    ├── test_networking_structure.py           # Validates directories, file sizes, zero TODOs in solutions
    └── test_networking_execution.py           # Automated functional tests using ephemeral sockets & TestClient
```

### 4.2 Master Layout Blueprint for TensorFlow Curriculum (`machine-learning/08_tensorflow_fundamentals/`)

```
/home/settings/Documents/pearl/machine-learning/08_tensorflow_fundamentals/
├── README.md                                  # Complete pedagogical guide & PyTorch vs TensorFlow comparative map
├── tf_compat.py                               # Zero-dependency Python 3.14 compatibility engine & fallback shim
├── 01_tf_tensors_and_variables.py             # tf.constant vs tf.Variable, shapes, dtypes, indexing, NumPy bridge
├── 02_gradient_tape.py                        # Automatic differentiation: tf.GradientTape(), tape.watch(), custom GD
├── 03_keras_model_architectures.py            # The 3 Keras paradigms: Sequential, Functional, Model Subclassing
├── 04_training_workflows.py                   # model.compile/fit vs custom GradientTape training loop vs PyTorch loop
├── 05_end_to_end_mlp_classifier.py            # Complete end-to-end classification pipeline with dataset & metrics
├── 06_pytorch_vs_tensorflow_rosetta.py        # The Master Rosetta Stone: 30+ side-by-side PyTorch vs TF code pairs
├── exercises.py                               # 4-tier progressive exercises (Recall, Debugging, Application, Challenge)
└── output/                                    # Generated diagnostic figures & training curve plots
```

**Paired Reference Solution**:
- `/home/settings/Documents/pearl/machine-learning/solutions/tensorflow_fundamentals_solutions.py`

### 4.3 Side-by-Side Framework Contrast Specification

| Dimension | PyTorch (`08_pytorch_fundamentals`) | TensorFlow & Keras (`08_tensorflow_fundamentals`) |
|:---|:---|:---|
| **Core Abstraction** | `torch.Tensor` (`requires_grad=True`) | `tf.constant` (immutable) & `tf.Variable` (mutable) |
| **Autograd Engine** | Dynamic backward pass (`loss.backward()`) | Context manager tape (`with tf.GradientTape() as tape:`) |
| **Gradient Access** | Stored on tensor attributes (`tensor.grad`) | Extracted explicitly via `tape.gradient(loss, vars)` |
| **Weight Updates** | `optimizer.step()` (in-place) | `optimizer.apply_gradients(zip(grads, vars))` / `assign_sub` |
| **Model Creation** | Subclass `nn.Module` with `forward()` | 3 Paradigms: Sequential, Functional, Subclassing `keras.Model` (`call()`) |
| **Standard Training** | Explicit 5-step loop written by developer | High-level `model.compile()` + `model.fit()` OR custom `GradientTape` |
| **Train/Eval Modes** | `model.train()` and `model.eval()` | `training=True/False` boolean passed to `model(x, training=...)` |
| **Data Pipelines** | `torch.utils.data.Dataset` & `DataLoader` | `tf.data.Dataset` (`from_tensor_slices`, `batch`, `prefetch`) |

---

## 5. Verification Method

To independently verify the discoveries and validate the eventual implementations:

### 5.1 Verification Commands
1. **Verify Python & Networking Environment**:
   ```bash
   python3 -c "import fastapi, uvicorn, requests, httpx; print('Networking dependencies ready')"
   ```
2. **Verify Level 6 Networking (Post-Implementation)**:
   ```bash
   # Run static syntax and undefined variable analysis
   flake8 --select=E999,F821 networking/
   
   # Run networking automated pytest suite
   pytest networking/tests/ -v
   ```
3. **Verify TensorFlow & Keras Module (Post-Implementation)**:
   ```bash
   # Verify standalone script executability
   python3 machine-learning/08_tensorflow_fundamentals/01_tf_tensors_and_variables.py
   python3 machine-learning/08_tensorflow_fundamentals/02_gradient_tape.py
   python3 machine-learning/08_tensorflow_fundamentals/03_keras_model_architectures.py
   python3 machine-learning/08_tensorflow_fundamentals/04_training_workflows.py
   python3 machine-learning/08_tensorflow_fundamentals/05_end_to_end_mlp_classifier.py
   python3 machine-learning/08_tensorflow_fundamentals/06_pytorch_vs_tensorflow_rosetta.py
   
   # Verify solutions have 0 remaining TODO markers
   grep -ri "TODO" machine-learning/solutions/tensorflow_fundamentals_solutions.py || echo "Zero TODOs verified"
   ```
4. **Curriculum Audit Verification**:
   ```bash
   python3 /home/settings/Documents/pearl/full_audit.py
   ```

### 5.2 Invalidation Conditions
- Any proposed networking script fails with unhandled socket errors due to hardcoded, already-bound ports.
- Any proposed TensorFlow script raises unhandled `ModuleNotFoundError` in Python 3.14 environments.
- Module READMEs omit learning objectives, conceptual diagrams, or fail the "Explain WHY before HOW" standard.
- Exercises fail to implement the 4 cognitive tiers or solutions leave uncompleted `# TODO` tags.
