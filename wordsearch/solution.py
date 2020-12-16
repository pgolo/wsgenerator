import copy
import random
import string

def placements(grid, word, grid_height, grid_width, points):
    #ys = list(range(grid_height))
    #xs = list(range(grid_width))
    #directions = [(0, 1), (1, 0), (1, -1), (1, 1)]
    while len(points) > 0:
        (x, y, direction) = points.pop()
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

def trace_grids(grid, words, word_index, grid_height, grid_width, www, points):
    word = words[word_index]
    while True:
        try:
            solution = next(placements(grid, word, grid_height, grid_width, points))
        except StopIteration:
            return []
        word_index += 1
        if word_index < len(words):
            temp = trace_grids(solution, words, word_index, grid_height, grid_width, www, points)
            if len(temp) > 0:
                return temp
        else:
            return solution

# words = [
#     'cow',
#     'goat',
#     'pig',
#     'buffalo',
#     'chicken',
#     'sheep',
#     'lamb',
#     'goose',
#     'turkey',
#     'duck'
#     'horse',
#     'cattle',
#     'llama',
#     'bison',
#     'hen',
#     'calf',
#     'rooster',
#     'bull',
#     'donkey',
#     'dog'
#     'geese',
#     'fish',
#     'deer',
#     'birds',
#     'bees',
#     'qwerty',
#     'uiop',
#     'asdfg',
#     'zxcvxc'
#     #'topyuytsdgfw'
# ]

words = [
    'aa',
    'bb',
    'cc',
    'dd'
]

grid_width = 3
grid_height = 3
grid = [['' for _ in range(grid_width)] for _ in range(grid_height)]

directions = [(0, 1), (1, 0), (1, -1), (1, 1)]
points = [item for sublist in [item for sublist in [[[(x, y, d) for x in range(grid_width)] for y in range(grid_height)] for d in directions] for item in sublist] for item in sublist]
#random.shuffle(points)

words.sort(key=lambda word: -len(word))

www = {}

solution = trace_grids(grid, words, 0, grid_height, grid_width, www, points)
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
