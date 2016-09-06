# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Iniciando Flask
app = Flask(__name__)
# Iniciando SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class TopicPost(db.Model):
    """
    Define os padrões da postagem em um tópico
    """
    __tablename__ = "topic_post"
    # Chave da tabela
    id = db.Column(db.Integer, primary_key=True)
    # Email do usuario autor do post
    email = db.Column(db.String(120), unique=False, nullable=False)
    # Titulo do post (pode nao ser preenchido)
    title = db.Column(db.String(140), unique=False, nullable=True)
    # Conteudo do post
    text = db.Column(db.String(2000), unique=False, nullable=False)
    # Pontuacao do post
    score = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, email, title, text):
        """
        Construtor
        """
        self.email = email
        self.title = title
        self.text = text
        self.score = 1

    def __repr__(self):
        """
        Representacao do objeto quando for chamado, tratando a possivel
        nao existencia de um titulo
        """
        if self.title is not None:
            return "<{}; {}>".format(self.email, self.title)
        else:
            return "<{}; No title".format(self.email)


class User(db.Model):
    """
    Deprecated
    """
    __tablename__ = "users"
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

    def __repr__(self):
        return "<{}; {}>".format(self.email, self.post_title)


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


# @app.route("/new_topic")
# def new_topic():
#     return render_template("new_topic.html")


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
        return render_template("new_topic.html")


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
