from flask import Flask, request, jsonify
import os
import secrets
import uuid
import nltk

curr_dir = os.path.dirname(__file__)
parent_dir = os.path.split(curr_dir)[0]
nltk_downlaod_dir = os.path.join(parent_dir, 'app/nlkt_data')
nltk.data.path.append(nltk_downlaod_dir)

from .hamlet import generate_Hamlet_ID
from .iliad import generate_Iliad_ID
from .general_book import generate_general_ID, generate_general_public_ID

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/python/iliad/get_ID/<n>")
def get_Iliad_ID(n):
    return jsonify(generate_Iliad_ID(n))

@app.route("/api/python/hamlet/get_ID/<n>")
def get_Hamlet_ID(n):
    return jsonify(generate_Hamlet_ID(n))
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
    return jsonify(generate_general_ID(n, file_path, names))

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
