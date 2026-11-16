// Apps Script de la hoja "Alzada – Envíos de talento" (Drive personal de Lorenzo).
// Recibe los envíos de "Talento – Envío de material" del formulario de Contacto
// y agrega un renglón en la pestaña "Envíos". No manda correos a nadie.
//
// Se pega en la hoja: Extensiones > Apps Script, y se publica como
// Implementar > Nueva implementación > Aplicación web
//   (Ejecutar como: Yo · Quién tiene acceso: Cualquier usuario).
// La URL que da Google va en TALENTO_URL de js/contacto.js.

const HOJA = "Envíos";

// Evita que un texto que empiece con = + - @ se tome como fórmula.
function limpiar(valor) {
  const texto = String(valor || "").trim().slice(0, 2000);
  return /^[=+\-@]/.test(texto) ? "'" + texto : texto;
}

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p["bot-field"]) return ContentService.createTextOutput("ok"); // trampa contra bots

  const hoja = SpreadsheetApp.getActive().getSheetByName(HOJA);
  hoja.appendRow([
    new Date(),
    limpiar(p.nombre),
    limpiar(p.nombre_artistico),
    limpiar(p.correo),
    limpiar(((p.pais || "").replace(/^.*\s(\+\d+)$/, "$1") + " " + (p.telefono || "")).trim()),
    limpiar(p.ciudad),
    limpiar(p.link_musica),
    limpiar(p.redes),
    limpiar(p.mensaje),
    "Nuevo",
  ]);
  return ContentService.createTextOutput("ok");
}
