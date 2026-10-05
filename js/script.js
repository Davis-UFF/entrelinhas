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
// Formulário de contato: validação, contador e rascunho automático
// (front-end apenas; o envio real será processado pelo back-end
// Java/Servlet, ainda não implementado).
// ============================================

const formContato = document.getElementById("formContato");

if (formContato) {
  const CHAVE_RASCUNHO = "entrelinhas:rascunho-contato";
  const campos = formContato.querySelectorAll("input, textarea");
  const mensagem = document.getElementById("mensagem");
  const contador = document.getElementById("contador-mensagem");
  const feedback = document.getElementById("form-feedback");

  // localStorage pode estar indisponível (modo privado, bloqueio de cookies),
  // então toda leitura/escrita é protegida para não quebrar o formulário.
  const rascunho = {
    salvar() {
      try {
        const dados = {};
        campos.forEach((c) => (dados[c.name] = c.value));
        localStorage.setItem(CHAVE_RASCUNHO, JSON.stringify(dados));
      } catch (e) { /* sem armazenamento: segue sem rascunho */ }
    },
    restaurar() {
      try {
        const dados = JSON.parse(localStorage.getItem(CHAVE_RASCUNHO) || "{}");
        campos.forEach((c) => {
          if (typeof dados[c.name] === "string") c.value = dados[c.name];
        });
      } catch (e) { /* rascunho corrompido ou indisponível: ignora */ }
    },
    limpar() {
      try {
        localStorage.removeItem(CHAVE_RASCUNHO);
      } catch (e) { /* ignora */ }
    },
  };

  // Campos obrigatórios preenchidos só com espaços são considerados vazios
  function validarCampo(campo) {
    const vazio = campo.required && campo.value.trim() === "";
    campo.setCustomValidity(vazio ? "Campo obrigatório" : "");
  }

  function atualizarContador() {
    const usados = mensagem.value.length;
    contador.textContent = `${usados}/${mensagem.maxLength} caracteres`;
    contador.classList.toggle("text-danger", usados >= mensagem.maxLength);
  }

  rascunho.restaurar();
  campos.forEach(validarCampo);
  atualizarContador();

  formContato.addEventListener("input", (event) => {
    validarCampo(event.target);
    if (event.target === mensagem) atualizarContador();
    feedback.style.display = "none";
    rascunho.salvar();
  });

  formContato.addEventListener("submit", (event) => {
    event.preventDefault();
    campos.forEach(validarCampo);

    if (!formContato.checkValidity()) {
      formContato.classList.add("was-validated");
      formContato.querySelector(":invalid").focus();
      return;
    }

    feedback.style.display = "block";
    formContato.reset();
    formContato.classList.remove("was-validated");
    rascunho.limpar();
    campos.forEach(validarCampo);
    atualizarContador();
  });
}
