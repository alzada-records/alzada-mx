"""Arma las páginas del sitio de Alzada, en español (/) e inglés (/en/).

Uso (desde la carpeta del sitio):  python3 herramientas/generar.py

Genera, en los dos idiomas:
  index.html                 inicio
  <artista>/index.html       una página por artista (misma dirección que en Wix)
  contacto/index.html        formulario (en inglés: en/contact/)
  404.html                   página de error (en inglés: en/404.html)
  sitemap.xml

De dónde salen los textos:
  datos/artistas.json        nombre, bio en español, redes y canal de YouTube de cada artista
  datos/bios_en.json         bio en inglés de cada artista
  herramientas/formulario.py y formulario_en.py   opciones y preguntas del formulario de Contacto
  Este archivo               todo lo demás (menú, secciones, botones), con t("español", "inglés")

Cada texto va en los dos idiomas. Después de cambiar algo, vuelve a correr este script.
"""
import json
import pathlib
import sys
from html import escape
from urllib.parse import quote

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from formulario import TIPOS, PAISES  # noqa: E402
from formulario_en import TIPOS_EN, PAISES_EN  # noqa: E402

DOMINIO = "https://www.alzada.mx"
ARTISTAS = json.loads((RAIZ / "datos/artistas.json").read_text(encoding="utf-8"))
BIOS_EN = json.loads((RAIZ / "datos/bios_en.json").read_text(encoding="utf-8"))

REDES = [  # clave en artistas.json, nombre visible, ícono
    ("instagram", "Instagram", "instagram"),
    ("tiktok", "TikTok", "tiktok"),
    ("youtube", "YouTube", "youtube"),
    ("facebook", "Facebook", "facebook"),
    ("spotify", "Spotify", "spotify"),
    ("apple", "Apple Music", "apple-music"),
]
REDES_ALZADA = {
    "instagram": "https://www.instagram.com/alzadaoficial/",
    "tiktok": "https://www.tiktok.com/@alzadaoficial",
    "youtube": "https://www.youtube.com/c/ALZADAOficial",
    "facebook": "https://www.facebook.com/alzadaoficial/",
    "spotify": "https://open.spotify.com/artist/68Nt8XHuyEgQSOHih2iMlv",
    "apple": "https://music.apple.com/mx/artist/alzada/299724687",
}
TIENDA = "https://alzadastreetwear.com/collections/merch-alzada"

# Lanzamientos destacados del encabezado del inicio (rotan cada 10 s), en orden.
#   fondo: foto de fondo (versión chica para celular y grande para compu)
#   portada: arte del disco (local o de Spotify)
#   mas: segundo botón (texto en español, texto en inglés, link; un link que empieza con / es del sitio)
HERO = [
    {"artista": "Yoss Bones", "titulo": "Bb $oy yo",
     "tipo": ("Nuevo EP · 2026", "New EP · 2026"),
     "portada": "https://i.scdn.co/image/ab67616d00001e02b1988474c2f167c7ee03ec74",
     "fondo": ("/img/artistas/yoss-bones-grande.webp", "/img/artistas/yoss-bones-grande.webp"),
     "posicion": "center 25%",
     "escuchar": "https://open.spotify.com/album/6bspMNWcjH8ryugufTcTxh",
     "mas": ("Ver artista", "View artist", "/yoss-bones/")},
    {"artista": "Neto Peña", "titulo": "Mañana Será Otro Día",
     "tipo": ("Álbum · 2025", "Album · 2025"),
     "portada": "https://i.scdn.co/image/ab67616d00001e022d60e35e9b7d95e9095081d5",
     "fondo": ("/img/artistas/neto-pena-grande.webp", "/img/artistas/neto-pena-grande.webp"),
     "posicion": "center 25%",
     "escuchar": "https://open.spotify.com/album/6LOpEa2PQnIhwMzeE9levS",
     "mas": ("Ver artista", "View artist", "/neto-pena/")},
    {"artista": "Zxmyr", "titulo": "ZXM-YR Mami",
     "tipo": ("Nuevo álbum · 2026", "New album · 2026"),
     "portada": "https://i.scdn.co/image/ab67616d00001e02834c90c7f6457811efc48042",
     "fondo": ("/img/artistas/zxmyr-grande.webp", "/img/artistas/zxmyr-grande.webp"),
     "posicion": "center 30%",
     "escuchar": "https://open.spotify.com/album/1lQGIOE4Buny19S91SjKKy",
     "mas": ("Ver artista", "View artist", "/zxmyr/")},
    {"artista": "Ladrones", "titulo": "Arriba La L",
     "tipo": ("Nuevo álbum · 2026", "New album · 2026"),
     "portada": "/img/lanzamientos/arriba-la-l.webp",
     "fondo": ("/img/artistas/ladrones-grande.webp", "/img/artistas/ladrones-grande.webp"),
     "posicion": "center 25%",
     "escuchar": "https://open.spotify.com/album/1XKtSl05ezH6lWTmVgTLUL",
     "mas": ("Toda la música", "All music", "https://www.ladrones.mx/lanzamientos/")},
    {"artista": "Toser One", "titulo": "Botellas En La Banqueta y Un Corazón Herido",
     "tipo": ("Nuevo álbum · 2026", "New album · 2026"),
     "portada": "https://i.scdn.co/image/ab67616d00001e02ec934a6b8bf7ca83f29a81ad",
     "fondo": ("/img/artistas/toser-one-grande.webp", "/img/artistas/toser-one-grande.webp"),
     "posicion": "center 25%",
     "escuchar": "https://open.spotify.com/album/37TRdrlnuAOvMxUOur1ILs",
     "mas": ("Ver artista", "View artist", "/toser-one/")},
]

MAILCHIMP = "https://alzada.us19.list-manage.com/subscribe/post?u=32d94c0e4051438d818e68013&amp;id=4bd0645e6c&amp;f_id=00b59be3f0"
TRAMPA = "b_32d94c0e4051438d818e68013_4bd0645e6c"

# ---------- Idioma ----------
LANG = "es"


def t(es, en):
    """El texto en el idioma de la página que se está armando."""
    return en if LANG == "en" else es


def u(ruta):
    """Link interno en el idioma actual: "/c-kan/" -> "/en/c-kan/"; "/#roster" -> "/en/#roster"."""
    return "/en" + ruta if LANG == "en" else ruta


def ruta_contacto(lang=None):
    return "/en/contact/" if (lang or LANG) == "en" else "/contacto/"


def guardar(ruta, html):
    """Guarda una página: "/" -> index.html, "/en/c-kan/" -> en/c-kan/index.html, "/404.html" -> 404.html."""
    destino = RAIZ / ruta.strip("/")
    if not ruta.endswith(".html"):
        destino = destino / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")


# ---------- Piezas comunes ----------
def cabeza(titulo, descripcion, rutas, imagen, extra="", actual=""):
    """rutas = (ruta en español, ruta en inglés) de esta misma página."""
    es, en = rutas
    ruta = en if LANG == "en" else es
    otra, otro_lang = (es, "es") if LANG == "en" else (en, "en")
    alternos = (f'  <link rel="alternate" hreflang="es" href="{DOMINIO}{es}">\n'
                f'  <link rel="alternate" hreflang="en" href="{DOMINIO}{en}">\n'
                f'  <link rel="alternate" hreflang="x-default" href="{DOMINIO}{es}">\n') if not es.endswith(".html") else ""
    menu = [
        ("/", t("Inicio", "Home"), actual == "inicio"),
        ("/#roster", "Roster", False),
        ("/#lanzamientos", t("Lanzamientos", "Releases"), False),
        ("/#nosotros", t("Nosotros", "About"), False),
        ("/#sync", "Sync", False),
        ("/#merch", "Merch", False),
    ]
    actual_attr = ' aria-current="page"'
    items = "\n".join(f'          <li><a href="{u(r)}"{actual_attr if a else ""}>{n}</a></li>' for r, n, a in menu)
    items += (f'\n          <li><a href="{ruta_contacto()}"{actual_attr if actual == "contacto" else ""}>'
              f'{t("Contacto", "Contact")}</a></li>')
    items += (f'\n          <li class="idioma"><a href="{otra}" lang="{otro_lang}" hreflang="{otro_lang}" '
              f'data-idioma="{otro_lang}" aria-label="{t("English", "Español")}">{otro_lang.upper()}</a></li>')
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)}</title>
  <meta name="description" content="{escape(descripcion)}">
  <meta name="theme-color" content="#0b0b0b">
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
  <meta property="og:title" content="{escape(titulo)}">
  <meta property="og:description" content="{escape(descripcion)}">
  <meta property="og:image" content="{DOMINIO}{imagen}">
  <meta property="og:image:alt" content="{escape(titulo)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Alzada">
  <meta property="og:locale" content="{t("es_MX", "en_US")}">
  <meta property="og:url" content="{DOMINIO}{ruta}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{DOMINIO}{ruta}">
{alternos}  <link rel="icon" href="/img/favicon.png" type="image/png">
  <link rel="stylesheet" href="/css/styles.css">
  <script src="/js/idioma.js"></script>
{extra}  <script src="/js/main.js" defer></script>
  <script src="/js/newsletter.js" defer></script>
</head>
<body>
  <a class="saltar" href="#contenido">{t("Saltar al contenido", "Skip to content")}</a>

  <header class="encabezado">
    <div class="contenedor">
      <a class="logo" href="{u("/")}"><img src="/img/logo.webp" alt="Alzada" width="88" height="96"></a>
      <nav aria-label="{t("Principal", "Main")}">
        <button class="menu-boton" type="button" aria-expanded="false" aria-controls="menu">{t("Menú", "Menu")}</button>
        <ul class="menu" id="menu">
{items}
        </ul>
      </nav>
    </div>
  </header>

  <main id="contenido">
"""


def lista_redes(redes, tam, con_texto, nombre):
    items = []
    for clave, visible, icono in REDES:
        url = redes.get(clave)
        if not url:
            continue
        if con_texto:
            items.append(f'          <li><a href="{url}" target="_blank" rel="noopener">'
                         f'<img src="/img/redes/{icono}.png" alt="" width="{tam}" height="{tam}">'
                         f'<span>{visible}</span></a></li>')
        else:
            items.append(f'        <li><a href="{url}" target="_blank" rel="noopener">'
                         f'<img src="/img/redes/{icono}.png" alt="{visible} {t("de", "of")} {escape(nombre)}" '
                         f'width="{tam}" height="{tam}" loading="lazy"></a></li>')
    return "\n".join(items)


def barra_redes(redes, nombre):
    if not redes:
        return ""
    return f"""
    <!-- Barra de redes -->
    <nav class="barra-redes" aria-label="{t("Redes de", "Social media of")} {escape(nombre)}">
      <div class="contenedor">
        <ul>
{lista_redes(redes, 24, True, nombre)}
        </ul>
      </div>
    </nav>
"""


def newsletter():
    return f"""
    <!-- Newsletter: Mailchimp (misma audiencia que Ladrones) -->
    <section class="seccion newsletter newsletter-foto" aria-labelledby="titulo-newsletter">
      <div class="contenedor">
        <div class="newsletter-caja">
        <h2 id="titulo-newsletter">{t("Únete a la familia", "Join the family")}</h2>
        <p class="seccion-intro">{t("Lanzamientos, fechas y noticias de tus artistas favoritos.", "Releases, tour dates and news from your favorite artists.")}</p>
        <form class="form-lista" action="{MAILCHIMP}" method="post" target="_blank" rel="noopener" novalidate>
          <div>
            <label for="nombre">{t("Nombre", "Name")}</label>
            <input type="text" id="nombre" name="FNAME" autocomplete="given-name" required>
          </div>
          <div>
            <label for="correo">{t("Correo", "Email")}</label>
            <input type="email" id="correo" name="EMAIL" autocomplete="email" spellcheck="false" required>
          </div>
          <div class="casilla">
            <input type="checkbox" id="acepto" name="acepto" required>
            <label for="acepto">{t("Quiero recibir noticias de Alzada y sus artistas.", "I want to get news from Alzada and its artists.")}</label>
          </div>
          <div class="trampa" aria-hidden="true"><input type="text" name="{TRAMPA}" tabindex="-1" value="" autocomplete="off"></div>
          <button class="boton" type="submit">{t("Suscribirme", "Subscribe")}</button>
          <p class="form-mensaje" role="status" aria-live="polite"></p>
        </form>
        </div>
      </div>
    </section>
"""


def pie():
    return f"""
  </main>

  <footer class="pie">
    <div class="contenedor">
      <p>{t("Sigue a", "Follow")} <span translate="no">Alzada</span></p>
      <ul class="redes">
{lista_redes(REDES_ALZADA, 28, False, "Alzada")}
      </ul>
      <p>© 2027 <span translate="no">Alzada</span></p>
    </div>
  </footer>
</body>
</html>
"""


def bio(a):
    return BIOS_EN[a["slug"]] if LANG == "en" else a["bio"]


# ---------- Inicio ----------
def roster():
    tarjetas = []
    for i, a in enumerate(ARTISTAS):
        carga = '' if i < 4 else ' loading="lazy"'
        tarjetas.append(f"""          <li class="artista-tarjeta">
            <a href="{u('/' + a['slug'] + '/')}">
              <img src="/img/artistas/{a['slug']}-400.webp" srcset="/img/artistas/{a['slug']}-400.webp 400w, /img/artistas/{a['slug']}-800.webp 800w" sizes="(min-width: 1000px) 260px, (min-width: 600px) 33vw, 50vw" alt="" width="400" height="400"{carga}>
              <span class="artista-nombre" translate="no">{escape(a['nombre'])}</span>
            </a>
          </li>""")
    return "\n".join(tarjetas)


def hero():
    diapos, puntos = [], []
    for i, h in enumerate(HERO):
        mas_es, mas_en, mas_link = h["mas"]
        externo = mas_link.startswith("http")
        mas_href = mas_link if externo else u(mas_link)
        mas_extra = ' target="_blank" rel="noopener"' if externo else ""
        carga = "" if i == 0 else ' loading="lazy"'
        diapos.append(f"""        <div class="hero-diapo hero-foto{' activa' if i == 0 else ''}" role="group" aria-roledescription="{t("diapositiva", "slide")}" aria-label="{i + 1} {t("de", "of")} {len(HERO)}"
          style="--fondo-chico: url('{h['fondo'][0]}'); --fondo-grande: url('{h['fondo'][1]}'); --fondo-posicion: {h['posicion']};">
          <div class="contenedor">
            <div class="hero-lanzamiento">
              <img src="{h['portada']}" alt="{t("Portada de", "Cover of")} {escape(h['titulo'])}" width="300" height="300"{carga}>
              <p class="seccion-intro"><span translate="no">{escape(h['artista'])}</span> · {escape(t(*h['tipo']))}</p>
            </div>
            <h2 class="hero-titulo"><span translate="no">{escape(h['titulo'])}</span></h2>
            <p><a class="boton" href="{h['escuchar']}" target="_blank" rel="noopener">{t("Escuchar", "Listen")}</a>
               <a class="boton boton-secundario" href="{mas_href}"{mas_extra}>{escape(t(mas_es, mas_en))}</a></p>
          </div>
        </div>""")
        puntos.append(f'<button type="button" class="hero-punto" aria-label="{t("Ver", "Show")} {escape(h["titulo"])}"></button>')
    return f"""    <!-- Lanzamientos destacados: rotan cada 10 s (js/hero.js). Se cambian en HERO, arriba en este archivo. -->
    <section class="hero-carrusel" aria-roledescription="{t("carrusel", "carousel")}" aria-label="{t("Lanzamientos destacados", "Featured releases")}">
      <h1 class="oculto">Alzada Records</h1>
{chr(10).join(diapos)}
      <div class="hero-controles contenedor">
        <div class="hero-puntos">{"".join(puntos)}</div>
        <button type="button" class="hero-pausa"></button>
      </div>
    </section>

"""


def inicio():
    html = cabeza(t("Alzada Records | Disquera mexicana independiente", "Alzada Records | Independent Mexican record label"),
                  t("Alzada Records: disquera mexicana independiente. Conoce a nuestros artistas, sus lanzamientos y el merch oficial.",
                    "Alzada Records: independent Mexican record label. Meet our artists, their latest releases and the official merch."),
                  ("/", "/en/"), "/img/compartir.jpg",
                  f'  <link rel="preload" as="image" href="{HERO[0]["fondo"][1]}" media="(min-width: 900px)" fetchpriority="high">\n'
                  f'  <link rel="preload" as="image" href="{HERO[0]["fondo"][0]}" media="(max-width: 899px)" fetchpriority="high">\n'
                  '  <link rel="preconnect" href="https://www.youtube.com">\n'
                  '  <link rel="preconnect" href="https://www.googleapis.com">\n'
                  '  <link rel="preconnect" href="https://alzadastreetwear.com">\n'
                  '  <script src="/js/videos.js" defer></script>\n'
                  '  <script src="/js/hero.js" defer></script>\n'
                  '  <script src="/js/merch.js" defer></script>\n',
                  actual="inicio")
    alzada = '<span translate="no">Alzada</span>'
    if LANG == "en":
        nosotros = (f"<p>{alzada} was born in Guadalajara, Jalisco, to open doors for emerging talent in an industry full of barriers and recycled formulas. What started as an independent movement is now a creative ecosystem built on authenticity, the streets and a direct connection with a new generation.</p>\n"
                    f"          <p>From the very beginning, it has bet on artists who are now leading names in the urban scene across Mexico and Latin America. With audiovisual production, digital content, brand partnerships and live experiences, {alzada} is more than a label: it’s a 360 platform that keeps breaking the mold and raising the bar for music in Latin America.</p>")
        sync = (f"<p>At {alzada}, sync and licensing turn music into a strategic asset. Our catalog brings together authentic, versatile artists ready for films, series, campaigns, video games and digital content, adding identity, emotion and value to every project.</p>\n"
                "          <p>We work in an agile, curated way, handling rights, clearances and deliverables so projects move without friction. From picking the right track to closing the license, we align creativity with business goals, helping brands, agencies and production companies reach new audiences through music.</p>")
    else:
        nosotros = (f"<p>{alzada} nace en Guadalajara, Jalisco, para abrirle paso al talento emergente en una industria llena de barreras y fórmulas repetidas. Lo que empezó como un movimiento independiente hoy es un ecosistema creativo construido sobre la autenticidad, la calle y la conexión directa con una nueva generación.</p>\n"
                    f"          <p>Desde etapas tempranas ha apostado por artistas que hoy son referentes de la escena urbana en México y Latinoamérica. Con producción audiovisual, contenido digital, colaboraciones con marcas y experiencias en vivo, {alzada} es más que un sello: una plataforma 360 que sigue rompiendo esquemas y elevando el estándar de la música en Latinoamérica.</p>")
        sync = (f"<p>En {alzada}, la sincronización y el licensing convierten la música en un activo estratégico. Nuestro catálogo reúne propuestas auténticas y versátiles, listas para integrarse en películas, series, campañas, videojuegos y contenido digital, aportando identidad, emoción y valor a cada proyecto.</p>\n"
                "          <p>Trabajamos de forma ágil y curatorial, facilitando la gestión de derechos, autorizaciones y entregables para acelerar procesos sin fricción. Desde la selección del track ideal hasta el cierre de la licencia, alineamos creatividad con objetivos comerciales, ayudando a marcas, agencias y productoras a conectar con nuevas audiencias a través de la música.</p>")
    html += f"""
{hero()}{barra_redes(REDES_ALZADA, "Alzada")}
    <!-- Roster: cada foto lleva a la página del artista -->
    <section class="seccion" id="roster" aria-labelledby="titulo-roster">
      <div class="contenedor">
        <h2 id="titulo-roster">Roster</h2>
        <ul class="roster">
{roster()}
        </ul>
      </div>
    </section>

    <!-- Videos: el más nuevo del canal de Alzada y los que siguen (js/videos.js) -->
    <section class="seccion videos-inicio" id="lanzamientos" data-canal="UCb41Xk6cDPcz1r_xEhQqvuA" aria-labelledby="titulo-videos">
      <div class="contenedor">
        <h2 id="titulo-videos">{t("Lanzamientos", "Releases")}</h2>
        <iframe class="video" id="reproductor"
          src="https://www.youtube.com/embed/videoseries?list=UULFb41Xk6cDPcz1r_xEhQqvuA"
          title="{t("Videos más recientes de Alzada", "Latest videos from Alzada")}"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
        <p class="video-actual" id="video-actual" aria-live="polite"></p>
        <ul class="videos-lista" id="videos-lista" aria-label="{t("Más videos", "More videos")}"></ul>
      </div>
    </section>

    <!-- Nosotros -->
    <section class="seccion nosotros" id="nosotros" aria-labelledby="titulo-nosotros">
      <div class="contenedor nosotros-grid">
        <div>
          <h2 id="titulo-nosotros">{t("Nosotros", "About")}</h2>
          {nosotros}
        </div>
        <img src="/img/nosotros-800.webp" srcset="/img/nosotros-800.webp 800w, /img/nosotros-1400.webp 1400w" sizes="(min-width: 900px) 540px, 100vw" alt="{t("Artistas de Alzada con sus discos de certificación", "Alzada artists with their certified records")}" width="1400" height="933" loading="lazy">
      </div>
    </section>
    <!-- Sync / Licensing -->
    <section class="seccion nosotros sync" id="sync" aria-labelledby="titulo-sync">
      <div class="contenedor nosotros-grid">
        <img src="/img/sync-800.webp" srcset="/img/sync-800.webp 800w, /img/sync-1400.webp 1400w" sizes="(min-width: 900px) 540px, 100vw" alt="{t("Recepción de las oficinas de Alzada con discos de certificación en las paredes", "Alzada’s office lobby with certified records on the walls")}" width="1400" height="933" loading="lazy">
        <div>
          <h2 id="titulo-sync">Sync / Licensing</h2>
          {sync}
          <p><a class="boton" href="{ruta_contacto()}?tipo=sync#formulario">{t("Contactar", "Get in touch")}</a></p>
        </div>
      </div>
    </section>
    <!-- Merch: productos de Alzada Streetwear (Shopify). Se llenan solos con js/merch.js. -->
    <section class="seccion merch" id="merch" aria-labelledby="titulo-merch">
      <div class="contenedor">
        <div class="merch-encabezado">
          <h2 id="titulo-merch">Merch</h2>
          <div class="merch-flechas" hidden>
            <button type="button" class="merch-flecha" data-dir="-1" aria-label="{t("Productos anteriores", "Previous products")}">←</button>
            <button type="button" class="merch-flecha" data-dir="1" aria-label="{t("Más productos", "More products")}">→</button>
          </div>
        </div>
        <ul class="merch-lista" id="merch-lista" aria-live="polite"></ul>
        <p><a class="boton boton-secundario" href="{TIENDA}" target="_blank" rel="noopener">{t("Ver tienda", "Visit the store")}</a></p>
      </div>
    </section>
{newsletter()}{pie()}"""
    guardar(u("/"), html)


# ---------- Página de artista ----------
def pagina_artista(a):
    nombre = a["nombre"]
    parrafos_bio = bio(a)
    resumen = parrafos_bio[0].split(". ")[0].rstrip(".") + "."
    spotify = a["redes"].get("spotify", "")
    canal = a.get("canal_youtube")
    html = cabeza(f"{nombre} | Alzada Records", resumen, (f"/{a['slug']}/", f"/en/{a['slug']}/"),
                  f"/img/artistas/{a['slug']}-800.webp",
                  '  <script src="/js/videos.js" defer></script>\n' if canal else "")
    parrafos = "\n".join(f"          <p>{escape(p)}</p>" for p in parrafos_bio)
    botones = (f'\n          <p class="artista-botones"><a class="boton" href="{ruta_contacto()}?tipo=booking&amp;artista='
               + quote(nombre) + f'#formulario">{t("Contrataciones", "Booking")}</a>')
    if a.get("sitio"):
        botones += f'\n             <a class="boton boton-secundario" href="{a["sitio"]}" target="_blank" rel="noopener">{t("Sitio oficial", "Official site")}</a>'
    botones += '</p>'
    musica = ""
    if spotify:
        embed = spotify.replace("open.spotify.com/artist/", "open.spotify.com/embed/artist/")
        musica = f"""
    <section class="seccion" aria-labelledby="titulo-musica">
      <div class="contenedor">
        <h2 id="titulo-musica">{t("Música", "Music")}</h2>
        <iframe class="spotify" src="{embed}?theme=0" title="{escape(nombre)} {t("en", "on")} Spotify" width="100%" height="352" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
      </div>
    </section>
"""
    with Image.open(RAIZ / f"img/artistas/{a['slug']}-grande.webp") as foto:
        ancho, alto = foto.size
    videos = ""
    if canal:
        videos = f"""
    <!-- Videos: el estreno más nuevo de su canal y los que siguen (js/videos.js) -->
    <section class="seccion" data-canal="{canal}" aria-labelledby="titulo-videos">
      <div class="contenedor">
        <h2 id="titulo-videos">Videos</h2>
        <iframe class="video" id="reproductor"
          src="https://www.youtube.com/embed/videoseries?list=UULF{canal[2:]}"
          title="{t("Videos de", "Videos by")} {escape(nombre)}"
          loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
        <p class="video-actual" id="video-actual" aria-live="polite"></p>
        <ul class="videos-lista" id="videos-lista" aria-label="{t("Más videos de", "More videos by")} {escape(nombre)}"></ul>
      </div>
    </section>
"""
    html += f"""
    <section class="seccion portada artista">
      <div class="contenedor artista-grid">
        <img class="artista-foto" src="/img/artistas/{a['slug']}-grande.webp" alt="{escape(nombre)}" width="{ancho}" height="{alto}" fetchpriority="high">
        <div class="artista-texto">
          <p class="seccion-intro"><a href="{u("/#roster")}">Roster</a></p>
          <h1 translate="no">{escape(nombre)}</h1>
{parrafos}{botones}
        </div>
      </div>
    </section>
{barra_redes(a["redes"], nombre)}{musica}{videos}
    <!-- Fechas: Bandsintown (se actualizan solas) -->
    <section class="seccion fechas" aria-labelledby="titulo-fechas">
      <div class="contenedor">
        <h2 id="titulo-fechas">{t("Próximas fechas", "Upcoming shows")}</h2>
        <script charset="utf-8" src="https://widgetv3.bandsintown.com/main.min.js"></script>
        <a class="bit-widget-initializer"
          data-artist-name="{escape(a.get('bandsintown', nombre))}"
          data-app-id="js_www.alzada.mx"
          data-display-limit="8"
          data-language="{LANG}"
          data-display-local-dates="false"
          data-display-past-dates="false"
          data-font="Helvetica"
          data-text-color="#111111"
          data-link-color="#111111"
          data-background-color="rgba(0,0,0,0)"
          data-popup-background-color="#ffffff"
          data-separator-color="#e2e2e2"
          data-widget-width="100%"
          data-auto-style="false"></a>
      </div>
    </section>
{newsletter()}{pie()}"""
    guardar(u(f"/{a['slug']}/"), html)


# ---------- Contacto ----------
def campo_extra(name, etiqueta, tipo, opciones, tipo_id):
    ide = f"{tipo_id}-{name}"
    if LANG == "en":
        etiqueta, opciones_en = TIPOS_EN[tipo_id]["campos"][name]
        if opciones_en:
            opciones = opciones_en
    if tipo == "select":
        if opciones == "ROSTER":
            opciones = [x["nombre"] for x in ARTISTAS]
        ops = "".join(f'<option>{escape(o)}</option>' for o in opciones)
        control = f'<select id="{ide}" name="{name}"><option value="">{t("Elige una opción", "Choose an option")}</option>{ops}</select>'
    else:
        extra = ' min="1"' if tipo == "number" else ""
        control = f'<input type="{tipo}" id="{ide}" name="{name}"{extra}>'
    return f'''            <div>
              <label for="{ide}">{escape(etiqueta)}</label>
              {control}
            </div>'''


def contacto():
    html = cabeza(t("Contacto | Alzada Records", "Contact | Alzada Records"),
                  t("Contacta a Alzada Records: booking de artistas, marcas, sync licensing, envío de material, producción musical y audiovisual, y renta de instalaciones.",
                    "Contact Alzada Records: artist booking, brands, sync licensing, music submissions, music and audiovisual production, and studio rental."),
                  (ruta_contacto("es"), ruta_contacto("en")), "/img/compartir.jpg",
                  '  <script src="/js/contacto.js" defer></script>\n', actual="contacto")
    paises = "".join(
        f'<option value="{escape(t(n, PAISES_EN.get(n, n)))} {l}"{" selected" if i == 0 else ""}>{b} {escape(t(n, PAISES_EN.get(n, n)))} {l}</option>'
        for i, (b, n, l) in enumerate(PAISES))

    def etiqueta(tp):
        return TIPOS_EN[tp["id"]]["etiqueta"] if LANG == "en" else tp["etiqueta"]

    def gracias(tp):
        return TIPOS_EN[tp["id"]]["gracias"] if LANG == "en" else tp["gracias"]

    tipos = "".join(
        f'<option value="{tp["id"]}" data-gracias="{escape(gracias(tp))}">{escape(etiqueta(tp))}</option>'
        for tp in TIPOS)
    grupos = "\n".join(
        f'''          <fieldset class="campos-tipo" data-tipo="{tp["id"]}" hidden disabled>
            <legend>{escape(etiqueta(tp))}</legend>
{chr(10).join(campo_extra(*c, tp["id"]) for c in tp["campos"])}
          </fieldset>''' for tp in TIPOS)
    # Copias ocultas para que Netlify registre cada tipo como formulario aparte (solo en la versión en español;
    # los envíos en inglés llegan a los mismos formularios).
    ocultos = ""
    if LANG == "es":
        todos = ["nombre", "correo", "pais", "telefono", "tipo", "mensaje"]
        filas = []
        for tp in TIPOS:
            nombres = todos + [c[0] for c in tp["campos"]]
            campos = "".join(f'<input name="{n}">' for n in nombres)
            filas.append(f'  <form name="contacto-{tp["id"]}" data-netlify="true" netlify-honeypot="bot-field" hidden>'
                         f'<input name="bot-field">{campos}</form>')
        ocultos = ("  <!-- Copias ocultas para Netlify Forms (una por tipo de solicitud). No se ven en la página. -->\n"
                   + "\n".join(filas) + "\n")
    html += f"""
    <section class="seccion contacto" id="formulario">
      <div class="contenedor contacto-grid">
        <div>
          <h1>{t("Contacto", "Contact")}</h1>
          <p class="seccion-intro">{t("Cuéntanos qué necesitas y la persona indicada de nuestro equipo te contactará.", "Tell us what you need and the right person on our team will get back to you.")}</p>
        </div>

        <form id="form-contacto" class="form-contacto" method="post" novalidate>
          <input type="hidden" name="form-name" value="contacto-booking">
          <p class="trampa" aria-hidden="true"><label>{t("No llenar", "Leave empty")} <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div>
            <label for="c-nombre">{t("Nombre", "Name")} *</label>
            <input type="text" id="c-nombre" name="nombre" autocomplete="name" required>
          </div>
          <div>
            <label for="c-correo">{t("Correo", "Email")} *</label>
            <input type="email" id="c-correo" name="correo" autocomplete="email" spellcheck="false" required>
          </div>
          <div>
            <label for="c-telefono">{t("Teléfono", "Phone")} *</label>
            <div class="telefono">
              <select id="c-pais" name="pais" aria-label="{t("País del teléfono", "Phone country")}" autocomplete="tel-country-code">{paises}</select>
              <input type="tel" id="c-telefono" name="telefono" autocomplete="tel-national" inputmode="tel" required>
            </div>
          </div>
          <div>
            <label for="tipo">{t("Tipo de solicitud", "Request type")} *</label>
            <select id="tipo" name="tipo" required><option value="">{t("Elige una opción", "Choose an option")}</option>{tipos}</select>
          </div>
{grupos}
          <div>
            <label for="c-mensaje">{t("Comentarios", "Comments")} *</label>
            <textarea id="c-mensaje" name="mensaje" rows="5" required></textarea>
          </div>
          <button class="boton" type="submit">{t("Enviar", "Send")}</button>
          <p class="form-mensaje" role="status" aria-live="polite"></p>
        </form>

        <div class="contacto-gracias" id="contacto-gracias" tabindex="-1" hidden>
          <h2>{t("¡Listo!", "Done!")}</h2>
          <p></p>
        </div>
      </div>
    </section>

{ocultos}{pie()}"""
    guardar(ruta_contacto(), html)


# ---------- 404 ----------
def pagina_404():
    ruta = u("/404.html")
    html = cabeza(t("Página no encontrada | Alzada Records", "Page not found | Alzada Records"),
                  t("Esta página no existe.", "This page doesn’t exist."), (ruta, ruta), "/img/compartir.jpg")
    html = html.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n  <meta name="viewport"', 1)
    html += f"""
    <section class="seccion">
      <div class="contenedor">
        <h1>{t("Página no encontrada", "Page not found")}</h1>
        <p class="seccion-intro">{t("La página que buscas no existe o cambió de lugar.", "The page you’re looking for doesn’t exist or has moved.")}</p>
        <p><a class="boton" href="{u("/")}">{t("Ir al inicio", "Go to home")}</a> <a class="boton boton-secundario" href="{u("/#roster")}">{t("Ver roster", "See the roster")}</a></p>
      </div>
    </section>
{pie()}"""
    guardar(ruta, html)


# ---------- Sitemap (los dos idiomas, con su par en el otro idioma) ----------
def sitemap():
    pares = [("/", "/en/"), (ruta_contacto("es"), ruta_contacto("en"))] + \
            [(f"/{a['slug']}/", f"/en/{a['slug']}/") for a in ARTISTAS]
    bloques = []
    for es, en in pares:
        for loc in (es, en):
            bloques.append(
                f"  <url>\n    <loc>{DOMINIO}{loc}</loc>\n"
                f'    <xhtml:link rel="alternate" hreflang="es" href="{DOMINIO}{es}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{DOMINIO}{en}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMINIO}{es}"/>\n  </url>')
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(bloques) + "\n</urlset>\n", encoding="utf-8")


faltan = [a["slug"] for a in ARTISTAS if a["slug"] not in BIOS_EN]
if faltan:
    sys.exit(f"Falta la bio en inglés (datos/bios_en.json) de: {', '.join(faltan)}")

paginas = 0
for LANG in ("es", "en"):
    inicio()
    contacto()
    pagina_404()
    for artista in ARTISTAS:
        pagina_artista(artista)
    paginas += 3 + len(ARTISTAS)
sitemap()
print("Listo:", paginas, "páginas")
