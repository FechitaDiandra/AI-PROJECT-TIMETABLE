import json
from collections import deque
import pandas as pd

zile = ["luni", "marti", "miercuri", "joi", "vineri"]
intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]

with open('data/activitati.json') as f:
    activitati = json.load(f)

with open('data/sali.json') as f:
    sali = json.load(f)

with open('data/profesori.json') as f:
    profesori = json.load(f)

with open('constrains/constrangeri.json') as f:
    constrangeri_raw = json.load(f).get("constrangeri", [])

constrangeri_aplicate = set()

def parse_constrangeri(constrangeri_raw):
    constrangeri = []
    for c in constrangeri_raw:
        if c["entitate"] == "profesor":
            constrangeri.append((
                c["nume"],
                None,  # Profesorul nu are o variabila secundara in acest context
                f"x['zi'] != '{c.get('zi', '')}' or x['interval'] != '{c.get('interval_orar', '')}'"
            ))
        elif c["entitate"] == "sala":
            constrangeri.append((
                c["nume"],
                None,  # Sala nu are o variabila secundara in acest context
                f"x['zi'] != '{c.get('zi', '')}' or x['interval'] != '{c.get('interval_orar', '')}'"
            ))
        elif c["entitate"] == "orar":
            constrangeri.append((
                "orar",
                None,
                f"x['interval'] != '{c.get('interval_orar', '')}'"
            ))
    return constrangeri

constrangeri = parse_constrangeri(constrangeri_raw)

def init_domenii(activitati, sali):
    domenii = {}
    for activitate in activitati:
        domenii[activitate["materie"]] = [
            {"sala": sala, "zi": zi, "interval": interval}
            for sala in sali
            for zi in zile
            for interval in intervale
            if check_disponibilitate(sala, zi, interval)
        ]
    return domenii

def check_disponibilitate(sala, zi, interval):
    # Verifica daca sala este disponibila in ziua si intervalul specificat
    rezervari = sali[sala].get("rezervari", [])
    for rezervare in rezervari:
        if rezervare["zi"] == zi and rezervare["interval"] == interval:
            return False
    return True

def verifica_constrangere(valoare_x, valoare_y, constrangere):
    # Aplica constrangerea specifica intre doua valori
    if "!=" in constrangere:
        # Extragere partea stângă și dreaptă a expresiei
        camp, valoare = constrangere.split("!=")
        camp = camp.strip("x['").strip("']")
        valoare = valoare.strip("'")
        return valoare_x.get(camp) != valoare
    elif "==" in constrangere:
        camp, valoare = constrangere.split("==")
        camp = camp.strip("x['").strip("']")
        valoare = valoare.strip("'")
        return valoare_x.get(camp) == valoare
    # Adaugă alte tipuri de constrângeri dacă este necesar
    return False


def aplica_arc_consistency(domenii, constrangeri):
    queue = deque(constrangeri)
    while queue:
        element = queue.popleft()
        if len(element) != 3:
            print(f"Element invalid in coada: {element}")
            continue
        (x, _, constrangere) = element
        domeniu_actualizat = []
        for valoare_x in domenii.get(x, []):
            valid = eval(constrangere.format(x=valoare_x))
            if valid:
                domeniu_actualizat.append(valoare_x)
        if len(domeniu_actualizat) < len(domenii.get(x, [])):
            domenii[x] = domeniu_actualizat
    return domenii

# Initializare domenii
domenii = init_domenii(activitati, sali)

# Aplicare Arc Consistency
domenii_finale = aplica_arc_consistency(domenii, constrangeri)

# Afisare domenii dupa preprocesare intr-un format de orar structurat
print("\nDomenii dupa aplicarea Arc Consistency:\n")
data = []
for variabila, domeniu in domenii_finale.items():
    for item in domeniu:
        data.append({
            "Materie": variabila,
            "Sala": item["sala"],
            "Zi": item["zi"],
            "Interval": item["interval"]
        })

# Conversie in DataFrame pentru afisare tabelara
orar_df = pd.DataFrame(data)
orar_df = orar_df.sort_values(by=["Zi", "Interval", "Sala"])
print(orar_df.to_string(index=False))