// Formulario de Contacto: muestra las preguntas según el tipo de solicitud y lo guarda en la
// hoja de Google "Alzada – Fans y contacto" (una pestaña por tipo) por medio del Apps Script
// (herramientas/apps-script-formularios.gs). El script le avisa por correo a Charlie,
// salvo "Talento – Envío de material", que solo se guarda.

// URL de la aplicación web de Apps Script (la misma en Alzada, Ladrones y Tattoo Music Fest).
const CONTACTO_URL = "https://script.google.com/macros/s/AKfycbw3XUBhCSspVCCI3nQIg-GEtVpGP2ZChQPaZpUB65EthL0vXAobaTE8q3tlmMF5dasO/exec";

// Manda los datos al Apps Script sin esperar su respuesta (Google tarda varios segundos y,
// desde otro sitio, la respuesta ni siquiera se puede leer). sendBeacon deja el envío en cola
// del navegador y regresa al instante; si no existe, se usa fetch con un tope de 6 segundos.
function mandarContacto(url, datos) {
  if (!url.startsWith("https://")) return Promise.reject(new Error("Falta la URL del Apps Script"));
  if (navigator.sendBeacon && navigator.sendBeacon(url, datos)) return Promise.resolve();
  const envio = fetch(url, { method: "POST", mode: "no-cors", body: datos, keepalive: true });
  return Promise.race([envio, new Promise((listo) => setTimeout(listo, 6000))]);
}

const form = document.getElementById("form-contacto");

if (form) {
  const tipo = form.querySelector("#tipo");
  const grupos = form.querySelectorAll(".campos-tipo");
  const mensaje = form.querySelector(".form-mensaje");
  const gracias = document.getElementById("contacto-gracias");
  const CONTACTO_EN = document.documentElement.lang === "en";
  const T = CONTACTO_EN
    ? { faltan: "Please fill in the required fields.", enviando: "Sending…", error: "We couldn't send your message. Please try again." }
    : { faltan: "Llena los campos obligatorios.", enviando: "Enviando…", error: "No se pudo enviar tu mensaje. Inténtalo de nuevo." };

  // Solo el grupo del tipo elegido está activo; los demás quedan ocultos y deshabilitados
  // para que sus campos obligatorios no bloqueen el envío.
  function mostrarTipo() {
    grupos.forEach((g) => {
      const activo = g.dataset.tipo === tipo.value;
      g.hidden = !activo;
      g.disabled = !activo;
    });
  }

  // Desde un link: /contacto/?tipo=booking&artista=C-Kan
  const params = new URLSearchParams(location.search);
  if (params.get("tipo")) tipo.value = params.get("tipo");
  mostrarTipo();
  const artista = form.querySelector('[data-tipo="booking"] [name="artista"]');
  if (artista && params.get("artista")) artista.value = params.get("artista");

  tipo.addEventListener("change", mostrarTipo);

  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    mensaje.removeAttribute("data-tipo");
    if (!form.checkValidity()) {
      mensaje.textContent = T.faltan;
      mensaje.dataset.tipo = "error";
      form.reportValidity();
      return;
    }

    const datos = new URLSearchParams(new FormData(form));
    datos.set("accion", "contacto");
    datos.set("sitio", "alzada");
    datos.set("idioma", CONTACTO_EN ? "en" : "es");
    const boton = form.querySelector('button[type="submit"]');
    boton.disabled = true;
    mensaje.textContent = T.enviando;

    try {
      await mandarContacto(CONTACTO_URL, datos);
      const opcion = tipo.options[tipo.selectedIndex];
      gracias.querySelector("p").textContent = opcion.dataset.gracias;
      form.hidden = true;
      gracias.hidden = false;
      gracias.focus();
    } catch (e) {
      mensaje.textContent = T.error;
      mensaje.dataset.tipo = "error";
      boton.disabled = false;
    }
  });
}
