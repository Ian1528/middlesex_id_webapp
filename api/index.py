from flask import Flask, request, jsonify, session, send_file
import os
import secrets
import uuid

from .nlkt_modules import *
from .hamlet import generate_Hamlet_ID
from .iliad import generate_Iliad_ID
from .exit_west import generate_exit_west_ID

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/python/iliad/get_ID/<n>")
def get_Iliad_ID(n):
    return jsonify(generate_Iliad_ID(n))

@app.route("/api/python/hamlet/get_ID/<n>")
def get_Hamlet_ID(n):
    return jsonify(generate_Hamlet_ID(n))

@app.route("/api/python/exit_west/get_ID/<n>")
def get_EW_ID(n):
    return jsonify(generate_exit_west_ID(n))

@app.route("/api/python/custom/get_ID/<n>")
def get_custom_ID(n):
    return jsonify("HELLO")

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
            temp_filename = f"{uuid.uuid4()}.txt"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
            file.save(file_path)

            # Store the file path in the session
            session['text_file'] = temp_filename

            # Read and return the content of the text file
            with open(file_path, 'r', encoding="utf8") as text_file:
                content = text_file.read()

            return jsonify({
                "message": "Text file uploaded successfully",
                "filename": temp_filename,
                "content": content
            }), 200
        except Exception as e:
            return jsonify({"error": f"Error processing text file: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type. Please upload a plain text file."}), 400

@app.route("/api/python/close_session", methods=["POST"])
def close_session():
    text_file = session.get('text_file')
    if text_file:
        text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], text_file)
        if os.path.exists(text_file_path):
            print("Deleting text file...")
            os.remove(text_file_path)
    return jsonify({"message": "Session closed"}), 200
