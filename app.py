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
    # TEST: Tendo a chave de um objeto usuario como parte da tabela
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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


@app.route("/new_topic", methods=["GET", "POST"])
def topic():
    if request.method == "POST":
        # Create new topic
        email = request.form["email"]
        title = request.form["title"]
        text = request.form["msg"]
        tpost = TopicPost(email, title, text)
        db.session.add(tpost)
        db.session.commit()
        return "Mensagem de {}, sob o titulo de {}"\
            .format(email, title)
    else:
        # DEBUG: Essa feature so faz sentido por enquanto
        #        criei para que possamos ver se a postagem
        #        funcionou ou nao
        return render_template("new_topic.html")


@app.route("/read/<email>")
def read_email(email):
    tpost = TopicPost.query.filter_by(email=email).first()
    if tpost:
        return tpost.email + " Título do post: &lt;" + tpost.title + "&gt;"
    else:
        return "Usuário não encontrado", 404


db.create_all()

if __name__ == "__main__":
    app.run()
