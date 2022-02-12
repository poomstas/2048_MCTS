# MCTS to Solve the 2048 Puzzle 

## Objective / Problem Statement
Create an agent that solves the 2048 puzzle. In this work, I employ the Monte-Carlo Tree Search (MCTS) algorithm to achieve this objective.

## The 2048 Game
2048 is a simple board game. As shown below, the board has 4x4 squares, some of which are occupied by number blocks. The player can press one of the four (up, down, left, right) arrows to shift the blocks in the specified direction. Adjacent blocks with the same number will add together, combining into one block with a value of the two blocks' values added together. If the adjacent blocks do not have the same number, then they will not combine.

The game is considered successfully solved if the largest number on the grid reaches 2048, hence the name. The game terminates unsuccessfully if, after an action is taken and a new block is added, there are no empty blocks left and there are no valid moves available. 

Play and get a sense of it [here](https://play2048.co/).

## The Monte Carlo Tree Search (MCTS) Algorithm
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
Selection process points the algorithm to which action is likely to be worth exploring. It takes the current state of the tree and selects decisions down that tree to a future state at a fixed depth. The relative value of different nodes are determined using the UCB equation (explained below), which systematically incorporates both the observed average returns and the uncertainty associated with the estimated average.

#### Upper Confidence Bound (UCB)
The upper confidence bound (UCB) is used in the MCTS’s selection stage to traverse the tree. UCB is used to balance the selection process between exploration and exploitation. Exploration and exploitation refers to the challenge posed to an agent to choose between acquiring new knowledge about the system and returning to an option that is expected to have large returns, based on current knowledge. The UCB algorithm proposes that the agent pull the arm that maximizes the following:

<p align="center">
  <img src="/readme_img/C_UcbEqn.png" width="450" title="UCB Equation">
</p>

The above equation is intuitive. The `ωi/ni` term is the current estimate of returns associated with a decision. The remaining `c sqrt(ln(Ni)/ni)` term represent the upper bound of the confidence interval associated with the estimate, which is updated as the number of observations accumulate over time. The second term decreases as more observations are sampled to represent increased confidence in the expected returns.

The parameter `c` in the above equation controls for the extent to which uncertain options are favored. If `c` is set to zero, then the UCB algorithm would recommend that the agent pulls the arm solely based on the expected returns without considering the uncertainties associated with the estimations (i.e. exploitation). If `c` is set to a larger value, then the relative contribution of the expected value is reduced in the selection process, shifting the significance more towards the uncertainties associated with estimates of expected returns. In other words, a UCB algorithm with a larger `c` tends to favor options that are not previously explored (i.e. exploration). An implementation of the selection process using the UCB equation will show that the algorithm will attempt to quickly identify the best alternative, and as it proceeds, it will keep searching for other good options while validating the optimality of the current “best”.



### Node Expansion
In this step, a new node is added to the tree as a child node of the node selected in the previous step. Only a single node is newly introduced to the tree at every iteration. In the figure, the expanded node has the numbers 0/0 because it has neither observed any wins nor simulations.

### Simulation / Rollout
The simulation step consists of randomly choosing moves until the algorithm reaches the terminal state or a specified threshold. Once the terminal conditions are met, then the algorithm calculates and returns a result of how well it performed as a score (in this work, the value is calculated from the NPV). This score is then passed to the backpropagation phase. This stage relies on a forward model that provides us with the outcomes of an action in any state.

### Backpropagation
Once the value of the newly introduced node is determined in the simulation phase, the tree structure is updated. In the backpropagation step, the algorithm updates the perceived value of a given state, not just to the state it executed in the simulation but also every state that led to that state in the tree. The collection of the updated nodes can be observed by tracing the arrow that leads back up to the original parent node in the figure above. This updating scheme allows the algorithm to search for early actions that may lead to opportunities that that may be observed in the future. The scores are updated until the root node (starting point) is reached.

Through the above four stages, we can take decisions to a fixed point in the tree, simulate their outcome, propagate back the perceived value of it. This process is repeated multiple times to balance out the optimal set of actions. Once the simulation count limit is reached, the algorithm chooses the optimal action leading to the state with the highest value.


## Why is MCTS an appropriate algorithm for solving this game?
1. Action space is discrete (up, down, left, right), and the number of available actions at each stage is small (<= 4).
2. The game follows a Markov decision process, a discrete-time stochastic control.
- Timesteps are discrete and well-defined. 
- After each action is taken, there is a stochastic process, which can be modeled easily using multiple Monte Carlo simulations/sampling.

I used the Python implementation of the 2048 puzzle that is taken from [REF].

# Hyperparameter Optimization
The main hyperparameters of the MCTS algorithm are: `nSearchPath`, `nSearchDepth`, and `explorationConst`, specifying the number of search paths, the depth of search, and the exploration constant. These hyperparameters together determine the tradeoff between exploration and exploitation. 

I have determined that the 

<p align="center">
  <img src="/readme_img/C_HyperparamOptim.png" width="450" title="Hyperparameter Optimization">
</p>

# Results
Running an instance of `MCTS.py` script will initialize a MCTS algorithm and attempt to solve a game of 2048. Below is an example of a successful run where the algorithm was able to reach 2048 before terminating.

<p align="center">
  <img src="/readme_img/Z_WonGame.png" width="450" title="Won Game">
</p>

`multiple_runs_sim.py` file simulates multiple runs to determine the rate of success 


# Observations (Needs Editing)
1. I probably don't need that many search paths, especially at the beginning. When there are many empty cells in the grid, it's nearly impossible to lose the game. It may even be more computationally efficient to simply sample randomly from the available four actions. Once a certain fraction of the grid is occupied by blocks, I can turn begin to calculate optimal actions based on the MCTS algorithm.
2. In a similar sense, I can adaptively adjust the number of search paths as the game progresses. This is also because I can afford to search a lot more in the later stages because each simulation doesn't run as long until the game is terminated.
3. It's kind of interesting to note that when a human plays the game, he probably approaches it more like a Markov model than this algorithm does, only seeing the next couple of steps. It is also likely that he abides by a simple heuristic than to simulate actions and resulting states.
