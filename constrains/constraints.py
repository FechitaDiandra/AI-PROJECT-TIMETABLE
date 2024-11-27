
def unicitate_activitati(orar):
    for activitate1, detalii1 in orar.items():
        for activitate2, detalii2 in orar.items():
            if activitate1 != activitate2 and detalii1 == detalii2:
                return False  # Incalcare unicitate
    return True  # Respectam unicitatea


def ordine_cursuri_seminare(orar, activitati):
    for activitate, detalii in activitati.items():
        if detalii["tip"] == "curs":
            for activitate2, detalii2 in activitati.items():
                if detalii2["tip"] in ["seminar", "laborator"]:
                    if orar[activitate][1] > orar[activitate2][1]:  # Comparam intervalele
                        return False  # Incalcare ordine
    return True  # Respectam ordinea


def limite_zilnice_profesori(orar, profesori, zile, activitati, max_activitati_pe_zi=3):
    activitati_per_zile = {zi: {profesor: 0 for profesor in profesori} for zi in zile}
    for activitate, detalii in orar.items():
        zi, interval, sala = detalii
        profesor = activitati[activitate]["profesor"]
        activitati_per_zile[zi][profesor] += 1
    for zi in activitati_per_zile.values():
        for profesor, numar_activitati in zi.items():
            if numar_activitati > max_activitati_pe_zi:
                return False  # Incalcare limita de activitati pe zi
    return True  # Limita este respectata

def intervale_interzise_profesori(orar, profesori, activitati, hard):
    for activitate, detalii in orar.items():
        zi, interval, sala = detalii
        profesor = activitati[activitate]["profesor"]
        for constr in hard:
            if constr.get("nivel") == "local" and constr.get("entitate") == "profesor":
                if (
                    profesor == constr.get("nume") and
                    zi == constr.get("zi") and
                    interval == constr.get("interval_orar")
                ):
                    return False  # Interval interzis
    return True  # Intervalele sunt respectate

def verifica_constrangere_arc(constrangere, activitate, valoare):
    if constrangere["entitate"] == "profesor":
        if activitate["profesor"] == constrangere.get("nume"):
            if constrangere.get("zi") and constrangere.get("interval_orar"):
                zi_restrictionata = constrangere["zi"]
                interval_orar = constrangere["interval_orar"].split("-")
                ora_inceput = int(interval_orar[0].split(":")[0])
                ora_sfarsit = int(interval_orar[1].split(":")[0])

                return not (valoare["zi"] == zi_restrictionata and 
                            ora_inceput <= valoare["interval"] <= ora_sfarsit)

    if constrangere["entitate"] == "sala":
        if valoare["sala"] == constrangere.get("nume"):
            if constrangere.get("zi") and constrangere.get("interval_orar"):
                zi_restrictionata = constrangere["zi"]
                interval_orar = constrangere["interval_orar"].split("-")
                ora_inceput = int(interval_orar[0].split(":")[0])
                ora_sfarsit = int(interval_orar[1].split(":")[0])

                return not (valoare["zi"] == zi_restrictionata and 
                            ora_inceput <= valoare["interval"] <= ora_sfarsit)

    return True

def respecta_constrangeri(orar, activitate, valoare, constrangeri):
    for constrangere in constrangeri:
        if constrangere["tip"] == "hard":
            if not verifica_constrangere_arc(constrangere, activitate, valoare):
                return False
    return True
