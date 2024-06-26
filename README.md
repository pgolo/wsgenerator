# wsgenerator
Word search puzzle generator

Usage:

```python
import wsgenerator

puzzle, solution = wsgenerator.pretty_puzzle('car', 'bicycle', 'airplane', 'bus', height=8, width=8, level=0)
for row in puzzle:
    print(row)
for word in solution:
    print(word, solution[word])

# [' ', '1', '2', '3', '4', '5', '6', '7', '8']
# ['1', 'U', 'B', 'J', 'J', 'C', 'Z', 'E', 'K']
# ['2', 'P', 'L', 'U', 'C', 'S', 'A', 'Y', 'I']
# ['3', 'J', 'P', 'G', 'S', 'R', 'Q', 'R', 'U']
# ['4', 'H', 'N', 'A', 'K', 'E', 'R', 'S', 'M']
# ['5', 'M', 'S', 'M', 'P', 'X', 'S', 'X', 'A']
# ['6', 'P', 'B', 'I', 'C', 'Y', 'C', 'L', 'E']
# ['7', 'A', 'I', 'R', 'P', 'L', 'A', 'N', 'E']
# ['8', 'R', 'M', 'P', 'B', 'N', 'N', 'K', 'V']
# AIRPLANE {'y1': 7, 'x1': 1, 'y2': 7, 'x2': 8, 'direction': 'L->R'}
# BICYCLE {'y1': 6, 'x1': 2, 'y2': 6, 'x2': 8, 'direction': 'L->R'}
# CAR {'y1': 1, 'x1': 5, 'y2': 3, 'x2': 7, 'direction': 'UL->DR'}
# BUS {'y1': 1, 'x1': 2, 'y2': 3, 'x2': 4, 'direction': 'UL->DR'}

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

# [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
# ['1', '#', '#', '#', '#', '#', 'W', '#', '#', '#', '#', '#']
# ['2', '#', '#', '#', '#', 'Y', 'B', 'A', '#', '#', '#', '#']
# ['3', '#', '#', '#', 'M', 'R', 'C', 'I', 'J', '#', '#', '#']
# ['4', '#', '#', 'C', 'R', 'E', 'N', 'R', 'A', 'K', '#', '#']
# ['5', '#', 'V', 'Q', 'A', 'G', 'K', 'P', 'U', 'T', 'H', '#']
# ['6', 'Q', 'G', 'B', 'O', 'R', 'E', 'L', 'O', 'M', 'K', 'A']
# ['7', '#', 'W', 'M', 'K', 'H', 'T', 'A', 'A', 'O', 'J', '#']
# ['8', '#', '#', 'T', 'R', 'A', 'I', 'N', 'T', 'D', '#', '#']
# ['9', '#', '#', '#', 'G', 'R', 'B', 'E', 'A', '#', '#', '#']
# ['10', '#', '#', '#', '#', 'V', 'U', 'Y', '#', '#', '#', '#']
# ['11', '#', '#', '#', '#', '#', 'S', '#', '#', '#', '#', '#']
# AIRPLANE {'y1': 2, 'x1': 7, 'y2': 9, 'x2': 7, 'direction': 'U->D'}
# TRAIN {'y1': 8, 'x1': 3, 'y2': 8, 'x2': 7, 'direction': 'L->R'}
# CAR {'y1': 4, 'x1': 3, 'y2': 6, 'x2': 5, 'direction': 'UL->DR'}
# BUS {'y1': 9, 'x1': 6, 'y2': 11, 'x2': 6, 'direction': 'U->D'}
