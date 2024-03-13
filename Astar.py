import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import queue

# Create an 8x8 array with all elements as 'Safe'
grid = np.full((8, 8), 'Safe')

# Function to populate the grid with 'WildAnimal' and 'Obstacle'
def populate_grid(grid, element, count):
    while count > 0:
        # Choose a random location in the grid
        row, col = random.randint(0, 7), random.randint(0, 7)
        # If the location is 'Safe', place the element there
        if grid[row, col] == 'Safe':
            # If the element is 'Obst', add a random direction (1-4)
            if element == 'Obst':
                direction = random.randint(1, 4)
                grid[row, col] = f'{direction}'
            else:
                grid[row, col] = element
            count -= 1

# Populate the grid with 10-15 'WildAnimal'
populate_grid(grid, 'W', random.randint(10, 15))

# Populate the grid with 5-7 'Obstacle'
populate_grid(grid, 'Obst', random.randint(5, 7))

# Set the bottom left cell as 'Start'
grid[7, 0] = 'Star'

# Set the top right cell as 'Goal'
grid[0, 7] = 'Goal'

# Create a new graph
G = nx.Graph()

# Add nodes and edges to the graph based on the grid
for i in range(8):
    for j in range(8):
        # Only add the node if it is not an obstacle
        if not str(grid[i, j]).startswith('Obst'):
            G.add_node((i, j))
            # Add an edge to the left node if it exists and is not an obstacle
            if j > 0 and not str(grid[i, j-1]).startswith('Obst'):
                G.add_edge((i, j), (i, j-1), weight=random.randint(1, 7))
            # Add an edge to the top node if it exists and is not an obstacle
            if i > 0 and not str(grid[i-1, j]).startswith('Obst'):
                G.add_edge((i, j), (i-1, j), weight=random.randint(1, 7))
            # Add an edge to the top left node if it exists and is not an obstacle
            if i > 0 and j > 0 and not str(grid[i-1, j-1]).startswith('Obst'):
                G.add_edge((i, j), (i-1, j-1), weight=random.randint(1, 7))
            # Add an edge to the top right node if it exists and is not an obstacle
            if i > 0 and j < 7 and not str(grid[i-1, j+1]).startswith('Obst'):
                G.add_edge((i, j), (i-1, j+1), weight=random.randint(1, 7))

# Function to check if it's safe to move to a node
def is_safe(node):
    # Check if the node is a 'WildAnimal'
    if grid[node] == 'W':
        # If it's a 'WildAnimal', there's a 0.8 probability of failing
        if random.random() < 0.8:
            return False
    return True

# Function to implement the UCS algorithm
def astar(G, start, goal):
    # Create a priority queue for the frontier
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    # Create a dictionary to store the cost to reach each node
    cost_to_reach = {start: 0}
    # Create a dictionary to store the path to each node
    path_to_node = {start: [start]}

    while not frontier.empty():
        # Get the node in the frontier with the lowest cost
        current_cost, current_node = frontier.get()

        # If the current node is the goal, return the cost and path to reach it
        if current_node == goal:
            return current_cost, path_to_node[current_node]

        # Check all neighbors of the current node
        for neighbor in G.neighbors(current_node):
            # Calculate the new cost to reach the neighbor
            new_cost = cost_to_reach[current_node] + G.edges[current_node, neighbor]['weight']
            
            # A* specific: Calculate the heuristic value (Manhattan distance to the goal)
            heuristic_value = abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
            
            # If the neighbor has not been visited yet or the new cost is lower than the previous cost
            if neighbor not in cost_to_reach or new_cost < cost_to_reach[neighbor]:
                # If it's safe to move to the neighbor
                if is_safe(neighbor):
                    # Update the cost to reach the neighbor
                    cost_to_reach[neighbor] = new_cost
                    # Update the path to the neighbor
                    path_to_node[neighbor] = path_to_node[current_node] + [neighbor]
                    # Add the neighbor to the frontier with priority based on f = g + h
                    frontier.put((new_cost + heuristic_value, neighbor))

# Use the UCS algorithm to find the minimum cost and path from 'Start' to 'Goal'
start, goal = (7, 0), (0, 7)
min_cost_astar_manhattan, path_astar_manhattan = astar(G, start, goal)

# Print the minimum cost and path
print("Minimum cost from 'Start' to 'Goal' (A* with Manhattan distance heuristic):")
print(min_cost_astar_manhattan)
print("Path from 'Start' to 'Goal' (A* with Manhattan distance heuristic):")
print(path_astar_manhattan)

# Create a new figure
fig, ax = plt.subplots()

# Create a color map for the grid
color_map = {
    'Safe': 'white',
    'W': 'green',
    '1': 'red',  # Obstacle facing left
    '2': 'blue',  # Obstacle facing top
    '3': 'yellow',  # Obstacle facing right
    '4': 'purple',  # Obstacle facing bottom
    'Star': 'orange',
    'Goal': 'pink',
    'Path': 'lightblue'  # Color for the path
}

# Color the cells in the path
for node in path_astar_manhattan:
    grid[node] = 'Path'

colors = [[color_map[cell] for cell in row] for row in grid]

# Use a table to visualize the grid
table = plt.table(cellText=grid, cellColours=colors, loc='center')

# Modify the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

plt.title("Treasure Hunt")
# Show the plot
plt.show()
