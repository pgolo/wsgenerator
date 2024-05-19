import copy
import random
import string

def placements(grid: list, words: list, grid_height: int, grid_width: int, points: list):
    """
    This function attempts to fit any item of "words" (list of strings)
    in a "grid" (list of lists of strings) with dimensions of ("grid_width", "grid_height")
    laying word out at the location ("x", "y") moving towards "direction"
    defined in next item of "points" (list of tuples: ("x", "y", "direction")).
    """
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

def trace_grids(grid: list, words: list, word_index: int, grid_height: int, grid_width: int, hints: dict, points: list, level: int=0):
    """
    This function attempts to recursively fit each item of "words" (list of strings)
    in a "grid" (list of lists) with dimensions of ("grid_width", "grid_height").

    "word_index" (integer): index of current element in "words".
    "hints" (dict): pointer to object to store the answer key.
    "points" (list): list of tuples ("x", "y", "d") representing each cell of the grid ("x", "y")
        and direction "d" (tuple ("dy", "dx")) in which a word can be layed out
    "level" (integer): percepted difficulty:
        0 (easy): word can only be placed horizontally left->right, vertically up->down, diagonally up->down-left, and diagonally up->down-right;
        1 (normal): words will be mostly placed horizontally left->right, vertically up->down, diagonally up->down-left, and diagonally up->down-right,
            but sometimes they will be also placed reversed (right->left, down->up, down->up-left, down->up-right);
        2 (hard): words will be mostly placed reversed (right->left, down->up, down->up-left, down->up-right),
            but sometimes they will be also placed in more convenient way (left->right, up->down, up->down-left, up->down-right);
        3 (insane): words can only be placed reversed (right->left, down->up, down->up-left, down->up-right).
    """
    word = words[word_index]
    reversed_word = ''.join(reversed(word))
    _words = {
        0: [word],
        1: [word, reversed_word],
        2: [reversed_word, word],
        3: [reversed_word]
    }[level]
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

def make_puzzle(height: int, width: int, words: list, grid: list, level: int=0):
    """
    This function generates word search puzzle.

    "height" (integer): height of the grid.
    "width" (integer): width of the grid.
    "words" (list): list of words to fit in the grid.
    "grid" (list): list of lists representing the grid to be filled with letters.
        Grid must have dimensions of ("width", "height")
    "level" (integer): percepted difficulty:
        0 (easy): word can only be placed horizontally left->right, vertically up->down, diagonally up->down-left, and diagonally up->down-right;
        1 (normal): words will be mostly placed horizontally left->right, vertically up->down, diagonally up->down-left, and diagonally up->down-right,
            but sometimes they will be also placed reversed (right->left, down->up, down->up-left, down->up-right);
        2 (hard): words will be mostly placed reversed (right->left, down->up, down->up-left, down->up-right),
            but sometimes they will be also placed in more convenient way (left->right, up->down, up->down-left, up->down-right);
        3 (insane): words can only be placed reversed (right->left, down->up, down->up-left, down->up-right).
    """
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
    solution, _, _, _, _ = trace_grids(grid, words, 0, height, width, hints, points, level)
    for row in solution:
        for i in range(len(row)):
            if row[i] == '':
                row[i] = random.choice(string.ascii_letters) # ' '
            row[i] = row[i].upper()
    return solution, hints

def translate_hints(hints: dict):
    """
    This function translates "hints" (dict) into readable answer key for a puzzle,
    and returns it as a dict object.
    """
    solution = {}
    directions = {
        (0, 1): ('L->R', 'R->L'),
        (1, 0): ('U->D', 'D->U'),
        (1, -1): ('UR->DL', 'DL->UR'),
        (1, 1): ('UL->DR', 'DR->UL')
    }
    for word in hints:
        (y1, x1, direction, letters) = hints[word]
        assert word == letters or word == ''.join(reversed(letters))
        order = 0
        if word != letters:
            y1 += direction[0] * (len(word) - 1)
            x1 += direction[1] * (len(word) - 1)
            order = 1
        direction_hint = directions[direction][order]
        y1 += 1
        y2 = y1 + direction[0] * (len(word) - 1) * (1 if order == 0 else -1)
        x1 += 1
        x2 = x1 + direction[1] * (len(word) - 1) * (1 if order == 0 else -1)
        solution[word.upper()] = {'y1': y1, 'x1': x1, 'y2': y2, 'x2': x2, 'direction': direction_hint}
    return solution

def check_template(c):
    """
    This function asserts that passed character is allowed in a template of a word search puzzle
    """
    assert c in [' ', '.', '#'], 'Only "." or "#" characters are allowed in template'
    return {' ': '#', '.': '#', '#': ''}[c]

def pretty_puzzle(*args, **kwargs):
    """
    This function generates a word search puzzle and an answer key for it.

    "*args": list of words to fit in the puzzle (required).
    "*kwargs": parameters of the puzzle:
        "height" (integer): height of the grid (required in "grid" is not provided);
        "width" (integer): width of the grid (required if "grid" is not provided);
        "grid" (list): list of lists representing the grid to fill (required if "width" and "height" are not provided);
        "template" (string): template for the grid (optional).
    If both "height" and "width" AND "grid" parameters are provided,
        then "grid" is expected to have dimensions of ("width", "height").
    "template" is a multi-line string containing characters "#" and ".".
        Character "#" represents a cell where a letter can be placed.
        Character "." represents a cell where a letter cannot be placed.
    """
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
