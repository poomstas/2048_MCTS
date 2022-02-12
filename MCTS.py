# %%
import random
from math import sqrt, log
from utils_2048 import add_two, reverse, transpose, cover_up, merge
from GameState import GameState

# %%
class Node:
    """Node object to represent a game state."""
    def __init__(self, move=None, parent=None, state=None): # Initialization scheme
        self.move = move                                    # The move that got us to this node - "None" for the root node
        self.parent_node = parent                           # "None" for the root node
        self.child_nodes = []                               # No child nodes when initializing. Use add_child to add child nodes
        self.visits = 0                                     # Refer to Wikipedia figure
        self.score = 0                                      # Refer to Wikipedia figure
        self.untried_moves = state.get_moves()              # Future child nodes

    def __repr__(self):
        """Representation of the current state as string."""
        return "[M:{}  S/V:{}  V:{}  Untried:{}]".format(self.move, self.score, self.visits, self.untried_moves)

    def select_child_UCT(self, C=sqrt(2)):
        """Select a child based on the UCT1 node. C is the bias parameter."""
        s = sorted(self.child_nodes, key=lambda c: c.score / c.visits + C * sqrt(log(self.visits) / c.visits))
        return s[-1]

    def add_child(self, move, state):
        """Remove move from untried_moves, add a new child node for this move. Return the added child node."""
        n = Node(move=move, parent=self, state=state)
        self.untried_moves.remove(move)
        self.child_nodes.append(n)
        return n

    def update(self, result):
        """Add one visit to the node and count the score."""
        self.visits += 1
        self.score += result

    def tree_to_string(self, indent):
        s = self.indent_string(indent) + str(self)
        for child in self.child_nodes:
            s += child.tree_to_string(indent + 1)
        return s

    def indent_string(self, indent):
        s = "\n"
        for _ in range(1, indent + 1):
            s += "| "
        return s

    def children_to_string(self):
        s = ""
        for child in self.child_nodes:
            s += str(child) + "\n"
        return s


# %%
def UCT(root_state, n_search_path, n_search_depth, exploration_const, verbose=False):
    """ Implements the UCT search for nSearchPath iteration starting from the root state.
        Return the best move to be executed at the root state. """
    
    root_node = Node(state=root_state)

    for _ in range(n_search_path):          # See what's happened after one iteration is done
        node = root_node                    # Start from the root node every iteration
        state = root_state.clone()          # Experiment with the clone of the root_state, not the actual one.

        # Select
        while node.untried_moves==[] and node.child_nodes!=[]: # Node is fully expanded and non-terminal
            node = node.select_child_UCT(C=exploration_const)
            state.do_move(node.move)

        # Expand
        if node.untried_moves!=[]:                  # If we can expand (i.e. state/node is non-terminal)
            move = random.choice(node.untried_moves)
            state.do_move(move)
            node = node.add_child(move, state)      # Add child and descend tree

        # Rollout
        search_depth_count = 0                      # Reset counter
        # Repeat while the state is non-terminal and the n_search_depth limit isn't yet reached:
        while state.game_state()=='not over' and search_depth_count<=n_search_depth:
            state.do_move(random.choice(state.get_moves()))
            search_depth_count += 1

        # Backpropagate
        while node is not None: # Backprop from the expanded node and work back to the root node.
            node.update(state.get_result()) # State is terminal. Update node with the result
            node = node.parent_node
    
    # Print info about the tree
    print(root_node.tree_to_string(0)) if verbose else print(root_node.children_to_string())

    # Return the move that was the most visited
    return sorted(root_node.child_nodes, key=lambda c: c.visits)[-1].move

# %%
def play_game():
    mat_init = add_two(add_two([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
    # mat_init = [[8, 4, 2, 8], [2, 16, 8, 4], [256, 32, 4, 2], [4, 2, 4, 2]]    # Death matrix for debugging
    # mat_init = [[2,4,32,2],[4,16,512,4],[4,8,128,16],[4,16,8,2]]               # Death matrix for debugging
    
    state = GameState(mat_init) # Initialize 2048 grid
    loop_count = 0
    game_over = False # True if add_two can't add anywhere after moving

    while state.game_state()=='not over' and game_over==False: # Run if the game is not over
        loop_count += 1

        print("Move count: " + str(loop_count))
        print("Points    : " + str(state.point_count))
        print(str(state))

        move = UCT(root_state=state, n_search_path=50, n_search_depth=5, exploration_const=100, verbose=True)

        print("Best Move: " + str(move) + "\n")
        game_over = state.do_move(move)

    print("======================= Game Over =======================")
    print(str(state))
    print(state.game_state())

# %%
if __name__ == "__main__":
    play_game()
