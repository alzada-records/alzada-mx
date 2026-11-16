/* =========================================================
   Lanzamientos del encabezado (portada del inicio)
   Para cambiarlos solo pega aquí los links de Spotify de los 6
   lanzamientos más nuevos, el más reciente primero.
   La portada y el título se jalan solos de Spotify.
   ========================================================= */
const LANZAMIENTOS = [
  "https://open.spotify.com/album/1XKtSl05ezH6lWTmVgTLUL",
];

(function () {
  const lista = document.getElementById("lanzamientos-lista");
  if (!lista) return;
  const EN = document.documentElement.lang === "en";

  LANZAMIENTOS.slice(0, 6).forEach(function (link, i) {
    const li = document.createElement("li");
    li.className = "lanzamiento";
    const a = document.createElement("a");
    a.href = link;
    a.target = "_blank";
    a.rel = "noopener";
    const img = document.createElement("img");
    img.width = 640;
    img.height = 640;
    img.alt = "";
    if (i > 1) img.loading = "lazy";
    const titulo = document.createElement("span");
    titulo.className = "lanzamiento-titulo";
    titulo.translate = false;
    titulo.textContent = EN ? "Listen" : "Escuchar";
    a.append(img, titulo);
    li.append(a);
    lista.append(li);

    fetch("https://open.spotify.com/oembed?url=" + encodeURIComponent(link))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        img.src = d.thumbnail_url;
        titulo.textContent = d.title;
        a.setAttribute("aria-label", (EN ? "Listen to " : "Escuchar ") + d.title);
      })
      .catch(function () { li.remove(); });
  });
})();
