import os
import xml.etree.ElementTree as et
import wordsearch

def css_style():
    with open('%s/style.css' % (os.path.abspath(os.path.dirname(__file__))), mode='r', encoding='utf8') as f:
        style = f.read()
    return style

def create(height, width, words):
    puzzle, hints = wordsearch.pretty_puzzle(height, width, words)
    html = et.Element('html')
    head = et.Element('head')
    body = et.Element('body')
    style = et.Element('style')
    style.text = css_style()
    table = et.Element('table')
    header_row = True
    for row in puzzle:
        html_row = et.Element('tr')
        header_column = True
        for cell in row:
            html_cell = et.Element('th' if header_row or header_column else 'td')
            html_cell.text = cell
            html_row.append(html_cell)
            header_column = False
        table.append(html_row)
        header_row = False
    head.append(style)
    body.append(table)
    html.append(head)
    html.append(body)
    html = et.tostring(html)
    return html

result = create(4, 4, ['cat', 'dog', 'frog'])
with open('out.html', mode='wb') as f:
    f.write(result)
