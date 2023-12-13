# for the first part it is straightforward since we can just try 
# all adjacent pipes if they are valid and then see if they lead back to S 
import sys

sys.setrecursionlimit(100000)
pipes = []
try:
    while True:
        pipes.append(input())
except EOFError:
    pass

# Edges are in the form J,F,7,|,-,L. Create a mapping to see if pipes connect
pipe_shapes = {
    '|': [(1,0),(-1,0)],
    '-': [(0,1),(0,-1)],
    'L': [(-1,0),(0,1)],
    '7': [(1,0),(0,-1)],
    'J': [(-1,0),(0,-1)],
    'F': [(1,0),(0,1)]
}

east_connectors = ['L','F','-']
west_connectors = ['7','J','-']
north_connectors = ['L','|', 'J']
south_connectors = ['7','|', 'F']

movement_to_connector = {
    (0,1): west_connectors,
    (0,-1): east_connectors,
    (1,0): north_connectors,
    (-1,0): south_connectors
}

START = 'S' 
GROUND = '.'

# find the coordinate of the start node
start_coord = None
for i, row in enumerate(pipes):
    for j, pipe in enumerate(row):
        if pipe == START:
            start_coord = (i,j)
            break

if start_coord == None:
    print("no start coord")
    exit()

def is_valid(i,j):
    return i >= 0 and i < len(pipes) and j >= 0 and j < len(pipes[0])

coord_negator = lambda x: (-x[0], -x[1])

def traverse(current_coord, prev_movement, visited):
    i,j = current_coord
    pipe_type = pipes[i][j]
    
    if pipe_type == GROUND or current_coord in visited:
        return False
    visited.add(current_coord)

    next_movement = list(filter(lambda x: x != coord_negator(prev_movement), pipe_shapes[pipe_type]))[0]
    next_coord = (i + next_movement[0], j + next_movement[1])
    
    if next_coord == start_coord:
        return True
    
    if not is_valid(next_coord[0], next_coord[1]):
        return False
    
    if pipes[next_coord[0]][next_coord[1]] not in movement_to_connector[next_movement]:
        return False
    
    return traverse(next_coord, next_movement, visited)

for i, movement_connectors_pair in enumerate(movement_to_connector.items()):
    movement, connectors = movement_connectors_pair
    
    next_position = (start_coord[0] + movement[0], start_coord[1] + movement[1])
    if not is_valid(next_position[0], next_position[1]):
        continue
    
    if pipes[next_position[0]][next_position[1]] not in connectors:
        continue
    
    visited = set()
    visited.add(start_coord)
    if traverse(next_position, movement, visited):
        print(len(visited)//2)