"""Arma las páginas del sitio de Alzada a partir de datos/artistas.json.

Uso (desde la carpeta del sitio):  python3 herramientas/generar.py

Genera:
  index.html            inicio (videos, redes, roster, merch, formulario)
  <artista>/index.html  una página por artista (misma dirección que en Wix)

Para cambiar un texto o un link de un artista, edita datos/artistas.json y
vuelve a correr este script. El orden del roster es el orden del archivo.
"""
import json
import pathlib
import sys
from urllib.parse import quote
from html import escape

from PIL import Image

from formulario import TIPOS, PAISES

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
DOMINIO = "https://www.alzada.mx"
ARTISTAS = json.loads((RAIZ / "datos/artistas.json").read_text(encoding="utf-8"))

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
HERO = [
    {"artista": "Ladrones", "titulo": "Arriba La L", "tipo": "Nuevo álbum · 2026",
     "portada": "/img/lanzamientos/arriba-la-l.webp",
     "fondo": ("/img/fondos/musica-960.webp", "/img/fondos/musica-1920.webp"),
     "posicion": "center 20%",
     "escuchar": "https://open.spotify.com/album/1XKtSl05ezH6lWTmVgTLUL",
     "mas": ("Toda la música", "https://www.ladrones.mx/lanzamientos/")},
    {"artista": "Toser One", "titulo": "Trankilon", "tipo": "Nuevo sencillo · 2026",
     "portada": "https://i.scdn.co/image/ab67616d00001e02b963875867bace9f797e7dc9",
     "fondo": ("/img/artistas/toser-one-grande.webp", "/img/artistas/toser-one-grande.webp"),
     "posicion": "center 25%",
     "escuchar": "https://open.spotify.com/album/6PIPifvLUMtTrjBacOlpqX",
     "mas": ("Ver artista", "/toser-one/")},
    {"artista": "Zxmyr", "titulo": "ZXM-YR Mami", "tipo": "Nuevo álbum · 2026",
     "portada": "https://i.scdn.co/image/ab67616d00001e02834c90c7f6457811efc48042",
     "fondo": ("/img/artistas/zxmyr-grande.webp", "/img/artistas/zxmyr-grande.webp"),
     "posicion": "center 30%",
     "escuchar": "https://open.spotify.com/album/1lQGIOE4Buny19S91SjKKy",
     "mas": ("Ver artista", "/zxmyr/")},
]

MAILCHIMP = "https://alzada.us19.list-manage.com/subscribe/post?u=32d94c0e4051438d818e68013&amp;id=4bd0645e6c&amp;f_id=00b59be3f0"
TRAMPA = "b_32d94c0e4051438d818e68013_4bd0645e6c"


def cabeza(titulo, descripcion, ruta, imagen, extra=""):
    return f"""<!doctype html>
<html lang="es">
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
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Alzada">
  <meta property="og:locale" content="es_MX">
  <meta property="og:url" content="{DOMINIO}{ruta}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{DOMINIO}{ruta}">
  <link rel="icon" href="/img/favicon.png" type="image/png">
  <link rel="stylesheet" href="/css/styles.css">
{extra}  <script src="/js/main.js" defer></script>
  <script src="/js/newsletter.js" defer></script>
</head>
<body>
  <a class="saltar" href="#contenido">Saltar al contenido</a>

  <header class="encabezado">
    <div class="contenedor">
      <a class="logo" href="/"><img src="/img/logo.webp" alt="Alzada" width="88" height="96"></a>
      <nav aria-label="Principal">
        <button class="menu-boton" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
        <ul class="menu" id="menu">
          <li><a href="/"{' aria-current="page"' if ruta == "/" else ""}>Inicio</a></li>
          <li><a href="/#roster">Roster</a></li>
          <li><a href="/#lanzamientos">Lanzamientos</a></li>
          <li><a href="/#nosotros">Nosotros</a></li>
          <li><a href="/#sync">Sync</a></li>
          <li><a href="/#merch">Merch</a></li>
          <li><a href="/contacto/"{' aria-current="page"' if ruta == "/contacto/" else ""}>Contacto</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="contenido">
"""


def lista_redes(redes, clase, tam, con_texto, nombre):
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
                         f'<img src="/img/redes/{icono}.png" alt="{visible} de {escape(nombre)}" '
                         f'width="{tam}" height="{tam}" loading="lazy"></a></li>')
    return "\n".join(items)


def barra_redes(redes, nombre):
    if not redes:
        return ""
    return f"""
    <!-- Barra de redes -->
    <nav class="barra-redes" aria-label="Redes de {escape(nombre)}">
      <div class="contenedor">
        <ul>
{lista_redes(redes, "", 24, True, nombre)}
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
        <h2 id="titulo-newsletter">Únete a la familia</h2>
        <p class="seccion-intro">Lanzamientos, fechas y noticias de tus artistas favoritos.</p>
        <form class="form-lista" action="{MAILCHIMP}" method="post" target="_blank" rel="noopener" novalidate>
          <div>
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" name="FNAME" autocomplete="given-name" required>
          </div>
          <div>
            <label for="correo">Correo</label>
            <input type="email" id="correo" name="EMAIL" autocomplete="email" spellcheck="false" required>
          </div>
          <div class="casilla">
            <input type="checkbox" id="acepto" name="acepto" required>
            <label for="acepto">Quiero recibir noticias de Alzada y sus artistas.</label>
          </div>
          <div class="trampa" aria-hidden="true"><input type="text" name="{TRAMPA}" tabindex="-1" value="" autocomplete="off"></div>
          <button class="boton" type="submit">Suscribirme</button>
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
      <p>Sigue a <span translate="no">Alzada</span></p>
      <ul class="redes">
{lista_redes(REDES_ALZADA, "", 28, False, "Alzada")}
      </ul>
      <p>© 2027 <span translate="no">Alzada Corp</span></p>
    </div>
  </footer>
</body>
</html>
"""


def roster():
    tarjetas = []
    for i, a in enumerate(ARTISTAS):
        carga = '' if i < 4 else ' loading="lazy"'
        tarjetas.append(f"""          <li class="artista-tarjeta">
            <a href="/{a['slug']}/">
              <img src="/img/artistas/{a['slug']}-400.webp" srcset="/img/artistas/{a['slug']}-400.webp 400w, /img/artistas/{a['slug']}-800.webp 800w" sizes="(min-width: 1000px) 260px, (min-width: 600px) 33vw, 50vw" alt="" width="400" height="400"{carga}>
              <span class="artista-nombre" translate="no">{escape(a['nombre'])}</span>
            </a>
          </li>""")
    return "\n".join(tarjetas)


def hero():
    diapos, puntos = [], []
    for i, h in enumerate(HERO):
        externo = h["mas"][1].startswith("http")
        mas_extra = ' target="_blank" rel="noopener"' if externo else ""
        carga = "" if i == 0 else ' loading="lazy"'
        diapos.append(f"""        <div class="hero-diapo hero-foto{' activa' if i == 0 else ''}" role="group" aria-roledescription="diapositiva" aria-label="{i + 1} de {len(HERO)}"
          style="--fondo-chico: url('{h['fondo'][0]}'); --fondo-grande: url('{h['fondo'][1]}'); --fondo-posicion: {h['posicion']};">
          <div class="contenedor">
            <div class="hero-lanzamiento">
              <img src="{h['portada']}" alt="Portada de {escape(h['titulo'])}" width="300" height="300"{carga}>
              <p class="seccion-intro"><span translate="no">{escape(h['artista'])}</span> · {escape(h['tipo'])}</p>
            </div>
            <h2 class="hero-titulo"><span translate="no">{escape(h['titulo'])}</span></h2>
            <p><a class="boton" href="{h['escuchar']}" target="_blank" rel="noopener">Escuchar</a>
               <a class="boton boton-secundario" href="{h['mas'][1]}"{mas_extra}>{escape(h['mas'][0])}</a></p>
          </div>
        </div>""")
        puntos.append(f'<button type="button" class="hero-punto" aria-label="Ver {escape(h["titulo"])}"></button>')
    return f"""    <!-- Lanzamientos destacados: rotan cada 10 s (js/hero.js). Se cambian en HERO, arriba en este archivo. -->
    <section class="hero-carrusel" aria-roledescription="carrusel" aria-label="Lanzamientos destacados">
      <h1 class="oculto">Alzada Records</h1>
{chr(10).join(diapos)}
      <div class="hero-controles contenedor">
        <div class="hero-puntos">{"".join(puntos)}</div>
        <button type="button" class="hero-pausa"></button>
      </div>
    </section>

"""


def inicio():
    html = cabeza("Alzada Records | Disquera mexicana independiente",
                  "Alzada Records: disquera mexicana independiente. Conoce a nuestros artistas, sus lanzamientos y el merch oficial.",
                  "/", "/img/compartir.jpg",
                  '  <link rel="preload" as="image" href="/img/fondos/musica-1920.webp" media="(min-width: 900px)" fetchpriority="high">\n'
                  '  <link rel="preload" as="image" href="/img/fondos/musica-960.webp" media="(max-width: 899px)" fetchpriority="high">\n'
                  '  <link rel="preconnect" href="https://www.youtube.com">\n'
                  '  <link rel="preconnect" href="https://www.googleapis.com">\n'
                  '  <link rel="preconnect" href="https://alzadastreetwear.com">\n'
                  '  <script src="/js/videos.js" defer></script>\n'
                  '  <script src="/js/hero.js" defer></script>\n'
                  '  <script src="/js/merch.js" defer></script>\n')
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
        <h2 id="titulo-videos">Lanzamientos</h2>
        <iframe class="video" id="reproductor"
          src="https://www.youtube.com/embed/videoseries?list=UULFb41Xk6cDPcz1r_xEhQqvuA"
          title="Videos más recientes de Alzada"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
        <p class="video-actual" id="video-actual" aria-live="polite"></p>
        <ul class="videos-lista" id="videos-lista" aria-label="Más videos"></ul>
      </div>
    </section>

    <!-- Nosotros -->
    <section class="seccion nosotros" id="nosotros" aria-labelledby="titulo-nosotros">
      <div class="contenedor nosotros-grid">
        <div>
          <h2 id="titulo-nosotros">Nosotros</h2>
          <p><span translate="no">Alzada</span> nace en Guadalajara, Jalisco, para abrirle paso al talento emergente en una industria llena de barreras y fórmulas repetidas. Lo que empezó como un movimiento independiente hoy es un ecosistema creativo construido sobre la autenticidad, la calle y la conexión directa con una nueva generación.</p>
          <p>Desde etapas tempranas ha apostado por artistas que hoy son referentes de la escena urbana en México y Latinoamérica. Con producción audiovisual, contenido digital, colaboraciones con marcas y experiencias en vivo, <span translate="no">Alzada</span> es más que un sello: una plataforma 360 que sigue rompiendo esquemas y elevando el estándar de la música en Latinoamérica.</p>
        </div>
        <img src="/img/nosotros-800.webp" srcset="/img/nosotros-800.webp 800w, /img/nosotros-1400.webp 1400w" sizes="(min-width: 900px) 540px, 100vw" alt="Artistas de Alzada con sus discos de certificación" width="1400" height="933" loading="lazy">
      </div>
    </section>
    <!-- Sync / Licensing -->
    <section class="seccion nosotros sync" id="sync" aria-labelledby="titulo-sync">
      <div class="contenedor nosotros-grid">
        <img src="/img/sync-800.webp" srcset="/img/sync-800.webp 800w, /img/sync-1400.webp 1400w" sizes="(min-width: 900px) 540px, 100vw" alt="Recepción de las oficinas de Alzada con discos de certificación en las paredes" width="1400" height="933" loading="lazy">
        <div>
          <h2 id="titulo-sync">Sync / Licensing</h2>
          <p>En <span translate="no">Alzada</span>, la sincronización y el licensing convierten la música en un activo estratégico. Nuestro catálogo reúne propuestas auténticas y versátiles, listas para integrarse en películas, series, campañas, videojuegos y contenido digital, aportando identidad, emoción y valor a cada proyecto.</p>
          <p>Trabajamos de forma ágil y curatorial, facilitando la gestión de derechos, autorizaciones y entregables para acelerar procesos sin fricción. Desde la selección del track ideal hasta el cierre de la licencia, alineamos creatividad con objetivos comerciales, ayudando a marcas, agencias y productoras a conectar con nuevas audiencias a través de la música.</p>
          <p><a class="boton" href="/contacto/?tipo=sync#formulario">Contactar</a></p>
        </div>
      </div>
    </section>
    <!-- Merch: productos de Alzada Streetwear (Shopify). Se llenan solos con js/merch.js. -->
    <section class="seccion merch" id="merch" aria-labelledby="titulo-merch">
      <div class="contenedor">
        <div class="merch-encabezado">
          <h2 id="titulo-merch">Merch</h2>
          <div class="merch-flechas" hidden>
            <button type="button" class="merch-flecha" data-dir="-1" aria-label="Productos anteriores">←</button>
            <button type="button" class="merch-flecha" data-dir="1" aria-label="Más productos">→</button>
          </div>
        </div>
        <ul class="merch-lista" id="merch-lista" aria-live="polite"></ul>
        <p><a class="boton boton-secundario" href="{TIENDA}" target="_blank" rel="noopener">Ver tienda</a></p>
      </div>
    </section>
{newsletter()}{pie()}"""
    (RAIZ / "index.html").write_text(html, encoding="utf-8")


def pagina_artista(a):
    nombre = a["nombre"]
    resumen = a["bio"][0].split(". ")[0] + "."
    spotify = a["redes"].get("spotify", "")
    html = cabeza(f"{nombre} | Alzada Records", resumen, f"/{a['slug']}/",
                  f"/img/artistas/{a['slug']}-800.webp",
                  '  <script src="/js/videos.js" defer></script>\n' if a.get("canal_youtube") else "")
    parrafos = "\n".join(f"          <p>{escape(p)}</p>" for p in a["bio"])
    sitio = '\n          <p class="artista-botones"><a class="boton" href="/contacto/?tipo=booking&amp;artista=' + quote(a["nombre"]) + '#formulario">Contrataciones</a>'
    if a.get("sitio"):
        sitio += f'\n             <a class="boton boton-secundario" href="{a["sitio"]}" target="_blank" rel="noopener">Sitio oficial</a>'
    sitio += '</p>'
    musica = ""
    if spotify:
        embed = spotify.replace("open.spotify.com/artist/", "open.spotify.com/embed/artist/")
        musica = f"""
    <section class="seccion" aria-labelledby="titulo-musica">
      <div class="contenedor">
        <h2 id="titulo-musica">Música</h2>
        <iframe class="spotify" src="{embed}?theme=0" title="{escape(nombre)} en Spotify" width="100%" height="352" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
      </div>
    </section>
"""
    with Image.open(RAIZ / f"img/artistas/{a['slug']}-grande.webp") as foto:
        ancho, alto = foto.size
    videos = ""
    canal = a.get("canal_youtube")
    if canal:
        videos = f"""
    <!-- Videos: el estreno más nuevo de su canal y los que siguen (js/videos.js) -->
    <section class="seccion" data-canal="{canal}" aria-labelledby="titulo-videos">
      <div class="contenedor">
        <h2 id="titulo-videos">Videos</h2>
        <iframe class="video" id="reproductor"
          src="https://www.youtube.com/embed/videoseries?list=UULF{canal[2:]}"
          title="Videos de {escape(nombre)}"
          loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
        <p class="video-actual" id="video-actual" aria-live="polite"></p>
        <ul class="videos-lista" id="videos-lista" aria-label="Más videos de {escape(nombre)}"></ul>
      </div>
    </section>
"""
    html += f"""
    <section class="seccion portada artista">
      <div class="contenedor artista-grid">
        <img class="artista-foto" src="/img/artistas/{a['slug']}-grande.webp" alt="{escape(nombre)}" width="{ancho}" height="{alto}" fetchpriority="high">
        <div class="artista-texto">
          <p class="seccion-intro"><a href="/#roster">Roster</a></p>
          <h1 translate="no">{escape(nombre)}</h1>
{parrafos}{sitio}
        </div>
      </div>
    </section>
{barra_redes(a["redes"], nombre)}{musica}{videos}
    <!-- Fechas: Bandsintown (se actualizan solas) -->
    <section class="seccion fechas" aria-labelledby="titulo-fechas">
      <div class="contenedor">
        <h2 id="titulo-fechas">Próximas fechas</h2>
        <script charset="utf-8" src="https://widgetv3.bandsintown.com/main.min.js"></script>
        <a class="bit-widget-initializer"
          data-artist-name="{escape(a.get('bandsintown', nombre))}"
          data-app-id="js_www.alzada.mx"
          data-display-limit="8"
          data-language="es"
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
    carpeta = RAIZ / a["slug"]
    carpeta.mkdir(exist_ok=True)
    (carpeta / "index.html").write_text(html, encoding="utf-8")


def campo_extra(name, etiqueta, tipo, opciones, tipo_id):
    ide = f"{tipo_id}-{name}"
    if tipo == "select":
        if opciones == "ROSTER":
            opciones = [x["nombre"] for x in ARTISTAS]
        ops = "".join(f'<option>{escape(o)}</option>' for o in opciones)
        control = f'<select id="{ide}" name="{name}"><option value="">Elige una opción</option>{ops}</select>'
    else:
        extra = ' min="1"' if tipo == "number" else ""
        control = f'<input type="{tipo}" id="{ide}" name="{name}"{extra}>'
    return f'''            <div>
              <label for="{ide}">{escape(etiqueta)}</label>
              {control}
            </div>'''


def contacto():
    html = cabeza("Contacto | Alzada Records",
                  "Contacta a Alzada Records: booking de artistas, marcas, sync licensing, envío de material, producción musical y audiovisual, y renta de instalaciones.",
                  "/contacto/", "/img/compartir.jpg",
                  '  <script src="/js/contacto.js" defer></script>\n')
    paises = "".join(
        f'<option value="{escape(n)} {l}"{" selected" if i == 0 else ""}>{b} {escape(n)} {l}</option>'
        for i, (b, n, l) in enumerate(PAISES))
    tipos = "".join(
        f'<option value="{t["id"]}" data-gracias="{escape(t["gracias"])}">{escape(t["etiqueta"])}</option>'
        for t in TIPOS)
    grupos = "\n".join(
        f'''          <fieldset class="campos-tipo" data-tipo="{t["id"]}" hidden disabled>
            <legend>{escape(t["etiqueta"])}</legend>
{chr(10).join(campo_extra(*c, t["id"]) for c in t["campos"])}
          </fieldset>''' for t in TIPOS)
    # Copias ocultas para que Netlify registre cada tipo como formulario aparte.
    todos = ["nombre", "correo", "pais", "telefono", "tipo", "mensaje"]
    ocultos = []
    for t in TIPOS:
        nombres = todos + [c[0] for c in t["campos"]]
        campos = "".join(f'<input name="{n}">' for n in nombres)
        ocultos.append(f'  <form name="contacto-{t["id"]}" data-netlify="true" netlify-honeypot="bot-field" hidden>'
                       f'<input name="bot-field">{campos}</form>')
    ocultos = "\n".join(ocultos)
    html += f"""
    <section class="seccion contacto" id="formulario">
      <div class="contenedor contacto-grid">
        <div>
          <h1>Contacto</h1>
          <p class="seccion-intro">Cuéntanos qué necesitas y la persona indicada de nuestro equipo te contactará.</p>
        </div>

        <form id="form-contacto" class="form-contacto" method="post" novalidate>
          <input type="hidden" name="form-name" value="contacto-booking">
          <p class="trampa" aria-hidden="true"><label>No llenar <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div>
            <label for="c-nombre">Nombre *</label>
            <input type="text" id="c-nombre" name="nombre" autocomplete="name" required>
          </div>
          <div>
            <label for="c-correo">Correo *</label>
            <input type="email" id="c-correo" name="correo" autocomplete="email" spellcheck="false" required>
          </div>
          <div>
            <label for="c-telefono">Teléfono *</label>
            <div class="telefono">
              <select id="c-pais" name="pais" aria-label="País del teléfono" autocomplete="tel-country-code">{paises}</select>
              <input type="tel" id="c-telefono" name="telefono" autocomplete="tel-national" inputmode="tel" required>
            </div>
          </div>
          <div>
            <label for="tipo">Tipo de solicitud *</label>
            <select id="tipo" name="tipo" required><option value="">Elige una opción</option>{tipos}</select>
          </div>
{grupos}
          <div>
            <label for="c-mensaje">Comentarios *</label>
            <textarea id="c-mensaje" name="mensaje" rows="5" required></textarea>
          </div>
          <button class="boton" type="submit">Enviar</button>
          <p class="form-mensaje" role="status" aria-live="polite"></p>
        </form>

        <div class="contacto-gracias" id="contacto-gracias" tabindex="-1" hidden>
          <h2>¡Listo!</h2>
          <p></p>
        </div>
      </div>
    </section>

  <!-- Copias ocultas para Netlify Forms (una por tipo de solicitud). No se ven en la página. -->
{ocultos}
{pie()}"""
    carpeta = RAIZ / "contacto"
    carpeta.mkdir(exist_ok=True)
    (carpeta / "index.html").write_text(html, encoding="utf-8")


def pagina_404():
    html = cabeza("Página no encontrada | Alzada Records", "Esta página no existe.", "/404.html", "/img/compartir.jpg")
    html = html.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n  <meta name="viewport"', 1)
    html += f"""
    <section class="seccion">
      <div class="contenedor">
        <h1>Página no encontrada</h1>
        <p class="seccion-intro">La página que buscas no existe o cambió de lugar.</p>
        <p><a class="boton" href="/">Ir al inicio</a> <a class="boton boton-secundario" href="/#roster">Ver roster</a></p>
      </div>
    </section>
{pie()}"""
    (RAIZ / "404.html").write_text(html, encoding="utf-8")

def sitemap():
    urls = ["/", "/contacto/"] + [f"/{a['slug']}/" for a in ARTISTAS]
    lineas = "\n".join(f"  <url><loc>{DOMINIO}{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{lineas}\n</urlset>\n", encoding="utf-8")

inicio()
pagina_404()
sitemap()
contacto()
for artista in ARTISTAS:
    pagina_artista(artista)
print("Listo:", 3 + len(ARTISTAS), "páginas")
