import copy
import random
import string

def placements(grid, word):
    grid_height = len(grid)
    grid_width = len(grid[0])
    ys = list(range(grid_height))
    xs = list(range(grid_width))
    directions = [(0, 1), (1, 0), (1, -1), (1, 1)]
    random.shuffle(ys)
    random.shuffle(xs)
    random.shuffle(directions)
    for y in ys:
        for x in xs:
            for direction in [(0, 1), (1, 0), (1, -1), (1, 1)]:
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
                    if not_fit:
                        continue
                    yield solution

def trace_grids(grid, words, word_index):
    word = words[word_index]
    try:
        solution = next(placements(grid, word))
    except StopIteration:
        return [] # <-- TODO: instead of giving up, fall back
    word_index += 1
    if word_index < len(words):
        return trace_grids(solution, words, word_index)
    else:
        return solution


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

words.sort(key=lambda word: -len(word))
solution = trace_grids(grid, words, 0)
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
