# %%
import random
from math import sqrt, log

# %%
class Node:
    """Node object to represent a game state."""

    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent_node = parent
        self.child_nodes = []
        self.visits = 0
        self.score = 0
        self.untried_moves = None  # Need to write some kind of get_moves method. 

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
        self.untried_move.remove(move)
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

    for _ in range(n_search_path):
        node = root_node
        state = root_state.Clone()

        # Select
        while node.untried_moves==[] and node.child_nodes!=[]: # Node is fully expanded and non-terminal
            node = node.select_child_UCT(C=exploration_const)
            state.do_move(node.move)

        # Expand
        if node.untried_moves!=[]:
            move = random.choice(node.untried_moves)
            state.do_move(move)
            node = node.add_child(move, state)

        # Rollout
        search_depth_count = 0
        while state.game_state()=='not over' and search_depth_count<=n_search_depth:
            state.do_move(random.choice(state.get_moves()))
            search_depth_count += 1

        # Backpropagate
        while node is not None:
            node.update(state.get_result())
            node = node.parent_node
    
    # Print info about the tree
    print(root_node.tree_to_string(0)) if verbose else print(root_node.children_to_string())

    # Return the move that was the most visited
    return sorted(root_node.child_nodes, key=lambda c: c.visits)[-1].move


# %%
if __name__ == "__main__":
    node = Node(state="0000/0000/0000/0020", move="up", parent=None)
