import pieces
import random
import board

def make_combos(pieces,num):
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

c = make_combos(pieces.PIECES,3)

import solver

for i in c:
    brd = board.new_board(3,5)
    sols = []
    pies = []    
    for n in i:
        pies.append(pieces.get_piece_by_name(n))
    solver.solve(brd, pies, 0, sols, True)
    if sols:
        print(i)
    