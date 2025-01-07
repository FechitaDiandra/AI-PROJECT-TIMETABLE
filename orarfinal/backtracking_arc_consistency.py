import json
from itertools import product
from collections import deque

# Load data from JSON files
with open('data/activitati.json') as f:
    activitati = json.load(f)

with open('data/sali.json') as f:
    sali = json.load(f)

with open('data/profesori.json') as f:
    profesori = json.load(f)

with open('constrains/constrangeri.json') as f:
    constrangeri = json.load(f).get("constrangeri", [])

# Separate constraints into hard and soft
hard_constraints = [c for c in constrangeri if c['tip'] == 'hard']
soft_constraints = [c for c in constrangeri if c['tip'] == 'soft']

zile = ["luni", "marti", "miercuri", "joi", "vineri"]
intervale = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]

# Initialize domains
def init_domenii(activitati, sali):
    domenii = {}
    for activitate in activitati:
        domenii[activitate["materie"]] = [
            {"sala": sala, "zi": zi, "interval": interval}
            for sala in sali
            for zi in zile
            for interval in intervale
        ]
    return domenii

def verifica_constrangere(valoare_x, valoare_y, constrangere):
    if constrangere.get("entitate") == "sala":
        if valoare_x["sala"] == constrangere["nume"] and valoare_x["zi"] == constrangere["zi"] and valoare_x["interval"] == constrangere["interval_orar"]:
            return False
    if constrangere.get("entitate") == "profesor":
        if valoare_x["zi"] == constrangere.get("zi") and valoare_x["interval"] == constrangere.get("interval_orar"):
            return False
    return True

def aplica_arc_consistency(domenii, constrangeri):
    queue = deque([(x, c) for x in domenii for c in constrangeri])
    while queue:
        (variabila, constrangere) = queue.popleft()
        domeniu_actualizat = []
        for valoare in domenii[variabila]:
            if verifica_constrangere(valoare, None, constrangere):
                domeniu_actualizat.append(valoare)
        if len(domeniu_actualizat) < len(domenii[variabila]):
            domenii[variabila] = domeniu_actualizat
            for alt_variabila in domenii:
                if alt_variabila != variabila:
                    queue.append((alt_variabila, constrangere))
    return domenii

def is_valid_allocation(activity, assignment, current_schedule):
    for scheduled in current_schedule.values():
        for sched in scheduled:
            if sched['day'] == assignment['zi'] and sched['time'] == assignment['interval'] and sched['room'] == assignment['sala']:
                return False
    return True

def backtrack_schedule(activities, domenii, current_schedule, index=0):
    if index == len(activities):
        return True

    activity = activities[index]
    materia = activity['materie']

    for assignment in domenii[materia]:
        if is_valid_allocation(activity, assignment, current_schedule):
            if activity['profesor'] not in current_schedule:
                current_schedule[activity['profesor']] = []
            current_schedule[activity['profesor']].append({
                'activity': activity,
                'day': assignment['zi'],
                'time': assignment['interval'],
                'room': assignment['sala']
            })
            if backtrack_schedule(activities, domenii, current_schedule, index + 1):
                return True
            current_schedule[activity['profesor']].pop()
    return False

# Apply Arc Consistency
domenii = init_domenii(activitati, sali)
domenii = aplica_arc_consistency(domenii, hard_constraints)

# Backtracking with reduced domains
schedule = {}
activities = sorted(activitati, key=lambda x: x['materie'])
if backtrack_schedule(activities, domenii, schedule):
    print("Orar generat cu succes!")
else:
    print("Generarea orarului a eșuat!")

for profesor, entries in schedule.items():
    print(f"Profesor: {profesor}")
    for entry in entries:
        activity = entry['activity']
        print(f"  Materie: {activity['materie']}, Tip: {activity['tip']}, Zi: {entry['day']}, Interval: {entry['time']}, Sala: {entry['room']}")
