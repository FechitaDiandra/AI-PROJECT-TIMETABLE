#model
import json

fisier_constrangeri = '/Users/denisroca/Downloads/Facultate/AI-PROJECT-TIMETABLE/constrains/constrangeri.json'

def citeste_constrangeri(fisier_constrangeri):
    try:
        with open(fisier_constrangeri, 'r') as f:
            date = json.load(f)
        return date["constrangeri"]
    except json.JSONDecodeError as e:
        print("Eroare la citirea JSON:", e)
        return []
    except FileNotFoundError:
        print("Fișierul nu a fost găsit:", fisier_constrangeri)
        return []
    
def clasifica_constrangeri(constrangeri):
    hard = []
    soft = []
    for c in constrangeri:
        if c["tip"] == "hard":
            hard.append(c)
        elif c["tip"] == "soft":
            soft.append(c)
    return hard, soft

def aplica_constrangeri(hard, soft, zi, interval, profesor=None):
    # Verificăm întâi constrângerile hard
    for constr in hard:
        if constr["nivel"] == "local" and constr["entitate"] == "profesor":
            if profesor == constr["nume"] and zi == constr["zi"] and interval == constr["interval_orar"]:
                return False  # Interval indisponibil
        elif constr["nivel"] == "global" and constr["entitate"] == "orar":
            if interval == constr["interval_orar"]:
                return False  # Interval indisponibil global

    # Aplicăm constrângerile soft (acestea sunt recomandări, deci poate să rămână True)
    for constr in soft:
        if constr["nivel"] == "global" and constr["interval_orar"] == interval:
            print("Avertisment: se evită preferabil intervalul soft:", interval)
    return True  # Interval disponibil

# Toate zilele săptămânii și intervalele
zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]

# Citim constrângerile
constrangeri = citeste_constrangeri(fisier_constrangeri)
hard, soft = clasifica_constrangeri(constrangeri)

# Testăm pentru fiecare zi și interval orar
for zi in zile:
    for interval in intervale:
        print(f"Verificăm pentru ziua {zi} și intervalul {interval}:")
        profesor = "Prof. Popescu"  # Exemplu de profesor
        if aplica_constrangeri(hard, soft, zi, interval, profesor):
            print(f"Interval {interval} este disponibil pentru alocare.\n")
        else:
            print(f"Interval {interval} este indisponibil, se aplică o constrângere hard.\n")
