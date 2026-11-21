import hmac
from functools import wraps

from flask import Blueprint, Response, abort, current_app, render_template, request

from .models import Encomenda, InscricaoClube, Mensagem

bp = Blueprint("admin", __name__, url_prefix="/admin")


def _exigir_login():
    return Response(
        "Acesso restrito.", 401, {"WWW-Authenticate": 'Basic realm="Entrelinhas admin"'}
    )


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        senha = current_app.config["ADMIN_PASSWORD"]
        if not senha:  # sem senha, painel desligado
            abort(404)
        auth = request.authorization
        usuario_ok = auth and hmac.compare_digest(auth.username or "", current_app.config["ADMIN_USER"])
        senha_ok = auth and hmac.compare_digest(auth.password or "", senha)
        if not (usuario_ok and senha_ok):
            current_app.logger.warning("Tentativa de acesso ao admin negada (%s)", request.remote_addr)
            return _exigir_login()
        return view(*args, **kwargs)

    return wrapper


@bp.route("/")
@admin_required
def painel():
    current_app.logger.info("Admin acessou o painel")
    return render_template(
        "admin.html",
        mensagens=Mensagem.query.order_by(Mensagem.criada_em.desc()).all(),
        encomendas=Encomenda.query.order_by(Encomenda.criada_em.desc()).all(),
        inscricoes=InscricaoClube.query.order_by(InscricaoClube.criada_em.desc()).all(),
    )
