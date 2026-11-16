// Reproductor con el video más nuevo de un canal de YouTube y, abajo, los que siguen.
// Se usa en el inicio (canal de Alzada) y en la página de cada artista (su canal).
// El canal sale del atributo data-canal de la sección; el HTML lo pone el generador.
// Usa la YouTube Data API. Si falla, se queda el reproductor de respaldo con la lista de subidas.

// Clave de Google Cloud (proyecto ladrones-web), restringida a alzada.mx y ladrones.mx.
const API_KEY = "AIzaSyAg_coKJfSwQj63NRfZtm59-AagOwJZnmg";

const seccionVideos = document.querySelector("[data-canal]");
const CANAL = seccionVideos ? seccionVideos.dataset.canal : "";
// "UULF" + el ID sin "UC" = videos largos, sin Shorts. "UU" + el ID sin "UC" = todo lo subido.
const LISTA_SIN_SHORTS = "UULF" + CANAL.slice(2);
const LISTA_TODO = "UU" + CANAL.slice(2);

// Cuántos videos se pueden elegir abajo del reproductor (contando el principal).
const CUANTOS = 9;

// Se guardan 3 horas en el navegador del visitante para no gastar cuota de más.
const CACHE_CLAVE = "alzada-videos-v2-" + CANAL;
const CACHE_HORAS = 3;

// Solo estrenos de canciones: se saltan audios, lyric videos, visualizers, en vivo,
// detrás de cámaras, teasers, entrevistas, podcasts y promos con hashtags.
// Para quitar otro tipo, agrégalo aquí.
const NO_ES_VIDEOCLIP = /audio|lyric|letra|visuali[sz]er|en vivo|\blive\b|behind|detr[aá]s de|making of|teaser|tr[aá]iler|entrevista|interview|podcast|reacci[oó]n|reaction|vlog|dj ?set|disponible|#/i;

const reproductor = document.getElementById("reproductor");
const tituloActual = document.getElementById("video-actual");
const listaVideos = document.getElementById("videos-lista");
const VIDEOS_EN = document.documentElement.lang === "en";

function leerCache() {
  try {
    const datos = JSON.parse(localStorage.getItem(CACHE_CLAVE));
    if (datos && Date.now() - datos.guardado < CACHE_HORAS * 3600 * 1000) return datos.videos;
  } catch (e) { /* sin almacenamiento disponible: se ignora */ }
  return null;
}

function guardarCache(videos) {
  try {
    localStorage.setItem(CACHE_CLAVE, JSON.stringify({ guardado: Date.now(), videos }));
  } catch (e) { /* sin almacenamiento disponible: se ignora */ }
}

async function traerLista(playlist) {
  const url = new URL("https://www.googleapis.com/youtube/v3/playlistItems");
  url.search = new URLSearchParams({ part: "snippet,contentDetails", maxResults: "50", playlistId: playlist, key: API_KEY });
  const respuesta = await fetch(url);
  if (!respuesta.ok) throw new Error("YouTube respondió " + respuesta.status);
  const datos = await respuesta.json();
  const videos = [];
  for (const item of datos.items || []) {
    const s = item.snippet;
    if (s.title === "Private video" || s.title === "Deleted video") continue;
    if (NO_ES_VIDEOCLIP.test(s.title)) continue;
    const m = s.thumbnails || {};
    videos.push({
      id: item.contentDetails.videoId,
      titulo: s.title,
      fecha: item.contentDetails.videoPublishedAt || s.publishedAt,
      imagen: (m.medium || m.high || m.default || {}).url,
    });
  }
  return videos;
}

function reproducir(video, iniciar) {
  reproductor.src = `https://www.youtube.com/embed/${video.id}?rel=0${iniciar ? "&autoplay=1" : ""}`;
  reproductor.title = video.titulo;
  tituloActual.textContent = video.titulo;
  listaVideos.querySelectorAll("[aria-current]").forEach((b) => b.removeAttribute("aria-current"));
  const boton = listaVideos.querySelector(`[data-id="${video.id}"]`);
  if (boton) boton.setAttribute("aria-current", "true");
}

function pintar(videos) {
  listaVideos.innerHTML = "";
  for (const video of videos) {
    const li = document.createElement("li");
    li.className = "video-tarjeta";
    const boton = document.createElement("button");
    boton.type = "button";
    boton.dataset.id = video.id;
    boton.setAttribute("aria-label", (VIDEOS_EN ? "Play " : "Ver ") + video.titulo);
    const img = document.createElement("img");
    img.src = video.imagen;
    img.alt = "";
    img.width = 320;
    img.height = 180;
    img.loading = "lazy";
    const titulo = document.createElement("span");
    titulo.className = "video-titulo";
    titulo.translate = false;
    titulo.textContent = video.titulo;
    boton.append(img, titulo);
    boton.addEventListener("click", () => reproducir(video, true));
    li.append(boton);
    listaVideos.append(li);
  }
}

async function iniciar() {
  if (!CANAL || !listaVideos) return;
  let videos = leerCache();
  if (!videos) {
    try {
      videos = await traerLista(LISTA_SIN_SHORTS);
    } catch (e) {
      try {
        videos = await traerLista(LISTA_TODO);
      } catch (e2) {
        return; // la API falló: se queda el reproductor de respaldo
      }
    }
    videos.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
    videos = videos.slice(0, CUANTOS);
    guardarCache(videos);
  }
  if (!videos.length) return;
  pintar(videos);
  reproducir(videos[0], false);
}

iniciar();
