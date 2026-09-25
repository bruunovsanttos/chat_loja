const form = document.querySelector("#form-chat");
const campo = document.querySelector("#mensagem");
const contador = document.querySelector("#contador");
const mensagens = document.querySelector("#mensagens");
const statusChat = document.querySelector("#status");
const painel = document.querySelector(".painel");
const menu = document.querySelector("#menu");
const selecao = document.querySelector("#selecao");
const lista = document.querySelector("#lista-produtos");
const tituloSelecao = document.querySelector("#titulo-selecao");

let ocupado = false;
let historico = [];


function atualizarContador() {
  contador.textContent = campo.value.length + "/2000";
  campo.setCustomValidity("");
}


function definirEspera(esperando, texto = "") {
  ocupado = esperando;
  campo.readOnly = esperando;

  painel.querySelectorAll("button").forEach((botao) => {
    botao.disabled = esperando;
  });

  statusChat.textContent = texto;
}


function adicionarMensagem(texto, tipo) {
  const artigo = document.createElement("article");
  artigo.className = "mensagem " + tipo;

  const autor = document.createElement("span");
  autor.className = "autor";
  autor.textContent = tipo === "usuario" ? "VOCÊ" : "LOJA";

  const balao = document.createElement("div");
  balao.className = "balao";

  const paragrafo = document.createElement("p");

  // Mostra negrito sem interpretar HTML enviado pela IA.
  const partes = tipo === "assistente"
    ? texto.split(/(\*\*[^*]+\*\*)/g)
    : [texto];

  for (const parte of partes) {
    if (
      tipo === "assistente" &&
      parte.startsWith("**") &&
      parte.endsWith("**")
    ) {
      const strong = document.createElement("strong");
      strong.textContent = parte.slice(2, -2);
      paragrafo.append(strong);
    } else {
      paragrafo.append(document.createTextNode(parte));
    }
  }

  balao.append(paragrafo);
  artigo.append(autor, balao);
  mensagens.append(artigo);

  mensagens.scrollTop = mensagens.scrollHeight;
}


async function requisitar(url, opcoes = {}, tempo = 180000) {
  const controller = new AbortController();

  const limite = setTimeout(() => {
    controller.abort();
  }, tempo);

  try {
    const resposta = await fetch(url, {
      ...opcoes,
      signal: controller.signal,
    });

    const dados = await resposta.json().catch(() => null);

    if (!resposta.ok) {
      throw new Error(
        typeof dados?.erro === "string"
          ? dados.erro
          : "Não foi possível consultar a loja. Tente novamente."
      );
    }

    if (!dados) {
      throw new Error(
        "A loja retornou uma resposta inválida."
      );
    }

    return dados;

  } catch (erro) {
    if (erro.name === "AbortError") {
      throw new Error(
        "A consulta demorou demais. Aguarde um pouco e tente novamente."
      );
    }

    if (erro instanceof TypeError) {
      throw new Error(
        "Não foi possível conectar à loja. Verifique sua conexão."
      );
    }

    throw erro;

  } finally {
    clearTimeout(limite);
  }
}


function mostrarMenu() {
  menu.hidden = false;
  selecao.hidden = true;
}


async function enviar(mensagem, digitada = false) {
  if (ocupado) {
    return;
  }

  mostrarMenu();

  definirEspera(
    true,
    "Consultando a loja. Aguarde um instante…"
  );

  adicionarMensagem(mensagem, "usuario");

  try {
    const dados = await requisitar(form.dataset.url, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        mensagem,
        historico,
      }),
    });

    if (
      typeof dados.resposta !== "string" ||
      !dados.resposta.trim()
    ) {
      throw new Error(
        "Não recebemos uma resposta. Tente novamente."
      );
    }

    adicionarMensagem(dados.resposta, "assistente");

    // Guarda somente interações concluídas com sucesso.
    historico.push(
      {
        role: "user",
        content: mensagem,
      },
      {
        role: "assistant",
        content: dados.resposta.slice(0, 8000),
      }
    );

    // Mantém as últimas seis perguntas e respostas.
    historico = historico.slice(-12);

    if (digitada) {
      campo.value = "";
      atualizarContador();
    }

  } catch (erro) {
    adicionarMensagem(erro.message, "erro");

  } finally {
    definirEspera(false);

    if (digitada) {
      campo.focus();
    } else {
      menu.querySelector("button").focus();
    }
  }
}


async function escolherProduto(acao) {
  if (ocupado) {
    return;
  }

  definirEspera(true, "Carregando os produtos…");

  let carregou = false;

  try {
    const dados = await requisitar(
      form.dataset.produtosUrl,
      { cache: "no-store" },
      15000
    );

    if (!Array.isArray(dados.produtos)) {
      throw new Error(
        "Não foi possível carregar os produtos."
      );
    }

    lista.replaceChildren();

    const titulos = {
      catalogo: "Qual produto você quer conhecer?",
      preco: "De qual produto você quer saber o preço?",
      estoque: "Qual produto você quer consultar?",
    };

    tituloSelecao.textContent = titulos[acao];

    if (dados.produtos.length === 0) {
      const aviso = document.createElement("p");
      aviso.textContent = "Ainda não há produtos cadastrados.";
      lista.append(aviso);
    }

    for (const produto of dados.produtos) {
      const botao = document.createElement("button");
      botao.type = "button";
      botao.className = "opcao-produto";

      const nome = document.createElement("strong");
      nome.textContent = produto.nome;

      const categoria = document.createElement("span");
      categoria.textContent = produto.categoria;

      botao.append(nome, categoria);

      botao.addEventListener("click", () => {
        const perguntas = {
          catalogo:
            "Quero conhecer o produto " + produto.nome +
            ". Qual é a descrição, o preço e a disponibilidade?",

          preco:
            "Qual é o preço do produto " + produto.nome + "?",

          estoque:
            "Quantas unidades do produto " + produto.nome +
            " estão disponíveis?",
        };

        enviar(perguntas[acao]);
      });

      lista.append(botao);
    }

    menu.hidden = true;
    selecao.hidden = false;
    carregou = true;

  } catch (erro) {
    adicionarMensagem(erro.message, "erro");
    mostrarMenu();

  } finally {
    definirEspera(false);

    if (carregou) {
      tituloSelecao.focus();
    }
  }
}


menu.querySelectorAll("[data-acao]").forEach((botao) => {
  botao.addEventListener("click", () => {
    escolherProduto(botao.dataset.acao);
  });
});


document.querySelector("#voltar").addEventListener("click", () => {
  if (ocupado) {
    return;
  }

  mostrarMenu();
  menu.querySelector("button").focus();
});


campo.addEventListener("input", atualizarContador);


campo.addEventListener("keydown", (evento) => {
  if (
    evento.key === "Enter" &&
    !evento.shiftKey &&
    !evento.isComposing
  ) {
    evento.preventDefault();

    if (!ocupado) {
      form.requestSubmit();
    }
  }
});


form.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const mensagem = campo.value.trim();

  if (!mensagem || mensagem.length > 2000) {
    campo.setCustomValidity(
      "Escreva uma mensagem de até 2000 caracteres."
    );

    campo.reportValidity();
    return;
  }

  enviar(mensagem, true);
});


document.querySelector("#nova-conversa").addEventListener(
  "click",
  () => {
    if (ocupado) {
      return;
    }

    historico = [];
    mensagens.replaceChildren();

    adicionarMensagem(
      "Olá! Escolha uma opção abaixo ou escreva sua pergunta.",
      "assistente"
    );

    campo.value = "";
    atualizarContador();
    mostrarMenu();
    campo.focus();
  }
);