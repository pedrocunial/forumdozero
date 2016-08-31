# -*- coding: utf-8 -*-

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/topic", methods=["GET", "POST"])
def topic():
    if request.method == "POST":
        return "Sua mensagem: {}, sob o título de: {}"\
            .format(request.form["msg"], request.form["title"])
    else:
        return render_template("topic.html")

if __name__ == "__main__":
    app.run()
