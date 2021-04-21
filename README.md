# mlops-flask-search


This Flask application stores submitted documents in Redis-DB. Using the **search** api one can search the documents.

List of API's:

1. *store_doc*: stores the documents
   * eg: ```echo '{"doc0": "new text up"}' | http POST http://localhost:8000/api/store/<submit_doc>```
1. *get_docs*: fetches all the document
    * eg: ```http -v get http://localhost:8000/api/get_docs/```
1. *get_doc_with_key*: fetches document related to the key(i.e. document name)
    * eg: ```http -v get http://localhost:8000/api/get_doc_with_key/doc15```
1. *process_data*: processes input documents and computed tf_idf matrix
   * eg: ```http -v get http://localhost:8000/api/process_data```
1. *search*: search's given string
   * eg:  ```http -v get http://localhost:8000/api/search/<search_string>```


