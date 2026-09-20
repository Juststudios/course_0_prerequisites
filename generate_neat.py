import os
import shutil
from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/neat")

# Clean old structure
shutil.rmtree(BASE_DIR, ignore_errors=True)
BASE_DIR.mkdir(parents=True, exist_ok=True)

dirs = [
    "01_evolutionary_computation",
    "02_genetic_algorithms",
    "03_neural_network_representation",
    "04_neat_fundamentals",
    "05_neat_python",
    "06_xor",
    "07_evolution_analysis",
    "08_control_problem",
    "09_neat_experiments",
    "exercises",
    "solutions",
    "projects",
    "capstone",
    "reference"
]

for d in dirs:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def write_file(path_str, content):
    with open(BASE_DIR / path_str, "w") as f:
        f.write(content.strip() + "\n")

write_file("README.md", """# NeuroEvolution of Augmenting Topologies (NEAT)

This course teaches how to evolve neural networks using the NEAT algorithm.

## Course Structure
1. Evolutionary Computation
2. Genetic Algorithms
3. NN Representation
4. NEAT Fundamentals
5. NEAT Python Library
6. XOR Problem
7. Evolution Analysis
8. Control Problem
9. Experiments
""")

write_file("05_neat_python/requirements.txt", """neat-python
matplotlib
graphviz
""")

write_file("06_xor/config-feedforward.txt", """[NEAT]
fitness_criterion     = max
fitness_threshold     = 3.9
pop_size              = 150
reset_on_extinction   = False

[DefaultGenome]
num_inputs              = 2
num_outputs             = 1
num_hidden              = 0
initial_connection      = full
feed_forward            = True
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5
conn_add_prob           = 0.5
conn_delete_prob        = 0.5
node_add_prob           = 0.2
node_delete_prob        = 0.2
activation_default      = sigmoid
activation_mutate_rate  = 0.0
aggregation_default     = sum
aggregation_mutate_rate = 0.0
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_max_value          = 30.0
bias_min_value          = -30.0
bias_mutate_power       = 0.5
bias_mutate_rate        = 0.7
bias_replace_rate       = 0.1
response_init_mean      = 1.0
response_init_stdev     = 0.0
response_max_value      = 30.0
response_min_value      = -30.0
response_mutate_power   = 0.0
response_mutate_rate    = 0.0
response_replace_rate   = 0.0
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 30
weight_min_value        = -30
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1
enabled_default         = True
enabled_mutate_rate     = 0.01

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 20
species_elitism      = 2

[DefaultReproduction]
elitism            = 2
survival_threshold = 0.2
""")

write_file("06_xor/train.py", """
import os
import neat

# XOR Inputs and Outputs
xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [   (0.0,),     (1.0,),     (1.0,),     (0.0,)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(xor_inputs, xor_outputs):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0]) ** 2

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 300)
    print('\\nBest genome:\\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    # Try running if neat-python is available
    try:
        run(config_path)
    except ModuleNotFoundError:
        print("neat-python not installed. Run: pip install neat-python")
""")

print("NEAT course generated.")
