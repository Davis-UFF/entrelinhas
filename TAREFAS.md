# Divisão de tarefas: Trabalho 2

Cinco partes, uma por pessoa. Cada parte mexe em arquivos diferentes, para evitar conflito.

## Plano de entrega

O projeto já cumpre os requisitos do professor: 8 rotas públicas mais o painel, 5 models, 3 forms, log e testes. As seções 2, 3 e 4 são melhorias opcionais. Se alguma não ficar pronta, a entrega não é afetada.

O que é obrigatório para entregar:
- Deploy no PythonAnywhere, com o link no README
- Divisão de tarefas preenchida no README
- Link do código no GitHub

Se alguém não fizer sua parte, o grupo segue sem ela. O deploy é do Pedro. Todo o resto é dos outros.

## 1. Estrutura, banco, forms e log (Pedro)

Já feito:
- [x] Estrutura Flask: `create_app`, `config.py`, `.env`, `wsgi.py`
- [x] 5 models com SQLite criado automaticamente (inclusive a pasta `instance/`)
- [x] 3 forms com validação e CSRF, com `PessoaForm` como base
- [x] Rotas e templates com herança de `base.html` e macros
- [x] Log em `logs/app.log` e no console
- [x] Painel `/admin` com HTTP Basic
- [x] 17 testes com pytest
- [x] README com organização de pastas e tabelas de models, forms e rotas

Falta:
- [ ] Deploy no PythonAnywhere e colocar o link no README

## 2. Visual e responsividade (responsável: A definir)

Só mexe em `app/static/` e nos templates.
- [ ] Trocar o `assets/sample.png` (vazio) por imagens reais
- [ ] Conferir o layout no celular em todas as páginas
- [ ] Acessibilidade: textos alternativos nas imagens, contraste e foco no teclado
- [ ] Ajustar espaçamentos e tamanhos de fonte onde ficar apertado
- [ ] Testar nos navegadores principais (Chrome e Firefox)

## 3. Dados iniciais (responsável: A definir)

Só mexe em `models.py` e `cli.py`.
- [ ] Ampliar a lista de serviços com textos realistas
- [ ] Ampliar as promoções, com selos e validades variados
- [ ] Incluir ao menos uma promoção inativa para testar o filtro `ativa`
- [ ] Conferir se o `popular()` continua sem duplicar dados ao rodar duas vezes
- [ ] Se mudar algum model, avisar o grupo (o banco precisa ser recriado)

## 4. Painel admin (responsável: A definir)

Só mexe em `admin.py` e `admin.html`.
- [ ] Rota para alterar o status da encomenda (pendente, pedida, chegou, entregue)
- [ ] Rota para apagar mensagem, encomenda e inscrição
- [ ] Botões no painel, com confirmação antes de apagar
- [ ] Proteger as novas rotas com `admin_required` e CSRF
- [ ] Registrar as ações no log

## 5. Qualidade e testes (responsável: A definir)

Só mexe em `tests/` e no guia do usuário do README.
- [ ] Mais testes: admin, validações de cada campo e páginas de erro
- [ ] Roteiro de teste manual (passo a passo para o professor)
- [ ] Revisar o guia do usuário no README
- [ ] Depois do deploy, testar os 3 formulários online e o painel `/admin`

## Fechamento (responsável: A definir)
- [ ] Preencher a divisão de tarefas no README
- [ ] Juntar o que cada um enviar e rodar os testes depois de cada junção
- [ ] Conferir o link do código no GitHub antes de entregar

## Regras

1. Cada um trabalha como preferir (branch, fork ou outra forma). O que importa é entregar ao professor dentro do prazo.
2. Rode `python -m pytest -q` antes de enviar. Tudo deve passar.
3. Nunca commite `.env`, `instance/` nem `logs/`.
