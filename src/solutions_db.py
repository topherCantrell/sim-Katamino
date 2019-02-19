"""
Manage piece solutions over the life of the experiment.
"""
import json

# Format of DB json file

# List of solutions is missing if it hasn't been tried/completed.
# List of solutions is empty [] if it has been tried and there are no solutions.
# Challenges is missing if it hasn't been determined.
# Challenges is empty [] if the combination is not used in a challenge.

with open('solutions.js') as db_file:
    SOLUTION_DB = json.load(db_file)


def _write_db():
    with open('solutions.js', 'w') as db_up_file:
        json.dump(SOLUTION_DB, db_up_file, indent=4)


def get_solutions(comb):
    """Get the solutions/challenges for the given piece combination"""
    comb = ''.join(sorted(comb))
    if comb not in SOLUTION_DB:
        return None
    return SOLUTION_DB[comb]


def ensure_combination(comb):
    """Make sure the combination has an entry in the DB"""
    comb = ''.join(sorted(comb))
    if comb not in SOLUTION_DB:
        SOLUTION_DB[comb] = {}


def set_solutions(comb, sols):
    """Set the solutions for the given piece combination"""
    comb = ''.join(sorted(comb))
    if comb in SOLUTION_DB:
        if sols:
            sols.sort()
        sols_org = SOLUTION_DB[comb]['solutions']
        if sols_org:
            sols_org.sort()
        if sols != sols_org:
            print(sols)
            print(sols_org)
            raise Exception('SOLVER MISMATCH')
    else:
        ensure_combination(comb)
        SOLUTION_DB[comb]['solutions'] = sols
        _write_db()


def add_challenge(comb, chal):
    """Set the challenges for the given piece combination"""
    comb = ''.join(sorted(comb))
    ensure_combination(comb)
    if 'challenges' not in SOLUTION_DB[comb]:
        SOLUTION_DB[comb]['challenges'] = []
    SOLUTION_DB[comb]['challenges'].append(chal)
    _write_db()
