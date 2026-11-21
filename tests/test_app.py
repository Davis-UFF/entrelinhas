import base64

import pytest

from app import create_app
from app.cli import popular
from app.extensions import db
from app.models import Encomenda, InscricaoClube, Mensagem
from config import TestConfig


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        popular()
        yield app.test_client()
        db.session.remove()


def auth(user="admin", senha="senha-teste"):
    token = base64.b64encode(f"{user}:{senha}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


@pytest.mark.parametrize(
    "rota", ["/", "/sobre", "/servicos", "/promocoes", "/endereco", "/contato", "/encomendas", "/clube"]
)
def test_paginas_publicas(client, rota):
    assert client.get(rota).status_code == 200


def test_servicos_e_promocoes_vem_do_banco(client):
    assert b"Caf\xc3\xa9 Liter\xc3\xa1rio" in client.get("/servicos").data
    assert b"LEIA10" in client.get("/promocoes").data


def test_404(client):
    assert client.get("/nao-existe").status_code == 404


def test_contato_valido_grava(client):
    r = client.post(
        "/contato",
        data={"nome": "Ana", "email": "ANA@exemplo.com", "assunto": "Oi", "texto": "Gostei muito da loja!"},
    )
    assert r.status_code == 302
    m = Mensagem.query.one()
    assert m.email == "ana@exemplo.com"


def test_contato_invalido_nao_grava(client):
    r = client.post("/contato", data={"nome": "", "email": "x", "assunto": "", "texto": "curta"})
    assert r.status_code == 200
    assert Mensagem.query.count() == 0
    assert "E-mail inválido".encode() in r.data


def test_encomenda_grava_e_telefone_opcional(client):
    r = client.post(
        "/encomendas",
        data={"nome": "Bia", "email": "bia@x.com", "titulo_livro": "Dom Casmurro", "autor": "Machado de Assis"},
    )
    assert r.status_code == 302
    e = Encomenda.query.one()
    assert e.telefone is None and e.status == "pendente"


def test_clube_bloqueia_email_duplicado(client):
    dados = {"nome": "Caio", "email": "caio@x.com", "genero_favorito": "romance"}
    assert client.post("/clube", data=dados).status_code == 302
    r = client.post("/clube", data=dados)
    assert r.status_code == 200
    assert "já está inscrito".encode() in r.data
    assert InscricaoClube.query.count() == 1


def test_integrity_error_reexibe_formulario(client, monkeypatch):
    # faz o commit falhar como se o e-mail já existisse
    from sqlalchemy.exc import IntegrityError

    def commit_falha():
        raise IntegrityError("INSERT", {}, Exception("UNIQUE constraint failed"))

    monkeypatch.setattr(db.session, "commit", commit_falha)
    r = client.post("/clube", data={"nome": "Duda", "email": "duda@x.com", "genero_favorito": "poesia"})
    assert r.status_code == 200
    assert "Este e-mail já está inscrito.".encode() in r.data
    assert InscricaoClube.query.count() == 0


def test_admin_exige_autenticacao(client):
    assert client.get("/admin/").status_code == 401
    assert client.get("/admin/", headers=auth(senha="errada")).status_code == 401
    assert client.get("/admin/", headers=auth()).status_code == 200


def test_app_cria_pasta_do_banco_com_config_normal(tmp_path):
    # simula um clone novo, onde instance/ ainda não existe
    from sqlalchemy import inspect

    from config import Config

    class ConfigTemporaria(Config):
        # a subpasta ainda não existe
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(tmp_path / "instance" / "teste.db")
        LOG_DIR = tmp_path / "logs"

    app = create_app(ConfigTemporaria)
    try:
        assert (tmp_path / "instance" / "teste.db").exists()
        with app.app_context():
            tabelas = set(inspect(db.engine).get_table_names())
            assert {"servicos", "promocoes", "mensagens", "encomendas", "inscricoes_clube"} <= tabelas
            db.session.remove()
            db.engine.dispose()
        assert app.test_client().get("/").status_code == 200
    finally:
        app.logger.handlers.clear()
