
import json

with open('constrains/constrangeri.json', 'r') as file:
    constraints = json.load(file)["constrangeri"]

with open('data/activitati.json', 'r') as file:
    activities = json.load(file)

with open('data/sali.json', 'r') as file:
    rooms = json.load(file)

with open('data/profesori.json', 'r') as file:
    professors = json.load(file)

with open('data/grupe.json', 'r') as file:
    groups = json.load(file)


def is_consistent(var, value, assignment, constraints, domains, activity_ids):
    """
    Check if assigning `value` to `var` (identified by ID) is consistent with constraints and current assignment.
    """
    activity = activity_ids[var]  # Retrieve the actual activity using the ID
    for constraint in constraints:
        if constraint["entitate"] == "profesor" and constraint["nume"] == activity["profesor"]:
            if "zi" in constraint and value["zi"] != constraint["zi"]:
                return False
            if "interval_orar" in constraint and value["interval"] not in constraint["interval_orar"]:
                return False

        if constraint["entitate"] == "sala" and constraint["nume"] == value["sala"]:
            if "zi" in constraint and value["zi"] == constraint["zi"]:
                if "interval_orar" in constraint and value["interval"] in constraint["interval_orar"]:
                    return False

    return True


def arc_consistency(variables, domains, constraints, activity_ids):
    """
    Apply Arc Consistency to reduce the domain of variables based on constraints.
    """
    queue = [(xi, xj) for xi in variables for xj in variables if xi != xj]

    while queue:
        xi, xj = queue.pop(0)
        if revise(xi, xj, domains, constraints, activity_ids):
            if not domains[xi]:
                return False
            for xk in variables:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))

    return True


def revise(xi, xj, domains, constraints, activity_ids):
    """
    Revise the domain of xi to ensure consistency with xj.
    """
    revised = False
    for x in domains[xi][:]:
        if not any(is_consistent(xi, x, {xj: y}, constraints, domains, activity_ids) for y in domains[xj]):
            domains[xi].remove(x)
            revised = True

    return revised


def backtracking_with_arc_consistency(variables, domains, constraints, activity_ids):
    """
    Backtracking search integrated with Arc Consistency.
    """

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment

        var = select_unassigned_variable(variables, assignment, domains)
        for value in domains[var]:
            if is_consistent(var, value, assignment, constraints, domains, activity_ids):
                assignment[var] = value
                local_domains = {v: list(domains[v]) for v in domains}
                if arc_consistency(variables, domains, constraints, activity_ids):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                domains.update(local_domains)
                assignment.pop(var)

        return None

    if not arc_consistency(variables, domains, constraints, activity_ids):
        return None

    return backtrack({})


def select_unassigned_variable(variables, assignment, domains):
    """
    Select the next unassigned variable using the Minimum Remaining Values (MRV) heuristic.
    """
    unassigned = [var for var in variables if var not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))

activity_ids = {idx: activity for idx, activity in enumerate(activities)}


domains = {
    idx: [{"zi": zi, "interval": interval, "sala": sala}
          for zi in ["luni", "marti", "miercuri", "joi", "vineri"]
          for interval in ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00"]
          for sala in rooms]
    for idx in activity_ids
}

print("Initial domains:")
for key, value in domains.items():
    print(f"Activity {key}: {value}")

print("\nConstraints:")
for constraint in constraints:
    print(constraint)

solution = backtracking_with_arc_consistency(list(activity_ids.keys()), domains, constraints, activity_ids)

mapped_solution = {
    idx: {
        "activity": activity_ids[idx],
        "allocation": value
    } for idx, value in solution.items()
} if solution else None

if mapped_solution:
    print("\nSolution found:")
    for activity_id, allocation in mapped_solution.items():
        print(f"{activity_id}: {allocation}")
else:
    print("\nNo solution found. Check constraints and domain definitions.")

solution_path = 'final_solution.json'
with open(solution_path, 'w') as file:
    json.dump(mapped_solution, file, indent=4)

print(f"\nSolution saved to {solution_path}")
if mapped_solution:
    schedule = {}
    for idx, allocation in mapped_solution.items():
        activity = allocation["activity"]
        professor = activity["profesor"]
        if professor not in schedule:
            schedule[professor] = []
        schedule[professor].append({
            "activity": activity,
            "day": allocation["allocation"]["zi"],
            "time": allocation["allocation"]["interval"],
            "room": allocation["allocation"]["sala"]
        })

    for professor, entries in schedule.items():
        print(f"Profesor: {professor}")
        for entry in entries:
            activity = entry['activity']
            print(f"  Materie: {activity['materie']}, Tip: {activity['tip']}, Zi: {entry['day']}, Interval: {entry['time']}, Sala: {entry['room']}")
else:
    print("Nu s-a găsit nicio soluție.")