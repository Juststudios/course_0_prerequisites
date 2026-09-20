## 2026-09-20T12:41:00Z
You are worker_neat.
Your working directory is: /home/settings/Documents/pearl/.agents/worker_neat/
Project workspace root: /home/settings/Documents/pearl

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/ORIGINAL_REQUEST.md (specifically Follow-up — 2026-09-20T12:32:36Z, R3 and Acceptance Criteria).
Read the Project Plan at: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_5/PROJECT.md
Read the NEAT Survey Handoff at: /home/settings/Documents/pearl/.agents/explorer_survey_neat/handoff.md

EXCLUSIVE WRITE OWNERSHIP:
You own all files under: /home/settings/Documents/pearl/neat/
Do NOT write to course_0_prerequisites/, engineering-mathematics/, or tests/e2e/.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your mission is to implement Milestone M3 — NEAT Curriculum Redesign & Projects:
1. Reorganize and clean up placeholders in neat/.
2. Implement from scratch the pure-Python zero-dependency `neat_engine/`:
   - gene.py (NodeGene, ConnectionGene dataclasses)
   - genome.py (Genome representation, weight mutation, add connection mutation, add node mutation, crossover, compatibility distance)
   - innovation.py (InnovationTracker global historical markings)
   - species.py (Species, explicit fitness sharing, reproduction)
   - population.py (Population manager, speciation, generation epoch, run loop)
   - network.py (FeedForwardNetwork DAG decoding, Kahn's topological sort, stable activation)
   - config.py (NEATConfig typed parameters)
3. Implement 6 progressive curriculum modules with README.md strictly adhering to:
   TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE
   and companion runnable Python demonstration scripts:
   - 01_evolutionary_computation/ (01_genotype_to_phenotype.py, 02_selection_schemes.py)
   - 02_genetic_algorithms/ (01_representation_and_mutation.py, 02_crossover_and_elitism.py)
   - 03_neuroevolution_topology/ (01_fixed_vs_variable_topology.py, 02_innovation_tracking.py)
   - 04_speciation_fitness_sharing/ (01_compatibility_distance.py, 02_fitness_sharing.py)
   - 05_crossover_mutation_operators/ (01_alignment_and_crossover.py, 02_topological_mutations.py)
   - 06_phenotype_network_activation/ (01_topological_sort_feedforward.py, 02_recurrent_activation.py)
4. Implement pure Matplotlib visualizers in `neat/visualizations/visualizer.py`:
   - plot_fitness(history, save_path)
   - plot_species(species_history, save_path) (stackplot of species over generations)
   - plot_network(genome, save_path) (layered network topology diagram without graphviz binary requirement)
   - demo_visualizations.py
5. Implement Project 1: XOR Evolution in `neat/projects/01_xor/`:
   - train_xor.py (evolves neural network solving XOR, achieves fitness > 3.9, outputs PNGs to output/)
   - verify_xor.py (validates XOR predictions against truth table)
6. Implement Project 2: Pole Balancing (Cart-Pole) in `neat/projects/02_cartpole/`:
   - cartpole_env.py (pure-Python dynamical simulation of cart-pole physics: Lagrangian equations, Euler-Cromer integration)
   - train_cartpole.py (evolves NEAT controller balancing pole >= 500 steps)
   - evaluate_controller.py (multi-trial evaluation and trajectory logging, outputs PNGs to output/)
7. Implement exercises/ and solutions/ with 4-tier exercises.
8. Implement tests/ (test_neat_engine.py, test_projects.py, test_visualizations.py).
9. Run verification: execute pytest on tests/, execute XOR project and Cart-Pole evaluation, verify all pass with exit code 0.
10. Maintain your progress.md with timestamps. Write your full completion report to /home/settings/Documents/pearl/.agents/worker_neat/handoff.md and message parent when complete.
