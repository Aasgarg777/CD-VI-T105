from flask import Flask, render_template, request, jsonify
from lexer import lexical_analysis
from parser import build_ast

app = Flask(__name__)

class WebASTNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

    def to_dict(self):
        return {
            'value': self.value,
            'children': self.children  
        }

def convert_ast_for_web(ast_node):
    if ast_node is None:
        return {}

    children = [convert_ast_for_web(child) for child in ast_node.children]
    return WebASTNode(ast_node.value, children).to_dict()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    sentence = request.json['sentence']
    pos_tags = lexical_analysis(sentence)
    ast_root = build_ast(pos_tags)
    ast_dict = convert_ast_for_web(ast_root)
    return jsonify({
        'tokens': pos_tags,
        'ast': ast_dict
    })

if __name__ == '__main__':
    app.run(debug=True)
