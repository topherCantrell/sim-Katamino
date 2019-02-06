"""
Manage piece solutions over the life of the experiment.
"""
import json

# Format of DB json file

# List of solutions is missing if it hasn't been tried/completed.
# List of solutions is empty [] if it has been tried and there are no solutions.
# Challenges is missing if it hasn't been determined.
# Challenges is empty [] if the combination is not used in a challenge.

'''
{

    'ABC' : {
        'challenges' : ['slam 1,ultimate 2'],
        'solutions' : [
            {
                'solver_version' : '1.22',
                'solve_time' : '24',
                'board','AAA......'
            },
            {}
    },

    'ADFL' : {
    },

}
'''

with open('solutions.js') as db_file:
    SOLUTION_DB = json.load(db_file)


def _write_db():
    with open('solutions.js', 'w') as db_up_file:
        json.dump(SOLUTION_DB, db_up_file, indent=4)


def get_solutions(comb):
    """Get the solutions/challenges for the given piece combination"""
    if comb not in SOLUTION_DB:
        return None
    return SOLUTION_DB[comb]


def add_solution(comb, board, solver_version, solve_time):
    """Set the solutions for the given piece combination"""
    if comb not in SOLUTION_DB:
        SOLUTION_DB[comb] = {'solutions': []}
    SOLUTION_DB[comb]['solution'].append(
        {'solver_version': solver_version, 'solve_time': solve_time, 'board': board})


def set_challenges(comb, chals):
    """Set the challenges for the given piece combination"""
    if comb not in SOLUTION_DB:
        SOLUTION_DB[comb] = {'challenges': chals}
    else:
        SOLUTION_DB[comb]['challenges'] = chals
    _write_db()
