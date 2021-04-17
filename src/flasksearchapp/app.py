import os

from flask import Flask, request
from nltk.tokenize import word_tokenize
from redis import Redis

app = Flask(__name__)
r = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db='0',
    decode_responses=True
)
REDIS_NAMES_KEY = "names"


@app.route('/api/<doc>', methods=['POST'])
def process_doc(doc):
    content = dict(request.json)
    doc_name = list(content.keys())[0]
    doc_content = list(content.values())[0]

    tokens = word_tokenize(doc_content)
    for i in tokens:
        new = r.rpush(i, doc_name)
    return {"tokens": list(tokens)}

@app.route('/api/<print_doc_names>', methods=['GET'])
def print_doc_names_api(print_doc_names):
    return {"total docs": r.llen()}
#
# @app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
# def add_message(uuid):
#     content = request.json
#     print content['mytext']
#     return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)