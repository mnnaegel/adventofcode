"""
can do bsearch on the rows and cols but i cba
"""

import bisect

space = []

try:
    while True:
        space.append(input())
except EOFError:
    pass

n = len(space)
m = len(space[0])
GALAXY = '#'
EMPTY = '.'

empty_cols = set()
empty_rows = set()
# identify the columns that are all empty
for j in range(m):
    is_empty = True
    for i in range(n):
        if space[i][j] == GALAXY:
            is_empty = False
            break
    empty_cols.add(j) if is_empty else None

# identify rows that are all empty 
for i in  range(n):
    is_empty = True
    for j in range(n):
        if space[i][j] == GALAXY:
            is_empty = False
            break
    empty_rows.add(i) if is_empty else None

galaxy_coordinates = []
for i in range(n):
    for j in range(m):
        if space[i][j] == GALAXY:
            galaxy_coordinates.append((i,j))

# you can't really avoid the empty rows and empty cols.. so just count 
# how many of them you have to cross 

distances = 0
gap_size = 1000000
print("ROWS:",empty_rows)
print("COLS:",empty_cols)
print(galaxy_coordinates)

for i in range(len(galaxy_coordinates)):
    for j in range(i, len(galaxy_coordinates)):
        lower_row = min(galaxy_coordinates[i][0], galaxy_coordinates[j][0])
        upper_row = max(galaxy_coordinates[i][0], galaxy_coordinates[j][0])
        lower_col = min(galaxy_coordinates[i][1], galaxy_coordinates[j][1])
        upper_col = max(galaxy_coordinates[i][1], galaxy_coordinates[j][1])

        columns_crossed = len(list(filter(lambda x: x >= lower_col and x <= upper_col, empty_cols)))
        rows_crossed = len(list(filter(lambda x: x >= lower_row and x <= upper_row, empty_rows)))
        
        distances += (columns_crossed + rows_crossed) * (gap_size)
        
        distances += abs(galaxy_coordinates[i][0] - galaxy_coordinates[j][0]) + abs(galaxy_coordinates[i][1] - galaxy_coordinates[j][1]) - columns_crossed - rows_crossed
        
print(distances)
