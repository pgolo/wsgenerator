import random
import wordsearch

def create(*args, **kwargs):
    puzzle, hints = wordsearch.pretty_puzzle(*args, **kwargs)
    wordbank = list(hints.keys())
    random.shuffle(wordbank)
    puzzle_code = ''
    with open('wordsearch/game.html', mode='r', encoding='utf8') as f:
        #puzzle_code = f.read().replace('$solution', '{}').replace('$words', str(wordbank).replace('\'', '"')).replace('$puzzle', str(puzzle).replace('\'', '"')).replace('$solution', str(hints).replace('\'', '"'))
        puzzle_code = f.read().replace('$words', str(wordbank).replace('\'', '"')).replace('$puzzle', str(puzzle).replace('\'', '"')).replace('$solution', str(hints).replace('\'', '"'))
    return puzzle_code

z = '''
###
  #
  #
  #
  #
   #
    #
     #
     #
     #
   ###
'''
#puzzle = create('aaa', 'bbb', 'ccc', words=['ddd', 'eee'], template=z)
puzzle = create(height=15, width=15, words=['Maryland', 'Virginia', 'Vermont', 'Montana', 'Delaware', 'Alabama', 'Alaska', 'Hawaii', 'Arizona', 'California', 'Texas', 'Indiana', 'Illinois', 'Minnesota', 'Wisconsin', 'Ohio', 'Nebraska', 'Iowa', 'Kentucky', 'Kansas', 'Florida', 'Arkansas'])
with open('puzzle.html', mode='w', encoding='utf8') as f:
    f.write(puzzle)
