import itertools
import random
import json

# Citirea datelor din fișierele JSON
def load_data():
    with open('data/activitati.json', 'r') as f:
        activitati = json.load(f)
    with open('data/grupe.json', 'r') as f:
        grupe = json.load(f)
    with open('data/profesori.json', 'r') as f:
        profesori = json.load(f)
    with open('data/sali.json', 'r') as f:
        sali = json.load(f)
    with open('constrains/constrangeri.json', 'r') as f:
        constrangeri = json.load(f)
    return activitati, grupe, profesori, sali, constrangeri

activitati, grupe, profesori, sali, constrangeri = load_data()

# Definirea variabilelor și domeniilor pentru problema de CSP
time_slots = [
    f"{day} {hour_start:02d}:00-{hour_end:02d}:00"
    for day in ["luni", "marți", "miercuri", "joi", "vineri"]
    for hour_start, hour_end in [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18)]
]

rooms = list(sali.keys())

# Definim variabilele ca tuple (activitate, grup, profesor)
variables = [
    (activity['materie'], group, activity['profesor'])
    for activity in activitati
    for group in grupe.keys()
]

domains = {var: random.sample(list(itertools.product(rooms, time_slots)), len(list(itertools.product(rooms, time_slots)))) for var in variables}

# Definirea funcției pentru verificarea constrângerilor
def check_constraints(assignments, new_assignment):
    materie, grup, profesor, sala, interval_orar = new_assignment

    # Verificăm dacă activitatea respectă constrângerile hard
    for assignment in assignments:
        _, _, _, assigned_room, assigned_time = assignment

        # Constrângerea de unicitate (nu pot fi două activități în aceeași sală la același timp)
        if sala == assigned_room and interval_orar == assigned_time:
            return False

        # Constrângerea ca un profesor să nu fie implicat în două activități în același timp
        if profesor == assignment[2] and interval_orar == assigned_time:
            return False

    # Verificăm restricțiile din fișierul constrangeri.json
    for constrangere in constrangeri['constrangeri']:
        if constrangere['tip'] == 'hard':
            if constrangere['entitate'] == 'profesor' and constrangere['nume'] == profesor:
                if constrangere.get('zi') and constrangere['zi'] in interval_orar and constrangere['interval_orar'] in interval_orar:
                    return False
                if not constrangere.get('zi') and constrangere['interval_orar'] in interval_orar:
                    return False
            if constrangere['entitate'] == 'sala' and constrangere['nume'] == sala:
                if constrangere.get('zi') and constrangere['zi'] in interval_orar and constrangere['interval_orar'] in interval_orar:
                    return False
                if not constrangere.get('zi') and constrangere['interval_orar'] in interval_orar:
                    return False
            if constrangere['entitate'] == 'orar' and constrangere['interval_orar'] in interval_orar:
                return False

    return True

# Funcție pentru a selecta variabila cu cele mai puține valori disponibile (MRV)
def select_unassigned_variable(assignments):
    unassigned_variables = [var for var in variables if var not in [a[:3] for a in assignments]]
    if not unassigned_variables:
        return None  # Dacă nu mai sunt variabile neasignate, înseamnă că nu există opțiuni valabile
    return min(unassigned_variables, key=lambda var: len(domains[var]))

# Funcție pentru forward checking optimizat
def forward_check(assignments, var, value):
    materie, grup, profesor = var
    sala, interval_orar = value
    for other_var in variables:
        if other_var != var and other_var not in [a[:3] for a in assignments]:
            new_domain = [
                other_value for other_value in domains[other_var]
                if check_constraints(assignments + [(materie, grup, profesor, sala, interval_orar)],
                                     (other_var[0], other_var[1], other_var[2], other_value[0], other_value[1]))
            ]
            domains[other_var] = new_domain
            if not domains[other_var]:  # Dacă nu există valori disponibile pentru other_var, ieșim din forward_check
                return False
    return True

# Funcție pentru selectarea valorii cu Least Constraining Value (LCV)
def order_domain_values(var, assignments):
    return sorted(domains[var], key=lambda val: count_conflicts(var, val, assignments))

def count_conflicts(var, value, assignments):
    # Numărăm conflictele pe care valoarea le va genera asupra celorlalte variabile neasignate
    count = 0
    materie, grup, profesor = var
    sala, interval_orar = value
    for other_var in variables:
        if other_var != var and other_var not in [a[:3] for a in assignments]:
            for other_value in domains[other_var]:
                if not check_constraints(assignments + [(materie, grup, profesor, sala, interval_orar)],
                                         (other_var[0], other_var[1], other_var[2], other_value[0], other_value[1])):
                    count += 1
    return count

# Algoritmul de backtracking cu optimizări MRV și LCV
def backtrack(assignments, depth=0):
    global domains  # declară variabila ca fiind globală

    if len(assignments) == len(variables):
        return assignments

    if depth > max_recursion_depth:
        return None

    # Selectăm următoarea variabilă neasignată folosind euristica MRV
    next_variable = select_unassigned_variable(assignments)
    if next_variable is None:
        return None  # Dacă nu mai sunt variabile disponibile, ieșim din recursie

    # Obținem valorile posibile ordonate după euristica LCV
    ordered_values = order_domain_values(next_variable, assignments)

    for value in ordered_values:
        new_assignment = (next_variable[0], next_variable[1], next_variable[2], value[0], value[1])

        if check_constraints(assignments, new_assignment):
            # Aplicăm forward checking
            import copy
            backup_domains = copy.deepcopy(domains)  # backup a domeniilor actuale

            if forward_check(assignments, next_variable, value):
                result = backtrack(assignments + [new_assignment], depth + 1)
                if result is not None:
                    return result

            # Restaurăm domeniile originale dacă nu am găsit o soluție
            domains = backup_domains

    return None

# Testarea algoritmului pe instanțele disponibile
max_recursion_depth = 1000  # Limităm adâncimea maximă de recursie pentru a evita blocarea
solution = backtrack([])

if solution:
    for assignment in solution:
        print(f"Materie: {assignment[0]}, Grup: {assignment[1]}, Profesor: {assignment[2]}, Sala: {assignment[3]}, Interval orar: {assignment[4]}")
else:
    print("Nu există nicio soluție care să satisfacă toate restricțiile.")