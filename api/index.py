"""
This module provides a Flask web application with several API endpoints for generating IDs based on different texts and uploading text files.
Routes:
    /api/python/iliad/get_ID:
        GET request to generate IDs based on the Iliad text.
        Query Parameters:
            - n (int): Number of IDs to generate.
            - hide_names (bool, optional): Whether to hide names in the generated IDs. Defaults to True.
    /api/python/hamlet/get_ID:
        GET request to generate IDs based on the Hamlet text.
        Query Parameters:
            - n (int): Number of IDs to generate.
            - hide_names (bool, optional): Whether to hide names in the generated IDs. Defaults to True.
    /api/python/get_custom_ID:
        GET request to generate custom IDs based on an uploaded text file.
        Query Parameters:
            - n (int): Number of IDs to generate.
            - names (str, optional): Comma-separated list of names to include in the generated IDs.
    /api/python/general_public/get_ID:
        GET request to generate general public IDs based on a specified file in the public directory of the app.
        Query Parameters:
            - filename (str): Name of the file to use for generating IDs.
            - n (int): Number of IDs to generate.
            - names (str, optional): Comma-separated list of names to include in the generated IDs.
    /api/python/upload_text:
        POST request to upload a plain text file.
        Request Files:
            - file (file): Plain text file to upload.
        Response:
            - message (str): Success message.
            - content (str): Content of the uploaded text file.
    /api/python/close_session:
        POST request to close the current session by deleting the uploaded text file.
        Response:
            - message (str): Success message indicating the session is closed.
"""
from flask import Flask, request, jsonify

import os
import secrets
import uuid
import nltk
import json

curr_dir = os.path.dirname(__file__)
parent_dir = os.path.split(curr_dir)[0]
nltk_downlaod_dir = os.path.join(parent_dir, 'app/nlkt_data')
nltk.data.path.append(nltk_downlaod_dir)

from .hamlet import generate_Hamlet_ID
from .iliad import generate_Iliad_ID
from .general_book import generate_custom_ID, generate_general_public_ID, generate_thecolony_id, generate_json_file_id

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/python/iliad/get_ID")
def get_Iliad_ID():
    args = request.args
    try:
        n = int(args.get("n"))
        hide_names = args.get("hide_names", "true").lower() == "true"
    except Exception as e:
        return jsonify(f"error Invalid request: {str(e)}"), 400
    return jsonify(generate_Iliad_ID(n, hide_names))

@app.route("/api/python/hamlet/get_ID")
def get_Hamlet_ID():
    args = request.args
    try:
        n = int(args.get("n"))
        hide_names = args.get("hide_names", "true").lower() == "true"
    except Exception as e:
        return jsonify(f"error Invalid request: {str(e)}"), 400
    
    return jsonify(generate_Hamlet_ID(n, hide_names))
@app.route("/api/python/get_custom_ID")
def get_custom_ID():
    args = request.args
    try:
        n = int(args.get('n'))
        if "names" in args.keys():
            names = args.get('names').split(',')
            names = [name.strip() for name in names]
        else:
            names = []
        if len(names) == 1 and names[0] == '':
            names = []
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "custom.txt")
    except Exception as e:
        return jsonify(f"error Invalid request: {str(e)}"), 400
    return jsonify(generate_custom_ID(n, file_path, names))

@app.route("/api/python/general_public/get_ID")
def get_general_ID():
    args = request.args
    try:
        filename = args.get('filename')
        n = int(args.get('n'))
        if "names" in args.keys():
            names = args.get('names').split(',')
            names = [name.strip() for name in names]
        else:
            names = []
        if len(names) == 1 and names[0] == '':
            names = []
    except Exception as e:
        return jsonify(f"error Invalid request: {str(e)}"), 400
    
    if filename =="thecolony.json":
        return jsonify(generate_thecolony_id(n, names))
    elif filename[-4:] == "json":
        return jsonify(generate_json_file_id(n, filename, names))
    return jsonify(generate_general_public_ID(n, filename, names))

@app.route("/api/python/upload_text", methods=["POST"])
def upload_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.content_type == 'text/plain':
        try:
            # Generate a unique filename and save the file temporarily
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], "custom.txt")
            file.save(file_path)

            print("File path is", file_path, flush=True)

            # Read and return the content of the text file
            with open(file_path, 'r', encoding="utf8") as text_file:
                content = text_file.read()

            return jsonify({
                "message": "Text file uploaded successfully",
                "content": content,
            }), 200
        except Exception as e:
            return jsonify({"error": f"Error processing text file: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type. Please upload a plain text file."}), 400

@app.route("/api/python/close_session", methods=["POST"])
def close_session():
    text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "custom.txt")
    if os.path.exists(text_file_path):
        os.remove(text_file_path)
    return jsonify("Session closed"), 200
