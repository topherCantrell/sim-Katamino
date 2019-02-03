"""
Katamino Simulator
"""

import copy
import datetime
import pieces
import board


def _rec_blanks(blanks, cur_set, current):
    test_cell = (current[0] + 1, current[1])
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)
    test_cell = (current[0] - 1, current[1])
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)
    test_cell = (current[0], current[1] + 1)
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)
    test_cell = (current[0], current[1] - 1)
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)


def ok_blanks(board):
    blanks = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == '.':
                blanks.append((x, y))
    while blanks:
        cur_set = [blanks[0]]
        del blanks[0]
        _rec_blanks(blanks, cur_set, cur_set[0])
        if len(cur_set) < 5:
            return False

    return True


def solve(brd, pieces, index, out):
    """recursive solve"""
    for rot in range(8):
        if index == 0:
            print('.', end='', flush=True)
        for y in range(len(brd)):
            for x in range(len(brd[0])):
                piece = pieces[index]
                if not piece.can_place(brd, x, y, rot):
                    continue
                piece.place(brd, x, y, rot)
                if index == (len(pieces) - 1):
                    board.write_board(brd, out)
                    out.flush()
                else:
                    if ok_blanks(brd):
                        solve(brd, pieces, index + 1, out)
                piece.remove(brd, x, y, rot)


SMALL_SLAM_3 = [
    'AHGEBFLD',
    'DECAFHGB',
    'ALEHDCFK',
    'HECDLKBG',
    'ADLFCGHB',
    'ECKHGDAB',
    'ALEFHBDK'
]


def main():
    """main"""

    with open('results.txt', 'w') as out:
        num = 0
        for sequence in SMALL_SLAM_3:
            num = num + 1
            pcs = []
            for pos in range(2):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
            pos += 1
            while pos < len(sequence):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
                brd = board.new_board(len(pcs))
                s = str(num) + ': '
                for p in pcs:
                    s = s + p.name
                print(s, end='')
                out.write(s + '\n')
                now = datetime.datetime.now()
                solve(brd, pcs, 0, out)
                after = datetime.datetime.now()

                print((after - now).seconds)
                pos += 1


if __name__ == '__main__':
    main()
