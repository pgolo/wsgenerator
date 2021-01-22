from flask import Flask, request, Response, render_template, jsonify, json
import random
import wordsearch

app = Flask(__name__)

def get_simple_args(rqst):
    return json.loads(rqst.args['height']), json.loads(rqst.args['width']), json.loads(rqst.args['words']).split(' ')

def get_fancy_args(rqst):
    data = rqst.form
    return data['template'], data['words'].split(' ')

def generate_puzzle(**kwargs):
    if 'template' in kwargs:
        assert 'words' in kwargs
        puzzle, solution = wordsearch.pretty_puzzle(template=kwargs['template'], words=kwargs['words'])
    else:
        assert 'height' in kwargs
        assert 'width' in kwargs
        assert 'words' in kwargs
        puzzle, solution = wordsearch.pretty_puzzle(height=kwargs['height'], width=kwargs['width'], words=kwargs['words'])
    wordbank = list(solution.keys())
    random.shuffle(wordbank)
    out = {'words': wordbank, 'puzzle': puzzle, 'solution': solution}
    return out, wordbank, puzzle, solution

@app.route('/api/instant/simple', methods=['GET'])
def get_simple_puzzle():
    height, width, words = get_simple_args(request)
    out, wordbank, puzzle, solution = generate_puzzle(height=height, width=width, words=words)
    if 'page' in request.args:
        return render_template('puzzle.html', words=wordbank, puzzle=puzzle, solution=solution, reveal_words='true' if 'reveal' in request.args else 'false')
    return jsonify(out)

@app.route('/api/instant/fancy', methods=['POST', 'GET'])
def get_fancy_puzzle():
    template, words = get_fancy_args(request)
    out, wordbank, puzzle, solution = generate_puzzle(template=template, words=words)
    if 'page' in request.args:
        return render_template('puzzle.html', words=wordbank, puzzle=puzzle, solution=solution)
    return jsonify(out)

if __name__ == '__main__':
    app.run()
