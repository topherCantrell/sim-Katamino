
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

print(len(sorted_keys))
for key in sorted_keys:
    for k in key:
        if k not in 'ABCDEFGHIJKL':
            raise Exception('Invalid:' + key)
    for i in range(len(key)):
        if (len(key) > 1) and (key[i] in key[i + 1:]):
            #raise Exception('Invalidd:' + key)
            print('Invalidd:' + key)

num_sols = 0
for entry in db:
    if 'solutions' in db[entry]:
        if db[entry]['solutions']:
            num_sols += len(db[entry]['solutions'])

print('Total solution boards', num_sols)

'''
# Should be 4095 (no entry for no-pieces)
print(len(db))

for i in range(1, 13):
    combs = piece_utils.make_combos(i)
    for comb in combs:
        sols = solutions_db.get_solutions(comb)
        if sols == None:
            print(comb)
'''
