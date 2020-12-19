import random
import wordsearch

def create(height, width, words):
    puzzle, hints = wordsearch.pretty_puzzle(height, width, words)
    puzzle_svg = '<svg>\n'
    puzzle_svg += '  <rect x="0" y="0" width="100%" height="100%" style="fill:white" />\n'
    hints_svg = '<svg>\n'
    hints_svg += '  <rect x="0" y="0" width="100%" height="100%" style="fill:white" />\n'
    cell_size = 50
    font_size = 45
    letter_offset = 8
    words = [word for word in hints.keys()]
    random.shuffle(words)
    n = 0
    y = 0
    for row in puzzle:
        x = 0
        for cell in row:
            puzzle_svg += '  <rect x="%d" y="%d" width="%d" height="%d" style="fill:white;stroke:black;stroke-width:%dpx" />\n' % (x, y, cell_size, cell_size, 1 if x != 0 and y != 0 else 0)
            puzzle_svg += '  <text x="%d" y="%d" font-size="%d">%s</text>\n' % (x + letter_offset, y + cell_size - letter_offset, font_size if x != 0 and y != 0 else font_size / 2, cell)
            x += cell_size
        if n < len(words):
            puzzle_svg += '  <text x="%d" y="%d" font-size="%d">%s</text>\n' % (x + cell_size, y + cell_size - letter_offset, font_size, words[n].upper())
            hints_svg += '  <text x="0" y="%d" font-size="%d">%s: row %d, column %d, direction %s</text>\n' % (y + cell_size - letter_offset, font_size, words[n].upper(), hints[words[n]]['row'], hints[words[n]]['column'], hints[words[n]]['direction'])
        y += cell_size
        n += 1
    while n < len(words):
        puzzle_svg += '  <text x="%d" y="%d" font-size="%d">%s</text>\n' % (x + cell_size, y + cell_size - letter_offset, cell_size, words[n].upper())
        n += 1
    puzzle_svg += '</svg>\n'
    hints_svg += '</svg>\n'
    return puzzle_svg, hints_svg

puzzle, hints = create(4, 4, ['cat', 'dog', 'frog', 'abc', 'def', 'qwe'])
with open('puzzle.svg', mode='w', encoding='utf8') as f:
    f.write(puzzle)
with open('cheatsheet.svg', mode='w', encoding='utf8') as f:
    f.write(hints)
