# Treasure Hunt

## Problem Description
The problem involves navigating through an 8x8 grid filled with safe zones, obstacles, and wild animals. The objective is to find the shortest path from the 'Start' cell to the 'Goal' (Treasure) cell while considering the constraints imposed by obstacles and the randomness associated with wild animals.

## UCS (Uniform Cost Search) Algorithm
The UCS algorithm is employed to find the minimum-cost path from the 'Start' to the 'Goal' on the grid. It explores paths based on the cost of each step and prioritizes paths with lower accumulated costs. The cost includes weights associated with grid edges and safety checks considering the presence of wild animals.

## A* Algorithm
A* search is utilized as an alternative to UCS. This algorithm combines the cost-to-reach a node with a heuristic function, which estimates the cost from the current node to the goal. In this implementation, both Euclidean and Manhattan distance heuristics are demonstrated. A* prioritizes paths with a balance of low accumulated costs and heuristic estimations.

## Libraries and Dependencies
The following Python libraries and dependencies are used in the code:

- `numpy`: Used for array manipulation and random number generation.
- `random`: Utilized for randomizing element placement in the grid.
- `matplotlib.pyplot`: Employed for grid visualization.
- `networkx`: Used for creating and manipulating graphs.
- `queue`: Used to implement priority queues for UCS and A* algorithms.

To run the code successfully, ensure you have these libraries installed in your Python environment. You can install them using the following command:

```bash
pip install numpy matplotlib networkx
