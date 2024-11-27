import json
import random
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas

def incarca_date(fisier):
    with open(fisier, 'r') as f:
        return json.load(f)

def alege_profesor(materie, profesori):
    profesori_pentru_materie = [k for k, v in profesori.items() if materie in v["materii"]]
    if profesori_pentru_materie:
        return random.choice(profesori_pentru_materie)
    raise KeyError(f"Nu exista profesori pentru materia '{materie}' in profesori.json.")

def genereaza_orar(activitati, grupe, sali, profesori, semestru):
    print(f"Generam orarul pentru semestrul {semestru}...")
    orar = {}
    ocupare_sali = {sala: {} for sala in sali.keys()}
    ocupare_grupe = {grupa: {} for grupa in grupe}
    ocupare_an = {an: {} for an in range(1, 4)}
    zile = ["luni", "marti", "miercuri", "joi", "vineri"]
    intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]

    sali_chei = sorted(sali.keys(), key=lambda x: sali[x]["capacitate"], reverse=True)

    grupe_pe_an_litera = {}
    for grupa in grupe:
        an, litera = int(grupa[0]), grupa[1]
        if (an, litera) not in grupe_pe_an_litera:
            grupe_pe_an_litera[(an, litera)] = []
        grupe_pe_an_litera[(an, litera)].append(grupa)

    for (an, litera), grupele in grupe_pe_an_litera.items():
        activitati_an = [a for a in activitati if a["an"] == an and a["semestru"] == semestru]

        # Alocare cursuri
        for activitate in activitati_an:
            if activitate["tip"] == "curs":
                profesor_cheie = alege_profesor(activitate["materie"], profesori)
                profesor_nume = profesori[profesor_cheie]["nume"]

                alocat = False
                for zi in zile:
                    for interval in intervale:
                        if (zi, interval) in ocupare_an[an]:
                            continue

                        for sala_id in sali_chei:
                            sala = sali[sala_id]
                            if sala["capacitate"] >= len(grupele) and interval not in ocupare_sali[sala_id].get(zi, []):
                                ocupare_sali[sala_id].setdefault(zi, []).append(interval)
                                ocupare_an[an][(zi, interval)] = True
                                for grupa in grupele:
                                    ocupare_grupe[grupa][(zi, interval)] = True

                                orar[f"{activitate['materie']}_{an}_{litera}_curs"] = {
                                    "materie": activitate["materie"],
                                    "tip": "curs",
                                    "zi": zi,
                                    "interval": interval,
                                    "sala": sala_id,
                                    "profesor": profesor_nume,
                                    "grupele": grupele
                                }
                                print(f"Curs alocat: {activitate['materie']} pentru {grupele} (an {an}, litera {litera}) in sala {sala_id}, {zi}, {interval}")
                                alocat = True
                                break
                        if alocat:
                            break
                    if alocat:
                        break

        # Alocare laboratoare
        for grupa in grupele:
            orar_grupa = []
            for activitate in activitati_an:
                if activitate["tip"] == "laborator":
                    profesor_cheie = alege_profesor(activitate["materie"], profesori)
                    profesor_nume = profesori[profesor_cheie]["nume"]

                    alocat = False
                    for zi in zile:
                        for interval in intervale:
                            if (zi, interval) in ocupare_grupe[grupa]:
                                continue

                            for sala_id in sali_chei:
                                sala = sali[sala_id]
                                if sala["capacitate"] >= 1 and interval not in ocupare_sali[sala_id].get(zi, []):
                                    ocupare_sali[sala_id].setdefault(zi, []).append(interval)
                                    ocupare_grupe[grupa][(zi, interval)] = True

                                    orar_grupa.append({
                                        "materie": activitate["materie"],
                                        "tip": "laborator",
                                        "zi": zi,
                                        "interval": interval,
                                        "sala": sala_id,
                                        "profesor": profesor_nume
                                    })
                                    print(f"Laborator alocat: {activitate['materie']} pentru grupa {grupa} in sala {sala_id}, {zi}, {interval}")
                                    alocat = True
                                    break
                            if alocat:
                                break
                        if alocat:
                            break

                    if not alocat:
                        print(f"Nu s-a putut aloca laboratorul: {activitate['materie']} pentru grupa {grupa}")

            orar[grupa] = orar_grupa

    return orar
#def salveaza_orar_in_pdf(orar, fisier_pdf):
    c = canvas.Canvas(fisier_pdf, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    y = 750  # Înălțimea paginii
    c.drawString(100, y, "Orar Generat")
    y -= 20

    for semestru, orar_semestru in orar.items():
        c.drawString(100, y, f"Semestru: {semestru}")
        y -= 20
        for grupa, activitati in orar_semestru.items():
            c.drawString(120, y, f"Grupa: {grupa}")
            y -= 20
            for activitate in activitati:
                if isinstance(activitate, dict):  # Verificăm structura activității
                    # Gestionăm cursuri și laboratoare
                    if all(k in activitate for k in ["materie", "tip", "zi", "interval", "sala", "profesor"]):
                        c.drawString(140, y, f"{activitate['materie']} ({activitate['tip']}) - {activitate['zi']} {activitate['interval']}, Sala: {activitate['sala']}, Profesor: {activitate['profesor']}")
                        y -= 20
                        if y < 50:  # Dacă ajungem la capătul paginii
                            c.showPage()
                            y = 750
                            c.setFont("Helvetica", 12)
                    else:
                        c.drawString(140, y, f"Activitate necunoscută: {activitate}")
                        y -= 20
                        if y < 50:
                            c.showPage()
                            y = 750
                            c.setFont("Helvetica", 12)

    c.save()
    print(f"PDF salvat în: {fisier_pdf}")
def afiseaza_profesori(profesori, orar):
    detalii_profesori = {profesor: {"nume": detalii["nume"], "activitati": []} for profesor, detalii in profesori.items()}
    
    # Iterăm prin orar pentru a colecta activitățile fiecărui profesor
    for semestru, orar_semestru in orar.items():
        for activitate, detalii in orar_semestru.items():
            if isinstance(detalii, list):  # Este vorba de laboratoare
                for laborator in detalii:
                    for profesor in profesori.keys():
                        if laborator["profesor"] == profesori[profesor]["nume"]:
                            detalii_profesori[profesor]["activitati"].append({
                                "materie": laborator["materie"],
                                "tip": laborator["tip"],
                                "zi": laborator["zi"],
                                "interval": laborator["interval"],
                                "sala": laborator["sala"],
                            })
            else:  # Este vorba de cursuri
                for profesor in profesori.keys():
                    if detalii["profesor"] == profesori[profesor]["nume"]:
                        detalii_profesori[profesor]["activitati"].append({
                            "materie": detalii["materie"],
                            "tip": detalii["tip"],
                            "zi": detalii["zi"],
                            "interval": detalii["interval"],
                            "sala": detalii["sala"],
                            "grupele": detalii["grupele"]
                        })

    # Afișăm informațiile despre profesori
    print("\nDetalii profesori:")
    for profesor, detalii in detalii_profesori.items():
        print(f"\nProfesor: {detalii['nume']}")
        if detalii["activitati"]:
            for activitate in detalii["activitati"]:
                print(f"  - {activitate['tip']} la {activitate['materie']} în sala {activitate['sala']}, {activitate['zi']} {activitate['interval']}")
        else:
            print("  - Fără activități alocate.")
def salveaza_orar(orar, fisier):
    with open(fisier, 'w') as f:
        json.dump(orar, f, indent=4)

if __name__ == "__main__":
    activitati = incarca_date("data/activitati.json")
    grupe = incarca_date("data/grupe.json")
    sali = incarca_date("data/sali.json")
    profesori = incarca_date("data/profesori.json")

    orar_final = {}
    for semestru in [1, 2]:
        orar_semestru = genereaza_orar(activitati, grupe, sali, profesori, semestru)
        orar_final[f"semestru_{semestru}"] = orar_semestru

    salveaza_orar(orar_final, "orar_generat.json")
    print("Orarul a fost generat si salvat in orar_generat.json.")
    # salveaza_orar_in_pdf(orar_final, "orar_generat.pdf")
    afiseaza_profesori(profesori, orar_final)
