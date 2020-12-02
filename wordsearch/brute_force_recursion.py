import copy

def placements(grid, word):
    solutions = []
    grid_height = len(grid)
    grid_width = len(grid[0])
    for y in range(grid_height):
        for x in range(grid_width):
            for direction in [(0, 1), (1, 0), (1, -1)]:
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
    return solutions

# recursion:
def trace_grids(solutions, words, word_index):
    word = words[word_index]
    partial_solutions = []
    for grid in solutions:
        fits = placements(grid, word)
        partial_solutions += fits
    word_index += 1
    if word_index == len(words):
        return partial_solutions
    return trace_grids(partial_solutions, words, word_index)

grid_width = 5
grid_height = 5
grid = [['' for _ in range(grid_width)] for _ in range(grid_height)]

words = ['qwer', 'rws', 'wow']

words.sort(key=lambda word: -len(word))
grids = [grid]
solutions = trace_grids(grids, words, 0)

for grid in solutions:
    for row in grid:
        print(row)
    print('---')

print(len(solutions))
