from flask import Flask, request, Response, render_template, jsonify, json
from multiprocessing import Process, Manager
import random
import sqlite3
import wordsearch

app = Flask(__name__)

def get_simple_args(rqst):
    return json.loads(rqst.args['height']), json.loads(rqst.args['width']), json.loads(rqst.args['words']).split(' '), json.loads(rqst.args['title'])

def get_fancy_args(rqst):
    data = rqst.form
    return data['template'], data['words'].split(' '), data['title']

def puzzle2template(puzzle):
    template = ''
    for row in puzzle[1:]:
        for cell in row[1:]:
            template += '#' if cell else ' '
        template += '\n'
    return template

def process_generate_puzzle(params, return_dict):
    puzzle, solution = wordsearch.pretty_puzzle(**params)
    return_dict['puzzle'] = puzzle
    return_dict['solution'] = solution

def generate_puzzle(**kwargs):
    #puzzle, solution = [], {}
    manager = Manager()
    return_dict = manager.dict()
    if 'template' in kwargs:
        assert 'words' in kwargs
        assert 'title' in kwargs
        #puzzle, solution = wordsearch.pretty_puzzle(template=kwargs['template'], words=kwargs['words'])
        args_to_pass = {'template': kwargs['template'], 'words': kwargs['words']}
    else:
        assert 'height' in kwargs
        assert 'width' in kwargs
        assert 'words' in kwargs
        assert 'title' in kwargs
        #puzzle, solution = wordsearch.pretty_puzzle(height=kwargs['height'], width=kwargs['width'], words=kwargs['words'])
        args_to_pass = {'height': kwargs['height'], 'width': kwargs['width'], 'words': kwargs['words']}
    title = kwargs['title']
    proc = Process(target=process_generate_puzzle, args=(args_to_pass, return_dict,))
    proc.start()
    proc.join(5)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return {'words': [], 'puzzle': [], 'solution': {}, 'title': title}, [], [], {}
    puzzle = return_dict['puzzle']
    solution = return_dict['solution']
    wordbank = list(solution.keys())
    random.shuffle(wordbank)
    out = {'words': wordbank, 'puzzle': puzzle, 'solution': solution, 'title': title}
    return out, wordbank, puzzle, solution

@app.route('/api/instant/simple', methods=['GET'])
def get_simple_puzzle():
    global conn
    global cur
    height, width, words, title = get_simple_args(request)
    out, wordbank, puzzle, solution = generate_puzzle(height=height, width=width, words=words, title=title)
    cur.execute('insert into puzzles (title, words, puzzle, solution, created) select ?, ?, ?, ?, datetime(\'now\');', (title, str(wordbank), str(puzzle), str(solution)))
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
    cur.execute('insert into puzzles (title, words, puzzle, solution, created) select ?, ?, ?, ?, datetime(\'now\');', (title, str(wordbank), str(puzzle), str(solution)))
    conn.commit()
    if 'page' in request.args:
        return render_template('puzzle.html', words=wordbank, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false', template=template)
    return jsonify(out)

@app.route('/api/saved/page', methods=['GET'])
def get_puzzle_by_id():
    global conn
    global cur
    _id = json.loads(request.args['id'])
    cur.execute('select rowid, title, words, puzzle, solution, created from puzzles where rowid = %d;' % (_id))
    row = cur.fetchone()
    rowid, title, words, puzzle, solution, created = row[0], row[1], row[2], row[3], row[4], row[5]
    return render_template('puzzle.html', words=words, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false', rowid=rowid, created=created)

@app.route('/api/instant/shuffle', methods=['POST'])
def shuffle_puzzle():
    global conn
    global cur
    puzzle_str, words_str, title = get_fancy_args(request)
    old_puzzle = [row.split(',') for row in puzzle_str.split('|')]
    template = puzzle2template(old_puzzle)
    words = words_str[0].split(',')
    out, _, _, _ = generate_puzzle(template=template, words=words, title=title)
    return jsonify(out)

@app.route('/')
def get_random_puzzle():
    global conn
    global cur
    cur.execute('select rowid, title, words, puzzle, solution, created from puzzles order by random() limit 1;')
    row = cur.fetchone()
    rowid, title, words, puzzle, solution, created = row[0], row[1], row[2], row[3], row[4], row[5]
    return render_template('puzzle.html', words=words, puzzle=puzzle, solution=solution, title=title, reveal_words='true' if 'reveal' in request.args else 'false', rowid=rowid, created=created)

if __name__ == '__main__':
    conn = sqlite3.connect('wordsearch.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select name from sqlite_master where type=\'table\' AND name=\'puzzles\';')
    if cur.fetchone() is None:
        with open('sample.json', mode='r', encoding='utf8') as f:
            sample = json.load(f)
        title, wordbank, puzzle, solution = sample['title'], str(sample['wordbank']), str(sample['puzzle']), str(sample['solution'])
        cur.execute('create table puzzles (title text, words text, puzzle text, solution text, created text, solved_by text, solved_on text, solved_in number);')
        cur.execute('insert into puzzles (title, words, puzzle, solution, created) select ?, ?, ?, ?, datetime(\'now\');', (title, wordbank, puzzle, solution))
        conn.commit()
    app.run()
