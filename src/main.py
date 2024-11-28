import json

# functia pentru citirea fisierelor json
def citeste_fisier_json(fisier):
    try:
        with open(fisier, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Eroare la citirea fisierului {fisier}: {e}")
        return {}

# functia pentru salvarea constrangerilor in fisier
def salveaza_constrangeri(fisier, constrangeri):
    try:
        with open(fisier, 'w') as f:
            json.dump({"constrangeri": constrangeri}, f, indent=4)
        print(f"Constrangerile au fost salvate in {fisier}.")
    except Exception as e:
        print(f"Eroare la salvarea constrangerilor: {e}")

# functia pentru adaugarea constrangerilor de la prompt
def adauga_constrangeri_la_prompt(constrangeri):
    print("Introduceti constrangerile noi (lasati campurile goale pentru a opri):")
    while True:
        tip = input("Tip (hard/soft): ").strip().lower()
        if not tip:
            break
        nivel = input("Nivel (local/global): ").strip().lower()
        entitate = input("Entitate (profesor/sala/orar): ").strip().lower()
        nume = input("Nume entitate (optional): ").strip()
        zi = input("Zi (optional): ").strip()
        interval_orar = input("Interval orar (hh:mm-hh:mm): ").strip()
        detalii = input("Detalii (optional): ").strip()
        
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
        print("Constrangerea a fost adaugata.")
    return constrangeri

# functia pentru clasificarea constrangerilor in hard si soft
def clasifica_constrangeri(constrangeri):
    hard = [c for c in constrangeri if c["tip"] == "hard"]
    soft = [c for c in constrangeri if c["tip"] == "soft"]
    return hard, soft

# functia pentru verificarea suprapunerii intervalelor
def suprapunere_intervale(interval1, interval2):
    start1, end1 = map(lambda x: int(x.replace(':', '')), interval1.split('-'))
    start2, end2 = map(lambda x: int(x.replace(':', '')), interval2.split('-'))
    return not (end1 <= start2 or end2 <= start1)

# functia pentru verificarea salilor disponibile
def verifica_sali(sali, zi, interval, constrangeri_hard, constrangeri_soft):
    sali_disponibile = []
    for nume_sala, detalii in sali.items():
        disponibil = True  # presupunem ca sala este disponibila

        # verificam daca ziua este in lista de zile disponibile pentru sala
        if zi.lower() not in map(str.lower, detalii["disponibilitate"]["zile"]):
            disponibil = False

        # verificam daca intervalul este in lista de intervale disponibile pentru sala
        elif interval not in detalii["disponibilitate"]["intervale"]:
            disponibil = False

        # aplicam constrangerile hard si soft pentru sala
        for constr in constrangeri_hard + constrangeri_soft:
            if constr["entitate"] == "sala" and constr.get("nume") == nume_sala:
                if (constr.get("zi") is None or zi.lower() == constr.get("zi", "").lower()) and suprapunere_intervale(interval, constr["interval_orar"]):
                    if constr["tip"] == "hard":
                        disponibil = False
                    elif constr["tip"] == "soft":
                        # preferintele soft nu schimba disponibilitatea, doar emit avertismente
                        pass

        # adaugam sala in lista disponibila daca nu exista restrictii
        if disponibil:
            sali_disponibile.append(nume_sala)

    return sali_disponibile

def safe_str_lower(value):
    return value.strip().lower() if value else ''

def aplica_constrangeri(hard, soft, zi, interval, profesor=None, sala=None):
    mesaj_final = []
    disponibil = True

    # aplica constrangerile hard
    for constr in hard:
        if constr["nivel"].lower() == "local":
            # verificam restrictiile pentru profesori
            if constr["entitate"].lower() == "profesor" and profesor:
                if (safe_str_lower(profesor) == safe_str_lower(constr.get("nume")) and
                        (constr.get("zi") is None or safe_str_lower(zi) == safe_str_lower(constr.get("zi"))) and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[HARD] Profesorul {profesor} este indisponibil in intervalul {interval} pe {zi}.")
                    disponibil = False
                    break  # oprire daca o regula hard este incalcata

            # verificam restrictiile pentru sali
            if constr["entitate"].lower() == "sala" and sala:
                if (safe_str_lower(sala) == safe_str_lower(constr.get("nume")) and
                        (constr.get("zi") is None or safe_str_lower(zi) == safe_str_lower(constr.get("zi"))) and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[HARD] Sala {sala} este rezervata pe {zi} in intervalul {interval}.")
                    disponibil = False
                    break  # oprire daca o regula hard este incalcata

        elif constr["nivel"].lower() == "global":
            if suprapunere_intervale(interval, constr["interval_orar"]):
                mesaj_final.append(f"[HARD] Intervalul {interval} este global indisponibil pe {zi}.")
                disponibil = False
                break  # oprire daca o regula hard este incalcata

    # daca exista constrangeri hard care invalideaza, iesim direct
    if not disponibil:
        return disponibil, mesaj_final

    # aplica constrangerile soft (doar daca nu exista conflicte hard)
    for constr in soft:
        if constr["nivel"].lower() == "local":
            # preferinte pentru profesori
            if constr["entitate"].lower() == "profesor" and profesor:
                if (safe_str_lower(profesor) == safe_str_lower(constr.get("nume")) and
                        (constr.get("zi") is None or safe_str_lower(zi) == safe_str_lower(constr.get("zi"))) and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[SOFT] Avertisment: {profesor} prefera sa nu aiba cursuri in intervalul {interval} pe {zi}.")

            # preferinte pentru sali
            if constr["entitate"].lower() == "sala" and sala:
                if (safe_str_lower(sala) == safe_str_lower(constr.get("nume")) and
                        (constr.get("zi") is None or safe_str_lower(zi) == safe_str_lower(constr.get("zi"))) and
                        suprapunere_intervale(interval, constr["interval_orar"])):
                    mesaj_final.append(f"[SOFT] Avertisment: Sala {sala} prefera sa nu fie utilizata in intervalul {interval}.")

        elif constr["nivel"].lower() == "global":
            if suprapunere_intervale(interval, constr["interval_orar"]):
                mesaj_final.append(f"[SOFT] Preferinta globala: Evita cursuri in intervalul {interval} pe {zi}.")

    return disponibil, list(set(mesaj_final))  # eliminam duplicatele

# citire date
fisier_constrangeri = 'constrains/constrangeri.json'
fisier_sali = 'data/sali.json'
fisier_profesori = 'data/profesori.json'

# citire date pentru constrangeri
optiune_constrangeri = input("Doriti sa cititi constrangerile dintr-un fisier sau sa le introduceti manual? (fisier/prompt): ").strip().lower()
if optiune_constrangeri == "fisier":
    constrangeri_actualizate = citeste_fisier_json(fisier_constrangeri).get("constrangeri", [])
elif optiune_constrangeri == "prompt":
    constrangeri_existente = citeste_fisier_json(fisier_constrangeri).get("constrangeri", [])
    constrangeri_actualizate = adauga_constrangeri_la_prompt(constrangeri_existente)
    salveaza_constrangeri(fisier_constrangeri, constrangeri_actualizate)
else:
    print("Optiune invalida. Se vor folosi constrangerile existente din fisier.")
    constrangeri_actualizate = citeste_fisier_json(fisier_constrangeri).get("constrangeri", [])

sali = citeste_fisier_json(fisier_sali)
profesori = citeste_fisier_json(fisier_profesori)

# clasificarea constrangerilor
hard, soft = clasifica_constrangeri(constrangeri_actualizate)

# verificarea constrangerilor
zile = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]

for profesor_key, profesor_data in profesori.items():
    profesor_nume = profesor_data["nume"]
    print(f"\n=== Verificari pentru {profesor_nume} ===")
    for zi in zile:
        print(f"\n-- Ziua {zi} --")
        for interval in intervale:
            sali_disponibile = verifica_sali(sali, zi, interval, hard, soft)
            sala = sali_disponibile[0] if sali_disponibile else None
            disponibil, mesaje = aplica_constrangeri(hard, soft, zi, interval, profesor_nume, sala)

            if disponibil:
                print(f"[DISPONIBIL] Interval {interval} pe {zi} este disponibil pentru {profesor_nume} in sala {sala if sala else 'Nicio sala'}.")
                for mesaj in mesaje:
                    print(f"  - {mesaj}")
            else:
                print(f"[INDISPONIBIL] Interval {interval} pe {zi} este indisponibil pentru {profesor_nume} in sala {sala if sala else 'Nicio sala'}:")
                for mesaj in mesaje:
                    print(f"  - {mesaj}")