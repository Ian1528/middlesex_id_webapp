from flask import Flask, jsonify
import os
from hamlet import generate_Hamlet_ID
from iliad import generate_Iliad_ID
app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/python/test_input/<output_string>")
def test_input(output_string):
    file_path = os.path.join(os.path.dirname(__file__), 'hamlet_textfile.txt')

    with open(file_path, 'r') as file:
        output_string = file.read()
    return jsonify(output_string)

@app.route("/api/python/iliad/get_ID/<n>")
def get_Iliad_ID(n):
    return jsonify(generate_Iliad_ID(n))

@app.route("/api/python/hamlet/get_ID/<n>")
def get_Hamlet_ID(n):
    return jsonify(generate_Hamlet_ID(n))