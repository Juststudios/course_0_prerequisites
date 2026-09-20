"""
Monte Carlo Tree Search (MCTS) Engine
=====================================
A domain-independent Monte Carlo Tree Search implementation using the
UCB1 (Upper Confidence Bound 1 applied to trees) algorithm.

Supports any game state adhering to the standard pearl Game AI contract:
  - state.current_player : int (1 or 2)
  - state.get_legal_moves() : list of valid actions
  - state.make_move(move) : returns a new state copy
  - state.is_terminal : bool
  - state.winner : int (1, 2, 0 for draw, or None)

THE 4 PHASES OF MCTS:
  1. Selection:
     Traverse the search tree from the root node using the UCB1 formula:
       UCB1_i = (Q_i / N_i) + c * sqrt((2 * ln(N_parent)) / N_i)
     until reaching a node that is not fully expanded or is terminal.

  2. Expansion:
     If the selected node is non-terminal, select an untried legal move
     and attach a new child node to the tree.

  3. Simulation (Rollout):
     Execute a fast, uniform-random playout from the new child node's
     state until a terminal game state is reached.

  4. Backpropagation:
     Propagate the rollout terminal result back up the tree to the root:
     incrementing visit counts N and updating win counts Q from the perspective
     of each node's active player.
"""

import math
import random
import time


class MCTSNode:
    """
    A single node in the Monte Carlo Search Tree.
    
    Attributes
    ----------
    state : object
        The game state at this node.
    parent : MCTSNode or None
        Parent node in the tree.
    move : object or None
        The action taken from parent to reach this state.
    player_just_moved : int
        The player who made `move` (1 or 2).
    children : dict of {move: MCTSNode}
        Map of action -> child node.
    untried_moves : list
        Legal actions from `state` not yet expanded into child nodes.
    visits : int
        Number of times this node has been visited (N).
    wins : float
        Cumulative reward score (Q) from rollouts.
    """

    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.player_just_moved = 3 - state.current_player if state.current_player in (1, 2) else None
        self.children = {}
        self.untried_moves = list(state.get_legal_moves()) if not state.is_terminal else []
        self.visits = 0
        self.wins = 0.0

    def is_fully_expanded(self):
        """Return True if all legal moves from this state have child nodes."""
        return len(self.untried_moves) == 0

    def is_terminal(self):
        """Return True if the node's game state is terminal."""
        return self.state.is_terminal

    def best_child(self, c_param=math.sqrt(2.0)):
        """
        Select the child node with the highest UCB1 score.
        
        Formula:
            UCB1 = (Q_i / N_i) + c * sqrt((2 * ln(N_parent)) / N_i)
        """
        best_score = -float('inf')
        best_nodes = []
        log_parent_visits = math.log(max(self.visits, 1))

        for move, child in self.children.items():
            if child.visits == 0:
                score = float('inf')
            else:
                exploitation = child.wins / child.visits
                exploration = c_param * math.sqrt((2.0 * log_parent_visits) / child.visits)
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_nodes = [child]
            elif math.isclose(score, best_score, rel_tol=1e-9):
                best_nodes.append(child)

        # Break ties uniformly at random
        return random.choice(best_nodes)

    def add_child(self, move, state):
        """Add a new child node for `move` and remove `move` from untried moves."""
        child_node = MCTSNode(state=state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children[move] = child_node
        return child_node

    def update(self, winner):
        """
        Update node statistics with the simulation result.
        
        Parameters
        ----------
        winner : int (1, 2, 0 for draw, or None)
        """
        self.visits += 1
        if winner == 0:
            # Draw: split reward
            self.wins += 0.5
        elif winner == self.player_just_moved:
            # Win for the player whose move created this state
            self.wins += 1.0
        # Loss gives +0.0


class MCTS:
    """
    Monte Carlo Tree Search algorithm coordinator.
    
    Parameters
    ----------
    c_param : float, default=sqrt(2) ~ 1.414
        Exploration parameter balancing exploitation vs exploration in UCB1.
    """

    def __init__(self, c_param=math.sqrt(2.0)):
        self.c_param = c_param

    def search(self, root_state, num_simulations=1000):
        """
        Run MCTS for a specified number of simulations and return root node.
        
        Parameters
        ----------
        root_state : object
            Starting game state.
        num_simulations : int, default=1000
        
        Returns
        -------
        root_node : MCTSNode
        """
        root_node = MCTSNode(state=root_state)

        for _ in range(num_simulations):
            # 1. Selection
            node = root_node
            while node.is_fully_expanded() and not node.is_terminal():
                node = node.best_child(self.c_param)

            # 2. Expansion
            if not node.is_terminal() and node.untried_moves:
                move = random.choice(node.untried_moves)
                next_state = node.state.make_move(move)
                node = node.add_child(move, next_state)

            # 3. Simulation (Rollout)
            sim_state = node.state
            while not sim_state.is_terminal:
                legal = sim_state.get_legal_moves()
                if not legal:
                    break
                sim_state = sim_state.make_move(random.choice(legal))
            winner = sim_state.winner

            # 4. Backpropagation
            curr = node
            while curr is not None:
                curr.update(winner)
                curr = curr.parent

        return root_node

    def get_best_move(self, state, num_simulations=1000):
        """
        Execute MCTS search and select the most robust action.
        The robust child selection rule chooses the child with the
        HIGHEST VISIT COUNT (N), rather than highest average win rate,
        as visit count is more resilient to outlier rollouts.
        
        Parameters
        ----------
        state : object
        num_simulations : int, default=1000
        
        Returns
        -------
        best_move : object
            The chosen legal move.
        """
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None
        if len(legal_moves) == 1:
            return legal_moves[0]

        root = self.search(state, num_simulations=num_simulations)

        # Select action with the maximum number of visits
        best_move = max(root.children.items(), key=lambda item: item[1].visits)[0]
        return best_move

    def get_move_statistics(self, state, num_simulations=1000):
        """
        Return inspection statistics for each explored child move.
        
        Returns
        -------
        list of dicts containing move, visits, wins, win_rate
        """
        root = self.search(state, num_simulations=num_simulations)
        stats = []
        for move, child in sorted(root.children.items(), key=lambda item: item[1].visits, reverse=True):
            win_rate = child.wins / child.visits if child.visits > 0 else 0.0
            stats.append({
                'move': move,
                'visits': child.visits,
                'wins': child.wins,
                'win_rate': win_rate
            })
        return stats
