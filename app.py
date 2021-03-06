# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Iniciando Flask
app = Flask(__name__)
# Iniciando SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Definindo temas possíveis (será utilizado para conferir se o url
# desejado é ou não plausível)
themes = [
    "Administração",
    "Economia",
    "Engenharia",
    "Outros",
    "Achados e Perdidos",
    "Clubes",
    "Entidades",
    "Atlética",
    "Consilium Insper",
    "Design Challenge",
    "Diretório Acadêmico",
    "Enactus",
    "GAS",
    "inFinance",
    "Insper Post",
    "Liga de Empreendedores",
    "Sementes Culturais"
]


class User(db.Model):
    """
    Usuario do forum
    Ainda nao utilizado, nao faz sentido enquanto
    nao houver um modelo de login completo
    """
    __tablename__ = "user"
    # Chave primaria da tabela
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=False, nullable=False)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, email, nome):
        self.email = email
        self.nome = nome

    def __repr__(self):
        """
        Representacao do objeto ao ser printado
        """
        return "<{}>".format(self.nome)


class TopicPost(db.Model):
    """
    Define os padrões da postagem em um tópico
    """
    __tablename__ = "post"
    # Chave da tabela
    id = db.Column(db.Integer, primary_key=True)
    # Email do usuario autor do post
    email = db.Column(db.String(120), unique=False, nullable=False)
    # Titulo do post (pode nao ser preenchido)
    title = db.Column(db.String(140), unique=True, nullable=False)
    # Conteudo do post
    text = db.Column(db.String(2000), unique=False, nullable=False)
    # Pontuacao do post
    score = db.Column(db.Integer, unique=False, nullable=False)
    # Categoria do topico
    category = db.Column(db.String(20), unique=False, nullable=False)
    # Tema do topico
    theme = db.Column(db.String(20), unique=False, nullable=False)

    def __init__(self, email, title, text, category, theme):
        """
        Construtor
        """
        self.email = email
        self.title = title
        self.text = text
        self.category = category
        self.theme = theme
        self.score = 1

    def __repr__(self):
        """
        Representacao do objeto
        """
        return "<{}; {}>".format(self.email, self.title)


class TopicResponse(db.Model):
    """
    Respostas ao topico (diferente da postagem original)
    """
    __tablename__ = "response"
    # Chave da tabela
    id = db.Column(db.Integer, primary_key=True)
    # Email do usuario autor do post
    email = db.Column(db.String(120), unique=False, nullable=False)
    # Titulo do post (pode nao ser preenchido)
    title = db.Column(db.String(140), nullable=True)
    # Conteudo do post
    text = db.Column(db.String(2000), unique=False, nullable=False)
    # Pontuacao do post
    score = db.Column(db.Integer, unique=False, nullable=False)
    # Chave extrangeira
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post = db.relationship("TopicPost")

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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/section/adm")
def adm():
    return render_template("adm.html")


@app.route("/section/eco")
def eco():
    return render_template("eco.html")


@app.route("/section/eng")
def eng():
    return render_template("eng.html")


@app.route("/section/outrosa")
def outrosa():
    return render_template("outrosa.html")


@app.route("/section/aep")
def aep():
    return render_template("aep.html")


@app.route("/section/club")
def club():
    return render_template("club.html")


@app.route("/section/outross")
def outross():
    return render_template("outross.html")


@app.route("/section/outros")
def outros():
    return render_template("outros.html")


@app.route("/section/atl")
def atl():
    return render_template("atl.html")


@app.route("/section/cons")
def cons():
    return render_template("cons.html")


@app.route("/section/desc")
def desc():
    return render_template("desc.html")


@app.route("/section/da")
def da():
    return render_template("da.html")


@app.route("/section/enac")
def enac():
    return render_template("enac.html")


@app.route("/section/gas")
def gas():
    return render_template("gas.html")


@app.route("/section/inf")
def inf():
    return render_template("inf.html")


@app.route("/section/inspo")
def inspo():
    return render_template("inspo.html")


@app.route("/section/liga")
def liga():
    return render_template("liga.html")


@app.route("/section/sement")
def sement():
    return render_template("sement.html")


@app.route("/new_topic", methods=["GET", "POST"])
def topic():
    if request.method == "POST":
        # Create new topic
        email = request.form["email"]
        title = request.form["title"]
        text = request.form["msg"]
        category = request.form["category"]
        theme = request.form["theme"]
        tpost = TopicPost(email, title, text, category, theme)
        db.session.add(tpost)
        db.session.commit()
        return render_template("topic_view.html",
                               senddata=TopicPost.query
                               .filter_by(theme=theme),
                               theme=theme.title())
        # return "Mensagem de {}, sob o titulo de {}"\
        #     .format(email, title)
    else:
        # DEBUG: Essa feature so faz sentido por enquanto
        #        criei para que possamos ver se a postagem
        #        funcionou ou nao
        return render_template("new_topic.html")


@app.route("/read/<email>")
def read_email(email):
    tpost = TopicPost.query.filter_by(email=email).first()
    if tpost:
        # [print(p.title) for p in TopicPost.query]  # DEBUG
        return str([p.title for p in TopicPost.query])
    else:
        return "Usuário não encontrado", 404


@app.route("/<theme>/thread")
def read_topic(theme):
    global themes
    if theme in themes:
        return render_template("topic_view.html",
                               senddata=TopicPost.query
                               .filter_by(theme=theme),
                               theme=theme.title())
    else:
        return "Tema não encontrado, seu burro", 404


db.create_all()

if __name__ == "__main__":
    app.run()
