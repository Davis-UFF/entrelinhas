/* js/script.js - Interatividade e Validação */

document.addEventListener("DOMContentLoaded", function() {
  
  // Seleciona o formulário da página de contato (se ele existir na página atual)
  const formContato = document.querySelector("form");

  if (formContato) {
    formContato.addEventListener("submit", function(event) {
      // Impede o envio padrão do formulário (que recarregaria a página)
      event.preventDefault();

      // Captura o nome digitado para personalizar a mensagem
      const nomeDigitado = document.getElementById("nome").value;

      // Exibe uma mensagem de sucesso simples na tela
      alert(`Obrigado pelo contato, ${nomeDigitado}! Sua mensagem foi enviada com sucesso para a Livraria Entrelinhas.`);

      // Limpa os campos do formulário após o envio
      formContato.reset();
    });
  }
});