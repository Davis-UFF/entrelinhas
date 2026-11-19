// ============================================
// Status de funcionamento da loja ("Aberto agora" / "Fechado")
// ============================================

// Horário da loja por dia da semana (0 = domingo ... 6 = sábado), em horas
// decimais. Fonte única de verdade: altere aqui se o horário mudar.
const HORARIOS = {
  0: null,                        // Domingo: fechado
  1: { abre: 9, fecha: 20 },
  2: { abre: 9, fecha: 20 },
  3: { abre: 9, fecha: 20 },
  4: { abre: 9, fecha: 20 },
  5: { abre: 9, fecha: 20 },
  6: { abre: 9, fecha: 14 },      // Sábado
};

const NOMES_DIAS = ["domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"];

// Data/hora atual no fuso da loja (Niterói), independente do fuso do visitante.
function agoraNaLoja() {
  const partes = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/Sao_Paulo",
    weekday: "short",
    hour: "numeric",
    minute: "numeric",
    hourCycle: "h23",
  }).formatToParts(new Date());

  const valor = (tipo) => partes.find((p) => p.type === tipo).value;
  const dia = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(valor("weekday"));
  return { dia, hora: Number(valor("hour")) + Number(valor("minute")) / 60 };
}

function formatarHora(h) {
  const horas = Math.floor(h);
  const minutos = Math.round((h - horas) * 60);
  return minutos ? `${horas}h${String(minutos).padStart(2, "0")}` : `${horas}h`;
}

function calcularStatus() {
  const { dia, hora } = agoraNaLoja();
  const hoje = HORARIOS[dia];

  if (hoje && hora >= hoje.abre && hora < hoje.fecha) {
    return { aberto: true, dia, texto: `Aberto agora · fecha às ${formatarHora(hoje.fecha)}` };
  }

  if (hoje && hora < hoje.abre) {
    return { aberto: false, dia, texto: `Fechado · abre hoje às ${formatarHora(hoje.abre)}` };
  }

  // Procura o próximo dia com expediente
  for (let i = 1; i <= 7; i++) {
    const proximo = (dia + i) % 7;
    if (HORARIOS[proximo]) {
      const quando = i === 1 ? "amanhã" : NOMES_DIAS[proximo];
      return { aberto: false, dia, texto: `Fechado · abre ${quando} às ${formatarHora(HORARIOS[proximo].abre)}` };
    }
  }

  return { aberto: false, dia, texto: "Fechado" };
}

function atualizarStatusLoja() {
  const status = calcularStatus();

  document.querySelectorAll(".status-loja").forEach((el) => {
    el.textContent = status.texto;
    el.classList.toggle("aberto", status.aberto);
    el.classList.toggle("fechado", !status.aberto);
  });

  // Destaca na tabela a linha correspondente ao dia de hoje
  document.querySelectorAll(".table-horarios tbody tr[data-dias]").forEach((linha) => {
    const dias = linha.dataset.dias.split(",").map(Number);
    linha.classList.toggle("hoje", dias.includes(status.dia));
  });
}

if (document.querySelector(".status-loja, .table-horarios")) {
  atualizarStatusLoja();
  setInterval(atualizarStatusLoja, 60 * 1000);
}

// ============================================
// Formulários (contato, encomenda, clube): contador de caracteres e
// rascunho automático. A validação real é feita no servidor (Flask-WTF);
// aqui só melhoramos a experiência de quem está digitando.
// ============================================

document.querySelectorAll("form[data-rascunho]").forEach((form) => {
  const chave = `entrelinhas:rascunho-${form.dataset.rascunho}`;
  // Ignora o token CSRF e o botão: só campos que o usuário preenche
  const campos = form.querySelectorAll("input:not([type=hidden]), textarea, select");
  const textarea = form.querySelector("textarea[maxlength]");
  const contador = document.getElementById("contador-mensagem");

  // localStorage pode estar indisponível (modo privado), então tudo é protegido.
  const rascunho = {
    salvar() {
      try {
        const dados = {};
        campos.forEach((c) => (dados[c.name] = c.value));
        localStorage.setItem(chave, JSON.stringify(dados));
      } catch (e) { /* segue sem rascunho */ }
    },
    restaurar() {
      try {
        const dados = JSON.parse(localStorage.getItem(chave) || "{}");
        campos.forEach((c) => {
          // Não sobrescreve o que o servidor devolveu após um erro de validação
          if (!c.value && typeof dados[c.name] === "string") c.value = dados[c.name];
        });
      } catch (e) { /* rascunho corrompido: ignora */ }
    },
    limpar() {
      try { localStorage.removeItem(chave); } catch (e) { /* ignora */ }
    },
  };

  function atualizarContador() {
    if (!textarea || !contador) return;
    const usados = textarea.value.length;
    contador.textContent = `${usados}/${textarea.maxLength} caracteres`;
    contador.classList.toggle("text-danger", usados >= textarea.maxLength);
  }

  // Após um POST bem sucedido o servidor redireciona (sem erros na página):
  // se não há mensagens de erro, descartamos o rascunho antigo.
  if (!form.querySelector(".invalid-feedback")) {
    if (document.querySelector(".alert-success")) rascunho.limpar();
  }

  rascunho.restaurar();
  atualizarContador();

  form.addEventListener("input", () => {
    atualizarContador();
    rascunho.salvar();
  });
});
