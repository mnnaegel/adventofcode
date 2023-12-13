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

# create new representation of space we can perform algos on...
new_space = []
for i, row in enumerate(space):
    new_row = []
    for j, col in enumerate(row):
        if j in empty_cols:
            new_row.append(EMPTY)
        new_row.append(col)
    new_space.append(new_row)
    if i in empty_rows:
        new_space.append([EMPTY] * (m+len(empty_cols)))

galaxy_coordinates = []
for i, row in enumerate(new_space):
    for j, col in enumerate(row):
        if col == GALAXY:
            galaxy_coordinates.append((i, j))

distances = 0
for i in range(len(galaxy_coordinates)):
    for j in range(i, len(galaxy_coordinates)):
        distances += abs(galaxy_coordinates[i][0] - galaxy_coordinates[j][0]) + abs(galaxy_coordinates[i][1] - galaxy_coordinates[j][1])

print(distances)
