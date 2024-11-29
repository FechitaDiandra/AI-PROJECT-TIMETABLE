import json
from itertools import product

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

curs_inaintea_laboratorului = any(
    c['entitate'] == 'activitate' and c.get('regula') == 'curs_inaintea_laboratorului'
    for c in hard_constraints
)

def is_valid_allocation(activity, day, time, room, current_schedule):
    # Step 1: Verify global hard constraints
    if activity['tip'] == 'laborator' and curs_inaintea_laboratorului:
        materie = activity['materie']
        cursuri_programate = [
            sched for sched in current_schedule.values() for sched in sched
            if sched['activity']['materie'] == materie and sched['activity']['tip'] == 'curs'
        ]
        if not cursuri_programate:
            print(f"Eșec: Nu există curs programat pentru {activity['materie']} înainte de laborator.")
            return False
        for curs in cursuri_programate:
            curs_time_index = intervale.index(curs['time'])
            lab_time_index = intervale.index(time)
            curs_day = zile.index(curs['day'])
            lab_day = zile.index(day)
            if lab_day < curs_day or (lab_day == curs_day and lab_time_index <= curs_time_index):
                print(f"Eșec: Laboratorul {activity['materie']} nu poate fi programat înaintea cursului.")
                return False

    for constraint in hard_constraints:
        # Step 2: Check room restrictions
        if constraint['nivel'] == 'global' and constraint['entitate'] == 'sala':
            if room == constraint['nume'] and constraint.get('zi') == day and constraint['interval_orar'] == time:
                print(f"Eșec: Sala {room} este restricționată global în {day} la {time}.")
                return False
        # Step 3: Check professor availability
        if constraint['nivel'] == 'local' and constraint['entitate'] == 'profesor' and activity['profesor'] == constraint['nume']:
            if 'zile_indisponibile' in constraint and day in constraint['zile_indisponibile']:
                print(f"Eșec: {activity['materie']} nu poate fi programată pentru {activity['profesor']} în {day}, zi indisponibilă.")
                return False
            if constraint.get('zi') == day and constraint['interval_orar'] == time:
                print(f"Eșec: {activity['materie']} nu poate fi programată pentru {activity['profesor']} în {day} la {time}.")
                return False
        # Step 4: Check room restrictions specific to activity type
        if constraint['nivel'] == 'local' and constraint['entitate'] == 'sala' and room == constraint['nume']:
            if 'restrictie' in constraint and constraint['restrictie'] == activity['tip']:
                print(f"Eșec: {activity['materie']} ({activity['tip']}) nu poate fi programată în sala {room}.")
                return False

    # Step 5: Check room capacity
    required_capacity = 3 if activity['tip'] == 'curs' else 1
    if sali[room]['capacitate'] < required_capacity:
        print(f"Eșec: Sala {room} nu are capacitate suficientă pentru {activity['materie']} ({activity['tip']}).")
        return False

    # Step 6: Check if room is already booked
    for scheduled in current_schedule.values():
        for scheduled_activity in scheduled:
            if scheduled_activity['day'] == day and scheduled_activity['time'] == time and scheduled_activity['room'] == room:
                print(f"Eșec: Sala {room} este deja rezervată în {day} la {time}.")
                return False

    return True

def score_soft_constraints(activity, day, time, room):
    score = 0
    for constraint in soft_constraints:
        if constraint['nivel'] == 'local' and constraint['entitate'] == 'profesor' and activity['profesor'] == constraint['nume']:
            if constraint.get('zi') == day or constraint.get('interval_orar') == time:
                score += 1
        if constraint['nivel'] == 'local' and constraint['entitate'] == 'sala' and room == constraint['nume']:
            if constraint.get('zi') == day or constraint.get('interval_orar') == time:
                score += 1
    return score

def backtrack_schedule(activities, current_schedule, index=0):
    if index == len(activities):
        return True
    activity = activities[index]
    best_score = -1
    best_option = None
    for day, time, room in product(zile, intervale, sali.keys()):
        if is_valid_allocation(activity, day, time, room, current_schedule):
            score = score_soft_constraints(activity, day, time, room)
            if score > best_score:
                best_score = score
                best_option = (day, time, room)
    if best_option:
        day, time, room = best_option
        if activity['profesor'] not in current_schedule:
            current_schedule[activity['profesor']] = []
        current_schedule[activity['profesor']].append({
            'activity': activity,
            'day': day,
            'time': time,
            'room': room
        })
        if backtrack_schedule(activities, current_schedule, index + 1):
            return True
        current_schedule[activity['profesor']].pop()
    return False

schedule = {}
activities = sorted(activitati, key=lambda x: x['materie'])
if backtrack_schedule(activities, schedule):
    print("Orar generat cu succes!")
else:
    print("Generarea orarului a eșuat!")

for profesor, entries in schedule.items():
    print(f"Profesor: {profesor}")
    for entry in entries:
        activity = entry['activity']
        print(f"  Materie: {activity['materie']}, Tip: {activity['tip']}, Zi: {entry['day']}, Interval: {entry['time']}, Sala: {entry['room']}")
