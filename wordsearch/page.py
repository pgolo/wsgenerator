import random
import wordsearch

def create(height, width, words):
    puzzle, hints = wordsearch.pretty_puzzle(height, width, words)
    puzzle_code = ''
    with open('wordsearch/game.html', mode='r', encoding='utf8') as f:
        puzzle_code = f.read().replace('$words', str(list(hints.keys())).replace('\'', '"')).replace('$puzzle', str(puzzle).replace('\'', '"'))
    return puzzle_code

puzzle = create(15, 15, ['Maryland', 'Virginia', 'Vermont', 'Monatna', 'Delaware', 'Alabama', 'Alaska', 'Hawaii', 'Arizona', 'California', 'Texas', 'Indiana'])
with open('puzzle.html', mode='w', encoding='utf8') as f:
    f.write(puzzle)
