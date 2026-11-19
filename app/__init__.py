"""Fábrica da aplicação Flask da Livraria Entrelinhas."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, render_template, request
from sqlalchemy.engine import make_url

from config import Config

from .extensions import csrf, db


def configurar_logs(app):
    """Logs em arquivo rotativo (logs/app.log) e no console, para debug."""
    nivel = getattr(logging, app.config["LOG_LEVEL"], logging.DEBUG)
    formato = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s"
    )

    app.config["LOG_DIR"].mkdir(parents=True, exist_ok=True)
    arquivo = RotatingFileHandler(
        app.config["LOG_DIR"] / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    arquivo.setFormatter(formato)
    arquivo.setLevel(nivel)

    console = logging.StreamHandler()
    console.setFormatter(formato)
    console.setLevel(nivel)

    app.logger.handlers.clear()
    app.logger.addHandler(arquivo)
    app.logger.addHandler(console)
    app.logger.setLevel(nivel)


def garantir_pasta_do_banco(app):
    """SQLite não cria pastas: garante que o diretório do arquivo .db exista (ex.: instance/)."""
    url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    if url.drivername.startswith("sqlite") and url.database not in (None, "", ":memory:"):
        Path(url.database).parent.mkdir(parents=True, exist_ok=True)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get("TESTING"):
        configurar_logs(app)
    else:
        app.logger.setLevel(logging.DEBUG)

    garantir_pasta_do_banco(app)
    db.init_app(app)
    csrf.init_app(app)

    from .admin import bp as admin_bp
    from .routes import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    from . import models  # noqa: F401  (registra os models antes do create_all)

    with app.app_context():
        db.create_all()
        app.logger.info("Banco pronto: %s", app.config["SQLALCHEMY_DATABASE_URI"])
        if not app.config.get("TESTING"):
            from .cli import popular

            popular()  # só insere se as tabelas estiverem vazias

    @app.after_request
    def log_requisicao(resposta):
        if not request.path.startswith("/static"):
            app.logger.debug("%s %s -> %s", request.method, request.path, resposta.status_code)
        return resposta

    @app.errorhandler(404)
    def erro_404(erro):
        app.logger.warning("404 em %s", request.path)
        return render_template("erro.html", codigo=404, mensagem="Página não encontrada."), 404

    @app.errorhandler(500)
    def erro_500(erro):
        return render_template("erro.html", codigo=500, mensagem="Algo deu errado do nosso lado."), 500

    return app
