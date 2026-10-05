// Validação e feedback do formulário de contato (front-end apenas; o envio
// real será processado pelo back-end Java/Servlet, ainda não implementado).
const formContato = document.getElementById("formContato");

if (formContato) {
  formContato.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!formContato.checkValidity()) {
      formContato.classList.add("was-validated");
      return;
    }

    document.getElementById("form-feedback").style.display = "block";
    formContato.reset();
    formContato.classList.remove("was-validated");
  });
}
