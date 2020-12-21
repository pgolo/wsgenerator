import random
import wordsearch

def create(height, width, words):
    puzzle, hints = wordsearch.pretty_puzzle(height, width, words)
    puzzle_js = '  <script type="text/javascript">\n'
    puzzle_js += '    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("width", "100%"); svg.setAttribute("height", "100%"); document.body.appendChild(svg);\n'
    puzzle_js += '    var grid = []; var letters = []; var buttons = [];\n'
    hints_js = '  <script type="text/javascript">\n'
    hints_js += '    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");\n'
    cell_size = 50
    font_size = 45
    words = [word for word in hints.keys()]
    random.shuffle(words)
    n = 0
    y = 0
    for row in puzzle:
        puzzle_js += '    grid.push([]); letters.push([]); buttons.push([]);\n'
        x = 0
        for cell in row:
            puzzle_js += '    grid[grid.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));\n'
            puzzle_js += '    grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("x", "%d");\n' % (x)
            puzzle_js += '    grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("y", "%d");\n' % (y)
            puzzle_js += '    grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("width", "%d");\n' % (cell_size)
            puzzle_js += '    grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("height", "%d");\n' % (cell_size)
            puzzle_js += '    grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("style", "fill:white;stroke:black;stroke-width:%dpx");\n' % (1 if x != 0 and y != 0 else 0)
            
            puzzle_js += '    letters[letters.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "text"));\n'
            puzzle_js += '    letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("x", "%d");\n' % (x + cell_size / 2)
            puzzle_js += '    letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("y", "%d");\n' % (y + cell_size  / 2)
            puzzle_js += '    letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("font-size", "%d");\n' % (font_size if x != 0 and y != 0 else font_size / 2)
            puzzle_js += '    letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("dominant-baseline", "middle");\n'
            puzzle_js += '    letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("text-anchor", "middle");\n'
            puzzle_js += '    letters[letters.length - 1][letters[letters.length - 1].length - 1].appendChild(document.createTextNode("%s"));\n' % (cell)
            
            puzzle_js += '    buttons[buttons.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));\n'
            puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("x", "%d");\n' % (x)
            puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("y", "%d");\n' % (y)
            puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("width", "%d");\n' % (cell_size)
            puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("height", "%d");\n' % (cell_size)
            puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("style", "fill:white;opacity:0%;stroke-width:0px");\n'
            
            if x != 0 and y != 0:
                puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseover", "evt.target.setAttribute(\'style\', \'fill:white;opacity:50%;stroke-width:0px\');");\n'
                puzzle_js += '    buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseout", "evt.target.setAttribute(\'style\', \'fill:white;opacity:0%;stroke-width:0px\');");\n'

            puzzle_js += '    svg.appendChild(grid[grid.length - 1][grid[grid.length - 1].length - 1]);\n'
            puzzle_js += '    svg.appendChild(letters[letters.length - 1][letters[letters.length - 1].length - 1]);\n'
            puzzle_js += '    svg.appendChild(buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1]);\n'
            x += cell_size
        y += cell_size
        n += 1
    puzzle_js += '  </script>\n'
    hints_js += '    document.body.appendChild(svg);\n'
    hints_js += '  </script>\n'
    return puzzle_js, hints_js

puzzle, hints = create(15, 15, ['cat', 'dog', 'frog', 'abc', 'def', 'qwe'])
with open('puzzle.html', mode='w', encoding='utf8') as f:
    f.write('<html>\n  <head>\n    <style type="text/css">body{-webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;}</style>\n  </head>\n  <body>\n%s  </body>\n</html>' % puzzle)
with open('cheatsheet.html', mode='w', encoding='utf8') as f:
    f.write('<html>\n  <head>\n    <style type="text/css">body{-webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;}</style>\n  </head>\n  <body>\n%s  </body>\n</html>' % hints)
