import copy

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
vowel_animals = [a for a in animals if a[0] in ['A', 'E', 'I', 'O', 'U']]

grid = {i : animals.copy() for i in range(9)}

def pos(x,y):
    return x+3*y

def print_grid(g, title = None, depth=0):
    print('\t' * depth, title)
    for y in range(3):
        for x in range(3):
            if len(g[pos(x, y)]) == 0:
                s = 'XXX'
            else:
                s = ','.join([s[0] for s in sorted(g[pos(x,y)])])
            s = s + " " * (16-len(s))
            print('\t' * depth, s, end='\t\t')
        print()
    print()

print_grid(grid, 'Start with a full grid')
print('Setting Goat & Hippo')
grid[pos(1, 1)] = ['Goat']
grid[pos(2, 2)] = ['Hippopotamus']

def get_known(g, x, y):
    values = g[pos(x, y)]
    if len(values) == 1:
        return values[0]
    return None

def remove_val(g, x, y, to_remove):
    remove_vals(g, x, y, [to_remove])

def remove_vals(g, x, y, to_remove):
    for r in to_remove:
        if r in g[pos(x, y)]:
            g[pos(x, y)].remove(r)

def positions():
    positions = []
    for y in range(3):
        for x in range(3):
            positions.append((x, y))
    return positions

def known_positions(g):
    known = []
    for x, y in positions():
        animal = get_known(g, x, y)
        if animal != None:
            known.append((x, y, animal))
    return known

def rule_there_can_only_be_one(g):
    for x, y, animal in known_positions(g):
        for i, j in positions():
            # Don't remove when it's the known position!
            if x != i or y != j:
                remove_val(g, i, j, animal)
   
def get_neighbours(animal):
    neighbours = []
    i = animals.index(animal)
    if i > 0:
        neighbours.append(animals[i-1])
    if (i+1) < len(animals):
        neighbours.append(animals[i+1])
    return neighbours
    
def rule_no_alphabetical_neighbour(g):
    for x, y, animal in known_positions(g):
        neighbours = get_neighbours(animal)
        # v neighbours can't be above/below/left/right
        if y > 0:
            remove_vals(g, x, y-1, neighbours)
        if y < 2:
            remove_vals(g, x, y+1, neighbours)
        if x > 0:
            remove_vals(g, x-1, y, neighbours)
        if x < 2:
            remove_vals(g, x+1, y, neighbours)

def same_col(x, y):
    others = []
    for j in range(3):
        if j != y:
            others.append((x, j))
    return others

def same_row(x, y):
    others = []
    for i in range(3):
        if i != x:
            others.append((i, y))
    return others

def rule_no_two_vowels(g):
    for x, y, animal in known_positions(g):
        if animal in vowel_animals:
            # can't have any other vowel animals on this row or col
            for i, j in same_col(x, y) + same_row(x, y):
                remove_vals(g, i, j, vowel_animals)

def rule_alligator_in_bottom_row(g):
    for y in range(2):
        for x in range(3):
            remove_val(g, x, y, 'Alligator')

def rule_duck_not_on_bottom(g):
    for x in range(3):
        remove_val(g, x, 2, 'Duck')

def rule_fox_not_in_third_col(g):
    for y in range(3):
        remove_val(g, 2, y, 'Fox')

def rule_iguana_is_in_corner(g):
    for y in range(3):
        remove_val(g, 1, y, 'Iguana')
    for x in range(3):
        remove_val(g, x, 1, 'Iguana')

def rule_beaver_eagle_same_col(g):
    looking_for = ['Beaver', 'Eagle']
    for x, y, animal in known_positions(g):
        if animal in looking_for:
            # Remove looking_for from other cols, where x is different
            for i, j in positions():
                if i != x:
                    remove_vals(g, i, j, looking_for)

def rule_cheetah_goat_same_row(g):
    looking_for = ['Cheetah', 'Goat']
    for x, y, animal in known_positions(g):
        if animal in looking_for:
            # Remove looking_for from other rows, where y is different
            for i, j in positions():
                if j != y:
                    remove_vals(g, i, j, looking_for)

print()
rule_alligator_in_bottom_row(grid)
rule_duck_not_on_bottom(grid)
rule_fox_not_in_third_col(grid)
rule_iguana_is_in_corner(grid)
print_grid(grid, 'Cleared obvious rules')

def has_empty_cells(g):
    for x, y in positions():
        if len(g[pos(x, y)]) == 0:
            return True
    return False

def finished(g):
    return len(known_positions(g)) == 9

def apply_rules(g):
    # Keep applying rules until known cells stable
    last_known_position_count = None
    while last_known_position_count != len(known_positions(g)):
        last_known_position_count = len(known_positions(g))
        rule_there_can_only_be_one(g)
        rule_no_alphabetical_neighbour(g)
        rule_no_two_vowels(g)
        rule_beaver_eagle_same_col(g)
        rule_cheetah_goat_same_row(g)

def step(g, depth):
    print_grid(g, 'Depth: ' + str(depth), depth)
    apply_rules(g)
    print_grid(g, 'After rules', depth)
    if has_empty_cells(g):
        return None
    if finished(g):
        print('Finished')
        return g

    guesses = []
    for y in range(3):
        for x in range(3):
            values = g[pos(x, y)]
            if len(values) > 1:
                for v in values:
                    guesses.append((x, y, v))
    for x, y, v in guesses:
        new_g = copy.deepcopy(g)
        print('Tweaking ', x, y, v)
        if x == 0 and y == 1 and v == 'Cheetah' and depth==3:
            print('omg')
        new_g[pos(x, y)] = [v]
        result = step(new_g, depth+1)
        if result != None:
            return result
    return None

result = step(grid, 0)
assert(result != None)
print_grid(result, 'Found solution')