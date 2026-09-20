"""Pure-Matplotlib visualization suite for NEAT.

Provides publication-quality visualizers for:
- Evolutionary fitness curves (best and mean fitness over generations).
- Speciation dynamics stackplots (population partition per niche over time).
- Layered neural network topology diagrams (zero graphviz binary requirement).
"""

from collections import defaultdict
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib
matplotlib.use('Agg')  # Headless backend
import matplotlib.pyplot as plt
import numpy as np

from neat.neat_engine.genome import Genome


def plot_fitness(
    history: Dict[str, List[float]],
    save_path: str,
    title: str = "NEAT Fitness Convergence",
    threshold: Optional[float] = None,
) -> None:
    """Plot best and mean fitness curves across evolutionary generations."""
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

    best_fitness = history.get('best_fitness', [])
    mean_fitness = history.get('mean_fitness', [])
    generations = list(range(len(best_fitness)))

    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)

    if best_fitness:
        ax.plot(generations, best_fitness, color='#27ae60', linewidth=2.2, label='Champion Fitness')
    if mean_fitness:
        ax.plot(generations, mean_fitness, color='#2980b9', linewidth=1.8, linestyle='--', label='Population Mean')

    if threshold is not None:
        ax.axhline(
            y=threshold,
            color='#c0392b',
            linestyle=':',
            linewidth=1.8,
            label=f'Target Threshold ({threshold})',
        )

    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Generation', fontsize=11)
    ax.set_ylabel('Fitness', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


def plot_species(
    species_history: Union[Dict[int, List[int]], List[Dict[int, int]]],
    save_path: str,
    title: str = "Speciation Dynamics Over Generations",
) -> None:
    """Generate a stacked area chart showing species population distributions over time."""
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

    # Normalize species history into Dict[int, List[int]]
    history_dict: Dict[int, List[int]] = {}
    if isinstance(species_history, list):
        # List of generation dicts
        num_gens = len(species_history)
        all_species = sorted({sp_id for gen_dict in species_history for sp_id in gen_dict})
        for sp_id in all_species:
            history_dict[sp_id] = [gen_dict.get(sp_id, 0) for gen_dict in species_history]
    elif isinstance(species_history, dict):
        history_dict = dict(species_history)
        if history_dict:
            max_len = max(len(counts) for counts in history_dict.values())
            for sp_id, counts in history_dict.items():
                if len(counts) < max_len:
                    history_dict[sp_id] = counts + [0] * (max_len - len(counts))

    if not history_dict:
        # Create empty plot
        fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
        ax.set_title(title)
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        plt.close(fig)
        return

    species_ids = sorted(history_dict.keys())
    num_gens = len(next(iter(history_dict.values())))
    generations = list(range(num_gens))
    data = [history_dict[sp_id] for sp_id in species_ids]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)

    colormap = plt.get_cmap('tab20')
    colors = [colormap(i % 20) for i in range(len(species_ids))]

    ax.stackplot(
        generations,
        *data,
        labels=[f'Species {sp_id}' for sp_id in species_ids],
        colors=colors,
        alpha=0.85,
    )

    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Generation', fontsize=11)
    ax.set_ylabel('Total Genomes per Species', fontsize=11)
    ax.set_xlim(0, max(1, num_gens - 1))
    ax.grid(True, linestyle='--', alpha=0.4)

    # Place legend outside if many species
    if len(species_ids) <= 12:
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.0), fontsize=8, ncol=1)
    else:
        ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.0), fontsize=7, ncol=2)

    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close(fig)


def _compute_node_depths(genome: Genome) -> Dict[int, int]:
    """Compute topological layer depth for each node in a genome."""
    depths: Dict[int, int] = {}
    for nid, node in genome.nodes.items():
        if node.node_type in ('input', 'bias'):
            depths[nid] = 0

    # Successive depth propagation
    enabled_edges = [(c.in_node, c.out_node) for c in genome.connections.values() if c.enabled]
    changed = True
    iterations = 0
    max_iter = len(genome.nodes) + 5

    while changed and iterations < max_iter:
        changed = False
        iterations += 1
        for u, v in enabled_edges:
            if u in depths:
                target_depth = depths[u] + 1
                if v not in depths or depths[v] < target_depth:
                    depths[v] = target_depth
                    changed = True

    # Assign default depth for disconnected nodes
    max_d = max(depths.values()) if depths else 0
    for nid, node in genome.nodes.items():
        if nid not in depths:
            if node.node_type == 'output':
                depths[nid] = max_d + 1
            else:
                depths[nid] = 1

    # Ensure output nodes are at the deepest layer
    max_hidden_depth = max(
        [d for nid, d in depths.items() if genome.nodes[nid].node_type != 'output'] + [0]
    )
    for nid, node in genome.nodes.items():
        if node.node_type == 'output':
            depths[nid] = max_hidden_depth + 1

    return depths


def plot_network(
    genome: Genome,
    save_path: str,
    title: str = "Evolved Network Topology",
) -> None:
    """Render the neural network graph using pure Matplotlib coordinates."""
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

    depths = _compute_node_depths(genome)
    max_depth = max(depths.values()) if depths else 1

    # Group nodes by layer depth
    layers: Dict[int, List[int]] = defaultdict(list)
    for nid, d in depths.items():
        layers[d].append(nid)

    # Sort nodes in each layer by ID
    for d in layers:
        layers[d].sort()

    # Assign (x, y) coordinates
    pos: Dict[int, Tuple[float, float]] = {}
    for d, node_list in sorted(layers.items()):
        x = 0.1 if d == 0 else (0.9 if d == max_depth else 0.1 + 0.8 * (d / max_depth))
        k = len(node_list)
        if k == 1:
            y_coords = [0.5]
        else:
            y_coords = np.linspace(0.15, 0.85, k)
        for nid, y in zip(node_list, y_coords):
            pos[nid] = (float(x), float(y))

    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)

    # Draw connections
    for conn in genome.connections.values():
        if conn.in_node not in pos or conn.out_node not in pos:
            continue

        x1, y1 = pos[conn.in_node]
        x2, y2 = pos[conn.out_node]

        if not conn.enabled:
            # Disabled connection: dashed light gray
            ax.plot([x1, x2], [y1, y2], color='#95a5a6', linestyle='--', linewidth=0.8, alpha=0.35, zorder=1)
        else:
            # Enabled connection: green if positive, red if negative
            color = '#27ae60' if conn.weight >= 0 else '#e74c3c'
            lw = max(0.6, min(4.0, abs(conn.weight) * 1.5))
            ax.plot([x1, x2], [y1, y2], color=color, linestyle='-', linewidth=lw, alpha=0.75, zorder=2)

    # Draw nodes
    type_colors = {
        'input': '#3498db',   # Blue
        'bias': '#f39c12',    # Gold
        'hidden': '#9b59b6',  # Purple
        'output': '#2ecc71',  # Green
    }

    for nid, node in genome.nodes.items():
        if nid not in pos:
            continue
        x, y = pos[nid]
        c = type_colors.get(node.node_type, '#34495e')
        ax.scatter(x, y, s=550, color=c, edgecolors='black', linewidths=1.5, zorder=3)

        label = f"{node.node_type[0].upper()}{nid}"
        if node.node_type in ('hidden', 'output') and abs(node.bias) > 0.01:
            label += f"\n({node.bias:+.2f})"
        ax.text(x, y, label, fontsize=8, ha='center', va='center', fontweight='bold', color='white', zorder=4)

    # Add legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor='#3498db', edgecolor='black', label='Input Node'),
        Patch(facecolor='#f39c12', edgecolor='black', label='Bias Node'),
        Patch(facecolor='#9b59b6', edgecolor='black', label='Hidden Node'),
        Patch(facecolor='#2ecc71', edgecolor='black', label='Output Node'),
        Line2D([0], [0], color='#27ae60', lw=2, label='Weight > 0'),
        Line2D([0], [0], color='#e74c3c', lw=2, label='Weight < 0'),
        Line2D([0], [0], color='#95a5a6', lw=1, linestyle='--', label='Disabled'),
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4, frameon=True)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close(fig)
