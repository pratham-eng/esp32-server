from flask import Flask, request, send_from_directory
import time
import os

app = Flask(__name__)

UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SECRET_KEY = "12345"

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get("Authorization") != SECRET_KEY:
        return "Unauthorized", 401

    image = request.data
    filename = f"img_{int(time.time())}.jpg"

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(image)

    return "OK"

# 👉 NEW ROUTE (IMPORTANT)
@app.route('/latest')
def latest():
    files = os.listdir(UPLOAD_FOLDER)

    if len(files) == 0:
        return "No images yet"

    files.sort(reverse=True)
    return send_from_directory(UPLOAD_FOLDER, files[0])

@app.route('/')
def home():
    return "Server Running"

app.run(host='0.0.0.0', port=10000)
