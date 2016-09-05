# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/academico")
def academico():
    return render_template("academic.html")


@app.route("/social")
def social():
    return render_template("social.html")


@app.route("/section")
def section():
    return render_template("section.html")


@app.route("/new_topic")
def new_topic():
    return render_template("new_topic.html")


@app.route("/topic", methods=["GET", "POST"])
def topic():
    if request.method == "POST":
        return "Sua mensagem: {}, sob o título de: {}"\
            .format(request.form["msg"], request.form["title"])
    else:
        return render_template("topic.html")

if __name__ == "__main__":
    app.run()
