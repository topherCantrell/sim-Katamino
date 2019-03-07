import solutions_db

cnts = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 0,
    '8': 0,
    '9': 0,
    '10': 0,
    '11': 0,
    '12': 0,
}
for sol in solutions_db.SOLUTION_DB:
    if 'solutions' in solutions_db.SOLUTION_DB[sol] and solutions_db.SOLUTION_DB[sol]['solutions']:
        cnts[str(len(sol))] += 1

print(cnts)

total = 0
for c in cnts:
    total += cnts[c]

print(total)

# TODO sort_by_slam
# TODO sort_by_combos
