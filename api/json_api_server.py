import os
from flask import Flask, jsonify, send_from_directory
from db.models import init_db, list_items
from dotenv import load_dotenv
load_dotenv()

app = Flask(_name_, static_folder="../frontend", static_url_path="/")


init_db()

@app.route("/api/items")
def api_items():
    items = list_items(limit=200)
    return jsonify(items)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(app.static_folder), filename)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)