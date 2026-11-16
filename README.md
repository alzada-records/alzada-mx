# alzada-mx

Sitio web de Alzada (alzada.mx), HTML y CSS sin CMS. Misma base que ladrones.mx.

## Cómo está armado

- `datos/artistas.json`: nombre, bio y redes de cada artista. **Aquí se cambian los textos.**
- `herramientas/generar.py`: arma `index.html` y la página de cada artista (`/c-kan/`, `/maho/`…) a partir de `artistas.json`. Después de cambiar el JSON se vuelve a correr.
- `js/videos.js`: el video más nuevo del canal de YouTube de Alzada y los 8 que siguen (YouTube Data API, misma clave que Ladrones).
- `js/merch.js`: productos de la colección merch-alzada de Alzada Streetwear (Shopify).
- `js/newsletter.js`: formulario a Mailchimp (misma audiencia que Ladrones).
- `img/artistas/`: foto de cada artista en cuadro (400 y 800 px) y grande para su página.
- Las direcciones de los artistas son las mismas que en Wix para no perder Google.

## Lista de pendientes

- [ ] Links de redes de MAHO
- [ ] Versión en inglés en `/en/`
- [ ] Nosotros, Sync Licensing y Contacto
- [ ] Redirecciones de Wix (`/blog`), sitemap y robots
- [ ] Netlify y dominio alzada.mx
