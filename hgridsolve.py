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

vowel_animals = []
for a in animals:
    if a[0] in ['A', 'E', 'I', 'O', 'U']:
        vowel_animals.append(a)

def positions():
    """
    All the valid positions in the 3x3 grid
    """
    positions = []
    for y in range(3):
        for x in range(3):
            positions.append((x, y))
    return positions

def print_grid(g, title = None, depth=0):
    """
    Print out the grid, a bit nicely.
    """
    print('\t' * depth, title)
    for y in range(3):
        for x in range(3):
            if len(g[(x, y)]) == 0:
                s = 'XXX'
            else:
                s = ','.join([s[0] for s in sorted(g[(x,y)])])
            s = s + " " * (16-len(s))
            print('\t' * depth, s, end='\t\t')
        print()
    print()

def get_known(g, x, y):
    """
    Value of a cell if it's known (only one possibility), otherwise None
    """
    values = g[(x, y)]
    if len(values) == 1:
        return values[0]
    return None

def remove_val(g, x, y, to_remove):
    """
    Remove a possibility from a cell.
    """
    remove_vals(g, x, y, [to_remove])

def remove_vals(g, x, y, to_remove):
    """
    Remove a list of possibilities from a cell
    """
    for r in to_remove:
        if r in g[(x, y)]:
            g[(x, y)].remove(r)

def known_positions(g):
    """
    All the positions where we know the value (and that value)
    """
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

def has_empty_cells(g):
    for x, y in positions():
        if len(g[(x, y)]) == 0:
            return True
    return False

def finished(g):
    return len(known_positions(g)) == 9

def apply_rules(g):
    count_of_known_positions_before_rules = len(known_positions(g))
    rule_there_can_only_be_one(g)
    rule_no_alphabetical_neighbour(g)
    rule_no_two_vowels(g)
    rule_beaver_eagle_same_col(g)
    rule_cheetah_goat_same_row(g)
    # Keep applying rules until known cells stable
    if count_of_known_positions_before_rules != len(known_positions(g)):
        apply_rules(g)

def step(g, depth):
    #print_grid(g, 'Depth: ' + str(depth), depth)
    apply_rules(g)
    #print_grid(g, 'After rules', depth)
    if has_empty_cells(g):
        return None
    if finished(g):
        print('Finished')
        return g

    guesses = []
    for y in range(3):
        for x in range(3):
            values = g[(x, y)]
            if len(values) > 1:
                for v in values:
                    guesses.append((x, y, v))
    for x, y, v in guesses:
        new_g = copy.deepcopy(g)
        new_g[(x, y)] = [v]
        result = step(new_g, depth+1)
        if result != None:
            return result
    return None

# Grid starts with all the animals as possible for all the cells
grid = {(x, y) : animals.copy() for x, y in positions()}
print_grid(grid, 'Start with a full grid')
print('Setting Goat & Hippo')
grid[(1, 1)] = ['Goat']
grid[(2, 2)] = ['Hippopotamus']

print()
rule_alligator_in_bottom_row(grid)
rule_duck_not_on_bottom(grid)
rule_fox_not_in_third_col(grid)
rule_iguana_is_in_corner(grid)
print_grid(grid, 'Cleared obvious rules')

result = step(grid, 0)
assert(result != None)
print_grid(result, 'Found solution')