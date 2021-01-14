from flask import Flask, request, Response, render_template, jsonify, json
import random
import wordsearch
import page

app = Flask(__name__)

def get_simple_args(rqst):
    return json.loads(request.args['height']), json.loads(request.args['width']), json.loads(request.args['words']).split(' ')

@app.route('/api/instant/simple', methods=['GET'])
def get_simple_puzzle():
    height, width, words = get_simple_args(request)
    puzzle, solution = wordsearch.pretty_puzzle(height=height, width=width, words=words)
    wordbank = list(solution.keys())
    random.shuffle(wordbank)
    out = {'words': wordbank, 'puzzle': puzzle, 'solution': solution}
    return jsonify(out)

@app.route('/api/instant/fancy', methods=['POST'])
def get_fancy_puzzle():
    data = request.form
    template = data['template']
    words = data['words'].split(' ')
    puzzle, solution = wordsearch.pretty_puzzle(template=template, words=words)
    wordbank = list(solution.keys())
    random.shuffle(wordbank)
    out = {'words': wordbank, 'puzzle': puzzle, 'solution': solution}
    return jsonify(out)

@app.route('/api/instant/simple/page', methods=['GET'])
def get_simple_page():
    height, width, words = get_simple_args(request)
    html = page.create(height=height, width=width, words=words)
    out = {'html': html}
    return jsonify(out)

if __name__ == '__main__':
    app.run()
