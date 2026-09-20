## 2026-09-10T16:38:14Z

You are Worker M3 for Calculus for Engineers (Change, Accumulation & Optimization).
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_m3_1
Original user request path: /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md
Master project specification: /home/settings/Documents/pearl/.agents/PROJECT.md
Target project directory: /home/settings/Documents/pearl/engineering-mathematics

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE FILE OWNERSHIP:
- /home/settings/Documents/pearl/engineering-mathematics/calculus/README.md
- /home/settings/Documents/pearl/engineering-mathematics/calculus/01_derivatives_and_rates.m
- /home/settings/Documents/pearl/engineering-mathematics/calculus/02_slope_and_optimization.m
- /home/settings/Documents/pearl/engineering-mathematics/calculus/03_integration_accumulation.m
- /home/settings/Documents/pearl/engineering-mathematics/calculus/04_differential_equations.m
- /home/settings/Documents/pearl/engineering-mathematics/calculus/mini_project_thermal_system.m
- /home/settings/Documents/pearl/engineering-mathematics/calculus/exercises.m
- /home/settings/Documents/pearl/engineering-mathematics/solutions/calculus_exercises_solution.m

TASK:
1. Thoroughly read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md and /home/settings/Documents/pearl/.agents/PROJECT.md.
2. Implement /home/settings/Documents/pearl/engineering-mathematics/calculus/README.md following the mandatory 9-section teaching standard ("Explain WHY before HOW"):
   - 1. Learning Objectives (Bloom's taxonomy)
   - 2. Why Engineers Need This (Dynamic physical systems, rates, energy accumulation, optimization)
   - 3. Mathematical Intuition (Derivatives as instantaneous rate of change, integrals as net accumulation)
   - 4. Formal Mathematics & Governing Equations (Kinematics, numerical differentiation, trapezoidal rule, ODE45)
   - 5. Worked Engineering Example (Vehicle velocity to acceleration and stopping distance)
   - 6. MATLAB Implementation (diff, gradient, trapz, integral, ode45)
   - 7. Common Student Pitfalls & Debugging Tips (diff reducing array length by 1, step-size errors, ode45 time vector)
   - 8. Engineering Interpretation (Physical interpretation of critical points, settling time, energy)
   - 9. Progressive Exercises Overview (Link to exercises.m and 4 tiers)
3. Implement all concept scripts in calculus/:
   - 01_derivatives_and_rates.m: kinematics s(t)->v(t)->a(t), numerical diff with forward/backward/central differences.
   - 02_slope_and_optimization.m: tangent line visualization, critical points, local minima/maxima, loss minimization.
   - 03_integration_accumulation.m: accumulation v->s, current to charge I->Q, power to energy P->E, trapz, integral.
   - 04_differential_equations.m: 1st-order ODEs (Newton cooling dT/dt = -k(T - T_env), RC circuit) using ode45.
   - mini_project_thermal_system.m: transient thermal cooling simulation with convective heat loss and parameter estimation.
4. Implement exercises.m with 4 distinct tiers:
   - %% Level 1: Recall (numerical diff, trapz accumulation)
   - %% Level 2: Understanding & Debugging (fixing diff array length mismatch, adjusting trapz spacing)
   - %% Level 3: Application (braking vehicle dynamics: stopping distance and deceleration profile)
   - %% Level 4: Challenge (designing an optimal heat sink cooling profile with ode45)
   Use `% TODO` markers for student completion.
5. Implement /home/settings/Documents/pearl/engineering-mathematics/solutions/calculus_exercises_solution.m with 100% complete, working solutions, 0 remaining TODOs, and thorough explanatory engineering comments.
6. Verify code quality: >= 20% comment lines, valid syntax, balanced blocks and brackets.
7. Write handoff.md in your working directory and send a completion message to the parent orchestrator.
