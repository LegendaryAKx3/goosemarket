from flask import Flask
from api.tags import add_tag_to_poll, create_tag, get_all_tags, get_tag_by_id
app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/tags/add", methods=["POST"])
def add_tag_route():
    return add_tag_to_poll()

@app.route("/api/tags/all", methods=["POST"])
def get_all_tags_route():
    return get_all_tags()

@app.route("/api/tags/id", methods=["POST"])
def get_tag_by_id_route():
    return get_tag_by_id()