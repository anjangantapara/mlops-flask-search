import os
from typing import List, Dict, AnyStr

from flask import Flask, request
from flasksearchapp.process import SearchDocuments
from redis import Redis

app = Flask(__name__)
r_docs = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=6379,
    db='0',
    decode_responses=True
)


class redis_io():

    def __init__(self, redis_connection) -> None:
        """
        initi function for the redis_io class
        :param redis_connection: redis_io object
        :type redis_connection: Redis
        """
        self.redis_connection = redis_connection

    def get_all_values(self) -> Dict:
        """
        Method to grab all the values stored in Redis
        :return: all the values/documents stored in Redis
        :rtype: dict
        """
        list_values = []
        for key in self.redis_connection.keys():
            list_values.append(self.redis_connection.get(key))
        return {"doc_content": list_values}

    def get_all_keys_values(self) -> Dict:
        """
        Method that returns both doc names and documents
        :return: all_doc_content
        :rtype: dict
        """
        list_keys = []
        list_values = []
        for key in self.redis_connection.keys():
            list_keys.append(key)
            list_values.append(r_docs.get(key))
        all_doc_content = {"doc_names": list_keys, "doc_content": list_values}
        return all_doc_content


redis_io.redis_connection = r_docs


@app.route('/api/store_doc/<submit_doc>', methods=['POST'])
def store_doc(submit_doc) -> AnyStr:
    """
    API to store the input strings/documents
    :param submit_doc: not used
    :type submit_doc: str
    :return: standard text: Inserted the doc to redis
    :rtype: str
    """
    content = dict(request.json)
    doc_name = list(content.keys())[0]
    doc_content = list(content.values())[0]
    #    tokens = word_tokenize(doc_content)
    r_docs.set(doc_name, doc_content)
    return "Inserted the doc to redis"


@app.route('/api/get_docs/<docs>', methods=['GET'])
def get_docs(docs) -> Dict:
    """
    API to fetch all documents
    :param docs:
    :type docs:str
    :return:
    :rtype:dict
    """
    redis_db = redis_io(redis_connection=r_docs)
    keys_values_dict = redis_db.get_all_keys_values()
    return keys_values_dict


@app.route('/api/get_doc_with_key/<key>', methods=['GET'])
def get_doc_with_key(key) -> AnyStr:
    """
    API to fetch a specific document with key
    :param key:
    :type key:str
    :return:
    :rtype:dict
    """
    # redis_db = redis_io(redis_connection=r_docs)
    # keys_values_dict = redis_db.get_all_keys_values()
    doc = r_docs.get(key)
    return doc


@app.route('/api/process_data', methods=['GET'])
def process() -> Dict:
    """
    API to process_data
    :return: dictionary containing the processed text
    :rtype: dict
    """
    redis_db = redis_io(redis_connection=r_docs)
    all_doc_content = redis_db.get_all_keys_values()
    # doc_content = redis_db.get_all_values()['doc_content']
    # initializing the input data
    SearchDocuments.set_documents(input_list_text=all_doc_content['doc_content'])
    SearchDocuments.set_documents_names(input_list_names=all_doc_content['doc_names'])

    # processing the text
    SearchDocuments.clean_all_documents()
    # calling create_tdm to create tdm matrix
    SearchDocuments.create_tdm()
    return "Successfully created tf_idf matrix"


@app.route('/api/search/<search_string>', methods=['GET'])
def search(search_string)->Dict:
    """
    API to search "search_string" in the stored documents
    :param search_string: search string provided by the user
    :type search_string: str
    :return: returns results i.e. return list of documents that are closest match to the search string
    :rtype: dict
    """
    processdata = SearchDocuments(search_string=search_string)
    res_list = processdata.get_relevant_documents()
    return {"search_results": res_list}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
