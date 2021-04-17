import os

from flask import Flask
from redis import Redis
from nltk.tokenize import word_tokenize


app = Flask(__name__)
r = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db='0',
    decode_responses=True
)
REDIS_NAMES_KEY = "names"


@app.route("/doc/<doc>", methods=["POST"])
def process_doc(doc):
    tokens = word_tokenize(doc)
    for i in tokens:
        new = r.rpush(i, "doc1")
    return {"tokens": list(tokens)}