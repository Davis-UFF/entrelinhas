"""Models (SQLAlchemy) da Livraria Entrelinhas."""
from datetime import datetime, timezone

from .extensions import db


def agora():
    return datetime.now(timezone.utc)


class Servico(db.Model):
    """Serviço oferecido pela livraria (venda, encomenda, clube, café)."""

    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ordem = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Servico {self.titulo}>"


class Promocao(db.Model):
    """Oferta, combo ou cupom exibido na página de promoções."""

    __tablename__ = "promocoes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    selo = db.Column(db.String(30), nullable=False)  # ex.: "20% OFF", "Cupom LEIA10"
    validade = db.Column(db.String(80), nullable=False, default="Válido até o fim do mês")
    ativa = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Promocao {self.titulo}>"


class Mensagem(db.Model):
    """Mensagem enviada pelo formulário de contato."""

    __tablename__ = "mensagens"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    assunto = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.String(1000), nullable=False)
    criada_em = db.Column(db.DateTime, nullable=False, default=agora)

    def __repr__(self):
        return f"<Mensagem {self.id} de {self.email}>"


class Encomenda(db.Model):
    """Pedido de um título que não está no acervo."""

    __tablename__ = "encomendas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    titulo_livro = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False, default="pendente")
    criada_em = db.Column(db.DateTime, nullable=False, default=agora)

    def __repr__(self):
        return f"<Encomenda {self.id} {self.titulo_livro}>"


class InscricaoClube(db.Model):
    """Inscrição no Clube de Leitura (e-mail único)."""

    __tablename__ = "inscricoes_clube"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    genero_favorito = db.Column(db.String(40), nullable=False)
    criada_em = db.Column(db.DateTime, nullable=False, default=agora)

    def __repr__(self):
        return f"<InscricaoClube {self.email}>"
