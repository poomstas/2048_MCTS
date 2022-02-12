# MCTS to Solve the 2048 Puzzle 

## Objective / Problem Statement
Create an agent that is able to solve the 2048 puzzle.

Employ the Monte-Carlo Tree Search (MCTS) algorithm to solve the 2048 puzzle. 

If you are unfamiliar with the 2048 puzzle, you can play and get a sense of it [here](https://play2048.co/).

## The 2048 Game
2048 is a simple board game. As shown below, the board has 4x4 squares, some of which are occupied by number blocks. The player can press one of the four (up, down, left, right) arrows to shift 

## The Monte Carlo Tree Search Algorithm
Monte Carlo Tree Search (MCTS) is a probabilistic tree search algorithm that uses repeated random sampling to estimate the value of actions as a game progresses. At every iterative state, stochastic sampling is used to update the estimates of the values of actions available at a given state, and the estimates are then used to expand the tree. Then, based on the expanded game tree, the next action is decided. As the algorithm continues to implement actions that are expected to be optimal, the process of traversing and expanding the tree is repeated at every iteration. MCTS is a probabilistic method because at the core of the algorithm, there is the stochastic sampling that attempts to capture the response of actions without exhaustively examining them. Although it does not guarantee that it will find the optimal series of actions, many applications of MCTS in different fields have demonstrated that it is able to provide a close approximation of the optimal policy.

As the name suggests, MCTS involves a tree-like structure; it is used to represent different states and available actions. An example of a tree structure of a tic-tac-toe game is in the figure below. In the diagram, the nodes represent different states that the tic-tac-toe board could take (nodes are more generally represented as a simple circle than a board). At the top of the tree, we start with the root node, with which represent the state of the board the game begins. Given this state, the first player has nine different actions he can take. Four of the nine available actions are visualized in the figure. In the diagram, the available actions are represented using edges, which are the lines that connect the states. The states of the board resulting from these actions are represented using the child nodes. Four of the nine child nodes are shown in the figure in the second row as an example. Once MCTS carries out an action, then the corresponding child node becomes the new root node, and its sibling nodes would be discarded.

<p align="center">
  <img src="/readme_img/A_TicTacToe.png" width="450" title="Monte-Carlo Tree Search Applied to Tic-Tac-Toe">
</p>


Each state carries with it an estimate of value that is calculated using Monte Carlo simulations. These values are then used to compare the quality of one action over another. Overall, MCTS consists of four stages: selection, expansion, simulation, and backpropagation. The four processes are repeated at every iteration, one of which is shown as an example in the figure below. The two numbers in the nodes of the example tree represent the number of simulated wins and the number of simulations (“visits”) that particular state has observed. The following sections will provide an overview of the mechanics of each stage using the example tree provided.

<p align="center">
  <img src="/readme_img/B_MCTS.png" width="450" title="The Four Stages in Monte-Carlo Tree Search Algorithm">
</p>

### Selection
Selection process points the algorithm to which action is likely to be worth exploring. It takes the current state of the tree and selects decisions down that tree to a future state at a fixed depth. The relative value of different nodes are determined using the UCB equation (explained in the next section), which systematically incorporates both the observed average returns and the uncertainty associated with the estimated average.

### Node Expansion
In this step, a new node is added to the tree as a child node of the node selected in the previous step. Only a single node is newly introduced to the tree at every iteration. In the figure, the expanded node has the numbers 0/0 because it has neither observed any wins nor simulations.

### Simulation / Rollout
The simulation step consists of randomly choosing moves until the algorithm reaches the terminal state or a specified threshold. Once the terminal conditions are met, then the algorithm calculates and returns a result of how well it performed as a score (in this work, the value is calculated from the NPV). This score is then passed to the backpropagation phase. This stage relies on a forward model that provides us with the outcomes of an action in any state.

### Backpropagation
Once the value of the newly introduced node is determined in the simulation phase, the tree structure is updated. In the backpropagation step, the algorithm updates the perceived value of a given state, not just to the state it executed in the simulation but also every state that led to that state in the tree. The collection of the updated nodes can be observed by tracing the arrow that leads back up to the original parent node in the figure above. This updating scheme allows the algorithm to search for early actions that may lead to opportunities that that may be observed in the future. The scores are updated until the root node (starting point) is reached.
Through the above four stages, we can take decisions to a fixed point in the tree, simulate their outcome, propagate back the perceived value of it. This process is repeated multiple times to balance out the optimal set of actions. Once the simulation count limit is reached, the algorithm chooses the optimal action leading to the state with the highest value.


The Monte Carlo Tree Search (MCTS) algorithm primarily consists of the following 4 phases:
1. Tree traversal
2. Node expansion
3. Rollout (random simulation)
4. Backpropagation



## Reason why MCTS is appropriate for this game
1. Action space is discrete, and the number of available actions at each stage is small (<= 4).
2. Discrete time steps
3. After each action is taken, there are a stochastic process that can be modeled using multiple Monte Carlo simulations

I used the Python implementation of the 2048 puzzle that is taken from https://github.com/weihanglo/py2048.

# Observations
1. Probably don't need that many search paths, especially at the beginning. It's kind of hard to lose the game at first.
2. Need to adaptively adjust the number of search paths as the game progresses. I can afford to search a lot more in the later stages because each simulation doesn't run as long.
3. It's kind of interesting to note that when a human plays the game, he probably approaches it more like a markov model than this algorithm does, only seeing the next couple of steps. 
