"""
Manage piece solutions over the life of the experiment.
"""
import json

# Format of DB json file

"""
{
  'challenges': ['Small Slam:A'], 
  'solutions': [[[1, 1, 8], [1, 8, 8], [1, 7, 8], [1, 7, 8], [7, 7, 7]]]
}
"""

# List of solutions is missing if it hasn't been tried/completed.
# List of solutions is empty [] if it has been tried and there are no solutions.
# Challenges is missing if it hasn't been determined.
# Challenges is empty [] if the combination is not used in a challenge.

with open('solutions.js') as db_file:
    SOLUTION_DB = json.load(db_file)


def get_solutions_for_challenge(challenge):
    ret = {}
    for key in SOLUTION_DB:
        entry = SOLUTION_DB[key]
        if 'challenges' in entry:
            for chal in entry['challenges']:
                if ':' in challenge:
                    b = chal == challenge
                else:
                    b = chal.startswith(challenge + ':')
                if b:
                    for r in entry['solutions']:
                        if len(r) == 5 or len(r[0]) == 5:
                            if chal not in ret:
                                ret[chal] = []
                            ret[chal].append(r)

    return ret


def get_solutions_for_board_size(width, height):
    ret = []
    if width < height:
        bs = [width, height]
    else:
        bs = [height, width]
    bs = str(bs)
    for key in SOLUTION_DB:
        entry = SOLUTION_DB[key]
        if 'solutions' in entry and entry['solutions']:
            for sol in entry['solutions']:
                width = len(sol[0])
                height = len(sol)
                if width < height:
                    tbs = [width, height]
                else:
                    tbs = [height, width]
                k = str(tbs)
                if k == bs:
                    ret.append(sol)
    return ret


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


def add_solutions(comb, sols):
    """Add solutions to the existing solutions for the given piece combination"""
    comb = ''.join(sorted(comb))
    if (comb in SOLUTION_DB) and ('solutions' in SOLUTION_DB[comb]) and (SOLUTION_DB[comb]['solutions'] != None):
        sols_org = SOLUTION_DB[comb]['solutions']
        # TODO we need an "in" function here that tries mirrors and rotates
        for sol in sols:
            if not sol in sols_org:
                sols_org.append(sol)
        _write_db()
    else:
        # No existing solutions ... these are new
        force_set_solutions(comb, sols)


def force_set_solutions(comb, sols):
    comb = ''.join(sorted(comb))
    ensure_combination(comb)
    SOLUTION_DB[comb]['solutions'] = sols
    _write_db()


def set_solutions(comb, sols):
    """Set the solutions for the given piece combination"""
    comb = ''.join(sorted(comb))
    if comb in SOLUTION_DB and 'solutions' in SOLUTION_DB[comb]:
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
