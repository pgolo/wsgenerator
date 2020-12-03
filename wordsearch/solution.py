import copy
import random
import string

def placements(grid, word):
    solutions = []
    grid_height = len(grid)
    grid_width = len(grid[0])
    for y in range(grid_height):
        for x in range(grid_width):
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
                    solutions.append(solution)
    random.shuffle(solutions)
    return solutions

def trace_grids(grids, words, word_index):
    word = words[word_index]
    solutions = []
    ret = []
    for grid in grids:
        fits = placements(grid, word)
        solutions += fits
    word_index += 1
    if word_index < len(words):
        random.shuffle(solutions)
        for i in range(0, len(solutions)):
            ret = trace_grids([solutions[i]], words, word_index)
            if len(ret) > 0:
                break
        return ret
    else:
        return solutions

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
    'zxcvxc',
    'topyuytsdgfwewq'
]

grid_width = 15
grid_height = 15
grid = [['' for _ in range(grid_width)] for _ in range(grid_height)]

words.sort(key=lambda word: -len(word))
grids = [grid]
solutions = trace_grids(grids, words, 0)
if len(solutions) > 0:
    solution = solutions[random.randint(0, len(solutions)-1)]
    for row in solution:
        for i in range(len(row)):
            if row[i] == '':
                #row[i] = random.choice(string.ascii_letters)
                row[i] = ' '
            row[i] = row[i].upper()

    for row in solution:
        print(row)
    print('---')

    print(len(solutions))
