import copy
import random
import string

def placements(grid, word, ys, xs, directions):
    visited = set()
    for y in ys:
        for x in xs:
            for direction in directions:
                for letters in [word, ''.join(reversed(word))]:
                    not_fit = False
                    solution = copy.deepcopy(grid)
                    for i in range(len(letters)):
                        this_y = y + i * direction[0]
                        this_x = x + i * direction[1]
                        if not (0 <= this_y < grid_height and 0 <= this_x < grid_width) or (grid[this_y][this_x] != '' and grid[this_y][this_x] != letters[i]):
                            not_fit = True
                            break
                        solution[this_y][this_x] = letters[i]
                    visited.add((y, x))
                    if not_fit:
                        continue
                    yield solution, visited

def trace_grids(grid, words, word_index, grid_height, grid_width, ys, xs, directions):
    word = words[word_index]
    try:
        solution, visited = next(placements(grid, word, ys, xs, directions))
    except StopIteration:
        return [], set()
    word_index += 1
    if word_index < len(words):
        _ys = list(ys)
        _xs = list(xs)
        _directions = list(directions)
        random.shuffle(_ys)
        random.shuffle(_xs)
        random.shuffle(_directions)
        while True:
            q, visited = trace_grids(solution, words, word_index, grid_height, grid_width, _ys, _xs, _directions)
            for ccc in visited:
                if ccc[0] in _ys:
                    _ys.remove(ccc[0])
                if ccc[1] in _xs:
                    _xs.remove(ccc[1])
            visited.clear()
            if q is not None and len(q) > 0:
                return q, visited
    else:
        return solution, visited


words = [
    'cow',
    'goat',
    'pig',
    'buffalo',
    'chicken',
    'sheep',
    'lamb',
    'goose',
    'turkey',
    'duck'
    'horse',
    'cattle',
    'llama',
    'bison',
    'hen',
    'calf',
    'rooster',
    'bull',
    'donkey',
    'dog'
    'geese',
    'fish',
    'deer',
    'birds',
    'bees',
    'qwerty',
    'uiop',
    'asdfg',
    'zxcvxc'
    #'topyuytsdgfwewq'
]

grid_width = 12
grid_height = 12
grid = [['' for _ in range(grid_width)] for _ in range(grid_height)]

ys = list(range(grid_height))
xs = list(range(grid_width))
directions = [(0, 1), (1, 0), (1, -1), (1, 1)]


words.sort(key=lambda word: -len(word))

solution, _ = trace_grids(grid, words, 0, grid_height, grid_width, ys, xs, directions)
for row in solution:
    for i in range(len(row)):
        if row[i] == '':
            #row[i] = random.choice(string.ascii_letters)
            row[i] = ' '
        row[i] = row[i].upper()

for row in solution:
    print(row)
print('---')

print(len(solution))
