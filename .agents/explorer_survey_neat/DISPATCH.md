## 2026-09-20T12:34:43Z

You are explorer_survey_neat.
Your working directory is: /home/settings/Documents/pearl/.agents/explorer_survey_neat/
Project workspace root: /home/settings/Documents/pearl

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/ORIGINAL_REQUEST.md, specifically the latest user request under "## Follow-up — 2026-09-20T12:32:36Z" regarding R3. Redesign the NEAT Course.

Your mission is to inspect the existing neat course directory and plan its full redesign:
1. Inspect /home/settings/Documents/pearl/neat (what files/directories exist currently? check placeholders vs real code).
2. Design a complete, progressive curriculum architecture:
   - Module 1: Foundations of Evolutionary Computation (Genotypes, Phenotypes, Fitness, Selection)
   - Module 2: Genetic Algorithms (Representation, Crossover, Mutation, Elitism)
   - Module 3: Neuroevolution & Topology Evolution (Fixed vs variable topology, Innovation numbers, Historical marking)
   - Module 4: Speciation & Fitness Sharing (Compatibility distance, Protecting innovation, Niches)
   - Module 5: Crossover & Mutation Operators in NEAT (Disjoint and excess genes, Weight mutations, Add connection, Add node)
   - Module 6: Neural Network Phenotype & Feedforward/Recurrent Activation (Decoding genomes into networks, evaluation)
3. Design the two required runnable projects:
   - Project 1: XOR Evolution Project. Must be a self-contained, from-scratch or clean Python implementation that reliably evolves a network solving XOR (outputs matching truth table).
   - Project 2: Pole Balancing (Cart-Pole) Control Project. Cart-pole dynamical simulation environment with physics + NEAT controller evolving to balance the pole.
4. Design the Matplotlib visualizations:
   - Fitness over generations (mean, best fitness curves)
   - Species tracking over generations (speciation dynamics, stackplots or species size over time)
   - Network topology visualizer (graphing nodes and connection weights)
5. Ensure pedagogical format for all instructional markdown files:
   TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE.

Deliverables:
- Keep your progress.md updated with timestamps.
- Write your comprehensive survey report to /home/settings/Documents/pearl/.agents/explorer_survey_neat/handoff.md.
- Send a message to the parent orchestrator with the handoff path once complete.
