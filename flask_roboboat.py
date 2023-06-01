# app.py
from flask import Flask, jsonify, request, render_template
import requests
app = Flask(__name__)


@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/task', methods=['GET', 'POST'])
def task():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'task': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')


@app.route('/test2')
def testy():
    url = '127.0.0.1:5000/task'
    myobj = {'somekey': 'somevalue'}

    x = requests.get(url)
    return x
