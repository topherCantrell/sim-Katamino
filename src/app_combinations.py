import random

import board
import pieces
import solutions_db
import solver


# n=12 pieces
#
# r=1  :  12 combinations
# r=2  :  66
# r=3  : 220
# r=4  : 495
# r=5  : 792
# r=6  : 924
# r=7  : 792
# r=8  : 495
# r=9  : 220
# r=10 :  66
# r=11 :  12
# r=12 :   1
#
# Total of 4095 (4096 = 2^12, if you count r=0)
def make_combos(pieces, num):
    """Make all possible combinations of N pieces."""
    # TODO there is a programmatic way to generate these instead of random
    ret = []
    for _ in range(100000):
        r = []
        np = pieces[:]
        for _ in range(num):
            p = random.choice(np)
            r.append(p.name)
            del np[np.index(p)]
        r = ''.join(sorted(r))
        if r not in ret:
            ret.append(r)
    return ret


def all_solveable_combos(num):
    '''Find all combinations of N pieces that have at least 1 solution'''
    c = make_combos(pieces.PIECES, num)

    for i in c:
        brd = board.new_board(num)
        sols = []
        pies = []
        for n in i:
            pies.append(pieces.get_piece_by_name(n))
        solver.solve(brd, pies, 0, sols, True)
        if sols:
            print(i)


def solve_all_combos(num):
    combos = make_combos(pieces.PIECES, num)
    with_solutions = 0
    print('Solving {total} combinations of {num}:'.format(
        total=len(combos), num=num), end='', flush=True)
    for com in combos:
        brd = board.new_board(num)
        sols = []
        pies = []
        for n in com:
            pies.append(pieces.get_piece_by_name(n))
        solver.solve(brd, pies, 0, sols)
        print('.', end='', flush=True)
        if sols:
            # print(len(sols))
            sols = solver.cull(sols)
            #print('to ' + str(len(sols)))
            solutions_db.set_solutions(com, sols)
            with_solutions += 1
        else:
            solutions_db.set_solutions(com, None)

    print()
    print('Found {total} combos with solutions.'.format(total=with_solutions))


# solve_all_combos(3)
# solve_all_combos(4)
# solve_all_combos(5)

solve_all_combos(6)

# solve_all_combos(7)
# solve_all_combos(8)
# solve_all_combos(9)
# solve_all_combos(10)
# solve_all_combos(11)
# solve_all_combos(12)
