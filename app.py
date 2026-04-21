from flask import Flask, request
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
    filename = f"{UPLOAD_FOLDER}/img_{int(time.time())}.jpg"

    with open(filename, "wb") as f:
        f.write(image)

    return "OK"

@app.route('/')
def home():
    return "Server Running"

app.run(host='0.0.0.0', port=10000)