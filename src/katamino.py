"""
Katamino Simulator
"""

import copy
import datetime
import pieces


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


def new_board(width, height=5):
    """Make a new (empty) board"""
    board = []
    for _ in range(0, height):
        row = []
        for _ in range(0, width):
            row.append('.')
        board.append(row)
    return board


def write_board(board, out):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            out.write(col)
        out.write('\n')
    out.write('\n')


def print_board(board):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            print(col, end='')
        print()
    print()


def solve(board, pieces, index, out):
    """recursive solve"""
    for rot in range(8):
        if index == 0:
            print('.', end='', flush=True)
        for y in range(len(board)):
            for x in range(len(board[0])):
                piece = pieces[index]
                if not piece.can_place(board, x, y, rot):
                    continue
                piece.place(board, x, y, rot)
                if index == (len(pieces) - 1):
                    write_board(board, out)
                    out.flush()
                else:
                    if ok_blanks(board):
                        solve(board, pieces, index + 1, out)
                piece.remove(board, x, y, rot)


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
                board = new_board(len(pcs))
                s = str(num) + ': '
                for p in pcs:
                    s = s + p.name
                print(s, end='')
                out.write(s + '\n')
                now = datetime.datetime.now()
                solve(board, pcs, 0, out)
                after = datetime.datetime.now()

                print((after - now).seconds)
                pos += 1


if __name__ == '__main__':
    main()
