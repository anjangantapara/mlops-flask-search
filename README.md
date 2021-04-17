# mlops-flask-search

flask application to store a document and search for it later


Command to send json file:
echo '{"doc0": "new text up"}' | http POST http://localhost:8000/api/doc

command to call the doc names
 http -v GET http://localhost:8000/api/print_doc_names

