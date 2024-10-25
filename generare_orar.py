import json

# Creare lista cu constrangeri
constrangeri_profesori = [
    {
        "profesor": "Ion Popescu",
        "zi": "joi",
        "interval": "dupa ora 16:00",
        "preferinta": "nu doreste ore"
    },
    {
        "profesor": "Maria Ionescu",
        "zi": "vineri",
        "interval": "pana la ora 14:00",
        "preferinta": "vrea ore"
    },
    {
        "profesor": "George Vasilescu",
        "zi": "miercuri",
        "interval": "dupa ora 15:00",
        "preferinta": "nu doreste ore"
    }
]

# Scriere in fisier JSON
with open('constrangeri_profesori.json', 'w') as f:
    json.dump(constrangeri_profesori, f, indent=4, ensure_ascii=False)

print("Fișierul 'constrangeri_profesori.json' a fost generat cu succes.")
