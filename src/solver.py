import copy

import board_utils
import piece_utils

''' 

# Solving algorithms

A board is an Nx5 grid, where N is the number of pieces in the set being played.

A piece has a starting point (x,y) and a list of drawing directions to draw the piece.
For instance "start at (2,2) and go right 1, up 1, right 1, and up 1". Each piece
has several of these lists to account for rotations and flips. The shape of the piece
determines how many different drawing lists it has. The '+' shaped piece, for instance,
looks the same no matter how you rotate it or flip it. It only has 1 draw string.
Some pieces have as many as 8 draw strings: four rotations, then flip over and four
more rotations.

The brute force solver tries every combination of starting points (x,y) on the
board and every rotation of each piece at each starting point.

There are Nx5 starting points. At a max, there are 8 rotations of each piece.

(N*5*8)^N

for 1 piece: (1*5*8)^1 = 40 tries
for 2 pieces: (2*5*8)^2 = 6400 tries
 3: 1,728,000
 4: 655,360,000
 5: 3.2e11
 6: 1.9e14
 7: 1.4e17
 8: 1.1e20
 9: 1.0e23
10: 1.0e26
11: 1.2e29
12: 1.5e32

This is just the worst cases. Many pieces have fewer than 8 rotations. And we
can abort the tries when we detect that the volume of a hole in the board created by
the pieces is not a multiple of 5 (no need to try the rest of the pieces since none
will fill the hole).

'''


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
    # return True
    blanks = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 0:
                blanks.append((x, y))
    stuck_count = 0
    while blanks:
        stuck_count += 1
        if stuck_count == 500:
            raise Exception('We are stuck')
        cur_set = [blanks[0]]
        del blanks[0]
        _rec_blanks(blanks, cur_set, cur_set[0])
        if (len(cur_set) % 5) != 0:
            return False

    return True


def cull(sols):
    ret = []
    for s in sols:
        if s in ret:
            continue
        if board_utils.flip_left_right(s) in ret:
            continue
        if board_utils.flip_top_bottom(s) in ret:
            continue
        if board_utils.flip_top_bottom(board_utils.flip_left_right(s)) in ret:
            continue
        ret.append(s)
    return ret


DOTCOUNT = 0


def feedback(c):
    global DOTCOUNT
    print(c, end='', flush=True)
    DOTCOUNT += 1
    if DOTCOUNT % 25 == 0:
        print()


def solve(board, pieces, sols, index=0, stop_on_first=False, feedback_on=0):
    """Recursively try pieces to find solutions.

    Params:
       board: the board with the pieces tried so far already in place
       pieces: the entire list of pieces to try
       index: the current index in the list of pieces (next piece to try)
       sols: growing list of solutions
       stop_on_first: stop if we find a single solution
    """
    piece = pieces[index]
    for u in piece['unique']:
        for y in range(len(board)):
            for x in range(len(board[0])):
                if index == feedback_on:
                    feedback('.')
                rem = piece_utils.place_piece(
                    board, piece, x, y, u, special_origin=False)
                if not rem:
                    continue
                if index == len(pieces) - 1:
                    sols.append(copy.deepcopy(board))
                else:
                    if ok_blanks(board):
                        solve(board, pieces, sols, index +
                              1, stop_on_first, feedback_on)
                piece_utils.remove_piece(board, rem)


"""
pieces = [
    piece_utils.get_piece_by_letter('A'),
    piece_utils.get_piece_by_letter('B'),
    piece_utils.get_piece_by_letter('C'),
    piece_utils.get_piece_by_letter('D'),
    piece_utils.get_piece_by_letter('E'),
    piece_utils.get_piece_by_letter('F'),
    piece_utils.get_piece_by_letter('G'),
    piece_utils.get_piece_by_letter('H'),
    piece_utils.get_piece_by_letter('I'),
    # piece_utils.get_piece_by_letter('J'),
    # piece_utils.get_piece_by_letter('K'),
    # piece_utils.get_piece_by_letter('L'),
]

board = board_utils.new_board(len(pieces))

sols = []

solve(board, pieces, sols, feedback_on=0)
print()

sols = cull(sols)
print(sols)
"""
