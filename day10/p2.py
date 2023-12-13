import sys
from collections import defaultdict

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

main_cycle_pipe_coordinates = set()
pipes_used = [] # keep track of which movement from S was valid, so we can determine which pipe shape S is
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
        main_cycle_pipe_coordinates = visited 
        pipes_used.append(movement)

print(pipes_used)
west_contacts = ['7','J','-']
east_contacts = ['L','F','-']
north_contacts = ['L','|', 'J']
south_contacts = ['7','|', 'F']

def get_start_pipe(movement_used):
    candidates = pipe_shapes.items()
    for key, val in candidates:
        if val[0] in movement_used and val[1] in movement_used:
            return key
    return None
    
print("Start pipe: ", get_start_pipe(pipes_used))
target_row = pipes[start_coord[0]]
# turn the string into a list so we can modify it
target_row = list(target_row)
target_row[start_coord[1]] = get_start_pipe(pipes_used)
pipes[start_coord[0]] = "".join(target_row) # complete the graph

# We create a more comprehensive graph representation to track whether or not the animal can squeeze through the pipes
# We do this by now having a vertex for the north, south, east, and west square of each pipe square. Our graph
# will be indexed by the coordinate (of the original pipe type) followed by the direction of the vertex
# e.g. (1,2) N will be the north vertex of the pipe at (1,2)

# for the sake of avoiding duplicate vertices (since north of i,j = south of i-1,j and east of i,j is west of i,j+1),
# we only annotate the west and north vertices of each pipe square.

def is_valid_augmented_coordinate(coordinate):
    i,j,direction = coordinate 
    row_bound = len(pipes) - 1 
    col_bound = len(pipes[0]) - 1
    
    if direction == "N":
        row_bound += 1
    if direction == "W":
        col_bound += 1
    
    return i >= 0 and i <= row_bound and j >= 0 and j <= col_bound

def add_undirected_edge(graph, coord1, coord2):
    graph[coord1].add(coord2)
    graph[coord2].add(coord1)

augmented_graph = defaultdict(set)
for i, row in enumerate(pipes):
    for j, pipe in enumerate(row):
        if (i,j) not in main_cycle_pipe_coordinates:
            continue
        
        if pipe == "L":
            add_undirected_edge(augmented_graph, (i,j,"N"), (i,j+1,"W"))
        elif pipe == "-":
            add_undirected_edge(augmented_graph, (i,j,"W"), (i,j+1,"W"))
        elif pipe == "7":
            add_undirected_edge(augmented_graph, (i,j,"W"), (i+1,j,"N"))
        elif pipe == "J":
            add_undirected_edge(augmented_graph, (i,j,"N"), (i,j,"N"))
        elif pipe == "F":
            add_undirected_edge(augmented_graph, (i,j+1,"W"), (i+1,j,"N"))
        elif pipe == "|":
            add_undirected_edge(augmented_graph, (i,j,"N"), (i+1,j,"N"))

visited = set()
pred = dict()
def dfs(graph, current, prev=None):
    if current in visited:
        return
    
    if not is_valid_augmented_coordinate(current):
        return
    
    visited.add(current)
    pred[current] = prev
    i,j,direction = current
            
    if direction == "N":
        # -1,0,N; -1,1,W; 0,1,N; 0,1,W; 1,0,N; 0,0,W; 0,-1,N; -1,0,W;
        if (i-1,j,"N") not in graph and is_valid(i-1,j) and not pipes[i-1][j] == "-":
            dfs(graph, (i-1,j,"N"), current)
        if (i,j+1,"N") not in graph:
            dfs(graph, (i,j+1,"N"), current)
        if (i+1,j,"N") not in graph and is_valid(i,j) and not pipes[i][j] == "-":
            dfs(graph, (i+1,j,"N"), current)
        if (i,j-1,"N") not in graph:
            dfs(graph, (i,j-1,"N"), current)
            
        if (i-1,j+1,"W") not in graph:
            dfs(graph, (i-1,j+1,"W"), current)
        if (i,j+1,"W") not in graph:
            dfs(graph, (i,j+1,"W"), current)
        if (i,j,"W") not in graph:
            dfs(graph, (i,j,"W"), current)
        if (i-1,j,"W") not in graph:
            dfs(graph, (i-1,j,"W"), current)
        
    elif direction == "W":
        # -1,0,W || 0,0,N || 0,1,W || 1,0,N || 1,0,W || 1,-1,N || 0,-1,W || 0,-1,N
        if (i-1,j,"W") not in graph:
            dfs(graph, (i-1,j,"W"), current)
        if (i,j+1,"W") not in graph and is_valid(i,j) and not pipes[i][j] == "|":
            dfs(graph, (i,j+1,"W"), current)
        if (i+1,j,"W") not in graph:
            dfs(graph, (i+1,j,"W"), current)
        if (i,j-1,"W") not in graph and is_valid(i,j-1) and not pipes[i][j-1] == "|":
            dfs(graph, (i,j-1,"W"), current)        
            
        if (i,j,"N") not in graph:
            dfs(graph, (i,j,"N"), current)
        if (i+1,j,"N") not in graph:
            dfs(graph, (i+1,j,"N"), current)
        if (i+1,j-1,"N") not in graph:
            dfs(graph, (i+1,j-1,"N"), current)
        if (i,j-1,"N") not in graph:
            dfs(graph, (i,j-1,"N"), current)
            
directions = ["N", "W"]

for j in range(len(pipes)+1):
    i = 0
    for direction in directions:
        if (i,j,direction) in augmented_graph:
            continue 
    
        dfs(augmented_graph, (i,j,direction)) # visits everything that can travel to the outside 

for i in range(len(pipes[0])+1):
    j = 0
    for direction in directions:
        if (i,j,direction) in augmented_graph:
            continue 
    
        dfs(augmented_graph, (i,j,direction)) # visits everything that can travel to the outside 

count = 0
for i in range(len(pipes)):
    for j in range(len(pipes[0])):
        if (i,j) in main_cycle_pipe_coordinates:
            continue
        
        # check if the north, south, east, or west vertex is reachable from the outside
        if (i,j,"N") not in visited and (i,j,"W") not in visited and  (i+1,j,"N") not in visited and (i,j+1,"W") not in visited:
            count += 1

f = lambda i,j: list(map(lambda x: x[2], filter(lambda x: x[0] == i and x[1] == j, visited)))
g = lambda i,j: f(i,j)+f(i,j+1)+f(i+1,j)

def get_pred_chain(coord):
    i,j,direction = coord
    
    prev = pred[coord]
    if prev is None:
        return [coord]
    
    return [coord] + get_pred_chain(prev)

# print(g(4,11))
# print(get_pred_chain((6,2,"W")))
print(count)