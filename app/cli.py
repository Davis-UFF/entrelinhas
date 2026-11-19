"""Dados iniciais do site (serviços e promoções)."""
from .extensions import db
from .models import Promocao, Servico

SERVICOS = [
    ("Venda de Livros", "Um acervo variado com literatura nacional e internacional, lançamentos e clássicos, sempre com a curadoria da nossa equipe."),
    ("Encomendas de Títulos", "Não achou o livro que procurava nas prateleiras? Encomendamos diretamente com as editoras e avisamos assim que chegar."),
    ("Clube de Leitura", "Encontros mensais para discutir uma obra escolhida pelo grupo, com direito a café e boas conversas."),
    ("Café Literário", "Um cantinho aconchegante para tomar um café artesanal enquanto lê, trabalha ou espera por um amigo."),
]

PROMOCOES = [
    ("Combo Clássicos", "Leve 3 clássicos da literatura por um preço especial e monte sua estante dos sonhos.", "20% OFF", "Válido até o fim do mês"),
    ("10% de Desconto", "Use o cupom LEIA10 e ganhe 10% de desconto em compras acima de R$ 80.", "Cupom LEIA10", "Válido até o fim do mês"),
    ("Clube do Livro", "Membros do Clube de Leitura ganham 15% de desconto em todas as compras na loja.", "15% OFF", "Promoção fixa para associados"),
]


def popular():
    """Insere os dados iniciais se as tabelas estiverem vazias. Retorna (servicos, promocoes) criados."""
    novos_s = novas_p = 0
    if Servico.query.count() == 0:
        for ordem, (titulo, desc) in enumerate(SERVICOS, start=1):
            db.session.add(Servico(titulo=titulo, descricao=desc, ordem=ordem))
            novos_s += 1
    if Promocao.query.count() == 0:
        for titulo, desc, selo, validade in PROMOCOES:
            db.session.add(Promocao(titulo=titulo, descricao=desc, selo=selo, validade=validade))
            novas_p += 1
    db.session.commit()
    return novos_s, novas_p

