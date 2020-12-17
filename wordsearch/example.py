import wordsearch

words = [
    'cow',
    'goat',
    'pig',
    'buffalo',
    'chicken',
    'sheep',
    'lamb',
    'goose',
    'turkey',
    'duck'
    'horse',
    'cattle',
    'llama',
    'bison',
    'hen',
    'calf',
    'rooster',
    'bull',
    'donkey',
    'dog'
    'geese',
    'fish',
    'deer',
    'birds',
    'bees',
    'qwerty',
    'uiop',
    'asdfg',
    'zxcvxc',
    'topyuytsdgfwqqq'
]

# words = [
#     'e',
#     'aaa',
#     'bb',
#     'c',
#     'dd'
# ]

puzzle, hints = wordsearch.pretty_puzzle(15, 15, words)
for row in puzzle:
    print(row)
for word in hints:
    print(word, hints[word])
