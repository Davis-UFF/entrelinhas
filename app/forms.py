"""Formulários (Flask-WTF) da aplicação."""
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, ValidationError

from .models import InscricaoClube

GENEROS = [
    ("", "Selecione..."),
    ("romance", "Romance"),
    ("ficcao", "Ficção científica e fantasia"),
    ("policial", "Policial e suspense"),
    ("classicos", "Clássicos"),
    ("nao-ficcao", "Não ficção"),
    ("poesia", "Poesia"),
    ("infantil", "Infantojuvenil"),
]


def limpar(valor):
    """Filtro: tira espaços das pontas (ignora None)."""
    return valor.strip() if isinstance(valor, str) else valor


def limpar_ou_none(valor):
    """Filtro para campos opcionais: texto vazio vira None (NULL no banco)."""
    return limpar(valor) or None


def limpar_email(valor):
    return limpar(valor).lower() if isinstance(valor, str) else valor


class PessoaForm(FlaskForm):
    """Campos que os três formulários têm em comum."""

    nome = StringField(
        "Nome", filters=[limpar], validators=[DataRequired("Informe seu nome."), Length(max=100)]
    )
    email = StringField(
        "E-mail",
        filters=[limpar_email],
        validators=[DataRequired("Informe seu e-mail."), Email("E-mail inválido."), Length(max=120)],
    )


class ContatoForm(PessoaForm):
    assunto = StringField(
        "Assunto", filters=[limpar], validators=[DataRequired("Informe o assunto."), Length(max=100)]
    )
    texto = TextAreaField(
        "Mensagem",
        filters=[limpar],
        validators=[
            DataRequired("Escreva sua mensagem."),
            Length(min=10, max=1000, message="A mensagem deve ter entre 10 e 1000 caracteres."),
        ],
    )


class EncomendaForm(PessoaForm):
    telefone = StringField(
        "Telefone (opcional)",
        filters=[limpar_ou_none],
        validators=[
            Optional(),
            Regexp(r"^[\d\s()+-]{8,20}$", message="Use apenas números, espaços, ( ) + e -."),
        ],
    )
    titulo_livro = StringField(
        "Título do livro", filters=[limpar], validators=[DataRequired("Informe o título."), Length(max=150)]
    )
    autor = StringField(
        "Autor", filters=[limpar], validators=[DataRequired("Informe o autor."), Length(max=100)]
    )
    observacoes = TextAreaField(
        "Observações (edição, editora, etc.)",
        filters=[limpar_ou_none],
        validators=[Optional(), Length(max=500)],
    )


class ClubeForm(PessoaForm):
    genero_favorito = SelectField(
        "Gênero favorito",
        choices=GENEROS,
        validators=[DataRequired("Escolha um gênero.")],
    )

    def validate_email(self, campo):
        """Validador inline: o WTForms chama validate_<campo> sozinho."""
        if InscricaoClube.query.filter_by(email=campo.data).first():
            raise ValidationError("Este e-mail já está inscrito no clube.")
