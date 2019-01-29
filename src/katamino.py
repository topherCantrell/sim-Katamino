"""
Katamino Simulator
"""

import copy

PIECES = [
    {'name':'A', 'pattern':'UUUR', 'color':'248 115 50'},
    {'name':'B', 'pattern':'RURU', 'color':'112 90 69'},
    {'name':'C', 'pattern':'URRD', 'color':'223 207 59'},
    {'name':'D', 'pattern':'RRDR', 'color':'61 35 112'},
    {'name':'E', 'pattern':'RRUL', 'color':'218 108 52'},
    {'name':'F', 'pattern':'LUUL', 'color':'31 183 223'},
    {'name':'G', 'pattern':'RRlDD', 'color':'32 148 52'},
    {'name':'H', 'pattern':'RUdRR', 'color':'121 68 50'},
    {'name':'I', 'pattern':'RRRR', 'color':'82 125 175'},
    {'name':'J', 'pattern':'DDuLrR', 'color':'244 70 39'},
    {'name':'K', 'pattern':'LULrU', 'color':'11 115 104'},
    {'name':'L', 'pattern':'RRDD', 'color':'19 148 191'},
]


def make_sequence(seq):
    ret = []
    for piece in seq:
        ret.append(get_piece_by_name(piece))
    return ret


def get_piece_by_name(name):
    """Find the given piece"""
    for piece in PIECES:
        if piece['name'] == name:
            return piece
    return None


def new_board(width, height=5):
    """Make a new (empty) board"""
    board = []
    for _ in range(0, height):
        row = []
        for _ in range(0, width):
            row.append('.')
        board.append(row)
    return board


def print_board(board):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            print(col, end='')
        print()
    print()


ROTS = [
    {'U':[0, -1], 'R':[1, 0], 'D':[ 0, 1], 'L':[-1, 0], },
    {'U':[1, 0], 'R':[0, 1], 'D':[-1, 0], 'L':[ 0, -1], },
    {'U':[0, 1], 'R':[-1, 0], 'D':[ 0, -1], 'L':[1, 0], },
    {'U':[-1, 0], 'R':[0, -1], 'D':[1, 0], 'L':[ 0, 1], },
    {'U':[0, 1], 'R':[1, 0], 'D':[ 0, -1], 'L':[-1, 0], },
    {'U':[1, 0], 'R':[0, -1], 'D':[-1, 0], 'L':[ 0, 1], },
    {'U':[0, -1], 'R':[-1, 0], 'D':[ 0, 1], 'L':[1, 0], },
    {'U':[-1, 0], 'R':[0, 1], 'D':[1, 0], 'L':[ 0, -1], },
]


def place_piece(board, x_start, y_start, piece, rotation):
    """Attempt to place a piece on the board"""
    if board[y_start][x_start] != '.':
        return False
    board[y_start][x_start] = piece['name']
    rot = ROTS[rotation]
    for direction in piece['pattern']:
        dir_no_case = direction.upper()
        ofs = rot[dir_no_case]
        y_start += ofs[1]
        x_start += ofs[0]
        if x_start < 0 or x_start >= len(board[0]) or y_start < 0 or y_start >= len(board):
            return False
        if dir_no_case == direction:
            if board[y_start][x_start] != '.':
                return False
            board[y_start][x_start] = piece['name']
    return True


def solve(board, pieces, index):
    """recursive solve"""
    for rot in range(8):
        if index == 0:
            print('.', end='', flush=True)
        for y in range(len(board)):
            for x in range(len(board[0])):
                tb = copy.deepcopy(board)
                if not place_piece(tb, x, y, pieces[index], rot):
                    continue
                if index == (len(pieces) - 1):
                    print_board(tb)
                    return True
                sol = solve(tb, pieces, index + 1)
                # if sol:
                #    return True
    return False


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
    
    # pieces = make_sequence('AHGEBFL')
    pieces = make_sequence('AHGEB')   
    board = new_board(len(pieces))
    solve(board, pieces, 0)


if __name__ == '__main__':
    main()
