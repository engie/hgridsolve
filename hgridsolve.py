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
    print('\t\ * depth, title)
    for y in range(3):
        for x in range(3):
            assert(len(g[pos(x, y)]) > 0)
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
    assert(len(g[pos(x, y)]) > 0)

def rule_there_can_only_be_one(g):
    for x in range(3):
        for y in range(3):
            v = get_known(g, x, y)
            if v != None:
                for i in range(3):
                    for j in range(3):
                        if x != i and y != j:
                            remove_val(g, i, j, v)
   
def get_neighbours(value):
    neighbours = []
    i = animals.index(value)
    if i > 0:
        neighbours.append(animals[i-1])
    if (i+1) < len(animals):
        neighbours.append(animals[i+1])
    return neighbours
    
def rule_no_alphabetical_neighbour(g):
    for y in range(3):
        for x in range(3):
            v = get_known(g, x, y)
            if v != None:
                neighbours = get_neighbours(v)
                # v neighbours can't be above/below/left/right
                if y > 0:
                    remove_vals(g, x, y-1, neighbours)
                if y < 2:
                    remove_vals(g, x, y+1, neighbours)
                if x > 0:
                    remove_vals(g, x-1, y, neighbours)
                if x < 2:
                    remove_vals(g, x+1, y, neighbours)

def rule_no_two_vowels(g):
    # For each row
    for y in range(3):
        for x in range(3):
            v = get_known(g, x, y)
            if v in vowel_animals:
                for i in range(3):
                    if i != x:
                        remove_vals(g, i, y, vowel_animals)
    
    # For each col
    for x in range(3):
        for y in range(3):
            v = get_known(g, x, y)
            if v in vowel_animals:
                for j in range(3):
                    if j != y: 
                        remove_vals(g, x, j, vowel_animals)

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
    found_col = None
    for x in range(3):
        for y in range(3):
            if get_known(g, x, y) in looking_for:
                assert(found_col == x or found_col == None)
                found_col = x
    if found_col != None:
        for x in range(3):
            if x != found_col:
                for y in range(3):
                    remove_val(g, x, y, looking_for)

def rule_cheetah_goat_same_row(g):
    looking_for = ['Cheetah', 'Goat']
    found_row = None
    for y in range(3):
        for x in range(3):
            if get_known(g, x, y) in looking_for:
                assert(found_row == y or found_row == None)
                found_row = y
    if found_row != None:
        for y in range(3):
            if y != found_row:
                for x in range(3):
                    remove_val(g, x, y, looking_for)

print()
rule_alligator_in_bottom_row(grid)
rule_duck_not_on_bottom(grid)
rule_fox_not_in_third_col(grid)
rule_iguana_is_in_corner(grid)
print_grid(grid, 'Cleared obvious rules')

def finished(g):
    for y in range(3):
        for x in range(3):
            if get_known(g, x, y) == None:
                return False
    return True

def apply_rules(g):
    try:
        rule_there_can_only_be_one(g)
        rule_no_alphabetical_neighbour(g)
        rule_no_two_vowels(g)
        rule_beaver_eagle_same_col(g)
        rule_cheetah_goat_same_row(g)
        return True
    except AssertionError:
        return False

def step(g, depth):
    print_grid(g, 'Depth: ' + str(depth), depth)
    if apply_rules(g) == False:
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
        new_g[pos(x, y)] = [v]
        result = step(new_g, depth+1)
        if result != None:
            return result
    return None

result = step(grid, 0)
assert(result != None)
print_grid(result, 'Found solution')