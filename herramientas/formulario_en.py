"""Textos en inglés del formulario de Contacto (para /en/contact/).

Mismo orden y mismos "id" y "name" que formulario.py; solo cambian las palabras.
Si agregas una opción o pregunta en formulario.py, agrégala aquí también.
"""

TIPOS_EN = {
    "booking": {
        "etiqueta": "Artist booking",
        "campos": {
            "artista": ("Artist", None),
            "fecha_evento": ("Event date", None),
            "ciudad": ("Event city and country", None),
            "tipo_evento": ("Event type", ["Concert", "Festival", "Private event", "Corporate event", "Other"]),
            "presupuesto": ("Approximate budget", None),
        },
        "gracias": "Thank you! We got your booking request. Our team will reach out to go over dates and availability.",
    },
    "marcas": {
        "etiqueta": "Brands and partnerships",
        "campos": {
            "empresa": ("Brand or company", None),
            "tipo_colaboracion": ("Type of partnership",
                                  ["Artist campaign", "Social media content", "Sponsorship", "Product or merch", "Other"]),
        },
        "gracias": "Thank you! We got your proposal. Our brand team will review it and get back to you.",
    },
    "sync": {
        "etiqueta": "Sync licensing",
        "campos": {
            "empresa": ("Company, agency or production company", None),
            "proyecto": ("Project type", ["Film", "Series", "Ad campaign", "Video game", "Digital content", "Other"]),
            "cancion": ("Song or artist you’re interested in", None),
            "fecha_uso": ("Project release date", None),
        },
        "gracias": "Thank you! We got your sync request. We’ll reach out with catalog options and next steps.",
    },
    "talento": {
        "etiqueta": "Talent – Submit your music",
        "campos": {
            "nombre_artistico": ("Artist name", None),
            "ciudad": ("City", None),
            "link_musica": ("Link to your music (Spotify, YouTube, SoundCloud…)", None),
            "redes": ("Your Instagram or TikTok", None),
        },
        "gracias": "Thanks for sharing your music! We listen to everything we receive; if we’re interested, we’ll be in touch.",
    },
    "produccion": {
        "etiqueta": "Music production",
        "campos": {
            "servicio": ("Service", ["Production", "Mixing", "Mastering", "Songwriting", "Other"]),
            "link_musica": ("Reference link or demo (optional)", None),
            "fecha_estimada": ("Estimated date", None),
        },
        "gracias": "Thank you! We got your music production request. We’ll reach out with availability and a quote.",
    },
    "audiovisual": {
        "etiqueta": "Audiovisual production",
        "campos": {
            "servicio": ("Service", ["Music video", "Social media content", "Photography", "Commercial", "Other"]),
            "fecha_estimada": ("Estimated date", None),
            "presupuesto": ("Approximate budget", None),
        },
        "gracias": "Thank you! We got your audiovisual production request. We’ll reach out with availability and a quote.",
    },
    "instalaciones": {
        "etiqueta": "Studio rental / Camps",
        "campos": {
            "espacio": ("What you need", ["Recording studio", "Songwriting camp", "Live room / session", "Other"]),
            "fechas": ("Dates you’re interested in", None),
            "personas": ("Number of people", None),
        },
        "gracias": "Thank you! We got your request. We’ll reach out with availability and pricing for our facilities.",
    },
}

PAISES_EN = {
    "México": "Mexico", "Estados Unidos": "United States", "Canadá": "Canada", "Perú": "Peru",
    "Panamá": "Panama", "República Dominicana": "Dominican Republic", "España": "Spain", "Otro": "Other",
}
