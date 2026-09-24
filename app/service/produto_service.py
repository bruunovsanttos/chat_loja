from app.models.produto import Produto


class ProdutoService:

    @staticmethod
    def buscar_produto(nome):
        return Produto.query.filter(
            Produto.nome.ilike(f"%{nome}%")
        ).first()

    @staticmethod
    def consultar_estoque(nome):
        produto = ProdutoService.buscar_produto(nome)

        if not produto:
            return {
                "encontrado": False,
                "mensagem": "Produto não encontrado."
            }

        return {
            "encontrado": True,
            "produto": produto.nome,
            "quantidade": produto.quantidade,
            "disponivel": produto.quantidade > 0
        }

    @staticmethod
    def consultar_preco(nome):
        produto = ProdutoService.buscar_produto(nome)

        if not produto:
            return {
                "encontrado": False,
                "mensagem": "Produto não encontrado."
            }

        return {
            "encontrado": True,
            "produto": produto.nome,
            "preco": produto.preco
        }

    @staticmethod
    def listar_produtos():
        produtos = Produto.query.all()

        return [produto.to_dict() for produto in produtos]