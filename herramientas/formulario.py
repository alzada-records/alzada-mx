"""Formulario de Contacto de Alzada: tipos de solicitud, preguntas extra y mensaje final.

Cada tipo se guarda en Netlify como un formulario aparte ("contacto-<id>"), así en
Netlify (Forms > Form notifications) se le pone a cada uno el correo de la persona
que lo atiende. La persona que llena el formulario solo ve uno.

Para cambiar opciones, preguntas o mensajes edita esta lista y vuelve a correr
herramientas/generar.py.
"""

# Campo extra: (name, etiqueta, tipo, opciones)
#   tipo: "text", "url", "date", "number" o "select" (para select, opciones es una lista)
TIPOS = [
    {
        "id": "booking",
        "etiqueta": "Booking de artistas",
        "campos": [
            ("artista", "Artista", "select", "ROSTER"),
            ("fecha_evento", "Fecha del evento", "date", None),
            ("ciudad", "Ciudad y país del evento", "text", None),
            ("tipo_evento", "Tipo de evento", "select",
             ["Concierto", "Festival", "Evento privado", "Evento corporativo", "Otro"]),
            ("presupuesto", "Presupuesto aproximado", "text", None),
        ],
        "gracias": "¡Gracias! Recibimos tu solicitud de booking. El equipo te contactará para revisar fecha y disponibilidad.",
    },
    {
        "id": "marcas",
        "etiqueta": "Marcas y colaboraciones",
        "campos": [
            ("empresa", "Marca o empresa", "text", None),
            ("tipo_colaboracion", "Tipo de colaboración", "select",
             ["Campaña con artista", "Contenido para redes", "Patrocinio", "Producto o merch", "Otro"]),
        ],
        "gracias": "¡Gracias! Recibimos tu propuesta. El equipo de marcas la revisará y te contactará.",
    },
    {
        "id": "sync",
        "etiqueta": "Sincronizaciones (Sync Licensing)",
        "campos": [
            ("empresa", "Empresa, agencia o productora", "text", None),
            ("proyecto", "Tipo de proyecto", "select",
             ["Película", "Serie", "Campaña publicitaria", "Videojuego", "Contenido digital", "Otro"]),
            ("cancion", "Canción o artista de interés", "text", None),
            ("fecha_uso", "Fecha de lanzamiento del proyecto", "date", None),
        ],
        "gracias": "¡Gracias! Recibimos tu solicitud de sync. Te contactaremos con opciones del catálogo y los siguientes pasos.",
    },
    {
        "id": "talento",
        "etiqueta": "Talento – Envío de material",
        "campos": [
            ("nombre_artistico", "Nombre artístico", "text", None),
            ("ciudad", "Ciudad", "text", None),
            ("link_musica", "Link a tu música (Spotify, YouTube, SoundCloud…)", "url", None),
            ("redes", "Tu Instagram o TikTok", "text", None),
        ],
        "gracias": "¡Gracias por compartir tu música! Escuchamos todo el material que nos llega; si hay interés, te contactaremos.",
    },
    {
        "id": "produccion",
        "etiqueta": "Producción musical",
        "campos": [
            ("servicio", "Servicio", "select",
             ["Producción", "Mezcla", "Masterización", "Composición", "Otro"]),
            ("link_musica", "Link de referencia o demo (opcional)", "url", None),
            ("fecha_estimada", "Fecha estimada", "date", None),
        ],
        "gracias": "¡Gracias! Recibimos tu solicitud de producción musical. Te contactaremos con disponibilidad y cotización.",
    },
    {
        "id": "audiovisual",
        "etiqueta": "Producción audiovisual",
        "campos": [
            ("servicio", "Servicio", "select",
             ["Videoclip", "Contenido para redes", "Fotografía", "Comercial", "Otro"]),
            ("fecha_estimada", "Fecha estimada", "date", None),
            ("presupuesto", "Presupuesto aproximado", "text", None),
        ],
        "gracias": "¡Gracias! Recibimos tu solicitud de producción audiovisual. Te contactaremos con disponibilidad y cotización.",
    },
    {
        "id": "instalaciones",
        "etiqueta": "Renta de instalaciones / Camps",
        "campos": [
            ("espacio", "Qué necesitas", "select",
             ["Estudio de grabación", "Camp de composición", "Foro / sesión", "Otro"]),
            ("fechas", "Fechas que te interesan", "text", None),
            ("personas", "Número de personas", "number", None),
        ],
        "gracias": "¡Gracias! Recibimos tu solicitud. Te contactaremos con disponibilidad y precios de las instalaciones.",
    },
]

# Países para el teléfono: (bandera, nombre, lada). El primero sale seleccionado.
PAISES = [
    ("🇲🇽", "México", "+52"),
    ("🇺🇸", "Estados Unidos", "+1"),
    ("🇨🇦", "Canadá", "+1"),
    ("🇨🇴", "Colombia", "+57"),
    ("🇦🇷", "Argentina", "+54"),
    ("🇨🇱", "Chile", "+56"),
    ("🇵🇪", "Perú", "+51"),
    ("🇪🇨", "Ecuador", "+593"),
    ("🇻🇪", "Venezuela", "+58"),
    ("🇬🇹", "Guatemala", "+502"),
    ("🇸🇻", "El Salvador", "+503"),
    ("🇭🇳", "Honduras", "+504"),
    ("🇨🇷", "Costa Rica", "+506"),
    ("🇵🇦", "Panamá", "+507"),
    ("🇩🇴", "República Dominicana", "+1"),
    ("🇵🇷", "Puerto Rico", "+1"),
    ("🇪🇸", "España", "+34"),
    ("🌎", "Otro", ""),
]
