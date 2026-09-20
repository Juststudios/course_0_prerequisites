# Engineering Mathematics + MATLAB: Existing Codebase Survey & Target Layout Map

**Author:** Explorer Survey 2  
**Date:** 2026-09-10  
**Target Project Directory:** `/home/settings/Documents/pearl/engineering-mathematics`  
**Workspace Root:** `/home/settings/Documents/pearl`  
**Curriculum Role:** Level 2 (Bridging Level 1: `python-data-tools` to Level 3: Machine Learning)  
**Authoritative Reference:** `/home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md`

---

## 1. Executive Summary

This survey report provides an exhaustive, forensic investigation of the existing files, software packages, Python environment, and developer tools across `/home/settings/Documents/pearl`, and establishes the authoritative directory structure and file layout for `/home/settings/Documents/pearl/engineering-mathematics`.

### Key Discoveries:
1. **Target Directory Status:** `/home/settings/Documents/pearl/engineering-mathematics` is currently an empty directory, primed for complete greenfield scaffolding adhering strictly to requirements R1–R6.
2. **Existing Level 1 Curriculum Identified:** `/home/settings/Documents/pearl/python-data-tools` is an existing, mature, standalone Git repository (`https://github.com/Juststudios/python-data-tools.git`, branch `master`, commit `7270e23`). It embodies the exact pedagogical standard (Level 1: Python, NumPy, Pandas, Matplotlib) that `engineering-mathematics` (Level 2) must seamlessly connect with and mirror in quality.
3. **Pedagogical Archetype to Match:** `python-data-tools` demonstrates a rigorous 4-tier mastery model (Recall $\rightarrow$ Understanding/Debugging $\rightarrow$ Application $\rightarrow$ Challenge), dedicated `solutions/` separation, an "Explain WHY before HOW" philosophy, multi-panel diagnostic visualizations, and a 100-point rubric assessment. Level 2 must match and extend this standard into engineering mathematics and MATLAB.
4. **Environment & Tooling Audit:** The active Python environment is Python 3.14.6 in `/home/settings/Documents/pearl/.venv` with `pytest 8.4.2` and deep scientific packages (`numpy`, `scipy 1.18.0`, `sympy 1.14.0`, `matplotlib`, `pandas`, `scikit-learn 1.9.0`, `torch 2.13.0+cpu`). Native `matlab` and `octave` CLI binaries are **not** present on PATH. Consequently, verification must be executed via an automated Python test suite (`pytest`, AST/regex syntax parsers, file structure auditors, and numerical companion verification).
5. **Architectural Blueprints:** An exact 82-file comprehensive layout is mapped out, covering all 5 core modules (`matlab/`, `linear_algebra/`, `calculus/`, `probability/`, `simulink/`), integration assets (`capstone/`, `ml_bridge/`, `assessments/`, `reference/`), separated reference solutions (`solutions/`), telemetry data (`data/`), and verification scripts (`scripts/`, `tests/`).

---

## 2. Comprehensive File System Survey

### 2.1 Workspace Root Inventory (`/home/settings/Documents/pearl`)

An inspection of `/home/settings/Documents/pearl` reveals 8 directories and 11 files:

```text
/home/settings/Documents/pearl/
├── README.md                              (2,733 B) Master workspace navigation & curriculum overview
├── requirements.txt                       (46 B)    Root dependencies (numpy, pandas, matplotlib)
├── .venv/                                 (Dir)     Virtual environment (Python 3.14.6)
├── .agents/                               (Dir)     Multi-agent orchestration metadata & logs
├── .vscode/                               (Dir)     VS Code workspace configuration
├── .idea/                                 (Dir)     JetBrains / PyCharm configuration
├── __pycache__/                           (Dir)     Python bytecode cache
├── a.py                                   (1,725 B) Scratch exploratory script
├── game.py                                (3,863 B) Tic-Tac-Toe console game (2D lists, game state logic)
├── lesson.py                              (677 B)   Introductory Python lesson (variables, loops)
├── lesson3.py                             (0 B)     Empty scratch file
├── nmpy.py                                (2,363 B) Exploratory NumPy array slicing and axis operations
├── pan.md                                 (24,427 B) Instructor teaching guide for Pandas 101
├── panda.py                               (0 B)     Empty scratch file
├── pans.md                                (14,328 B) Student handbook & reference for Pandas
├── pearl.cpp                              (329 B)   C++ basic test file
├── hshs/                                  (Dir)     Unrelated Flutter cross-platform mobile project
├── python-data-tools/                     (Dir)     LEVEL 1 CURRICULUM: Complete Python data tools package
└── engineering-mathematics/               (Dir)     LEVEL 2 TARGET: Currently empty directory
```

### 2.2 Forensic Analysis of Individual Workspace Components

* **`README.md` (Pearl Root):**
  - Explicitly documents the curriculum pathway: section 1 covers foundational python lessons (`lesson.py`, `game.py`, `nmpy.py`, `pan.md`, `pans.md`); section 2 documents the complete data tools curriculum inside `python-data-tools/`.
  - Establishes quickstart instructions referencing `python-data-tools/projects/student_performance_analysis/analysis.py` and `python-data-tools/solutions/capstone_solution.py`.
* **`engineering-mathematics/` (Target Directory):**
  - Confirmed completely empty.
  - Ownership and permissions allow full read/write operations by the development agents.
* **`hshs/` Directory:**
  - Contains a Flutter app (`pubspec.yaml`, `android/`, `ios/`, `lib/`, `test/`, `web/`, `windows/`).
  - Completely unrelated to the data science and engineering mathematics curriculum pipeline.
* **Loose Root Scripts (`lesson.py`, `game.py`, `nmpy.py`, `pan.md`, `pans.md`):**
  - Represent informal, early draft pedagogical prototypes prior to the modular creation of `python-data-tools`.
  - Confirms that the educational direction evolved into formal, modular packages with structured subdirectories.

---

## 3. Existing Level 1 Package Analysis (`python-data-tools`)

The directory `python-data-tools/` serves as the concrete, implemented **Level 1** curriculum. Investigating its structure, conventions, and style provides the exact benchmark for **Level 2** (`engineering-mathematics`).

### 3.1 Git Status & Provenance
* **Git Repository:** `python-data-tools/` contains its own `.git` repository.
* **Origin Remote:** `https://github.com/Juststudios/python-data-tools.git`
* **Current Branch:** `master` (up to date with `origin/master`)
* **Commit:** `7270e23` (*Initial commit*)
* **Untracked Cache:** `projects/student_performance_analysis/src/__pycache__/`

### 3.2 Directory Structure of Level 1 (`python-data-tools`)

```text
python-data-tools/
├── README.md                              (12,225 B) Master curriculum map, pedagogy, quickstart
├── requirements.txt                       (46 B)     Python dependencies (numpy, pandas, matplotlib)
├── datasets/                              (CSV Datasets)
│   ├── orders.csv                         (56 rows) E-commerce customer order logs
│   ├── student_performance.csv            (160 rows) Academic records across 4 majors
│   └── machine_sensor_log.csv             (120 rows) Factory IoT telemetry for 6 machines
├── lessons/
│   ├── 01_numpy/
│   │   ├── README.md                      (9,812 B) Module guide & learning objectives
│   │   ├── 01_arrays.py                   Array creation, attributes (shape, size, ndim, dtype)
│   │   ├── 02_indexing.py                 1D/2D slicing, views vs copies (.copy())
│   │   ├── 03_operations.py               Vectorized arithmetic, performance benchmark, Ohm's law
│   │   ├── 04_statistics.py               Summary stats, outlier sensitivity, axis=0 vs axis=1
│   │   ├── 05_beyond_basics.py            Masking, broadcasting, reshaping, matrix multiplication
│   │   └── exercises.py                   4-tier progressive student exercises
│   ├── 02_pandas/
│   │   ├── README.md                      Module guide & learning objectives
│   │   ├── 01_series.py                   1D labeled Series, indexing, value_counts
│   │   ├── 02_dataframes.py               Loading CSVs, .info, .describe, .loc vs .iloc
│   │   ├── 03_filtering.py                Boolean masks, compound queries (&, |, ~)
│   │   ├── 04_cleaning.py                 .isna(), .fillna(), .dropna(), type casting
│   │   ├── 05_grouping.py                 .groupby(), .agg(), split-apply-combine
│   │   └── exercises.py                   4-tier progressive student exercises
│   └── 03_matplotlib/
│       ├── README.md                      Module guide & learning objectives
│       ├── 01_basic_plots.py              Line, bar, scatter, histogram
│       ├── 02_customization.py            Styles, grid, labels, threshold lines, annotations
│       ├── 03_subplots.py                 Multi-panel stacked & 2x2 grid dashboards
│       ├── 04_real_data.py                Plotting directly from DataFrames & sensor logs
│       ├── output/                        Generated high-res PNG plots (11 files)
│       └── exercises.py                   4-tier progressive student exercises
├── projects/
│   └── student_performance_analysis/      Flagship integrated capstone
│       ├── README.md                      Project workflow, research questions, interpretation
│       ├── analysis.py                    Executable analysis script
│       ├── requirements.txt               Project dependencies
│       ├── data/student_performance.csv   Project data
│       ├── student_performance_dashboard.png Exported multi-panel visualization
│       └── src/
│           ├── __init__.py
│           ├── data_loader.py             Data cleaning & imputation
│           ├── metrics.py                 Statistical computations & correlation
│           └── visualizer.py              Matplotlib multi-panel dashboard
├── capstone/
│   ├── README.md                          Problem statement, tasks, 100-pt grading rubric
│   ├── data/machine_sensor_log.csv        Factory sensor telemetry
│   ├── fleet_health_dashboard.png         Reference dashboard output
│   └── starter_template.py                Scaffolded student template with TODO markers
├── assessment/
│   ├── FINAL_ASSESSMENT.md                100-point comprehensive exam (concept, code reading, debug)
│   └── practical_test.py                  Scaffolded coding test runner (pytest-compatible)
└── solutions/
    ├── numpy_exercises_solution.py        Complete solution for NumPy exercises
    ├── pandas_exercises_solution.py       Complete solution for Pandas exercises
    ├── matplotlib_exercises_solution.py   Complete solution for Matplotlib exercises
    ├── capstone_solution.py               Complete implementation of industrial capstone
    └── assessment_answers.md              Full 100-point answer key & explanations
```

### 3.3 Key Pedagogical Patterns Extracted from Level 1

To guarantee curriculum continuity, `engineering-mathematics` must incorporate the following established patterns from `python-data-tools`:

1. **"Explain WHY Before HOW" Principle:**
   - In `python-data-tools`, every module begins with an explanation of the fundamental computational problem that necessitated the tool (e.g., Python lists are pointers causing slow dynamic type checks, so NumPy introduces contiguous SIMD memory).
   - In `engineering-mathematics`, every module must open by explaining *why* engineers need MATLAB and mathematics (e.g., MATLAB's matrix-first memory model and backslash operator $x = A \setminus b$ are engineered for numerical stability in stiffness/admittance matrices where Python's general-purpose syntax requires heavier boilerplate).
2. **Standard Module `README.md` Anatomy:**
   Every lesson directory has a `README.md` structured as follows:
   - Learning Objectives (bulleted checklist)
   - What Problem Does This Solve? / Why Engineers Need This
   - Key Terminology (callout quotes defining technical terms)
   - Concept Explanation (organized into *Must Know*, *Good to Know*, and *Advanced*)
   - Code Examples (ordered file progression)
   - Understanding the Output (how to interpret numbers, arrays, and graphs)
   - Why This Is Useful & Real-World Applications
   - Common Mistakes (with verbatim incorrect code and corrected code)
   - Practice Exercises & Challenge Overview
   - What You Should Know Before Moving On
3. **The 4-Tier Progressive Mastery Framework:**
   Every exercise file (`exercises.py` in Level 1, `exercises.m` in Level 2) must feature four strict tiers:
   - **Tier 1 — Recall:** Reproduce foundational syntax and definitions.
   - **Tier 2 — Understanding / Debugging:** Diagnose and repair realistic broken code (e.g., fixing operator precedence, 0-based vs 1-based indexing errors, matrix vs element-wise mistakes, dimension mismatches).
   - **Tier 3 — Application:** Solve self-contained physical engineering problems independently.
   - **Tier 4 — Challenge:** Synthesize multiple concepts into a multi-step analytical workflow.
4. **Decoupled Reference Solutions:**
   Student exercise templates (`exercises.m`) contain instructions, test prints, and `TODO` markers. Solutions are cleanly isolated in `solutions/`, complete with explanatory comments.
5. **Multi-Disciplinary Realistic Datasets:**
   Data is never random or meaningless `[1, 2, 3]`; it reflects real engineering telemetry (sensor noise, thermal decay, circuit voltages, structural load distributions).
6. **100-Point Rubric Final Assessment:**
   The assessment is structured into conceptual questions, code output predictions, debugging challenges, and an end-to-end practical project, scored against an explicit rubric.

---

## 4. Python Environment & Available Tooling Audit

A thorough terminal audit was conducted to verify the local runtime environment, compilers, and test runners:

### 4.1 System Specifications & Tool Paths
| Tool | Version / Status | Path / Details | Notes |
|---|---|---|---|
| **OS** | Linux (Ubuntu/Debian) | Kernel 6.6+ | Standard Linux container |
| **Python** | `Python 3.14.6` | `/home/settings/Documents/pearl/.venv/bin/python3` | Modern, cutting-edge release |
| **Pytest** | `pytest 8.4.2` | `/home/settings/Documents/pearl/.venv/bin/pytest` | Installed with pluggy 1.6.0, asyncio |
| **MATLAB CLI** | **Not Installed** | Not found on PATH (`which matlab` $\rightarrow$ empty) | Requires static validation / Python test harness |
| **GNU Octave** | **Not Installed** | Not found on PATH (`which octave` $\rightarrow$ empty) | Headless environment |
| **Git** | `git 2.x` | Functional in `python-data-tools` | Pearl root is not a Git repo |

### 4.2 Installed Python Scientific Packages
The local `.venv` environment contains a comprehensive scientific and testing stack:
* **Numerical & Mathematical Computing:** `numpy` (>=1.24), `scipy` (1.18.0), `sympy` (1.14.0)
* **Data Wrangling & Analysis:** `pandas` (>=2.0.0), `pyarrow` (23.0.1)
* **Scientific Visualization:** `matplotlib` (>=3.7.0), `seaborn` (0.13.2), `plotly` (6.7.0)
* **Machine Learning & AI (Level 3 Ready):** `scikit-learn` (1.9.0), `torch` (2.13.0+cpu), `torchvision` (0.28.0+cpu)
* **Code Analysis & Linting:** `ruff` (0.14.0), `pylint` (4.0.6), `pycodestyle` (2.14.0), `rope` (1.14.0)
* **Rich Terminal Formatting:** `rich` (15.0.0)

### 4.3 Engineering Implication of the Headless MATLAB Environment
Because native MATLAB is not present on this Linux host, students and automated evaluators cannot invoke `matlab -batch "run(...)"`. 

To ensure **100% verification integrity, executability, and zero broken links**, the following testing architecture must be implemented:
1. **Python-Based Verification Auditor (`scripts/verify_package.py`):**
   - Implements an automated static analyzer and structural validator.
   - Parses all `.m` files using regex and syntax grammars to verify MATLAB syntax conformance (proper function signatures `function [out] = name(in)`, matching `end` statements, valid comments `%`, non-empty bodies, absence of Pythonisms like `def` or `import`).
   - Verifies the presence and integrity of all 4 exercise tiers (Recall, Understanding, Application, Challenge) across all modules.
   - Validates that every exercise file has a corresponding solution in `solutions/`.
   - Checks all Markdown links across READMEs, ensuring zero 404s or broken file references.
2. **Pytest Integration Test Suite (`tests/test_package_structure.py`):**
   - Wraps the verification auditor into standard `pytest` fixtures so that running `pytest` in `/home/settings/Documents/pearl/engineering-mathematics` executes the entire verification pipeline.
3. **Companion Mathematical Verification (`ml_bridge/04_python_ml_bridge.py` & companion scripts):**
   - Companion Python scripts use `numpy`, `scipy`, and `sympy` to execute the exact mathematical calculations presented in the MATLAB modules (e.g. eigenvalue decomposition, backslash solve $Ax=b$, trapezoidal integration, Runge-Kutta ODE solving, Monte Carlo pi estimation), proving mathematical correctness and reinforcing the cross-language comparison.

---

## 5. Authoritative Directory Tree & File Layout for `engineering-mathematics`

Based on `ORIGINAL_REQUEST.md`, `python-data-tools` precedent, and the Orchestrator's plan, the following layout is mapped out for `/home/settings/Documents/pearl/engineering-mathematics`.

### 5.1 High-Level Directory Overview

```text
/home/settings/Documents/pearl/engineering-mathematics/
├── README.md                                  <- Main Level 2 landing page & curriculum map
├── requirements.txt                           <- Python environment dependencies for testing/ML bridge
│
├── matlab/                                    <- Module 1: MATLAB Fundamentals & Environment (R1)
├── linear_algebra/                            <- Module 2: Linear Algebra for Engineers & ML (R2)
├── calculus/                                  <- Module 3: Calculus for Engineers (R3)
├── probability/                               <- Module 4: Probability & Uncertainty in Eng (R4)
├── simulink/                                  <- Module 5: Simulink for Beginners (R5)
│
├── capstone/                                  <- Integrated Engineering Telemetry Capstone (R6)
├── ml_bridge/                                 <- Level 1 -> Level 2 -> Level 3 Bridge (R6)
├── assessments/                               <- 100-Point Comprehensive Final Assessment (R6)
├── reference/                                 <- Central Quick Reference & Cheat Sheets (R6)
├── solutions/                                 <- Centralized Reference Solutions Repository
├── data/                                      <- Shared Engineering Datasets & Telemetry CSVs
├── scripts/                                   <- Package Verification & Validation Utilities
└── tests/                                     <- Pytest Test Suite for Package Integrity
```

---

### 5.2 Granular File-by-File Inventory (82 Files Total)

#### A. Root Package Files (2 files)
1. `engineering-mathematics/README.md`
   - Comprehensive curriculum guide, pedagogical philosophy ("Explain WHY before HOW"), 3-level pipeline roadmap (Level 1 $\to$ Level 2 $\to$ Level 3), repository layout, quickstart instructions, and prerequisites.
2. `engineering-mathematics/requirements.txt`
   - Python dependencies for testing, validation, and the ML bridge (`pytest>=8.0.0`, `numpy>=1.24.0`, `scipy>=1.10.0`, `matplotlib>=3.7.0`, `scikit-learn>=1.2.0`, `rich>=13.0.0`).

---

#### B. Module 1: MATLAB Fundamentals & Computational Environment (`matlab/`) (9 files)
*Fulfills Requirement R1: Transition from Python/NumPy to MATLAB, 1-based indexing, matrix vs element-wise math, functions, plotting, side-by-side comparison.*

1. `matlab/README.md`
   - Module teaching guide following standard template: Learning Objectives, Why Engineers Need MATLAB, Intuition, Syntax & Memory Architecture, Worked Examples, Common Mistakes, Exercises Overview.
2. `matlab/01_environment_and_variables.m`
   - Command Window, Workspace, `whos`, `clear`, `clc`, scalar assignment, variable types, semicolon suppression, memory inspection.
3. `matlab/02_vectors_and_matrices.m`
   - Row vs column vectors, 2D matrices, `zeros`, `ones`, `eye`, `linspace`, 1-based indexing, slicing (`start:step:stop`, `end`), column-major memory layout.
4. `matlab/03_matrix_vs_elementwise.m`
   - The defining MATLAB distinction: `*` vs `.*`, `/` vs `./`, `^` vs `.^`, conjugate transpose `'` vs non-conjugate transpose `.'`. Why MATLAB defaults to matrix operations.
5. `matlab/04_scripts_and_functions.m`
   - Scripts vs functions, input/output argument handling, multiple outputs (`[mean_val, std_val] = stat_calc(x)`), local helper functions.
6. `matlab/calculate_trajectory.m`
   - Reusable engineering function computing 2D projectile motion with drag, illustrating multiple returns and vectorized computation.
7. `matlab/05_plotting_and_visualization.m`
   - 2D curves (`plot`), styling (colors, markers, linewidth), multi-plot management (`hold on`, `grid on`, `legend`, `xlabel`, `ylabel`), `subplot`, 3D surface visualization (`surf`, `mesh`, `contour`).
8. `matlab/06_python_vs_matlab.m`
   - Side-by-side code demonstrations contrasting NumPy arrays with MATLAB matrices, indexing differences, and execution paradigms.
9. `matlab/exercises.m`
   - 4-Tier Student Exercises:
     - *Recall:* Matrix creation, indexing extraction, transpose.
     - *Understanding/Debugging:* Diagnosing dimension mismatch in `*` vs `.*` and off-by-one 1-based indexing bugs.
     - *Application:* Sensor calibration offset and scaling equation.
     - *Challenge:* Multi-stage array transformation and multi-panel subplot generator.

---

#### C. Module 2: Linear Algebra for Engineers & Machine Learning (`linear_algebra/`) (9 files)
*Fulfills Requirement R2: Applied linear algebra, dot products, projections, transformations, $Ax = b$ backslash operator, circuit/truss engineering models, eigenvalues/eigenvectors, ML connection.*

1. `linear_algebra/README.md`
   - Standard teaching guide: Learning Objectives, Why Engineers Need Linear Algebra, Intuition, Mathematics, MATLAB Implementation, Common Pitfalls, Exercises.
2. `linear_algebra/01_vectors_dot_cross_projections.m`
   - Vector norms ($L_1$, $L_2$), dot product (`dot`, `u'*v`), angle between vectors, orthogonal vector projection formula and implementation.
3. `linear_algebra/02_matrix_transforms_and_determinants.m`
   - 2D coordinate transformations (rotation matrix $R(\theta)$, scaling, shear), geometric meaning of determinant (`det`), area scaling, singularity detection.
4. `linear_algebra/03_systems_of_equations_backslash.m`
   - Solving $Ax = b$ using the backslash operator `x = A \ b` (`mldivide`). Comparison against `inv(A)*b` explaining numerical conditioning and floating-point errors.
5. `linear_algebra/04_matrix_inverses_and_conditioning.m`
   - Matrix inverse `inv(A)`, condition number `cond(A)`, ill-conditioned systems, Hilbert matrix sensitivity demonstration.
6. `linear_algebra/05_eigenvalues_and_eigenvectors.m`
   - Eigenvalue decomposition `[V, D] = eig(A)`, characteristic equation, physical vibration modes of a 2-DOF spring-mass system, principal stress directions.
7. `linear_algebra/06_linear_algebra_for_ml.m`
   - Transition to ML: Feature matrices $X \in \mathbb{R}^{N \times D}$, mean centering, covariance matrix $C = \frac{1}{N}X^T X$, Principal Component Analysis (PCA) projection.
8. `linear_algebra/mini_project_truss_analysis.m`
   - Applied Engineering Mini-Project: Static force equilibrium analysis of a 2D pin-jointed Warren truss. Assembles stiffness/equilibrium matrix $A$, load vector $b$, solves member forces $x = A \setminus b$, identifies tension vs compression members, plots deflected truss.
9. `linear_algebra/exercises.m`
   - 4-Tier Student Exercises:
     - *Recall:* Vector norms, dot products, eigenvalues calculation.
     - *Understanding/Debugging:* Fixing singular matrix division bugs and incorrect backslash orientation (`b / A` vs `A \ b`).
     - *Application:* Kirchhoff's Current Law (KCL) 3-loop circuit solver.
     - *Challenge:* Complete 3D coordinate frame transformation pipeline and PCA dimensionality reduction from scratch.

---

#### D. Module 3: Calculus for Engineers: Change, Accumulation, & Optimization (`calculus/`) (8 files)
*Fulfills Requirement R3: Rate of change, physical kinematics, slope visualization, optimization, accumulation/integration, trapz/integral, 1st-order ODEs (cooling, RC circuits), ode45.*

1. `calculus/README.md`
   - Standard teaching guide: Learning Objectives, Why Engineers Need Calculus, Rates of Change & Accumulation, Mathematical Formulations, MATLAB Implementation, Common Pitfalls, Exercises.
2. `calculus/01_functions_and_rates_of_change.m`
   - Physical motion kinematics: Position $s(t) \to$ Velocity $v(t) = \frac{ds}{dt} \to$ Acceleration $a(t) = \frac{dv}{dt}$. Numerical forward, backward, and central finite differences (`diff`).
3. `calculus/02_derivatives_tangents_optimization.m`
   - Visualizing tangent slopes, finding critical points ($f'(x) = 0$), second derivative test ($f''(x) > 0$), loss minimization intuition for machine learning.
4. `calculus/03_integration_as_accumulation.m`
   - Physical accumulation: Velocity to displacement ($s = \int v \, dt$), current to charge ($Q = \int I \, dt$), power to energy ($E = \int P \, dt$).
5. `calculus/04_numerical_integration.m`
   - Numerical integration algorithms: Trapezoidal rule (`trapz`), adaptive Simpson quadrature (`integral`), error analysis and step-size convergence.
6. `calculus/05_differential_equations.m`
   - First-order Ordinary Differential Equations (ODEs): Newton's Law of Cooling $\frac{dT}{dt} = -k(T - T_{env})$, RC circuit charging $\frac{dV_c}{dt} = \frac{V_{in} - V_c}{RC}$. Analytical solution vs numerical integration using `ode45`.
7. `calculus/mini_project_cooling_system.m`
   - Applied Engineering Mini-Project: Transient thermal analysis of an industrial electronics enclosure with variable ambient temperature and internal heat dissipation. Computes temperature profile via `ode45`, finds peak operating temperature, and sizes cooling heat sinks.
8. `calculus/exercises.m`
   - 4-Tier Student Exercises:
     - *Recall:* Finite difference calculation, `trapz` call, function handles `@(t, y)`.
     - *Understanding/Debugging:* Fixing `diff` array dimension mismatch (length $N-1$) and improper ODE function signature for `ode45`.
     - *Application:* Energy consumption calculation by integrating variable solar panel telemetry.
     - *Challenge:* Non-linear hydraulic tank drainage ODE solver ($\frac{dh}{dt} = -\frac{a}{A}\sqrt{2gh}$) with time-to-empty detection.

---

#### E. Module 4: Probability & Uncertainty in Engineering (`probability/`) (9 files)
*Fulfills Requirement R4: Noise modeling, physical variation, discrete/continuous RVs, distributions, expectation, variance, Bayes' rule, Monte Carlo simulations, sensor noise, reliability.*

1. `probability/README.md`
   - Standard teaching guide: Learning Objectives, Why Engineers Need Probability, Intuition, Mathematics of Uncertainty, MATLAB Implementation, Common Pitfalls, Exercises.
2. `probability/01_sample_spaces_and_random_variables.m`
   - Sample spaces, discrete vs continuous random variables, empirical histograms, cumulative distribution functions (CDF).
3. `probability/02_probability_distributions.m`
   - Uniform distribution (`rand`), Normal/Gaussian distribution (`randn`), Binomial distribution (`binornd` / manual formula). Probability density function (PDF) formulas, mean $\mu$, variance $\sigma^2$.
4. `probability/03_expectation_variance_and_moments.m`
   - Expected value $E[X]$, sample mean vs population mean, variance $\text{Var}(X)$, standard deviation $\sigma$, skewness, covariance.
5. `probability/04_conditional_probability_and_bayes.m`
   - Conditional probability $P(A|B) = \frac{P(A \cap B)}{P(B)}$, Bayes' Theorem, medical/industrial fault diagnostics, false alarm probability vs true positive rate.
6. `probability/05_monte_carlo_simulations.m`
   - Monte Carlo methods: Estimating $\pi$ via circle-square dart throwing, mechanical tolerance stack-up analysis across 5 manufactured interlocking components.
7. `probability/06_sensor_noise_and_filtering.m`
   - Sensor noise modeling: True signal + additive white Gaussian noise (AWGN), Signal-to-Noise Ratio (SNR) in decibels (dB), moving average filter implementation.
8. `probability/mini_project_component_reliability.m`
   - Applied Engineering Mini-Project: High-reliability satellite power subsystem composed of parallel redundant battery packs and series converters. Simulates component failure lifetimes (Weibull/Exponential distribution), calculates System Mean Time Between Failures (MTBF), and plots survival curves.
9. `probability/exercises.m`
   - 4-Tier Student Exercises:
     - *Recall:* Random number generation (`rand`, `randn`), mean and standard deviation computation.
     - *Understanding/Debugging:* Fixing improper scaling/shifting in `randn` ($\mu + \sigma \cdot z$) and Monte Carlo loop indexing bugs.
     - *Application:* Quality control defect rate estimation via binomial simulation.
     - *Challenge:* Monte Carlo estimation of structural beam failure probability under uncertain stochastic wind loading.

---

#### F. Module 5: Simulink for Beginners: Dynamic System Modeling (`simulink/`) (9 files)
*Fulfills Requirement R5: Connecting math to dynamic block-diagram simulations, blocks, signals, sources, sinks, feedback, solvers, companion scripts, physical models.*

1. `simulink/README.md`
   - Standard teaching guide: What is Simulink?, Block Diagram Paradigm vs Procedural Code, Blocks, Signals, Sources, Sinks, Feedback Loops, Numerical Solvers, Companion Script Architecture, Common Mistakes, Exercises.
2. `simulink/01_simulink_fundamentals.m`
   - Conceptual introduction script: Simulating block diagram execution flow in MATLAB code, comparing state integration in continuous time vs discrete steps.
3. `simulink/02_first_order_system_rc_circuit.m`
   - Companion MATLAB script for RC circuit simulation: Defines parameters ($R, C, V_{step}$), simulates system response, computes 63.2% rise time ($1\tau$), and plots comparative response.
4. `simulink/03_thermal_system_simulation.m`
   - Companion MATLAB script for thermal cooling block diagram: Implements convective heat transfer model, ambient step input, and equilibrium state verification.
5. `simulink/04_dc_motor_speed_response.m`
   - Companion MATLAB script for electromechanical DC motor model: Couples electrical armature equation ($V = Ri + L\frac{di}{dt} + K_b \omega$) with mechanical rotor dynamics ($J\frac{d\omega}{dt} = K_t i - b\omega$).
6. `simulink/models/rc_circuit_model_spec.md`
   - Step-by-step block-by-block diagram blueprint for building the RC circuit model in Simulink (Step $\to$ Sum $\to$ Gain $\to$ Integrator $\to$ Scope), including port configurations and solver settings.
7. `simulink/models/thermal_cooling_model_spec.md`
   - Step-by-step block-by-block diagram blueprint for building the thermal cooling model in Simulink.
8. `simulink/models/dc_motor_model_spec.md`
   - Step-by-step block-by-block diagram blueprint for building the 2nd-order DC motor electromechanical simulation.
9. `simulink/exercises.m`
   - 4-Tier Student Exercises:
     - *Recall:* Identifying Simulink block categories (Sources, Sinks, Continuous, Math Operations).
     - *Understanding/Debugging:* Diagnosing algebraic loop errors, improper integrator initial conditions, and solver step-size instability.
     - *Application:* Parameterizing a mass-spring-damper second-order block diagram companion script.
     - *Challenge:* Designing a closed-loop Proportional-Integral (PI) speed governor companion simulation with disturbance rejection.

---

#### G. Capstone: Integrated Engineering Telemetry Project (`capstone/`) (6 files)
*Fulfills Requirement R6: Multi-disciplinary project combining MATLAB, linear algebra, calculus, probability, and visual multi-panel dashboard.*

1. `capstone/README.md`
   - Capstone specification: Autonomous Electric Vehicle (EV) Powertrain & Telemetry Audit.
   - Comprehensive problem statement, physical telemetry variables, workflow steps, expected deliverables, and 100-point rubric.
2. `capstone/generate_telemetry_data.m`
   - Data generation script producing realistic telemetry: time vector, motor phase currents, battery voltage, chassis accelerations (with gravity and drift), wheel speed RPM, temperature, and AWGN sensor noise.
3. `capstone/data/ev_powertrain_telemetry.csv`
   - The realistic 1,000-row telemetry dataset generated by `generate_telemetry_data.m`.
4. `capstone/starter_capstone.m`
   - Student starter template containing full workflow structure, data loading logic, descriptive TODO markers, and plotting scaffolds.
5. `capstone/capstone_telemetry_analysis.m`
   - Complete, reference implementation executing:
     1. Data import and cleaning.
     2. Linear algebra coordinate transformation (converting body-frame accelerations to inertial frame via rotation matrix).
     3. Calculus integration: Integrating current over time to compute consumed Ampere-hours ($Q = \int I \, dt$), integrating acceleration to velocity ($v = \int a \, dt$).
     4. Probability & noise analysis: Computing signal statistics, estimating noise variance, applying 5-point moving average filter.
     5. Multi-panel diagnostic telemetry dashboard (4 subplots: Raw vs Filtered Telemetry, Consumed Battery Energy, Inertial Trajectory, Noise Distribution Histogram).
6. `capstone/ev_telemetry_dashboard.png`
   - Visual reference artifact illustrating the expected high-resolution 4-panel dashboard output.

---

#### H. Machine Learning Bridge: Level 1 $\to$ Level 2 $\to$ Level 3 (`ml_bridge/`) (5 files)
*Fulfills Requirement R6: Conceptual and practical bridge connecting Python data tools, engineering math, and ML (Scikit-Learn/PyTorch).*

1. `ml_bridge/README.md`
   - Comprehensive architectural guide: "The Three-Tier Pipeline".
   - Maps Level 1 (`python-data-tools`: Pandas tables, NumPy arrays) $\to$ Level 2 (`engineering-mathematics`: matrix transforms, gradients, probability density) $\to$ Level 3 (Machine Learning: weights, loss functions, optimization, Bayes classifiers, evaluation metrics).
2. `ml_bridge/01_linear_algebra_to_ml.m`
   - Matrix representations in ML: Feature matrix $X \in \mathbb{R}^{N \times D}$, target vector $y$, linear regression normal equation $\beta = (X^T X)^{-1} X^T y$ solved stably via `X \ y`, and Singular Value Decomposition (SVD).
3. `ml_bridge/02_calculus_to_optimization.m`
   - Calculus in ML: Loss functions (Mean Squared Error $J(w)$), analytical gradient $\nabla J(w)$, batch Gradient Descent implementation from scratch in MATLAB, visualizing the loss surface and descent path.
4. `ml_bridge/03_probability_to_classification.m`
   - Probability in ML: Maximum Likelihood Estimation (MLE), Bayes Decision Rule, Gaussian Naive Bayes classifier implementation classifying two-class sensor faults.
5. `ml_bridge/04_python_ml_bridge.py`
   - Executable, production-grade Python script mirroring the MATLAB ML bridge using `numpy`, `scipy`, and `scikit-learn`. Demonstrates identical normal equations, gradient descent steps, and classification metrics, cementing cross-language fluency.

---

#### I. Comprehensive Assessments (`assessments/`) (3 files)
*Fulfills Requirement R6: 100-point rubric assessment, conceptual questions, code-reading, debugging, engineering analysis.*

1. `assessments/FINAL_ASSESSMENT.md`
   - 100-Point Final Exam:
     - Part 1: Conceptual Understanding (20 Points) — 4 questions on memory layout, linear solver selection, calculus accumulation, and probability modeling.
     - Part 2: Code Reading & Output Prediction (20 Points) — 4 code snippets (matrix indexing, backslash solve, `diff` length reduction, Gaussian noise filtering) requiring exact output prediction and explanation.
     - Part 3: Code Debugging Challenges (20 Points) — 4 broken snippets with subtle bugs (elementwise vs matrix operator misuse, singular matrix inversion, improper ODE signature, Monte Carlo off-by-one).
     - Part 4: Practical Engineering Analysis (40 Points) — Applied telemetry analysis challenge requiring matrix transformation, numerical integration, and noise filtering.
2. `assessments/assessment_rubric.md`
   - Complete 100-point grading rubric with objective criteria for each question, point deductions for common student errors, and qualitative scoring tiers.
3. `assessments/practical_assessment_runner.m`
   - Scaffolded MATLAB test runner for students to implement and verify their practical exam answers.

---

#### J. Central Quick Reference & Cheat Sheets (`reference/`) (6 files)
*Fulfills Requirement R6: Concise, high-density cheat sheets for every subject area and a cross-language Rosetta Stone.*

1. `reference/README.md`
   - Index of quick reference guides and recommended engineering lookup workflows.
2. `reference/matlab_cheat_sheet.md`
   - High-density syntax guide: Environment commands, vector/matrix creation, slicing syntax, matrix vs elementwise operators, functions, plotting commands.
3. `reference/linear_algebra_cheat_sheet.md`
   - Formulas and MATLAB commands: Dot/cross products, projections, matrix multiplication, determinants, inverses, backslash solver, eigenvalues/eigenvectors, PCA.
4. `reference/calculus_cheat_sheet.md`
   - Formulas and MATLAB commands: Numerical derivatives (`diff`), critical points, integration (`trapz`, `integral`), 1st-order ODE formulas, `ode45` syntax.
5. `reference/probability_cheat_sheet.md`
   - Formulas and MATLAB commands: Distributions (PDF, CDF), expected value, variance, standard deviation, Bayes' theorem, random number generators, SNR formulas.
6. `reference/python_matlab_rosetta.md`
   - Exhaustive side-by-side Rosetta Stone table translating over 60 operations between Python/NumPy/SciPy/Matplotlib and MATLAB.

---

#### K. Central Reference Solutions Repository (`solutions/`) (8 files)
*Fulfills Acceptance Criteria: Dedicated solution files completely separated from student exercise templates.*

1. `solutions/README.md`
   - Instructor guide to the reference solutions, code verification standards, and pedagogical advice for grading.
2. `solutions/matlab_exercises_solution.m`
   - Complete, verified solutions for all 4 tiers of `matlab/exercises.m`.
3. `solutions/linear_algebra_exercises_solution.m`
   - Complete, verified solutions for all 4 tiers of `linear_algebra/exercises.m`.
4. `solutions/calculus_exercises_solution.m`
   - Complete, verified solutions for all 4 tiers of `calculus/exercises.m`.
5. `solutions/probability_exercises_solution.m`
   - Complete, verified solutions for all 4 tiers of `probability/exercises.m`.
6. `solutions/simulink_exercises_solution.m`
   - Complete, verified solutions for all 4 tiers of `simulink/exercises.m`.
7. `solutions/capstone_solution.m`
   - Standalone reference implementation of the EV telemetry capstone analysis.
8. `solutions/assessment_answers.md`
   - Complete, authoritative answer key and model responses for all 100 points of `assessments/FINAL_ASSESSMENT.md`.

---

#### L. Shared Engineering Datasets (`data/`) (2 files)
1. `data/README.md`
   - Documentation of dataset schemas, units of measurement, physical contexts, and sampling frequencies.
2. `data/ev_powertrain_telemetry.csv`
   - Central repository copy of the 1,000-row telemetry dataset used across the capstone, assessments, and exercises.

---

#### M. Verification Infrastructure & Test Suites (`scripts/` and `tests/`) (3 files)
*Fulfills Acceptance Criteria: Python-based syntax and structure auditor, cross-reference verifier, automated test suite.*

1. `scripts/verify_package.py`
   - Self-contained, executable Python verification script:
     - Scans the entire package to ensure all 82 expected files exist.
     - Validates that every exercise file contains all 4 distinct levels (`LEVEL 1: RECALL`, `LEVEL 2: UNDERSTANDING`, `LEVEL 3: APPLICATION`, `LEVEL 4: CHALLENGE`).
     - Performs static syntax parsing on all `.m` files (verifies matching `function ... end`, no invalid Python keywords, proper commenting).
     - Checks all internal Markdown relative links to ensure 0 broken links.
     - Confirms that every exercise has a corresponding solution in `solutions/`.
2. `tests/test_package_structure.py`
   - Pytest-native test suite importing `scripts/verify_package.py` and running automated assertions against directory structure, file completeness, syntax validity, and documentation links.
3. `tests/__init__.py`
   - Test package initialization file.

---

## 6. Structural Mapping & Requirements Traceability Matrix

The table below proves 100% requirements coverage across all deliverables:

| Requirement / Acceptance Item | Target Directory / Deliverable Files | Traceability & Scope |
|---|---|---|
| **R1. MATLAB Fundamentals** | `matlab/` (9 files) | Environment, vectors/matrices, matrix vs elementwise math, functions, plotting, Python comparison, 4-tier exercises. |
| **R2. Linear Algebra** | `linear_algebra/` (9 files) | Dot products, projections, coordinate transforms, backslash solver $Ax=b$, circuit/truss engineering models, eigenvalues, ML connection, mini-project, 4-tier exercises. |
| **R3. Calculus for Engineers** | `calculus/` (8 files) | Rates of change ($s \to v \to a$), slope visualization, optimization, accumulation ($v \to s$, $I \to Q$), `trapz`, `integral`, 1st-order ODEs (`ode45`), cooling mini-project, 4-tier exercises. |
| **R4. Probability & Uncertainty** | `probability/` (9 files) | Sample spaces, distributions (Uniform, Binomial, Normal), moments, Bayes' rule, Monte Carlo, sensor noise, reliability mini-project, 4-tier exercises. |
| **R5. Simulink for Beginners** | `simulink/` (9 files) | Block diagrams, sources, sinks, feedback loops, solvers, companion scripts (RC, thermal, DC motor), model specs, 4-tier exercises. |
| **R6. Capstone Project** | `capstone/` (6 files) | Integrated EV telemetry capstone, dataset generator, raw CSV data, starter template, full analysis script, dashboard visual artifact. |
| **R6. Machine Learning Bridge** | `ml_bridge/` (5 files) | 3-tier pipeline roadmap, linear algebra to ML, calculus to optimization, probability to classification, executable Python comparison script. |
| **R6. Assessments** | `assessments/` (3 files) | 100-point final exam (concept, code reading, debugging, telemetry project), explicit scoring rubric, student runner script. |
| **R6. Quick Reference Sheets** | `reference/` (6 files) | Cheat sheets for MATLAB, Linear Algebra, Calculus, Probability, Simulink, plus exhaustive Python-MATLAB Rosetta Stone. |
| **Acceptance: Separated Solutions** | `solutions/` (8 files) | Standalone reference solutions for all 5 module exercises, capstone project, and full assessment answer key. |
| **Acceptance: Verification Script** | `scripts/verify_package.py`, `tests/test_package_structure.py` | Python-based syntax and structure auditor validating files, syntax, links, and exercise tiers via `pytest`. |

---

## 7. Comparative Analysis: Level 1 (`python-data-tools`) vs Level 2 (`engineering-mathematics`)

| Dimension | Level 1: `python-data-tools` | Level 2: `engineering-mathematics` |
|---|---|---|
| **Primary Languages** | Python (NumPy, Pandas, Matplotlib) | MATLAB (`.m`) with Python companion validation |
| **Mathematical Abstraction** | Data structures: 1D/2D arrays, series, dataframes | Mathematical objects: Vector spaces, linear operators, ODEs, probability distributions |
| **Primary Operations** | Tabular filtering, grouped aggregation, data cleaning | Matrix transformations, $Ax = b$ backslash solve, numerical integration, differential equations |
| **Indexing Paradigm** | 0-based, half-open intervals `[start, stop)` | 1-based, closed intervals `start:step:stop` |
| **Arithmetic Default** | Element-wise arithmetic (`*` is elementwise) | Matrix algebra (`*` is matrix multiplication; `.*` is elementwise) |
| **Visualization Goal** | Business & descriptive plots (bars, correlations) | Engineering diagnostics (subsystem telemetry, dynamic response, vector fields) |
| **Upstream Prerequisite** | Basic Python (variables, loops, functions) | Level 1 (`python-data-tools` or foundational Python) |
| **Downstream Destination** | Data Analytics / Entry-level data science | Level 3: Machine Learning, Robotics, Dynamic Control Systems |

---

## 8. Recommendations for the Implementation Phase

1. **Scaffold Directory Skeleton Immediately:** Create all 13 planned subdirectories within `/home/settings/Documents/pearl/engineering-mathematics`.
2. **Prioritize the Verification Harness First:** Build `scripts/verify_package.py` and `tests/test_package_structure.py` early so Worker agents can validate their deliverables incrementally.
3. **Strict Adherence to Exercise Tiers:** Ensure every `exercises.m` file has clearly demarcated sections for Level 1 Recall, Level 2 Understanding/Debugging, Level 3 Application, and Level 4 Challenge.
4. **Authentic Mathematical Code (No Dummy Facades):** All MATLAB scripts must contain real, working mathematics, parameter values, and clear engineering comments.
5. **Cross-Language Consistency:** Ensure that the Python companion script (`ml_bridge/04_python_ml_bridge.py`) produces numerical results that match the MATLAB bridge scripts, establishing genuine cross-language equivalence.

---
*Report compiled by Explorer Survey 2 for the Teamwork Preview Orchestrator and Worker subagents.*
