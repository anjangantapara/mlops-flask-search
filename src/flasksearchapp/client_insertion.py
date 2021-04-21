import requests

from nltk.corpus import reuters

n_insertions = 1000
url = "http://0.0.0.0:8000/api/store_doc/submit_doc"
for index, i in enumerate(reuters.fileids()):
    doc = reuters.raw(fileids=[i])
    doc_name = "doc" + str(index)
    insert_dict = {doc_name: doc}
    r = requests.post(url=url, json=insert_dict)
    print(doc_name)
    print(r)
    if index==n_insertions:
        break
print("Inserted {} doccuments",n_insertions)