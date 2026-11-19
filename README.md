# Livraria Entrelinhas (Trabalho 2: aplicação Flask)

**Universidade Federal Fluminense**
**Disciplina:** Programação Web
**Professor:** Prof. José Viterbo Filho

Links da entrega:

* Aplicação em execução no PythonAnywhere: `PREENCHER_COM_O_LINK`
* Código no GitHub: https://github.com/Davis-UFF/entrelinhas

---

## 1. Identificação do grupo

**Nome do grupo:** Entrelinhas

**Componentes:**

* Davis Esmael
* Débora Barbosa
* João Pedro Souza
* João Victor Amaral
* Pedro de Araujo Salgado Lopes
* Rafael Lucio Carvalho

**Divisão de tarefas na implementação:**

| Componente | Responsabilidade |
| :-- | :-- |
| `PREENCHER` | Estrutura da aplicação (`create_app`, config, `.env`, `wsgi.py`) e deploy no PythonAnywhere |
| `PREENCHER` | Models e banco de dados (`models.py`, `cli.py` com dados iniciais) |
| `PREENCHER` | Forms e validações (`forms.py`) e rotas de contato, encomendas e clube (`routes.py`) |
| `PREENCHER` | Templates Jinja2 (`base.html`, páginas, macros) e ajustes de CSS/JS |
| `PREENCHER` | Log de debug, painel `/admin` e testes automatizados (`tests/`) |
| `PREENCHER` | README, documentação e revisão final |

---

## 2. Sobre o projeto

Site institucional da **Livraria Entrelinhas**, uma livraria de bairro fictícia com espaço de leitura e café. O Trabalho 1 entregou o site estático em HTML, CSS e Bootstrap. Neste trabalho ele foi convertido em uma aplicação Web dinâmica com **Flask**, com persistência de dados.

O que passou a ser dinâmico:

* Serviços e promoções saem do banco de dados.
* Contato, encomenda de livros e inscrição no Clube de Leitura são gravados no banco.
* Um painel `/admin` protegido por senha lista tudo que foi enviado pelos formulários.

### Requisitos do trabalho

| Requisito | Mínimo | Entregue |
| :-- | :-- | :-- |
| Rotas | 5 | 8 públicas (`/`, `/sobre`, `/servicos`, `/promocoes`, `/endereco`, `/contato`, `/encomendas`, `/clube`) mais `/admin/` |
| Models | 3 | 5 (`Servico`, `Promocao`, `Mensagem`, `Encomenda`, `InscricaoClube`) |
| Forms | 2 | 3 (`ContatoForm`, `EncomendaForm`, `ClubeForm`) |
| Log para debug | sim | `logs/app.log` (arquivo rotativo) e console |

### Tecnologias

Flask, Jinja2, Flask-WTF (formulários e CSRF), Flask-SQLAlchemy (SQLite por padrão), python-dotenv, Bootstrap 5, JavaScript e pytest.

---

## 3. Organização da aplicação

```
entrelinhas/
├── app/
│   ├── __init__.py        # create_app: config, logs, extensões, blueprints, handlers 404/500
│   ├── extensions.py      # instâncias de db (SQLAlchemy) e csrf (CSRFProtect)
│   ├── models.py          # Servico, Promocao, Mensagem, Encomenda, InscricaoClube
│   ├── forms.py           # ContatoForm, EncomendaForm, ClubeForm
│   ├── routes.py          # blueprint "main": rotas públicas
│   ├── admin.py           # blueprint "admin": painel com HTTP Basic
│   ├── cli.py             # dados iniciais (popular) e comando `flask seed`
│   ├── templates/
│   │   ├── base.html      # layout, navbar, mensagens flash, rodapé
│   │   ├── _macros.html   # macros: campo de formulário e banner de página
│   │   ├── index.html, sobre.html, servicos.html, promocoes.html, endereco.html
│   │   ├── contato.html, encomendas.html, clube.html
│   │   ├── admin.html     # tabelas do painel
│   │   └── erro.html      # páginas de erro 404 e 500
│   └── static/
│       ├── css/style.css  # estilos do site
│       ├── js/script.js   # status "aberto agora", contador e rascunho de formulários
│       └── assets/
├── tests/test_app.py      # testes automatizados (pytest)
├── config.py              # classes Config e TestConfig (lê o .env)
├── wsgi.py                # ponto de entrada da aplicação
├── requirements.txt       # dependências
├── .env.example           # modelo das variáveis de ambiente
├── .gitignore
├── instance/              # banco SQLite (criado automaticamente, fora do Git)
└── logs/                  # app.log (criado automaticamente, fora do Git)
```

### Models

| Model | Campos principais | Usado em |
| :-- | :-- | :-- |
| `Servico` | titulo, descricao, ordem | `/servicos`, `/` |
| `Promocao` | titulo, descricao, selo, validade, ativa | `/promocoes`, `/` |
| `Mensagem` | nome, email, assunto, texto, criada_em | `/contato`, `/admin/` |
| `Encomenda` | nome, email, telefone, titulo_livro, autor, observacoes, status | `/encomendas`, `/admin/` |
| `InscricaoClube` | nome, email (único), genero_favorito | `/clube`, `/admin/` |

### Rotas

| Rota | Métodos | Descrição |
| :-- | :-- | :-- |
| `/` | GET | Página inicial com destaque de promoção |
| `/sobre` | GET | História e missão |
| `/servicos` | GET | Lista de serviços vindos do banco |
| `/promocoes` | GET | Promoções ativas vindas do banco |
| `/endereco` | GET | Endereço, tabela de horários e mapa |
| `/contato` | GET, POST | Formulário de contato |
| `/encomendas` | GET, POST | Formulário de encomenda de livro |
| `/clube` | GET, POST | Inscrição no Clube de Leitura |
| `/admin/` | GET | Painel (exige usuário e senha) |

### Log

O log é configurado em `create_app` e grava em `logs/app.log` (rotativo, 1 MB por arquivo, 3 backups) e no console. O nível vem de `LOG_LEVEL` no `.env`. São registrados:

* cada requisição (método, caminho, status e tempo em ms), em nível DEBUG;
* gravações no banco (INFO), falhas de gravação com traceback (ERROR) e rollback;
* formulários inválidos com os erros de validação (DEBUG);
* inscrição duplicada no clube, páginas 404 e tentativas negadas no admin (WARNING).

---

## 4. Como executar localmente

```bash
git clone https://github.com/Davis-UFF/entrelinhas.git
cd entrelinhas
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # edite SECRET_KEY e ADMIN_PASSWORD
flask --app wsgi run --debug
```

Abra http://127.0.0.1:5000. Na primeira execução as tabelas e os dados iniciais (serviços e promoções) são criados automaticamente. Para rodar os testes: `pytest`.

### Variáveis do `.env`

| Variável | Para que serve |
| :-- | :-- |
| `SECRET_KEY` | Assinatura de sessão e token CSRF |
| `DATABASE_URL` | Opcional. Vazio usa `instance/entrelinhas.db` |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`... |
| `ADMIN_USER` e `ADMIN_PASSWORD` | Acesso ao `/admin/`. Sem senha definida, o painel fica desligado |

### Deploy no PythonAnywhere

1. Em um console Bash: `git clone` do repositório e criar o virtualenv com `mkvirtualenv --python=python3.12 entrelinhas` seguido de `pip install -r requirements.txt`.
2. Criar o arquivo `.env` na raiz do projeto com valores de produção.
3. Na aba **Web**, criar um app **Manual configuration**, escolher o virtualenv e editar o arquivo WSGI para conter:

   ```python
   import sys
   sys.path.insert(0, "/home/SEU_USUARIO/entrelinhas")
   from wsgi import app as application
   ```
4. Em **Static files**, mapear `/static/` para `/home/SEU_USUARIO/entrelinhas/app/static`.
5. Clicar em **Reload**.

---

## 5. Guia do usuário

| Quero... | Onde ir | O que acontece |
| :-- | :-- | :-- |
| Conhecer a livraria | **Sobre** | Lê a história e a missão |
| Ver o que a loja oferece | **Explorar > Serviços & Café** | Lista de serviços |
| Ver ofertas e cupons | **Explorar > Promoções do Mês** | Lista de promoções ativas |
| Saber se a loja está aberta | Página inicial ou **Endereço** | Selo "Aberto agora" ou "Fechado" com o horário, e a linha do dia atual destacada |
| Chegar à loja | **Endereço** | Endereço, horários e mapa |
| Enviar dúvida ou sugestão | **Contato** | Preenche nome, e-mail, assunto e mensagem (10 a 1000 caracteres). Aparece "Mensagem enviada!" |
| Pedir um livro que não está na loja | **Explorar > Encomendar um Livro** | Informa título e autor (telefone e observações são opcionais) |
| Entrar no Clube de Leitura | **Explorar > Clube de Leitura** | Informa nome, e-mail e gênero favorito. Cada e-mail só pode se inscrever uma vez |

Dicas sobre os formulários:

* Campos com erro aparecem em vermelho com a explicação logo abaixo, e o que foi digitado é mantido.
* O texto digitado é guardado como rascunho no navegador, então não se perde se a página for fechada sem querer.
* Se a sessão expirar, o envio é recusado (proteção CSRF). Basta recarregar a página e enviar de novo.

### Para a administração da loja

Acessar `/admin/` e informar `ADMIN_USER` e `ADMIN_PASSWORD`. O painel mostra mensagens, encomendas e inscritos do clube, do mais recente para o mais antigo.
