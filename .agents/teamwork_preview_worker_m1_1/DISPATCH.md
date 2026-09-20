## 2026-09-10T16:38:14Z

You are Worker M1 for MATLAB Fundamentals & Computational Environment.
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_m1_1
Original user request path: /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md
Master project specification: /home/settings/Documents/pearl/.agents/PROJECT.md
Target project directory: /home/settings/Documents/pearl/engineering-mathematics

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE FILE OWNERSHIP:
- /home/settings/Documents/pearl/engineering-mathematics/matlab/README.md
- /home/settings/Documents/pearl/engineering-mathematics/matlab/01_environment_and_variables.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/02_vectors_and_matrices.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/03_operations_and_math.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/04_scripts_and_functions.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/05_plotting_and_visualization.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/06_python_numpy_bridge.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/mini_project_signal_calc.m
- /home/settings/Documents/pearl/engineering-mathematics/matlab/exercises.m
- /home/settings/Documents/pearl/engineering-mathematics/solutions/matlab_exercises_solution.m

TASK:
1. Thoroughly read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md and /home/settings/Documents/pearl/.agents/PROJECT.md.
2. Implement /home/settings/Documents/pearl/engineering-mathematics/matlab/README.md following the mandatory 9-section teaching standard ("Explain WHY before HOW"):
   - 1. Learning Objectives (Bloom's taxonomy)
   - 2. Why Engineers Need This (MATLAB in industry, transition from Python)
   - 3. Mathematical Intuition (Vectorized array computing mental model)
   - 4. Formal Mathematics & Governing Equations (Matrix definitions, index formulas)
   - 5. Worked Engineering Example (Signal processing / calibration example)
   - 6. MATLAB Implementation (Syntax guide and best practices)
   - 7. Common Student Pitfalls & Debugging Tips (1-based indexing, `*` vs `.*`, semicolon suppression)
   - 8. Engineering Interpretation (Reading outputs, memory efficiency)
   - 9. Progressive Exercises Overview (Link to exercises.m and 4 tiers)
3. Implement all concept scripts in matlab/:
   - 01_environment_and_variables.m: workspace, memory, variables, clear/clc/close all, data types.
   - 02_vectors_and_matrices.m: row/col vectors, concatenation, 1-based indexing, slicing (`:`), linear/logical indexing.
   - 03_operations_and_math.m: matrix math (`*`, `/`, `^`) vs element-wise (`.*`, `./`, `.^`) with physical rationale.
   - 04_scripts_and_functions.m: function syntax, multiple inputs/outputs, helper functions.
   - 05_plotting_and_visualization.m: plot, subplot, xlabel, ylabel, title, grid, legend, plot3, surf.
   - 06_python_numpy_bridge.m: comprehensive Rosetta stone contrasting MATLAB vs NumPy/Matplotlib.
   - mini_project_signal_calc.m: signal generation, sensor calibration, FFT power visualization.
4. Implement exercises.m with 4 distinct tiers:
   - %% Level 1: Recall (basic syntax, indexing, element-wise math)
   - %% Level 2: Understanding & Debugging (buggy code snippets with instructions to fix)
   - %% Level 3: Application (realistic engineering sensor calibration challenge)
   - %% Level 4: Challenge (multi-sensor telemetry signal pipeline)
   Use `% TODO` markers for student completion.
5. Implement /home/settings/Documents/pearl/engineering-mathematics/solutions/matlab_exercises_solution.m with 100% complete, working solutions, 0 remaining TODOs, and thorough explanatory engineering comments.
6. Verify code quality: >= 20% comment lines, valid syntax, balanced blocks and brackets.
7. Write handoff.md in your working directory and send a completion message to the parent orchestrator.
