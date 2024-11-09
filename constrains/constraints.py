
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


def limite_zilnice_profesori(orar, profesori, max_activitati_pe_zi=3):
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

def intervale_interzise_profesori(orar, profesori):
    for activitate, detalii in orar.items():
        zi, interval, sala = detalii
        profesor = activitati[activitate]["profesor"]
        if zi in profesori[profesor]["restrictii"]:
            return False  # Incalcare restrictie interval
    return True  # Restrictiile sunt respectate