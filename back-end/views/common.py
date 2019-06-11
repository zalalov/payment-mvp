from flask import send_from_directory
from app import app


@app.route("/static/<path:path>")
def hello(path):
    return send_from_directory(configuration.DIST_DIR, path)
