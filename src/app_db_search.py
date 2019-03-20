
import board_utils
import piece_utils
import solutions_db


db = solutions_db.SOLUTION_DB

sorted_keys = []
for entry in db:
    sorted_entry = ''.join(sorted(entry))
    if sorted_entry in sorted_keys:
        raise Exception('Duplicates:' + entry + ',' + sorted_entry)
    else:
        sorted_keys.append(sorted_entry)


def get_total_solution_boards():
    num_sols = 0
    for entry in db:
        if 'solutions' in db[entry]:
            if db[entry]['solutions']:
                num_sols += len(db[entry]['solutions'])
    print(num_sols, 'total solution boards')


def find_remove_invalid_combos():
    # The manual has a mistake it resulting in 3 combinations
    # with double "D" pieces.
    invalids = []
    for key in sorted_keys:
        for k in key:
            if k not in 'ABCDEFGHIJKL':
                raise Exception('Invalid:' + key)
        for i in range(len(key)):
            if (len(key) > 1) and (key[i] in key[i + 1:]):
                #raise Exception('Invalidd:' + key)
                invalids.append(key)

    print("Invalid combinations", invalids)
    for comb in invalids:
        del db[comb]
    solutions_db._write_db()


def clean_challenges():
    for key in db:
        entry = db[key]
        if 'challenges' in entry:
            print(key, entry['challenges'])
            nc = []
            for ch in entry['challenges']:
                if ch not in nc:
                    nc.append(ch)
            entry['challenges'] = nc
    solutions_db._write_db()


def verify_all_combinations_have_been_tried():
    print('There are', len(sorted_keys),
          'combinations recorded in the database. There should be 4095 (no-pieces would be the 4096th).')
    if len(db) != len(sorted_keys):
        raise Exception('DB has ' + len(db) + ' entries.')
    not_tried = []
    with_solutions = []
    without_solutions = []
    for key in db:
        entry = db[key]
        if 'solutions' not in entry:
            not_tried.append(key)
        elif entry['solutions']:
            with_solutions.append(key)
        else:
            without_solutions.append(key)

    print(len(with_solutions), 'combinations with solutions')
    print(len(without_solutions), 'combinations without solutions')

    if(not_tried):
        raise Exception(
            'These combinations have not been tried ' + str(not_tried))


def get_solutions_for_board_sizes():
    known_sizes = {}
    for brds in board_utils.BOARDS_FOR_PIECES:
        for brd in brds:
            known_sizes[str(brd)] = 0

    tried = []
    for key in db:
        entry = db[key]
        if 'solutions' in entry and entry['solutions']:
            for sol in entry['solutions']:
                width = len(sol[0])
                height = len(sol)
                if width < height:
                    bs = [width, height]
                else:
                    bs = [height, width]
                k = str(bs)
                known_sizes[k] += 1
                if k not in tried:
                    tried.append(k)

    print('Solution counts', known_sizes)

    nosols = []
    total_sols = 0
    for key in known_sizes:
        if known_sizes[key] == 0:
            nosols.append(key)
        total_sols += known_sizes[key]

    print('Boards with no solutions', nosols)
    print('Total solutions (cross check)', total_sols)


# clean_challenges()
# find_remove_invalid_combos()
verify_all_combinations_have_been_tried()
get_total_solution_boards()
get_solutions_for_board_sizes()

sols = solutions_db.get_solutions_for_board_size(3, 20)
print(sols)

#print(solutions_db.get_solutions_for_challenge('Ultimate Challenges 4:No3'))
