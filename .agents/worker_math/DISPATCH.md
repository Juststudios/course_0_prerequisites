## 2026-09-20T12:41:00Z

You are worker_math.
Your working directory is: /home/settings/Documents/pearl/.agents/worker_math/
Project workspace root: /home/settings/Documents/pearl

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/ORIGINAL_REQUEST.md (specifically Follow-up — 2026-09-20T12:32:36Z, R2 and Acceptance Criteria).
Read the Project Plan at: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_5/PROJECT.md
Read the Math Survey Handoff at: /home/settings/Documents/pearl/.agents/explorer_survey_math/handoff.md

EXCLUSIVE WRITE OWNERSHIP:
You own all files under: /home/settings/Documents/pearl/engineering-mathematics/
Do NOT write to course_0_prerequisites/, neat/, or tests/e2e/.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your mission is to implement Milestone M2 — Engineering Mathematics AI Bridges & Package Integrity:
1. Fix package structure defects so that `python3 scripts/verify_package.py` passes with 0 errors:
   - Create root `README.md` (> 2500 bytes) with course overview, curriculum map, pedagogical standard, verification instructions.
   - Create `ml_bridge/README.md` (> 2000 bytes) synthesizing Linear Algebra, Calculus, and Probability into modern AI architectures.
   - Create `reference/` cheat sheets: `matlab_cheat_sheet.md`, `linear_algebra_cheat_sheet.md`, `calculus_cheat_sheet.md`, `probability_cheat_sheet.md`.
   - Create `assessments/FINAL_ASSESSMENT.md` (> 3500 bytes) and `assessments/RUBRIC.md` (> 1200 bytes).
   - Add `capstone/capstone_analysis_complete.m` (resolving broken link in capstone/README.md:169).
2. Integrate the 3 AI/ML Bridges directly into the existing modules (do NOT create a standalone separate math course):
   - Linear Algebra -> ML: Add `linear_algebra/07_ai_ml_linear_algebra_bridge.md`, `linear_algebra/07_embeddings_attention_svd.py` (runnable NumPy), and `linear_algebra/07_embeddings_attention_svd.m`. Update `linear_algebra/README.md`.
     * Topics: High-D embeddings, cosine similarity, orthogonal projection, SVD/LoRA, Scaled Dot-Product Attention math.
   - Calculus -> ML: Add `calculus/05_ai_ml_calculus_bridge.md`, `calculus/05_optimization_gradients_backprop.py` (runnable NumPy), and `calculus/05_gradients_hessians_backprop.m`. Update `calculus/README.md`.
     * Topics: Multivariable gradients, Jacobians, Hessians/saddle points, Backpropagation tensor chain rule, Adam optimizer dynamics.
   - Probability -> ML: Add `probability/05_ai_ml_probability_bridge.md`, `probability/05_bayesian_entropy_sampling.py` (runnable NumPy), and `probability/05_bayesian_entropy_sampling.m`. Update `probability/README.md`.
     * Topics: Continuous Bayesian inference, Information Theory (Entropy, Cross-Entropy, KL Divergence), Aleatoric/Epistemic uncertainty, agent sampling (Temperature, Top-p, Monte Carlo).
3. All new Markdown lessons must strictly adhere to:
   TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE.
4. Run verification: execute `python3 scripts/verify_package.py`, `pytest tests/ -v`, and execute the runnable Python bridge scripts. Verify all pass with 0 errors.
5. Maintain your progress.md with timestamps. Write your full completion report to /home/settings/Documents/pearl/.agents/worker_math/handoff.md and message parent when complete.
