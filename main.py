import json
import re

# Funcție pentru maparea zilelor săptămânii
def mapare_zile_saptamanii(text):
    zile = {
        "luni": 1,
        "marți": 2,
        "miercuri": 3,
        "joi": 4,
        "vineri": 5
    }
    for zi in zile:
        if zi in text.lower():
            return zile[zi]
    return None

# Funcție pentru maparea intervalelor orare
def mapare_intervale_orare(text):
    intervale = {
        "08:00": 1,
        "10:00": 2,
        "12:00": 3,
        "14:00": 4,
        "16:00": 5,
        "18:00": 6
    }
    for ora, cod in intervale.items():
        if ora in text:
            return cod
    return None

# Funcție pentru extragerea profesorului din text
def extragere_profesor(text):
    match = re.search(r"profesorul (\w+)", text.lower())
    if match:
        return match.group(1).capitalize()
    return None

# Funcție pentru aplicarea modificărilor în orar
def aplicare_modificari(orar, mesaj):
    ziua = mapare_zile_saptamanii(mesaj)
    interval = mapare_intervale_orare(mesaj)
    profesor = extragere_profesor(mesaj)

    if ziua is not None and interval is not None and profesor is not None:
        for interval_orar in orar:
            if interval_orar["zi"] == ziua and interval_orar["interval"] == interval:
                # Verificăm dacă mesajul conține "nu vrea"
                if "nu vrea" in mesaj.lower():
                    interval_orar["profesor"] = None  # Eliminăm profesorul din orar
                    print(f"Orarul a fost actualizat (eliminare): {interval_orar}")
                elif "vrea" in mesaj.lower():
                    interval_orar["profesor"] = profesor  # Setăm profesorul
                    print(f"Orarul a fost actualizat (adăugare): {interval_orar}")
                return

    print("Nu s-au putut aplica modificările. Verificați mesajul de intrare.")

# Citirea orarului din fișier JSON
def citire_orar_din_fisier(fisier):
    with open(fisier, 'r', encoding='utf-8') as f:
        return json.load(f)

# Scrierea orarului actualizat în fișier JSON
def scriere_orar_in_fisier(fisier, orar):
    with open(fisier, 'w', encoding='utf-8') as f:
        json.dump(orar, f, indent=4)

# Fișierul orar.json
fisier_orar = 'orar.json'

# Citim orarul din fișier
orar = citire_orar_din_fisier(fisier_orar)

# Mesaj de la prompt (exemple)
mesaj2 = "Profesorul Popescu vrea să aibă cursuri luni de la 08:00 la 10:00."

# Aplicăm modificările pentru mesajul 1


# Aplicăm modificările pentru mesajul 2
aplicare_modificari(orar, mesaj2)

# Scriem orarul actualizat în fișier
scriere_orar_in_fisier(fisier_orar, orar)

# Afișăm orarul actualizat

