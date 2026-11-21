revision_manual = [

    {
        "consulta": "¿Cuándo se creó Python?",
        "f1": 0.44,
        "correccion_factual": "no",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "la respuesta da un año distinto al de la referencia"
        ),
    },

]



import json



with open(

    "docs/revision_manual.json", "w", encoding="utf-8"

) as archivo:

    json.dump(

        revision_manual, archivo, indent=2, ensure_ascii=False

    )
