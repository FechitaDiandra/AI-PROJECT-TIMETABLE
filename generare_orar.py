import json

# Definim zilele săptămânii și intervalele orare
zile_saptamanii = [1, 2, 3, 4, 5]  # Luni-Vineri
intervale_orare = [1, 2, 3, 4, 5, 6]  # Intervalele orare 1-6

# Lista în care vom stoca obiectele
orar = []

# Generăm 30 de obiecte fără detalii suplimentare
for zi in zile_saptamanii:
    for interval in intervale_orare:
        interval_orar = {
            "zi": zi,
            "interval": interval,
            "profesor": None,  # Profesor necompletat
            "sala": None,      # Sala necompletată
            "grupa": None,     # Grupa necompletată
            "materie": None,   # Materie necompletată
            "tip": None        # Tip (Curs/Laborator) necompletat
        }
        orar.append(interval_orar)

# Salvăm obiectele într-un fișier JSON
with open('orar.json', 'w') as file:
    json.dump(orar, file, indent=4)

# Afișăm rezultatul
print(json.dumps(orar, indent=4))
