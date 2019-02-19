import copy

import board_utils
import piece_utils


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
            if board[y][x] == 0:
                blanks.append((x, y))
    while blanks:
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
                    print('.', end='', flush=True)
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
