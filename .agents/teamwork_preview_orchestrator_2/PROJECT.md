# PROJECT — Curriculum Content Audit & Specification

## Architecture & Curriculum Overview
The curriculum at `/home/settings/Documents/pearl` is an end-to-end engineering and data science pipeline spanning from introductory Python and engineering mathematics to machine learning, neuroevolution, and game artificial intelligence.

The repository establishes three mutually reinforcing taxonomy framings:
1. **The Pedagogical Sequence**:
   - Level 1: Python Data Tools (`python-data-tools/`) — NumPy, Pandas, Matplotlib
   - Level 2: Engineering Mathematics (`engineering-mathematics/`) — MATLAB, Linear Algebra, Calculus, Probability, Simulink
   - Level 3: Machine Learning (`machine-learning/01–06`) — Supervised, Unsupervised, Model Evaluation, from-scratch math
   - Level 4: Deep Learning & Neuroevolution (`machine-learning/07–11` and `neat/`) — PyTorch, MLPs, CNNs, Transformers, NEAT
   - Level 5: Advanced Deep Learning Systems (`machine-learning/12_capstone`, Transformers, Industrial Sensor Capstone)
   - Level 6: Computer Networking (`TCP/IP`, `HTTP/HTTPS`, `REST APIs` — currently missing)
   - Level 7: Game AI & Board Game Algorithms (`game-ai/01–12`) — Pygame, Minimax, Alpha-Beta, Connect Four, Chess, MCTS, RL

2. **Audit Taxonomy (from `generate_audit_report.py`)**:
   - Level 1: Python Data Tools
   - Level 2: Engineering Mathematics
   - Level 3: Machine Learning (01–06)
   - Level 3.5: Math-First ML (`ml-course`)
   - Level 4: NEAT
   - Level 5: Deep Learning (07–11, PyTorch)
   - Level 6: Networking (TCP/IP, HTTP, REST APIs)
   - Level 7: Game AI (01–12)

3. **Master Audit Batches**:
   - Batch 1: Level 1 (`python-data-tools` + root scripts)
   - Batch 2: Level 2 (`engineering-mathematics/`)
   - Batch 3: Level 3 (`machine-learning/01–06` & `ml-course/`)
   - Batch 4: Level 4 (`machine-learning/07–11` & `neat/`)
   - Batch 5: Level 5 (`machine-learning/12_capstone`, PyTorch systems)
   - Batch 6: Level 6 (Networking & MLOps) & Level 7 (`game-ai/01–12`)

---

## Feature Inventory & Completion Status

| # | Curriculum Level | Module / Component | Stated Scope | Observed Status | Textual Evidence / Primary Gaps |
|---|------------------|--------------------|--------------|-----------------|---------------------------------|
| 1 | Level 1 | `01_numpy` | Arrays, indexing, vectorization, stats, broadcasting | **COMPLETE** | 5 lesson files (166 lines exercises), SIMD explanation, memory layout, Ohm's law. Full solutions in `solutions/01_numpy_solutions.py`. |
| 2 | Level 1 | `02_pandas` | Series, DataFrames, filtering, cleaning, groupby | **COMPLETE** | 5 lesson files (146 lines exercises), split-apply-combine, customer orders dataset. Full solutions in `solutions/02_pandas_solutions.py`. |
| 3 | Level 1 | `03_matplotlib` | Plots, customization, subplots, real data | **COMPLETE** | 4 lesson files, figure/axes hierarchy, 9 generated figures. Full solutions in `solutions/03_matplotlib_solutions.py`. |
| 4 | Level 1 | `projects/student_performance` | Multi-library integration | **COMPLETE** | Full data pipeline (`data_loader.py`, `metrics.py`, `visualizer.py`, `analysis.py`), 4-panel dashboard output. |
| 5 | Level 1 | `capstone` & assessment | Industrial equipment reliability capstone | **COMPLETE** | 100-point rubric, starter template, 4-tier practical exam (`practical_test.py`), reference solutions. |
| 6 | Level 2 | `matlab/` | MATLAB environment, memory, syntax, plotting | **COMPLETE** | 9-part README, 6 concept scripts, mini-project (`circuit_mesh_analysis.m`), 4-tier exercises, solutions. |
| 7 | Level 2 | `linear_algebra/` | Matrix math, transformations, eigenvalues, solving $Ax=b$ | **COMPLETE** | 9-part README, 7 concept scripts, truss analysis mini-project, 4-tier exercises, solutions. |
| 8 | Level 2 | `calculus/` | Rates of change, integration as accumulation, 1st-order ODEs | **COMPLETE** | 9-part README, 6 concept scripts, RC circuit transient mini-project, 4-tier exercises, solutions. |
| 9 | Level 2 | `probability/` | Distributions, Monte Carlo, sensor noise, reliability | **PARTIAL** | Complete README and 4 concept scripts, but **missing decoupled solution** `solutions/probability_exercises_solution.m`. |
| 10 | Level 2 | `simulink/` | Block diagrams, feedback, solvers, companion scripts | **PARTIAL** | README and RC circuit blueprint exist, but **missing 3 companion scripts (03, 04, 05), motor control mini-project, 2 blueprints, exercises, solutions**. |
| 11 | Level 2 | `capstone/` | EV powertrain telemetry analysis | **PARTIAL** | Data generator and starter template exist, but **missing complete reference solution** `capstone_analysis_complete.m`. |
| 12 | Level 2 | Reference & Bridges | ML Bridge, Cheat sheets, Assessments, root README | **MISSING** | Entire `ml_bridge/`, `assessments/`, `reference/`, and root `engineering-mathematics/README.md` are absent. |
| 13 | Level 3 | `01_ml_fundamentals` | ML paradigm, types, workflows | **COMPLETE** | Teaching README, concept scripts, end-to-end workflow, exercises, solutions. |
| 14 | Level 3 | `02_data_preprocessing` | Scaling, imputation, encoding, train/test split | **COMPLETE** | MinMax/StandardScaler scratch vs sklearn, 4-tier exercises, solutions. |
| 15 | Level 3 | `03_regression` | Linear/Polynomial regression, OLS derivation | **COMPLETE** | Normal equation $(X^T X)^{-1} X^T y$ derivation, gradient descent, 4-tier exercises, solutions. |
| 16 | Level 3 | `04_classification` | Logistic regression, Decision Trees, Random Forests, SVM | **PARTIAL** | Strong lessons, but **missing dedicated solution file** (`solutions/classification_solutions.py`). Logistic regression lacks scratch GD in lesson. |
| 17 | Level 3 | `05_unsupervised` | K-Means, PCA, clustering | **PARTIAL** | K-Means has scratch implementation; PCA relies purely on `sklearn.decomposition.PCA` without NumPy covariance eigen-decomposition. |
| 18 | Level 3 | `06_model_evaluation` | Confusion matrix, ROC-AUC, cross-validation | **COMPLETE** | Scratch metric calculations, 4-tier exercises, cross-validation loops. |
| 19 | Level 3.5| `ml-course/` | Math-first ML course | **MISSING / PHANTOM** | Directory exists but contains only an unpopulated alternate `README.md`. No code files. |
| 20 | Level 4 | `neat/` | NeuroEvolution of Augmenting Topologies | **PARTIAL** | XOR and CartPole tutorials work, but modules 01, 02, 03 have empty `examples/` and `exercises/`. Capstone lacks solution. |
| 21 | Level 4 / 5 | `07_deep_learning_intro` | PyTorch tensors, autograd, linear model | **COMPLETE** | Complete tensor operations, computational graph, autograd, Dataset/DataLoader. |
| 22 | Level 4 / 5 | `08_pytorch_fundamentals`| nn.Module, losses, optimizers, training loop | **COMPLETE** | Full modular architecture, custom training loop, multi-class classification. |
| 23 | Level 4 / 5 | `09_neural_networks` | Activations, backprop, deep MLPs | **PARTIAL / DEFICIT** | README advertises 5 lessons (`02_weight_initialization.py`, `03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`); only 2 exist on disk. |
| 24 | Level 4 / 5 | `10_cnns` | Convolutions, pooling, architectures, transfer learning | **PARTIAL** | From-scratch 2D convolution and full PyTorch CNNs exist, but **missing dedicated solution file**. |
| 25 | Level 4 / 5 | `11_transformers` | Attention mechanisms, self-attention, scaled dot-product | **COMPLETE** | Manual scaled dot-product self-attention from scratch, multi-head attention concepts, exercises. |
| 26 | Level 5 | `12_capstone` | Industrial Predictive Failure System (Meridian) | **PARTIAL** | 200-point rubric, synthetic generator, starter template, but **missing reference solution** `solutions/capstone_solution.py`. |
| 27 | Level 6 | `networking/` & MLOps | TCP/IP, HTTP/HTTPS, REST APIs, FastAPI, Docker, MLflow | **MISSING (100%)** | Zero files exist in repository. Specified in `generate_audit_report.py` and ML roadmap as Level 6. |
| 28 | Level 7 | `game-ai/01-05` | Pygame, Tic-Tac-Toe, Minimax, Alpha-Beta | **COMPLETE** | Working Pygame games, tree search, minimax, alpha-beta pruning with node count tracking. |
| 29 | Level 7 | `game-ai/07, 09` | Connect Four, Chess AI | **COMPLETE** | Bitboard-style Connect Four and `python-chess` integration with Piece-Square Tables. |
| 30 | Level 7 | `game-ai/02, 06, 08, 10, 11, 12` | Checkers, MCTS, Reinforcement Learning, Neural Game AI | **PARTIAL / THEORY ONLY** | Markdown essays only. Checkers engine skipped, MCTS has zero code, RL has zero code, Neural Game AI has zero code. |
| 31 | Level 7 | `game-ai/capstone` | Reversi (Othello) AI | **PARTIAL** | Starter template exists; **missing reference solution** in `solutions/`. |
