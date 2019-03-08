import random

import board_utils
import piece_utils
import solutions_db
import solver

"""
pieces = [
    piece_utils.get_piece_by_letter('A'),
    piece_utils.get_piece_by_letter('H'),
    piece_utils.get_piece_by_letter('G'),
    piece_utils.get_piece_by_letter('E'),
    piece_utils.get_piece_by_letter('B'),
    piece_utils.get_piece_by_letter('F'),
    piece_utils.get_piece_by_letter('L'),
    # piece_utils.get_piece_by_letter('D'),
]

board = board_utils.new_board(len(pieces))

sols = []

solve(board, pieces, sols)
print()

sols = cull(sols)
print(sols)
"""


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
            r.append(p['name'])
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
    combos = make_combos(piece_utils.PIECES, num)
    with_solutions = 0
    dotcnt = 0
    print('Solving {total} combinations of {num}:'.format(
        total=len(combos), num=num), end='', flush=True)
    for com in combos:
        brd = board_utils.new_board(num)
        sols = []
        pies = []
        for n in com:
            pies.append(piece_utils.get_piece_by_letter(n))
        solver.feedback('#')
        solver.solve(brd, pies, sols)
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

def solve_all_combos_multi(num):
    combos = make_combos(piece_utils.PIECES, num)
    combos.sort()    
    print('Solving {total} combinations of {num}:'.format(
        total=len(combos), num=num))
    boards_with_solutions = []
    for com in combos:        
        for bd in board_utils.BOARDS_FOR_PIECES[num]:
            with_solutions = 0
            print('---------- Board',bd,com,'----------')
            brd = board_utils.new_board(bd[0],bd[1])
            sols = []
            pies = []
            for n in com:
                pies.append(piece_utils.get_piece_by_letter(n))
            solver.feedback('#')
            solver.solve(brd, pies, sols)        
            if sols:
                sols = solver.cull(sols)
                #solutions_db.set_solutions(com, sols)
                with_solutions += 1
            else:
                #solutions_db.set_solutions(com, None)
                pass

            print()
            print('Found {total} combos with solutions.'.format(total=with_solutions))
            if with_solutions:
                if bd not in boards_with_solutions:
                    boards_with_solutions.append(bd)
        print()
    print('Boards with solutions',boards_with_solutions)

#solve_all_combos_multi(1) # [1,5]
#solve_all_combos_multi(2) # (No solutions)
#solve_all_combos_multi(3) # [3, 5]
#solve_all_combos_multi(4) # [4, 5], [2, 10]
#solve_all_combos_multi(5) # [5,5]
#solve_all_combos_multi(6) # [6, 5], [3, 10]
#solve_all_combos_multi(7) # [7, 5]
solve_all_combos_multi(8)
# solve_all_combos_multi(9)
# solve_all_combos_multi(10)
# solve_all_combos_multi(11)
# ? solve_all_combos_multi(12)
