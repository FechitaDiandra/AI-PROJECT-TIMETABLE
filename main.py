import re
import json

# Sinonime pentru zile
zile_sinonime = {
    "luni": ["lunea"],
    "marti": ["martia"],
    "miercuri": ["miercurea"],
    "joi": ["joia"],
    "vineri": ["vinerea"]
}

# Tokenizare fraza
def tokenize(fraza):
    return fraza.split()

# Extrage numele profesorului
def extrage_profesor(fraza):
    pattern = r"Profesorul\s+([A-Za-z]+\s+[A-Za-z]+)"
    match = re.search(pattern, fraza, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# Extrage zilele si orele, inclusiv inainte si dupa ora
def extrage_zile_ore(fraza):
    zile = []
    ora = None
    tip_constrangere = None  # Tipul constrangerii: "inainte de" sau "dupa"
    
    # Identificam zilele din fraza
    for zi, sinonime in zile_sinonime.items():
        for sinonim in sinonime + [zi]:
            if sinonim in fraza:
                zile.append(zi)

    # Identificam ora si tipul de constrangere
    ora_dupa_match = re.search(r"dupa ora (\d{1,2}):(\d{2})", fraza)
    ora_inainte_match = re.search(r"inainte de ora (\d{1,2}):(\d{2})", fraza)
    
    if ora_dupa_match:
        ora = f"{ora_dupa_match.group(1)}:{ora_dupa_match.group(2)}"
        tip_constrangere = "dupa"
    elif ora_inainte_match:
        ora = f"{ora_inainte_match.group(1)}:{ora_inainte_match.group(2)}"
        tip_constrangere = "inainte"

    return zile, ora, tip_constrangere

# Determina constrangerea generala
def determina_constrangere_generala(zile):
    if not zile:
        return "constrangerea se aplica pe toata saptamana"
    return zile

# Verifica daca profesorul nu poate preda
def verifica_constrangere_negativa(fraza, zile):
    # Cautam cuvintele cheie
    for zi in zile:
        # Cautam expresii care indica negarea predarii in ziua respectiva
        if re.search(rf"\bnu\b.*?\bpredea\b.*?\b{zi}\b", fraza) or re.search(rf"\bnu\b.*?\bvrea\b.*?\bpredea\b.*?\b{zi}\b", fraza):
            return False
        
        # Cautam formulări alternative
        if re.search(rf"\bnu\b.*?\bsă\b.*?\bpredea\b.*?\bdoar\b.*?\b{zi}\b", fraza):
            return False

    return True

# Actualizeaza disponibilitatea profesorului
def actualizeaza_disponibilitatea(profesor, ora_constrangere, zile_disponibile):
    # Citim datele existente din fisier JSON
    with open('profesori.json', 'r') as f:
        disponibilitate = json.load(f)

    # [Implementați logica de actualizare a disponibilității aici]
    
    # Salvăm datele actualizate în fișier JSON
    with open('profesori.json', 'w') as f:
        json.dump(disponibilitate, f, indent=4)

    print(f"Disponibilitatea profesorului {profesor} a fost actualizata.")

# Funcție pentru citirea fișierului JSON
def citire_fisier(nume_fisier):
    try:
        with open(nume_fisier, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Eroare: Fișierul '{nume_fisier}' nu a fost găsit.")
        exit(1)  # Oprește execuția scriptului

# Funcție pentru identificarea tipului de constrângere
def identifica_tip_constrangere(constrangere):
    tip_constrangere = {
        "hard": False,
        "soft": False,
        "locala": False,
        "globala": False
    }

    if constrangere.get("maxim_ore", None) == 0:
        tip_constrangere["hard"] = True
        tip_constrangere["locala"] = True
    else:
        tip_constrangere["soft"] = True
        tip_constrangere["locala"] = True
    
    if "interval_restrictiv" in constrangere and constrangere["interval_restrictiv"] == "14:00 - 16:00":
        tip_constrangere["globala"] = True

    return tip_constrangere

def aplica_constrangeri(profesori_data, constrangeri):
    profesori = profesori_data.get("profesori", [])
    for constrangere in constrangeri:
        nume_profesor = constrangere.get("profesor")
        zi_restrictiva = constrangere.get("zi_restrictiva")
        interval_restrictiv = constrangere.get("interval_restrictiv")
        
        tip_constrangere = identifica_tip_constrangere(constrangere)
        print(f"Tipul constrângerii pentru {nume_profesor}: {tip_constrangere}")

        for profesor in profesori:
            if profesor["nume"] == nume_profesor:
                if zi_restrictiva in profesor["disponibilitate"]:
                    print(f"Aplică constrângerea pentru {nume_profesor}: zi {zi_restrictiva}, interval {interval_restrictiv}")
                    
                    # Verificăm și ștergem intervalul din listă
                    if interval_restrictiv in profesor["disponibilitate"][zi_restrictiva]["intervale"]:
                        profesor["disponibilitate"][zi_restrictiva]["intervale"].remove(interval_restrictiv)
                        profesor["disponibilitate"][zi_restrictiva]["maxim_ore"] -= 1
                        print(f"Intervalul {interval_restrictiv} a fost șters pentru {nume_profesor} în ziua {zi_restrictiva}.")
                    else:
                        print(f"Intervalul {interval_restrictiv} nu se găsește în lista de intervale pentru {nume_profesor} în ziua {zi_restrictiva}.")
                else:
                    print(f"Ziua {zi_restrictiva} nu există în disponibilitatea lui {nume_profesor}.")

# Funcție pentru a obține constrângeri de la utilizator
def obtine_constrangeri_de_la_tastatura():
    constrangeri = []
    while True:
        fraza = input("Introduceti fraza: ")
        
        # Tokenizare si extragere informatii
        tokeni = tokenize(fraza)
        profesor = extrage_profesor(fraza)
        zile, ora, tip_constrangere = extrage_zile_ore(fraza)
        zile_constrangere = determina_constrangere_generala(zile)
        poate_preda = verifica_constrangere_negativa(fraza, zile)

        # Afisam rezultatele
        print("Profesor:", profesor)
        if isinstance(zile_constrangere, str):
            print(zile_constrangere)
        else:
            if tip_constrangere:
                print(f"Constrangere: {tip_constrangere} ora {ora}")
                print("Zile disponibile:", zile)
                print("Poate preda:", poate_preda)

                # Actualizam disponibilitatea pe baza constrangerilor
                if ora and zile:
                    actualizeaza_disponibilitatea(profesor, ora, zile)
            else:
                print("Nu a fost gasita o constrangere de timp specificata.")

        # Verificăm dacă utilizatorul dorește să continue
        if input("Doriti sa adaugati o alta constrangere? (da/nu): ").lower() != "da":
            break
    
    return constrangeri

# Meniu de opțiuni
optiune = input("Alegeți opțiunea: 1 - Citire din fișier, 2 - Introduceți constrângeri de la tastatură: ")

if optiune == "1":
    nume_fisier_profesori = input("Introduceți numele fișierului cu profesorii (ex: profesori.json): ")
    nume_fisier_constrangeri = input("Introduceți numele fișierului cu constrângerile (ex: constrangeri_prof.json): ")

    # Citirea fișierelor
    profesori_data = citire_fisier(nume_fisier_profesori)
    constrangeri = citire_fisier(nume_fisier_constrangeri)

elif optiune == "2":
    profesori_data = citire_fisier(input("Introduceți numele fișierului cu profesorii (ex: profesori.json): "))
    constrangeri = obtine_constrangeri_de_la_tastatura()

# Aplica constrangerile
aplica_constrangeri(profesori_data, constrangeri)
