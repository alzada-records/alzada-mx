# alzada-mx

Sitio web de Alzada (alzada.mx), HTML y CSS sin CMS. Misma base que ladrones.mx.

## Cómo está armado

- `datos/artistas.json`: nombre, bio y redes de cada artista. **Aquí se cambian los textos.**
- `herramientas/generar.py`: arma `index.html` y la página de cada artista (`/c-kan/`, `/maho/`…) a partir de `artistas.json`. Después de cambiar el JSON se vuelve a correr.
- `js/hero.js` + lista `HERO` en `herramientas/generar.py`: lanzamientos destacados del encabezado del inicio, rotan cada 10 s (con botón de pausa).
- `js/videos.js`: reproductor con el estreno más nuevo de un canal de YouTube y los 8 que siguen. En el inicio usa el canal de Alzada y en cada artista su canal (`canal_youtube` en `artistas.json`). Se saltan audios, lyric videos, en vivo, teasers, etc.
- `js/merch.js`: productos de la colección merch-alzada de Alzada Streetwear (Shopify).
- `herramientas/formulario.py`: tipos de solicitud de Contacto, sus preguntas extra y el mensaje final de cada uno.
- `js/contacto.js`: muestra las preguntas del tipo elegido y envía a Netlify Forms como `contacto-<tipo>` (solo funciona ya publicado en Netlify).
- `js/newsletter.js`: formulario a Mailchimp (misma audiencia que Ladrones).
- `img/artistas/`: foto de cada artista en cuadro (400 y 800 px) y grande para su página.
- Las direcciones de los artistas son las mismas que en Wix para no perder Google.

## Lista de pendientes

- [ ] Versión en inglés en `/en/`
- [ ] En Netlify > Forms > notificaciones: avisos a charliefelix@alzada.mx para booking, marcas, sync, produccion, audiovisual e instalaciones
- [x] Redirecciones de Wix, sitemap (se arma solo con generar.py), robots y página 404
- [ ] Netlify y dominio alzada.mx
