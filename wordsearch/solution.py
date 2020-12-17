import copy
import random
import string

def placements(grid, words, grid_height, grid_width, points):
    while len(points) > 0:
        (x, y, direction) = points.pop()
        for letters in words:
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
            yield solution, y, x, direction, letters

def trace_grids(grid, words, word_index, grid_height, grid_width, hints, points):
    word = words[word_index]
    _words = [word, ''.join(reversed(word))]
    _points = list(points)
    random.shuffle(_words)
    random.shuffle(_points)
    while True:
        try:
            solution, y, x, direction, letters = next(placements(grid, _words, grid_height, grid_width, _points))
            hints[word] = (y, x, direction, letters)
        except StopIteration:
            return [], None, None, None, None
        if word_index < len(words) - 1:
            temp, _, _, _, _ = trace_grids(solution, words, word_index + 1, grid_height, grid_width, hints, points)
            if len(temp) > 0:
                return temp, None, None, None, None
            del hints[word]
        else:
            return solution, None, None, None, None

def translate_hints(hints):
    solution = {}
    directions = {
        (0, 1): ('L->R', 'R->L'),
        (1, 0): ('U->D', 'D->U'),
        (1, -1): ('UR->DL', 'DL->UR'),
        (1, 1): ('UL->DR', 'DR->UL')
    }
    for word in hints:
        (y, x, direction, letters) = hints[word]
        assert word == letters or word == ''.join(reversed(letters))
        order = 0
        if word != letters:
            y += direction[0] * (len(word) - 1)
            x += direction[1] * (len(word) - 1)
            order = 1
        direction_hint = directions[direction][order]
        x += 1
        y += 1
        solution[word] = {'row': y, 'column': x, 'direction': direction_hint}
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
    'zxcvxc',
    'topyuytsdgfwqqq'
]

# words = [
#     'e',
#     'aaa',
#     'bb',
#     'c',
#     'dd'
# ]

grid_width = 15
grid_height = 15
grid = [['' for _ in range(grid_width)] for _ in range(grid_height)]

directions = [(0, 1), (1, 0), (1, -1), (1, 1)]
points = [item for sublist in [item for sublist in [[[(x, y, d) for x in range(grid_width)] for y in range(grid_height)] for d in directions] for item in sublist] for item in sublist]

words.sort(key=lambda word: -len(word))

hints = {}

solution, _, _, _, _ = trace_grids(grid, words, 0, grid_height, grid_width, hints, points)
for row in solution:
    for i in range(len(row)):
        if row[i] == '':
            #row[i] = random.choice(string.ascii_letters)
            row[i] = ' '
        row[i] = row[i].upper()

header_row = [' '] + ['%d' % (column_number + 1) for column_number in range(len(solution[0]))]
print(header_row)
row_number = 0
for row in solution:
    row_number += 1
    printed_row = ['%d' % (row_number)] + row
    print(printed_row)
print('---')
translated_hints = translate_hints(hints)
for word in translated_hints:
    print(word, translated_hints[word])

print('---')
