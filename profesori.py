import json

profesori = {
    "profesori": [
        {
            "nume": "Prof. Popescu",
            "disponibilitate": {
                "luni": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "marți": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "miercuri": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "joi": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "vineri": {
                    "intervale": [],
                    "maxim_ore": 0
                }
            },
            "curs_inainte_de_laborator": False
        },
        {
            "nume": "Prof. Ionescu",
            "disponibilitate": {
                "luni": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "marți": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "miercuri": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "joi": {
                    "intervale": [],
                    "maxim_ore": 0
                },
                "vineri": {
                    "intervale": [],
                    "maxim_ore": 0
                }
            },
            "curs_inainte_de_laborator": False
        }
    ]
}

with open('profesori.json', 'w') as f:
    json.dump(profesori, f, indent=4)

print("Constrângerile profesorilor au fost salvate în 'profesori.json'.")
