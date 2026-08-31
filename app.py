from flask import Flask, jsonify, render_template, request, send_file

from kgqa.data import CATEGORIES, chart_data, image_path, people, relations
from kgqa.parser import get_target_array
from kgqa.queries import get_answer_profile, get_KGQA_answer, query

app = Flask(__name__)
app.config.update(MAX_CONTENT_LENGTH=4096, MAX_FORM_MEMORY_SIZE=4096, MAX_FORM_PARTS=8)


def argument(name):
    value = request.args.get(name) if request.method == "GET" else request.form.get(name)
    if value is None or not value.strip() or len(value) > 200:
        raise ValueError("参数不能为空，且不得超过 200 字符")
    return value.strip()


@app.errorhandler(ValueError)
def bad_request(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(KeyError)
def unknown_person(error):
    return jsonify(error="未找到该人物"), 404


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    )
    return response


@app.route("/")
@app.route("/index")
@app.route("/get_all_relation")
def index():
    return render_template("graph.html", mode="all", categories=CATEGORIES, names=sorted(people()))


@app.route("/search")
def search():
    return render_template("graph.html", mode="search", categories=CATEGORIES, names=sorted(people()))


@app.route("/KGQA")
def KGQA():
    return render_template("graph.html", mode="qa", categories=CATEGORIES, names=sorted(people()))


@app.route("/graph_data")
def graph_data():
    return jsonify(chart_data(relations()))


@app.route("/get_profile", methods=["GET", "POST"])
def get_profile():
    return jsonify(get_answer_profile(argument("character_name")))


@app.route("/portrait")
def portrait():
    path = image_path(argument("name"))
    if path is None:
        return "", 404
    return send_file(path, mimetype="image/jpeg")


@app.route("/KGQA_answer", methods=["GET", "POST"])
def KGQA_answer():
    return jsonify(get_KGQA_answer(get_target_array(argument("name"))))


@app.route("/search_name", methods=["GET", "POST"])
def search_name():
    return jsonify(query(argument("name")))


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)
