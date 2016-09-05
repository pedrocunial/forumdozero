# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    post_title = db.Column(db.String(140), unique=True)
    post_text = db.Column(db.String(2000), unique=True)
    score = db.Column(db.Integer, unique=True)

    def __init__(self, email, post_title, post_text, score):
        self.email = email
        self.post_title = post_title
        self.post_text = post_text
        self.score = score


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/academico")
def academico():
    return render_template("academic.html")


@app.route("/social")
def social():
    return render_template("social.html")


@app.route("/topic", methods=["GET", "POST"])
def topic():
    if request.method == "POST":
        email = "johndoe"
        post_title = request.form["title"]
        post_text = request.form["msg"]
        score = 1
        user = User(email, post_title, post_text, score)
        db.session.add(user)
        db.session.commit()
        return "Sua mensagem: {}, sob o título de: {}"\
            .format(post_text, post_title)
    else:
        return render_template("topic.html")


@app.route("/read/<email>")
def read_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.email + " Título do post: &lt;" + user.post_title + "&gt;"
    else:
        return "Usuário não encontrado", 404


db.create_all()

if __name__ == "__main__":
    app.run()
