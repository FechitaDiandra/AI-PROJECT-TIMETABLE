import re
import json

# sinonime pentru zile
zile_sinonime = {
    "luni": ["lunea"],
    "marti": ["martia"],
    "miercuri": ["miercurea"],
    "joi": ["joia"],
    "vineri": ["vinerea"]
}

# tokenizez fraza
def tokenize(fraza):
    return fraza.split()

# extrag numele profesorului
def extrage_profesor(fraza):
    pattern = r"Profesorul\s+([A-Za-z]+\s+[A-Za-z]+)"
    match = re.search(pattern, fraza, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# extrag zilele si orele, inclusiv inainte si dupa ora
def extrage_zile_ore(fraza):
    zile = []
    ora = None
    tip_constrangere = None  # tipul constrangerii: "inainte de" sau "dupa"
    
    # identific zilele din fraza
    for zi, sinonime in zile_sinonime.items():
        for sinonim in sinonime + [zi]:
            if sinonim in fraza:
                zile.append(zi)

    # verific expresia "in ziua de"
    match_in_ziua_de = re.search(r"in ziua de\s+([A-Za-z]+)", fraza, re.IGNORECASE)
    if match_in_ziua_de:
        zi = match_in_ziua_de.group(1).lower()
        if zi in zile_sinonime:
            zile = [zi]  # setez zilele ca fiind doar acea zi

            # verific daca nu este specificata o ora
            ora_dupa_match = re.search(r"dupa ora (\d{1,2}):(\d{2})", fraza)
            ora_inainte_match = re.search(r"inainte de ora (\d{1,2}):(\d{2})", fraza)
            
            if not ora_dupa_match and not ora_inainte_match:
                # daca nu este specificata o ora, setez tipul de constrangere
                tip_constrangere = "toata ziua"

    # identific ora si tipul de constrangere
    ora_dupa_match = re.search(r"dupa ora (\d{1,2}):(\d{2})", fraza)
    ora_inainte_match = re.search(r"inainte de ora (\d{1,2}):(\d{2})", fraza)
    
    if ora_dupa_match:
        ora = f"{ora_dupa_match.group(1)}:{ora_dupa_match.group(2)}"
        tip_constrangere = "dupa"
    elif ora_inainte_match:
        ora = f"{ora_inainte_match.group(1)}:{ora_inainte_match.group(2)}"
        tip_constrangere = "inainte"

    return zile, ora, tip_constrangere

# determin constrangerea generala
def determina_constrangere_generala(zile):
    if not zile:
        return "constrangerea se aplica pe toata saptamana"
    return zile

# verific daca profesorul nu poate preda
def verifica_constrangere_negativa(fraza, zile):
    # caut cuvintele cheie
    for zi in zile:
        # caut expresii care indica negarea predarii in ziua respectiva
        if re.search(rf"\bnu\b.*?\bpredea\b.*?\b{zi}\b", fraza) or re.search(rf"\bnu\b.*?\bvrea\b.*?\bpredea\b.*?\b{zi}\b", fraza):
            return False
        
        # caut formulări alternative
        if re.search(rf"\bnu\b.*?\bsă\b.*?\bpredea\b.*?\bdoar\b.*?\b{zi}\b", fraza):
            return False

    return True

# afisez meniul
def afiseaza_meniu():
    print("1. Citire din fisier")
    print("2. Citire de la tastatura")
    print("3. Iesire")
    return input("Alege o optiune: ")

# functie principala
def main():
    while True:
        optiune = afiseaza_meniu()
        
        if optiune == '1':
            # citire din fisier
            try:
                with open('constrangeri_profesori.json', 'r') as f:
                    profesor_data = json.load(f)  # incarc datele din fisier

                # verific tip de date
                if isinstance(profesor_data, list):  # verific daca datele sunt o lista
                    for profesor in profesor_data:
                        # ma asigur ca fiecare element este un dictionar
                        if isinstance(profesor, dict):
                            print(f"Profesor: {profesor['profesor']}, Zi: {profesor['zi']}, Interval: {profesor['interval']}, Preferinta: {profesor['preferinta']}")
                        else:
                            print("elementul nu este un dictionar:", profesor)
                else:
                    print("datele nu sunt intr-un format corect. Se asteapta o lista.")

            except json.JSONDecodeError as e:
                print(f"eroare la decodarea JSON: {e}")
            except FileNotFoundError:
                print("fisierul nu a fost gasit.")

        elif optiune == '2':
            # citire de la tastatura
            fraza = input("Introduceti fraza: ")

            # tokenizare si extragere informatii
            tokeni = tokenize(fraza)
            profesor = extrage_profesor(fraza)
            zile, ora, tip_constrangere = extrage_zile_ore(fraza)
            zile_constrangere = determina_constrangere_generala(zile)
            poate_preda = verifica_constrangere_negativa(fraza, zile)

            # afisez rezultatele
            print("Profesor:", profesor)
            if isinstance(zile_constrangere, str):
                print(zile_constrangere)
            else:
                if tip_constrangere:
                    if tip_constrangere == "toata ziua":
                        print(f"Constrangere: se aplica toata ziua")
                    else:
                        print(f"Constrangere: {tip_constrangere} ora {ora}")
                    print("Zile disponibile:", zile)
                    print("Poate preda:", poate_preda)
                else:
                    print("Nu a fost gasita o constrangere de timp specificata.")

        elif optiune == '3':
            # ies din bucla
            print("Ies din program.")
            break

        else:
            print("Optiune invalida. Te rog sa alegi 1, 2 sau 3.")

# apelarea functiei principale
if __name__ == "__main__":
    main()
