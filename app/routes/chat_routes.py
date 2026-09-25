from flask import Blueprint, current_app, jsonify, request

from app.service.ia_service import IAService


chat_bp = Blueprint("chat", __name__)


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
        resposta = IAService.responder(mensagem)

    except ValueError:
        current_app.logger.error(
            "Falha na IA: verifique a configuração de OPENROUTER_API_KEY."
        )

        return jsonify(
            erro="O serviço de IA não está configurado."
        ), 503

    except RuntimeError as exc:
        current_app.logger.error("Falha na IA: %s", exc)

        return jsonify(
            erro=(
                "Não foi possível obter uma resposta da IA. "
                "Tente novamente."
            )
        ), 502

    except Exception as exc:
        current_app.logger.error(
            "Falha no chat: %s", type(exc).__name__
        )

        return jsonify(
            erro="Ocorreu um erro interno ao consultar a loja."
        ), 500

    return jsonify(resposta=resposta), 200