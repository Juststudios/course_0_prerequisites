## 2026-09-10T16:45:54Z

You are Worker M4 for Probability & Uncertainty in Engineering.
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_m4_1
Original user request path: /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md
Master project specification: /home/settings/Documents/pearl/.agents/PROJECT.md
Target project directory: /home/settings/Documents/pearl/engineering-mathematics

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE FILE OWNERSHIP:
- /home/settings/Documents/pearl/engineering-mathematics/probability/README.md
- /home/settings/Documents/pearl/engineering-mathematics/probability/01_probability_foundations.m
- /home/settings/Documents/pearl/engineering-mathematics/probability/02_distributions_and_moments.m
- /home/settings/Documents/pearl/engineering-mathematics/probability/03_monte_carlo_simulation.m
- /home/settings/Documents/pearl/engineering-mathematics/probability/04_sensor_noise_filtering.m
- /home/settings/Documents/pearl/engineering-mathematics/probability/mini_project_reliability.m
- /home/settings/Documents/pearl/engineering-mathematics/probability/exercises.m
- /home/settings/Documents/pearl/engineering-mathematics/solutions/probability_exercises_solution.m

TASK:
1. Thoroughly read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md and /home/settings/Documents/pearl/.agents/PROJECT.md.
2. Implement /home/settings/Documents/pearl/engineering-mathematics/probability/README.md following the mandatory 9-section teaching standard ("Explain WHY before HOW"):
   - 1. Learning Objectives (Bloom's taxonomy)
   - 2. Why Engineers Need This (Sensor noise, manufacturing tolerances, component failure, risk)
   - 3. Mathematical Intuition (Physical variability, law of large numbers, signal-to-noise ratio)
   - 4. Formal Mathematics & Governing Equations (PDF, CDF, expectation, variance, Bayes' theorem P(A|B))
   - 5. Worked Engineering Example (Diagnostic sensor false-alarm rate via Bayes' theorem)
   - 6. MATLAB Implementation (rand, randn, mean, std, var, histogram, filter)
   - 7. Common Student Pitfalls & Debugging Tips (rand [0,1] vs randn N(0,1), sample variance N-1 vs N)
   - 8. Engineering Interpretation (Confidence intervals, 3-sigma tolerance, MTBF)
   - 9. Progressive Exercises Overview (Link to exercises.m and 4 tiers)
3. Implement all concept scripts in probability/:
   - 01_probability_foundations.m: sample spaces, discrete/continuous RVs, conditional probability, Bayes' rule for sensor diagnostics.
   - 02_distributions_and_moments.m: Uniform, Binomial, Normal (Gaussian) distributions, expectation, variance, std dev, 68-95-99.7 rule.
   - 03_monte_carlo_simulation.m: Monte Carlo estimation (e.g. area estimation, component tolerance stack-up, Law of Large Numbers).
   - 04_sensor_noise_filtering.m: synthetic sensor signal + Gaussian white noise, SNR calculation, moving-average filter, before/after analysis.
   - mini_project_reliability.m: system reliability modeling (series vs parallel components, exponential failure distribution, MTBF, survival probability curve).
4. Implement exercises.m with 4 distinct tiers:
   - %% Level 1: Recall (generating normal noise, computing sample mean/variance)
   - %% Level 2: Understanding & Debugging (fixing biased estimator, correcting Bayes calculation)
   - %% Level 3: Application (sensor telemetry noise suppression and SNR optimization)
   - %% Level 4: Challenge (Monte Carlo reliability simulation of an aircraft quad-redundant hydraulic system)
   Use `% TODO` markers for student completion.
5. Implement /home/settings/Documents/pearl/engineering-mathematics/solutions/probability_exercises_solution.m with 100% complete, working solutions, 0 remaining TODOs, and thorough explanatory engineering comments.
6. Verify code quality: >= 20% comment lines, valid syntax, balanced blocks and brackets.
7. Write handoff.md in your working directory and send a completion message to the parent orchestrator.
