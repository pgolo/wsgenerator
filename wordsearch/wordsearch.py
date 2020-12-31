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
            return solution, y, x, direction, letters
    return [], None, None, None, None

def trace_grids(grid, words, word_index, grid_height, grid_width, hints, points):
    word = words[word_index]
    _words = [word, ''.join(reversed(word))]
    _points = [point for point in points if grid[point[1]][point[0]] != '#']
    random.shuffle(_words)
    random.shuffle(_points)
    while True:
        solution, y, x, direction, letters = placements(grid, _words, grid_height, grid_width, _points)
        if solution:
            hints[word] = (y, x, direction, letters)
        else:
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

def make_puzzle(height, width, words, grid):
    directions = [(0, 1), (1, 0), (1, -1), (1, 1)]
    points = [
        item for sublist in [
            item for sublist in [
                [
                    [
                        (x, y, d) for x in range(width)
                    ] for y in range(height)
                ] for d in directions
            ] for item in sublist
        ] for item in sublist
    ]
    hints = {}
    words = sorted(words, key=lambda word: -len(word))
    solution, _, _, _, _ = trace_grids(grid, words, 0, height, width, hints, points)
    for row in solution:
        for i in range(len(row)):
            if row[i] == '':
                row[i] = random.choice(string.ascii_letters) # ' '
            row[i] = row[i].upper()
    return solution, hints

def check_template(c):
    assert c in [' ', '.', '#'], 'Only "." or "#" characters are allowed in template'
    return {' ': '#', '.': '#', '#': ''}[c]

def pretty_puzzle(*args, **kwargs):
    words = []
    if 'words' in kwargs:
        words = list(kwargs['words'])
    words += list(args)
    grid = None
    height = None
    width = None
    if 'grid' in kwargs:
        grid = kwargs['grid']
    if 'template' in kwargs:
        grid = [[check_template(cell) for cell in row] for row in kwargs['template'].strip('\n').split('\n')]
        max_length = max([len(row) for row in grid])
        for i in range(0, len(grid)):
            diff = max_length - len(grid[i])
            if diff <= 0:
                continue
            grid[i] += ['#'] * diff
    if grid is not None:
        height = len(grid)
        width = len(grid[0])
    if 'height' in kwargs:
        height = kwargs['height']
    if 'width' in kwargs:
        width = kwargs['width']
    assert len(words) > 0, 'No words to process'
    assert grid is not None or (height is not None and width is not None), 'Grid paremeters are not specified'
    if grid is None:
        grid = [['' for _ in range(width)] for _ in range(height)]
    puzzle, hints = make_puzzle(height, width, words, grid)
    if len(puzzle) == 0:
        return [], {}
    _pretty_puzzle = []
    _pretty_puzzle.append([' '] + ['%d' % (column_number + 1) for column_number in range(len(puzzle[0]))])
    row_number = 0
    for row in puzzle:
        row_number += 1
        _pretty_puzzle.append(['%d' % (row_number)] + row)
    _pretty_hints = translate_hints(hints)
    return _pretty_puzzle, _pretty_hints
