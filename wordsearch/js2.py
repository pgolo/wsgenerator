import random
import wordsearch

def create(height, width, words):
    puzzle, hints = wordsearch.pretty_puzzle(height, width, words)
    puzzle_js = '  <script type="text/javascript">\n'
    puzzle_js += '    var puzzle = %s;\n' % (str(puzzle).replace('\'', '"'))
    puzzle_js += '    var grid = []; var letters = []; var buttons = [];\n'
    puzzle_js += '    var x_margin = 1; var y_margin = 1;\n'
    puzzle_js += '    var x = x_margin; var y = y_margin;\n'
    puzzle_js += '    var cell_size = 1; var font_size = 0.8;\n'
    puzzle_js += '    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("width", (puzzle[0].length + 1) * cell_size + x_margin * 2 + "cm"); svg.setAttribute("height", (puzzle.length + 1) * cell_size + x_margin * 2 + "cm"); document.body.appendChild(svg);\n'

    hints_js = '  <script type="text/javascript">\n'
    hints_js += '    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");\n'
    puzzle_js += '    for (r = 0; r < puzzle.length; r++) {\n'
    puzzle_js += '      x = x_margin;\n'
    puzzle_js += '      grid.push([]); letters.push([]); buttons.push([]);\n'
    puzzle_js += '      for (c = 0; c < puzzle[r].length; c++) {\n'

    puzzle_js += '        grid[grid.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));\n'
    puzzle_js += '        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("x", x + "cm");\n'
    puzzle_js += '        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("y", y + "cm");\n'
    puzzle_js += '        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("width", cell_size + "cm");\n'
    puzzle_js += '        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("height", cell_size + "cm");\n'
    puzzle_js += '        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("shape-rendering", "crispEdges");\n'
    puzzle_js += '        if (r * c != 0) {\n'
    puzzle_js += '          grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("style", "fill:white;stroke:black;stroke-width:1px");\n'
    puzzle_js += '        } else {\n'
    puzzle_js += '          grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("style", "fill:white;stroke:black;stroke-width:0px");\n'
    puzzle_js += '        }\n'
    
    puzzle_js += '        letters[letters.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "text"));\n'
    puzzle_js += '        letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("x", x + cell_size / 2 + "cm");\n'
    puzzle_js += '        letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("y", y + cell_size / 2 + "cm");\n'
    puzzle_js += '        if (r * c != 0) {\n'
    puzzle_js += '          letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("font-size", font_size + "cm");\n'
    puzzle_js += '        } else {\n'
    puzzle_js += '          letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("font-size", font_size / 2 + "cm");\n'
    puzzle_js += '        }\n'
    puzzle_js += '        letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("dominant-baseline", "middle");\n'
    puzzle_js += '        letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("text-anchor", "middle");\n'
    puzzle_js += '        letters[letters.length - 1][letters[letters.length - 1].length - 1].appendChild(document.createTextNode(puzzle[r][c]));\n'

    puzzle_js += '        buttons[buttons.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));\n'
    puzzle_js += '        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("x", x + "cm");\n'
    puzzle_js += '        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("y", y + "cm");\n'
    puzzle_js += '        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("width", cell_size + "cm");\n'
    puzzle_js += '        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("height", cell_size + "cm");\n'
    puzzle_js += '        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("style", "fill:white;opacity:0%;stroke-width:0px");\n'

    puzzle_js += '        if (r * c != 0) {\n'
    puzzle_js += '          buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseover", "evt.target.setAttribute(\'style\', \'fill:white;opacity:50%;stroke-width:0px\');");\n'
    puzzle_js += '          buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseout", "evt.target.setAttribute(\'style\', \'fill:white;opacity:0%;stroke-width:0px\');");\n'
    puzzle_js += '          buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmousedown", "alert(\'" + puzzle[r][c] + "\');");\n'
    puzzle_js += '        }\n'

    puzzle_js += '        svg.appendChild(grid[grid.length - 1][grid[grid.length - 1].length - 1]);\n'
    puzzle_js += '        svg.appendChild(letters[letters.length - 1][letters[letters.length - 1].length - 1]);\n'
    puzzle_js += '        svg.appendChild(buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1]);\n'

    puzzle_js += '        x += cell_size;\n'
    puzzle_js += '      }\n'
    puzzle_js += '      y += cell_size;\n'
    puzzle_js += '    }\n'

    puzzle_js += '    var frame = document.createElementNS("http://www.w3.org/2000/svg", "rect");\n'
    puzzle_js += '    frame.setAttribute("width", (puzzle[0].length + 1) * cell_size + x_margin * 2 + "cm");\n'
    puzzle_js += '    frame.setAttribute("height", (puzzle.length + 1) * cell_size + x_margin * 2 + "cm");\n'
    puzzle_js += '    frame.setAttribute("style", "fill:none;stroke:black;stroke-width:1px");\n'
    puzzle_js += '    frame.setAttribute("rx", "10");\n'
    puzzle_js += '    frame.setAttribute("ry", "10");\n'
    puzzle_js += '    svg.appendChild(frame);\n'

    puzzle_js += '  </script>\n'
    hints_js += '    document.body.appendChild(svg);\n'
    hints_js += '  </script>\n'
    return puzzle_js, hints_js

puzzle, hints = create(15, 15, ['Maryland', 'Virginia', 'Vermont', 'Monatna', 'Delaware', 'Alabama', 'Alaska', 'Hawaii', 'Arizona', 'California', 'Texas', 'Indiana'])
with open('puzzle.html', mode='w', encoding='utf8') as f:
    f.write('<html>\n  <head>\n    <style type="text/css">body{-webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;}</style>\n  </head>\n  <body>\n%s  </body>\n</html>' % puzzle)
with open('cheatsheet.html', mode='w', encoding='utf8') as f:
    f.write('<html>\n  <head>\n    <style type="text/css">body{-webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;}</style>\n  </head>\n  <body>\n%s  </body>\n</html>' % hints)
