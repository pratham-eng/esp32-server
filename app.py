from flask import Flask, request, send_from_directory
import time
import os

app = Flask(__name__)

UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SECRET_KEY = "12345"

# Upload image
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

# Show latest image (FIXED)
@app.route('/latest')
def latest():
    files = os.listdir(UPLOAD_FOLDER)

    if len(files) == 0:
        return "No images yet"

    files = sorted(
        files,
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
        reverse=True
    )

    return send_from_directory(UPLOAD_FOLDER, files[0])

# Show all images (Gallery)
@app.route('/gallery')
def gallery():
    files = os.listdir(UPLOAD_FOLDER)

    if len(files) == 0:
        return "No images yet"

    files = sorted(
        files,
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
        reverse=True
    )

    html = "<h2>All Images</h2>"

    for file in files:
        html += f'<div style="margin-bottom:20px;"><img src="/image/{file}" width="300"><p>{file}</p></div>'

    return html

# Serve image
@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Home
@app.route('/')
def home():
    return "Server Running"

app.run(host='0.0.0.0', port=10000)
