BANCO_DE_PROMPT = [

    {
        "nombre": "HotelAmaru",
        "system_instruction": "Eres un experto en Hotel Amaru de Arica.",
        "ejemplo_usuario": "Dame información de Contacto del Hotel Amaru en Arica.",
    "claves_esperadas": ["Telefono", "Direccion", "Email", "Distancia del Morro de Arica"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "Telefono": {"type": "STRING"},
                "Direccion": {"type": "STRING"},
                "Email": {"type": "STRING"},
                "Distancia del Morro de Arica": {"type": "INTEGER"},
            },
            "required": ["Telefono", "Direccion", "Email", "Distancia del Morro de Arica"]
        }
    }
,
    {
            "nombre": "HotelSpaLasTaguas",
            "system_instruction": "Eres un experto en Hotel Spa Las Taguas de Arica.",
            "ejemplo_usuario": "Dame información de Contacto del Hotel Spa Las Taguas en Arica.",
        "claves_esperadas": ["Telefono", "Direccion", "Email", "Distancia del Morro de Arica"],
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "Telefono": {"type": "STRING"},
                    "Direccion": {"type": "STRING"},
                    "Email": {"type": "STRING"},
                    "Distancia del Morro de Arica": {"type": "INTEGER"},
                },
                "required": ["Telefono", "Direccion", "Email", "Distancia del Morro de Arica"]
            }
        }
]

