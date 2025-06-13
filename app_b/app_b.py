from flask import Flask, request, render_template, redirect, send_from_directory
import os
from Pyro5.api import Proxy
from mirror_utils import mirror_file
import requests

app = Flask(__name__)
FILES_DIR = "files"
MIRROR_URL = "http://0.0.0.0:5000"  # Reverse this in app_b
PYRO_URI = "PYRO:docmanager@0.0.0.0:9090"

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)


@app.route("/")
def index():
    files = os.listdir(FILES_DIR)
    with Proxy(PYRO_URI) as docman:
        states = {f: docman.get_lock_info(f) for f in files}
    return render_template("index.html", files=files, states=states)


@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit(filename):
    ip = request.remote_addr
    path = os.path.join(FILES_DIR, filename)

    with Proxy(PYRO_URI) as docman:
        if not docman.request_lock(filename, ip):
            return render_template("locked.html")

    if request.method == "POST":
        content = request.form["content"]
        with open(path, "w") as f:
            f.write(content)
        mirror_file(path, MIRROR_URL, filename)

        if request.form["action"] == "save_release":
            with Proxy(PYRO_URI) as docman:
                docman.release_lock(filename, ip)

        return redirect("/")

    if not os.path.exists(path):
        return "File not found", 404

    with open(path) as f:
        content = f.read()
    return render_template("edit.html", filename=filename, content=content)


@app.route("/view/<filename>")
def view(filename):
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        return "File not found", 404
    with open(path) as f:
        content = f.read()
    return render_template("view.html", filename=filename, content=content)


@app.route("/mirror_receive/<filename>", methods=["POST"])
def mirror_receive(filename):
    file = request.files["file"]
    path = os.path.join(FILES_DIR, filename)
    file.save(path)
    return "OK"


@app.route("/create", methods=["POST"])
def create():
    filename = request.form["filename"]
    path = os.path.join(FILES_DIR, filename)
    open(path, "w").close()
    mirror_file(path, MIRROR_URL, filename)
    return redirect("/")


@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    ip = request.remote_addr
    with Proxy(PYRO_URI) as docman:
        if docman.get_lock_info(filename) != ip:
            return "Forbidden", 403
        docman.release_lock(filename, ip)

    os.remove(os.path.join(FILES_DIR, filename))
    try:
        requests.post(f"{MIRROR_URL}/mirror_delete/{filename}", timeout=2)
    except:
        pass
    return redirect("/")


@app.route("/mirror_delete/<filename>", methods=["POST"])
def mirror_delete(filename):
    try:
        os.remove(os.path.join(FILES_DIR, filename))
    except FileNotFoundError:
        pass
    return "OK"


if __name__ == "__main__":
    app.run(port=5001)  # Change to 5001 for app_b
