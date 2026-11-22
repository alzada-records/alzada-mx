// Apps Script de los formularios de Alzada, Ladrones y Tattoo Music Fest.
// Vive en la hoja "Alzada – Fans y contacto" (Drive personal de Lorenzo) y también
// escribe en la hoja "Tattoo Music Fest – Fans y contacto".
//
// Se pega en la hoja de Alzada: Extensiones > Apps Script, y se publica como
// Implementar > Nueva implementación > Aplicación web
//   (Ejecutar como: Yo · Quién tiene acceso: Cualquier usuario).
// La URL que da Google va en FORMULARIOS_URL de los js de los tres sitios.
//
// Qué recibe (parámetro "accion"):
//   suscribir  → fans (Alzada y Ladrones) o asistentes de TMF. No avisa a nadie.
//   contacto   → una pestaña por tipo. Avisa a Charlie salvo los tipos con avisa:false.
//   baja       → marca "Baja" con fecha. No borra nada.

const AVISOS = "charliefelix@alzada.mx";
const TMF_ID = "1dBEODJUrxEmahEdy3ThB-h4velpq6FYDzFXA0wTPJ0w";

// Pestaña, campos (en orden, después de Fecha, Nombre, Correo y Teléfono) y si avisa.
const CONTACTO = {
  alzada: {
    booking:       { hoja: "Booking",                campos: ["artista", "fecha_evento", "ciudad", "tipo_evento", "presupuesto"], avisa: true },
    marcas:        { hoja: "Marcas",                 campos: ["empresa", "tipo_colaboracion"], avisa: true },
    sync:          { hoja: "Sync",                   campos: ["empresa", "proyecto", "cancion", "fecha_uso"], avisa: true },
    talento:       { hoja: "Talento",                campos: ["nombre_artistico", "ciudad", "link_musica", "redes"], avisa: false },
    produccion:    { hoja: "Producción musical",     campos: ["servicio", "link_musica", "fecha_estimada"], avisa: true },
    audiovisual:   { hoja: "Producción audiovisual", campos: ["servicio", "fecha_estimada", "presupuesto"], avisa: true },
    instalaciones: { hoja: "Instalaciones",          campos: ["espacio", "fechas", "personas"], avisa: true },
  },
  tmf: {
    concurso:    { hoja: "TMF - Concurso tattoo",      campos: ["nombre_artistico", "estudio", "ciudad", "estilo", "portafolio"], avisa: true },
    expo:        { hoja: "TMF - Stands",               campos: ["negocio", "giro", "ciudad", "redes"], avisa: true },
    alimentos:   { hoja: "TMF - Alimentos y bebidas",  campos: ["negocio", "tipo_comida", "necesita_luz", "redes"], avisa: true },
    patrocinios: { hoja: "TMF - Marcas y patrocinios", campos: ["empresa", "cargo", "sitio_web", "tipo_colaboracion"], avisa: true },
  },
};
const NOMBRES_TIPO = {
  booking: "Booking", marcas: "Marcas", sync: "Sync", talento: "Talento", produccion: "Producción musical",
  audiovisual: "Producción audiovisual", instalaciones: "Instalaciones", concurso: "Concurso tattoo",
  expo: "Stands", alimentos: "Alimentos y bebidas", patrocinios: "Marcas y patrocinios",
  aviso: "Avísame edición 2027", boletos: "Boletos TMF 2027",
};

// Evita que un texto que empiece con = + - @ se tome como fórmula.
function limpiar(valor) {
  const texto = String(valor || "").trim().slice(0, 2000);
  return /^[=+\-@]/.test(texto) ? "'" + texto : texto;
}
function correoValido(c) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c); }
function telefono(p) {
  if (!String(p.telefono || "").trim()) return "";
  return ((p.pais || "").replace(/^.*\s(\+\d+)$/, "$1") + " " + p.telefono).trim();
}
function libro(sitio) { return sitio === "tmf" ? SpreadsheetApp.openById(TMF_ID) : SpreadsheetApp.getActive(); }
function respuesta(texto) { return ContentService.createTextOutput(texto); }

function doPost(e) {
  const p = (e && e.parameter) || {};
  const varios = (e && e.parameters) || {};
  if (p["bot-field"]) return respuesta("ok"); // trampa contra bots
  const sitio = ["alzada", "ladrones", "tmf"].includes(p.sitio) ? p.sitio : "";
  const correo = String(p.correo || "").trim().toLowerCase();
  if (!sitio || !correoValido(correo)) return respuesta("datos incompletos");

  const candado = LockService.getScriptLock();
  candado.waitLock(20000);
  try {
    if (p.accion === "suscribir") suscribir(sitio, p, varios, correo);
    else if (p.accion === "contacto") contacto(sitio, p, correo);
    else if (p.accion === "baja") baja(sitio, correo);
    else return respuesta("acción desconocida");
  } finally {
    candado.releaseLock();
  }
  return respuesta("ok");
}

// ---------- Registro maestro ("Todos" / "TMF - Todos") ----------
function registrar(sitio, tipo, nombre, correo, tel, detalle) {
  const hoja = libro(sitio).getSheetByName(sitio === "tmf" ? "TMF - Todos" : "Todos");
  const fuente = { alzada: "Alzada Web", ladrones: "Ladrones Web", tmf: "TMF Web" }[sitio];
  hoja.appendRow([new Date(), tipo, limpiar(nombre), correo, limpiar(tel), fuente, limpiar(detalle)]);
}

// ---------- Suscripciones ----------
function suscribir(sitio, p, varios, correo) {
  const ahora = new Date();
  if (sitio === "tmf") return suscribirTmf(p, correo, ahora);

  const fuente = sitio === "ladrones" ? "Ladrones Web" : "Alzada Web";
  let artistas = sitio === "ladrones" ? ["Ladrones"] : (varios.artistas || []).map(String).filter(Boolean);
  if (!artistas.length) return;
  const hoja = SpreadsheetApp.getActive().getSheetByName("Fans");
  const datos = hoja.getDataRange().getValues();
  const fila = datos.findIndex((r, i) => i > 0 && String(r[2]).toLowerCase() === correo);

  if (fila > 0) {
    // Ya existe: junta artistas y fuentes, y si estaba de baja lo reactiva.
    const r = datos[fila];
    const unir = (a, b) => [...new Set(String(a).split(", ").filter(Boolean).concat(b))].join(", ");
    hoja.getRange(fila + 1, 2, 1, 9).setValues([[
      limpiar(p.nombre) || r[1], correo, unir(r[3], artistas), unir(r[4], [fuente]),
      p.idioma || r[5], "Sí", "Activo", "", ahora,
    ]]);
  } else {
    hoja.appendRow([ahora, limpiar(p.nombre), correo, artistas.join(", "), fuente, p.idioma || "es", "Sí", "Activo", "", ahora]);
  }
  registrar(sitio, "Suscripción", p.nombre, correo, "", artistas.join(", "));
}

function suscribirTmf(p, correo, ahora) {
  const tipo = p.tipo === "boletos" ? "boletos" : "aviso";
  const hoja = libro("tmf").getSheetByName("TMF - Asistentes");
  if (tipo === "aviso") {
    // Sin repetidos: si ya está inscrito al aviso, solo lo reactiva.
    const datos = hoja.getDataRange().getValues();
    const fila = datos.findIndex((r, i) => i > 0 && r[1] === NOMBRES_TIPO.aviso && String(r[3]).toLowerCase() === correo);
    if (fila > 0) {
      hoja.getRange(fila + 1, 9, 1, 3).setValues([["Sí", "Activo", ""]]);
      registrar("tmf", NOMBRES_TIPO.aviso, p.nombre, correo, telefono(p), "Ya estaba inscrito");
      return;
    }
  }
  hoja.appendRow([ahora, NOMBRES_TIPO[tipo], limpiar(p.nombre), correo, limpiar(telefono(p)),
    limpiar(p.ciudad), limpiar(p.boletos), limpiar(p.mensaje), p.acepto ? "Sí" : "", "Activo", ""]);
  registrar("tmf", NOMBRES_TIPO[tipo], p.nombre, correo, telefono(p), p.ciudad || "");
}

// ---------- Contacto ----------
function contacto(sitio, p, correo) {
  const config = CONTACTO[sitio === "tmf" ? "tmf" : "alzada"][p.tipo];
  if (!config) return;
  const tel = telefono(p);
  const extra = config.campos.map((c) => limpiar(p[c]));
  const fila = [new Date(), limpiar(p.nombre), correo, limpiar(tel)].concat(extra).concat([limpiar(p.mensaje)]);
  if (sitio !== "tmf") fila.push(p.idioma || "es");
  fila.push("Nuevo");
  libro(sitio).getSheetByName(config.hoja).appendRow(fila);
  registrar(sitio, NOMBRES_TIPO[p.tipo], p.nombre, correo, tel, "");

  if (config.avisa) {
    const marca = sitio === "tmf" ? "Tattoo Music Fest" : "Alzada";
    const lineas = [
      "Llegó una solicitud nueva desde " + (sitio === "tmf" ? "tattoomusicfest.mx" : "alzada.mx") + ".",
      "",
      "Tipo: " + NOMBRES_TIPO[p.tipo],
      "Nombre: " + (p.nombre || ""),
      "Correo: " + correo,
      "Teléfono: " + tel,
    ];
    config.campos.forEach((c) => { if (p[c]) lineas.push(c.replace(/_/g, " ").replace(/^./, (l) => l.toUpperCase()) + ": " + p[c]); });
    if (p.mensaje) lineas.push("", "Comentarios:", p.mensaje);
    lineas.push("", "Para contestarle, responde a este correo. Todo queda guardado en la hoja \"" + libro(sitio).getName() + "\", pestaña \"" + config.hoja + "\".");
    MailApp.sendEmail({
      to: AVISOS,
      replyTo: correo,
      name: marca + " – Formularios",
      subject: marca + " · " + NOMBRES_TIPO[p.tipo] + " · " + (p.nombre || correo),
      body: lineas.join("\n"),
    });
  }
}

// ---------- Bajas ----------
function baja(sitio, correo) {
  const ahora = new Date();
  if (sitio === "tmf") {
    const hoja = libro("tmf").getSheetByName("TMF - Asistentes");
    const datos = hoja.getDataRange().getValues();
    datos.forEach((r, i) => { if (i > 0 && String(r[3]).toLowerCase() === correo) hoja.getRange(i + 1, 10, 1, 2).setValues([["Baja", ahora]]); });
  } else {
    const hoja = SpreadsheetApp.getActive().getSheetByName("Fans");
    const datos = hoja.getDataRange().getValues();
    datos.forEach((r, i) => { if (i > 0 && String(r[2]).toLowerCase() === correo) hoja.getRange(i + 1, 8, 1, 3).setValues([["Baja", ahora, ahora]]); });
  }
  registrar(sitio, "Baja", "", correo, "", "");
}
