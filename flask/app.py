from flask import Flask, url_for, render_template, request
from risk.simulator import simulate_turn
app = Flask(__name__)


@app.route("/", methods={"GET"})
def index():
    return render_template(
        "index.html",
        cssfile=url_for("static", filename="style.css"),
        jsfile=url_for("static", filename="index.js"),
    )


@app.route("/", methods={"POST"})
def index_post():
    # print(request.json)
    return simulate_turn(request.json)
