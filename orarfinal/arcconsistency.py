import json
from collections import deque

zile = ["luni", "marti", "miercuri", "joi", "vineri"]
intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]

with open('data/activitati.json') as f:
    activitati = json.load(f)

with open('data/sali.json') as f:
    sali = json.load(f)

with open('data/profesori.json') as f:
    profesori = json.load(f)

with open('constrains/constrangeri.json') as f:
    constrangeri = json.load(f).get("constrangeri", [])

constrangeri_aplicate = set()

def init_domenii(activitati, sali):
    domenii = {}
    for activitate in activitati:
        domenii[activitate["materie"]] = [
            {"sala": sala, "zi": zi, "interval": interval}
            for sala in sali
            for zi in zile
            for interval in intervale
            if check_disponibilitate(sali[sala], zi, interval)
        ]
    return domenii

def check_disponibilitate(sala, zi, interval):
    return True

def verifica_constrangere(valoare_x, constrangere, activitate):
    entitate = constrangere["entitate"].lower()
    zi = constrangere.get("zi", "").lower().strip() if constrangere.get("zi") else ""
    interval_orar = constrangere.get("interval_orar", "").strip()
    tip_constrangere = constrangere["tip"]
    detalii_constrangere = constrangere.get("detalii", "Fără detalii")

    if entitate == "sala":
        if valoare_x["sala"].lower().strip() == constrangere.get("nume", "").lower().strip():
            if (not zi or zi == valoare_x["zi"].lower().strip()) and (not interval_orar or interval_orar == valoare_x["interval"]):
                constrangeri_aplicate.add((tip_constrangere, f"{detalii_constrangere} (activitate: {activitate}, sala: {valoare_x['sala']}, zi: {valoare_x['zi']}, interval: {valoare_x['interval']})"))
                return tip_constrangere != "hard"

    elif entitate == "orar":
        if interval_orar == valoare_x["interval"].strip():
            constrangeri_aplicate.add((tip_constrangere, f"{detalii_constrangere} (activitate: {activitate}, interval: {valoare_x['interval']}, zi: {valoare_x['zi']})"))
            return tip_constrangere != "hard"

    elif entitate == "profesor":
        profesor = valoare_x.get("profesor", "").lower().strip()
        nume_profesor = constrangere.get("nume", "").lower().strip()
        if profesor == nume_profesor:
            if (not zi or zi == valoare_x["zi"].lower().strip()) and (not interval_orar or interval_orar == valoare_x["interval"]):
                constrangeri_aplicate.add((tip_constrangere, f"{detalii_constrangere} (activitate: {activitate}, profesor: {profesor}, zi: {valoare_x['zi']}, interval: {valoare_x['interval']})"))
                return tip_constrangere != "hard"

    return True

def restrange_domeniu(x, domenii, constrangeri):
    valori_de_retinut = []
    for valoare_x in domenii[x]:
        valid = True
        for constrangere in constrangeri:
            if not verifica_constrangere(valoare_x, constrangere, x):
                valid = False
                break
        if valid:
            valori_de_retinut.append(valoare_x)
        else:
            constrangeri_aplicate.add(("hard", f"Valoarea {valoare_x} eliminată pentru activitatea '{x}' din cauza constrângerii {constrangere}."))

    if not valori_de_retinut:
        print(f"Eroare: Domeniul activității '{x}' a devenit gol după aplicarea constrângerilor.")
        print("Constrângeri aplicate:")
        for constrangere in constrangeri:
            print(constrangere)
        raise ValueError(f"Domeniu gol pentru activitatea '{x}'. Verificați constrângerile.")

    domenii[x] = valori_de_retinut
    return len(valori_de_retinut) < len(domenii[x])

def aplica_arc_consistency(domenii, constrangeri):
    queue = deque(domenii.keys())
    while queue:
        x = queue.popleft()
        try:
            if restrange_domeniu(x, domenii, constrangeri):
                queue.extend([y for y in domenii if y != x])
        except ValueError as e:
            print(e)
            return None 
    return domenii



domenii = init_domenii(activitati, sali)

print("Domenii inițiale:")
domenii_initiale = {}
for activitate, domeniu in domenii.items():
    domenii_initiale[activitate] = len(domeniu)
    print(f"{activitate}: {len(domeniu)} opțiuni")

domenii_finale = aplica_arc_consistency(domenii, constrangeri)

if domenii_finale:
    print("\nDomenii finale după aplica_arc_consistency:")
    for activitate, domeniu in domenii_finale.items():
        numar_initial = domenii_initiale[activitate]
        numar_final = len(domeniu)
        print(f"{activitate}: {numar_final} opțiuni (inițial: {numar_initial}, diferență: {numar_initial - numar_final})")
        for optiune in domeniu:
            print(f"  sala: {optiune['sala']}, zi: {optiune['zi']}, interval: {optiune['interval']}")
else:
    print("\nProces oprit din cauza domeniilor goale.")

print("\nConstrângeri aplicate:")
for tip, detalii in constrangeri_aplicate:
    print(f"Tip: {tip}, Detalii: {detalii}")
