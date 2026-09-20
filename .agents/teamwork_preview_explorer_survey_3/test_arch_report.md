# Engineering Mathematics + MATLAB Teaching Package
## Test & Verification Infrastructure Architecture Report

**Author:** Explorer Survey 3 (Test & Verification Architect)  
**Target Repository:** `/home/settings/Documents/pearl/engineering-mathematics`  
**Date:** 2026-09-10  
**Status:** Approved Architecture & Specification  

---

## 1. Executive Summary & Verification Philosophy

### 1.1 Context and Purpose
The Engineering Mathematics + MATLAB teaching package serves as **Level 2** in the engineering curriculum pipeline, bridging **Level 1** (Python data tools: NumPy, Pandas, Matplotlib in `python-data-tools`) and **Level 3** (Machine Learning & Advanced Modeling). To ensure instructional excellence, the package must maintain uncompromising pedagogical clarity, absolute file integrity, and syntactically flawless MATLAB code.

Because the development and continuous-integration environment is Linux-based without proprietary MathWorks desktop MATLAB or Octave licenses, verification cannot depend on external proprietary runtime engines. Therefore, this document architectures a **self-contained, zero-proprietary-dependency Python verification suite** capable of:
1. Validating complete directory trees, module manifests, and mandatory teaching artifacts.
2. Detecting broken relative Markdown links and section anchor mismatches across all documentation.
3. Performing lexical analysis, bracket/delimiter balancing, control-flow block matching (`function...end`, `if...end`, `for...end`, etc.), semantic trap detection (such as Python-style 0-based indexing), and engineering rationale documentation auditing on all MATLAB `.m` files.
4. Auditing the 4-tier progressive exercise structure (Recall, Understanding, Application, Challenge) and verifying matching reference solutions.
5. Validating tabular telemetry datasets and capstone artifacts.
6. Executing a formal 4-tier E2E testing framework combining Category-Partition, Boundary Value Analysis, Pairwise Combinatorics, and Real-World User Scenarios.

### 1.2 Verification Philosophy: The "Zero-Silent-Failure" Standard
Educational repositories require higher verification rigor than standard software packages:
- **No Broken Mental Models:** A syntax error or broken link in an educational template destroys student trust and creates cognitive friction.
- **Explain WHY before HOW:** Code without engineering rationale comments fails the curriculum standard.
- **Structural Symmetry:** Every exercise file must have a 1:1 paired reference solution with matching variables and verified tier completion.
- **Dual Execution Modes:** The verification harness must run both as an instant single-file CLI tool (`python scripts/verify_package.py`) for rapid local development, and as a formal `pytest` suite for automated regression testing.

---

## 2. Verification Harness Architecture

### 2.1 System Decomposition
The verification infrastructure consists of an extensible modular pipeline with five specialized validation engines coordinated by a master test runner:

```
                      +----------------------------------+
                      |      VerificationRunner          |
                      |   (CLI & Pytest Test Runner)     |
                      +-----------------+----------------+
                                        |
      +-------------------+-------------+-------------+-------------------+
      |                   |                           |                   |
+-----v-----+      +------v------+             +------v------+     +------v------+
| Directory |      |  Markdown   |             |   MATLAB    |     |  Exercise   |
| Structure |      | Cross-Link  |             |   Syntax    |     |    Tier     |
| Validator |      |  Validator  |             |   Auditor   |     |   Auditor   |
+-----+-----+      +------+------+             +------+------+     +------+------+
      |                   |                           |                   |
      +-------------------+-------------+-------------+-------------------+
                                        |
                              +---------v---------+
                              | Dataset & Capstone|
                              |     Validator     |
                              +---------+---------+
                                        |
                              +---------v---------+
                              | Unified Report &  |
                              | Diagnostic Output |
                              +-------------------+
```

### 2.2 Standardized Diagnostic Model
Every validator yields structured diagnostic records conforming to the following dataclass model:

```python
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any

class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARN"
    ERROR = "ERROR"

@dataclass
class Diagnostic:
    validator: str
    severity: Severity
    file_path: Path
    line_number: Optional[int]
    column_number: Optional[int]
    message: str
    remediation: str
    context_snippet: Optional[str] = None

@dataclass
class ValidationReport:
    total_checks: int = 0
    passed_checks: int = 0
    warning_count: int = 0
    error_count: int = 0
    diagnostics: List[Diagnostic] = field(default_factory=list)
    
    @property
    def is_success(self) -> bool:
        return self.error_count == 0
```

---

## 3. Subsystem Specifications

### 3.1 Subsystem 1: Directory Structure & Manifest Validator (`DirectoryStructureValidator`)

#### 3.1.1 Mandatory Target Directory Tree Schema
The validator checks the existence, type, and non-emptiness of all designated modules, subdirectories, and key artifacts:

```
engineering-mathematics/
├── README.md                                 # Top-level curriculum map & quick-start
├── PROJECT.md                                # Unified technical architecture & milestones
├── matlab/                                   # R1: MATLAB Fundamentals
│   ├── README.md                             # 9-section teaching guide
│   ├── 01_environment_basics.m               # Desktop, variables, memory model
│   ├── 02_vectors_and_matrices.m             # Construction, 1-based indexing, slicing
│   ├── 03_matrix_vs_elementwise.m            # *, /, ^ vs .*, ./, .^
│   ├── 04_plotting_foundations.m             # plot, subplot, labels, 2D/3D
│   ├── 05_user_functions.m                   # Multi-input, multi-output functions
│   ├── exercises.m                           # 4-tier student practice template
│   └── solutions/
│       └── exercises_solution.m              # Dedicated reference solutions
├── linear_algebra/                           # R2: Linear Algebra for Engineers & ML
│   ├── README.md                             # 9-section teaching guide
│   ├── 01_vectors_projections.m              # Dot product, geometric projection
│   ├── 02_matrix_transforms.m                # Transformations, determinants, rank
│   ├── 03_linear_systems_solve.m             # x = A\b vs inv(A), condition number
│   ├── 04_eigenvalues_eigenvectors.m         # eig(A), physical vibration modes
│   ├── 05_truss_circuit_project.m            # Mini-project: structural/circuit system
│   ├── exercises.m                           # 4-tier student practice template
│   └── solutions/
│       └── exercises_solution.m              # Dedicated reference solutions
├── calculus/                                 # R3: Calculus (Change, Accumulation, Opt)
│   ├── README.md                             # 9-section teaching guide
│   ├── 01_rates_of_change.m                  # Kinematics s(t)->v(t)->a(t), diff()
│   ├── 02_numerical_integration.m           # trapz, integral, accumulation
│   ├── 03_optimization_loss.m                # Critical points, gradient descent intuition
│   ├── 04_differential_equations.m           # 1st-order ODEs (cooling, RC circuits, ode45)
│   ├── 05_calculus_mini_project.m            # Dynamic system response mini-project
│   ├── exercises.m                           # 4-tier student practice template
│   └── solutions/
│       └── exercises_solution.m              # Dedicated reference solutions
├── probability/                              # R4: Probability & Uncertainty
│   ├── README.md                             # 9-section teaching guide
│   ├── 01_random_variables.m                 # Discrete vs continuous distributions
│   ├── 02_expectation_variance.m             # Mean, variance, std, conditional prob
│   ├── 03_monte_carlo_simulation.m           # Stochastic experiments, noise generation
│   ├── 04_sensor_reliability.m               # Component MTBF & reliability analysis
│   ├── 05_probability_mini_project.m         # Sensor noise filtering mini-project
│   ├── exercises.m                           # 4-tier student practice template
│   └── solutions/
│       └── exercises_solution.m              # Dedicated reference solutions
├── simulink/                                 # R5: Simulink for Beginners
│   ├── README.md                             # 9-section guide + block diagram workflows
│   ├── companions/                           # Standalone ODE45 script companions
│   │   ├── rc_circuit_companion.m            # RC charging state equation simulation
│   │   ├── thermal_cooling_companion.m       # Newton's law ODE simulation
│   │   └── motor_speed_companion.m           # DC motor velocity response
│   ├── exercises.m                           # 4-tier student practice template
│   └── solutions/
│       └── exercises_solution.m              # Dedicated reference solutions
├── capstone/                                 # R6: Integrated Capstone Project
│   ├── README.md                             # Multi-disciplinary mission & rubric
│   ├── data/
│   │   └── industrial_telemetry.csv          # Multi-sensor time series dataset
│   ├── starter_template.m                    # Scaffolded capstone template
│   ├── capstone_solution.m                   # Comprehensive reference solution
│   └── generate_telemetry.py                 # Deterministic dataset generation script
├── ml_bridge/                                # R6: Machine Learning Bridge
│   ├── README.md                             # Level 1 -> Level 2 -> Level 3 roadmap
│   ├── math_to_ml_roadmap.md                 # Concept mapping matrix
│   ├── linear_regression_bridge.m            # Normal equations & gradient in MATLAB
│   └── linear_regression_bridge.py           # Matching Scikit-Learn validation
├── assessments/                              # R6: Assessments & Exams
│   ├── FINAL_ASSESSMENT.md                   # 100-point comprehensive exam
│   ├── assessment_rubric.md                  # Grading rubric & learning objectives
│   └── assessment_answers.md                 # Complete faculty answer key
├── reference/                                # R6: Quick Reference Cheat Sheets
│   ├── matlab_cheatsheet.md                  # Syntax, indexing, operators, plotting
│   ├── linear_algebra_cheatsheet.md          # Matrix rules, eigenvalues, solve
│   ├── calculus_cheatsheet.md                # Derivative/integral rules, ode45
│   └── probability_cheatsheet.md             # Distributions, formulas, Monte Carlo
├── datasets/                                 # Centralized Engineering Datasets
│   ├── industrial_telemetry.csv              # Industrial pump telemetry
│   └── sensor_calibration.csv                # Voltage-temperature calibration
├── scripts/                                  # Test & Verification Infrastructure
│   ├── verify_package.py                     # Standalone package auditor
│   └── generate_test_data.py                 # Test fixture generator
└── tests/                                    # Pytest Test Suite
    ├── test_package_structure.py             # Manifest & directory tests
    ├── test_markdown_links.py                # Cross-reference & anchor tests
    ├── test_matlab_syntax.py                 # Lexer, block, delimiter tests
    ├── test_exercise_tiers.py                # Tier 1-4 exercise auditor tests
    └── test_datasets_and_capstone.py         # CSV & Capstone tests
```

#### 3.1.2 Validation Rules
1. **Directory Existence**: All 10 primary directories (`matlab/`, `linear_algebra/`, `calculus/`, `probability/`, `simulink/`, `capstone/`, `ml_bridge/`, `assessments/`, `reference/`, `datasets/`, `scripts/`, `tests/`) must exist.
2. **File Non-Emptiness**: Every file must be strictly $> 0$ bytes.
3. **Minimum Content Thresholds**:
   - Module `README.md` files: $\ge 1,500$ bytes (ensuring full 9-part pedagogical coverage).
   - `.m` script files: $\ge 200$ bytes (preventing empty stubs).
   - Cheat sheets: $\ge 1,000$ bytes.
   - `FINAL_ASSESSMENT.md`: $\ge 3,000$ bytes.
4. **Naming Conventions**:
   - MATLAB `.m` files must be lowercase with underscores (`[a-z0-9_]+\.m`) to satisfy MATLAB's identifier rules.
   - Markdown files must use standard naming (`README.md`, `*_cheatsheet.md`, `FINAL_ASSESSMENT.md`).

---

### 3.2 Subsystem 2: Markdown Cross-Reference & Link Validator (`MarkdownLinkValidator`)

#### 3.2.1 Link Extraction Engine
The link validator inspects every `.md` file across the package, extracting both inline links and reference links:
- Inline links: `\[([^\]]+)\]\(([^)]+)\)`
- Image references: `!\[([^\]]*)\]\(([^)]+)\)`

#### 3.2.2 Path Resolution & Anchor Verification
For each link target `target_str`:
1. **External Filter**: If `target_str` starts with `http://`, `https://`, `mailto:`, or `ftp://`, categorize as external.
2. **Path Decomposition**: Split `target_str` into `file_part` and `anchor_part` at `#`.
3. **Relative Path Resolution**:
   - If `file_part` is non-empty: compute `target_path = (current_file.parent / file_part).resolve()`.
   - Verify `target_path.exists()` on filesystem. If not, emit `Diagnostic(Severity.ERROR, "Broken relative link: file does not exist")`.
4. **Heading Slug Parsing & Anchor Validation**:
   - If `anchor_part` is present:
     - Read the target Markdown file (or current file if `file_part` is empty).
     - Extract all Markdown headings (`^#{1,6}\s+(.+)$`).
     - Convert headings to CommonMark/GitHub slugs:
       $$\text{slug}(h) = \text{re.sub}(r'[^a-z0-9\-_ ]', '', h.strip().lower()).replace(' ', '-')$$
     - Check if `anchor_part` exists in the generated slug set.
     - If not, emit `Diagnostic(Severity.ERROR, f"Broken anchor '#{anchor_part}' in {target_path}")`.

#### 3.2.3 Cross-Module Link Integrity Matrix
The validator enforces that the curriculum navigation graph is complete and unbroken:
- `engineering-mathematics/README.md` must link to all 5 module READMEs, the capstone, the ML bridge, and the 4 cheat sheets.
- Each module `README.md` must link to its local `exercises.m`, its paired `solutions/exercises_solution.m`, and the central reference directory.
- `ml_bridge/README.md` must link back to `linear_algebra/README.md`, `calculus/README.md`, and `probability/README.md`.

---

### 3.3 Subsystem 3: Non-Proprietary MATLAB Syntax & Quality Auditor (`MatlabSyntaxAuditor`)

#### 3.3.1 Context-Aware Lexer Specification
MATLAB syntax presents unique lexical ambiguities that cannot be resolved with naive regexes. Most notably, the single quote character `'` denotes a **matrix conjugate transpose** in post-operand positions, but opens a **character vector literal** elsewhere.

The auditor implements a deterministic finite-state lexical scanner:

```python
class MatlabTokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"            # "double quoted string"
    CHAR_VEC = "CHAR_VEC"        # 'character array'
    TRANSPOSE = "TRANSPOSE"      # A' or (A+B)' or [1,2]'
    OPERATOR = "OPERATOR"        # .*, ./, .^, .\, *, /, ^, \, +, -, ==, etc.
    DELIMITER = "DELIMITER"      # (, ), [, ], {, }
    COMMENT = "COMMENT"          # % single-line comment
    BLOCK_COMMENT = "BLOCK_COMMENT" # %{ ... %}
    ELLIPSIS = "ELLIPSIS"        # ... line continuation
    NEWLINE = "NEWLINE"
    PUNCTUATION = "PUNCTUATION"  # ;, ,, :
```

**Transpose vs. Char Vector Disambiguation Rule:**
When encountering `'`:
- If the immediately preceding non-whitespace token is one of `[IDENTIFIER, DELIMITER_CLOSE_PAREN ')', DELIMITER_CLOSE_BRACKET ']', DELIMITER_CLOSE_BRACE '}', TRANSPOSE, CHAR_VEC]`:
  $\rightarrow$ Emit `TRANSPOSE` token.
- Otherwise:
  $\rightarrow$ Emit `CHAR_VEC` token, reading until the matching unescaped `'` (handling escaped `''`).

#### 3.3.2 Control-Flow Block Matching
The auditor tracks control-flow keywords on an explicit lexical stack:
- **Block Openers:** `function`, `for`, `parfor`, `while`, `if`, `switch`, `try`, `classdef`.
- **Block Intermediate Clauses:** `elseif`, `else`, `case`, `otherwise`, `catch`.
- **Block Closer:** `end`.

**Validation Rules:**
1. Every opened block must push `(keyword, line_number, col_number)` to the control stack.
2. Every `end` pops from the control stack. If the stack is empty, emit `Diagnostic(Severity.ERROR, "Dangling 'end' without matching opener")`.
3. At End-of-File, if the stack is non-empty, emit `Diagnostic(Severity.ERROR, f"Unclosed block '{top.keyword}' opened at line {top.line}")`.
4. **Function Closure Rule**: In modern MATLAB scripts containing local functions, every `function` must have an explicit matching `end`. The auditor strictly enforces this to avoid ambiguous scope boundaries.

#### 3.3.3 Delimiter & Bracket Matching
Parentheses `()`, square brackets `[]`, and curly braces `{}` are tracked on a delimiter stack:
- Open tokens push `(char, line, col)`.
- Close tokens verify that the top of the stack is the exact matching opener:
  - `)` matches `(`
  - `]` matches `[`
  - `}` matches `{`
- Any mismatch or EOF residue triggers a syntax error diagnostic with line and column precision.

#### 3.3.4 Static Semantic & Beginner Pitfall Detection

| Check ID | Target Pattern / Pitfall | Pedagogical Rationale & Remediation |
| :--- | :--- | :--- |
| **SEM-01** | **0-Based Indexing Detection**<br>`\b[A-Za-z_][A-Za-z0-9_]*\s*\(\s*0\s*[,)]` | Coming from Python/NumPy, students frequently attempt `v(0)` or `A(0, :)`. In MATLAB, indexing is strictly 1-based; index 0 throws a runtime `Index exceeds matrix dimensions` error. |
| **SEM-02** | **Negative Indexing Detection**<br>`\b[A-Za-z_][A-Za-z0-9_]*\s*\(\s*-\s*\d+\s*\)` | In Python, `arr[-1]` accesses the last element. In MATLAB, negative indices are invalid; `v(end)` must be used. |
| **SEM-03** | **Element-Wise vs Matrix Confusion**<br>Using `^2` on vectors instead of `.^2`<br>Using `*` between same-dimension column vectors | Matrix power `A^2` requires square matrices. For vectors or arrays, element-wise `.^2` is required. The auditor checks vector transformation exercises for missing dots (`.*`, `./`, `.^`). |
| **SEM-04** | **Inefficient Matrix Inversion**<br>`inv\s*\(\s*[A-Za-z0-9_]+\s*\)\s*\*` | Flag `inv(A) * b` in linear systems exercises and suggest the numerically stable backslash operator `A \ b`. |
| **SEM-05** | **Unsuppressed Loop Output**<br>Assignment inside `for`/`while` without trailing `;` | Missing semicolons inside loops flood the Command Window and cause severe performance degradation. |

#### 3.3.5 Engineering Rationale & Documentation Quality Standards
Educational scripts must teach *why* code exists:
1. **Header Docstring**: Every `.m` file must begin with a structured header comment containing:
   - Module / Script Title.
   - Engineering Objective / Physical Problem.
   - Author / Level context.
2. **Comment-to-Code Ratio**:
   $$\text{Ratio} = \frac{\text{Lines of Comments}}{\text{Total Non-Empty Lines}} \ge 0.20 \quad (20\%)$$
3. **Engineering Keyword Presence**: Checks for presence of physical units or rationale indicators (`Units:`, `Formula:`, `Rationale:`, `Physical:`, `Assumption:`).

---

### 3.4 Subsystem 4: 4-Tier Progressive Exercise Structure Auditor (`ExerciseTierAuditor`)

#### 3.4.1 Pedagogical Tier Specification
Each module's `exercises.m` must strictly partition practice into four cognitive stages:

```
+-----------------------------------------------------------------------+
| TIER 1: RECALL (Reproduce Core Concepts & Basic Syntax)               |
| - Verify fundamental formulas, construct vectors/matrices, indexing   |
+-----------------------------------------------------------------------+
                                  |
+---------------------------------v-------------------------------------+
| TIER 2: UNDERSTANDING (Debug Flawed Code & Fix Engineering Errors)    |
| - Diagnose dimensional mismatches, fix 0-based indexing, correct dots |
+-----------------------------------------------------------------------+
                                  |
+---------------------------------v-------------------------------------+
| TIER 3: APPLICATION (Solve Realistic Engineering Problem)             |
| - Physical circuits, structural truss, RC transient, sensor noise     |
+-----------------------------------------------------------------------+
                                  |
+---------------------------------v-------------------------------------+
| TIER 4: CHALLENGE (Open-Ended Multi-Step Synthesis)                   |
| - Multi-variable optimization, failure threshold prediction           |
+-----------------------------------------------------------------------+
```

#### 3.4.2 Auditing Logic
For each `exercises.m` and paired `solutions/exercises_solution.m`:
1. **Section Header Verification**:
   Scan for MATLAB cell divider banners:
   - `%% Level 1: Recall` or `%% Tier 1: Recall`
   - `%% Level 2: Understanding` or `%% Tier 2: Understanding`
   - `%% Level 3: Application` or `%% Tier 3: Application`
   - `%% Level 4: Challenge` or `%% Tier 4: Challenge`
2. **Student Template Structure**:
   - Verify presence of student actionable comments: `% TODO:` or `% TASK:`.
   - Verify that starter variables are initialized to placeholder values (`[]` or `NaN` or unassigned) with instructions.
3. **Paired Solution Verification**:
   - Locate corresponding solution file (`solutions/exercises_solution.m`).
   - Confirm solution file exists and has size $\ge 500$ bytes.
   - Confirm solution file contains **zero** unresolved `% TODO` markers.
   - Verify that all variable names requested in the student template are defined and computed in the reference solution.

---

### 3.5 Subsystem 5: Dataset & Capstone Validator (`DatasetCapstoneValidator`)

#### 3.5.1 Dataset Schema & File Integrity
The validator checks all CSV datasets in `datasets/` and `capstone/data/`:
1. **Parsability**: Files must be valid UTF-8 and parsable by Python `csv.reader` without exceptions.
2. **Tabular Consistency**: Every row must have the exact same number of columns as the header row.
3. **Minimum Row Count**: Telemetry datasets must contain $\ge 100$ records to ensure realistic time-series analysis and numerical stability.
4. **Expected Telemetry Columns**:
   `timestamp`, `temperature_c`, `vibration_rms`, `motor_current_a`, `pressure_kpa`, `system_status`
5. **Numerical Integrity**: Columns designated as sensor readings must contain valid float values (no unexpected strings or corrupt tokens).

#### 3.5.2 Capstone Package Integrity
The capstone package (`capstone/`) requires complete end-to-end integration:
1. `capstone/README.md`: Must detail the industrial system context (e.g., centrifugal pump or gas turbine health monitoring), failure modes, mathematical equations, and a 100-point rubric.
2. `capstone/data/industrial_telemetry.csv`: Validated sensor dataset.
3. `capstone/generate_telemetry.py`: Deterministic Python generator using NumPy with a fixed seed (`seed=42`) ensuring reproducible datasets.
4. `capstone/starter_template.m`: Scaffolded MATLAB template guiding students through:
   - Phase 1: Data Ingestion & Missing Value Handling (`readtable`, `fillmissing`).
   - Phase 2: Sensor Signal Filtering & Noise Analysis (Calculus & Probability).
   - Phase 3: Structural / Electrical System State Estimation (Linear Algebra).
   - Phase 4: Time-to-Failure Prediction & Maintenance Decision.
5. `capstone/capstone_solution.m`: Fully executed reference script generating expected summary tables and figures.

---

## 4. 4-Tier End-to-End (E2E) Test Plan

A formal verification harness requires structured test case generation spanning the full input domain, extreme boundaries, multi-variable interactions, and authentic user journeys.

```
================================================================================
                    4-TIER END-TO-END TEST ARCHITECTURE
================================================================================

  +--------------------------------------------------------------------------+
  | TIER 1: CATEGORY-PARTITION TESTING                                       |
  | Systematic coverage of curriculum categories, modules, and file formats |
  +--------------------------------------------------------------------------+
                                      |
  +-----------------------------------v--------------------------------------+
  | TIER 2: BOUNDARY VALUE ANALYSIS (BVA)                                    |
  | Dimensional edge cases (0x0, 1x1, vectors), numerical limits (eps, Inf) |
  +--------------------------------------------------------------------------+
                                      |
  +-----------------------------------v--------------------------------------+
  | TIER 3: PAIRWISE (COMBINATORIAL) TESTING                                 |
  | 2-way combinatorial interactions (Operators x Dimensions x Modules)     |
  +--------------------------------------------------------------------------+
                                      |
  +-----------------------------------v--------------------------------------+
  | TIER 4: REAL-WORLD USER SCENARIOS                                        |
  | Full student lifecycle simulations, capstone pipelines, ML bridge flows  |
  +--------------------------------------------------------------------------+
```

---

### 4.1 Tier 1: Category-Partition Test Suite (Equivalence Classes)

The input domain of the teaching package is partitioned into orthogonal categories, choices, and constraints:

#### Category-Partition Matrix
| Category | Partition / Choice | Expected Properties | Test Verification ID |
| :--- | :--- | :--- | :--- |
| **C1: Module Domains** | P1.1: Foundations (`matlab/`) | Python-to-MATLAB syntax, 1-based indexing, plotting | `TEST-CP-MOD-01` |
| | P1.2: Linear Algebra (`linear_algebra/`) | Vectors, matrix ops, `A\b`, eigenvalues, truss circuit | `TEST-CP-MOD-02` |
| | P1.3: Calculus (`calculus/`) | Kinematics, `trapz`, loss minimization, `ode45` | `TEST-CP-MOD-03` |
| | P1.4: Probability (`probability/`) | Distributions, Monte Carlo, sensor noise, reliability | `TEST-CP-MOD-04` |
| | P1.5: Dynamic Sim (`simulink/`) | Block diagrams, solver setups, companion scripts | `TEST-CP-MOD-05` |
| | P1.6: Integrative (`capstone/`, `ml_bridge/`) | Multi-disciplinary telemetry, ML roadmap & code | `TEST-CP-MOD-06` |
| **C2: Artifact Types** | P2.1: Pedagogical Readmes (`.md`) | Follows 9-part pedagogical template, $>1500$ bytes | `TEST-CP-ART-01` |
| | P2.2: Demo Scripts (`.m`) | Valid MATLAB syntax, $\ge 20\%$ comments, runnable | `TEST-CP-ART-02` |
| | P2.3: User Functions (`.m`) | Explicit `function` and `end`, header docstrings | `TEST-CP-ART-03` |
| | P2.4: Exercise Files (`.m`) | Contains all 4 tiers, TODO markers present | `TEST-CP-ART-04` |
| | P2.5: Solution Files (`.m`) | Paired with exercises, zero TODOs, syntax valid | `TEST-CP-ART-05` |
| | P2.6: Telemetry Data (`.csv`) | Non-empty, consistent columns, valid numeric types | `TEST-CP-ART-06` |
| | P2.7: Cheat Sheets (`.md`) | Centralized in `reference/`, valid markdown syntax | `TEST-CP-ART-07` |
| **C3: Teaching README Sections** | P3.1: Learning Objectives | Clear, measurable engineering outcomes | `TEST-CP-PED-01` |
| | P3.2: Why Engineers Need This | Real engineering motivation (bridge, circuit, flight) | `TEST-CP-PED-02` |
| | P3.3: Intuition | Physical/visual mental model before formulas | `TEST-CP-PED-03` |
| | P3.4: Mathematics | Rigorous equations with LaTeX formatting | `TEST-CP-PED-04` |
| | P3.5: Worked Examples | Step-by-step problem with analytical solution | `TEST-CP-PED-05` |
| | P3.6: MATLAB Implementation | Code implementing worked example | `TEST-CP-PED-06` |
| | P3.7: Common Mistakes | Traps, indexing errors, dimensional mismatches | `TEST-CP-PED-07` |
| | P3.8: Engineering Interpretation | Physical meaning of numerical output | `TEST-CP-PED-08` |
| | P3.9: Exercises Reference | Links to `exercises.m` and solutions | `TEST-CP-PED-09` |

---

### 4.2 Tier 2: Boundary Value Analysis (BVA)

Boundary testing verifies system resilience at numerical, dimensional, and syntactic limits:

| Test ID | Boundary Dimension | Boundary Values Tested | Expected Behavior / Verification |
| :--- | :--- | :--- | :--- |
| **BVA-DIM-01** | Matrix Dimensions | $0 \times 0$ (empty `[]`), $1 \times 1$ (scalar), $1 \times N$ (row), $N \times 1$ (col), $N \times N$ | Auditor verifies that row/column vector distinction is respected in matrix math; detects accidental dimension mismatches. |
| **BVA-DIM-02** | Inner vs Outer Product | Row $(1 \times N) \times$ Col $(N \times 1) \rightarrow 1 \times 1$<br>Col $(N \times 1) \times$ Row $(1 \times N) \rightarrow N \times N$ | Verifies scripts correctly distinguish scalar dot product (`u' * v` or `dot(u, v)`) from outer covariance matrix (`v * u'`). |
| **BVA-IDX-01** | Subscript Index Lower Bound | $k = 0$ (invalid), $k = 1$ (first valid) | `SEM-01` rule flags any occurrence of literal index `(0)`. |
| **BVA-IDX-02** | Subscript Index Upper Bound | $k = \text{length}(x)$, $k = \text{end}$, $k = \text{length}(x) + 1$ | Verifies exercises test boundary slicing up to `end`. |
| **BVA-NUM-01** | Machine Epsilon & Tolerances | Difference $|a - b| < 10^{-6}$ vs exact equality `a == b` | Floating-point comparison exercises must avoid direct equality `==` on calculated floats and teach `abs(a - b) < tol`. |
| **BVA-NUM-02** | Matrix Condition Number | $\det(A) \approx 0$, $\kappa(A) > 10^{12}$ (near-singular) | Linear algebra module includes ill-conditioned matrix example illustrating why `A \ b` warns or produces large errors compared to well-conditioned systems. |
| **BVA-NUM-03** | Probability Bounds | $P(A) = 0.0$, $P(A) = 1.0$, $\sum p_i = 1.0 \pm 10^{-9}$ | Probability scripts verify cumulative sum boundaries and non-negative probabilities. |
| **BVA-FIL-01** | File Size Limits | $0$ bytes (corrupt), $1$ byte (stub), $\ge 1500$ bytes (full) | Structure validator rejects files $\le 0$ bytes with critical error. |
| **BVA-LNK-01** | Link Traversal Depth | Local `./`, Parent `../`, Multi-level `../../` | Link validator successfully resolves paths up to 3 directory levels deep. |

---

### 4.3 Tier 3: Pairwise (Combinatorial) Testing

Pairwise testing ensures all 2-way interactions between orthogonal curriculum parameters are covered:

#### Combinatorial Parameters:
- **Parameter 1: Data Construct** $\in \{\text{Scalar}, \text{Row Vector}, \text{Column Vector}, \text{2D Matrix}, \text{Time Series Table}\}$
- **Parameter 2: Operator Type** $\in \{\text{Linear Combination } (+, -), \text{Matrix Multiply } (*), \text{Element-wise } (.*, ./), \text{Backslash } (\setminus), \text{Calculus } (\text{diff}, \text{trapz})\}$
- **Parameter 3: Domain Application** $\in \{\text{Circuit Analysis}, \text{Structural Truss}, \text{Thermal Cooling}, \text{Sensor Filtering}, \text{Motor Dynamics}\}$

#### Generated Pairwise Test Matrix (Sample of 15 Key Interactions)
| Test ID | Data Construct | Operator Type | Domain Application | Verification Target in Curriculum |
| :--- | :--- | :--- | :--- | :--- |
| **PAIR-01** | Column Vector | Backslash ($\setminus$) | Circuit Analysis | Node voltage equations $G v = i$ in `linear_algebra/03_linear_systems_solve.m` |
| **PAIR-02** | 2D Matrix | Backslash ($\setminus$) | Structural Truss | Stiffness matrix $K u = F$ in `linear_algebra/05_truss_circuit_project.m` |
| **PAIR-03** | Row Vector | Element-wise ($.*$) | Sensor Filtering | Voltage-to-temperature calibration curve in `matlab/03_matrix_vs_elementwise.m` |
| **PAIR-04** | Time Series Table | Calculus ($\text{trapz}$) | Thermal Cooling | Energy accumulation $\int P \, dt$ in `calculus/02_numerical_integration.m` |
| **PAIR-05** | Column Vector | Calculus ($\text{diff}$) | Motor Dynamics | Angular acceleration from velocity $\alpha = \frac{d\omega}{dt}$ in `calculus/01_rates_of_change.m` |
| **PAIR-06** | 2D Matrix | Matrix Multiply ($*$) | ML Linear Projection | Feature transformation $Z = X W$ in `ml_bridge/linear_regression_bridge.m` |
| **PAIR-07** | Time Series Table | Element-wise ($./$) | Industrial Telemetry | Normalized vibration index in `capstone/capstone_solution.m` |
| **PAIR-08** | Scalar | Linear Combination | Circuit Analysis | Voltage divider calculations in `matlab/01_environment_basics.m` |
| **PAIR-09** | Column Vector | Calculus (`ode45`) | RC Circuit | Capacitor transient response in `calculus/04_differential_equations.m` |
| **PAIR-10** | Row Vector | Monte Carlo (`rand`) | Sensor Noise | Gaussian noise synthesis $\mathcal{N}(\mu, \sigma^2)$ in `probability/03_monte_carlo_simulation.m` |
| **PAIR-11** | 2D Matrix | Eigenvalues (`eig`) | Structural Vibration | Resonance modes of 2-DOF system in `linear_algebra/04_eigenvalues_eigenvectors.m` |
| **PAIR-12** | Time Series Table | Probability (`mean`, `std`)| Machine Reliability| Pump failure probability in `probability/04_sensor_reliability.m` |
| **PAIR-13** | Column Vector | Element-wise ($.^{\wedge}$) | Optimization Loss | Quadratic cost function $J(\theta)$ in `calculus/03_optimization_loss.m` |
| **PAIR-14** | 2D Matrix | Transpose ($'$) | Normal Equation | $(X^T X)^{-1} X^T y$ derivation in `ml_bridge/linear_regression_bridge.m` |
| **PAIR-15** | Row Vector | Plotting (`plot`, `grid`)| Dynamic Simulation | Motor step response plot in `simulink/companions/motor_speed_companion.m` |

---

### 4.4 Tier 4: Real-World Scenarios (Student & Curriculum Journeys)

These scenarios simulate end-to-end user journeys and authentic engineering workflows:

#### Scenario 1: Beginner Student Journey (Python Transition $\rightarrow$ MATLAB Foundations)
- **Actor:** Engineering student proficient in Python/NumPy starting Level 2.
- **Workflow Steps:**
  1. Clones repository and opens `engineering-mathematics/README.md`.
  2. Reads the Level 1 $\rightarrow$ Level 2 curriculum progression roadmap.
  3. Navigates via relative link to `matlab/README.md`.
  4. Studies the "Python vs MATLAB Rosetta Stone" comparison table (0-based vs 1-based indexing, slice boundaries, `*` vs `.*`, row vs column vector storage).
  5. Opens `matlab/exercises.m` and attempts Tier 1 (Recall) and Tier 2 (Understanding/Debugging).
  6. In Tier 2, student fixes intentional bugs: converting `v(0)` to `v(1)`, replacing `x * y` with `x .* y`.
  7. Cross-checks results with `matlab/solutions/exercises_solution.m`.
- **Automated Verification:**
  `test_e2e_student_transition_flow()` verifies all cross-links resolve, comparison tables exist, exercise bugs are well-documented, and solutions run without syntax warnings.

#### Scenario 2: Structural & Electrical Engineering Multi-Physics Pipeline (R2)
- **Actor:** Student modeling physical equilibrium in trusses and circuits.
- **Workflow Steps:**
  1. Opens `linear_algebra/05_truss_circuit_project.m`.
  2. Formulates 5-joint planar truss stiffness matrix $K \in \mathbb{R}^{10 \times 10}$ and nodal force vector $F \in \mathbb{R}^{10}$.
  3. Solves for nodal displacements $u = K \setminus F$.
  4. Verifies physical sanity: equilibrium condition $\sum F_x = 0, \sum F_y = 0$.
  5. Formulates 4-mesh electrical circuit impedance matrix $Z$ and voltage vector $V$, solving mesh currents $I = Z \setminus V$.
  6. Visualizes deformed truss geometry and current distributions using MATLAB subplots.
- **Automated Verification:**
  `test_e2e_linear_physics_pipeline()` verifies numerical solvability of $K \setminus F$, verifies backslash operator usage, and verifies comment explanations for physical units (Newtons, meters, Volts, Amperes).

#### Scenario 3: Transient Thermal Cooling & RC Circuit Simulation (R3 & R5)
- **Actor:** Student studying rates of change and dynamic simulation.
- **Workflow Steps:**
  1. Opens `calculus/04_differential_equations.m` and `simulink/companions/rc_circuit_companion.m`.
  2. Implements 1st-order cooling equation $\frac{dT}{dt} = -k(T - T_{\text{env}})$ with initial $T(0) = 90^\circ\text{C}$, $T_{\text{env}} = 22^\circ\text{C}$.
  3. Compares analytical solution $T(t) = T_{\text{env}} + (T_0 - T_{\text{env}}) e^{-kt}$ with numerical integration using Euler method and `ode45`.
  4. Computes total heat energy dissipated using numerical accumulation `trapz(t, Q_rate)`.
  5. Inspects the Simulink block-diagram visual documentation in `simulink/README.md` and verifies matching parameter definitions in the `.m` companion script.
- **Automated Verification:**
  `test_e2e_transient_calculus_pipeline()` verifies numerical convergence between analytical and numerical vectors, confirms `trapz` implementation, and audits Simulink companion script syntax.

#### Scenario 4: Industrial Pump Fleet Telemetry & Predictive Maintenance Capstone (R4 & R6)
- **Actor:** Student completing the final integrative capstone project.
- **Workflow Steps:**
  1. Reads `capstone/README.md` specifying telemetry from 4 industrial centrifugal pumps.
  2. Ingests `capstone/data/industrial_telemetry.csv` containing 500 hours of operating logs (`timestamp`, `temperature_c`, `vibration_rms`, `motor_current_a`).
  3. Implements signal conditioning: filters sensor measurement noise modeled by Gaussian distribution $\mathcal{N}(0, \sigma^2)$ using a moving-average window.
  4. Computes rate of temperature rise $\frac{dT}{dt}$ using finite difference (`diff`).
  5. Solves linear regression normal equation $(X^T X)^{-1} X^T y$ to extrapolate hours until bearing vibration exceeds critical threshold ($4.5\,\text{mm/s}$).
  6. Generates 4-panel diagnostic dashboard: raw vs filtered telemetry, temperature derivative, vibration trend extrapolation, and probability of failure within 24 hours.
- **Automated Verification:**
  `test_e2e_capstone_pipeline()` verifies CSV dataset existence, column headers, deterministic generator script execution, starter template TODO structure, and reference solution completeness.

#### Scenario 5: Machine Learning Bridge Integration (R6)
- **Actor:** Student transitioning from Engineering Mathematics to Machine Learning.
- **Workflow Steps:**
  1. Opens `ml_bridge/README.md` and `ml_bridge/math_to_ml_roadmap.md`.
  2. Traces how matrix operations map to feature matrices $X \in \mathbb{R}^{m \times n}$, weights $w \in \mathbb{R}^n$, and predictions $\hat{y} = X w$.
  3. Traces how calculus derivatives map to Mean Squared Error cost gradients $\nabla_w J(w) = \frac{1}{m} X^T (X w - y)$.
  4. Traces how normal distributions map to Gaussian Naive Bayes and Maximum Likelihood Estimation.
  5. Runs `ml_bridge/linear_regression_bridge.m` (MATLAB normal equation and batch gradient descent).
  6. Runs `ml_bridge/linear_regression_bridge.py` and confirms that the learned weights match within machine precision ($< 10^{-5}$).
- **Automated Verification:**
  `test_e2e_ml_bridge_parity()` executes the Python ML bridge script, verifies numerical parameter convergence with the MATLAB reference comments, and validates cross-links.

---

## 5. Complete Python Reference Implementation (`scripts/verify_package.py`)

Below is the complete, production-grade reference architecture for the package verification harness. This script runs under standard Python 3.10+ without external packages (using only Python standard library `pathlib`, `re`, `sys`, `dataclasses`, `enum`, `csv`, `typing`), ensuring maximum portability across all platforms and continuous-integration pipelines.

```python
#!/usr/bin/env python3
"""
================================================================================
ENGINEERING MATHEMATICS TEACHING PACKAGE — SYNTAX & STRUCTURE AUDITOR
================================================================================
Author: Teamwork Engineering Verification Architect
Target: /home/settings/Documents/pearl/engineering-mathematics
License: MIT / Educational Open License

Zero-Proprietary-Dependency Verification Suite:
- Manifest & Directory Structure Validation
- Markdown Cross-Reference & Anchor Validation (Zero 404s)
- MATLAB Non-Proprietary Lexer, Parser & Block Auditor
- 4-Tier Exercise Structure & Paired Solution Auditor
- Telemetry Dataset & Capstone Package Validator
- Formatted Terminal Diagnostic Reporting & JSON Artifact Generation
================================================================================
"""

import sys
import os
import re
import csv
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Set, Tuple, Optional, Any

# ==============================================================================
# DIAGNOSTIC DATA MODELS
# ==============================================================================

class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARN"
    ERROR = "ERROR"

@dataclass
class Diagnostic:
    validator: str
    severity: Severity
    file_path: Path
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    message: str = ""
    remediation: str = ""
    snippet: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "validator": self.validator,
            "severity": self.severity.value,
            "file_path": str(self.file_path),
            "line_number": self.line_number,
            "column_number": self.column_number,
            "message": self.message,
            "remediation": self.remediation,
            "snippet": self.snippet
        }

@dataclass
class AuditReport:
    total_checks: int = 0
    passed_checks: int = 0
    warning_count: int = 0
    error_count: int = 0
    diagnostics: List[Diagnostic] = field(default_factory=list)

    def add_diagnostic(self, diag: Diagnostic):
        self.diagnostics.append(diag)
        if diag.severity == Severity.ERROR:
            self.error_count += 1
        elif diag.severity == Severity.WARNING:
            self.warning_count += 1

    @property
    def is_success(self) -> bool:
        return self.error_count == 0


# ==============================================================================
# VALIDATOR 1: DIRECTORY STRUCTURE & MANIFEST VALIDATOR
# ==============================================================================

class DirectoryStructureValidator:
    """Validates existence, hierarchy, and minimum size of all curriculum modules."""

    REQUIRED_MODULES = [
        "matlab",
        "linear_algebra",
        "calculus",
        "probability",
        "simulink",
        "capstone",
        "ml_bridge",
        "assessments",
        "reference",
        "datasets",
        "scripts"
    ]

    REQUIRED_FILES = {
        "README.md": 1000,
        "matlab/README.md": 1500,
        "matlab/exercises.m": 300,
        "matlab/solutions/exercises_solution.m": 500,
        "linear_algebra/README.md": 1500,
        "linear_algebra/exercises.m": 300,
        "linear_algebra/solutions/exercises_solution.m": 500,
        "calculus/README.md": 1500,
        "calculus/exercises.m": 300,
        "calculus/solutions/exercises_solution.m": 500,
        "probability/README.md": 1500,
        "probability/exercises.m": 300,
        "probability/solutions/exercises_solution.m": 500,
        "simulink/README.md": 1500,
        "simulink/exercises.m": 300,
        "simulink/solutions/exercises_solution.m": 500,
        "capstone/README.md": 1500,
        "capstone/starter_template.m": 500,
        "capstone/capstone_solution.m": 800,
        "capstone/data/industrial_telemetry.csv": 500,
        "ml_bridge/README.md": 1200,
        "assessments/FINAL_ASSESSMENT.md": 2500,
        "reference/matlab_cheatsheet.md": 1000,
        "reference/linear_algebra_cheatsheet.md": 1000,
        "reference/calculus_cheatsheet.md": 1000,
        "reference/probability_cheatsheet.md": 1000,
    }

    def __init__(self, root_dir: Path, report: AuditReport):
        self.root_dir = root_dir.resolve()
        self.report = report

    def validate(self):
        # 1. Check root directory
        if not self.root_dir.exists() or not self.root_dir.is_dir():
            self.report.add_diagnostic(Diagnostic(
                validator="DirectoryStructure",
                severity=Severity.ERROR,
                file_path=self.root_dir,
                message="Target package directory does not exist.",
                remediation="Ensure project directory is initialized."
            ))
            return

        # 2. Check required module subdirectories
        for mod in self.REQUIRED_MODULES:
            mod_path = self.root_dir / mod
            self.report.total_checks += 1
            if not mod_path.exists() or not mod_path.is_dir():
                self.report.add_diagnostic(Diagnostic(
                    validator="DirectoryStructure",
                    severity=Severity.ERROR,
                    file_path=mod_path,
                    message=f"Mandatory module directory '{mod}/' is missing.",
                    remediation=f"Create directory '{mod}/' with required teaching artifacts."
                ))
            else:
                self.report.passed_checks += 1

        # 3. Check required files and size thresholds
        for rel_path_str, min_size in self.REQUIRED_FILES.items():
            file_path = self.root_dir / rel_path_str
            self.report.total_checks += 1
            if not file_path.exists():
                self.report.add_diagnostic(Diagnostic(
                    validator="DirectoryStructure",
                    severity=Severity.ERROR,
                    file_path=file_path,
                    message=f"Mandatory file '{rel_path_str}' is missing.",
                    remediation=f"Create file '{rel_path_str}' following curriculum specifications."
                ))
            else:
                size = file_path.stat().st_size
                if size == 0:
                    self.report.add_diagnostic(Diagnostic(
                        validator="DirectoryStructure",
                        severity=Severity.ERROR,
                        file_path=file_path,
                        message=f"File '{rel_path_str}' is empty (0 bytes).",
                        remediation="Populate file with authentic pedagogical or code content."
                    ))
                elif size < min_size:
                    self.report.add_diagnostic(Diagnostic(
                        validator="DirectoryStructure",
                        severity=Severity.WARNING,
                        file_path=file_path,
                        message=f"File '{rel_path_str}' size ({size} B) is below threshold ({min_size} B).",
                        remediation="Expand file to fulfill comprehensive curriculum standards."
                    ))
                else:
                    self.report.passed_checks += 1


# ==============================================================================
# VALIDATOR 2: MARKDOWN CROSS-REFERENCE & LINK VALIDATOR
# ==============================================================================

class MarkdownLinkValidator:
    """Validates all relative links and section anchor slugs across Markdown files."""

    LINK_REGEX = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)')
    IMG_REGEX = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    HEADING_REGEX = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    def __init__(self, root_dir: Path, report: AuditReport):
        self.root_dir = root_dir.resolve()
        self.report = report
        self.heading_slug_cache: Dict[Path, Set[str]] = {}

    @staticmethod
    def slugify(heading_text: str) -> str:
        # CommonMark / GitHub slug format
        clean = re.sub(r'[^\w\s-]', '', heading_text.strip().lower())
        return re.sub(r'[-\s]+', '-', clean).strip('-')

    def get_heading_slugs(self, file_path: Path) -> Set[str]:
        if file_path in self.heading_slug_cache:
            return self.heading_slug_cache[file_path]
        slugs = set()
        if file_path.exists() and file_path.is_file():
            try:
                content = file_path.read_text(encoding='utf-8')
                for match in self.HEADING_REGEX.finditer(content):
                    heading_text = match.group(2)
                    slugs.add(self.slugify(heading_text))
            except Exception:
                pass
        self.heading_slug_cache[file_path] = slugs
        return slugs

    def validate(self):
        md_files = list(self.root_dir.rglob("*.md"))
        for md_file in md_files:
            try:
                lines = md_file.read_text(encoding='utf-8').splitlines()
            except Exception as e:
                self.report.add_diagnostic(Diagnostic(
                    validator="MarkdownLinks",
                    severity=Severity.ERROR,
                    file_path=md_file,
                    message=f"Failed to read Markdown file: {e}",
                    remediation="Ensure file is valid UTF-8 text."
                ))
                continue

            for line_idx, line in enumerate(lines, start=1):
                # Search for all links in line
                for match in self.LINK_REGEX.finditer(line):
                    self.report.total_checks += 1
                    link_text = match.group(1)
                    raw_target = match.group(2).strip()

                    # Ignore external links and mailto
                    if raw_target.startswith(("http://", "https://", "mailto:", "ftp://")):
                        self.report.passed_checks += 1
                        continue

                    # Split path and anchor
                    if "#" in raw_target:
                        target_file_str, anchor = raw_target.split("#", 1)
                    else:
                        target_file_str, anchor = raw_target, None

                    # Resolve target file path
                    if target_file_str:
                        target_path = (md_file.parent / target_file_str).resolve()
                    else:
                        target_path = md_file

                    # Check file existence
                    if not target_path.exists():
                        self.report.add_diagnostic(Diagnostic(
                            validator="MarkdownLinks",
                            severity=Severity.ERROR,
                            file_path=md_file,
                            line_number=line_idx,
                            message=f"Broken relative link '{raw_target}': target does not exist.",
                            remediation=f"Correct relative path pointing to '{target_path}'.",
                            snippet=line.strip()
                        ))
                        continue

                    # Check anchor existence if specified
                    if anchor:
                        slugs = self.get_heading_slugs(target_path)
                        clean_anchor = anchor.lower()
                        if clean_anchor not in slugs:
                            self.report.add_diagnostic(Diagnostic(
                                validator="MarkdownLinks",
                                severity=Severity.ERROR,
                                file_path=md_file,
                                line_number=line_idx,
                                message=f"Broken section anchor '#{anchor}' in '{target_path.name}'.",
                                remediation=f"Update link to match target heading slug.",
                                snippet=line.strip()
                            ))
                            continue

                    self.report.passed_checks += 1


# ==============================================================================
# VALIDATOR 3: NON-PROPRIETARY MATLAB SYNTAX & QUALITY AUDITOR
# ==============================================================================

class MatlabSyntaxAuditor:
    """Zero-dependency lexical analyzer and syntax auditor for MATLAB (.m) files."""

    MATLAB_KEYWORDS = {
        'function', 'end', 'for', 'parfor', 'while', 'if', 'elseif', 'else',
        'switch', 'case', 'otherwise', 'try', 'catch', 'return', 'break',
        'continue', 'global', 'persistent', 'classdef', 'properties', 'methods'
    }

    BLOCK_OPENERS = {'function', 'for', 'parfor', 'while', 'if', 'switch', 'try', 'classdef'}
    DELIMITER_PAIRS = {'(': ')', '[': ']', '{': '}'}
    DELIMITER_CLOSERS = {')': '(', ']': '[', '}': '{'}

    def __init__(self, root_dir: Path, report: AuditReport):
        self.root_dir = root_dir.resolve()
        self.report = report

    def tokenize(self, code: str, file_path: Path) -> List[Tuple[str, str, int, int]]:
        pos = 0
        n = len(code)
        tokens = []
        line = 1
        col = 1
        prev_token_type = None

        while pos < n:
            c = code[pos]

            # Newline
            if c == '\n':
                tokens.append(('NEWLINE', '\n', line, col))
                line += 1
                col = 1
                pos += 1
                continue

            # Whitespace
            if c in ' \t\r':
                col += 1
                pos += 1
                continue

            # Block comment %{ ... %}
            if c == '%' and pos + 1 < n and code[pos+1] == '{':
                start_line, start_col = line, col
                pos += 2
                col += 2
                comment = '%{'
                while pos < n:
                    if code[pos] == '%' and pos + 1 < n and code[pos+1] == '}':
                        comment += '%}'
                        pos += 2
                        col += 2
                        break
                    if code[pos] == '\n':
                        line += 1
                        col = 1
                    else:
                        col += 1
                    comment += code[pos]
                    pos += 1
                tokens.append(('BLOCK_COMMENT', comment, start_line, start_col))
                continue

            # Single-line comment % ...
            if c == '%':
                start_col = col
                comment = ''
                while pos < n and code[pos] != '\n':
                    comment += code[pos]
                    pos += 1
                    col += 1
                tokens.append(('COMMENT', comment, line, start_col))
                continue

            # Line continuation ...
            if code[pos:pos+3] == '...':
                tokens.append(('ELLIPSIS', '...', line, col))
                pos += 3
                col += 3
                while pos < n and code[pos] != '\n':
                    pos += 1
                    col += 1
                continue

            # Double-quoted string "..."
            if c == '"':
                start_col = col
                s = '"'
                pos += 1
                col += 1
                while pos < n and code[pos] != '"':
                    if code[pos] == '\n':
                        break
                    s += code[pos]
                    pos += 1
                    col += 1
                if pos < n and code[pos] == '"':
                    s += '"'
                    pos += 1
                    col += 1
                tokens.append(('STRING', s, line, start_col))
                prev_token_type = 'STRING'
                continue

            # Single quote: Transpose vs Char vector
            if c == "'":
                if prev_token_type in ('IDENT', 'CLOSE_PAREN', 'CLOSE_BRACKET', 'CLOSE_BRACE', 'TRANSPOSE', 'CHAR_VEC'):
                    tokens.append(('TRANSPOSE', "'", line, col))
                    prev_token_type = 'TRANSPOSE'
                    pos += 1
                    col += 1
                    continue
                else:
                    start_col = col
                    s = "'"
                    pos += 1
                    col += 1
                    while pos < n:
                        if code[pos] == "'":
                            if pos + 1 < n and code[pos+1] == "'":
                                s += "''"
                                pos += 2
                                col += 2
                            else:
                                s += "'"
                                pos += 1
                                col += 1
                                break
                        elif code[pos] == '\n':
                            break
                        else:
                            s += code[pos]
                            pos += 1
                            col += 1
                    tokens.append(('CHAR_VEC', s, line, start_col))
                    prev_token_type = 'CHAR_VEC'
                    continue

            # Multi-character operators
            two_char = code[pos:pos+2]
            if two_char in ('.*', './', '.^', '.\\', '==', '~=', '<=', '>=', '&&', '||'):
                tokens.append(('OPERATOR', two_char, line, col))
                prev_token_type = 'OPERATOR'
                pos += 2
                col += 2
                continue

            # Delimiters
            if c in '()[]{}':
                tag_map = {
                    '(': 'OPEN_PAREN', ')': 'CLOSE_PAREN',
                    '[': 'OPEN_BRACKET', ']': 'CLOSE_BRACKET',
                    '{': 'OPEN_BRACE', '}': 'CLOSE_BRACE'
                }
                tag = tag_map[c]
                tokens.append((tag, c, line, col))
                prev_token_type = tag
                pos += 1
                col += 1
                continue

            # Identifiers and keywords
            if c.isalpha() or c == '_':
                start_col = col
                ident = ''
                while pos < n and (code[pos].isalnum() or code[pos] == '_'):
                    ident += code[pos]
                    pos += 1
                    col += 1
                if ident in self.MATLAB_KEYWORDS:
                    tokens.append(('KEYWORD', ident, line, start_col))
                    prev_token_type = 'KEYWORD'
                else:
                    tokens.append(('IDENT', ident, line, start_col))
                    prev_token_type = 'IDENT'
                continue

            # Numbers
            if c.isdigit() or (c == '.' and pos + 1 < n and code[pos+1].isdigit()):
                start_col = col
                num = ''
                while pos < n and (code[pos].isalnum() or code[pos] in '.eE+-'):
                    num += code[pos]
                    pos += 1
                    col += 1
                tokens.append(('NUMBER', num, line, start_col))
                prev_token_type = 'NUMBER'
                continue

            # Fallback punctuation
            tokens.append(('PUNCT', c, line, col))
            prev_token_type = 'PUNCT'
            pos += 1
            col += 1

        return tokens

    def audit_file(self, m_file: Path):
        try:
            content = m_file.read_text(encoding='utf-8')
        except Exception as e:
            self.report.add_diagnostic(Diagnostic(
                validator="MatlabSyntax",
                severity=Severity.ERROR,
                file_path=m_file,
                message=f"Could not read .m file: {e}",
                remediation="Ensure file is valid UTF-8."
            ))
            return

        tokens = self.tokenize(content, m_file)
        lines = content.splitlines()

        # 1. Block Matching (function, if, for, while, switch, try -> end)
        block_stack = []
        for t_type, t_val, t_line, t_col in tokens:
            if t_type == 'KEYWORD':
                if t_val in self.BLOCK_OPENERS:
                    block_stack.append((t_val, t_line, t_col))
                elif t_val == 'end':
                    if not block_stack:
                        self.report.add_diagnostic(Diagnostic(
                            validator="MatlabSyntax",
                            severity=Severity.ERROR,
                            file_path=m_file,
                            line_number=t_line,
                            column_number=t_col,
                            message="Dangling 'end' without matching block opener.",
                            remediation="Remove extraneous 'end' or add corresponding opener.",
                            snippet=lines[t_line - 1] if t_line <= len(lines) else None
                        ))
                    else:
                        block_stack.pop()

        if block_stack:
            unclosed_op, u_line, u_col = block_stack[-1]
            self.report.add_diagnostic(Diagnostic(
                validator="MatlabSyntax",
                severity=Severity.ERROR,
                file_path=m_file,
                line_number=u_line,
                column_number=u_col,
                message=f"Unclosed '{unclosed_op}' block (missing matching 'end' before EOF).",
                remediation=f"Add 'end' statement to close block opened at line {u_line}.",
                snippet=lines[u_line - 1] if u_line <= len(lines) else None
            ))

        # 2. Delimiter Balancing (), [], {}
        delim_stack = []
        for t_type, t_val, t_line, t_col in tokens:
            if t_type in ('OPEN_PAREN', 'OPEN_BRACKET', 'OPEN_BRACE'):
                delim_stack.append((t_val, t_line, t_col))
            elif t_type in ('CLOSE_PAREN', 'CLOSE_BRACKET', 'CLOSE_BRACE'):
                expected_opener = self.DELIMITER_CLOSERS.get(t_val)
                if not delim_stack:
                    self.report.add_diagnostic(Diagnostic(
                        validator="MatlabSyntax",
                        severity=Severity.ERROR,
                        file_path=m_file,
                        line_number=t_line,
                        column_number=t_col,
                        message=f"Unmatched closing delimiter '{t_val}'.",
                        remediation="Check for mismatched parentheses, brackets, or braces.",
                        snippet=lines[t_line - 1] if t_line <= len(lines) else None
                    ))
                else:
                    actual_opener, o_line, o_col = delim_stack.pop()
                    if actual_opener != expected_opener:
                        self.report.add_diagnostic(Diagnostic(
                            validator="MatlabSyntax",
                            severity=Severity.ERROR,
                            file_path=m_file,
                            line_number=t_line,
                            column_number=t_col,
                            message=f"Mismatched delimiter: expected '{self.DELIMITER_PAIRS[actual_opener]}' to match '{actual_opener}' from line {o_line}, got '{t_val}'.",
                            remediation="Correct delimiter pair.",
                            snippet=lines[t_line - 1] if t_line <= len(lines) else None
                        ))

        if delim_stack:
            unclosed_del, d_line, d_col = delim_stack[-1]
            self.report.add_diagnostic(Diagnostic(
                validator="MatlabSyntax",
                severity=Severity.ERROR,
                file_path=m_file,
                line_number=d_line,
                column_number=d_col,
                message=f"Unclosed delimiter '{unclosed_del}' opened at line {d_line}.",
                remediation=f"Add matching '{self.DELIMITER_PAIRS[unclosed_del]}'.",
                snippet=lines[d_line - 1] if d_line <= len(lines) else None
            ))

        # 3. Static Semantic Checks: 0-Based Indexing Detection
        zero_idx_pattern = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\s*\(\s*0\s*[,)]')
        for idx, line_str in enumerate(lines, start=1):
            if zero_idx_pattern.search(line_str) and not line_str.strip().startswith('%'):
                self.report.add_diagnostic(Diagnostic(
                    validator="MatlabSyntax",
                    severity=Severity.ERROR,
                    file_path=m_file,
                    line_number=idx,
                    message="Detected 0-based indexing attempt (e.g. 'var(0)'). MATLAB is strictly 1-based.",
                    remediation="Change index 0 to 1 or appropriate 1-based expression.",
                    snippet=line_str.strip()
                ))

        # 4. Engineering Rationale / Comment Coverage
        comment_lines = sum(1 for line in lines if line.strip().startswith('%'))
        non_empty_lines = sum(1 for line in lines if line.strip())
        if non_empty_lines > 10:
            comment_ratio = comment_lines / non_empty_lines
            if comment_ratio < 0.15:
                self.report.add_diagnostic(Diagnostic(
                    validator="MatlabSyntax",
                    severity=Severity.WARNING,
                    file_path=m_file,
                    message=f"Low comment-to-code ratio ({comment_ratio:.1%}). Expected >= 20%.",
                    remediation="Add comments explaining engineering rationale and physical units."
                ))

        self.report.total_checks += 1
        self.report.passed_checks += 1

    def validate(self):
        m_files = list(self.root_dir.rglob("*.m"))
        for m_file in m_files:
            self.audit_file(m_file)


# ==============================================================================
# VALIDATOR 4: 4-TIER PROGRESSIVE EXERCISE AUDITOR
# ==============================================================================

class ExerciseTierAuditor:
    """Validates 4-tier progressive structure in exercise files and solution pairing."""

    REQUIRED_TIER_PATTERNS = [
        re.compile(r'%%\s*(Level|Tier)\s*1\s*:\s*Recall', re.IGNORECASE),
        re.compile(r'%%\s*(Level|Tier)\s*2\s*:\s*Understanding', re.IGNORECASE),
        re.compile(r'%%\s*(Level|Tier)\s*3\s*:\s*Application', re.IGNORECASE),
        re.compile(r'%%\s*(Level|Tier)\s*4\s*:\s*Challenge', re.IGNORECASE),
    ]

    def __init__(self, root_dir: Path, report: AuditReport):
        self.root_dir = root_dir.resolve()
        self.report = report

    def validate(self):
        # Locate all exercise files
        exercise_files = list(self.root_dir.rglob("exercises.m"))
        for ex_file in exercise_files:
            self.report.total_checks += 1
            content = ex_file.read_text(encoding='utf-8')

            # 1. Check Tier 1 - 4 section headers
            for tier_idx, pattern in enumerate(self.REQUIRED_TIER_PATTERNS, start=1):
                if not pattern.search(content):
                    self.report.add_diagnostic(Diagnostic(
                        validator="ExerciseTierAuditor",
                        severity=Severity.ERROR,
                        file_path=ex_file,
                        message=f"Missing mandatory Tier {tier_idx} section header.",
                        remediation=f"Include '%% Level {tier_idx}: [Title]' in {ex_file.name}."
                    ))

            # 2. Check for TODO markers in student template
            if "TODO" not in content and "TASK" not in content:
                self.report.add_diagnostic(Diagnostic(
                    validator="ExerciseTierAuditor",
                    severity=Severity.WARNING,
                    file_path=ex_file,
                    message="No '% TODO' or '% TASK' markers found in student exercise file.",
                    remediation="Add clear TODO prompts indicating where students should implement code."
                ))

            # 3. Check for matching solution file
            # Standard location: ../solutions/exercises_solution.m or same dir /solutions/
            sol_path_1 = ex_file.parent / "solutions" / "exercises_solution.m"
            sol_path_2 = ex_file.parent / "exercises_solution.m"
            sol_path_3 = ex_file.parent.parent / "solutions" / f"{ex_file.parent.name}_exercises_solution.m"

            solution_path = None
            for p in (sol_path_1, sol_path_2, sol_path_3):
                if p.exists():
                    solution_path = p
                    break

            if not solution_path:
                self.report.add_diagnostic(Diagnostic(
                    validator="ExerciseTierAuditor",
                    severity=Severity.ERROR,
                    file_path=ex_file,
                    message=f"Missing reference solution file for '{ex_file.relative_to(self.root_dir)}'.",
                    remediation="Create dedicated solution file in 'solutions/exercises_solution.m'."
                ))
            else:
                # Validate solution file
                sol_content = solution_path.read_text(encoding='utf-8')
                if "TODO" in sol_content:
                    self.report.add_diagnostic(Diagnostic(
                        validator="ExerciseTierAuditor",
                        severity=Severity.WARNING,
                        file_path=solution_path,
                        message="Reference solution file contains unresolved 'TODO' comments.",
                        remediation="Ensure reference solution is fully implemented without placeholders."
                    ))
                self.report.passed_checks += 1


# ==============================================================================
# VALIDATOR 5: DATASET & CAPSTONE VALIDATOR
# ==============================================================================

class DatasetCapstoneValidator:
    """Validates tabular dataset integrity and capstone project completeness."""

    def __init__(self, root_dir: Path, report: AuditReport):
        self.root_dir = root_dir.resolve()
        self.report = report

    def validate_csv(self, csv_file: Path, min_rows: int = 100):
        self.report.total_checks += 1
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    self.report.add_diagnostic(Diagnostic(
                        validator="DatasetValidator",
                        severity=Severity.ERROR,
                        file_path=csv_file,
                        message="CSV file is empty or missing header row.",
                        remediation="Add valid column headers."
                    ))
                    return

                col_count = len(header)
                row_count = 0
                for row_idx, row in enumerate(reader, start=2):
                    row_count += 1
                    if len(row) != col_count:
                        self.report.add_diagnostic(Diagnostic(
                            validator="DatasetValidator",
                            severity=Severity.ERROR,
                            file_path=csv_file,
                            line_number=row_idx,
                            message=f"Inconsistent column count: header has {col_count}, row has {len(row)}.",
                            remediation="Ensure uniform comma-separated columns across all records."
                        ))
                        return

                if row_count < min_rows:
                    self.report.add_diagnostic(Diagnostic(
                        validator="DatasetValidator",
                        severity=Severity.WARNING,
                        file_path=csv_file,
                        message=f"Dataset has only {row_count} rows (expected >= {min_rows}).",
                        remediation="Generate realistic time series with at least 100 observations."
                    ))
                else:
                    self.report.passed_checks += 1
        except Exception as e:
            self.report.add_diagnostic(Diagnostic(
                validator="DatasetValidator",
                severity=Severity.ERROR,
                file_path=csv_file,
                message=f"CSV reading exception: {e}",
                remediation="Ensure valid UTF-8 CSV formatting."
            ))

    def validate(self):
        # 1. Validate all datasets in datasets/ and capstone/data/
        csv_files = list(self.root_dir.rglob("*.csv"))
        for csv_file in csv_files:
            self.validate_csv(csv_file)

        # 2. Validate Capstone artifacts
        capstone_dir = self.root_dir / "capstone"
        if capstone_dir.exists():
            generator_script = capstone_dir / "generate_telemetry.py"
            if not generator_script.exists():
                self.report.add_diagnostic(Diagnostic(
                    validator="DatasetValidator",
                    severity=Severity.WARNING,
                    file_path=capstone_dir,
                    message="Capstone telemetry generator script 'generate_telemetry.py' missing.",
                    remediation="Add reproducible Python data generator script."
                ))


# ==============================================================================
# MASTER RUNNER & REPORT FORMATTER
# ==============================================================================

class VerificationRunner:
    """Coordinates execution of all validators, formats console output, and emits JSON."""

    def __init__(self, root_dir: Path, json_out: Optional[Path] = None, verbose: bool = False):
        self.root_dir = root_dir.resolve()
        self.json_out = json_out
        self.verbose = verbose
        self.report = AuditReport()

    def run(self) -> int:
        print("=" * 80)
        print("ENGINEERING MATHEMATICS TEACHING PACKAGE — AUDIT & VERIFICATION")
        print(f"Target Directory: {self.root_dir}")
        print("=" * 80)

        # Run pipeline
        validators = [
            ("Directory Structure", DirectoryStructureValidator(self.root_dir, self.report)),
            ("Markdown Links & Anchors", MarkdownLinkValidator(self.root_dir, self.report)),
            ("MATLAB Syntax & Quality", MatlabSyntaxAuditor(self.root_dir, self.report)),
            ("4-Tier Exercise Structure", ExerciseTierAuditor(self.root_dir, self.report)),
            ("Datasets & Capstone", DatasetCapstoneValidator(self.root_dir, self.report)),
        ]

        for name, validator in validators:
            print(f"[*] Running {name} Validator...")
            validator.validate()

        # Display Diagnostics
        print("\n" + "-" * 80)
        print("DIAGNOSTIC RESULTS SUMMARY")
        print("-" * 80)

        if not self.report.diagnostics:
            print("[PASS] All verification checks passed cleanly! Zero errors or warnings.")
        else:
            for diag in self.report.diagnostics:
                if diag.severity == Severity.ERROR:
                    prefix = "\033[91m[ERROR]\033[0m"
                elif diag.severity == Severity.WARNING:
                    prefix = "\033[93m[WARN ]\033[0m"
                else:
                    prefix = "[INFO ]"

                loc = f"{diag.file_path.relative_to(self.root_dir) if diag.file_path.is_relative_to(self.root_dir) else diag.file_path.name}"
                if diag.line_number:
                    loc += f":{diag.line_number}"
                if diag.column_number:
                    loc += f":{diag.column_number}"

                print(f"{prefix} [{diag.validator}] {loc} — {diag.message}")
                if self.verbose or diag.severity == Severity.ERROR:
                    if diag.snippet:
                        print(f"        Code: {diag.snippet}")
                    print(f"        Fix:  {diag.remediation}")

        # Summary box
        print("-" * 80)
        print(f"Checks Performed : {self.report.total_checks}")
        print(f"Checks Passed    : {self.report.passed_checks}")
        print(f"Warnings Emitted : {self.report.warning_count}")
        print(f"Errors Found     : {self.report.error_count}")
        print("=" * 80)

        # Emit JSON if requested
        if self.json_out:
            out_data = {
                "root_dir": str(self.root_dir),
                "is_success": self.report.is_success,
                "total_checks": self.report.total_checks,
                "passed_checks": self.report.passed_checks,
                "warning_count": self.report.warning_count,
                "error_count": self.report.error_count,
                "diagnostics": [d.to_dict() for d in self.report.diagnostics]
            }
            try:
                self.json_out.parent.mkdir(parents=True, exist_ok=True)
                self.json_out.write_text(json.dumps(out_data, indent=2), encoding='utf-8')
                print(f"Wrote audit report to {self.json_out}")
            except Exception as e:
                print(f"Failed to write JSON output: {e}", file=sys.stderr)

        if self.report.is_success:
            print("\033[92m>>> VERIFICATION STATUS: SUCCESS (Package is 100% compliant)\033[0m\n")
            return 0
        else:
            print("\033[91m>>> VERIFICATION STATUS: FAILED (Resolve errors listed above)\033[0m\n")
            return 1


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Audit and verify engineering-mathematics teaching package.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="Root directory of the engineering-mathematics package")
    parser.add_argument("--json", type=Path, default=None,
                        help="Path to output JSON diagnostic report")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose diagnostic snippets and remediation advice")
    args = parser.parse_args()

    runner = VerificationRunner(root_dir=args.root, json_out=args.json, verbose=args.verbose)
    sys.exit(runner.run())

if __name__ == "__main__":
    main()
```

---

## 6. Pytest Suite Integration & CI Automation

In addition to running standalone as `python scripts/verify_package.py`, the test infrastructure seamlessly plugs into standard `pytest` workflows. This enables automated continuous integration, selective test execution, and assertion reporting.

### 6.1 Pytest Test Suite Layout (`tests/`)
```
tests/
├── conftest.py                       # Global fixtures: package root path, shared runner
├── test_package_structure.py         # Manifest, file sizes, naming rules
├── test_markdown_links.py            # Relative paths, anchor slugs, zero 404s
├── test_matlab_syntax.py             # Lexer, block matching, bracket matching, 0-indexing
├── test_exercise_tiers.py            # 4-tier verification, paired solution check
├── test_datasets_and_capstone.py     # CSV tabular validity, telemetry generator
└── test_e2e_scenarios.py             # 5 End-to-end curriculum integration scenarios
```

### 6.2 Pytest Integration Sample (`tests/test_package_structure.py`)
```python
import pytest
from pathlib import Path
from scripts.verify_package import (
    DirectoryStructureValidator,
    AuditReport,
    Severity
)

@pytest.fixture
def package_root():
    return Path(__file__).resolve().parent.parent

def test_manifest_and_directory_structure(package_root):
    report = AuditReport()
    validator = DirectoryStructureValidator(package_root, report)
    validator.validate()
    
    errors = [d for d in report.diagnostics if d.severity == Severity.ERROR]
    assert len(errors) == 0, f"Directory structure failed with {len(errors)} errors:\n" + \
        "\n".join(f"- {d.file_path.name}: {d.message}" for d in errors)

def test_module_readmes_exist_and_non_empty(package_root):
    modules = ["matlab", "linear_algebra", "calculus", "probability", "simulink", "capstone", "ml_bridge"]
    for mod in modules:
        readme = package_root / mod / "README.md"
        assert readme.exists(), f"README.md missing for module '{mod}'"
        assert readme.stat().st_size >= 1500, f"README.md for '{mod}' too short ({readme.stat().st_size} bytes)"
```

---

## 7. Forensic Audit & Verification Gate Checklist

Prior to approving any implementation milestone or declaring the teaching package production-ready, the test harness enforces the following forensic gate check:

```
+-------------------------------------------------------------------------------+
|                      FINAL VERIFICATION GATE CHECKLIST                        |
+-------------------------------------------------------------------------------+
| [ ] 1. DIRECTORY INTEGRITY                                                   |
|        - All 10 module directories present with zero missing targets          |
|        - All files > 0 bytes; READMEs satisfy minimum depth (>1500 B)         |
+-------------------------------------------------------------------------------+
| [ ] 2. LINK & ANCHOR INTEGRITY                                               |
|        - 100% of relative links resolve to existing local files               |
|        - 100% of section anchors match target heading slugs                   |
|        - Zero broken navigation links across the curriculum graph             |
+-------------------------------------------------------------------------------+
| [ ] 3. MATLAB SYNTAX & QUALITY INTEGRITY                                      |
|        - All control blocks (function, if, for, while, switch, try) balanced  |
|        - All delimiters ((), [], {}) balanced without cross-nesting errors    |
|        - Zero instances of 0-based indexing (v(0)) or negative indexing      |
|        - All .m files satisfy >= 20% comment ratio with engineering rationale |
+-------------------------------------------------------------------------------+
| [ ] 4. EXERCISE & SOLUTION SYMMETRY                                          |
|        - Every module exercises.m contains all 4 tiers (Recall -> Challenge)  |
|        - Every exercises.m has a paired solutions/exercises_solution.m        |
|        - Reference solutions have 0 unresolved TODO markers                   |
+-------------------------------------------------------------------------------+
| [ ] 5. DATASET & CAPSTONE COMPLETENESS                                        |
|        - CSV telemetry has consistent column counts and >= 100 data rows      |
|        - Deterministic Python telemetry generator runs cleanly                |
|        - Capstone starter template and full solution both verified            |
+-------------------------------------------------------------------------------+
| [ ] 6. 4-TIER E2E TEST PASS RATE                                              |
|        - Category-Partition tests: 100% passing                               |
|        - Boundary Value Analysis tests: 100% passing                          |
|        - Pairwise Combinatorial tests: 100% passing                           |
|        - Real-World User Scenarios 1-5: 100% passing                          |
+-------------------------------------------------------------------------------+
```

---
*End of Test & Verification Infrastructure Architecture Report.*
