import json

from openai import OpenAI

from app.service.produto_service import ProdutoService


client = OpenAI()


TOOLS = [
    {
        "type": "function",
        "name": "consultar_estoque",
        "description": (
            "Consulta se um produto existe na loja e quantas "
            "unidades estão disponíveis em estoque."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome do produto procurado pelo cliente."
                }
            },
            "required": ["nome"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "consultar_preco",
        "description": "Consulta o preço atual de um produto da loja.",
        "parameters": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome do produto procurado pelo cliente."
                }
            },
            "required": ["nome"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "listar_produtos",
        "description": (
            "Lista os produtos disponíveis no catálogo da loja. "
            "Use quando o cliente perguntar quais produtos existem."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }
]


def executar_ferramenta(nome, argumentos):

    if nome == "consultar_estoque":
        return ProdutoService.consultar_estoque(
            argumentos["nome"]
        )

    if nome == "consultar_preco":
        return ProdutoService.consultar_preco(
            argumentos["nome"]
        )

    if nome == "listar_produtos":
        return ProdutoService.listar_produtos()

    return {
        "erro": "Ferramenta não encontrada."
    }


class IAService:

    @staticmethod
    def responder(mensagem):

        instrucoes = """
        Você é o assistente virtual de uma loja de tecnologia.

        Sua função é ajudar clientes com informações sobre os produtos
        cadastrados na loja.

        Regras importantes:

        - Nunca invente produtos.
        - Nunca invente preços.
        - Nunca invente quantidade em estoque.
        - Sempre utilize as ferramentas disponíveis quando a pergunta
          depender de informações da loja.
        - Se um produto não existir, informe isso claramente.
        - Responda em português do Brasil.
        - Seja simpático, objetivo e profissional.
        """

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instrucoes,
            input=mensagem,
            tools=TOOLS
        )

        chamadas = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not chamadas:
            return response.output_text

        outputs = []

        for chamada in chamadas:

            argumentos = json.loads(chamada.arguments)

            resultado = executar_ferramenta(
                chamada.name,
                argumentos
            )

            outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": chamada.call_id,
                    "output": json.dumps(
                        resultado,
                        ensure_ascii=False
                    )
                }
            )

        resposta_final = client.responses.create(
            model="gpt-5-mini",
            instructions=instrucoes,
            previous_response_id=response.id,
            input=outputs,
            tools=TOOLS
        )

        return resposta_final.output_text