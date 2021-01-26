from flask import Flask, request, Response, render_template, jsonify, json
import random
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
    conn = sqlite3.connect('wordsearch.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select name from sqlite_master where type=\'table\' AND name=\'puzzles\';')
    if cur.fetchone() is None:
        with open('sample.json', mode='r', encoding='utf8') as f:
            sample = json.load(f)
        title, wordbank, puzzle, solution = sample['title'], str(sample['wordbank']), str(sample['puzzle']), str(sample['solution'])
        print(title)
        cur.execute('create table puzzles (title text, words text, puzzle text, solution text);')
        cur.execute('insert into puzzles (title, words, puzzle, solution) select ?, ?, ?, ?;', (title, wordbank, puzzle, solution))
        conn.commit()
    app.run()
