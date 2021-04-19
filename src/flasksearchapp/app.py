import os

from flask import Flask, request
from flasksearchapp.process import ProcessData
from redis import Redis, StrictRedis

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



class redis_io():

    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    def get_all_values(self):
        list_values = []
        for key in self.redis_connection.keys():
            list_values.append(self.redis_connection.get(key))
        return {"doc_content": list_values}
    def get_all_keys_values(self):
        list_keys = []
        list_values = []
        for key in self.redis_connection.keys():
            list_keys.append(key)
            list_values.append(r_docs.get(key))
        return {"doc_names": list_keys, "doc_content": list_values}

redis_io.redis_connection = r_docs


@app.route('/api/store/<submit_doc>', methods=['POST'])
def store_input(submit_doc):
    content = dict(request.json)
    doc_name = list(content.keys())[0]
    doc_content = list(content.values())[0]
    #    tokens = word_tokenize(doc_content)
    r_docs.set(doc_name, doc_content)
    return "Inserted the doc to redis"


#    for i, val in enumerate(tokens):
#        r_tokens.rpush(doc_name, val)
#   return {"tokens": tokens}


@app.route('/api/process_data', methods=['GET'])
def process():
    redis_db = redis_io(redis_connection=r_docs)
    doc_content = redis_db.get_all_values()['doc_content']
    # initializing the input data
    ProcessData.set_list_texts(input_list_text=doc_content)
    # processing the text
    ProcessData.text_processing()
    # calling create_tdm to create tdm matrix
    ProcessData.create_tdm()
    return {'key': ProcessData.text_zonder_punctuations}


@app.route('/api/search_string/<search_string>', methods=['GET'])
def search(search_string):
    processdata = ProcessData(search_string=search_string)
    res_list = processdata.get_similar_articles()
    return {"res": res_list}


@app.route('/api/get_docs/<docs>', methods=['GET'])
def get_docs(docs):
    redis_db = redis_io(redis_connection=r_docs)
    keys_values_dict = redis_db.get_all_keys_values()
    return keys_values_dict


@app.route('/api/get_tokens/<tokens>', methods=['GET'])
def get_tokens(tokens):
    dict_tokens = {}
    for key in r_tokens.keys():
        list_temp = []
        while (r_tokens.llen(key) != 0):
            list_temp.append(r_tokens.rpop(key))
        dict_tokens[key] = list_temp
    return dict_tokens


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
