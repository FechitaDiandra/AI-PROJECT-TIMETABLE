import json

# Funcția pentru citirea fișierelor JSON
def citeste_fisier_json(fisier):
    try:
        with open(fisier, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Eroare la citirea fișierului {fisier}: {e}")
        return {}

# Funcția pentru salvarea constrângerilor în fișier
def salveaza_constrangeri(fisier, constrangeri):
    try:
        with open(fisier, 'w') as f:
            json.dump({"constrangeri": constrangeri}, f, indent=4)
        print(f"Constrângerile au fost salvate în {fisier}.")
    except Exception as e:
        print(f"Eroare la salvarea constrângerilor: {e}")

# Funcția pentru adăugarea constrângerilor de la prompt
def adauga_constrangeri_la_prompt(constrangeri):
    print("Introduceți constrângerile noi (lăsați câmpurile goale pentru a opri):")
    while True:
        tip = input("Tip (hard/soft): ").strip().lower()
        if not tip:
            break
        nivel = input("Nivel (local/global): ").strip().lower()
        entitate = input("Entitate (profesor/sala/orar): ").strip().lower()
        nume = input("Nume entitate (opțional): ").strip()
        zi = input("Zi (opțional): ").strip()
        interval_orar = input("Interval orar (hh:mm-hh:mm): ").strip()
        detalii = input("Detalii (opțional): ").strip()
        
        constrangere = {
            "tip": tip,
            "nivel": nivel,
            "entitate": entitate,
            "nume": nume if nume else None,
            "zi": zi if zi else None,
            "interval_orar": interval_orar,
            "detalii": detalii if detalii else None
        }
        constrangeri.append(constrangere)
        print("Constrângerea a fost adăugată.")
    return constrangeri

# Funcția pentru clasificarea constrângerilor în hard și soft
def clasifica_constrangeri(constrangeri):
    hard = [c for c in constrangeri if c["tip"] == "hard"]
    soft = [c for c in constrangeri if c["tip"] == "soft"]
    return hard, soft

# Funcția pentru verificarea suprapunerii intervalelor
def suprapunere_intervale(interval1, interval2):
    start1, end1 = map(lambda x: int(x.replace(':', '')), interval1.split('-'))
    start2, end2 = map(lambda x: int(x.replace(':', '')), interval2.split('-'))
    return not (end1 <= start2 or end2 <= start1)

# Funcția pentru verificarea sălilor disponibile
def verifica_sali(sali, zi, interval, constrangeri_hard, constrangeri_soft):
    sali_disponibile = []
    for nume_sala, detalii in sali.items():
        disponibil = True  # Presupunem că sala este disponibilă

        # Verificăm dacă ziua este în lista de zile disponibile pentru sală
        if zi.lower() not in map(str.lower, detalii["disponibilitate"]["zile"]):
            disponibil = False

        # Verificăm dacă intervalul este în lista de intervale disponibile pentru sală
        elif interval not in detalii["disponibilitate"]["intervale"]:
            disponibil = False

        # Aplicăm constrângerile hard și soft pentru sală
        for constr in constrangeri_hard + constrangeri_soft:
            if constr["entitate"] == "sala" and constr["nume"] == nume_sala:
                if zi.lower() == constr.get("zi", "").lower() and suprapunere_intervale(interval, constr["interval_orar"]):
                    if constr["tip"] == "hard":
                        disponibil = False
                    elif constr["tip"] == "soft":
                        # Preferințele soft nu schimbă disponibilitatea, doar emit avertismente
                        pass

        # Adăugăm sala în lista disponibilă dacă nu există restricții
        if disponibil:
            sali_disponibile.append(nume_sala)

    return sali_disponibile


def aplica_constrangeri(hard, soft, zi, interval, profesor=None, sala=None):
    mesaj_final = []
    disponibil = True

    # Aplica constrângerile hard
    for constr in hard:
        if constr["nivel"].lower() == "local":
            # Verificăm restricțiile pentru profesori
            if constr["entitate"].lower() == "profesor" and profesor:
                if (profesor.strip().lower() == constr["nume"].strip().lower() and
                        zi.strip().lower() == constr["zi"].strip().lower() and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[HARD] Profesorul {profesor} este indisponibil în intervalul {interval} pe {zi}.")
                    disponibil = False
                    break  # Stop further checks if a hard rule is violated

            # Verificăm restricțiile pentru săli
            if constr["entitate"].lower() == "sala" and sala:
                if (sala.strip().lower() == constr["nume"].strip().lower() and
                        zi.strip().lower() == constr["zi"].strip().lower() and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[HARD] Sala {sala} este rezervată pe {zi} în intervalul {interval}.")
                    disponibil = False
                    break  # Stop further checks if a hard rule is violated

        elif constr["nivel"].lower() == "global":
            if suprapunere_intervale(interval, constr["interval_orar"]):
                mesaj_final.append(f"[HARD] Intervalul {interval} este global indisponibil pe {zi}.")
                disponibil = False
                break  # Stop further checks if a hard rule is violated

    # Dacă există constrângeri hard care invalidează, ieșim direct
    if not disponibil:
        return disponibil, mesaj_final

    # Aplica constrângerile soft (doar dacă nu există conflicte hard)
    for constr in soft:
        if constr["nivel"].lower() == "local":
            # Preferințe pentru profesori
            if constr["entitate"].lower() == "profesor" and profesor:
                if (profesor.strip().lower() == constr["nume"].strip().lower() and
                        zi.strip().lower() == constr["zi"].strip().lower() and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[SOFT] Avertisment: {profesor} preferă să nu aibă cursuri în intervalul {interval} pe {zi}.")

            # Preferințe pentru săli
            if constr["entitate"].lower() == "sala" and sala:
                if (sala.strip().lower() == constr["nume"].strip().lower() and
                        zi.strip().lower() == constr["zi"].strip().lower() and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[SOFT] Avertisment: Sala {sala} preferă să nu fie utilizată în intervalul {interval}.")

        elif constr["nivel"].lower() == "global":
            if suprapunere_intervale(interval, constr["interval_orar"]):
                mesaj_final.append(f"[SOFT] Preferință globală: Evită cursuri în intervalul {interval} pe {zi}.")

    return disponibil, list(set(mesaj_final))  # Eliminăm duplicatele

    # Aplica constrângerile soft
    for constr in soft:
        if constr["nivel"] == "local":
            # Preferințe pentru profesori
            if constr["entitate"] == "profesor" and profesor:
                if (profesor.lower() == constr["nume"].lower() and
                        zi.lower() == constr["zi"].lower() and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[SOFT] Avertisment: {profesor} preferă să nu aibă cursuri în intervalul {interval} pe {zi}.")

            # Preferințe pentru săli
            if constr["entitate"] == "sala" and sala:
                if (sala.lower() == constr["nume"].lower() and
                        zi.lower() == constr["zi"].lower() and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[SOFT] Avertisment: Sala {sala} preferă să nu fie utilizată în intervalul {interval}.")

        elif constr["nivel"] == "global":
            if suprapunere_intervale(interval, constr["interval_orar"]):
                mesaj_final.append(f"[SOFT] Preferință globală: Evită cursuri în intervalul {interval} pe {zi}.")

    # Returnăm disponibilitatea și mesajele
    return disponibil, list(set(mesaj_final))  # Eliminăm duplicatele


# Citire date
fisier_constrangeri = '/Users/diandrafechita/AI-PROJECT-TIMETABLE/constrains/constrangeri.json'
fisier_sali = '/Users/diandrafechita/AI-PROJECT-TIMETABLE/data/sali.json'
fisier_profesori = '/Users/diandrafechita/AI-PROJECT-TIMETABLE/data/profesori.json'

# Citire date pentru constrângeri
optiune_constrangeri = input("Doriți să citiți constrângerile dintr-un fișier sau să le introduceți manual? (fisier/prompt): ").strip().lower()
if optiune_constrangeri == "fisier":
    constrangeri_actualizate = citeste_fisier_json(fisier_constrangeri).get("constrangeri", [])
elif optiune_constrangeri == "prompt":
    constrangeri_existente = citeste_fisier_json(fisier_constrangeri).get("constrangeri", [])
    constrangeri_actualizate = adauga_constrangeri_la_prompt(constrangeri_existente)
    salveaza_constrangeri(fisier_constrangeri, constrangeri_actualizate)
else:
    print("Opțiune invalidă. Se vor folosi constrângerile existente din fișier.")
    constrangeri_actualizate = citeste_fisier_json(fisier_constrangeri).get("constrangeri", [])


sali = citeste_fisier_json(fisier_sali)
profesori = citeste_fisier_json(fisier_profesori)

# Clasificarea constrângerilor
hard, soft = clasifica_constrangeri(constrangeri_actualizate)

# Verificarea constrângerilor
zile = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]

for profesor_key, profesor_data in profesori.items():
    profesor_nume = profesor_data["nume"]
    print(f"\n=== Verificări pentru {profesor_nume} ===")
    for zi in zile:
        print(f"\n-- Ziua {zi} --")
        for interval in intervale:
            sali_disponibile = verifica_sali(sali, zi, interval, hard, soft)
            sala = sali_disponibile[0] if sali_disponibile else None
            disponibil, mesaje = aplica_constrangeri(hard, soft, zi, interval, profesor_nume, sala)

            if disponibil:
                print(f"[DISPONIBIL] Interval {interval} pe {zi} este disponibil pentru {profesor_nume} în sala {sala if sala else 'Nicio sală'}.")
                for mesaj in mesaje:
                    print(f"  - {mesaj}")
            else:
                print(f"[INDISPONIBIL] Interval {interval} pe {zi} este indisponibil pentru {profesor_nume} în sala {sala if sala else 'Nicio sală'}:")
                for mesaj in mesaje:
                    print(f"  - {mesaj}")
