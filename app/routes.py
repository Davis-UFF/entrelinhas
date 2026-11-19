"""Rotas públicas do site."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from .extensions import db
from .forms import ClubeForm, ContatoForm, EncomendaForm
from .models import Encomenda, InscricaoClube, Mensagem, Promocao, Servico

bp = Blueprint("main", __name__)

HORARIOS = [
    {"dias": "1,2,3,4,5", "rotulo": "Segunda a Sexta", "horario": "09h às 20h"},
    {"dias": "6", "rotulo": "Sábado", "horario": "09h às 14h"},
    {"dias": "0", "rotulo": "Domingo", "horario": "Fechado"},
]


def tratar_form(form, model, template, sucesso, **contexto):
    """Fluxo comum dos formulários: valida, grava, avisa e redireciona (padrão PRG)."""
    if form.validate_on_submit():
        dados = {campo: valor for campo, valor in form.data.items() if campo != "csrf_token"}
        registro = model(**dados)
        try:
            db.session.add(registro)
            db.session.commit()
        except IntegrityError:
            # Corrida: outro pedido gravou o mesmo e-mail entre a validação e o commit
            db.session.rollback()
            current_app.logger.warning("Violação de integridade ao salvar %s", model.__name__)
            form.email.errors.append("Este e-mail já está inscrito.")
        else:
            current_app.logger.info("%s salvo(a) com id=%s", model.__name__, registro.id)
            flash(sucesso, "success")
            return redirect(url_for(request.endpoint))
    elif form.is_submitted():
        current_app.logger.debug("%s inválido(a): %s", model.__name__, form.errors)
    return render_template(template, form=form, **contexto)


@bp.route("/")
def index():
    servicos = Servico.query.order_by(Servico.ordem).limit(3).all()
    promocoes = Promocao.query.filter_by(ativa=True).limit(3).all()
    return render_template("index.html", servicos=servicos, promocoes=promocoes)


@bp.route("/sobre")
def sobre():
    return render_template("sobre.html")


@bp.route("/servicos")
def servicos():
    lista = Servico.query.order_by(Servico.ordem).all()
    return render_template("servicos.html", servicos=lista)


@bp.route("/promocoes")
def promocoes():
    lista = Promocao.query.filter_by(ativa=True).order_by(Promocao.id).all()
    return render_template("promocoes.html", promocoes=lista)


@bp.route("/endereco")
def endereco():
    return render_template("endereco.html", horarios=HORARIOS)


@bp.route("/contato", methods=["GET", "POST"])
def contato():
    return tratar_form(
        ContatoForm(), Mensagem, "contato.html", "Mensagem enviada! Responderemos em breve."
    )


@bp.route("/encomendas", methods=["GET", "POST"])
def encomendas():
    return tratar_form(
        EncomendaForm(), Encomenda, "encomendas.html",
        "Encomenda registrada! Avisaremos quando o livro chegar.",
    )


@bp.route("/clube", methods=["GET", "POST"])
def clube():
    return tratar_form(
        ClubeForm(), InscricaoClube, "clube.html", "Bem-vindo(a) ao Clube de Leitura!",
        total=InscricaoClube.query.count(),
    )
