// Formulario de Contacto: muestra las preguntas según el tipo de solicitud,
// lo envía a Netlify Forms como "contacto-<tipo>" y enseña el mensaje de ese tipo.
// Netlify manda el aviso por correo a quien atiende cada tipo (se configura en Netlify).
// "Talento – Envío de material" no va a Netlify: se guarda en una hoja de Google Sheets
// del Drive personal de Lorenzo (ver herramientas/apps-script-talento.gs) y no avisa a nadie.

// URL de la aplicación web de Apps Script de la hoja "Alzada – Envíos de talento".
const TALENTO_URL = "https://script.google.com/macros/s/AKfycbzJysmieOQpNjOfEHKlE8DDbaUZ8oqQT-lryZgElxL2Nhw0Fs1N8yVPG2eNvp4VKt1A/exec";

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

    const datos = new FormData(form);
    datos.set("form-name", "contacto-" + tipo.value);
    const boton = form.querySelector('button[type="submit"]');
    boton.disabled = true;
    mensaje.textContent = T.enviando;

    try {
      if (tipo.value === "talento") {
        if (!TALENTO_URL) throw new Error("Falta TALENTO_URL");
        // Apps Script no deja leer su respuesta desde otro sitio ("no-cors"); si no hay error de red, llegó.
        await fetch(TALENTO_URL, { method: "POST", mode: "no-cors", body: new URLSearchParams(datos) });
      } else {
        const respuesta = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(datos).toString(),
        });
        if (!respuesta.ok) throw new Error(respuesta.status);
      }
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
