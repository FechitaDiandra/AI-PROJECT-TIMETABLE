import json
import random

# Datele de intrare
profesori = ["Prof. Popescu", "Prof. Ionescu", "Prof. Vasile", "Prof. Maria"]
grupe = ["Grupa A", "Grupa B", "Grupa C", "Grupa D"]
materii = ["Matematica", "Fizica", "Informatica", "Chimie"]
sali = ["Sala 1", "Sala 2", "Sala 3", "Sala 4"]

# Citim constrângerile
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

# Toate zilele săptămânii și intervalele
zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
intervale = ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]

# Funcția care verifică constrângerile și alocă profesorilor intervale
def aplica_constrangeri(hard, soft, zi, interval, profesor=None):
    for constr in hard:
        if constr["nivel"] == "local" and constr["entitate"] == "profesor":
            if profesor == constr["nume"] and zi == constr["zi"] and interval == constr["interval_orar"]:
                return False  # Interval indisponibil
        elif constr["nivel"] == "global" and constr["entitate"] == "orar":
            if interval == constr["interval_orar"]:
                return False  # Interval indisponibil global
    for constr in soft:
        if constr["nivel"] == "global" and constr["interval_orar"] == interval:
            print("Avertisment: se evită preferabil intervalul soft:", interval)
    return True  # Interval disponibil

# Generăm orarul
def genereaza_orar(profesori, grupele, materii, sali, hard, soft):
    orar = {}
    for zi in zile:
        orar[zi] = {}
        for interval in intervale:
            # Alegem un profesor, grupă, materie și sală aleatoriu
            profesor = random.choice(profesori)
            grupa = random.choice(grupe)
            materie = random.choice(materii)
            sala = random.choice(sali)

            # Verificăm dacă intervalul este disponibil
            if aplica_constrangeri(hard, soft, zi, interval, profesor):
                orar[zi][interval] = {
                    "profesor": profesor,
                    "grupa": grupa,
                    "materie": materie,
                    "sala": sala
                }
            else:
                orar[zi][interval] = {
                    "profesor": "N/A",
                    "grupa": "N/A",
                    "materie": "N/A",
                    "sala": "N/A"
                }
    return orar

# Citim constrângerile
constrangeri = citeste_constrangeri(fisier_constrangeri)
hard, soft = clasifica_constrangeri(constrangeri)

# Generăm orarul
orar = genereaza_orar(profesori, grupe, materii, sali, hard, soft)

# Afișăm orarul generat
for zi, intervale_orar in orar.items():
    print(f"Orar pentru {zi}:")
    for interval, detalii in intervale_orar.items():
        print(f"  {interval}: {detalii}")
