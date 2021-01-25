from flask import Flask, request, Response, render_template, jsonify, json
import random
import os
import sqlite3
import wordsearch

app = Flask(__name__)

def get_simple_args(rqst):
    return json.loads(rqst.args['height']), json.loads(rqst.args['width']), json.loads(rqst.args['words']).split(' '), json.loads(rqst.args['title'])

def get_fancy_args(rqst):
    data = rqst.form
    return data['template'], data['words'].split(' '), data['title']

def generate_puzzle(**kwargs):
    if 'template' in kwargs:
        assert 'words' in kwargs
        assert 'title' in kwargs
        puzzle, solution = wordsearch.pretty_puzzle(template=kwargs['template'], words=kwargs['words'])
    else:
        assert 'height' in kwargs
        assert 'width' in kwargs
        assert 'words' in kwargs
        assert 'title' in kwargs
        puzzle, solution = wordsearch.pretty_puzzle(height=kwargs['height'], width=kwargs['width'], words=kwargs['words'])
    wordbank = list(solution.keys())
    random.shuffle(wordbank)
    title = kwargs['title']
    out = {'words': wordbank, 'puzzle': puzzle, 'solution': solution, 'title': title}
    return out, wordbank, puzzle, solution

@app.route('/api/instant/simple', methods=['GET'])
def get_simple_puzzle():
    global conn
    global cur
    height, width, words, title = get_simple_args(request)
    out, wordbank, puzzle, solution = generate_puzzle(height=height, width=width, words=words, title=title)
    cur.execute('insert into puzzles (title, words, puzzle, solution) select ?, ?, ?, ?;', (title, str(wordbank), str(puzzle), str(solution)))
    conn.commit()
    if 'page' in request.args:
        return render_template('puzzle.html', words=wordbank, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false')
    return jsonify(out)

@app.route('/api/instant/fancy', methods=['POST', 'GET'])
def get_fancy_puzzle():
    global conn
    global cur
    template, words, title = get_fancy_args(request)
    out, wordbank, puzzle, solution = generate_puzzle(template=template, words=words, title=title)
    cur.execute('insert into puzzles (title, words, puzzle, solution) select ?, ?, ?, ?;', (title, str(wordbank), str(puzzle), str(solution)))
    conn.commit()
    if 'page' in request.args:
        return render_template('puzzle.html', words=wordbank, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false')
    return jsonify(out)

@app.route('/api/saved/page', methods=['GET'])
def get_puzzle_by_id():
    global conn
    global cur
    _id = json.loads(request.args['id'])
    cur.execute('select title, words, puzzle, solution from puzzles where rowid = %d;' % (_id))
    row = cur.fetchone()
    title, words, puzzle, solution = row[0], row[1], row[2], row[3]
    return render_template('puzzle.html', words=words, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false')

@app.route('/')
def get_random_puzzle():
    global conn
    global cur
    cur.execute('select title, words, puzzle, solution from puzzles order by random() limit 1;')
    row = cur.fetchone()
    title, words, puzzle, solution = row[0], row[1], row[2], row[3]
    return render_template('puzzle.html', words=words, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false')

if __name__ == '__main__':
    create_schema = True
    if os.path.exists('wordsearch.db'):
        create_schema = False
    conn = sqlite3.connect('wordsearch.db', check_same_thread=False)
    cur = conn.cursor()
    if create_schema:
        cur.execute('create table puzzles (title text, words text, puzzle text, solution text);')
        title = 'Across the United States'
        wordbank = '["ALASKA", "VERMONT", "ILLINOIS", "KANSAS", "ARIZONA", "TEXAS", "HAWAII", "KENTUCKY", "ALABAMA", "IOWA", "CALIFORNIA", "MONTANA", "NEBRASKA", "VIRGINIA", "DELAWARE", "MARYLAND", "INDIANA", "WISCONSIN", "MINNESOTA", "FLORIDA", "OHIO"]'
        puzzle = '[[" ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], ["1", "V", "L", "D", "S", "Z", "F", "B", "A", "L", "A", "B", "A", "M", "A", "G"], ["2", "H", "K", "V", "I", "A", "N", "A", "T", "N", "O", "M", "X", "P", "T", "M"], ["3", "B", "C", "A", "L", "I", "F", "O", "R", "N", "I", "A", "O", "W", "B", "A"], ["4", "N", "E", "R", "K", "I", "L", "V", "E", "R", "M", "O", "N", "T", "I", "R"], ["5", "I", "Q", "O", "E", "T", "L", "W", "I", "I", "Y", "B", "S", "W", "S", "Y"], ["6", "S", "B", "I", "N", "K", "A", "L", "A", "S", "K", "A", "A", "P", "E", "L"], ["7", "N", "J", "H", "T", "H", "D", "M", "I", "N", "N", "E", "S", "O", "T", "A"], ["8", "O", "C", "O", "U", "A", "Y", "I", "L", "N", "K", "N", "N", "E", "A", "N"], ["9", "C", "X", "V", "C", "W", "I", "B", "N", "A", "O", "V", "A", "X", "K", "D"], ["10", "S", "T", "X", "K", "A", "Y", "N", "R", "D", "A", "I", "K", "S", "S", "S"], ["11", "I", "A", "W", "Y", "I", "P", "I", "I", "E", "I", "L", "S", "V", "A", "A"], ["12", "W", "W", "M", "D", "I", "Z", "H", "G", "G", "J", "A", "B", "B", "R", "X"], ["13", "Q", "O", "M", "L", "O", "D", "S", "H", "N", "R", "T", "N", "G", "B", "E"], ["14", "I", "I", "L", "N", "U", "A", "F", "L", "O", "R", "I", "D", "A", "E", "T"], ["15", "E", "R", "A", "W", "A", "L", "E", "D", "J", "F", "F", "V", "X", "N", "F"]]'
        solution = '{"CALIFORNIA": {"y1": 3, "x1": 2, "y2": 3, "x2": 11, "direction": "L->R"}, "MINNESOTA": {"y1": 7, "x1": 7, "y2": 7, "x2": 15, "direction": "L->R"}, "WISCONSIN": {"y1": 12, "x1": 1, "y2": 4, "x2": 1, "direction": "D->U"}, "MARYLAND": {"y1": 2, "x1": 15, "y2": 9, "x2": 15, "direction": "U->D"}, "VIRGINIA": {"y1": 15, "x1": 12, "y2": 8, "x2": 5, "direction": "DR->UL"}, "DELAWARE": {"y1": 15, "x1": 8, "y2": 15, "x2": 1, "direction": "R->L"}, "ILLINOIS": {"y1": 4, "x1": 5, "y2": 11, "x2": 12, "direction": "UL->DR"}, "NEBRASKA": {"y1": 15, "x1": 14, "y2": 8, "x2": 14, "direction": "D->U"}, "KENTUCKY": {"y1": 4, "x1": 4, "y2": 11, "x2": 4, "direction": "U->D"}, "VERMONT": {"y1": 4, "x1": 7, "y2": 4, "x2": 13, "direction": "L->R"}, "MONTANA": {"y1": 2, "x1": 11, "y2": 2, "x2": 5, "direction": "R->L"}, "ALABAMA": {"y1": 1, "x1": 8, "y2": 1, "x2": 14, "direction": "L->R"}, "ARIZONA": {"y1": 9, "x1": 9, "y2": 15, "x2": 3, "direction": "UR->DL"}, "INDIANA": {"y1": 8, "x1": 7, "y2": 14, "x2": 13, "direction": "UL->DR"}, "FLORIDA": {"y1": 14, "x1": 7, "y2": 14, "x2": 13, "direction": "L->R"}, "ALASKA": {"y1": 6, "x1": 6, "y2": 6, "x2": 11, "direction": "L->R"}, "HAWAII": {"y1": 7, "x1": 5, "y2": 12, "x2": 5, "direction": "U->D"}, "KANSAS": {"y1": 10, "x1": 12, "y2": 5, "x2": 12, "direction": "D->U"}, "TEXAS": {"y1": 14, "x1": 15, "y2": 10, "x2": 15, "direction": "D->U"}, "OHIO": {"y1": 8, "x1": 3, "y2": 5, "x2": 3, "direction": "D->U"}, "IOWA": {"y1": 14, "x1": 2, "y2": 11, "x2": 2, "direction": "D->U"}}'
        cur.execute('insert into puzzles (title, words, puzzle, solution) select ?, ?, ?, ?;', (title, wordbank, puzzle, solution))
        conn.commit()
    app.run()
