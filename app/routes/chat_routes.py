@chat_bp.get("/produtos")
def produtos():
    try:
        catalogo = ProdutoService.listar_produtos()

        opcoes = [
            {
                "id": produto["id"],
                "nome": produto["nome"],
                "descricao": (
                    produto.get("descricao")
                    or "Sem descrição cadastrada."
                ),
            }
            for produto in catalogo
        ]

        sem_estoque = [
            produto["nome"]
            for produto in catalogo
            if produto["quantidade"] <= 0
        ]

        resposta = jsonify(
            produtos=opcoes,
            sem_estoque=sem_estoque,
        )

        resposta.headers["Cache-Control"] = "no-store"

        return resposta

    except Exception as exc:
        current_app.logger.error(
            "Falha ao listar produtos: %s",
            type(exc).__name__,
        )

        return jsonify(
            erro="Não foi possível carregar os produtos. Tente novamente."
        ), 500