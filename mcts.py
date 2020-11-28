from random import choice
from math import sqrt, log
# from pprint import pprint

class Node:
	''' Node object to represent a game state. '''

	def __init__(self, state, move, parent):
		self.move = move
		self.parent_node = parent
		self.child_nodes = []
		
		self.visits = 0
		self.wins   = 0
		self.untried_moves = None # Need to write some kind of get_moves method.
	
	def __repr__(self):
		return "[M:{}  W/V:{}  V:{}  Untried:{}]".format(self.move, self.wins, self.visits, self.untried_moves)
	
	def add_child(self, move, state):
		''' 
			Remove move from untried_moves, 
			and add a new child node for this move. 
			Return the added child node. 
		'''
		n = Node(move=move, parent=self, state=state)
		self.untried_move.remove(move)
		self.child_nodes.append(n)

		return n
	
	def update(self, result):
		''' Add one visit to the node and count the wins. '''
		self.visits += 1
		self.wins += result

	def select_child_UCT(self, C = sqrt(2)):
		''' Select a child based on the UCT1 node. '''
		# C : Bias parameter
		s = sorted(self.child_nodes, 
			key=lambda c: c.wins/c.visits + C * sqrt(log(self.visits)/c.visits))[-1]
		return s
	
if __name__=="__main__":
	node = Node(state="0000/0000/0000/0020", move="up", parent=None)
