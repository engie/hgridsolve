from ortools.sat.python import cp_model

animals = [
    'Alligator',
    'Beaver',
    'Cheetah',
    'Duck',
    'Eagle',
    'Fox',
    'Goat',
    'Hippopotamus',
    'Iguana',
]

model = cp_model.CpModel()

# Represent the cells
# Each cell will have an int representing the offset into the animals array
assert len(animals) == 3*3, 'Zoo mis-sized'
cells = [[model.new_int_var(0, len(animals), f"cell_{x}_{y}") for x in range(3)] for y in range(3)]
# Each cell must be different
model.AddAllDifferent(sum(cells, []))

# Initial known states
model.Add(cells[1][1] == animals.index('Goat'))
model.Add(cells[2][2] == animals.index('Hippopotamus'))

# Rules
# No animals have alphabetical neighbour by col or row
# Approach: Use ForbiddenAssignments for adjacent animals between rows and cols
def adjacent(a, b):
    return abs(ord(animals[a][0]) - ord(animals[b][0])) == 1
alpha_neighbours = [(i, j) for i in range(len(animals)) for j in range(len(animals)) if adjacent(i, j)]

#Vertical
for row in range(2):
    for col in range(3):
        model.AddForbiddenAssignments((cells[row][col], cells[row+1][col]), alpha_neighbours)
#Horizontal
for row in range(3):
    for col in range(2):
        model.AddForbiddenAssignments((cells[row][col], cells[row][col+1]), alpha_neighbours)

# Return a bool variable that's true if cell contains a value from values. Values are strings.
def cell_has_one_of_values(name, cell, values):
    # For all the animal IDs, (ID, 0/1) where bool value is 1 if animal id in the list
    valid_pairs = [(i,int(animal in values)) for i, animal in enumerate(animals)]
    is_value = model.NewBoolVar(name)
    model.AddAllowedAssignments((cell, is_value), valid_pairs)
    return is_value

# Map a list of cells to a list of bools where bool is true if cell in values. Values are strings.
def cells_have_one_of_values(name, cells, values):
    bools = []
    for i, cell in enumerate(cells):
        bools.append(cell_has_one_of_values(f"{name}_{i}", cell, values))
    return bools

# No more than one animal starting with vowel per row or col
vowelimals = [animal for animal in animals if animal[0] in ['A', 'E', 'I', 'O', 'U']]
for row in range(3):
    model.AddAtMostOne(*cells_have_one_of_values(f'vowel_row_{row}', cells[row], vowelimals))
for col in range(3):
    col_cells = [cells[i][col] for i in range(3)]
    model.AddAtMostOne(*cells_have_one_of_values(f'vowel_col_{col}', col_cells, vowelimals))

# Alligator in bottom row
model.AddExactlyOne(*cells_have_one_of_values('alligator', cells[2], ['Alligator']))

# Duck not on bottom
for col in range(3):
    model.Add(cells[2][col] != animals.index('Duck'))

# Fox not in third col
for row in range(3):
    model.Add(cells[row][2] != animals.index('Fox'))

# Iguana is in a corner
corners = [cells[0][0], cells[0][2], cells[2][0], cells[2][2]]
model.AddExactlyOne(*cells_have_one_of_values('iguana', corners, ['Iguana']))

# Count how many times specific values show up in a set of cells
# For every cell have bool cells for is in the values list
# Have an int that is the sum of those bools, this counts them
# Have a bool cell that is true if the sum equals a counter
def exact_count_values_seen_in_cells(name, cells, values, count):
    values_seen = cells_have_one_of_values(name, cells, values)
    sum_bools = model.NewIntVar(0, 3, f"{name}_sum")
    model.Add(sum_bools == sum(values_seen))
    is_count = model.NewBoolVar(f"{name}_count")
    model.Add(sum_bools == count).OnlyEnforceIf(is_count)
    model.Add(sum_bools != count).OnlyEnforceIf(is_count.Not())
    return is_count

# Beaver and Eagle in the same column
# For every column, get a bool true if the column has both animals
# Assert that only one of those bool cells is true.
col_counts = []
for col in range(3):
    col_cells = [cells[i][col] for i in range(3)]
    is_count = exact_count_values_seen_in_cells(f"beavereaglec_{col}", col_cells, ['Beaver', 'Eagle'], 2)
    col_counts.append(is_count)
model.AddExactlyOne(col_counts)

# Cheetah and Goat in the same row
row_counts = []
for row in range(3):
    is_count = exact_count_values_seen_in_cells(f"cheetahgoat_{row}", cells[row], ['Cheetah', 'Goat'], 2)
    row_counts.append(is_count)
model.AddExactlyOne(row_counts)

solver = cp_model.CpSolver()
status = solver.solve(model)
assert status == 4, "Couldn't find a solution"

from grid import print_3x3_grid
print_3x3_grid(0, lambda x, y: animals[solver.value(cells[y][x])])