from flask import Flask, request, render_template, redirect, url_for
from Pyro5.api import Proxy
import os

app = Flask(__name__)
FILE_DIR = "files"
os.makedirs(FILE_DIR, exist_ok=True)


def get_doc_manager():
    return Proxy("PYRO:docmanager@0.0.0.0:9090")


@app.route("/")
def index():
    files = os.listdir(FILE_DIR)
    file_states = {}
    with get_doc_manager() as doc_manager:
        for f in files:
            file_states[f] = doc_manager.get_lock_info(f)
    return render_template("index.html", files=sorted(files), states=file_states)


@app.route("/create", methods=["POST"])
def create():
    filename = request.form["filename"].strip()
    if not filename:
        return redirect(url_for("index"))
    path = os.path.join(FILE_DIR, filename)
    if not os.path.exists(path):
        open(path, "w").close()
    return redirect(url_for("index"))


@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit(filename):
    ip = request.remote_addr
    path = os.path.join(FILE_DIR, filename)
    if not os.path.exists(path):
        return "File not found", 404

    with get_doc_manager() as doc_manager:
        if request.method == "GET":
            if not doc_manager.request_lock(filename, ip):
                return render_template("locked.html"), 200

            with open(path) as f:
                content = f.read()
            return render_template("edit.html", filename=filename, content=content)

        else:
            action = request.form.get("action")
            with open(path, "w") as f:
                f.write(request.form.get("content", ""))
            if action == "save_release":
                doc_manager.release_lock(filename, ip)
                return redirect(url_for("index"))
            else:
                return redirect(url_for("edit", filename=filename))


@app.route("/view/<filename>")
def view(filename):
    path = os.path.join(FILE_DIR, filename)
    if not os.path.exists(path):
        return "File not found", 404

    with open(path) as f:
        content = f.read()
    return render_template("view.html", filename=filename, content=content)


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")
