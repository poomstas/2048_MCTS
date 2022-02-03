# MCTS to Solve the 2048 Puzzle 

## Objective / Problem Statement
Create an agent that is able to solve the 2048 puzzle.

Employ the Monte-Carlo Tree Search (MCTS) algorithm to solve the 2048 puzzle. 

If you are unfamiliar with the 2048 puzzle, you can play and get a sense of it [here](https://play2048.co/).

## The 2048 Game
2048 is a simple board game. As shown below, the board has 4x4 squares, some of which are occupied by number blocks. The player can press one of the four (up, down, left, right) arrows to shift 

## Reason why MCTS is appropriate for this game
1. Action space is discrete, and the number of available actions at each stage is small (<= 4).
2. Discrete time steps
3. After each action is taken, there are a stochastic process that can be modeled using multiple Monte Carlo simulations

I used the Python implementation of the 2048 puzzle that is taken from https://github.com/weihanglo/py2048.
