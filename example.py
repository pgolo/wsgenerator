import wsgenerator

puzzle, solution = wsgenerator.pretty_puzzle('car', 'bicycle', 'airplane', 'bus', height=8, width=8, level=0)
for row in puzzle:
    print(row)
for word in solution:
    print(word, solution[word])

template = '''
.....#.....
....###....
...#####...
..#######..
.#########.
###########
.#########.
..#######..
...#####...
....###....
.....#.....
'''
puzzle, solution = wsgenerator.pretty_puzzle('car', 'train', 'airplane', 'bus', template=template, level=0)
for row in puzzle:
    print(row)
for word in solution:
    print(word, solution[word])
