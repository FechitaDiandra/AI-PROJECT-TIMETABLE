import re

def tokenizare(fraza):
    rezultate = {
        "profesor": None,
        "zile": [],
        "interval": [],
        "disponibilitate": None,
        "tip_curs": None,
        "doar": False,
        "maxim_ore": None,
        "curs_inainte_de_laborator": False,
        "intervale_restrictive": [],
        "zile_restrictive": [],
        "preferinte": {
            "preferinte_zile": [],
            "preferinte_interval": [],
        },
    }

    # Caută numele complet al profesorului
    nume_profesor = re.search(r'Profesorul\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)', fraza)
    if nume_profesor:
        rezultate["profesor"] = f"{nume_profesor.group(1)} {nume_profesor.group(2)}"

    # Caută zilele și intervalele
    zile_posibile = ["luni", "marți", "miercuri", "joi", "vineri"]
    intervale_posibile = ["08:00 - 10:00", "10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00", "16:00 - 18:00", "18:00 - 20:00"]
    
    for zi in zile_posibile:
        if re.search(r'\b' + zi + r'\b', fraza.lower()):
            rezultate["zile"].append(zi.capitalize())
            rezultate["preferinte"]["preferinte_zile"].append(zi.capitalize())
    
    for interval in intervale_posibile:
        if re.search(r'\b' + interval + r'\b', fraza):
            rezultate["interval"].append(interval)
            rezultate["preferinte"]["preferinte_interval"].append(interval)

    if re.search(r'\bdoar\b', fraza.lower()):
        rezultate["doar"] = True

    return rezultate

fraza_test = input("Introduceți constrângerea: ")
rezultate = tokenizare(fraza_test)
print(rezultate)
