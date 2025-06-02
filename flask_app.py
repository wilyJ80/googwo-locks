# flask_app.py
from flask import Flask, request, render_template, redirect, url_for
from Pyro5.api import Proxy
import os

app = Flask(__name__)
FILE_DIR = "files"
os.makedirs(FILE_DIR, exist_ok=True)


# Always create a new proxy per request
def get_doc_manager():
    return Proxy("PYRO:docmanager@localhost:9090")


@app.route("/")
def index():
    files = os.listdir(FILE_DIR)
    file_states = {}
    with get_doc_manager() as doc_manager:
        for f in files:
            file_states[f] = doc_manager.get_lock_info(f)
    return render_template("index.html", files=files, states=file_states)


@app.route("/create", methods=["POST"])
def create():
    filename = request.form["filename"]
    path = os.path.join(FILE_DIR, filename)
    open(path, "w").close()
    return redirect(url_for("index"))


@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit(filename):
    ip = request.remote_addr
    path = os.path.join(FILE_DIR, filename)
    with get_doc_manager() as doc_manager:
        if request.method == "POST":
            if doc_manager.request_lock(filename, ip):
                with open(path, "w") as f:
                    f.write(request.form["content"])
            return redirect(url_for("index"))
        if not doc_manager.request_lock(filename, ip):
            return "File is locked by another user.", 403
    with open(path) as f:
        content = f.read()
    return render_template("edit.html", filename=filename, content=content)


@app.route("/release/<filename>", methods=["POST"])
def release(filename):
    ip = request.remote_addr
    with get_doc_manager() as doc_manager:
        doc_manager.release_lock(filename, ip)
    return redirect(url_for("index"))


@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    path = os.path.join(FILE_DIR, filename)
    os.remove(path)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
