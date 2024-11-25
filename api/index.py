from flask import Flask, jsonify
import os
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
    return jsonify({"output": output_string})
