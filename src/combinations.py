import random

import board
import pieces
import solver


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

# Find all combinations of N pieces that have at least 1 solution


c = make_combos(pieces.PIECES, 5)

for i in c:
    brd = board.new_board(5)
    sols = []
    pies = []
    for n in i:
        pies.append(pieces.get_piece_by_name(n))
    solver.solve(brd, pies, 0, sols, True)
    if sols:
        print(i)
