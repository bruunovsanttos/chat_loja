from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
)

from app.service.ia_service import IAService, validar_historico
from app.service.produto_service import ProdutoService


chat_bp = Blueprint("chat", __name__)


@chat_bp.get("/")
def index():
    return render_template("chat.html")


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


@chat_bp.post("/chat")
def chat():
    if not request.is_json:
        return jsonify(
            erro="Envie o corpo como application/json."
        ), 415

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify(
            erro="Envie um objeto JSON válido."
        ), 400

    mensagem = dados.get("mensagem")

    if not isinstance(mensagem, str) or not mensagem.strip():
        return jsonify(
            erro="O campo mensagem deve ser um texto não vazio."
        ), 400

    mensagem = mensagem.strip()

    if len(mensagem) > 2000:
        return jsonify(
            erro="A mensagem deve ter no máximo 2000 caracteres."
        ), 400

    try:
        historico = validar_historico(
            dados.get("historico", [])
        )

    except ValueError:
        return jsonify(
            erro="Histórico inválido. Inicie uma nova conversa."
        ), 400

    try:
        resposta = IAService.responder(
            mensagem,
            historico,
        )

    except ValueError:
        current_app.logger.error(
            "Falha na IA: verifique OPENROUTER_API_KEY."
        )

        return jsonify(
            erro="O atendimento está indisponível no momento."
        ), 503

    except RuntimeError as exc:
        current_app.logger.error(
            "Falha na IA: %s",
            exc,
        )

        return jsonify(
            erro="Não foi possível responder agora. Tente novamente."
        ), 502

    except Exception as exc:
        current_app.logger.error(
            "Falha no chat: %s",
            type(exc).__name__,
        )

        return jsonify(
            erro="Não foi possível consultar a loja. Tente novamente."
        ), 500

    return jsonify(resposta=resposta), 200