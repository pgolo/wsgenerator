import os
import xml.etree.ElementTree as et
import wordsearch

def css_style():
    with open('%s/style.css' % (os.path.abspath(os.path.dirname(__file__))), mode='r', encoding='utf8') as f:
        style = f.read()
    return style

def create(height, width, words):
    # generate puzzle
    puzzle, hints = wordsearch.pretty_puzzle(height, width, words)

    # elements
    html = et.Element('html')
    head = et.Element('head')
    body = et.Element('body')
    style = et.Element('style')
    style.text = css_style()
    puzzle_caption = et.Element('h1')
    puzzle_table = et.Element('table')
    legend_caption = et.Element('h1')
    legend_table = et.Element('table')

    # add the content

    # puzzle caption
    puzzle_caption.text = 'Puzzle'

    # legend caption
    legend_caption.text = 'Legend'

    # puzzle
    header_row = True
    for row in puzzle:
        html_row = et.Element('tr')
        header_column = True
        for cell in row:
            html_cell = et.Element('th' if header_row or header_column else 'td')
            html_cell.text = cell
            html_row.append(html_cell)
            header_column = False
        puzzle_table.append(html_row)
        header_row = False
    
    # legend
    legend = [[]]
    legend_columns = 3
    n = 0
    for word in hints:
        legend[-1].append(word)
        n += 1
        if n % legend_columns == 0:
            legend.append([])
    if len(legend[-1]) == 0:
        legend = legend[:-1]
    legend[-1] += [''] * (len(legend[0]) - len(legend[-1]))
    for row in legend:
        html_row = et.Element('tr')
        for cell in row:
            html_cell = et.Element('td')
            html_cell.text = cell
            html_row.append(html_cell)
        legend_table.append(html_row)
    
    # render all
    head.append(style)
    body.append(puzzle_caption)
    body.append(puzzle_table)
    body.append(legend_caption)
    body.append(legend_table)
    html.append(head)
    html.append(body)
    html = et.tostring(html)
    return html

result = create(4, 4, ['cat', 'dog', 'frog', 'abc', 'def'])
with open('puzzle.html', mode='wb') as f:
    f.write(result)
