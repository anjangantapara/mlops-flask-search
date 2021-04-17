import os

from flask import Flask, request
from nltk.tokenize import word_tokenize
from redis import Redis, StrictRedis

import pandas as pd
import numpy as np
import string
import random

import nltk
from nltk.corpus import brown
from nltk.corpus import reuters

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords

from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer  # Instantiate a TfidfVectorizer object
from process import create_tdm, text_processing, get_similar_articles
app = Flask(__name__)
r_docs = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db='0',
    decode_responses=True
)

r_tokens = StrictRedis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db='1',
    decode_responses=True
)
REDIS_NAMES_KEY = "names"



@app.route('/api/<submit_doc>', methods=['POST'])
def store_input(submit_doc):
    content = dict(request.json)
    doc_name = list(content.keys())[0]
    doc_content = list(content.values())[0]

    tokens = word_tokenize(doc_content)
    r_docs.set(doc_name, doc_content)
    for i, val in enumerate(tokens):
        r_tokens.rpush(doc_name, val)
    # for i in tokens:
    #     new_list = r_tokens.rpush(i, doc_name)
    #     new_str = r_docs.set(doc_name, doc_content)
    return {"tokens": tokens}

@app.route('/api/process', methods=['GET'])
def process():
    content = get_docs()
    doc_content = content['doc_content']
    processed_text = text_processing(doc_content)
    return {'key': processed_text}

@app.route('/api/search/<search_string>', methods=['GET'])
def search(search_string):
    processed_text = process()
    df_tdm, vectorizer = create_tdm(processed_text)
    res_list = get_similar_articles(search_string, df_tdm, vectorizer)



    return {"res": res_list}

@app.route('/api/<docs>', methods=['GET'])
def get_docs():
    list_keys = []
    list_values = []
    for key in r_docs.keys():
        list_keys.append(key)
        list_values.append(r_docs.get(key))
    return {"doc_names": list_keys, "doc_content": list_values}

@app.route('/api/<tokens>', methods=['GET'])
def get_tokens(tokens):
    dict_tokens ={}
    for key in r_tokens.keys():
        list_temp = []
        while (r_tokens.llen(key) != 0):
            list_temp.append(r_tokens.rpop(key))
        dict_tokens[key] = list_temp
    return dict_tokens
#
# @app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
# def add_message(uuid):
#     content = request.json
#     print content['mytext']
#     return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)