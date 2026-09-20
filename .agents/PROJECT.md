# Project: Engineering Mathematics + MATLAB Teaching Package (Level 2)

## Architecture
The Engineering Mathematics + MATLAB teaching package serves as Level 2 in the curriculum pipeline: connecting Level 1 (`python-data-tools`: Python, NumPy, Pandas, Matplotlib) to Level 3 (Machine Learning).

```
Level 1: python-data-tools (NumPy, Pandas, Matplotlib)
                      │
                      ▼
Level 2: engineering-mathematics (MATLAB, Linear Algebra, Calculus, Probability, Simulink)
                      │
                      ▼
Level 3: Machine Learning (Scikit-Learn, PyTorch, Optimization, Statistical Learning)
```

### Module Boundaries & Directory Layout
Target directory: `/home/settings/Documents/pearl/engineering-mathematics/`
```
engineering-mathematics/
├── README.md                          # Master curriculum index & pedagogical philosophy
├── requirements.txt                   # Python verification dependencies
├── matlab/                            # R1: MATLAB Fundamentals & Environment
│   ├── README.md                      # 9-section teaching guide (Explain WHY before HOW)
│   ├── 01_environment_and_variables.m # Environment, workspace, data types, memory
│   ├── 02_vectors_and_matrices.m      # 1-based indexing, slicing, concatenation
│   ├── 03_operations_and_math.m       # Matrix vs element-wise operations (.*, ./, .^)
│   ├── 04_scripts_and_functions.m     # User-defined functions, multiple outputs
│   ├── 05_plotting_and_visualization.m# 2D/3D visualization (plot, subplot, surf)
│   ├── 06_python_numpy_bridge.m       # Side-by-side Rosetta stone & mental model
│   ├── mini_project_signal_calc.m     # Foundational mini-project
│   └── exercises.m                    # 4-tier progressive exercises (Levels 1-4)
├── linear_algebra/                    # R2: Linear Algebra for Engineers & ML
│   ├── README.md                      # 9-section teaching guide
│   ├── 01_vectors_and_spaces.m        # Dot products, projections, coordinate frames
│   ├── 02_matrix_transformations.m    # Rotations, scaling, shear, determinants
│   ├── 03_solving_linear_systems.m    # Gaussian elimination & backslash x = A\b
│   ├── 04_engineering_systems.m       # Circuit nodal analysis & truss force balance
│   ├── 05_eigenvalues_eigenvectors.m  # Characteristic equation, vibration/stress modes
│   ├── 06_linear_algebra_for_ml.m     # Feature matrices, weight vectors, covariance
│   ├── mini_project_truss_analysis.m  # Applied structural truss mini-project
│   └── exercises.m                    # 4-tier progressive exercises
├── calculus/                          # R3: Calculus for Engineers
│   ├── README.md                      # 9-section teaching guide
│   ├── 01_derivatives_and_rates.m     # Kinematics s(t)->v(t)->a(t), numerical diff
│   ├── 02_slope_and_optimization.m    # Tangent visualization, critical points, loss
│   ├── 03_integration_accumulation.m  # Accumulation (v->s, I->Q, P->E), trapz, integral
│   ├── 04_differential_equations.m    # 1st-order ODEs (Newton cooling, RC) via ode45
│   ├── mini_project_thermal_system.m  # Transient thermal cooling mini-project
│   └── exercises.m                    # 4-tier progressive exercises
├── probability/                       # R4: Probability & Uncertainty in Engineering
│   ├── README.md                      # 9-section teaching guide
│   ├── 01_probability_foundations.m   # Sample spaces, events, axioms, conditional/Bayes
│   ├── 02_distributions_and_moments.m # Uniform, Binomial, Normal, mean, variance, sigma
│   ├── 03_monte_carlo_simulation.m    # Monte Carlo simulation & numerical experiments
│   ├── 04_sensor_noise_filtering.m    # Gaussian noise modeling & moving average filter
│   ├── mini_project_reliability.m     # Component MTBF & reliability mini-project
│   └── exercises.m                    # 4-tier progressive exercises
├── simulink/                          # R5: Simulink for Beginners
│   ├── README.md                      # 9-section teaching guide
│   ├── 01_block_diagram_basics.md     # Blocks, signals, sources, sinks, feedback
│   ├── 02_solvers_and_simulation.md   # ODE solvers, step sizes, simulation time
│   ├── 03_rc_circuit_companion.m      # RC charging simulation script (ode45)
│   ├── 04_thermal_cooling_companion.m # Thermal cooling simulation script
│   ├── 05_dc_motor_companion.m        # DC motor speed response simulation script
│   ├── mini_project_motor_control.m   # DC motor feedback control mini-project
│   ├── models/                        # Step-by-step block diagram visual blueprints
│   │   ├── rc_circuit_model.md
│   │   ├── thermal_cooling_model.md
│   │   └── dc_motor_model.md
│   └── exercises.m                    # 4-tier progressive exercises
├── capstone/                          # R6: Integrated Capstone Project
│   ├── README.md                      # EV Powertrain Telemetry Capstone Specification
│   ├── generate_capstone_data.m       # Telemetry generator script
│   ├── generate_capstone_data.py      # Python fallback generator
│   ├── capstone_analysis_template.m   # Student starter template
│   └── capstone_analysis_complete.m   # Full reference implementation
├── ml_bridge/                         # R6: Machine Learning Bridge
│   ├── README.md                      # 3-tier roadmap (Level 1 -> Level 2 -> Level 3)
│   ├── 01_linear_algebra_to_ml.md     # Features, weights, projections, PCA
│   ├── 02_calculus_to_optimization.md # Gradient descent, loss surfaces, backprop
│   ├── 03_probability_to_ml.md        # Likelihood, Bayes, entropy, classification
│   └── verify_ml_bridge.py            # Executable Python script validating math -> ML
├── assessments/                       # R6: Assessments & Rubric
│   ├── README.md                      # Assessment guide & test administration
│   ├── FINAL_ASSESSMENT.md            # 100-point comprehensive exam (4 sections)
│   └── RUBRIC.md                      # Detailed 100-point scoring rubric
├── reference/                         # R6: Central Quick Reference Sheets
│   ├── matlab_cheat_sheet.md          # Syntax, operators, indexing, plotting
│   ├── linear_algebra_cheat_sheet.md  # Vectors, matrices, backslash, eigenvalues
│   ├── calculus_cheat_sheet.md        # Derivatives, integrals, ODEs, functions
│   ├── probability_cheat_sheet.md     # Formulas, distributions, moments, noise
│   ├── simulink_cheat_sheet.md        # Block types, shortcuts, solver selection
│   └── python_matlab_rosetta.md       # Python/NumPy vs MATLAB side-by-side
├── solutions/                         # Decoupled Reference Solutions
│   ├── matlab_exercises_solution.m
│   ├── linear_algebra_exercises_solution.m
│   ├── calculus_exercises_solution.m
│   ├── probability_exercises_solution.m
│   ├── simulink_exercises_solution.m
│   ├── capstone_solution.m
│   └── final_assessment_answers.md
├── data/                              # Shared Telemetry Datasets & Schemas
│   ├── ev_telemetry.csv
│   └── dataset_schema.md
├── scripts/                           # Quality Assurance & Verification
│   └── verify_package.py              # Zero-dependency Python syntax & structure auditor
└── tests/                             # E2E Pytest Suite
    ├── __init__.py
    ├── test_package_structure.py      # Full E2E structural & link test suite
    └── test_mathematical_integrity.py # Numerical verification of algorithms
```

---

## Feature Inventory
Every feature from the Survey phase appears here with its assigned milestone.

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | MATLAB Environment & Workspace | Command window, workspace, editor, memory model, clear/clc | M1 | R1 |
| 2 | Variables & Types | double, char, string, logical, scalar vs vector vs matrix | M1 | R1 |
| 3 | Vectors & Concatenation | Row vs column vectors, transpose (`'`), `[A, B]`, `[A; B]` | M1 | R1 |
| 4 | Indexing & Slicing | 1-based indexing, `start:step:end`, linear & logical indexing | M1 | R1 |
| 5 | Element-wise vs Matrix Math | Physical/mathematical justification for `*` vs `.*`, `^` vs `.^` | M1 | R1 |
| 6 | Scripts & User Functions | Multiple inputs/outputs, local helper functions | M1 | R1 |
| 7 | 2D/3D Visualization | `plot`, `subplot`, `xlabel`, `ylabel`, `grid`, `legend`, `surf` | M1 | R1 |
| 8 | Python-NumPy Bridge | Side-by-side comparison, indexing differences, memory layout | M1 | R1 |
| 9 | M1 4-Tier Exercises & Solutions | Recall, Understanding, Application, Challenge + decoupled sol | M1 | R1, AC |
| 10 | Vector Operations | Norm, dot product, cross product, orthogonal projections | M2 | R2 |
| 11 | Matrix Transformations | Rotations, scaling, coordinate frame transformations, det | M2 | R2 |
| 12 | Matrix Invertibility & Condition | Determinants, rank, condition number `cond`, singularity | M2 | R2 |
| 13 | Linear Solvers $Ax = b$ | Backslash `x = A\b` vs `inv(A)*b`, numerical stability | M2 | R2 |
| 14 | Physical System Models | Circuit nodal analysis & pin-jointed truss force balance | M2 | R2 |
| 15 | Eigenvalues & Eigenvectors | `eig`, characteristic equation, vibration & principal stress | M2 | R2 |
| 16 | Linear Algebra for ML | Feature matrix $X$, weight vector $w$, covariance matrix | M2 | R2 |
| 17 | M2 Mini-Project & 4-Tier Exercises | Truss analysis mini-project + 4-tier exercises + solutions | M2 | R2, AC |
| 18 | Derivatives & Rates of Change | Kinematics $s(t) \to v(t) \to a(t)$, numerical `diff` | M3 | R3 |
| 19 | Slope & Optimization Intuition | Tangent line viz, critical points, loss minimization | M3 | R3 |
| 20 | Accumulation & Integration | Physical accumulation ($v \to s$, $I \to Q$, $P \to E$) | M3 | R3 |
| 21 | Numerical Quadrature | `trapz`, `integral`, Simpson's rule comparison | M3 | R3 |
| 22 | 1st-Order Differential Equations | Newton cooling, RC circuit transient response via `ode45` | M3 | R3 |
| 23 | M3 Mini-Project & 4-Tier Exercises | Thermal cooling mini-project + 4-tier exercises + solutions | M3 | R3, AC |
| 24 | Probability Foundations & Bayes | Sample spaces, discrete/continuous RVs, conditional, Bayes | M4 | R4 |
| 25 | Distributions & Moments | Uniform, Binomial, Normal, $\mu$, $\sigma^2$, $\sigma$ | M4 | R4 |
| 26 | Monte Carlo Simulations | `rand`, `randn`, `randi`, law of large numbers experiments | M4 | R4 |
| 27 | Sensor Noise & Filtering | Gaussian noise on sensor signals, moving-average filter | M4 | R4 |
| 28 | Component Reliability & MTBF | Exponential failure distribution, MTBF analysis | M4 | R4 |
| 29 | M4 Mini-Project & 4-Tier Exercises | Sensor telemetry reliability + 4-tier exercises + solutions | M4 | R4, AC |
| 30 | Simulink Block-Diagram Basics | Blocks, signals, sources, sinks, feedback loops | M5 | R5 |
| 31 | Solvers & Simulation Time | Fixed vs variable step, ODE45 Dormand-Prince, sample times | M5 | R5 |
| 32 | Simulink Companion Scripts | Standalone `.m` dynamic scripts (RC, thermal cooling, DC motor) | M5 | R5 |
| 33 | Simulink Visual Model Specs | Textual/graphical block blueprints (`simulink/models/*.md`) | M5 | R5 |
| 34 | M5 Mini-Project & 4-Tier Exercises | Motor speed control mini-project + 4-tier exercises + solutions | M5 | R5, AC |
| 35 | Integrated Capstone Project | EV powertrain telemetry project (combining linear alg, calc, noise) | M6 | R6 |
| 36 | Capstone Data Generator & CSV | Reproducible generator (`.m` and `.py`) + `ev_telemetry.csv` | M6 | R6 |
| 37 | Capstone Analysis Pipeline | Starter template + complete reference solution | M6 | R6 |
| 38 | Machine Learning Bridge | 3-tier roadmap (Level 1 -> 2 -> 3) + Python validation script | M6 | R6 |
| 39 | 100-Point Final Assessment | Conceptual, code reading, debugging, engineering interpretation | M6 | R6 |
| 40 | Scoring Rubric | Granular 100-point rubric breakdown | M6 | R6 |
| 41 | Central Reference Cheat Sheets | 4 cheat sheets (MATLAB, Linear Alg, Calc, Prob) + Rosetta stone | M6 | R6 |
| 42 | Decoupled Solutions Directory | Central `solutions/` directory pairing with all exercises | M6 | AC |
| 43 | Teaching Standard ("Explain WHY before HOW") | 9-section standard applied to all module `README.md` files | M1-M6 | AC |
| 44 | E2E Testing Track Infrastructure | `scripts/verify_package.py` + `tests/test_package_structure.py` | E2E Track | AC |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | `scripts/verify_package.py`, `tests/test_package_structure.py`, `TEST_INFRA.md`, publish `TEST_READY.md` | Survey | PLANNED |
| M1 | MATLAB Fundamentals | `matlab/` (README, 6 concept scripts, mini-project, exercises) + `solutions/matlab_exercises_solution.m` | Survey | PLANNED |
| M2 | Linear Algebra for Engineers | `linear_algebra/` (README, 6 concept scripts, mini-project, exercises) + `solutions/linear_algebra_exercises_solution.m` | M1 interfaces | PLANNED |
| M3 | Calculus for Engineers | `calculus/` (README, 4 concept scripts, mini-project, exercises) + `solutions/calculus_exercises_solution.m` | M1 interfaces | PLANNED |
| M4 | Probability & Uncertainty | `probability/` (README, 4 concept scripts, mini-project, exercises) + `solutions/probability_exercises_solution.m` | M1 interfaces | PLANNED |
| M5 | Simulink for Beginners | `simulink/` (README, 2 concept docs, 3 companion scripts, mini-project, models/, exercises) + `solutions/simulink_exercises_solution.m` | M3 ODEs | PLANNED |
| M6 | Capstone, ML Bridge, Assessments & Reference | `capstone/`, `ml_bridge/`, `assessments/`, `reference/`, `data/`, master `README.md`, final solutions | M1-M5 | PLANNED |
| Final | Final E2E Verification & Adversarial Hardening | 100% pass of E2E verification suite (Tiers 1-4) + Tier 5 Adversarial Coverage Hardening | All M1-M6, E2E Track | PLANNED |

---

## Interface Contracts

### 1. Pedagogical Template Contract (All Module `README.md` files)
Every module `README.md` MUST contain these 9 sections in order:
1. `# <Module Title>`
2. `## 1. Learning Objectives` (Action-oriented, Bloom's taxonomy)
3. `## 2. Why Engineers Need This` (Realistic industry context, Level 1 -> Level 2 transition)
4. `## 3. Mathematical Intuition` ("Explain WHY before HOW", physical metaphors)
5. `## 4. Formal Mathematics & Governing Equations` (LaTeX formulas, variable definitions)
6. `## 5. Worked Engineering Example` (Step-by-step hand calculation / problem formulation)
7. `## 6. MATLAB Implementation` (Clean code snippet, vectorization, standard syntax)
8. `## 7. Common Student Pitfalls & Debugging Tips` (1-based indexing, `*` vs `.*`, memory)
9. `## 8. Engineering Interpretation` (Connecting numerical outputs to physical decisions)
10. `## 9. Progressive Exercises Overview` (Link to `exercises.m` and 4 tiers)

### 2. 4-Tier Exercise Contract (All `exercises.m` files)
Every `exercises.m` MUST implement 4 distinct cell blocks:
- `%% Level 1: Recall` (Basic syntax reproduction, 1-based indexing, element-wise math)
- `%% Level 2: Understanding & Debugging` (Fixing buggy code, explaining differences)
- `%% Level 3: Application` (Solving a domain engineering problem independently)
- `%% Level 4: Challenge` (Combining multiple techniques, optimization, open-ended)
- Must contain `% TODO` markers for student completion.

### 3. Solution File Decoupling Contract
- For each `<module>/exercises.m`, a corresponding `solutions/<module>_exercises_solution.m` must exist.
- Reference solutions must contain 0 remaining `% TODO` markers and provide complete, runnable code with explanatory comments.

### 4. Code Quality & Syntax Contract
- Valid MATLAB syntax compatible with context-aware parser (balanced blocks `function...end`, `for...end`, `if...end`, balanced delimiters `()`, `[]`, `{}`).
- Minimum 20% comment lines explaining engineering rationale.
- Explicit prohibition of dummy facade stubs or hardcoded answers.

### 5. Telemetry & Data Contract (`capstone/` & `data/`)
- `data/ev_telemetry.csv` columns:
  `timestamp_s`, `motor_speed_rpm`, `motor_torque_nm`, `battery_voltage_v`, `battery_current_a`, `inverter_temp_c`, `ambient_temp_c`
- Units and physical ranges strictly documented in `data/dataset_schema.md`.
- `capstone_analysis_complete.m` must compute:
  1. Mechanical Power: $P_{\text{mech}} = \frac{\text{torque} \times \text{rpm} \times 2\pi}{60}$
  2. Electrical Power: $P_{\text{elec}} = V \times I$
  3. Powertrain Efficiency: $\eta = P_{\text{mech}} / P_{\text{elec}}$
  4. Total Energy Consumed: $E = \int P_{\text{elec}} dt$ via `trapz`
  5. Temperature Rate of Change: $dT/dt$ via numerical differentiation `diff`
  6. Noise Analysis: Gaussian filter on noisy telemetry signals.
